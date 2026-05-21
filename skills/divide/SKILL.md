---
name: divide-skill
description: 两数除法运算技能。当需要计算 a / b 时使用。
---

# Divide Skill

## 工具

- `divide_numbers(a: float, b: float) -> str`：返回 a/b 的结果字符串，调用时会触发用户确认。

## 规则

- 必须调用 `divide_numbers` 工具，不允许心算。
- 若除数为 0，工具直接返回错误信息，无需用户确认。
- 工具会暂停执行并征求用户确认（approve/reject）；若被拒绝则照实回报"用户拒绝"。
