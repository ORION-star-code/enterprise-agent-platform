from __future__ import annotations

ORDER_STATUS_MAP: dict[str, str] = {
    "PENDING": "待支付",
    "PAID": "已支付",
    "PRODUCING": "生产中",
    "SHIPPED": "已发货",
    "CLOSED": "已关闭",
}

REFUND_STATUS_MAP: dict[str, str] = {
    "NONE": "无退款",
    "REQUESTED": "退款申请中",
    "APPROVED": "退款已批准",
    "REJECTED": "退款已拒绝",
    "COMPLETED": "退款已完成",
}


async def get_order_status_definition() -> str:
    """Return order status code to label mapping.

    URI: business://order-status-definition
    """
    lines = ["Order Status Definitions:\n"]
    for code, label in ORDER_STATUS_MAP.items():
        lines.append(f"  {code}: {label}")
    return "\n".join(lines)


async def get_refund_status_mapping() -> str:
    """Return refund status code to label mapping.

    URI: business://refund-status-mapping
    """
    lines = ["Refund Status Definitions:\n"]
    for code, label in REFUND_STATUS_MAP.items():
        lines.append(f"  {code}: {label}")
    return "\n".join(lines)
