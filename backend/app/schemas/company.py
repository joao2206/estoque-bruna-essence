from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CompanyCreate(BaseModel):
    name: str
    trade_name: str | None = None
    cnpj: str | None = None
    phone: str | None = None


class CompanyResponse(BaseModel):
    id: int
    name: str
    trade_name: str | None
    cnpj: str | None
    phone: str | None
    active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)