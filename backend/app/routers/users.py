from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.company import Company
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.security import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_data: UserCreate,
    database: DatabaseSession,
):
    company = database.get(Company, user_data.company_id)

    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada.",
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
        company_id=user_data.company_id,
        name=user_data.name.strip(),
        email=normalized_email,
        password_hash=hash_password(user_data.password),
        role=user_data.role,
    )

    database.add(user)
    database.commit()
    database.refresh(user)

    return user


@router.get("", response_model=list[UserResponse])
def list_users(database: DatabaseSession):
    return database.scalars(
        select(User).order_by(User.name)
    ).all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    database: DatabaseSession,
):
    user = database.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado.",
        )

    return user