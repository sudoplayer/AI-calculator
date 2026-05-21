from langchain_core.tools import tool
from langgraph.types import interrupt

from .subtract import subtract


@tool
def subtract_numbers(a: float, b: float) -> str:
    """计算两个数的差 a - b，并在返回前征求用户确认。

    Args:
        a: 被减数
        b: 减数
    """
    result = subtract(a, b)
    approval = interrupt(
        {
            "agent": "subtract_agent",
            "operation": f"{a} - {b}",
            "result": result,
        }
    )
    if approval.get("approved"):
        return str(result)
    return f"REJECTED: {approval.get('reason', '用户拒绝')}"
