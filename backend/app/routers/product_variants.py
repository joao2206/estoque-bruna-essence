from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import CurrentUser
from app.models.product import Product
from app.models.product_variant import ProductVariant
from app.models.user import User
from app.schemas.product_variant import (
    ProductVariantCreate,
    ProductVariantResponse,
)

router = APIRouter(
    prefix="/product-variants",
    tags=["Product Variants"],
)

DatabaseSession = Annotated[Session, Depends(get_db)]


def require_admin(current_user: User) -> None:
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem realizar esta ação.",
        )


@router.post(
    "",
    response_model=ProductVariantResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product_variant(
    variant_data: ProductVariantCreate,
    database: DatabaseSession,
    current_user: CurrentUser,
):
    require_admin(current_user)

    product = database.scalar(
        select(Product).where(
            Product.id == variant_data.product_id,
            Product.company_id == current_user.company_id,
            Product.active.is_(True),
        )
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado.",
        )

    normalized_color = variant_data.color.strip().title()
    normalized_size = variant_data.size.strip().upper()

    existing_variant = database.scalar(
        select(ProductVariant).where(
            ProductVariant.product_id == product.id,
            func.lower(ProductVariant.color) == normalized_color.lower(),
            func.lower(ProductVariant.size) == normalized_size.lower(),
        )
    )

    if existing_variant:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Esta combinação de cor e tamanho já existe.",
        )

    variant = ProductVariant(
        company_id=current_user.company_id,
        product_id=product.id,
        sku=f"TEMP-{uuid4().hex}",
        color=normalized_color,
        size=normalized_size,
        cost_price=variant_data.cost_price,
        sale_price=variant_data.sale_price,
        minimum_stock=variant_data.minimum_stock,
    )

    database.add(variant)
    database.flush()

    variant.sku = f"BN{variant.id:06d}"

    database.commit()
    database.refresh(variant)

    return variant


@router.get("", response_model=list[ProductVariantResponse])
def list_product_variants(
    database: DatabaseSession,
    current_user: CurrentUser,
    product_id: int | None = None,
):
    statement = select(ProductVariant).where(
        ProductVariant.company_id == current_user.company_id,
        ProductVariant.active.is_(True),
    )

    if product_id is not None:
        statement = statement.where(
            ProductVariant.product_id == product_id
        )

    statement = statement.order_by(
        ProductVariant.product_id,
        ProductVariant.color,
        ProductVariant.size,
    )

    return database.scalars(statement).all()


@router.get(
    "/{variant_id}",
    response_model=ProductVariantResponse,
)
def get_product_variant(
    variant_id: int,
    database: DatabaseSession,
    current_user: CurrentUser,
):
    variant = database.scalar(
        select(ProductVariant).where(
            ProductVariant.id == variant_id,
            ProductVariant.company_id == current_user.company_id,
        )
    )

    if variant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Variação não encontrada.",
        )

    return variant