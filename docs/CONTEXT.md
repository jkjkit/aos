# Project Context

> 项目级持久上下文。Runtime 在执行 Skill / Workflow 之前会先读这个文件，了解当前项目的约定与工具链。

---

## 用途

AOS Skill 本身是**通用的工程能力**。但每个项目有自己的语言、框架、目录约定、issue tracker 等。

`CONTEXT.md` 是项目级 hook：把项目特有的信息集中在这里，避免污染通用 Skill，又让 Agent 能按项目定制行为。

---

## 用法

### 在自己的项目中放置

```bash
# 在项目根目录创建
touch CONTEXT.md
```

### 在 AOS Skill 调用前由 Agent 读取

按 AOS 协议，Runtime 在加载 Skill 前应优先读 `CONTEXT.md`（如果存在）。例如：

```text
Runtime 接到任务
   ↓
读 ./CONTEXT.md（如果存在）
   ↓
读取 ~/.agents/MANIFEST.md 发现能力
   ↓
加载匹配的 SKILL.md
   ↓
应用时优先遵守 CONTEXT.md 的项目约定
```

### 模板

复制下面的 YAML/正文到项目的 `CONTEXT.md`，按需删除与填写。

---

## 模板

```markdown
# Project Context

最后更新：YYYY-MM-DD

## 项目基本信息

- 名称：
- 简介（一句话）：
- 主要语言：
- 包管理器：
- 测试框架：
- 部署目标：

## Issue Tracker

- 系统：[GitHub Issues / Linear / Jira / GitLab]
- 链接：
- 标签规范：

## 目录约定

- 源码：
- 测试：
- 配置：
- 文档：

## 代码风格

- 命名：[camelCase / snake_case / kebab-case]
- 缩进：[2 空格 / 4 空格 / Tab]
- 引号：[单引号 / 双引号]
- 分号：[是 / 否]

## 团队约定

- 提交规范：[Conventional Commits / Gitmoji / 自定义]
- 分支模型：[GitHub Flow / Gitflow / Trunk-based]
- Code Review 工具：[GitHub PR / GitLab MR / Phabricator]

## 已知约束

- 不能用的库：
- 必须用的库：
- 性能预算：

## 关键人员

- Tech Lead：
- Reviewers：
- 值班表：

## 不在范围内

- （列出本项目明确不做的事）
```

---

## 与 Skill 的关系

| 维度 | Skill | CONTEXT.md |
|---|---|---|
| 范围 | 通用 / 跨项目 | 当前项目特有 |
| 修改频率 | 随 AOS 版本演进 | 随项目本身演进 |
| 位置 | `~/.agents/skills/<name>/SKILL.md` | 项目根目录 `CONTEXT.md` |
| 谁维护 | AOS 维护者 | 项目成员 |
| 影响 | 所有项目 | 当前项目 |

**原则：** 能放进 `CONTEXT.md` 的项目约定不要硬编码进 Skill，保持 Skill 的通用性。

---

## 示例

参考 `examples/todo-app/CONTEXT.md`（如有）。
---

## 项目目录结构示例

以下是「Agent 协作开发」项目的典型目录结构，**仅作示例，不强制要求**：

```text
project-root/
├── main/                 # 项目源代码（可修改）
├── temp/                 # 临时文件（不提交）
├── imgs/                 # 图片 / 视频
├── docs/                 # 参考文档（只读）
├── agent.md              # 系统约束（Runtime 入口）
├── requirements.md       # 需求：要做什么
├── architecture.md       # 架构：应该怎么做
├── phasetasks.md         # 任务：现在做什么
├── progress.md           # 进度：做到哪里了
└── risk.md               # 风险：不踩哪些坑
```

### 与 AOS 的关系

| Agent 工作流文档 | AOS 对应物 |
|------------------|-----------|
| `requirements.md` | `requirement` Skill 产出 |
| `architecture.md` | `design` Skill 产出 |
| `phasetasks.md` | `task` Skill 产出 |
| `progress.md` | 由 `git` Skill 维护 |
| `risk.md` | `risk-analysis` Skill 产出 |

### 读写规则

```text
读：requirements.md、architecture.md、phasetasks.md、progress.md
写：phasetasks.md、progress.md、risk.md
可修改：main/、temp/ 下的文件
只读：docs/
```

### 核心纪律

- **文档优先**：任何开发前必须先读项目文档，不能根据聊天猜测需求
- **文件不存在先询问**：不得自行初始化项目文档
- **agent.md 不得自改**：变更需用户明确指示
- **用户口头指令与文档冲突时先确认**
- **对话过长时主动同步关键决策到 progress.md**

---

## 参考

- [mattpocock/skills](https://github.com/mattpocock/skills) — Real Engineering
- [docs/adr/](adr/) — 架构决策记录
