# Workflow Protocol

Version: v0.2.0

Status: Draft

---

# 1. Purpose

Workflow Protocol 定义如何组织和编排多个 Skill。

本协议确保：

- Workflow 职责清晰
- Skill 编排标准化
- 执行流程可预测
- 易于维护和扩展

---

# 2. Definition

Workflow 是 Skill 的编排序列。

Workflow：

不负责业务逻辑。

不负责推理分析。

只负责组织执行顺序。

---

# 3. Directory Structure

每个 Workflow 必须遵循统一目录结构：

```
workflow-name/
├── WORKFLOW.md       # 必需：Workflow 定义
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
✅ new-feature
✅ bug-fix
✅ code-review-flow
✅ project-init

❌ NewFeature
❌ BUG_FIX
❌ codeReviewFlow
```

---

## 4.2 命名原则

使用业务流程名称。

保持描述性。

避免技术术语。

示例：

```
✅ new-feature       （开发新功能）
✅ bug-fix          （修复 Bug）
✅ research         （技术研究）
✅ project-init     （初始化项目）

❌ skill-chain-1
❌ process-executor
❌ flow-handler
```

---

# 5. WORKFLOW.md Structure

WORKFLOW.md 是 Workflow 的核心定义文件。

必须包含以下章节：

```markdown
# Name

# Purpose

# Trigger

# Skills

# Steps

# Input

# Output

# Error Handling

# Examples
```

---

## 5.1 Name

Workflow 的名称。

示例：

```markdown
# Name

New Feature Development
```

---

## 5.2 Purpose

说明 Workflow 的目标。

示例：

```markdown
# Purpose

完整的新功能开发流程，从需求分析到代码提交。
```

---

## 5.3 Trigger

定义触发条件。

示例：

```markdown
# Trigger

使用此 Workflow 当：

- 需要开发新功能
- 有明确的需求描述
- 需要完整的开发流程

不使用此 Workflow 当：

- 简单的 Bug 修复
- 代码重构
- 文档更新
```

---

## 5.4 Skills

列出使用的所有 Skill。

示例：

```markdown
# Skills

本 Workflow 使用以下 Skills：

- requirement    （需求分析）
- design         （架构设计）
- coding         （代码实现）
- review         （代码审查）
- git            （版本管理）
- document       （文档编写）
```

---

## 5.5 Steps

定义执行步骤。

要求：

- 步骤明确
- 顺序清晰
- 可执行
- 无业务逻辑

示例：

```markdown
# Steps

## Step 1: Requirement Analysis

Skill: requirement

Input: 用户需求描述

Output: 结构化需求文档

---

## Step 2: Architecture Design

Skill: design

Input: 需求文档（Step 1 输出）

Output: 架构设计文档

---

## Step 3: Implementation

Skill: coding

Input: 设计文档（Step 2 输出）

Output: 代码实现

---

## Step 4: Code Review

Skill: review

Input: 代码实现（Step 3 输出）

Output: Review 报告

---

## Step 5: Git Commit

Skill: git

Input: 已审查的代码

Output: Git commit 记录

---

## Step 6: Documentation

Skill: document

Input: 完整实现

Output: 更新的文档
```

---

## 5.6 Input

定义 Workflow 的输入。

示例：

```markdown
# Input

## Required

- 功能需求描述
- 目标代码库路径

## Optional

- 设计约束
- 技术栈要求
- 时间要求
```

---

## 5.7 Output

定义 Workflow 的输出。

示例：

```markdown
# Output

## Final Deliverables

- 需求文档
- 设计文档
- 实现代码
- Review 报告
- Git commit
- 更新的文档

## Format

每个 Step 的输出保持原始格式
```

---

## 5.8 Error Handling

定义错误处理策略。

示例：

```markdown
# Error Handling

## Step 失败

如果某个 Step 失败：

1. 记录失败原因
2. 暂停 Workflow
3. 通知用户
4. 等待修复后继续

## 回滚策略

- Step 1-2 失败：无需回滚
- Step 3-4 失败：保留代码，等待修复
- Step 5-6 失败：检查 Git 状态

## 重试策略

允许从任意 Step 重新开始。
```

---

## 5.9 Examples

提供实际示例。

示例：

```markdown
# Examples

参见：

- examples/example-1.md - 开发 API 端点
- examples/example-2.md - 实现前端组件
```

---

# 6. Design Principles

## 6.1 纯编排

Workflow 只负责编排。

```
✅ 
Step 1: 执行 Skill A
Step 2: 执行 Skill B
Step 3: 执行 Skill C

❌ 
Step 1: 分析需求并判断是否需要...
Step 2: 根据复杂度选择不同的设计方案...
```

---

## 6.2 无业务逻辑

Workflow 不包含业务逻辑。

业务逻辑在 Skill 中。

```
✅ 
Step 1: requirement
Step 2: design

❌ 
Step 1: 如果需求简单，跳过设计
Step 2: 如果需求复杂，先做技术调研
```

---

## 6.3 线性流程

优先使用线性流程。

```
✅ 
A → B → C → D

可选：
A → B → C
      ↓
      D
      ↓
      E

❌ 复杂的条件分支和循环
```

---

## 6.4 松耦合

Skill 之间松耦合。

通过输入输出连接。

```
✅ 
Skill A 输出 → Skill B 输入

❌ 
Skill A 直接调用 Skill B
```

---

# 7. Prohibited Patterns

## 7.1 嵌入 Prompt

禁止在 Workflow 中写 Prompt。

```
❌ 
Step 1: 
请分析以下需求，注意要考虑性能、安全性...
[大段 Prompt]
```

Prompt 应该在 Skill 中。

---

## 7.2 条件分支逻辑

避免复杂的条件分支。

```
❌ 
if 需求复杂度 > 8:
    执行完整设计流程
else:
    跳过设计直接编码
```

由 Runtime 决定使用哪个 Workflow。

---

## 7.3 动态 Skill 选择

避免动态选择 Skill。

```
❌ 
根据语言选择不同的 coding skill
```

明确指定 Skill。

---

# 8. Flow Patterns

## 8.1 Sequential（顺序）

最常用模式。

```
A → B → C → D
```

示例：

```
Requirement → Design → Coding → Review
```

---

## 8.2 Parallel（并行）

可选模式。

```
    ┌→ B ┐
A →─┤    ├→ D
    └→ C ┘
```

示例：

```
需求分析
    ├→ 前端设计
    └→ 后端设计
         ↓
       集成
```

---

## 8.3 Optional Steps

可选步骤。

```
A → B → [C] → D

[C] 表示可选
```

示例：

```
Requirement → Design → [Prototype] → Coding
```

---

# 9. Quality Standards

## 9.1 完整性检查

- [ ] 所有 Step 指定明确的 Skill
- [ ] 输入输出定义清晰
- [ ] 错误处理定义完整
- [ ] 提供实际示例

---

## 9.2 可执行性检查

- [ ] 每个 Step 可以独立执行
- [ ] Step 之间依赖关系明确
- [ ] 输入输出可以连接
- [ ] 整体流程合理

---

## 9.3 维护性检查

- [ ] 命名符合规范
- [ ] 文档结构清晰
- [ ] 职责边界明确
- [ ] 易于理解和修改

---

# 10. Metadata

推荐在 WORKFLOW.md 头部添加元数据：

```markdown
---
name: new-feature
version: v1.0.0
category: development
complexity: medium
estimated_time: 30-60min
skills_required: [requirement, design, coding, review, git, document]
author: AOS
created: 2026-07-19
updated: 2026-07-19
---
```

---

# 11. README.md Structure

README.md 提供使用说明。

推荐结构：

```markdown
# Workflow Name

## 简介

## 适用场景

## 使用步骤

## 示例

## 常见问题

## 相关 Workflows
```

---

# 12. Examples Structure

examples/ 目录必须包含完整示例。

每个示例文件结构：

```markdown
# Example: [场景名称]

## Scenario

[场景描述]

## Initial Input

[初始输入]

## Execution

### Step 1: [Skill Name]
Input: [...]
Output: [...]

### Step 2: [Skill Name]
Input: [...]
Output: [...]

...

## Final Output

[最终输出]

## Lessons Learned

[经验教训]
```

---

# 13. Testing

tests/ 目录包含测试用例：

```markdown
# Test Cases

## Test 1: Happy Path

### Input
[测试输入]

### Expected Flow
Step 1 → Step 2 → ... → Step N

### Expected Output
[期望输出]

### Status
✅ Pass

---

## Test 2: Error Handling

### Input
[错误输入]

### Expected Behavior
[期望的错误处理]

### Status
✅ Pass
```

---

# 14. Versioning

Workflow 版本管理：

```
workflow-name/
├── WORKFLOW.md       # 包含版本号
├── CHANGELOG.md      # 变更历史
```

版本格式：

```markdown
Version: v1.0.0
```

变更规则：

- Major: Skill 变更、流程重构
- Minor: 新增可选步骤
- Patch: 文档优化、错误修复

---

# 15. Dependencies

## 15.1 允许依赖

- Skills（核心依赖）
- Knowledge（规范参考）
- Template（输出格式）

---

## 15.2 禁止依赖

- 其它 Workflow
- 特定 Runtime
- 外部系统

---

# 16. Composition

Workflow 不嵌套。

```
✅ 
Workflow A: Skill 1 → Skill 2 → Skill 3
Workflow B: Skill 4 → Skill 5

❌ 
Workflow A: 
  Step 1: Skill 1
  Step 2: 执行 Workflow B
  Step 3: Skill 2
```

---

# 17. Runtime Integration

Runtime 执行 Workflow：

```
1. 读取 WORKFLOW.md
2. 解析 Steps
3. 按序加载 Skills
4. 执行每个 Step
5. 传递输入输出
6. 处理错误
7. 返回结果
```

---

# 18. Validation Checklist

创建 Workflow 前检查：

- [ ] 是否需要 Workflow（单个 Skill 可能就够了）
- [ ] 是否已有类似 Workflow
- [ ] Skills 是否都已存在
- [ ] 流程是否合理
- [ ] 是否纯编排（无业务逻辑）
- [ ] 输入输出是否明确

---

# 19. Review Checklist

Review Workflow 时检查：

- [ ] 文档完整性
- [ ] 纯编排（无业务逻辑）
- [ ] Skills 依赖合理
- [ ] 输入输出连接正确
- [ ] 错误处理完善
- [ ] 示例充分
- [ ] 命名规范

---

# 20. Migration Guide

从复杂 Prompt 迁移到 Workflow：

```
旧方式：
一个超长 Prompt 描述整个流程

↓

新方式：
1. 识别独立步骤
2. 为每个步骤创建 Skill
3. 用 Workflow 组织 Skills
4. 定义输入输出连接
```

---

# 21. Common Patterns

## 21.1 Development Flow

```
Requirement → Design → Coding → Review → Git → Document
```

---

## 21.2 Bug Fix Flow

```
Debug → Coding → Review → Git → Release Note
```

---

## 21.3 Research Flow

```
Research → Analysis → Summary → Document
```

---

## 21.4 Refactor Flow

```
Analysis → Design → Coding → Review → Testing → Git
```

---

# 22. Examples

参考实现：

```
workflows/
├── new-feature/
│   ├── WORKFLOW.md
│   ├── README.md
│   └── examples/
├── bug-fix/
│   ├── WORKFLOW.md
│   ├── README.md
│   └── examples/
└── research/
    ├── WORKFLOW.md
    ├── README.md
    └── examples/
```