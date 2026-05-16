from __future__ import annotations

import json

from app.clients.business_api_client import BusinessApiClient


async def query_order_by_id(order_id: str) -> str:
    """Look up a single order by its ID.

    Args:
        order_id: The order identifier (e.g., 'RG1001').
    """
    client = BusinessApiClient()
    order = client.get_order(order_id)
    if order is None:
        return json.dumps(
            {"found": False, "error": f"Order {order_id} not found"},
            ensure_ascii=False,
        )
    return json.dumps({"found": True, "order": order}, ensure_ascii=False, indent=2)


async def query_recent_orders(
    customer_name: str, limit: int = 5
) -> str:
    """Get recent orders for a customer.

    Args:
        customer_name: The customer's name (e.g., '张三').
        limit: Maximum number of orders to return.
    """
    client = BusinessApiClient()
    orders = client.get_recent_orders(customer_name, limit)
    return json.dumps(
        {"customer_name": customer_name, "orders": orders, "total": len(orders)},
        ensure_ascii=False,
        indent=2,
    )
