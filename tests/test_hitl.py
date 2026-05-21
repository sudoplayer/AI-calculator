"""HITL 决策解析与工具响应离线单测。"""

from __future__ import annotations

from utils.hitl import parse_user_decision, resolve_tool_response


def test_parse_user_decision_approve_empty():
    assert parse_user_decision("") == {"approved": True}


def test_parse_user_decision_approve_y():
    assert parse_user_decision("Y") == {"approved": True}
    assert parse_user_decision("y") == {"approved": True}


def test_parse_user_decision_reject_n():
    assert parse_user_decision("n") == {"approved": False, "reason": "n"}


def test_parse_user_decision_reject_feedback():
    assert parse_user_decision("把结果改成8") == {
        "approved": False,
        "reason": "把结果改成8",
    }


def test_resolve_tool_response_approved():
    assert resolve_tool_response(6.0, {"approved": True}) == "6.0"


def test_resolve_tool_response_rejected():
    assert resolve_tool_response(
        6.0,
        {"approved": False, "reason": "把结果改成8"},
    ) == "REJECTED: 把结果改成8"
