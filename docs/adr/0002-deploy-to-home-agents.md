# ADR-0002: AOS 部署到 ~/.agents/

## 状态

`Accepted` · 2026-07-20

## 背景

AOS 的设计目标是为多个 AI Runtime（Claude Code、Codex、Cursor、Gemini CLI 等）提供统一的 Agent 能力。

需要选择一个**部署目录**：

- 选项 A：每个 Runtime 自己的配置目录（`~/.claude/`、`~/.codex/` ...）
- 选项 B：AOS 自己的目录（`~/.aos/`）
- 选项 C：Runtime 无关的共享目录（`~/.agents/`）

## 决策

AOS 部署到 **`~/.agents/`**，供所有 Runtime 共享。

各 Runtime 的入口文件（`~/.claude/CLAUDE.md` / `~/.codex/AGENT.md` 等）只声明「AOS 在 `~/.agents/`」并指向能力索引 `MANIFEST.md`。

## 备选方案

| 方案 | 优点 | 缺点 |
|---|---|---|
| **当前选择**：`~/.agents/` | Runtime 共享、配置简单、与已有 `find-skills` 等工具兼容 | 需要让 Runtime 主动读 |
| `~/.aos/` | 命名清晰 | 引入新抽象层、需额外配置 |
| 各 Runtime 独立部署 | 隔离性好 | 重复维护、无法共享 Skill |

## 后果

### 正面

- 一处部署，所有 Runtime 都能用
- 与 mattpocock/skills、skills.sh 等生态的目录约定一致
- AOS 不需要为每个 Runtime 写适配代码
- 第三方 Skill（如 `find-skills`、`code-review`）可以无冲突共存

### 负面

- Runtime 必须支持读取外部目录的 Markdown（绝大多数现代 Runtime 都支持）
- 如果 Runtime 不支持，入口文件需要变通（如把 Skill 内容嵌入提示词）

### 中性

- 需要维护 deploy 脚本（已通过 `deploy.sh` / `deploy.ps1` 实现）
- 第三方 Skill 的 frontmatter 格式必须兼容；当前生态已统一为 `name` + `description`

## 实施

- `deploy.sh` / `deploy.ps1`：把 `skills/`、`workflows/`、`protocols/`、`templates/`、`knowledge/` 复制到 `~/.agents/`
- 入口文件：`runtimes/claude.md` → `~/.claude/CLAUDE.md`，声明 AOS Root
- 能力索引：`MANIFEST.md` 描述所有可用能力

## 备注

- `~/.agents/skills/` 是 skills.sh 生态的标准目录
- 大部分 Runtime（Claude Code、Codex、Cursor、Gemini CLI）都支持读取这个目录
- ADR 不可随意改：路径变更会影响所有已部署用户