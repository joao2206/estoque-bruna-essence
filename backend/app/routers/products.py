from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import CurrentUser
from app.models.category import Category
from app.models.product import Product
from app.models.user import User
from app.schemas.product import ProductCreate, ProductResponse

router = APIRouter(
    prefix="/products",
    tags=["Products"],
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
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product_data: ProductCreate,
    database: DatabaseSession,
    current_user: CurrentUser,
):
    require_admin(current_user)

    category = database.scalar(
        select(Category).where(
            Category.id == product_data.category_id,
            Category.company_id == current_user.company_id,
            Category.active.is_(True),
        )
    )

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada.",
        )

    normalized_name = product_data.name.strip()

    existing_product = database.scalar(
        select(Product).where(
            Product.company_id == current_user.company_id,
            func.lower(Product.name) == normalized_name.lower(),
        )
    )

    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um produto com este nome.",
        )

    product = Product(
        company_id=current_user.company_id,
        category_id=category.id,
        name=normalized_name,
        description=product_data.description,
        brand=product_data.brand,
        image_url=product_data.image_url,
    )

    database.add(product)
    database.commit()
    database.refresh(product)

    return product


@router.get("", response_model=list[ProductResponse])
def list_products(
    database: DatabaseSession,
    current_user: CurrentUser,
    category_id: int | None = None,
    search: str | None = None,
):
    statement = select(Product).where(
        Product.company_id == current_user.company_id,
        Product.active.is_(True),
    )

    if category_id is not None:
        statement = statement.where(Product.category_id == category_id)

    if search:
        statement = statement.where(
            Product.name.ilike(f"%{search.strip()}%")
        )

    statement = statement.order_by(Product.name)

    return database.scalars(statement).all()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    database: DatabaseSession,
    current_user: CurrentUser,
):
    product = database.scalar(
        select(Product).where(
            Product.id == product_id,
            Product.company_id == current_user.company_id,
        )
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado.",
        )

    return product