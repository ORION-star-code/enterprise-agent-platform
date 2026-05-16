from __future__ import annotations

import json

from app.tools.customer_tools import query_customer_by_name
from app.tools.inventory_tools import query_inventory_by_sku
from app.tools.order_tools import query_order_by_id, query_recent_orders
from app.tools.ticket_tools import query_ticket_by_customer


async def test_query_order_by_id_found() -> None:
    result = await query_order_by_id("RG1001")
    data = json.loads(result)
    assert data["found"] is True
    assert data["order"]["order_id"] == "RG1001"
    assert data["order"]["customer_name"] == "张三"


async def test_query_order_by_id_not_found() -> None:
    result = await query_order_by_id("NONEXISTENT")
    data = json.loads(result)
    assert data["found"] is False
    assert "error" in data


async def test_query_recent_orders() -> None:
    result = await query_recent_orders("张三")
    data = json.loads(result)
    assert data["total"] == 1
    assert data["orders"][0]["order_id"] == "RG1001"


async def test_query_recent_orders_empty() -> None:
    result = await query_recent_orders("不存在的人")
    data = json.loads(result)
    assert data["total"] == 0


async def test_query_customer_by_name_found() -> None:
    result = await query_customer_by_name("张三")
    data = json.loads(result)
    assert data["found"] is True
    assert data["customer"]["customer_id"] == "C001"


async def test_query_customer_by_name_not_found() -> None:
    result = await query_customer_by_name("不存在")
    data = json.loads(result)
    assert data["found"] is False


async def test_query_inventory_by_sku_found() -> None:
    result = await query_inventory_by_sku("SKU001")
    data = json.loads(result)
    assert data["found"] is True
    assert data["item"]["product_name"] == "定制水杯"
    assert data["available_quantity"] == 1500


async def test_query_inventory_by_sku_not_found() -> None:
    result = await query_inventory_by_sku("NOPE")
    data = json.loads(result)
    assert data["found"] is False


async def test_query_ticket_by_customer() -> None:
    result = await query_ticket_by_customer("张三")
    data = json.loads(result)
    assert data["total"] == 1
    assert data["tickets"][0]["ticket_id"] == "T001"


async def test_query_ticket_by_customer_empty() -> None:
    result = await query_ticket_by_customer("不存在")
    data = json.loads(result)
    assert data["total"] == 0
