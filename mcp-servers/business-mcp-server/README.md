# Business MCP Server

MCP server exposing business data tools (orders, customers, inventory, tickets) to the agent-gateway.

## Architecture

```
agent-gateway (MCP client) --> business-mcp-server (SSE, port 8002) --> mock data (MVP)
```

MVP uses hardcoded mock data. Will be replaced with HTTP calls to business-service (Spring Boot) when available.

## Quick Start

```bash
cd mcp-servers/business-mcp-server && uv sync
uv run pytest tests/ -x
uv run python -m app.server
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `order_lookup` | Look up a single order by ID |
| `recent_orders` | Get recent orders for a customer |
| `customer_lookup` | Look up a customer by name |
| `inventory_check` | Check inventory for a product by SKU |
| `ticket_lookup` | Get support tickets for a customer |

## MCP Resources

| URI | Description |
|-----|-------------|
| `business://order-status-definition` | Order status code to label mapping |
| `business://refund-status-mapping` | Refund status code to label mapping |
| `business://refund-rules` | Refund business rules |
| `business://invoice-rules` | Invoice business rules |
| `mysql://schema/{table}` | DDL schema for business tables |

## MCP Prompts

| Prompt | Parameters | Description |
|--------|-----------|-------------|
| `order_summary` | order_info, issue | Template for customer-service order summary |
| `customer_reply` | customer_name, context, tone | Template for customer reply |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BUSINESS_SERVICE_URL` | `http://localhost:8080` | business-service base URL (future use) |
| `MCP_HOST` | `0.0.0.0` | MCP server bind host |
| `MCP_PORT` | `8002` | MCP server bind port |
