from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyResponse

router = APIRouter(
    prefix="/companies",
    tags=["Companies"],
)

DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post(
    "",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_company(
    company_data: CompanyCreate,
    database: DatabaseSession,
):
    if company_data.cnpj:
        existing_company = database.scalar(
            select(Company).where(Company.cnpj == company_data.cnpj)
        )

        if existing_company:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe uma empresa cadastrada com este CNPJ.",
            )

    company = Company(**company_data.model_dump())

    database.add(company)
    database.commit()
    database.refresh(company)

    return company


@router.get("", response_model=list[CompanyResponse])
def list_companies(database: DatabaseSession):
    companies = database.scalars(
        select(Company).order_by(Company.name)
    ).all()

    return companies


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(
    company_id: int,
    database: DatabaseSession,
):
    company = database.get(Company, company_id)

    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada.",
        )

    return company