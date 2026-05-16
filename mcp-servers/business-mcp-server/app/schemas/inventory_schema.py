from __future__ import annotations

from pydantic import BaseModel


class InventoryItem(BaseModel):
    sku: str
    product_name: str
    stock_quantity: int
    locked_quantity: int


class InventoryQueryResult(BaseModel):
    found: bool
    item: InventoryItem | None = None
    available_quantity: int = 0
    error: str | None = None
