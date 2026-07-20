# ADR-0003: Runtime Agnostic

## 状态

`Accepted` · 2026-07-20

## 背景

AI Agent Runtime 市场分散：Claude Code、Codex、Cursor、Gemini CLI、Cline、Roo Code 等。如果 AOS 绑定到某一个 Runtime：

- 用户切换 Runtime 时失去 AOS 能力
- AOS 必须为每个 Runtime 写适配层
- 生态被锁定，无法跨 Runtime 复用能力

## 决策

AOS **严格 Runtime Agnostic**：

- Skill / Workflow / Knowledge / Template 都是纯 Markdown + YAML frontmatter
- 不依赖任何 Runtime 特有 API
- 不内嵌 SDK 调用
- 通过 Runtime 入口文件（CLAUDE.md / AGENT.md 等）做最薄适配

## 备选方案

| 方案 | 优点 | 缺点 |
|---|---|---|
| **当前选择**：Runtime Agnostic | 跨 Runtime、长期稳定、生态友好 | 失去 Runtime 深度集成能力 |
| 绑定 Claude Code | 深度集成 | 用户被锁定 |
| 绑定 Codex | 深度集成 | 用户被锁定 |
| 多 Runtime 适配 | 兼容性好 | 维护成本 ×N |
| 用 Plugin 形式发布 | 自动分发 | 仍需适配每个 Runtime 插件市场 |

## 后果

### 正面

- 一份 Skill 跨多个 Runtime 工作
- AOS 长期稳定（Runtime 变了 AOS 不变）
- 任何新 Runtime 只要支持读取 Markdown 就能用 AOS
- 与开源生态兼容（mattpocock/skills、skills.sh 等）

### 负面

- 无法使用 Runtime 特有能力（如 Claude Code 的 hooks、Codex 的 sub-agent）
- 高级特性需要 Runtime 配合才能实现

### 中性

- 入口文件（CLAUDE.md / AGENT.md）是 Runtime 适配的「适配层」
- 如果未来需要 Runtime 特有能力，可以在入口文件层面扩展，不污染 Skill 本身

## 实施

- `protocols/agent.md` 定义 Runtime 入口文件结构
- `runtimes/` 目录提供每个 Runtime 的入口模板
- 所有 Skill / Workflow / Knowledge 不引用任何 Runtime 私有 API

## 备注

- AOS 哲学第 3 条：「Runtime Agnostic」
- 极端情况下，如果某个 Runtime 完全不支持外部 Markdown 读取，AOS 对其无效——但这种 Runtime 在当前生态中没有