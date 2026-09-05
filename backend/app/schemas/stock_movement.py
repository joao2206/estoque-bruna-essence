from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class StockMovementCreate(BaseModel):
    product_variant_id: int
    movement_type: Literal["ENTRY", "EXIT"]
    quantity: int = Field(gt=0)
    notes: str | None = Field(default=None, max_length=255)


class StockMovementResponse(BaseModel):
    id: int
    company_id: int
    product_variant_id: int
    user_id: int
    movement_type: Literal["ENTRY", "EXIT"]
    quantity: int
    notes: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class StockMovementListItemResponse(BaseModel):
    id: int
    product_variant_id: int
    sku: str
    product_name: str
    color: str
    size: str
    movement_type: Literal["ENTRY", "EXIT"]
    quantity: int
    notes: str | None
    created_at: datetime