# Choosing a Skill

> 不知道该调用哪个 Skill 时，先看用户当前要得到什么交付物，再看任务属于哪个领域。
>
> Runtime 日常使用当前 Profile 的轻量 `ROUTER.md`；完整能力目录见 `MANIFEST.md`；结构化路由数据见 `data/skill-routing.json`。

---

## 1. 核心原则：按最终交付物匹配

不要只根据用户说出的关键词选 Skill。相同主题可以对应完全不同的动作和交付物。

例如用户都在说“登录”：

| 用户当前要得到的结果 | 应选 Skill |
|---|---|
| 澄清登录需求中的假设和盲点 | `grill` |
| 用户故事、业务规则和验收标准 | `requirement` |
| 现有仓库的入口、模块和调用链地图 | `codebase-exploration` |
| 拟议修改的调用方、契约和发布影响 | `change-impact-analysis` |
| 服务边界、组件关系和数据流 | `design` |
| 登录页交互、布局和视觉规范 | `design-interface` |
| 请求、响应、鉴权和错误码契约 | `api-design` |
| 表结构、Migration 和索引方案 | `database` |
| 在现有项目中新增或修改源代码 | `coding` |
| 实现后运行质量门禁并判断能否交付 | `verification` |
| 创建或调整 AOS Skill 与路由规则 | `skill-authoring` |
| 把已确定方案拆成执行任务 | `task` |

匹配时遵守以下顺序：

1. 判断用户要求的**最终交付物**。
2. Runtime 已提供 Skill Catalog 时，先根据 `name + description` 直接匹配。
3. 只有无法唯一确定时，才读取当前 Profile 的 `ROUTER.md` 缩小候选范围。
4. 优先选择职责更具体的 Skill，不要让通用 Skill 抢走专用任务。
5. 确定后只读取选中的 `SKILL.md`；只有交付物确实不明确时才询问用户。

---

## 2. 高频混淆边界

### 需求、设计与实现

| Skill | 选择它时 | 不要选择它时 |
|---|---|---|
| `requirement` | 需要范围、用户故事、业务规则或验收标准 | 需求已经明确，当前要方案或代码 |
| `codebase-exploration` | 需要理解现有代码库的结构、入口、模块、调用链和相关文件 | 需要外部调研、拟议变更的影响分析、方案或代码 |
| `change-impact-analysis` | 修改前需要识别调用方、契约、数据、测试和交付影响 | 只需理解代码库、审查已完成改动或设计方案 |
| `design` | 需要系统架构、组件边界、技术选型或关键技术流程 | 需要界面视觉、API 细节、数据库细节或实际代码 |
| `design-interface` | 需要页面或组件的交互流程、布局和视觉规范 | 需要系统架构或实际前端代码 |
| `api-design` | 需要端点、字段、错误码、鉴权和版本契约 | 需要系统总体架构或第三方 API 调用实现 |
| `database` | 需要 Schema、Migration、索引或查询方案 | 需要系统总体架构或业务代码 |
| `coding` | 需要新增或修改应用源代码、配置或测试文件，并执行必要自检 | 当前只需要探索、影响分析、方案、审查、交付验证或 Skill 定义 |
| `task` | 目标和方案已确定，需要拆成近期执行任务 | 需求或技术方向尚未确定 |
| `roadmap` | 需要中长期阶段、里程碑、依赖和取舍 | 需要单个功能需求或近期任务清单 |

### AI 系统设计与评估

| Skill | 选择它时 | 不要选择它时 |
|---|---|---|
| `prompt-writing` | 需要编写或优化 system prompt、few-shot、Agent、评估或图像 Prompt 正文 | 需要运行时上下文契约或完整质量评估体系 |
| `context-engineering` | 需要设计上下文来源、选择、排序、压缩、记忆、工具结果、信任边界和 Token 预算 | 只需 Prompt 文案、代码库导航、通用架构或模型质量评估 |
| `llm-evaluation` | 需要评估集、Rubric、评估器、指标、基线比较、失败分析和回归门禁 | 只需 Prompt、上下文工程、在线 A/B 实验或普通软件测试 |

### 研究、分析与摘要

| Skill | 选择它时 | 不要选择它时 |
|---|---|---|
| `research` | 需要查证外部未知问题、比较技术方案并形成结论 | 需要理解现有代码库、竞品矩阵、用户访谈或压缩已有材料 |
| `competitive-analysis` | 需要比较竞品定位、能力、体验和差异化 | 需要技术选型或业务数据分析 |
| `user-research` | 需要访谈、问卷、可用性测试或用户洞察 | 只有竞品资料或产品行为数据 |
| `data-analysis` | 需要分析已有数据并解释趋势、原因或行动 | 没有数据，或只需压缩现有文字 |
| `summary` | 只需要压缩已有文档、代码或对话 | 需要新增判断、代码库探索、调研、方案或评价 |

### 代码质量与问题处理

| Skill | 选择它时 | 不要选择它时 |
|---|---|---|
| `testing` | 需要设计测试策略、用例、边界条件或覆盖计划 | 需要执行最终交付门禁、审查 diff 或定位已发生故障 |
| `review` | 已有代码或 diff，需要检查缺陷、规范和需求符合度 | 需要专项可访问性、隐私或安全审计，或直接实现、定位根因、最终验证 |
| `accessibility-audit` | 需要审计键盘、焦点、语义、屏幕阅读器、对比度、缩放、表单和动态内容 | 需要界面设计、普通代码审查、功能测试或安全/隐私审计 |
| `debug` | 已经出现错误、异常或性能回退，需要复现和定位根因 | 没有具体故障，只做常规审查 |
| `security` | 需要检查攻击面、漏洞、权限或保护控制 | 需要判断个人信息处理目的、必要性和生命周期 |
| `privacy-review` | 需要审查个人信息分类、目的、最小化、同意、保留、删除、共享、日志和模型使用 | 需要漏洞测试、广义项目风险、普通代码审查或法律结论 |
| `performance` | 有性能目标或基线，需要测量瓶颈并验证优化 | 普通功能错误或没有证据的提前优化 |
| `verification` | 实现完成后需要实际运行构建、lint、测试和验收门禁 | 需要设计测试、审查代码、定位失败根因或修改实现 |

### 文档、内容与能力定义

| Skill | 选择它时 | 不要选择它时 |
|---|---|---|
| `document` | 需要 README、API、架构或用户指南等稳定文档 | 需要 AOS Skill 定义、摘要、会议纪要、FAQ、版本日志或营销文案 |
| `skill-authoring` | 需要创建或修改 AOS Skill、职责边界、路由规则和回归用例 | 需要普通文档、通用 Prompt、业务代码或安装已有 Skill |
| `changelog` | 需要把代码变更整理成面向用户的版本日志 | 需要通用项目文档或执行 Git 操作 |
| `meeting-notes` | 需要从会议材料提取决策、行动项和负责人 | 只是通用摘要或正式项目文档 |
| `faq-generation` | 需要从历史资料整理可检索的问答知识库 | 需要即时客服回复或通用文档 |
| `copywriting` | 需要营销、邮件、社媒、广告或品牌表达 | 需要技术文档、客服标准回复或事实摘要 |

完整且可机器读取的规则以 `data/skill-routing.json` 为准；构建脚本会按 Profile 生成 `ROUTER.md` 与 `routers/*.md`。`MANIFEST.md` 仅保留完整能力目录。

---

## 3. 岗位标签只用于缩小候选范围

`data/skill-roles.json` 将 Skill 标注为通用、开发、运维、数据、设计、客服、产品或创意等岗位。岗位标签适合做浏览和发现，但不是最终路由依据。

原因是：

- 一个岗位会使用多个不同交付物的 Skill。
- 一个 Skill 也可能服务多个岗位。
- “开发任务”可能是在做架构、实现、测试、审查或调试，仅凭岗位无法区分。

正确用法：

1. 用岗位标签缩小候选集合。
2. 再用最终交付物和排除条件确定唯一主 Skill。
3. 不要因为 Skill 与用户岗位相同就直接选择它。

---

## 4. 单阶段用 Skill，多阶段用 Workflow

一个 Skill 应只负责一个主要阶段。用户同时要求多个阶段时，不要一次加载多个互相竞争的主 Skill，应优先匹配 Workflow。

| 场景 | 推荐 Workflow / 顺序 |
|---|---|
| 新功能从需求到交付 | `new-feature` |
| Bug 复现、修复和回归 | `bug-fix` |
| 对已有改动做系统审查 | `code-review` |
| 部署前、中、后操作 | `deployment` |
| 版本发布、日志和回滚准备 | `release` |

如果没有合适 Workflow，再按阶段串联 Skill，并明确每一步的输入与输出。

---

## 5. 如何维护匹配质量

### Skill 自身

创建或修改能力时优先使用 `skill-authoring`。每个 `SKILL.md` 的 `description` 至少要表达：

1. **动作**：这个 Skill 做什么。
2. **交付物**：最终产出是什么。
3. **边界**：最容易与哪些 Skill 混淆，以及何时不要使用。

高混淆 Skill 的正文还应提供清晰的正向和负向触发条件。

### 路由数据

`data/skill-routing.json` 是高混淆能力路由的单一事实源。出现以下情况时应更新它：

- 新 Skill 与已有 Skill 的职责相邻。
- Runtime 经常在两个或多个 Skill 之间误匹配。
- 仅靠 `description` 无法稳定表达选择与排除条件。
- 需要加入可回归验证的典型用户意图。

`data/skill-roles.json` 只维护岗位标签，不应承载精细路由逻辑。

### 匹配回归语料

`tests/skill-routing/cases.json` 记录真实用户表达及预期 Skill / Workflow。每次出现真实误匹配时，应把能够复现问题的表达加入语料，避免后续修改造成同类退化。

每条用例需要包含：

- 唯一 ID
- 不直接暴露 Skill 名称的自然语言输入
- 预期 Skill 或 Workflow
- 容易混淆的候选能力
- 选择该能力的原因

测试运行器 `scripts/test-skill-routing.py` 会检查路由覆盖、Profile Router、默认 Router、Manifest 目录和引用完整性，并可对 Runtime 生成的预测结果计算准确率和混淆方向。

### 修改后的验证

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

测试真实 Runtime 时，可以生成预测模板并对结果评分：

```powershell
python .\scripts\test-skill-routing.py --write-eval .\tmp\routing-eval.json
python .\scripts\test-skill-routing.py --write-template .\tmp\routing-predictions.json
python .\scripts\test-skill-routing.py --predictions .\tmp\routing-predictions.json
```

不要直接编辑 `MANIFEST.md`、`ROUTER.md` 或 `routers/*.md`；它们由 Skill、Workflow、Profile 和路由数据自动生成。完整测试说明见 `tests/skill-routing/README.md`。