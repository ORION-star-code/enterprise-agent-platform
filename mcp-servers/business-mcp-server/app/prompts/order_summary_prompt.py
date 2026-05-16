from __future__ import annotations


def order_summary_prompt(order_info: str, issue: str = "") -> str:
    """Generate a prompt for creating a customer-service order summary.

    Args:
        order_info: Structured order information (JSON or text).
        issue: Optional issue or complaint description.
    """
    issue_section = ""
    if issue:
        issue_section = f"\nCustomer Issue:\n{issue}\n"

    return (
        "请根据以下订单信息，生成一段面向客服人员的订单摘要。\n"
        "摘要应包含：订单状态、关键金额、商品明细，"
        "以及如有异常问题则给出处理建议。\n\n"
        f"订单信息:\n{order_info}\n"
        f"{issue_section}\n"
        "订单摘要:"
    )
