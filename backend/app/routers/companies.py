from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import CurrentUser
from app.models.company import Company
from app.schemas.company import CompanyResponse

router = APIRouter(
    prefix="/companies",
    tags=["Companies"],
)

DatabaseSession = Annotated[Session, Depends(get_db)]


@router.get("/me", response_model=CompanyResponse)
def get_current_company(
    database: DatabaseSession,
    current_user: CurrentUser,
):
    company = database.get(Company, current_user.company_id)

    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada.",
        )

    return company


@router.get("", response_model=list[CompanyResponse])
def list_companies(
    database: DatabaseSession,
    current_user: CurrentUser,
):
    company = database.get(Company, current_user.company_id)

    if company is None:
        return []

    return [company]


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(
    company_id: int,
    database: DatabaseSession,
    current_user: CurrentUser,
):
    if company_id != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada.",
        )

    company = database.get(Company, company_id)

    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada.",
        )

    return company