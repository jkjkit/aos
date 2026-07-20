# Todo App - 待办事项应用

完整的项目示例，展示如何使用 AOS 从需求到部署的全流程。

---

## 📋 项目概述

一个简单的待办事项管理应用，用于演示 AOS 的完整使用流程。

**技术栈：**
- 前端：React + TypeScript
- 后端：Node.js + Express
- 数据库：MongoDB
- 部署：Docker + Kubernetes

---

## 🎯 AOS 使用流程

### Phase 1: 需求分析

**使用：** `requirement` skill

```bash
# 查看需求分析文档
cat 01-requirement.md
```

**输出：**
- 用户故事
- 功能需求
- 非功能需求
- 验收标准

---

### Phase 2: 任务分解

**使用：** `task` skill

```bash
# 查看任务分解
cat 02-tasks.md
```

**输出：**
- 开发任务列表
- 优先级排序
- 时间估算

---

### Phase 3: 技术研究

**使用：** `research` skill

```bash
# 查看技术选型
cat 03-research.md
```

**输出：**
- 技术选型方案
- 技术可行性分析
- 风险评估

---

### Phase 4: 架构设计

**使用：** `design` skill

```bash
# 查看架构设计
cat 04-design.md
```

**输出：**
- 系统架构图
- 数据库设计
- API 设计
- 技术栈选择

---

### Phase 5: 代码实现

**使用：** `coding` skill + `new-feature` workflow

```bash
# 查看实现指南
cat 05-coding.md

# 查看代码示例
ls src/
```

**输出：**
- 代码实现
- 单元测试
- 集成测试

---

### Phase 6: 代码审查

**使用：** `review` skill + `code-review` workflow

```bash
# 查看审查报告
cat 06-review.md
```

**输出：**
- 代码审查报告
- 问题清单
- 改进建议

---

### Phase 7: 问题调试

**使用：** `debug` skill

```bash
# 查看调试记录
cat 07-debug.md
```

**输出：**
- 问题定位
- 解决方案
- 测试验证

---

### Phase 8: 文档编写

**使用：** `document` skill

**输出：**
- README.md
- API 文档
- 部署文档

```bash
# 查看文档
cat 08-documentation/
```

---

### Phase 9: 版本控制

**使用：** `git` skill + `git-workflow` knowledge

```bash
# 查看 Git 工作流
cat 09-git-workflow.md
```

**输出：**
- Git 提交记录
- 分支管理
- PR 流程

---

### Phase 10: 部署发布

**使用：** `deployment` workflow + `release` workflow

```bash
# 查看部署文档
cat 10-deployment.md

# 查看发布说明
cat 11-release.md
```

**输出：**
- 部署配置
- 发布说明
- 回滚方案

---

## 📂 项目结构

```
todo-app/
├── README.md                    本文件
├── 01-requirement.md            需求分析
├── 02-tasks.md                  任务分解
├── 03-research.md               技术研究
├── 04-design.md                 架构设计
├── 05-coding.md                 实现指南
├── 06-review.md                 审查报告
├── 07-debug.md                  调试记录
├── 08-documentation/            项目文档
│   ├── README.md
│   ├── API.md
│   └── DEPLOYMENT.md
├── 09-git-workflow.md           Git 工作流
├── 10-deployment.md             部署文档
├── 11-release.md                发布说明
└── src/                         代码示例
    ├── frontend/
    ├── backend/
    └── tests/
```

---

## 🎓 学习要点

### 1. 标准化流程

完整的 11 个阶段，覆盖从需求到部署的全流程。

### 2. 文档驱动

每个阶段都有详细的文档，确保清晰的沟通。

### 3. 质量保证

代码审查、测试、调试的完整流程。

### 4. 最佳实践

遵循 AOS 的设计原则和最佳实践。

---

## 🚀 如何使用

### 学习示例

1. 按顺序阅读每个阶段的文档
2. 理解 AOS 的使用方式
3. 学习最佳实践

### 应用到项目

1. 复制这个结构
2. 根据项目调整内容
3. 遵循相同的流程

---

## 📊 时间估算

| 阶段 | 时间 | 说明 |
|------|------|------|
| 需求分析 | 2-4 小时 | requirement skill |
| 任务分解 | 1-2 小时 | task skill |
| 技术研究 | 4-8 小时 | research skill |
| 架构设计 | 4-6 小时 | design skill |
| 代码实现 | 2-3 周 | coding skill |
| 代码审查 | 2-4 小时 | review skill |
| 问题调试 | 按需 | debug skill |
| 文档编写 | 4-8 小时 | document skill |
| 版本控制 | 持续 | git skill |
| 部署发布 | 4-8 小时 | deployment workflow |

**总计：** 约 3-4 周（小型项目）

---

## 🎯 关键收益

### 效率提升

- 清晰的流程，减少返工
- 标准化的文档，减少沟通成本
- 复用的模板，加快开发速度

### 质量保证

- 完整的审查流程
- 标准化的测试
- 文档化的最佳实践

### 团队协作

- 统一的工作方式
- 清晰的交付标准
- 便于知识传承

---

## 📚 相关资源

**Skills：**
- [requirement skill](../../skills/requirement/README.md)
- [design skill](../../skills/design/README.md)
- [coding skill](../../skills/coding/README.md)
- [review skill](../../skills/review/README.md)

**Workflows：**
- [new-feature workflow](../../workflows/new-feature/WORKFLOW.md)
- [deployment workflow](../../workflows/deployment/WORKFLOW.md)

**Knowledge：**
- [coding-style](../../knowledge/coding-style/KNOWLEDGE.md)
- [git-workflow](../../knowledge/git-workflow/KNOWLEDGE.md)

---

**Build Once. Run Everywhere.**

**AOS - Agent Operating System**
