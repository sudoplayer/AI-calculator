from langchain_core.tools import tool
from langgraph.types import interrupt

from .divide import DivisionByZeroError, divide


@tool
def divide_numbers(a: float, b: float) -> str:
    """计算两个数的商 a / b，并在返回前征求用户确认。

    Args:
        a: 被除数
        b: 除数
    """
    try:
        result = divide(a, b)
    except DivisionByZeroError as exc:
        return f"ERROR: {exc}"

    approval = interrupt(
        {
            "agent": "divide_agent",
            "operation": f"{a} / {b}",
            "result": result,
        }
    )
    if approval.get("approved"):
        return str(result)
    return f"REJECTED: {approval.get('reason', '用户拒绝')}"
