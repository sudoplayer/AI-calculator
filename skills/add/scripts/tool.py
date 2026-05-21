from langchain_core.tools import tool
from langgraph.types import interrupt

from .add import add


@tool
def add_numbers(a: float, b: float) -> str:
    """计算两个数的和 a + b，并在返回前征求用户确认。

    Args:
        a: 第一个操作数
        b: 第二个操作数
    """
    result = add(a, b)
    approval = interrupt(
        {
            "agent": "add_agent",
            "operation": f"{a} + {b}",
            "result": result,
        }
    )
    if approval.get("approved"):
        return str(result)
    return f"REJECTED: {approval.get('reason', '用户拒绝')}"
