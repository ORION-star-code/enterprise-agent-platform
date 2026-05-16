from __future__ import annotations

from typing import Any

# --- Mock Data (MVP) ---

MOCK_ORDERS: dict[str, dict[str, Any]] = {
    "RG1001": {
        "order_id": "RG1001",
        "customer_name": "张三",
        "status": "SHIPPED",
        "total_amount": 12800.00,
        "created_at": "2026-05-01",
        "items": [
            {
                "sku": "SKU001",
                "name": "定制水杯",
                "quantity": 500,
                "unit_price": 25.60,
            }
        ],
    },
    "RG1002": {
        "order_id": "RG1002",
        "customer_name": "李四",
        "status": "PAID",
        "total_amount": 3600.00,
        "created_at": "2026-05-10",
        "items": [
            {
                "sku": "SKU002",
                "name": "企业笔记本",
                "quantity": 200,
                "unit_price": 18.00,
            }
        ],
    },
}

MOCK_CUSTOMERS: dict[str, dict[str, Any]] = {
    "张三": {
        "customer_id": "C001",
        "name": "张三",
        "phone": "13800138000",
        "email": "zhangsan@example.com",
        "company": "ABC科技",
    },
    "李四": {
        "customer_id": "C002",
        "name": "李四",
        "phone": "13900139000",
        "email": "lisi@example.com",
        "company": "XYZ贸易",
    },
}

MOCK_INVENTORY: dict[str, dict[str, Any]] = {
    "SKU001": {
        "sku": "SKU001",
        "product_name": "定制水杯",
        "stock_quantity": 2000,
        "locked_quantity": 500,
    },
    "SKU002": {
        "sku": "SKU002",
        "product_name": "企业笔记本",
        "stock_quantity": 5000,
        "locked_quantity": 200,
    },
}

MOCK_TICKETS: dict[str, list[dict[str, Any]]] = {
    "张三": [
        {
            "ticket_id": "T001",
            "customer_name": "张三",
            "order_id": "RG1001",
            "issue_type": "退款咨询",
            "status": "处理中",
            "content": "客户询问已发货订单是否可以退款",
            "created_at": "2026-05-12",
        },
    ],
    "李四": [
        {
            "ticket_id": "T002",
            "customer_name": "李四",
            "order_id": "RG1002",
            "issue_type": "发货催促",
            "status": "已解决",
            "content": "客户催促尽快发货",
            "created_at": "2026-05-11",
        },
    ],
}


class BusinessApiClient:
    """Business data client. MVP returns mock data.

    Replace with HTTP calls to business-service when available.
    """

    def get_order(self, order_id: str) -> dict[str, Any] | None:
        return MOCK_ORDERS.get(order_id)

    def get_recent_orders(
        self, customer_name: str, limit: int = 5
    ) -> list[dict[str, Any]]:
        orders = [
            o
            for o in MOCK_ORDERS.values()
            if o["customer_name"] == customer_name
        ]
        return orders[:limit]

    def get_customer(self, customer_name: str) -> dict[str, Any] | None:
        return MOCK_CUSTOMERS.get(customer_name)

    def get_inventory(self, sku: str) -> dict[str, Any] | None:
        return MOCK_INVENTORY.get(sku)

    def get_tickets(
        self, customer_name: str
    ) -> list[dict[str, Any]]:
        return MOCK_TICKETS.get(customer_name, [])
