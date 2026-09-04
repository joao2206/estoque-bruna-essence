from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductVariantCreate(BaseModel):
    product_id: int
    color: str = Field(min_length=2, max_length=50)
    size: str = Field(min_length=1, max_length=20)
    cost_price: Decimal = Field(ge=0, decimal_places=2)
    sale_price: Decimal = Field(ge=0, decimal_places=2)
    minimum_stock: int = Field(default=0, ge=0)


class ProductVariantResponse(BaseModel):
    id: int
    company_id: int
    product_id: int
    sku: str
    color: str
    size: str
    cost_price: Decimal
    sale_price: Decimal
    minimum_stock: int
    active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)