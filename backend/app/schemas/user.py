from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    company_id: int
    name: str = Field(min_length=3, max_length=150)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: Literal["ADMIN", "EMPLOYEE"] = "EMPLOYEE"


class UserResponse(BaseModel):
    id: int
    company_id: int
    name: str
    email: str
    role: str
    active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)