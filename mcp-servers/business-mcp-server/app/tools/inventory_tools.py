from __future__ import annotations

import json

from app.clients.business_api_client import BusinessApiClient


async def query_inventory_by_sku(sku: str) -> str:
    """Check inventory for a product by SKU.

    Args:
        sku: The product SKU (e.g., 'SKU001').
    """
    client = BusinessApiClient()
    item = client.get_inventory(sku)
    if item is None:
        return json.dumps(
            {"found": False, "error": f"SKU {sku} not found in inventory"},
            ensure_ascii=False,
        )
    available = item["stock_quantity"] - item["locked_quantity"]
    return json.dumps(
        {"found": True, "item": item, "available_quantity": available},
        ensure_ascii=False,
        indent=2,
    )
