"""HITL 决策解析与工具响应格式化。"""

from __future__ import annotations

from typing_extensions import NotRequired, TypedDict


class ConfirmOperationPayload(TypedDict):
    """与 skills/*/tool.py 中 interrupt({...}) 的 payload 一致。"""

    agent: str
    operation: str
    result: float | int


class ResumeDecision(TypedDict, total=False):
    """TUI / runner 传给 Command(resume=...) 的决策。"""

    approved: bool
    reason: NotRequired[str]


def parse_user_decision(raw: str) -> ResumeDecision:
    """解析 TUI 用户输入为 resume payload。

    Y / 回车 → {approved: True}
    其他任意输入 → {approved: False, reason: raw}
    """
    stripped = raw.strip()
    if stripped == "" or stripped.lower() == "y":
        return {"approved": True}
    return {"approved": False, "reason": raw}


def resolve_tool_response(computed: float, approval: ResumeDecision) -> str:
    """根据用户决策返回工具结果或 REJECTED 消息。"""
    if approval.get("approved"):
        return str(computed)
    return f"REJECTED: {approval.get('reason', '')}"
