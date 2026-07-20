# Template Protocol

Version: v0.2.0

Status: Draft

---

# 1. Purpose

Template Protocol 定义输出格式的标准规范。

本协议确保：

- 所有输出格式统一
- 内容与表现分离
- 易于复用和维护
- 结构清晰一致

---

# 2. Definition

Template 定义输出的结构和格式。

Template：

不包含业务逻辑。

不参与推理分析。

只定义展示结构。

---

# 3. Directory Structure

每个 Template 必须遵循统一目录结构：

```
template-name/
├── TEMPLATE.md       # 必需：模板定义
├── README.md         # 必需：使用说明
├── template.md       # 必需：实际模板
└── examples/         # 必需：示例
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
✅ prd-template
✅ api-doc-template
✅ meeting-notes-template
✅ release-note-template

❌ PRDTemplate
❌ API_Doc
❌ meetingNotes
```

---

## 4.2 命名原则

使用文档类型名称。

保持描述性。

避免缩写。

示例：

```
✅ prd              （产品需求文档）
✅ api-doc          （API 文档）
✅ meeting-notes    （会议记录）
✅ release-note     （发布说明）

❌ doc-1
❌ template-a
❌ output-format
```

---

# 5. TEMPLATE.md Structure

TEMPLATE.md 是 Template 的定义文件。

必须包含以下章节：

```markdown
# Name

# Purpose

# When To Use

# Structure

# Fields

# Format

# Examples
```

---

## 5.1 Name

Template 的名称。

示例：

```markdown
# Name

Product Requirement Document (PRD)
```

---

## 5.2 Purpose

说明 Template 的用途。

示例：

```markdown
# Purpose

标准化产品需求文档格式，确保需求描述完整、清晰、可执行。
```

---

## 5.3 When To Use

定义使用场景。

示例：

```markdown
# When To Use

使用此 Template 当：

- 编写新功能需求
- 整理产品规划
- 与团队沟通需求
- 需要标准化文档

不使用此 Template 当：

- 简单的 Bug 描述
- 内部临时讨论
- 技术实现细节
```

---

## 5.4 Structure

定义文档结构。

示例：

```markdown
# Structure

## 一级结构

1. 项目概述
2. 背景
3. 目标
4. 功能需求
5. 非功能需求
6. 验收标准

## 层级关系

- 使用 Markdown 标题
- 最多 3 级标题
- 保持层级清晰
```

---

## 5.5 Fields

定义所有字段。

示例：

```markdown
# Fields

## Required Fields

### 项目名称
- 类型：文本
- 说明：项目的正式名称
- 示例：用户认证系统

### 版本
- 类型：版本号
- 格式：vX.Y.Z
- 示例：v1.0.0

### 状态
- 类型：枚举
- 可选值：Draft / Review / Approved / Implemented
- 默认：Draft

## Optional Fields

### 相关文档
- 类型：链接列表
- 说明：相关的设计文档、技术文档链接
```

---

## 5.6 Format

定义格式要求。

示例：

```markdown
# Format

## File Format

Markdown (.md)

## Encoding

UTF-8

## Metadata

使用 YAML Frontmatter：

\`\`\`yaml
---
title: 项目名称
version: v1.0.0
status: Draft
author: 作者名
date: 2026-07-19
---
\`\`\`

## Sections

- 使用 # ## ### 标题
- 使用 - 列表
- 使用 \`\`\` 代码块
- 使用 > 引用
```

---

## 5.7 Examples

提供示例引用。

示例：

```markdown
# Examples

参见：

- examples/example-1.md - 用户认证需求
- examples/example-2.md - API 设计需求
```

---

# 6. template.md Structure

template.md 是实际的模板文件。

使用占位符表示可变内容。

示例：

```markdown
---
title: [项目名称]
version: [版本号]
status: [状态]
author: [作者]
date: [日期]
---

# [项目名称]

## 1. 项目概述

[简要描述项目目标和范围]

## 2. 背景

### 2.1 业务背景

[描述业务背景和动机]

### 2.2 用户痛点

[描述要解决的问题]

## 3. 目标

### 3.1 业务目标

- [目标 1]
- [目标 2]

### 3.2 用户目标

- [目标 1]
- [目标 2]

## 4. 功能需求

### 4.1 [功能模块 1]

**描述**

[功能描述]

**用户故事**

作为 [角色]
我想要 [功能]
以便于 [价值]

**验收标准**

- [ ] [标准 1]
- [ ] [标准 2]

## 5. 非功能需求

### 5.1 性能要求

[性能指标]

### 5.2 安全要求

[安全要求]

## 6. 验收标准

- [ ] [标准 1]
- [ ] [标准 2]

## 7. 附录

### 7.1 术语表

[术语定义]

### 7.2 相关文档

[文档链接]
```

---

# 7. Design Principles

## 7.1 内容与格式分离

Template 只定义格式。

内容由 Skill 生成。

```
✅ 
## 功能需求
[由 requirement skill 填充]

❌ 
## 功能需求
根据业务分析，我们需要实现...
```

---

## 7.2 结构清晰

使用清晰的层级结构。

```
✅ 
# 标题
## 子标题
### 详细内容

❌ 
扁平的段落堆砌
```

---

## 7.3 占位符明确

使用明确的占位符。

```
✅ 
[项目名称]
[功能描述]

❌ 
XXX
TODO
...
```

---

## 7.4 可扩展

支持可选章节。

```
✅ 
## 4. 功能需求（必需）
## 5. 非功能需求（可选）
## 6. 附录（可选）
```

---

# 8. Prohibited Patterns

## 8.1 包含业务逻辑

禁止在 Template 中包含判断逻辑。

```
❌ 
如果是简单需求，使用简化版格式
如果是复杂需求，使用完整版格式
```

---

## 8.2 嵌入 Prompt

禁止在 Template 中嵌入 Prompt。

```
❌ 
## 背景
请详细分析业务背景，注意考虑...
```

---

## 8.3 过度复杂

避免过于复杂的结构。

```
❌ 
5 层嵌套标题
100+ 字段
复杂的条件章节
```

---

# 9. Common Templates

## 9.1 Document Templates

```
- prd                  产品需求文档
- design-doc           设计文档
- api-doc              API 文档
- architecture-doc     架构文档
- readme               README
```

---

## 9.2 Meeting Templates

```
- meeting-notes        会议记录
- standup-notes        站会记录
- retrospective        回顾会议
```

---

## 9.3 Development Templates

```
- task                 任务描述
- bug-report           Bug 报告
- code-review          Review 报告
- release-note         发布说明
```

---

# 10. Placeholder Convention

## 10.1 格式

使用方括号包裹：

```
[占位符名称]
```

---

## 10.2 命名

使用描述性名称：

```
✅ 
[项目名称]
[功能描述]
[作者名]

❌ 
[1]
[field]
[xxx]
```

---

## 10.3 类型说明

可选：在占位符后添加类型说明：

```
[项目名称: 文本]
[版本号: vX.Y.Z]
[状态: Draft | Review | Approved]
[日期: YYYY-MM-DD]
```

---

# 11. Metadata Standards

## 11.1 Frontmatter

推荐使用 YAML Frontmatter：

```yaml
---
title: 文档标题
version: v1.0.0
status: Draft
author: 作者
date: 2026-07-19
tags: [tag1, tag2]
---
```

---

## 11.2 必需字段

```yaml
title: [必需] 文档标题
version: [必需] 版本号
status: [必需] 状态
date: [必需] 日期
```

---

## 11.3 可选字段

```yaml
author: 作者
reviewers: [审核人列表]
tags: [标签列表]
related: [相关文档]
```

---

# 12. Quality Standards

## 12.1 完整性检查

- [ ] 包含所有必需章节
- [ ] 占位符定义清晰
- [ ] 格式说明完整
- [ ] 提供实际示例

---

## 12.2 可用性检查

- [ ] 结构清晰易懂
- [ ] 占位符易于识别
- [ ] 格式容易遵循
- [ ] 示例充分

---

## 12.3 维护性检查

- [ ] 命名符合规范
- [ ] 文档结构合理
- [ ] 易于更新
- [ ] 版本管理清晰

---

# 13. README.md Structure

README.md 提供使用说明。

推荐结构：

```markdown
# Template Name

## 简介

## 适用场景

## 如何使用

## 字段说明

## 示例

## 常见问题
```

---

# 14. Examples Structure

examples/ 目录包含填充后的示例。

每个示例文件结构：

```markdown
---
title: [实际标题]
version: v1.0.0
status: Approved
author: AOS Team
date: 2026-07-19
---

# [实际项目名称]

## 1. 项目概述

[实际内容]

...

---

## Notes

这是一个示例文档，展示如何使用此模板。
```

---

# 15. Versioning

Template 版本管理：

```
template-name/
├── TEMPLATE.md       # 包含版本号
├── template.md       # 实际模板
├── CHANGELOG.md      # 变更历史
```

版本格式：

```markdown
Version: v1.0.0
```

变更规则：

- Major: 结构重大变更
- Minor: 新增可选章节
- Patch: 文案优化、格式调整

---

# 16. Integration with Skills

## 16.1 Skill 生成内容

```
Skill: requirement
↓
生成内容
↓
填充到 PRD Template
↓
输出格式化文档
```

---

## 16.2 调用方式

Skill 引用 Template：

```markdown
# Output

使用 Template: prd

填充字段：
- title: [从分析中提取]
- requirements: [从分析中提取]
- acceptance: [从分析中提取]
```

---

# 17. Validation Checklist

创建 Template 前检查：

- [ ] 是否已有类似 Template
- [ ] 结构是否清晰
- [ ] 字段是否完整
- [ ] 占位符是否明确
- [ ] 是否纯格式（无逻辑）
- [ ] 是否易于使用

---

# 18. Review Checklist

Review Template 时检查：

- [ ] 文档完整性
- [ ] 结构合理性
- [ ] 占位符清晰性
- [ ] 格式一致性
- [ ] 示例充分性
- [ ] 命名规范性

---

# 19. Migration Guide

从硬编码格式迁移到 Template：

```
旧方式：
在 Skill 中硬编码输出格式

↓

新方式：
1. 提取格式结构
2. 创建 Template
3. Skill 只生成内容
4. 使用 Template 格式化
```

---

# 20. Best Practices

## 20.1 保持简洁

只包含必需的章节和字段。

---

## 20.2 一致性

同类 Template 保持结构一致。

---

## 20.3 可选性

使用可选章节支持不同复杂度。

---

## 20.4 文档化

充分说明每个字段的用途。

---

# 21. Examples

参考实现：

```
templates/
├── prd/
│   ├── TEMPLATE.md
│   ├── README.md
│   ├── template.md
│   └── examples/
├── api-doc/
│   ├── TEMPLATE.md
│   ├── README.md
│   ├── template.md
│   └── examples/
└── meeting-notes/
    ├── TEMPLATE.md
    ├── README.md
    ├── template.md
    └── examples/
```

---

