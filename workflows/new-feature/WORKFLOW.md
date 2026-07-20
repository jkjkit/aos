# New Feature Development Workflow

---

# Purpose

完整的新功能开发流程，从需求分析到代码提交和文档更新。

---

# Trigger

使用此 Workflow 当：

- 需要开发新功能
- 有明确的功能需求描述
- 需要完整的开发流程（需求 → 设计 → 实现 → 审查）
- 功能具有一定复杂度

不使用此 Workflow 当：

- 简单的 Bug 修复（使用 bug-fix workflow）
- 代码重构（使用 refactor workflow）
- 文档更新（直接使用 document skill）
- 快速原型（可跳过部分步骤）

---

# Skills

本 Workflow 使用以下 Skills：

1. **requirement** - 需求分析
2. **design** - 架构设计
3. **database** - 数据模型设计（如涉及）
4. **coding** - 代码实现
5. **testing** - 测试用例设计与补齐
6. **security** - 安全审查（如涉及认证、敏感数据）
7. **review** - 代码审查
8. **git** - 版本管理
9. **document** - 文档更新

---

# Steps

## Step 1: Requirement Analysis

**Skill:** requirement

**Input:** 
- 用户功能需求描述
- 相关背景信息（可选）
- 约束条件（可选）

**Output:** 
- 结构化需求文档
- 功能规格说明
- 验收标准

**Duration:** 10-20 min

---

## Step 2: Architecture Design

**Skill:** design

**Input:** 
- 需求文档（来自 Step 1）
- 现有系统架构
- 技术栈约束

**Output:** 
- 架构设计文档
- 组件设计
- API 设计
- 数据模型

**Duration:** 15-30 min

---

## Step 3: Implementation

**Skill:** coding

**Input:** 
- 设计文档（来自 Step 2）
- 代码库路径
- 编码规范（来自 Knowledge）

**Output:** 
- 实现代码
- 单元测试
- 代码注释

**Duration:** 30-60 min

---

## Step 3.5: Testing

**Skill:** testing

**Input:**
- 实现代码（来自 Step 3）
- 覆盖率目标

**Output:**
- 测试用例
- 覆盖率报告

**Duration:** 15-25 min

---

## Step 3.6: Security Review (可选)

**Skill:** security

**Input:**
- 实现代码
- 涉及认证、授权或敏感数据的接口

**Output:**
- 安全审查发现
- 修复建议

**Duration:** 10-20 min

---

## Step 4: Code Review

**Skill:** review

**Input:** 
- 实现代码（来自 Step 3）
- 编码规范（来自 Knowledge）
- Review 清单

**Output:** 
- Review 报告
- 问题列表
- 改进建议
- 审批状态

**Duration:** 10-20 min

**Decision Point:**
- ✅ Approved → 继续 Step 5
- ⚠️ Approved with comments → 修复后继续
- ❌ Changes requested → 返回 Step 3 修复

---

## Step 5: Git Commit

**Skill:** git

**Input:** 
- 已审查的代码
- Git 仓库路径
- Commit 规范

**Output:** 
- Git commit 记录
- 分支信息
- Push 状态

**Duration:** 5 min

---

## Step 6: Documentation

**Skill:** document

**Input:** 
- 完整实现（来自 Step 3）
- 设计文档（来自 Step 2）
- 现有文档

**Output:** 
- 更新的 README
- API 文档（如适用）
- 使用说明

**Duration:** 10-15 min

---

# Input

## Required

- **功能需求描述**：清晰的功能说明
- **代码库路径**：目标代码库位置

## Optional

- **设计约束**：技术栈、性能要求等
- **时间要求**：预期完成时间
- **优先级**：功能优先级

---

# Output

## Final Deliverables

1. **需求文档** - 结构化的需求规格
2. **设计文档** - 架构和 API 设计
3. **实现代码** - 包含测试的代码
4. **Review 报告** - 代码审查结果
5. **Git Commit** - 提交记录
6. **更新文档** - README 和 API 文档

## Format

每个 Step 的输出保持原始格式，最终汇总所有交付物。

---

# Error Handling

## Step 失败处理

### Step 1-2 失败

**原因：** 需求不清晰、设计不可行

**处理：**
1. 暂停 Workflow
2. 与用户澄清需求
3. 从失败的 Step 重新开始

**回滚：** 无需回滚

---

### Step 3 失败

**原因：** 编译错误、测试失败、实现困难

**处理：**
1. 检查错误日志
2. 返回 Step 2 检查设计
3. 或直接修复实现问题
4. 重新执行 Step 3

**回滚：** 保留代码，标记为 WIP

---

### Step 4 失败

**原因：** Review 发现问题

**处理：**
1. 根据 Review 意见修复
2. 返回 Step 3 修改代码
3. 重新执行 Step 4

**回滚：** 保留代码和 Review 意见

---

### Step 5-6 失败

**原因：** Git 冲突、文档问题

**处理：**
1. 解决冲突或修复文档
2. 重新执行失败的 Step

**回滚：** 如需要，使用 git reset

---

## 重试策略

- **自动重试：** 不支持
- **手动重试：** 允许从任意 Step 重新开始
- **部分重试：** 可只重试失败的 Step

---

## 回滚策略

### 代码回滚

```bash
# 回滚到开始前状态
git reset --hard <commit-before-start>
```

### 文档回滚

保留 git 历史，手动恢复文档。

---

# Examples

参见：

- `examples/example-api-endpoint.md` - 开发 REST API 端点
- `examples/example-ui-component.md` - 实现前端组件

---

# Quality Checks

## Workflow 级别检查

执行完成后验证：

- [ ] 所有 6 个 Step 都已完成
- [ ] 每个 Step 的输出完整
- [ ] 代码通过 Review
- [ ] Git commit 成功
- [ ] 文档已更新

---

## 交付物检查

- [ ] 需求文档清晰完整
- [ ] 设计文档合理可行
- [ ] 代码可编译运行
- [ ] 测试覆盖充分
- [ ] 通过 Code Review
- [ ] Git 历史清晰
- [ ] 文档更新正确

---

# Variations

## 简化版（用于简单功能）

跳过 Step 2（设计），直接从需求到编码：

```
Step 1: Requirement
↓
Step 3: Coding
↓
Step 4: Review
↓
Step 5: Git
↓
Step 6: Document
```

---

## 扩展版（用于复杂功能）

在 Step 3 和 Step 4 之间增加测试步骤：

```
Step 1: Requirement
↓
Step 2: Design
↓
Step 3: Coding
↓
Step 3.5: Testing
↓
Step 4: Review
↓
Step 5: Git
↓
Step 6: Document
```

---

# Related Workflows

- **bug-fix** - Bug 修复流程（更轻量）
- **refactor** - 代码重构流程
- **research** - 技术研究流程（无实现）
- **project-init** - 新项目初始化

---

# Metrics

## 成功指标

- 完成率 > 95%
- Review 通过率 > 90%
- 平均完成时间 < 90 分钟

## 跟踪数据

- 每个 Step 的执行时间
- 失败的 Step 和原因
- 重试次数

---

# Best Practices

1. **需求先行** - 确保 Step 1 输出清晰后再继续
2. **设计验证** - Step 2 完成后与团队确认设计方案
3. **小步提交** - Step 5 提交应该是小的、原子的变更
4. **文档同步** - Step 6 应该与代码同时更新
5. **持续 Review** - 不要等到最后才做 Review

---

# Version History

## v1.0.0 - 2026-07-19

- Initial release
- 6-step workflow
- 基础错误处理
- 示例和最佳实践

---
