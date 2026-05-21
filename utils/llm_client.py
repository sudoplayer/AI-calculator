"""DeepSeek LLM 客户端，通过 OpenAI 兼容接口接入。"""

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

ENV_PATH = Path(__file__).resolve().parent.parent / "config" / ".env"
load_dotenv(ENV_PATH)


@lru_cache(maxsize=1)
def get_llm(temperature: float = 0.0) -> ChatOpenAI:
    """返回已配置的 DeepSeek LLM 实例。"""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    api_base = os.getenv("DEEPSEEK_API_BASE")
    model = os.getenv("DEEPSEEK_MODEL")

    if not api_key or not api_base or not model:
        raise ValueError(
            "未设置 DEEPSEEK_API_KEY, DEEPSEEK_API_BASE, DEEPSEEK_MODEL，请在 config/.env 中配置。"
        )

    return ChatOpenAI(
        model=model,
        openai_api_key=api_key,
        openai_api_base=api_base,
        temperature=temperature,
        extra_body={"thinking": {"type": "disabled"}},
    )
