from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from app.config import get_settings
from app.prompts.customer_reply_prompt import customer_reply_prompt
from app.prompts.order_summary_prompt import order_summary_prompt
from app.resources.business_rule_resource import (
    get_invoice_rules,
    get_refund_rules,
)
from app.resources.mysql_schema_resource import get_table_schema
from app.resources.order_status_resource import (
    get_order_status_definition,
    get_refund_status_mapping,
)
from app.tools.customer_tools import query_customer_by_name
from app.tools.inventory_tools import query_inventory_by_sku
from app.tools.order_tools import query_order_by_id, query_recent_orders
from app.tools.ticket_tools import query_ticket_by_customer

settings = get_settings()

mcp = FastMCP(
    settings.mcp_server_name,
    host=settings.mcp_host,
    port=settings.mcp_port,
)


# --- Tools ---


@mcp.tool()
async def order_lookup(order_id: str) -> str:
    """Look up a single order by its ID."""
    return await query_order_by_id(order_id)


@mcp.tool()
async def recent_orders(customer_name: str, limit: int = 5) -> str:
    """Get recent orders for a customer."""
    return await query_recent_orders(customer_name, limit)


@mcp.tool()
async def customer_lookup(customer_name: str) -> str:
    """Look up a customer by name."""
    return await query_customer_by_name(customer_name)


@mcp.tool()
async def inventory_check(sku: str) -> str:
    """Check inventory for a product by SKU."""
    return await query_inventory_by_sku(sku)


@mcp.tool()
async def ticket_lookup(customer_name: str) -> str:
    """Get support tickets for a customer."""
    return await query_ticket_by_customer(customer_name)


# --- Resources ---


@mcp.resource("business://order-status-definition")
async def order_status_resource() -> str:
    """Order status code to label mapping."""
    return await get_order_status_definition()


@mcp.resource("business://refund-status-mapping")
async def refund_status_resource() -> str:
    """Refund status code to label mapping."""
    return await get_refund_status_mapping()


@mcp.resource("business://refund-rules")
async def refund_rules_resource() -> str:
    """Refund business rules."""
    return await get_refund_rules()


@mcp.resource("business://invoice-rules")
async def invoice_rules_resource() -> str:
    """Invoice business rules."""
    return await get_invoice_rules()


@mcp.resource("mysql://schema/{table}")
async def table_schema_resource(table: str) -> str:
    """DDL schema for a business table."""
    return await get_table_schema(table)


# --- Prompts ---


@mcp.prompt()
def order_summary(order_info: str, issue: str = "") -> str:
    """Template for generating a customer-service order summary."""
    return order_summary_prompt(order_info, issue)


@mcp.prompt()
def customer_reply(
    customer_name: str, context: str, tone: str = "professional"
) -> str:
    """Template for generating a customer reply."""
    return customer_reply_prompt(customer_name, context, tone)


def main() -> None:
    """Run the MCP server with SSE transport."""
    mcp.run(transport="sse")


if __name__ == "__main__":
    main()
