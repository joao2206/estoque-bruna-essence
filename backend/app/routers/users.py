from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import CurrentUser
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.security import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"],
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
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_data: UserCreate,
    database: DatabaseSession,
    current_user: CurrentUser,
):
    require_admin(current_user)

    if user_data.company_id != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não é permitido criar usuários para outra empresa.",
        )

    normalized_email = str(user_data.email).lower()

    existing_user = database.scalar(
        select(User).where(User.email == normalized_email)
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um usuário com este e-mail.",
        )

    user = User(
        company_id=current_user.company_id,
        name=user_data.name.strip(),
        email=normalized_email,
        password_hash=hash_password(user_data.password),
        role=user_data.role,
    )

    database.add(user)
    database.commit()
    database.refresh(user)

    return user
    return user


@router.get("", response_model=list[UserResponse])
def list_users(
    database: DatabaseSession,
    current_user: CurrentUser,
):
    return database.scalars(
        select(User)
        .where(User.company_id == current_user.company_id)
        .order_by(User.name)
    ).all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    database: DatabaseSession,
    current_user: CurrentUser,
):
    user = database.scalar(
        select(User).where(
            User.id == user_id,
            User.company_id == current_user.company_id,
        )
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado.",
        )

    return user