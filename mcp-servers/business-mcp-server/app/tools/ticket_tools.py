from __future__ import annotations

import json

from app.clients.business_api_client import BusinessApiClient


async def query_ticket_by_customer(customer_name: str) -> str:
    """Get support tickets for a customer.

    Args:
        customer_name: The customer's name (e.g., '张三').
    """
    client = BusinessApiClient()
    tickets = client.get_tickets(customer_name)
    return json.dumps(
        {
            "customer_name": customer_name,
            "tickets": tickets,
            "total": len(tickets),
        },
        ensure_ascii=False,
        indent=2,
    )
