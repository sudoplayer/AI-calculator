[English](./README.md) | 中文

# 🧮 AI Calculator

*Master-agent + Sub-agents MVP — powered by LangChain ecosystem's [deepagents](https://github.com/langchain-ai/deepagents)*

---

> **本项目是为普适场景迁移扩展提供的参考实现**，以 **AI 计算器** 为演示载体，展示 deepagents 的核心编排模式。你可以将它作为脚手架，复用到任意多智能体协作场景——代码审查助手、数据分析管线、文档生成工作流等。

## 🎬 演示

![AI Calculator 演示](assets/ai-calculator.gif)

## ✨ 核心特性


| 特性                 | 说明                                         |
| ------------------ | ------------------------------------------ |
| 🧠 **主-子架构**       | 一个 Orchestrator 集中决策，按需调度专业 Sub-agent 协作完成 |
| 👤 **人在回路 (HITL)** | 每步关键计算结果需人工确认/驳回，确保安全可控                    |
| 🧩 **Skill 机制**    | 每个子智能体以 `skills/` 文件夹独立组织，职责边界分明           |
| 🔌 **即改即用**        | 替换 Skill 定义与工具函数即可适配新领域，架构零改动              |


## 🖥️ 快速体验

```bash
# 1️⃣ 安装依赖
uv sync

# 2️⃣ 配置 DeepSeek 凭证
cp config/.env.example config/.env
# 编辑 config/.env，填入 DEEPSEEK_API_KEY

# 3️⃣ 启动交互终端
uv run python main.py
```

输入表达式 `(3 + 5) * 2`，观察 Orchestrator 如何拆解任务、调度子智能体、请求你的确认——整个过程清晰可见。

## 🏗️ 架构总览

```
        用户输入: "(3+5)*2"
              │
              ▼
   ┌─────────────────────────────────────────────┐
   │                Orchestrator                 │
   │         (解析表达式、处理优先级、编排执行顺序)    │
   └──────┬──────────────┬──────────────┬───────┘
          │              │              │
          ▼              ▼              ▼
     ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
     │   加法    │   │   减法   │   │   乘法    │   │   除法    │
     │  Agent   │   │  Agent   │   │  Agent   │   │  Agent   │
     └────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘
          │              │              │              │
          ▼              ▼              ▼              ▼
     ┌──────────────────────────────────────────────────┐
     │              Tool 纯函数计算                       │
     │          → interrupt() 请求用户确认                │
     └──────────────────────────────────────────────────┘
          │              │              │              │
          ▼              ▼              ▼              ▼
               ✅ 确认 / ❌ 驳回并说明原因
          │              │              │              │
          └──────────────┴──────────────┴──────────────┘
                    │
                    ▼
          Orchestrator 代入结果，继续下一步
                    │
                    ▼
              最终输出: 16
```

### 核心流程

1. **Orchestrator** 接收用户表达式，按运算符优先级分解为子任务
2. **Sub-agent** 被调度执行单一二元运算（加/减/乘/除）
3. **Tool 函数** 执行纯算术逻辑后调用 `interrupt()` 暂停流程
4. **用户确认/驳回**：确认则结果回填；驳回可附原因，Sub-agent 据此调整
5. **Orchestrator** 将已确认结果代入表达式推进，直至得出最终答案

## 📁 项目结构

```
.
├── main.py                       # TUI 入口 (Rich 控制台界面)
├── agents/
│   └── builder.py                # 构建 Orchestrator + 4 个 Sub-agent
├── skills/
│   ├── orchestration/SKILL.md    # Orchestrator 工作流指令
│   ├── add/SKILL.md              # 加法技能定义
│   ├── subtract/SKILL.md         # 减法技能定义
│   ├── multiply/SKILL.md         # 乘法技能定义
│   ├── divide/SKILL.md           # 除法技能定义
│   └── */scripts/
│       ├── tool.py               # LangChain @tool 函数 (含 interrupt)
│       └── *.py                  # 纯算术函数
├── utils/
│   ├── runner.py                 # run_until_complete 循环
│   ├── hitl.py                   # HITL 类型定义与决策解析
│   └── llm_client.py             # DeepSeek LLM 客户端
├── tests/
│   ├── test_arithmetic.py        # 算术函数单元测试
│   ├── test_hitl.py              # HITL 解析单元测试
│   └── test_integration.py       # 端到端集成测试
├── config/
│   ├── .env.example              # 环境变量模板
│   └── .env                      # 你的 API 凭证（不提交）
├── assets/
│   └── ai-calculator.gif         # 录屏演示
├── pyproject.toml
├── README.md
└── README_CN.md
```

## 🛠️ 技术栈


| 类别      | 技术                                                                            |
| ------- | ----------------------------------------------------------------------------- |
| 核心框架    | [deepagents](https://github.com/langchain-ai/deepagents) (LangChain)          |
| 状态图     | [LangGraph](https://langchain-ai.github.io/langgraph/)                        |
| LLM 客户端 | [langchain-openai](https://pypi.org/project/langchain-openai/) → DeepSeek API |
| 终端界面    | [Rich](https://rich.readthedocs.io/)                                          |
| 包管理     | [uv](https://github.com/astral-sh/uv)                                         |
| 测试      | pytest                                                                        |


## 🧪 测试

```bash
# 离线单元测试（无需网络/LLM）
uv run pytest tests/test_arithmetic.py tests/test_hitl.py -v

# 全部测试（含端到端，需网络 + API Key）
uv run pytest tests/ -v
```

## 🔄 迁移到新场景

以本项目为脚手架，将 AI 计算器转换为其他多智能体场景：

1. **定义技能**：在 `skills/` 下创建新 Skill 目录，参照现有 `SKILL.md` 编写指令
2. **实现工具**：编写新的 `tool.py`，复用 `interrupt()` 实现人的确认
3. **注册 Agent**：在 `builder.py` 中注册新 Sub-agent 并挂载工具
4. **调整编排**：修改 Orchestrator 的 Skill 指令，告知它新能力

> 项目架构围绕"编排 + 确认回环"设计，替换的是**领域知识**和**工具函数**，复用的是**协作流程**和**HITL 模式**。

## 📄 License

[MIT](LICENSE)

---

**AI Calculator** — deepagents 多智能体编排的 MVP 参考实现