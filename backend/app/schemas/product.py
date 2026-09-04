from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    category_id: int
    name: str = Field(min_length=2, max_length=150)
    description: str | None = None
    brand: str | None = Field(default=None, max_length=100)
    image_url: str | None = Field(default=None, max_length=500)


class ProductResponse(BaseModel):
    id: int
    company_id: int
    category_id: int
    name: str
    description: str | None
    brand: str | None
    image_url: str | None
    active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)