---
name: refactor
description: 在不改变外部行为的前提下重构代码结构，提升可读性与可维护性
---

# Refactor

在不改变外部行为的前提下改进代码结构。**不修复 Bug，不加新功能**。

## 何时使用

- 模块越来越长、越来越难读
- 出现重复代码或职责混乱
- 命名、耦合、依赖方向需要调整
- 计划扩展前先整理结构
- 清理技术债

不要用于：

- 需要加新功能（用 design + coding）
- 修复 Bug（用 debug）
- 整体重写（用 design 重新设计）

## 第一原则：保持行为不变

> 重构的承诺是「改完之后，所有现有调用方的行为完全一致」。如果行为可能变，那就是重写。

任何重构前确认两点：

1. 已有测试覆盖，或能写出等价验证
2. 重构范围明确——不要顺手改业务

## 流程

1. **识别代码异味**：长函数、重复代码、Feature Envy、神密命名、Primitive Obsession、Shotgun Surgery 等
2. **明确目标**：本次要解决哪几类问题；不解决的列出来
3. **选择重构手法**：每次只用一种
   - Extract Method / Extract Class
   - Rename / Move / Inline
   - Replace Conditional with Polymorphism
   - Introduce Parameter Object
   - 调整依赖方向
4. **逐步执行**：每步后跑测试；保持提交粒度独立可回滚
5. **行为验证**：测试通过 + 关键路径手测
6. **输出报告**：变更点、验证结果、遗留风险

## 常用手法速查

| 异味 | 手法 |
|------|------|
| 长函数 | Extract Method |
| 大类 | Extract Class |
| 重复代码 | Extract Method + 调用 |
| 神密命名 | Rename |
| 临时字段 | Extract Class |
| 条件分支过多 | Replace Conditional with Polymorphism |
| 参数过多 | Introduce Parameter Object |
| 平行继承 | Move Method + Move Field |
| 跨模块纠缠 | 调整依赖方向、引入中间层 |

## 输出格式

```markdown
# Refactor Report

## 目标
[本次要解决的问题]

## Smells 识别
- [位置]：[异味]
- ...

## 步骤
1. [手法] [位置] — 验证：测试 X 通过
2. ...

## 行为不变量
- [保持不变的接口 / 输出 / 副作用]

## 验证
- 测试：[通过 / 失败]
- 手动：[关键路径]

## 遗留风险
- [后续建议]
```

## 行为准则

- **不在重构里加功能**：发现需要新功能时单独开任务
- **不修改测试以迁就代码**：测试失败说明行为可能变了
- **每步可回滚**：小颗粒提交
- **不删除「看起来没用」的代码**：先确认真没引用

## 不要做的事

- 不要在重构里顺手修 Bug——那是另一个工作
- 不要在没测试覆盖的代码上做大重构
- 不要为了「漂亮」做没有目标驱动的重构