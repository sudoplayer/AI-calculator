"""Agent 运行循环，处理 HITL interrupt 与 resume。"""

from __future__ import annotations

from collections.abc import Callable
from typing import cast

from langchain.agents.middleware.types import AgentState
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command, GraphOutput

from utils.hitl import ConfirmOperationPayload, ResumeDecision


def run_until_complete(
    orchestrator: CompiledStateGraph,
    user_expr: str,
    thread_id: str,
    on_interrupt: Callable[[ConfirmOperationPayload], ResumeDecision],
) -> AgentState:
    """运行智能体直到完成或用户拒绝。

    Args:
        orchestrator: create_deep_agent 返回的 CompiledStateGraph。
        user_expr: 用户输入的表达式。
        thread_id: 会话 ID，invoke / resume 须保持一致。
        on_interrupt: 回调，接收 interrupt payload，返回 resume 决策：
            确认 → {'approved': True}
            拒绝 → {'approved': False, 'reason': '<用户输入原文>'}

    Returns:
        最终 AgentState，含 messages 等字段。
    """
    config = {"configurable": {"thread_id": thread_id}}
    inputs = {"messages": [{"role": "user", "content": user_expr}]}

    result: GraphOutput[AgentState] = orchestrator.invoke(
        inputs, config=config, version="v2"
    )

    while result.interrupts:
        payload = cast(ConfirmOperationPayload, result.interrupts[0].value)
        decision = on_interrupt(payload)
        result = orchestrator.invoke(
            Command(resume=decision),
            config=config,
            version="v2",
        )

    return result.value
