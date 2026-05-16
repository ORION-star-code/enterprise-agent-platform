from __future__ import annotations

import json

from app.clients.business_api_client import BusinessApiClient


async def query_customer_by_name(customer_name: str) -> str:
    """Look up a customer by name.

    Args:
        customer_name: The customer's name (e.g., '张三').
    """
    client = BusinessApiClient()
    customer = client.get_customer(customer_name)
    if customer is None:
        return json.dumps(
            {"found": False, "error": f"Customer '{customer_name}' not found"},
            ensure_ascii=False,
        )
    return json.dumps(
        {"found": True, "customer": customer}, ensure_ascii=False, indent=2
    )
