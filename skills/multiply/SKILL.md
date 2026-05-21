---
name: multiply-skill
description: 两数乘法运算技能。当需要计算 a * b 时使用。
---

# Multiply Skill

## 工具

- `multiply_numbers(a: float, b: float) -> str`：返回 a*b 的结果字符串，调用时会触发用户确认。

## 规则

- 必须调用 `multiply_numbers` 工具，不允许心算。
- 工具会暂停执行并征求用户确认（approve/reject）；若被拒绝则照实回报"用户拒绝"。
