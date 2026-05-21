"""集成测试：自动 approve 所有 interrupt，验证多智能体计算流程。"""

from __future__ import annotations

import uuid

from agents.builder import build_orchestrator
from main import extract_final_message
from utils.hitl import ConfirmOperationPayload, ResumeDecision
from utils.runner import run_until_complete


def auto_approve(_payload: ConfirmOperationPayload) -> ResumeDecision:
    return {"approved": True}


def test_simple_addition():
    orchestrator = build_orchestrator()
    state = run_until_complete(
        orchestrator,
        "3+5",
        thread_id=str(uuid.uuid4()),
        on_interrupt=auto_approve,
    )
    final = extract_final_message(state)
    assert "8" in final, f"期望结果含 8，实际: {final!r}"


def test_parentheses_expression():
    orchestrator = build_orchestrator()
    state = run_until_complete(
        orchestrator,
        "(3+5)*2",
        thread_id=str(uuid.uuid4()),
        on_interrupt=auto_approve,
    )
    final = extract_final_message(state)
    assert "16" in final, f"期望结果含 16，实际: {final!r}"


def test_divide_by_zero():
    orchestrator = build_orchestrator()
    state = run_until_complete(
        orchestrator,
        "10/0",
        thread_id=str(uuid.uuid4()),
        on_interrupt=auto_approve,
    )
    final = extract_final_message(state)
    lowered = final.lower()
    assert any(k in lowered for k in ("除", "zero", "错误", "error", "0")), f"期望除零错误提示，实际: {final!r}"


def feedback_override_first_add(payload: ConfirmOperationPayload) -> ResumeDecision:
    operation = payload.get("operation", "")
    if "2.0 + 4.0" in operation or "2 + 4" in operation.replace(" ", ""):
        return {"approved": False, "reason": "把结果改成8"}
    return {"approved": True}


def test_feedback_correction_parentheses_expression():
    """第一步加法被拒绝并给出修正反馈，子 agent 应采纳 reason 继续计算。"""
    orchestrator = build_orchestrator()
    state = run_until_complete(
        orchestrator,
        "(2+4)*6",
        thread_id=str(uuid.uuid4()),
        on_interrupt=feedback_override_first_add,
    )
    final = extract_final_message(state)
    assert "48" in final, f"期望结果含 48，实际: {final!r}"
