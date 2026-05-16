from __future__ import annotations

REFUND_RULES = """Business Rules: Refund Policy

1. 发货后 7 天内可申请退款，需提供订单号和退款原因。
2. 已签收订单退款需退回商品，验收合格后 3-5 个工作日退款。
3. 生产中的订单退款需扣除 10% 材料费。
4. 已关闭订单不可退款。
5. 退款金额超过 5000 元需人工审批。
"""

INVOICE_RULES = """Business Rules: Invoice Policy

1. 订单支付后可申请开票。
2. 普通发票 3 个工作日开具，增值税专用发票 7 个工作日。
3. 发票抬头需与付款方一致。
4. 已开发票的订单退款需先退回发票。
"""


async def get_refund_rules() -> str:
    """Return refund business rules.

    URI: business://refund-rules
    """
    return REFUND_RULES


async def get_invoice_rules() -> str:
    """Return invoice business rules.

    URI: business://invoice-rules
    """
    return INVOICE_RULES
