from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import CurrentUser
from app.models.product_variant import ProductVariant
from app.models.stock_movement import StockMovement
from app.schemas.stock_movement import (
    StockMovementCreate,
    StockMovementListItemResponse,
    StockMovementResponse,
)
from app.models.product import Product

router = APIRouter(
    prefix="/stock-movements",
    tags=["Stock Movements"],
)

DatabaseSession = Annotated[Session, Depends(get_db)]


def get_current_stock(
    database: Session,
    product_variant_id: int,
    company_id: int,
) -> int:
    balance = database.scalar(
        select(
            func.coalesce(
                func.sum(
                    case(
                        (
                            StockMovement.movement_type == "ENTRY",
                            StockMovement.quantity,
                        ),
                        else_=-StockMovement.quantity,
                    )
                ),
                0,
            )
        ).where(
            StockMovement.product_variant_id == product_variant_id,
            StockMovement.company_id == company_id,
        )
    )

    return int(balance or 0)

@router.get(
    "",
    response_model=list[StockMovementListItemResponse],
)
def list_stock_movements(
    database: DatabaseSession,
    current_user: CurrentUser,
):
    rows = database.execute(
        select(
            StockMovement.id,
            StockMovement.product_variant_id,
            ProductVariant.sku,
            Product.name.label("product_name"),
            ProductVariant.color,
            ProductVariant.size,
            StockMovement.movement_type,
            StockMovement.quantity,
            StockMovement.notes,
            StockMovement.created_at,
        )
        .join(
            ProductVariant,
            ProductVariant.id
            == StockMovement.product_variant_id,
        )
        .join(
            Product,
            Product.id == ProductVariant.product_id,
        )
        .where(
            StockMovement.company_id
            == current_user.company_id,
        )
        .order_by(
            StockMovement.created_at.desc(),
            StockMovement.id.desc(),
        )
    ).all()

    return [
        StockMovementListItemResponse(
            id=row.id,
            product_variant_id=row.product_variant_id,
            sku=row.sku,
            product_name=row.product_name,
            color=row.color,
            size=row.size,
            movement_type=row.movement_type,
            quantity=row.quantity,
            notes=row.notes,
            created_at=row.created_at,
        )
        for row in rows
    ]

@router.post(
    "",
    response_model=StockMovementResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_stock_movement(
    movement_data: StockMovementCreate,
    database: DatabaseSession,
    current_user: CurrentUser,
):
    variant = database.scalar(
        select(ProductVariant)
        .where(
            ProductVariant.id == movement_data.product_variant_id,
            ProductVariant.company_id == current_user.company_id,
            ProductVariant.active.is_(True),
        )
        .with_for_update()
    )

    if variant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Variação não encontrada.",
        )

    current_stock = get_current_stock(
        database=database,
        product_variant_id=variant.id,
        company_id=current_user.company_id,
    )

    if (
        movement_data.movement_type == "EXIT"
        and movement_data.quantity > current_stock
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Estoque insuficiente. "
                f"Saldo disponível: {current_stock}."
            ),
        )

    movement = StockMovement(
        company_id=current_user.company_id,
        product_variant_id=variant.id,
        user_id=current_user.id,
        movement_type=movement_data.movement_type,
        quantity=movement_data.quantity,
        notes=(
            movement_data.notes.strip()
            if movement_data.notes
            else None
        ),
    )

    database.add(movement)
    database.commit()
    database.refresh(movement)

    return movement