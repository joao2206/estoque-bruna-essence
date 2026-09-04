from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import CurrentUser
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryResponse

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
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
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category_data: CategoryCreate,
    database: DatabaseSession,
    current_user: CurrentUser,
):
    require_admin(current_user)

    normalized_name = category_data.name.strip()

    existing_category = database.scalar(
        select(Category).where(
            Category.company_id == current_user.company_id,
            func.lower(Category.name) == normalized_name.lower(),
        )
    )

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe uma categoria com este nome.",
        )

    category = Category(
        company_id=current_user.company_id,
        name=normalized_name,
    )

    database.add(category)
    database.commit()
    database.refresh(category)

    return category


@router.get("", response_model=list[CategoryResponse])
def list_categories(
    database: DatabaseSession,
    current_user: CurrentUser,
):
    return database.scalars(
        select(Category)
        .where(
            Category.company_id == current_user.company_id,
            Category.active.is_(True),
        )
        .order_by(Category.name)
    ).all()


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    database: DatabaseSession,
    current_user: CurrentUser,
):
    category = database.scalar(
        select(Category).where(
            Category.id == category_id,
            Category.company_id == current_user.company_id,
        )
    )

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada.",
        )

    return category