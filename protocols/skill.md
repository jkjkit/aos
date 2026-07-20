# Skill Protocol

Version: v0.2.0

Status: Draft

---

# 1. Purpose

Skill Protocol 定义 AOS 中 Skill 的标准规范。

本协议确保：

- 所有 Skill 结构统一
- 所有 Skill 可独立运行
- 所有 Skill 可自由组合
- 所有 Skill 易于维护

---

# 2. Definition

Skill 是 AOS 中的最小执行单元。

一个 Skill：

完成一件明确的事情。

拥有清晰的输入输出。

可以独立运行。

可以被组合调用。

---

# 3. Directory Structure

每个 Skill 必须遵循统一目录结构：

```
skill-name/
├── SKILL.md          # 必需：Skill 定义
├── README.md         # 必需：使用说明
├── examples/         # 必需：示例
│   ├── example-1.md
│   └── example-2.md
└── tests/            # 推荐：测试用例
    └── test-cases.md
```

---

# 4. Naming Convention

## 4.1 目录命名

格式：

```
kebab-case
```

使用：

小写字母、数字、连字符。

示例：

```
✅ code-review
✅ api-design
✅ bug-fix

❌ CodeReview
❌ API_Design
❌ bugFix
```

---

## 4.2 命名原则

使用动词或动作描述。

保持简短清晰。

避免缩写。

示例：

```
✅ summary
✅ coding
✅ review
✅ debug
✅ design

❌ super-helper
❌ ai-assistant
❌ do-everything
```

---

# 5. SKILL.md Structure

SKILL.md 是 Skill 的核心定义文件。

必须包含以下章节：

```markdown
# Name

# Purpose

# When To Use

# Input

# Process

# Output

# Quality Check

# Limitations

# Examples
```

---

## 5.1 Name

Skill 的名称。

要求：

简短。

清晰。

唯一。

示例：

```markdown
# Name

Code Review
```

---

## 5.2 Purpose

说明 Skill 的目标。

要求：

一句话说明。

使用主动语态。

示例：

```markdown
# Purpose

Review code changes for bugs, best practices, and maintainability issues.
```

---

## 5.3 When To Use

明确使用场景。

要求：

列举典型场景。

说明触发条件。

示例：

```markdown
# When To Use

使用此 Skill 当：

- 完成代码编写，准备提交
- 收到 Pull Request
- 需要第二视角检查代码
- 重构代码后需要验证

不使用此 Skill 当：

- 代码尚未完成
- 只是简单的格式调整
- 已经过多轮 Review
```

---

## 5.4 Input

定义输入要求。

要求：

类型明确。

格式清晰。

前置条件。

示例：

```markdown
# Input

## Required

- 代码文件或 diff
- 编程语言

## Optional

- 编码规范
- 项目上下文
- Review 重点

## Preconditions

- 代码可以编译/解析
- 包含必要的上下文
```

---

## 5.5 Process

说明执行步骤。

要求：

步骤清晰。

逻辑连贯。

可执行。

示例：

```markdown
# Process

1. 读取代码变更
2. 理解代码意图
3. 检查常见问题：
   - 语法错误
   - 逻辑错误
   - 性能问题
   - 安全隐患
   - 可读性问题
4. 评估影响范围
5. 提供改进建议
6. 输出 Review 报告
```

---

## 5.6 Output

定义输出格式。

要求：

结构明确。

格式统一。

内容完整。

示例：

```markdown
# Output

## Structure

\`\`\`markdown
# Review Report

## Summary
[概述]

## Issues Found
- [Issue 1]
- [Issue 2]

## Suggestions
- [Suggestion 1]
- [Suggestion 2]

## Approval Status
[✅ Approved / ⚠️ Approved with comments / ❌ Changes requested]
\`\`\`

## Format

Markdown

## Content Requirements

- 必须包含 Summary
- Issues 按严重程度排序
- Suggestions 具体可执行
- 必须给出明确的 Approval Status
```

---

## 5.7 Quality Check

定义质量标准。

示例：

```markdown
# Quality Check

输出质量检查：

- [ ] 是否发现真实问题
- [ ] 建议是否可执行
- [ ] 是否有误报
- [ ] 输出是否完整
- [ ] 格式是否正确
```

---

## 5.8 Limitations

说明局限性。

示例：

```markdown
# Limitations

本 Skill 的局限：

- 不能发现所有 bug
- 不能替代人工 Review
- 依赖代码上下文质量
- 不执行代码测试
- 不检查运行时行为
```

---

## 5.9 Examples

提供实际示例。

示例：

```markdown
# Examples

参见：

- examples/example-1.md
- examples/example-2.md
```

---

# 6. README.md Structure

README.md 提供使用说明。

推荐结构：

```markdown
# Skill Name

## 简介

## 快速开始

## 使用场景

## 示例

## 常见问题

## 相关 Skills
```

---

# 7. Examples Structure

examples/ 目录必须包含实际示例。

每个示例文件结构：

```markdown
# Example: [场景名称]

## Input

[实际输入]

## Process

[执行过程]

## Output

[实际输出]

## Notes

[注意事项]
```

---

# 8. Design Principles

## 8.1 Single Responsibility

一个 Skill 只做一件事。

```
✅ Code Review
✅ Summary
✅ API Design

❌ Code Review + Testing + Deployment
```

---

## 8.2 独立性

Skill 必须可以独立运行。

不依赖：

- 其它 Skill
- 特定 Workflow
- 特定上下文

---

## 8.3 可组合性

Skill 可以自由组合。

示例：

```
Requirement → Design → Coding → Review
```

每个 Skill 独立，但可以串联。

---

## 8.4 明确边界

输入边界清晰。

输出边界清晰。

职责边界清晰。

---

# 9. Prohibited Patterns

## 9.1 万能 Skill

禁止创建：

```
❌ AI Super Assistant
   - 编码
   - 设计
   - 测试
   - 部署
   - 文档
```

---

## 9.2 隐藏 Workflow

Skill 内禁止嵌入复杂流程。

```
❌ 
Process:
1. 需求分析
2. 设计方案
3. 编写代码
4. 测试验证
5. 部署上线
```

这是 Workflow，不是 Skill。

---

## 9.3 大量知识嵌入

Skill 内禁止嵌入：

- 公司规范（属于 Knowledge）
- 编码标准（属于 Knowledge）
- 领域知识（属于 Knowledge）

---

# 10. Quality Standards

## 10.1 文档完整性

- [ ] SKILL.md 包含所有必需章节
- [ ] README.md 提供清晰说明
- [ ] examples/ 包含实际示例
- [ ] 所有字段填写完整

---

## 10.2 可执行性

- [ ] 输入要求明确
- [ ] 执行步骤清晰
- [ ] 输出格式统一
- [ ] 可以独立运行

---

## 10.3 可维护性

- [ ] 命名符合规范
- [ ] 结构符合协议
- [ ] 职责单一清晰
- [ ] 文档易于理解

---

# 11. Versioning

Skill 版本管理：

```
skill-name/
├── SKILL.md          # 包含版本号
├── CHANGELOG.md      # 可选：变更历史
```

版本格式：

```markdown
Version: v1.2.0
```

---

# 12. Metadata

推荐在 SKILL.md 头部添加元数据：

```markdown
---
name: code-review
version: v1.0.0
category: development
tags: [code, review, quality]
author: AOS
created: 2026-07-19
updated: 2026-07-19
---
```

---

# 13. Testing

tests/ 目录包含测试用例：

```markdown
# Test Cases

## Test 1: [场景]

### Input
[测试输入]

### Expected Output
[期望输出]

### Actual Output
[实际输出]

### Status
✅ Pass / ❌ Fail
```

---

# 14. Dependencies

## 14.1 允许依赖

- Knowledge（规范、标准）
- Template（输出格式）

---

## 14.2 禁止依赖

- 其它 Skill
- 特定 Workflow
- 特定 Runtime

---

# 15. Output Protocol

Skill 输出必须遵循 Output Protocol。

推荐结构：

```markdown
# Summary

# Analysis

# Recommendations

# Next Steps
```

详见：output.md

---

# 16. Integration

Skill 应该：

- 被 Workflow 调用
- 被 Runtime 直接调用
- 与其它 Skill 组合

Skill 不应该：

- 调用其它 Skill
- 定义执行流程
- 管理生命周期

---

# 17. Validation Checklist

新建 Skill 前检查：

- [ ] 是否已有类似 Skill
- [ ] 是否符合单一职责
- [ ] 是否可以独立运行
- [ ] 是否有明确的输入输出
- [ ] 是否遵循命名规范
- [ ] 是否包含完整文档
- [ ] 是否提供实际示例

---

# 18. Review Checklist

Review Skill 时检查：

- [ ] 文档完整性
- [ ] 职责单一性
- [ ] 独立可运行
- [ ] 输入输出明确
- [ ] 示例充分
- [ ] 命名规范
- [ ] 无禁止模式

---

# 19. Migration Guide

从 Prompt 迁移到 Skill：

```
旧方式：
一个长 Prompt 包含所有逻辑

↓

新方式：
拆分为多个独立 Skill
每个 Skill 符合本协议
通过 Workflow 组合
```

---

# 20. Examples

参考实现：

```
skills/
├── summary/
│   ├── SKILL.md
│   ├── README.md
│   └── examples/
├── coding/
│   ├── SKILL.md
│   ├── README.md
│   └── examples/
└── review/
    ├── SKILL.md
    ├── README.md
    └── examples/
```

---

# 21. Matching Quality

Skill 不仅要能执行，还必须能被 Runtime 正确选择。

## 21.1 Description

`description` 是 MANIFEST 的主要匹配入口，必须同时包含：

1. **动作**：该 Skill 做什么
2. **对象或交付物**：最终产出什么
3. **关键边界**：最容易混淆但不属于它的任务

推荐格式：

```yaml
description: <动作与交付物>；不负责 <最容易混淆的相邻职责>
```

禁止只写宽泛描述，例如“帮助设计系统”“处理文档”“分析问题”。

## 21.2 Positive and Negative Triggers

“何时使用”必须同时说明：

- 选择此 Skill 的典型场景
- 不选择此 Skill 的相邻场景
- 应转交给哪个相邻 Skill

高混淆 Skill 应增加“匹配边界”，按最终交付物给出选择示例。

## 21.3 Routing Data

如果 Skill 属于高混淆能力组，必须在 `data/skill-routing.json` 中登记：

- `choose_when`
- `avoid_when`
- 至少一个能够区分相邻 Skill 的示例

修改后必须重新生成 MANIFEST，并确认路由数据引用的 Skill 全部存在。

## 21.4 Routing Regression

高混淆 Skill 的路由修改必须同步维护 `tests/skill-routing/cases.json`：

- 每个登记在 `data/skill-routing.json` 中的 Skill 至少有 2 条自然语言回归用例
- 每条用例必须声明预期能力、易混淆候选和选择理由
- 真实误匹配修复后必须增加能够复现问题的用例
- 多阶段输入应验证其选择对应 Workflow，而不是同时选择多个主 Skill

修改 Skill、Workflow 或路由数据后必须运行：

```bash
python scripts/build-manifest.py
python scripts/test-skill-routing.py
```

静态测试验证路由契约和覆盖范围。若要验证具体 Runtime 的语义匹配结果，使用 `--predictions` 提交该 Runtime 对全部用例的选择结果，任何错误匹配都应导致回归失败。
