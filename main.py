"""
AI 计算器 - 主入口

用法：
    python main.py

环境要求：
    1. 将 config/.env.example 复制为 config/.env 并填入 DEEPSEEK_API_KEY
    2. 安装依赖：uv sync
"""

from __future__ import annotations

import sys
import uuid

from langchain.agents.middleware.types import AgentState
from rich.console import Console
from rich.panel import Panel

from utils.hitl import ConfirmOperationPayload, ResumeDecision, parse_user_decision


console = Console()


def prompt_interrupt(payload: ConfirmOperationPayload) -> ResumeDecision:
    """TUI 处理一次 interrupt，返回 resume 决策。"""

    agent = payload.get("agent", "unknown")
    operation = payload.get("operation", "")
    result = payload.get("result", "")

    console.print()
    console.print(
        Panel(
            f"[bold cyan]{agent}[/bold cyan]\n"
            f"运算: [yellow]{operation}[/yellow]\n"
            f"结果: [green]{result}[/green]",
            title="请确认此步运算结果",
            border_style="blue",
        )
    )

    raw = console.input(
        "[bold]确认此步结果？[Y/回车 确认，或直接输入 拒绝原因][/bold] "
    )
    decision = parse_user_decision(raw)
    if not decision.get("approved"):
        console.print(f"[dim]已拒绝，等待 {agent} 根据反馈修正...[/dim]")
    return decision


def extract_final_message(state: AgentState) -> str:
    """从最终 state 中提取最后一条 AI 回复。"""
    from langchain_core.messages import AIMessage

    for msg in reversed(state.get("messages", [])):
        if isinstance(msg, AIMessage) and msg.content:
            return str(msg.content)
    return "(无输出)"


def main() -> None:
    console.print("[bold blue]AI Calculator (Deep Agents MVP)[/bold blue]")
    console.print("[dim]输入含 + - * / 与括号的表达式；输入 quit | exit | q 退出[/dim]\n")

    try:
        from agents.builder import build_orchestrator
        from utils.runner import run_until_complete
    except ImportError as exc:
        console.print(f"[red]导入失败：{exc}[/red]")
        console.print("请运行：uv sync")
        sys.exit(1)

    try:
        orchestrator = build_orchestrator()
    except ValueError as exc:
        console.print(f"[red]编排器构建失败：{exc}[/red]")
        sys.exit(1)

    while True:
        try:
            expr = console.input("[bold]> [/bold]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n再见。")
            break

        if not expr:
            continue
        if expr.lower() in {"quit", "exit", "q"}:
            console.print("再见。")
            break

        thread_id = str(uuid.uuid4())
        console.print(f"[dim]会话 ID: {thread_id}[/dim]")

        try:
            state = run_until_complete(
                orchestrator,
                expr,
                thread_id,
                on_interrupt=prompt_interrupt,
            )
        except Exception as exc:
            console.print(f"[red]运行失败：{exc}[/red]")
            continue

        final = extract_final_message(state)
        console.print()
        console.print(Panel(final, title="最终结果", border_style="green"))
        console.print()


if __name__ == "__main__":
    main()
