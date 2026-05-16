from __future__ import annotations

from app.prompts.customer_reply_prompt import customer_reply_prompt
from app.prompts.order_summary_prompt import order_summary_prompt


def test_order_summary_prompt_contains_order_info() -> None:
    result = order_summary_prompt('{"order_id": "RG1001"}')
    assert "RG1001" in result


def test_order_summary_prompt_with_issue() -> None:
    result = order_summary_prompt("order info", issue="客户要求退款")
    assert "客户要求退款" in result


def test_order_summary_prompt_without_issue() -> None:
    result = order_summary_prompt("order info")
    assert "订单摘要:" in result


def test_customer_reply_prompt_contains_name() -> None:
    result = customer_reply_prompt("张三", "订单已发货")
    assert "张三" in result


def test_customer_reply_prompt_contains_context() -> None:
    result = customer_reply_prompt("张三", "订单 RG1001 已发货")
    assert "RG1001" in result


def test_customer_reply_prompt_tone_apologetic() -> None:
    result = customer_reply_prompt("张三", "问题", tone="apologetic")
    assert "道歉" in result


def test_customer_reply_prompt_tone_friendly() -> None:
    result = customer_reply_prompt("张三", "问题", tone="friendly")
    assert "友好" in result
