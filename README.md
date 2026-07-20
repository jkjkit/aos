# AOS - Agent Operating System

> Build Once. Run Everywhere.

一套面向 AI Agent 的工程化能力框架。部署到 `~/.agents/`，供不同 AI Runtime 自动发现、准确匹配并按需调用。

---

## 它解决什么问题

随着 AI Agent 深入研发和业务流程，Prompt / Skill 越来越多，但常见问题也越来越明显：

- 能力重复建设，无法跨 Runtime 复用
- Skill 职责重叠，Runtime 容易按关键词误匹配
- 输出格式混乱，多阶段工作无法稳定编排
- 一次加载过多上下文，Token 消耗持续增长

AOS 通过统一的 Protocol、结构化 Skill、Workflow 和显式路由规则组织能力。任何支持读取 Markdown 的 AI Runtime 都能使用。

---

## 支持的 Runtime

- Claude Code
- Codex
- Cursor
- Gemini CLI
- Cline / Roo Code
- 任何支持读取 Markdown 的 AI Agent

---

## 一键部署

默认使用轻量 `core` Profile，并把非 AOS 第三方 Skill 隔离到 `~/.agents/packs/third-party/skills/`：

**Windows（PowerShell）：**

```powershell
.\deploy.ps1 -Profile core -ThirdParty isolate
```

**macOS / Linux / Git Bash：**

```bash
bash deploy.sh core isolate
```

可选 Profile：

| Profile | Skill 数 | 用途 |
|---|---:|---|
| `core`（默认） | 31 | 日常研发与运维，优先控制启动上下文 |
| `ai` | 34 | `core` + Prompt、上下文工程、LLM 评估 |
| `design` | 38 | `core` + 产品研究、内容和可访问性设计 |
| `full` | 50 | 全部 AOS Skill，用于能力探索和维护 |

Third-party policies are `isolate`, `keep`, and `restore`. The deployment scripts regenerate the Router/Manifest, activate only the selected AOS Skills, and write `.aos-managed-skills.json`. **By default, deployment updates only `~/.agents/`; it does not overwrite user-owned Claude, Codex, or Cursor entry files.**

To use the Runtime entry templates bundled with this repository, install them explicitly (this overwrites the corresponding files):

```powershell
.\deploy.ps1 -Profile core -ThirdParty isolate -InstallRuntime
```

```bash
AOS_INSTALL_RUNTIME=1 bash deploy.sh core isolate
```

Explicit Runtime installation writes:

- `~/.claude/CLAUDE.md`
- `~/.codex/AGENT.md`
- `~/.cursor/rules/aos.md`

After deployment, a Runtime uses its registered Skill Catalog first. It reads the lightweight `ROUTER.md` only when matching remains ambiguous; it does not read the complete `MANIFEST.md` on every turn.

---

## Simple workspace convention

AOS is a shared capability library. Keep real projects outside the AOS directory:

```text
D:\AOS/                 # AOS source, Skills, and deployment scripts
D:\Work\Project-1/      # Real project code (its own Git repository)
```

Keep the rules minimal:

1. Do not put real projects under `D:\AOS`.
2. `D:\Work` is only a project container, not a Git repository; each `Project-*` owns its Git history.
3. Change into the target project directory before development, builds, tests, or starting an Agent.
4. Add a short project-level `AGENTS.md` only for project-specific constraints; do not copy AOS content into it.

See [Workspace convention](docs/Workspace.md) for a complete example.

---

## 仓库结构与部署目标

仓库是 AOS 的源码和维护环境；部署脚本把运行所需内容整理到 `~/.agents/`。

**仓库：**

```text
AOS/
├── README.md                  # 项目说明
├── ROUTER.md                  # 默认 Profile 的轻量 Runtime 路由
├── routers/                   # core / ai / design / full Router
├── MANIFEST.md                # 自动生成的完整能力目录
├── CHANGELOG.md
├── deploy.sh
├── deploy.ps1
├── data/
│   ├── skill-routing.json     # 高混淆 Skill 的显式路由规则
│   ├── skill-profiles.json    # 活动 Skill Profile
│   ├── context-budgets.json   # Runtime / Router / Skill 上下文预算
│   └── skill-roles.json       # 岗位标签
├── runtimes/                  # 各 Runtime 轻量入口文件模板
├── protocols/                 # 8 个内部协议文件
├── skills/                    # 50 个 Skill
├── workflows/                 # 5 个 Workflow
├── templates/                 # 7 个文档模板
├── knowledge/                 # 6 个知识模块
├── scripts/                   # Manifest、lint、路由回归、反馈与健康度工具
├── tests/skill-routing/       # Skill / Workflow 匹配回归语料
├── docs/                      # 设计和维护文档（不部署）
└── examples/                  # 示例（不部署）
```

**部署目标：**

```text
~/.agents/
├── ROUTER.md                  # 当前 Profile 的轻量路由
├── MANIFEST.md                # 完整目录，仅用于发现和维护
├── .aos-managed-skills.json   # 当前 Profile 与托管 Skill 清单
├── protocols/
├── skills/                    # 只包含当前 Profile + 按策略保留的第三方 Skill
├── packs/third-party/skills/  # 被隔离的第三方 Skill
├── workflows/
├── templates/
└── knowledge/
```

`docs/`、`examples/`、`data/`、`tests/`、部署脚本和 `routers/` 是仓库维护资料，不整体进入 `~/.agents/`；部署时仅把所选 `routers/<profile>.md` 写成 `~/.agents/ROUTER.md`。

---

## Skills

当前仓库包含 50 个原子 Skill，覆盖以下主要领域：

| 能力组 | 代表 Skill |
|---|---|
| 需求、设计与实现 | `requirement`、`design`、`design-interface`、`api-design`、`database`、`coding` |
| 代码库理解与变更 | `codebase-exploration`、`change-impact-analysis` |
| AI 系统设计与评估 | `prompt-writing`、`context-engineering`、`llm-evaluation` |
| 代码质量、可访问性与隐私 | `testing`、`review`、`accessibility-audit`、`security`、`privacy-review`、`debug`、`verification`、`performance` |
| 研究、产品与数据 | `research`、`competitive-analysis`、`user-research`、`data-analysis`、`metrics-design`、`ab-testing` |
| 文档、内容与能力定义 | `document`、`skill-authoring`、`changelog`、`meeting-notes`、`faq-generation`、`copywriting` |
| 客服与运营 | `support-triage`、`cs-response`、`customer-recovery` |
| 通用协作 | `grill`、`summary`、`task`、`brainstorm`、`git` |

日常匹配使用 `ROUTER.md`；完整清单和岗位索引仅在能力发现或维护时查看 `MANIFEST.md`。

---

## 5 个 Workflows

| Workflow | 用途 |
|---|---|
| `new-feature` | 完整的新功能开发流程 |
| `bug-fix` | Bug 复现 → 根因 → 修复 → 回归 |
| `code-review` | 代码审查流程 |
| `deployment` | 部署前、中、后的标准动作 |
| `release` | 版本发布（含 tag、Changelog、回滚） |

---

## 核心概念

| 概念 | 职责 | 示例 |
|---|---|---|
| **Skill** | 最小执行单元，单一职责 | coding, review, debug |
| **Workflow** | 编排多个 Skill | new-feature, bug-fix |
| **Template** | 输出格式 | PRD, API Doc, Changelog |
| **Knowledge** | 领域规范与最佳实践 | 编码规范, 安全清单 |
| **Protocol** | 系统级规范 | 按需加载, 匹配规则, 输出标准 |

---

## Runtime 如何匹配和调用

```text
User → Runtime（Claude Code / Codex / ...）
         ↓
       读取约 1.2 KiB 的入口文件
         ↓
       根据 Runtime 已提供的 name + description 直接匹配
         ↓（仅在无法唯一确定时）
       读取当前 Profile 的轻量 ROUTER.md
         ↓
       单阶段选择最具体的一个主 Skill
       多阶段任务选择对应 Workflow
         ↓
       只加载选中的 SKILL.md / WORKFLOW.md
         ↓（明确需要时）
       按需加载 knowledge / template
```

匹配的关键不是用户是否说了“设计”“分析”“写一下”，而是用户最终要得到代码库地图、影响矩阵、架构、代码、测试方案、审查报告、交付验证还是 Skill 定义。

详细规则见 `docs/choosing-a-skill.md`；结构化路由源见 `data/skill-routing.json`。`MANIFEST.md` 不在日常请求关键路径中。

---

## 添加或修改 Skill

新增或调整能力时使用 `skill-authoring`，并遵循 `~/.agents/` 单文件规范：

```text
skills/<name>/
└── SKILL.md
```

`SKILL.md` 必须包含：

```markdown
---
name: <name>
description: <动作 + 交付物 + 关键职责边界>
---

# <Name>

[正文：何时使用 / 不要用于什么 / 执行步骤 / 输出 / 行为准则]
```

**规范要点：**

- frontmatter 仅包含 `name` 和 `description`
- `description` 不只写抽象动作，要写清交付物和最容易混淆的边界
- 单一 `SKILL.md`，不要添加 README.md 或 `examples/` 目录
- 不要添加 `# End` 标题
- 内容用可执行的叙述步骤，不强制固定章节数量
- 中文为主，保留必要的英文术语
- 新 Skill 若与现有能力职责相邻，应登记到 `data/skill-routing.json`
- 岗位标签维护在 `data/skill-roles.json`，不要把岗位标签当作精细路由规则

修改完成后先重新生成 Manifest/Router，再运行上下文预算、lint 和匹配回归测试：

```powershell
python .\scripts\build-manifest.py
python .\scripts\context-budget-report.py --check
.\scripts\lint-skill.ps1 .
.\scripts\test-skill-routing.ps1
```

macOS / Linux：

```bash
python3 scripts/build-manifest.py
python3 scripts/context-budget-report.py --check
bash scripts/lint-skill.sh .
bash scripts/test-skill-routing.sh
```

`MANIFEST.md`、`ROUTER.md` 和 `routers/*.md` 都是生成物，不要手工维护。确认检查通过后，再按需运行部署脚本。

---

## 添加新 Workflow

Workflow 不需要 frontmatter。Runtime 通过轻量 `ROUTER.md` 或入口文件发现它：

```text
workflows/<name>/
└── WORKFLOW.md
```

`WORKFLOW.md` 用叙述形式说明触发场景、Skill 编排顺序、每步输入输出、错误处理和回滚方式。一个任务横跨需求、设计、实现、测试等多个阶段时，优先新增或复用 Workflow，而不是让多个主 Skill 同时竞争。

---

## 设计原则

- **Runtime Agnostic** — 不绑定任何特定 AI 产品
- **On-Demand Loading** — 只加载当前任务需要的内容
- **Deliverable-First Matching** — 按最终交付物选择 Skill，而不是只看关键词
- **Specific Over Generic** — 专用 Skill 优先于通用 Skill
- **Single Responsibility** — 一个 Skill 只负责一个主要阶段
- **Workflow for Multi-Stage Work** — 多阶段任务通过 Workflow 编排
- **Protocol First** — 协议高于实现
- **Stable Core** — Protocol、目录和命名保持稳定
- **Skill Ecosystem Compatibility** — 与 `~/.agents/skills/` 中的第三方 Skill 共存
- **Real Engineering, Not Vibe Coding** — 纪律、验证和可维护性优先
- **Anti-Slop** — 禁止营销腔、空话和凑数内容

## 进阶文档

- `docs/choosing-a-skill.md` — Skill 匹配决策指南
- `data/skill-routing.json` — 高混淆 Skill 的结构化路由数据
- `data/skill-profiles.json` — core / ai / design / full 活动能力配置
- `data/context-budgets.json` — 上下文硬限制和告警阈值
- `data/skill-roles.json` — Skill 岗位标签
- `tests/skill-routing/` — 71 条 Skill / Workflow 匹配回归用例
- `docs/CONTEXT.md` — 项目级上下文模板
- `docs/adr/` — 架构决策记录
- `docs/feedback-system.md` — 反馈与健康度报告
- `protocols/hard-rules.md` — 不可违反的硬规则
- `protocols/skill.md` — Skill 协议完整规范
- `scripts/build-manifest.py` — 自动生成 MANIFEST
- `scripts/lint-skill.ps1` / `scripts/lint-skill.sh` — 合规检查
- `scripts/test-skill-routing.py` — 路由语料校验和 Runtime 预测评分
- `scripts/aos-feedback.py` — 记录 Skill 使用反馈
- `scripts/skill-health-report.py` — 生成健康度报告

## 反馈与自我演化（可选）

AOS 是闭环系统：除了输入、处理和输出，还有反馈与学习环节。

```bash
# 记录一次 Skill 使用反馈
python3 scripts/aos-feedback.py coding --rating useful --note "清晰"

# 标记 Runtime 第一次就调对了
python3 scripts/aos-feedback.py coding --first-match

# 查看单个 Skill 的反馈
python3 scripts/aos-feedback.py coding --show

# 生成健康度报告
python3 scripts/skill-health-report.py
# → 输出 ~/.agents/health-report.md
```

数据保存在 `~/.agents/feedback/`，报告输出到 `~/.agents/health-report.md`。详细设计见 `docs/feedback-system.md`。

---

## License

MIT
