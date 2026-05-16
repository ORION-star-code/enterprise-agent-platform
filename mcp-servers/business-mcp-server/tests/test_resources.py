from __future__ import annotations

from app.resources.business_rule_resource import (
    get_invoice_rules,
    get_refund_rules,
)
from app.resources.mysql_schema_resource import get_table_schema
from app.resources.order_status_resource import (
    get_order_status_definition,
    get_refund_status_mapping,
)


async def test_order_status_definition() -> None:
    result = await get_order_status_definition()
    assert "PENDING" in result
    assert "SHIPPED" in result
    assert "待支付" in result


async def test_refund_status_mapping() -> None:
    result = await get_refund_status_mapping()
    assert "REQUESTED" in result
    assert "退款申请中" in result


async def test_refund_rules() -> None:
    result = await get_refund_rules()
    assert "7 天内" in result
    assert "5000" in result


async def test_invoice_rules() -> None:
    result = await get_invoice_rules()
    assert "增值税" in result


async def test_table_schema_order_info() -> None:
    result = await get_table_schema("order_info")
    assert "CREATE TABLE" in result
    assert "order_no" in result


async def test_table_schema_customer() -> None:
    result = await get_table_schema("customer")
    assert "customer_name" in result


async def test_table_schema_not_found() -> None:
    result = await get_table_schema("nonexistent")
    assert "not found" in result
    assert "order_info" in result
