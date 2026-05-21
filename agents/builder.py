"""
主编排智能体构建模块。

使用 deepagents.create_deep_agent 构建一个主智能体和 4 个算术子智能体。
每个子智能体显式注册 tools。
"""

from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends.filesystem import FilesystemBackend
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph

from skills.add.scripts.tool import add_numbers
from skills.divide.scripts.tool import divide_numbers
from skills.multiply.scripts.tool import multiply_numbers
from skills.subtract.scripts.tool import subtract_numbers
from utils.llm_client import get_llm

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = str(PROJECT_ROOT / "skills")

ORCHESTRATOR_SYSTEM_PROMPT = (
    "你是 AI 计算器的主编排智能体。给定一个含 + - * / 与括号的代数表达式，"
    "按运算优先级（括号 → 乘除 → 加减）逐步归约。每一步只取出一个二元运算，"
    "用 task 工具调用四个子智能体之一：add_agent / subtract_agent / multiply_agent / divide_agent。"
    "**禁止调用 general-purpose 子智能体；禁止自己心算运算结果**。"
    "每次调用 task 时，在 description 中明确传入两个操作数。"
    "等子智能体返回（含用户确认）后，将结果代回原表达式继续归约，直到只剩一个数。"
    "最后用一段话给出完整计算过程与最终结果。"
)

REJECTED_FEEDBACK_RULES = (
    "若工具返回以 REJECTED: 开头的消息："
    "1. 将冒号后的 reason 视为用户反馈，理解用户要改的是「结果」还是「操作数」。"
    "2. 若用户纠正结果（如「改成8」「结果应该是8」）：直接回复修正后的数值（可附一句说明），禁止再次调用工具。"
    "3. 若用户指出操作数错误：可用正确操作数重新调用工具。"
    "4. 若 reason 仅为简单否定（如 n、否）：向主编排说明本步被拒绝，不要重试相同输入。"
    "5. 禁止忽略 reason、禁止返回原 computed 结果敷衍。"
)


def build_orchestrator() -> CompiledStateGraph:
    """构建并返回主编排智能体。"""
    llm = get_llm(temperature=0.0)
    checkpointer = MemorySaver()

    add_def = {
        "name": "add_agent",
        "description": "执行两个数的加法运算。",
        "system_prompt": (
            "你是加法子智能体。收到两个操作数 a 和 b，必须调用 add_numbers(a, b) 工具得到结果。"
            "禁止心算，禁止编造结果。工具返回什么，你就返回什么。"
            + REJECTED_FEEDBACK_RULES
        ),
        "tools": [add_numbers],
        "skills": [f"{SKILLS_ROOT}/add/"],
    }

    subtract_def = {
        "name": "subtract_agent",
        "description": "执行两个数的减法运算。",
        "system_prompt": (
            "你是减法子智能体。收到两个操作数 a 和 b，必须调用 subtract_numbers(a, b) 工具得到结果。"
            "禁止心算，禁止编造结果。工具返回什么，你就返回什么。"
            + REJECTED_FEEDBACK_RULES
        ),
        "tools": [subtract_numbers],
        "skills": [f"{SKILLS_ROOT}/subtract/"],
    }

    multiply_def = {
        "name": "multiply_agent",
        "description": "执行两个数的乘法运算。",
        "system_prompt": (
            "你是乘法子智能体。收到两个操作数 a 和 b，必须调用 multiply_numbers(a, b) 工具得到结果。"
            "禁止心算，禁止编造结果。工具返回什么，你就返回什么。"
            + REJECTED_FEEDBACK_RULES
        ),
        "tools": [multiply_numbers],
        "skills": [f"{SKILLS_ROOT}/multiply/"],
    }

    divide_def = {
        "name": "divide_agent",
        "description": "执行两个数的除法运算。",
        "system_prompt": (
            "你是除法子智能体。收到两个操作数 a 和 b，必须调用 divide_numbers(a, b) 工具得到结果。"
            "禁止心算，禁止编造结果。工具返回什么，你就返回什么。"
            + REJECTED_FEEDBACK_RULES
        ),
        "tools": [divide_numbers],
        "skills": [f"{SKILLS_ROOT}/divide/"],
    }

    orchestrator = create_deep_agent(
        model=llm,
        backend=FilesystemBackend(root_dir=str(PROJECT_ROOT), virtual_mode=True),
        skills=[f"{SKILLS_ROOT}/orchestration/"],
        subagents=[add_def, subtract_def, multiply_def, divide_def],
        system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,
        checkpointer=checkpointer,
    )

    return orchestrator

