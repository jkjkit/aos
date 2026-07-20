# Output Protocol

Version: v0.2.0

Status: Draft

---

# 1. Purpose

Output Protocol 定义所有模块的输出标准。

本协议确保：

- 输出格式统一
- 结构清晰一致
- 易于解析和使用
- 便于模块组合

---

# 2. Definition

Output 是 Skill、Workflow 的执行结果。

Output：

格式统一。

结构标准。

内容完整。

---

# 3. General Principles

## 3.1 统一结构

所有输出遵循统一结构：

```markdown
# Summary

# Analysis

# Recommendations

# Next Steps
```

---

## 3.2 清晰分层

输出分为多个层次：

- Summary: 概要
- Detail: 详细内容
- Action: 可执行建议

---

## 3.3 可组合性

输出应该：

- 可被后续 Skill 使用
- 可被 Workflow 传递
- 可被用户直接阅读

---

# 4. Standard Output Structure

## 4.1 基础结构

```markdown
# Summary

[一句话概述结果]

# Analysis

[详细分析内容]

# Recommendations

[建议和改进点]

# Next Steps

[后续行动项]
```

---

## 4.2 必需章节

### Summary

- 位置：最前面
- 长度：1-3 句话
- 内容：核心结论

示例：

```markdown
# Summary

代码 Review 完成。发现 3 个潜在问题，2 个改进建议。总体质量良好，建议修复问题后合并。
```

---

### Analysis

- 位置：Summary 之后
- 长度：根据需要
- 内容：详细分析

示例：

```markdown
# Analysis

## Issues Found

### Issue 1: Potential Null Pointer

**Location:** `src/utils.ts:45`

**Description:** 
变量 `user` 可能为 null，未做空值检查。

**Impact:** 
运行时可能抛出异常。

**Severity:** High

---

### Issue 2: Performance Concern

**Location:** `src/service.ts:120`

**Description:**
在循环中执行数据库查询。

**Impact:**
N+1 查询问题，影响性能。

**Severity:** Medium
```

---

### Recommendations

- 位置：Analysis 之后
- 长度：根据需要
- 内容：可执行建议

示例：

```markdown
# Recommendations

## Priority: High

1. **添加空值检查**
   - 文件：`src/utils.ts:45`
   - 方法：添加 `if (user === null)` 检查
   - 预期：消除运行时异常风险

## Priority: Medium

2. **优化数据库查询**
   - 文件：`src/service.ts:120`
   - 方法：使用批量查询或缓存
   - 预期：提升性能 10x
```

---

### Next Steps

- 位置：最后
- 长度：简洁
- 内容：明确行动

示例：

```markdown
# Next Steps

- [ ] 修复 Issue 1 和 Issue 2
- [ ] 运行测试确保修复有效
- [ ] 再次 Review
- [ ] 合并代码
```

---

## 4.3 可选章节

根据 Skill 类型添加：

```markdown
# Metadata

[元信息]

# Appendix

[附录]

# References

[参考资料]
```

---

# 5. Format Standards

## 5.1 Markdown

使用标准 Markdown：

```markdown
# 一级标题
## 二级标题
### 三级标题

- 列表项
- [ ] 待办事项
- [x] 已完成事项

**粗体**
*斜体*
`代码`

\`\`\`language
代码块
\`\`\`

> 引用

[链接](url)
```

---

## 5.2 代码块

使用语言标识：

```markdown
\`\`\`typescript
const user = getUser();
\`\`\`

\`\`\`python
def get_user():
    return user
\`\`\`
```

---

## 5.3 表格

使用 Markdown 表格：

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Value 1  | Value 2  | Value 3  |
```

---

## 5.4 清单

使用标准清单格式：

```markdown
- [ ] 待办项 1
- [x] 已完成项
- [ ] 待办项 2
```

---

# 6. Severity Levels

## 6.1 标准级别

```
Critical    严重：立即修复
High        高：优先修复
Medium      中：计划修复
Low         低：可选修复
Info        信息：无需修复
```

---

## 6.2 使用方式

```markdown
**Severity:** High
```

或

```markdown
🔴 Critical
🟠 High
🟡 Medium
🟢 Low
🔵 Info
```

---

# 7. Status Indicators

## 7.1 标准状态

```
✅ Success / Completed / Approved
⚠️  Warning / Needs Attention
❌ Error / Failed / Rejected
🔄 In Progress
⏸️  Paused
⏭️  Skipped
```

---

## 7.2 使用示例

```markdown
## Status

✅ Code quality check passed
⚠️  Performance optimization needed
❌ Security vulnerability found
```

---

# 8. Skill-Specific Output

## 8.1 Summary Skill

```markdown
# Summary

原文档约 5000 字，涵盖 [主题]。

# Key Points

1. [要点 1]
2. [要点 2]
3. [要点 3]

# Details

## [主题 1]

[详细内容]

## [主题 2]

[详细内容]

# Recommendations

[建议]

# Next Steps

- [ ] [行动项]
```

---

## 8.2 Coding Skill

```markdown
# Summary

功能实现完成。新增 [文件数] 个文件，[行数] 行代码。

# Implementation

## Files Created

- `src/feature.ts` - 核心实现
- `tests/feature.test.ts` - 测试

## Code

\`\`\`typescript
[关键代码]
\`\`\`

# Testing

\`\`\`bash
npm test
\`\`\`

# Next Steps

- [ ] Code Review
- [ ] Integration Test
```

---

## 8.3 Review Skill

```markdown
# Summary

Review 完成。发现 [数量] 个问题，[数量] 个建议。

# Issues Found

## Critical

[严重问题]

## High Priority

[高优先级问题]

## Medium Priority

[中优先级问题]

# Suggestions

[改进建议]

# Approval Status

✅ Approved / ⚠️ Approved with comments / ❌ Changes requested

# Next Steps

- [ ] [修复项]
```

---

## 8.4 Design Skill

```markdown
# Summary

设计完成。包含 [组件数] 个组件，[API 数] 个 API。

# Architecture

\`\`\`
[架构图或描述]
\`\`\`

# Components

## Component 1

**Purpose:** [用途]
**Interface:** [接口]
**Dependencies:** [依赖]

# API Design

## Endpoint 1

\`\`\`
GET /api/resource
\`\`\`

**Request:** [请求格式]
**Response:** [响应格式]

# Recommendations

[建议]

# Next Steps

- [ ] Review 设计
- [ ] 开始实现
```

---

## 8.5 Debug Skill

```markdown
# Summary

Bug 定位完成。根因是 [原因]。

# Analysis

## Symptoms

[症状描述]

## Root Cause

[根本原因]

## Evidence

[证据]

# Recommendations

## Fix

[修复方案]

## Prevention

[预防措施]

# Next Steps

- [ ] 实现修复
- [ ] 添加测试
- [ ] 验证修复
```

---

# 9. Metadata

## 9.1 推荐 Metadata

```markdown
# Metadata

- Skill: [Skill 名称]
- Version: [Skill 版本]
- Timestamp: [时间戳]
- Duration: [执行时长]
- Status: [状态]
```

---

## 9.2 可选 Metadata

```markdown
# Metadata

- Input Hash: [输入哈希]
- Context: [上下文信息]
- Model: [使用的模型]
- Token Count: [Token 数量]
```

---

# 10. Error Output

## 10.1 错误格式

```markdown
# Error

执行失败：[错误信息]

# Details

**Error Type:** [错误类型]
**Location:** [位置]
**Message:** [详细信息]

# Cause

[可能原因]

# Recommendations

[解决建议]

# Next Steps

- [ ] [修复步骤]
```

---

## 10.2 示例

```markdown
# Error

Skill 执行失败：文件未找到

# Details

**Error Type:** FileNotFoundError
**Location:** `src/missing-file.ts`
**Message:** ENOENT: no such file or directory

# Cause

可能原因：

1. 文件路径错误
2. 文件已被删除
3. 权限不足

# Recommendations

1. 检查文件路径是否正确
2. 确认文件是否存在
3. 检查文件权限

# Next Steps

- [ ] 验证文件路径
- [ ] 重新执行
```

---

# 11. Validation

## 11.1 输出验证清单

- [ ] 包含 Summary
- [ ] 结构符合标准
- [ ] Markdown 格式正确
- [ ] 内容完整
- [ ] 可读性好
- [ ] 可执行性强（如有建议）

---

## 11.2 质量标准

### Clarity（清晰）

- 语言简洁
- 逻辑清晰
- 重点突出

### Completeness（完整）

- 包含必需章节
- 信息完整
- 无遗漏

### Actionability（可执行）

- 建议具体
- 步骤明确
- 可以执行

---

# 12. Multi-Language Support

## 12.1 语言选择

输出语言：

- 跟随用户输入语言
- 或在 Skill 中明确指定

---

## 12.2 示例

用户使用中文：

```markdown
# 摘要

代码审查完成。发现 3 个问题。

# 分析

...
```

用户使用英文：

```markdown
# Summary

Code review completed. Found 3 issues.

# Analysis

...
```

---

# 13. Workflow Output

## 13.1 Workflow 输出结构

```markdown
# Summary

Workflow 完成。执行了 [步骤数] 个步骤。

# Steps Executed

## Step 1: [Skill Name]

**Status:** ✅ Success

**Output Summary:**
[Step 输出摘要]

**Duration:** [时长]

---

## Step 2: [Skill Name]

**Status:** ✅ Success

**Output Summary:**
[Step 输出摘要]

**Duration:** [时长]

# Final Deliverables

- [交付物 1]
- [交付物 2]

# Overall Status

✅ Success / ⚠️ Partial Success / ❌ Failed

# Next Steps

- [ ] [后续行动]
```

---

## 13.2 失败处理

```markdown
# Summary

Workflow 执行失败。在 Step [N] 失败。

# Steps Executed

## Step 1: [Skill Name]

**Status:** ✅ Success

## Step 2: [Skill Name]

**Status:** ❌ Failed

**Error:** [错误信息]

# Recovery Options

1. [恢复选项 1]
2. [恢复选项 2]

# Next Steps

- [ ] [修复步骤]
```

---

# 14. Integration

## 14.1 输出传递

Step 1 输出作为 Step 2 输入：

```markdown
# Step 1 Output

# Summary
[内容]

# Analysis
[内容]

↓

# Step 2 Input

使用 Step 1 的 Analysis 部分
```

---

## 14.2 输出转换

根据需要提取：

```markdown
Step 1 完整输出
↓
提取 Key Points
↓
作为 Step 2 输入
```

---

# 15. Template Integration

## 15.1 使用 Template

```markdown
# Output

使用 Template: prd

填充内容：
[生成的内容]
```

---

## 15.2 格式化

```markdown
原始输出
↓
应用 Template
↓
格式化输出
```

---

# 16. Best Practices

## 16.1 摘要优先

最重要的信息放在 Summary。

---

## 16.2 结构清晰

使用标题和列表。

保持层次清晰。

---

## 16.3 可执行性

建议具体可执行。

Next Steps 明确清晰。

---

## 16.4 一致性

同类 Skill 输出格式一致。

---

# 17. Examples

## 17.1 简单输出

```markdown
# Summary

功能实现完成。

# Analysis

实现了用户登录功能，包括：
- 用户名密码验证
- Session 管理
- 错误处理

# Recommendations

建议添加：
- 密码强度检查
- 登录失败限制

# Next Steps

- [ ] Code Review
- [ ] 测试
```

---

## 17.2 复杂输出

```markdown
# Summary

完整的需求分析完成。识别出 5 个核心功能，3 个非功能需求。

# Analysis

## Functional Requirements

### FR1: User Authentication

**Description:**
用户需要能够注册、登录、登出。

**User Story:**
作为用户，我想要能够注册账号，以便使用系统功能。

**Acceptance Criteria:**
- [ ] 支持邮箱注册
- [ ] 密码强度验证
- [ ] 邮箱验证

### FR2: Profile Management

...

## Non-Functional Requirements

### NFR1: Performance

- 响应时间 < 200ms
- 支持 1000 并发用户

### NFR2: Security

- 密码加密存储
- HTTPS only
- SQL 注入防护

# Recommendations

1. 优先实现核心认证功能
2. 性能要求需要负载测试验证
3. 安全要求需要专项 Review

# Next Steps

- [ ] 设计架构
- [ ] 技术选型
- [ ] 开始开发
```

---

# 18. Prohibited Patterns

## 18.1 混乱结构

```
❌ 
内容堆砌，无结构
段落连续，无标题
信息混乱
```

---

## 18.2 过度简单

```
❌ 
# Summary
完成了。

# Next Steps
继续。
```

---

## 18.3 过度复杂

```
❌ 
10 层标题嵌套
1000 行输出
无重点内容
```

---

# 19. Validation Checklist

输出前检查：

- [ ] 包含 Summary
- [ ] 结构完整
- [ ] Markdown 正确
- [ ] 内容清晰
- [ ] 建议可执行
- [ ] Next Steps 明确
- [ ] 格式统一

---

# 20. Review Checklist

Review 输出时检查：

- [ ] 符合标准结构
- [ ] 内容完整准确
- [ ] 格式规范
- [ ] 可读性好
- [ ] 可执行性强
- [ ] 无语法错误
- [ ] 逻辑连贯
