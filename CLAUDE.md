# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Run the TUI app
uv run python main.py

# Run offline unit tests (arithmetic + HITL parsing)
uv run pytest tests/test_arithmetic.py tests/test_hitl.py -v

# Run all tests including integration (requires config/.env + network)
uv run pytest tests/ -v

# Configure DeepSeek credentials (required before running)
cp config/.env.example config/.env
# Then edit config/.env with DEEPSEEK_API_KEY, DEEPSEEK_API_BASE, DEEPSEEK_MODEL
```

## Architecture

Multi-agent AI calculator where an orchestrator agent decomposes arithmetic expressions and delegates each binary operation to a specialized sub-agent. Every sub-agent result requires human confirmation via `interrupt()` before being substituted back into the expression.

### Flow

```
User expression (e.g. "(3+5)*2")
  → Orchestrator (parses, applies precedence)
    → Sub-agent (add/subtract/multiply/divide)
      → Tool function (pure arithmetic in skills/*/scripts/*.py)
        → interrupt() for user confirmation (HITL)
      → Resume approved/rejected
    → Orchestrator substitutes result back
  → Final result
```

### Key files

- [main.py](main.py) — TUI entry point with Rich console UI
- [agents/builder.py](agents/builder.py) — Constructs orchestrator + 4 sub-agents via `create_deep_agent`. Tools are **explicitly registered** per sub-agent
- [utils/runner.py](utils/runner.py) — `run_until_complete()`: invoke/resume loop handling interrupts with `version="v2"` + `GraphOutput`
- [utils/hitl.py](utils/hitl.py) — HITL TypedDict definitions, `parse_user_decision()`, `resolve_tool_response()`
- [utils/llm_client.py](utils/llm_client.py) — DeepSeek LLM client via `ChatOpenAI` (OpenAI-compatible API). Disables thinking by default
- [skills/orchestration/SKILL.md](skills/orchestration/SKILL.md) — Orchestrator workflow instructions loaded as skill
- [skills/*/SKILL.md](skills/add/SKILL.md) — Per-operation skill definitions loaded as context
- [skills/*/scripts/tool.py](skills/add/scripts/tool.py) — LangChain `@tool` functions, each calling `interrupt()` with `{agent, operation, result}` payload
- [skills/*/scripts/*.py](skills/add/scripts/add.py) — Pure arithmetic functions (no langchain dependency)

### HITL pattern

1. `@tool` function calls `interrupt({agent, operation, result})`
2. Runner receives `result.interrupts[0].value` as `ConfirmOperationPayload`
3. TUI calls `parse_user_decision()` to get `ResumeDecision`
4. Runner resumes with `Command(resume=decision)`
5. Tool checks `approval.get("approved")`: confirm → return result string; reject → return `"REJECTED: {reason}"`
6. Sub-agent system prompt (`REJECTED_FEEDBACK_RULES` in `builder.py`) tells sub-agent how to handle rejection feedback

### Framework dependencies

- **deepagents** (`create_deep_agent` + `FilesystemBackend`)
- **langgraph** (`CompiledStateGraph`, `interrupt`, `Command`, `GraphOutput`, `MemorySaver`)
- **langchain-openai** (`ChatOpenAI` for DeepSeek API)
- **rich** (TUI console)
- **httpx[socks]** (for SOCKS proxy environments)
- **uv** (package manager, NOT pip/poetry)

### Test strategy

- `test_arithmetic.py` — Pure unit tests of arithmetic functions (no LLM/agents needed)
- `test_hitl.py` — Unit tests for HITL payload parsing and decision formatting
- `test_integration.py` — End-to-end tests using `run_until_complete` with `auto_approve` callback

