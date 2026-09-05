from pydantic import BaseModel


class StockItemResponse(BaseModel):
    product_variant_id: int
    sku: str
    product_name: str
    color: str
    size: str
    current_stock: int
    minimum_stock: int
    low_stock: bool