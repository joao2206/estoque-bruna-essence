from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.security import create_access_token, verify_password
from app.dependencies.auth import CurrentUser
from app.schemas.user import UserResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post("/login", response_model=TokenResponse)
def login(
    login_data: LoginRequest,
    database: DatabaseSession,
):
    normalized_email = str(login_data.email).lower()

    user = database.scalar(
        select(User).where(User.email == normalized_email)
    )

    invalid_credentials = (
        user is None
        or not verify_password(
            login_data.password,
            user.password_hash if user else "",
        )
    )

    if invalid_credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos.",
        )

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo.",
        )

    token = create_access_token(
        user_id=user.id,
        company_id=user.company_id,
        role=user.role,
    )

    return TokenResponse(access_token=token)

@router.get("/me", response_model=UserResponse)
def get_authenticated_user(current_user: CurrentUser):
    return current_user