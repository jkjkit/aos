# Knowledge Protocol

Version: v0.2.0

Status: Draft

---

# 1. Purpose

Knowledge Protocol 定义知识管理的标准规范。

本协议确保：

- 知识结构统一
- 长期可维护
- 易于查询和使用
- 内容与执行分离

---

# 2. Definition

Knowledge 是长期沉淀的规范、标准、经验和最佳实践。

Knowledge：

不参与推理。

不触发执行。

只提供参考。

---

# 3. Directory Structure

每个 Knowledge 必须遵循统一目录结构：

```
knowledge-name/
├── KNOWLEDGE.md      # 必需：知识定义
├── README.md         # 必需：使用说明
├── content.md        # 必需：实际内容
└── examples/         # 推荐：示例
    ├── example-1.md
    └── example-2.md
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
✅ coding-style
✅ git-workflow
✅ database-convention
✅ security-checklist

❌ CodingStyle
❌ Git_Workflow
❌ databaseConvention
```

---

## 4.2 命名原则

使用知识类型名称。

保持描述性。

避免模糊。

示例：

```
✅ coding-style          编码规范
✅ architecture-guide    架构指南
✅ database-convention   数据库约定
✅ security-checklist    安全检查清单

❌ knowledge-1
❌ project-info
❌ misc-notes
```

---

# 5. KNOWLEDGE.md Structure

KNOWLEDGE.md 是 Knowledge 的定义文件。

必须包含以下章节：

```markdown
# Name

# Purpose

# Scope

# Content Type

# Update Frequency

# Usage

# Maintenance
```

---

## 5.1 Name

Knowledge 的名称。

示例：

```markdown
# Name

Coding Style Guide
```

---

## 5.2 Purpose

说明 Knowledge 的用途。

示例：

```markdown
# Purpose

定义项目的编码规范，确保代码风格统一、可读性好、易于维护。
```

---

## 5.3 Scope

定义适用范围。

示例：

```markdown
# Scope

适用于：

- 所有项目代码
- 所有编程语言
- 所有团队成员

不适用于：

- 第三方库代码
- 自动生成的代码
- 临时测试代码
```

---

## 5.4 Content Type

定义内容类型。

示例：

```markdown
# Content Type

类型：规范（Convention）

包含：

- 命名规范
- 格式规范
- 注释规范
- 最佳实践
- 反模式警告
```

---

## 5.5 Update Frequency

定义更新频率。

示例：

```markdown
# Update Frequency

更新频率：按需更新

触发条件：

- 团队共识变化
- 新技术引入
- 发现规范缺陷
- 行业标准更新

审核周期：每季度 Review
```

---

## 5.6 Usage

说明如何使用。

示例：

```markdown
# Usage

## 使用时机

- 编写新代码前
- Code Review 时
- 技术决策时
- 新成员入职时

## 使用方式

- 作为参考指南
- 作为 Review 标准
- 作为培训材料

## 不使用

Knowledge 不参与：

- 自动执行
- 推理决策
- Workflow 触发
```

---

## 5.7 Maintenance

定义维护规则。

示例：

```markdown
# Maintenance

## 维护者

技术负责人

## 更新流程

1. 提出修改建议
2. 团队讨论
3. 达成共识
4. 更新内容
5. 通知团队

## 版本管理

遵循语义化版本：

- Major: 重大变更
- Minor: 新增内容
- Patch: 修正错误
```

---

# 6. content.md Structure

content.md 是实际的知识内容。

结构根据知识类型而定。

## 6.1 规范类（Convention）

```markdown
# [规范名称]

## 1. 总则

[整体原则]

## 2. [分类 1]

### 2.1 规则

[具体规则]

### 2.2 示例

✅ 正确示例：
[代码/文本]

❌ 错误示例：
[代码/文本]

### 2.3 例外

[例外情况]

## 3. [分类 2]

...
```

---

## 6.2 指南类（Guide）

```markdown
# [指南名称]

## 1. 概述

[背景和目标]

## 2. 原则

[核心原则]

## 3. 最佳实践

### 3.1 [实践 1]

**说明**

[详细说明]

**示例**

[实际示例]

**注意事项**

[注意事项]

## 4. 常见问题

[FAQ]
```

---

## 6.3 清单类（Checklist）

```markdown
# [清单名称]

## 使用说明

[如何使用此清单]

## 检查项

### [分类 1]

- [ ] [检查项 1]
- [ ] [检查项 2]
- [ ] [检查项 3]

### [分类 2]

- [ ] [检查项 1]
- [ ] [检查项 2]

## 说明

[详细说明]
```

---

## 6.4 术语类（Glossary）

```markdown
# [术语表名称]

## A

### [术语 1]

**定义**

[定义]

**用法**

[使用场景]

**示例**

[示例]

## B

...
```

---

# 7. Knowledge Types

## 7.1 Convention（规范）

定义统一标准。

示例：

```
- coding-style
- git-workflow
- database-convention
- api-convention
```

---

## 7.2 Guide（指南）

提供指导建议。

示例：

```
- architecture-guide
- performance-guide
- security-guide
- testing-guide
```

---

## 7.3 Checklist（清单）

提供检查清单。

示例：

```
- security-checklist
- review-checklist
- deployment-checklist
- onboarding-checklist
```

---

## 7.4 Glossary（术语）

定义术语。

示例：

```
- business-glossary
- technical-glossary
- domain-glossary
```

---

## 7.5 Best Practice（最佳实践）

总结经验。

示例：

```
- error-handling-best-practice
- logging-best-practice
- caching-best-practice
```

---

# 8. Design Principles

## 8.1 被动性

Knowledge 是被读取的。

不主动触发任何行为。

```
✅ 
Skill 读取 Knowledge 作为参考

❌ 
Knowledge 触发 Skill 执行
```

---

## 8.2 规范性

Knowledge 提供规范和标准。

不包含实现细节。

```
✅ 
函数命名使用 camelCase

❌ 
请使用以下代码实现函数命名检查...
[代码实现]
```

---

## 8.3 长期性

Knowledge 是长期积累的。

不是临时信息。

```
✅ 
编码规范（长期有效）

❌ 
本周的临时任务（短期信息）
```

---

## 8.4 独立性

Knowledge 独立于执行。

不依赖 Skill、Workflow。

---

# 9. Prohibited Patterns

## 9.1 包含 Prompt

禁止在 Knowledge 中包含 Prompt。

```
❌ 
请按照以下步骤检查代码...
[详细 Prompt]
```

---

## 9.2 包含执行逻辑

禁止包含执行指令。

```
❌ 
1. 执行代码分析
2. 运行测试
3. 生成报告
```

这些属于 Skill 或 Workflow。

---

## 9.3 临时信息

禁止存储临时信息。

```
❌ 
本周任务
当前 Bug 列表
会议记录
```

这些不是 Knowledge。

---

## 9.4 项目特定细节

避免过于具体的项目细节。

```
✅ 
数据库表命名使用 snake_case

❌ 
user_accounts 表的字段定义...
```

后者属于项目文档，不是 Knowledge。

---

# 10. Metadata Standards

## 10.1 Frontmatter

推荐使用 YAML Frontmatter：

```yaml
---
name: coding-style
version: v2.1.0
type: convention
category: development
author: Tech Lead
created: 2025-01-15
updated: 2026-07-19
reviewers: [reviewer1, reviewer2]
next_review: 2026-10-19
---
```

---

## 10.2 必需字段

```yaml
name: [必需] Knowledge 名称
version: [必需] 版本号
type: [必需] 类型（convention/guide/checklist/glossary/best-practice）
category: [必需] 分类
updated: [必需] 最后更新日期
```

---

## 10.3 可选字段

```yaml
author: 作者
created: 创建日期
reviewers: 审核人列表
next_review: 下次审核日期
related: 相关 Knowledge
deprecated: 是否废弃
```

---

# 11. Categories

## 11.1 Development

```
- coding-style
- git-workflow
- testing-practice
- code-review-standard
```

---

## 11.2 Architecture

```
- architecture-principles
- design-patterns
- system-design-guide
```

---

## 11.3 Infrastructure

```
- database-convention
- api-standard
- deployment-guide
```

---

## 11.4 Security

```
- security-checklist
- auth-guide
- data-protection
```

---

## 11.5 Process

```
- development-process
- release-process
- incident-response
```

---

## 11.6 Domain

```
- business-glossary
- domain-concepts
- industry-standards
```

---

# 12. Quality Standards

## 12.1 完整性检查

- [ ] 定义清晰
- [ ] 范围明确
- [ ] 内容完整
- [ ] 示例充分
- [ ] 更新策略明确

---

## 12.2 可用性检查

- [ ] 易于查询
- [ ] 易于理解
- [ ] 易于应用
- [ ] 格式清晰

---

## 12.3 维护性检查

- [ ] 版本管理清晰
- [ ] 更新流程明确
- [ ] 责任人明确
- [ ] 审核机制完善

---

# 13. README.md Structure

README.md 提供使用说明。

推荐结构：

```markdown
# Knowledge Name

## 简介

## 适用范围

## 如何使用

## 重要更新

## 相关 Knowledge

## 维护信息
```

---

# 14. Examples Structure

examples/ 目录包含应用示例。

每个示例文件结构：

```markdown
# Example: [场景名称]

## Scenario

[场景描述]

## Knowledge Applied

[应用的知识点]

## Before

[应用前的情况]

## After

[应用后的情况]

## Lessons

[经验教训]
```

---

# 15. Versioning

Knowledge 版本管理：

```
knowledge-name/
├── KNOWLEDGE.md      # 包含版本号
├── content.md        # 实际内容（包含版本）
├── CHANGELOG.md      # 变更历史
```

版本格式：

```markdown
Version: v2.1.0
```

变更规则：

- Major: 重大变更，需要适应
- Minor: 新增内容，向后兼容
- Patch: 修正、澄清、格式优化

---

# 16. Integration with Skills

## 16.1 Skill 引用 Knowledge

```
Skill: coding
↓
读取 Knowledge: coding-style
↓
按照规范编写代码
↓
输出符合规范的代码
```

---

## 16.2 引用方式

在 Skill 中引用：

```markdown
# Process

1. 读取 Knowledge: coding-style
2. 理解编码规范
3. 按照规范实现功能
4. 自检代码是否符合规范
```

---

# 17. Lifecycle

## 17.1 创建

```
识别需求
↓
编写内容
↓
团队 Review
↓
批准发布
```

---

## 17.2 更新

```
发现需要更新
↓
提出修改建议
↓
讨论达成共识
↓
更新内容
↓
通知相关方
```

---

## 17.3 废弃

```
识别过时内容
↓
标记为 deprecated
↓
提供替代方案
↓
通知相关方
↓
归档
```

---

# 18. Validation Checklist

创建 Knowledge 前检查：

- [ ] 是否长期有效（不是临时信息）
- [ ] 是否已有类似 Knowledge
- [ ] 内容是否规范性（不是执行性）
- [ ] 范围是否明确
- [ ] 是否有维护计划

---

# 19. Review Checklist

Review Knowledge 时检查：

- [ ] 文档完整性
- [ ] 内容准确性
- [ ] 范围合理性
- [ ] 被动性（不触发执行）
- [ ] 长期有效性
- [ ] 维护计划完善

---

# 20. Best Practices

## 20.1 保持简洁

只包含必要内容。

避免过度详细。

---

## 20.2 持续更新

定期 Review。

及时反映变化。

---

## 20.3 易于查询

清晰的分类。

完善的索引。

---

## 20.4 团队共识

Knowledge 应该是团队共识。

不是个人偏好。

---

# 21. Examples

参考实现：

```
knowledge/
├── coding-style/
│   ├── KNOWLEDGE.md
│   ├── README.md
│   ├── content.md
│   └── examples/
├── git-workflow/
│   ├── KNOWLEDGE.md
│   ├── README.md
│   ├── content.md
│   └── examples/
└── security-checklist/
    ├── KNOWLEDGE.md
    ├── README.md
    ├── content.md
    └── examples/
```