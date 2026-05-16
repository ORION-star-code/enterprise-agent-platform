from __future__ import annotations

TABLE_SCHEMAS: dict[str, str] = {
    "order_info": (
        "CREATE TABLE order_info (\n"
        "    id BIGINT PRIMARY KEY AUTO_INCREMENT,\n"
        "    order_no VARCHAR(50) NOT NULL UNIQUE,\n"
        "    customer_id BIGINT NOT NULL,\n"
        "    status VARCHAR(50) NOT NULL,\n"
        "    total_amount DECIMAL(10,2),\n"
        "    created_at DATETIME,\n"
        "    updated_at DATETIME\n"
        ");"
    ),
    "customer": (
        "CREATE TABLE customer (\n"
        "    id BIGINT PRIMARY KEY AUTO_INCREMENT,\n"
        "    customer_name VARCHAR(100) NOT NULL,\n"
        "    phone VARCHAR(50),\n"
        "    email VARCHAR(100),\n"
        "    company_name VARCHAR(100),\n"
        "    created_at DATETIME,\n"
        "    updated_at DATETIME\n"
        ");"
    ),
    "inventory": (
        "CREATE TABLE inventory (\n"
        "    id BIGINT PRIMARY KEY AUTO_INCREMENT,\n"
        "    sku VARCHAR(50) NOT NULL UNIQUE,\n"
        "    product_name VARCHAR(100),\n"
        "    stock_quantity INT,\n"
        "    locked_quantity INT,\n"
        "    updated_at DATETIME\n"
        ");"
    ),
    "ticket": (
        "CREATE TABLE ticket (\n"
        "    id BIGINT PRIMARY KEY AUTO_INCREMENT,\n"
        "    customer_id BIGINT,\n"
        "    order_no VARCHAR(50),\n"
        "    issue_type VARCHAR(50),\n"
        "    content TEXT,\n"
        "    status VARCHAR(50),\n"
        "    created_at DATETIME\n"
        ");"
    ),
}


async def get_table_schema(table: str) -> str:
    """Return the DDL schema for a business table.

    URI: mysql://schema/{table}
    """
    schema = TABLE_SCHEMAS.get(table)
    if schema is None:
        available = ", ".join(TABLE_SCHEMAS.keys())
        return f"Table '{table}' not found. Available: {available}"
    return schema
