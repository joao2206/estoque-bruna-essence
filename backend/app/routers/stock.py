from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import CurrentUser
from app.models.product import Product
from app.models.product_variant import ProductVariant
from app.models.stock_movement import StockMovement
from app.schemas.stock import StockItemResponse


router = APIRouter(
    prefix="/stock",
    tags=["Stock"],
)

DatabaseSession = Annotated[Session, Depends(get_db)]


@router.get(
    "",
    response_model=list[StockItemResponse],
)
def list_stock(
    database: DatabaseSession,
    current_user: CurrentUser,
):
    movement_balance = (
        select(
            StockMovement.product_variant_id.label(
                "product_variant_id"
            ),
            func.sum(
                case(
                    (
                        StockMovement.movement_type == "ENTRY",
                        StockMovement.quantity,
                    ),
                    else_=-StockMovement.quantity,
                )
            ).label("current_stock"),
        )
        .where(
            StockMovement.company_id == current_user.company_id
        )
        .group_by(StockMovement.product_variant_id)
        .subquery()
    )

    rows = database.execute(
        select(
            ProductVariant.id.label("product_variant_id"),
            ProductVariant.sku,
            Product.name.label("product_name"),
            ProductVariant.color,
            ProductVariant.size,
            ProductVariant.minimum_stock,
            func.coalesce(
                movement_balance.c.current_stock,
                0,
            ).label("current_stock"),
        )
        .join(
            Product,
            Product.id == ProductVariant.product_id,
        )
        .outerjoin(
            movement_balance,
            movement_balance.c.product_variant_id
            == ProductVariant.id,
        )
        .where(
            ProductVariant.company_id
            == current_user.company_id,
            ProductVariant.active.is_(True),
        )
        .order_by(
            Product.name,
            ProductVariant.sku,
        )
    ).all()

    return [
        StockItemResponse(
            product_variant_id=row.product_variant_id,
            sku=row.sku,
            product_name=row.product_name,
            color=row.color,
            size=row.size,
            current_stock=int(row.current_stock),
            minimum_stock=row.minimum_stock,
            low_stock=(
                int(row.current_stock) <= row.minimum_stock
            ),
        )
        for row in rows
    ]