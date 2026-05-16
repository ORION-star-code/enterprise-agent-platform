from __future__ import annotations

from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    sku: str
    name: str
    quantity: int
    unit_price: float


class Order(BaseModel):
    order_id: str
    customer_name: str
    status: str
    total_amount: float
    created_at: str
    items: list[OrderItem] = Field(default_factory=list)


class OrderQueryResult(BaseModel):
    found: bool
    order: Order | None = None
    error: str | None = None
