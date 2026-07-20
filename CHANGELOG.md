# Changelog

AOS 所有重要变更的记录。格式遵循 [Keep a Changelog](https://keepachangelog.com/)。

## [Unreleased]

### Added
- 新增 4 个 P0 Skill：`codebase-exploration`、`change-impact-analysis`、`verification`、`skill-authoring`
- 新增 4 个 P1 Skill：`llm-evaluation`、`context-engineering`、`accessibility-audit`、`privacy-review`
- 新增 `data/skill-routing.json`，集中维护高混淆 Skill 的选择条件、排除条件和典型意图
- 新增轻量 `ROUTER.md` 与 `routers/core.md`、`ai.md`、`design.md`、`full.md`，按 Profile 提供最小路由上下文
- 新增 `tests/skill-routing/cases.json`，现覆盖 66 条 Skill 和 5 条 Workflow 自然语言匹配用例
- 新增 `scripts/test-skill-routing.py` 及跨平台包装脚本，用于路由契约校验、覆盖检查和 Runtime 预测评分
- 新增 `data/skill-profiles.json` 与 `scripts/skill_profiles.py`，支持 `core`、`ai`、`design`、`full` 四类活动 Skill Profile
- 新增 `data/context-budgets.json` 与上下文预算报告脚本，对 Runtime 入口、默认 Router、活动 Skill 数、description 和单 Skill 大小设置质量门禁

### Changed
- 为新 P0 Skill 增加岗位标签、显式路由边界和 8 条匹配回归用例，并同步相邻 Skill 的排除条件
- 为 P1 AI 评估、上下文工程、可访问性和隐私能力补齐岗位标签、路由边界及 10 条回归用例，并收紧相邻 Skill 边界
- 重写 `requirement`、`design`、`design-interface`、`coding` 等高混淆 Skill 的描述和职责边界
- Runtime 入口改为渐进加载：优先使用 Runtime 已提供的 Skill Catalog，仅在歧义时读取 `ROUTER.md`，确定后只读取选中的 `SKILL.md`
- `MANIFEST.md` 退出日常请求关键路径，仅作为完整能力目录和维护索引
- 部署脚本支持 Profile 选择和第三方 Skill 的 `isolate` / `keep` / `restore` 策略，并写入 AOS 托管状态清单
- Manifest 的岗位分组压缩为名称索引，完整描述只保留一份，减少重复内容和匹配噪声
- 更新 Skill 协议、选择指南和 README，明确岗位标签只用于缩小候选范围，多阶段任务应使用 Workflow
- 将匹配回归测试加入 Skill 维护流程，真实误匹配修复后必须补充可复现用例

### Fixed
- 修复 `design`、`design-interface`、`api-design`、`database` 与 `coding` 容易按关键词误匹配的问题
- 修复 Windows PowerShell 5 读取 lint 脚本时的 UTF-8 / Unicode 状态字符解析问题
- 补充 `performance` 和 `security` 的岗位标签，避免在 Manifest 中被归为未分类 Skill

### Planned
- CONTRIBUTING.md（贡献指南）
- GitHub Actions CI（自动 lint + manifest 检查）
- 卸载脚本 `scripts/uninstall.sh`
- todo-app 示例补齐 05-11 阶段
- CLI 工具（`aos search` / `aos info` 等）

---

## [0.9.0] - 2026-07-20

### Changed
- **架构重构**：AOS 从「文档项目」转型为「可部署的 Runtime 能力系统」
- **部署目标**：核心内容部署到 `~/.agents/`，供 Claude Code / Codex / Cursor 等 Runtime 自动发现
- **Skill 规范**：所有 Skill 改为符合 `~/.agents/` 真实规范的单文件 SKILL.md
  - frontmatter 仅含 `name` + `description`
  - 删除 README.md / examples/ 目录 / `# End` 标记
- **Protocols 重写**：清理冗余，按 AOS 内部协议分层（Skill / Workflow / Template / Knowledge / Output / Context / Agent）
- **MANIFEST 自动生成**：新增 `scripts/build-manifest.sh` / `build-manifest.ps1`
- **协议 lint**：新增 `scripts/lint-skill.sh` / `lint-skill.ps1`
- **跨平台部署脚本**：新增 `deploy.sh`（macOS/Linux/Git Bash）+ `deploy.ps1`（Windows PowerShell）
- **Runtime 入口文件**：新增 `runtimes/claude.md` / `codex.md` / `cursor.md`

### Added
- **6 个第一批 Skill**（PRD 定义的核心能力）：
  - `requirement` — 需求分析
  - `design` — 架构设计
  - `coding` — 代码实现
  - `review` — 代码审查
  - `debug` — 问题调试
  - `task` — 任务分解
  - `git` — 版本控制
  - `document` — 文档编写
  - `research` — 技术调研
  - `summary` — 文档总结
- **5 个核心 Workflow**：new-feature / bug-fix / code-review / deployment / release
- **6 个 Knowledge 模块**：coding-style / security-checklist / rest-api-design / database-design / git-workflow / testing-best-practices
- **7 个 Templates**：prd / api-doc / test-plan / readme / contributing / architecture / changelog
- **7 个 Protocols**：agent / skill / workflow / template / knowledge / output / context
- **6 个 Docs**：Philosophy / PRD / Architecture / RoadMap / Development / FAQ

### Removed
- 大量元文件清理：DONE.txt / DONE-v0.3.0.txt / COMPLETION*.txt / FINAL-SUMMARY*.txt / MILESTONE-*.md / PROGRESS-*.md / RELEASE-*.md / Phase.txt / STATS.md / STATUS.md / SUMMARY.md / INDEX.md / STRUCTURE.md / PROJECT-OVERVIEW.md / QUICKSTART.md
- 全部 Skill 的 README.md 与 examples/ 目录
- 全部文档中的 `# End` 标记

### Fixed
- 目录命名规范：`Protocols/` → `protocols/`（与架构文档一致）
- Template 文件名规范：`template.md` → `TEMPLATE.md`（与其它模板对齐）

---

## [0.5.0] - 2026-07-19

### Added
- 协议系统（7 个 Protocol）
- Workflow 系统初版（5 个核心 Workflow）
- 模板系统（7 个 Template）
- 知识库（6 个 Knowledge）

### Changed
- 完成 Phase 0-5 全部里程碑
- 项目从「设计阶段」进入「可用阶段」

---

## [0.3.0] - 2026-07-19

### Added
- 核心 Skill 系统（10 个 Skill）
- todo-app 示例（4/11 阶段）

### Changed
- 完成 Phase 3（Core Skills）
- 项目完成度从 25% 提升至 55%

---

## [0.2.0] - 2026-07-19

### Added
- 7 个核心 Protocol（agent / skill / workflow / template / knowledge / output / context）
- 协议驱动的模块设计

---

## [0.1.0] - 2026-07-19

### Added
- 项目骨架：README / VERSION / CHANGELOG
- 文档体系：Philosophy / PRD / Architecture / RoadMap / Development / FAQ
- 目录结构：docs/ / protocols/ / skills/ / workflows/ / templates/ / knowledge/ / examples/
- 18 条设计原则（Philosophy.md）
- MIT License

---

## 版本规则

AOS 采用 [语义化版本](https://semver.org/)：

- **Major**（X.0.0）：协议层破坏性变更
- **Minor**（0.X.0）：新增 Skill / Workflow / Knowledge / Template
- **Patch**（0.0.X）：Bug 修复、文档优化、内部改进

每个 Skill / Workflow 自身可独立迭代版本（在各自 frontmatter 中维护）。

## 发布策略

- 每次新增 Skill → Minor 版本
- 每次 Protocol 变化 → Major 版本
- 每次 bug 修复 → Patch 版本
- CHANGELOG.md 在每次发布前更新

## 历史里程碑

- **v0.1.0** — 基础框架（10%）
- **v0.2.0** — 协议系统（25%）
- **v0.3.0** — 核心 Skill（55%）
- **v0.5.0** — 全面完善（66%）
- **v0.9.0** — 架构重构 / Runtime 化 / Skill 规范对齐（92%）
- **v1.0.0** — 正式版（目标 100%）