# AI Calculator — Main-Agent + Sub-Agents MVP

一个基于 **LangChain** 生态中 **[deepagents](https://github.com/langchain-ai/deepagents)** 库实现的主智能体 + 子智能体架构的 MVP 示例项目。

> **本项目是为普适场景迁移扩展提供的参考实现**，以 AI 计算器为演示载体，展示 deepagents 的核心编排模式。你可以将它作为脚手架，复用到文档处理、代码审查、数据分析、客服工单等任意多智能体协作场景。

## 核心概念

通过一个**主编排智能体**（Orchestrator）统一理解用户意图，动态拆解任务并按需调度多个**专业子智能体**（Sub-agents）协作完成。每个子智能体专注于单一领域，结果可经人工确认后再汇入最终输出。

## 快速开始

```bash
# 安装依赖
uv sync

# 配好模型凭证
cp config/.env.example config/.env
# 编辑 config/.env，填入你的 API Key

# 启动交互终端
uv run python main.py
```

## 适用场景参考

本项目的架构可迁移至以下场景：

- **智能客服**：编排 agent 理解用户问题 → 分派查询/退款/投诉子 agent
- **内容写作**：编排 agent 规划大纲 → 分派调研/撰写/配图子 agent
- **代码审查**：编排 agent 分析 diff → 分派安全/性能/风格子 agent
- **数据处理**：编排 agent 解析需求 → 分派清洗/转换/聚合子 agent
- **工作流自动化**：编排 agent 理解流程 → 分派审批/执行/通知子 agent

## 项目特点

- **主-子架构清晰**：一个 orchestrator 集中决策，多个 sub-agent 各司其职，关注点分离
- **人在回路(HITL)**：关键步骤支持人工确认/驳回，确保安全可控
- **Skill 机制**：每个子智能体以 Skill 文件夹组织，职责边界分明
- **即改即用**：替换 Skill 定义和工具函数即可适配新领域
