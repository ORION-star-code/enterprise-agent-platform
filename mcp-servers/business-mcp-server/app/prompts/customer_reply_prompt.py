from __future__ import annotations


def customer_reply_prompt(
    customer_name: str, context: str, tone: str = "professional"
) -> str:
    """Generate a template for replying to a customer.

    Args:
        customer_name: The customer's name.
        context: Relevant context (order info, issue details, etc.).
        tone: Tone of reply — 'professional', 'friendly', or 'apologetic'.
    """
    tone_instructions = {
        "professional": "使用专业、正式的语气。",
        "friendly": "使用友好、亲切的语气。",
        "apologetic": "使用诚恳道歉的语气，表达对问题的重视。",
    }
    tone_note = tone_instructions.get(tone, tone_instructions["professional"])

    return (
        f"请为以下客户生成回复。\n\n"
        f"客户姓名: {customer_name}\n"
        f"语气要求: {tone_note}\n\n"
        f"相关背景:\n{context}\n\n"
        f"回复内容:"
    )
