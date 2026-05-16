from __future__ import annotations

from pydantic import BaseModel


class Customer(BaseModel):
    customer_id: str
    name: str
    phone: str
    email: str
    company: str


class CustomerQueryResult(BaseModel):
    found: bool
    customer: Customer | None = None
    error: str | None = None
