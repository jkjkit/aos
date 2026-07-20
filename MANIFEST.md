# AOS Manifest

完整能力目录，用于发现和维护；Runtime 日常匹配请使用轻量 `ROUTER.md`。

> 自动生成于 2026-07-20。修改源数据后重新运行 `python3 scripts/build-manifest.py`。

## Skill 岗位索引

岗位只用于浏览和发现；Runtime 路由应优先使用轻量 `ROUTER.md`。

| Role | Skills |
|---|---|
| 🌐 通用 | `grill`, `summary`, `task` |
| 🔧 开发 | `accessibility-audit`, `api-design`, `api-integration`, `change-impact-analysis`, `changelog`, `codebase-exploration`, `coding`, `context-engineering`, `database`, `debug`, `design`, `design-interface`, `document`, `git`, `llm-evaluation`, `performance`, `privacy-review`, `prompt-writing`, `refactor`, `requirement`, `research`, `review`, `risk-analysis`, `security`, `skill-authoring`, `testing`, `verification` |
| ⚙️ 运维 | `change-impact-analysis`, `changelog`, `database`, `dependency-audit`, `dependency-management`, `devops`, `git`, `incident-response`, `meeting-notes`, `migration`, `observability`, `performance`, `privacy-review`, `risk-analysis`, `security`, `verification` |
| 📈 数据 | `ab-testing`, `cohort-analysis`, `data-analysis`, `llm-evaluation`, `metrics-design` |
| 🎨 设计 | `accessibility-audit`, `api-design`, `context-engineering`, `design`, `design-interface`, `document`, `requirement`, `research`, `user-research` |
| 👥 客服 | `copywriting`, `cs-response`, `customer-recovery`, `document`, `faq-generation`, `meeting-notes`, `support-triage` |
| 📊 产品 | `ab-testing`, `brainstorm`, `cohort-analysis`, `competitive-analysis`, `data-analysis`, `design`, `llm-evaluation`, `meeting-notes`, `metrics-design`, `privacy-review`, `requirement`, `research`, `risk-analysis`, `roadmap`, `user-research` |
| ✨ 创意 | `brainstorm`, `copywriting` |

> 通用 Skill 可被任何岗位使用；岗位标签不是最终路由依据。

## Skills（按字母顺序）

| Name | 适用岗位 | 路径 | 用途 |
|---|---|---|---|
| ab-testing | data, product | skills/ab-testing/SKILL.md | 为生产流量设计和解读随机对照 A/B 实验，覆盖假设、变体、样本量、显著性和护栏指标；不用于 LLM 离线质量评估或普通数据分析 |
| accessibility-audit | design, dev | skills/accessibility-audit/SKILL.md | 审计网站或应用的语义结构、键盘操作、焦点、屏幕阅读器、对比度、缩放、表单和动态内容可访问性，输出带证据与复测方法的问题清单；不负责界面视觉设计、普通代码审查或功能测试 |
| api-design | dev, design | skills/api-design/SKILL.md | 为已明确的业务需求定义 RESTful 或 GraphQL API 契约、错误码与版本策略；不负责系统总体架构或调用实现 |
| api-integration | dev | skills/api-integration/SKILL.md | 对接第三方 API：客户端封装、限流、错误处理、降级与监控 |
| brainstorm | creative, product | skills/brainstorm/SKILL.md | 发散思维，生成多种可能性。包含 standard / lateral / analogical / extreme 四种子模式。 |
| change-impact-analysis | dev, ops | skills/change-impact-analysis/SKILL.md | 在修改现有系统前分析直接与间接影响，识别调用方、依赖、契约、数据、配置、测试和发布风险并输出影响矩阵；不负责审查已完成 diff、通用风险评估、方案设计或测试实现 |
| changelog | dev, ops | skills/changelog/SKILL.md | 把 Git 变更整理为面向用户的版本变更日志；不用于通用项目文档或提交操作 |
| codebase-exploration | dev | skills/codebase-exploration/SKILL.md | 探索陌生或大型代码库，建立目录结构、入口、核心模块、关键调用链、项目约定和任务相关文件的导航报告；不负责 Agent 上下文工程、外部调研、方案设计、变更影响评估或修改代码 |
| coding | dev | skills/coding/SKILL.md | 在需求和实现方向已明确时编写或修改应用源代码、配置与测试并完成最小自检；不负责需求澄清、方案设计、最终交付验证或 AOS Skill 定义 |
| cohort-analysis | data, product | skills/cohort-analysis/SKILL.md | 同期群分析、留存矩阵、LTV/CAC 测算与解读 |
| competitive-analysis | product | skills/competitive-analysis/SKILL.md | 分析竞品定位、能力、体验和差异化策略；不用于技术选型、用户访谈或通用数据分析 |
| context-engineering | dev, design | skills/context-engineering/SKILL.md | 设计或审计 LLM 与 Agent 的上下文选择、检索、排序、压缩、记忆、工具结果和 Token 预算，输出可执行的上下文契约；不负责 Prompt 文案、代码库导航、通用系统架构或模型质量评估 |
| copywriting | creative, cs | skills/copywriting/SKILL.md | 创作面向外部受众的营销、邮件、社媒、广告或品牌文案；不用于技术文档、客服标准回复或事实摘要 |
| cs-response | cs | skills/cs-response/SKILL.md | 根据客户问题和服务政策生成准确、可执行的客服回复；不用于工单分类、客户挽回或营销文案 |
| customer-recovery | cs | skills/customer-recovery/SKILL.md | 为投诉、流失或高风险客户制定挽回方案与回访话术；不用于普通客服回复或工单分流 |
| data-analysis | data, product | skills/data-analysis/SKILL.md | 对已有数据进行描述、诊断、预测或处方分析并给出结论；不用于用户访谈、竞品研究或原文摘要 |
| database | dev, ops | skills/database/SKILL.md | 设计或变更数据模型、Migration、索引和查询方案；不负责系统总体架构或业务代码实现 |
| debug | dev | skills/debug/SKILL.md | 针对已出现的异常、失败或性能回退复现问题并定位根因；不用于常规代码审查或预防性测试设计 |
| dependency-audit | ops | skills/dependency-audit/SKILL.md | 扫描依赖漏洞、分析影响面、产出修复与缓解方案 |
| dependency-management | ops | skills/dependency-management/SKILL.md | 评估第三方依赖的引入、升级与淘汰策略，控制供应链风险 |
| design | dev, design, product | skills/design/SKILL.md | 为已明确的需求产出系统级技术方案，覆盖架构、组件边界、技术选型与关键流程；不负责界面视觉、LLM 上下文组装契约或代码实现 |
| design-interface | design, dev | skills/design-interface/SKILL.md | 为页面或组件产出交互流程与视觉规范；不负责独立可访问性审计、系统架构、API、数据库或代码实现 |
| devops | ops | skills/devops/SKILL.md | 设计 CI/CD 流水线、容器化、部署与监控告警的配置 |
| document | dev, design, cs | skills/document/SKILL.md | 基于已知事实编写或更新 README、API、架构和用户指南；不用于 AOS Skill 定义、原文摘要、会议纪要或版本变更日志 |
| faq-generation | cs | skills/faq-generation/SKILL.md | 从工单、文档或会议材料提炼可检索的问答知识库；不用于客服即时回复或通用文档 |
| git | dev, ops | skills/git/SKILL.md | 处理日常 Git 操作：分支、提交、合并、冲突解决、撤销与历史改写 |
| grill | general | skills/grill/SKILL.md | 对一个想法或方案进行多轮追问，澄清前提、暴露盲点、要求证据。不产出方案，只澄清问题。 |
| incident-response | ops | skills/incident-response/SKILL.md | 生产事故响应流程：OnCall 角色、时间线、沟通、Postmortem 无指责复盘 |
| llm-evaluation | dev, data, product | skills/llm-evaluation/SKILL.md | 为 LLM、Prompt、RAG 或 Agent 建立评估集、评分标准、评估器、指标和回归门禁，并分析结果与失败模式；不负责撰写 Prompt、在线 A/B 实验、普通软件测试或最终构建验收 |
| meeting-notes | product, ops, cs | skills/meeting-notes/SKILL.md | 把会议内容整理为决策、行动项、负责人和待澄清问题；不用于通用摘要或正式项目文档 |
| metrics-design | data, product | skills/metrics-design/SKILL.md | 设计指标体系：北极星指标、AARRR 漏斗、HEART 模型、看板分层 |
| migration | ops | skills/migration/SKILL.md | 设计框架升级、数据库迁移、API 版本切换的整体迁移方案 |
| observability | ops | skills/observability/SKILL.md | 设计日志、指标、链路追踪的结构化方案，让系统可被观察、可被调试 |
| performance | dev, ops | skills/performance/SKILL.md | 通过测量和证据定位性能瓶颈并验证优化效果；不用于普通功能故障、安全问题或无基线调优 |
| privacy-review | dev, ops, product | skills/privacy-review/SKILL.md | 审查产品或系统中的个人信息分类、数据流、处理目的、最小化、同意、保留、删除、共享、日志和模型使用，输出隐私发现与整改清单；不负责安全漏洞测试、广义项目风险或提供法律结论 |
| prompt-writing | dev | skills/prompt-writing/SKILL.md | 把意图转化为精确可控的 LLM Prompt 正文，包括系统提示、few-shot、Agent、评估和图像 Prompt；不负责运行时上下文工程、完整 LLM 评估体系、AOS Skill 或业务代码 |
| refactor | dev | skills/refactor/SKILL.md | 在不改变外部行为的前提下重构代码结构，提升可读性与可维护性 |
| requirement | product, design, dev | skills/requirement/SKILL.md | 把尚未明确的产品想法整理为范围、用户故事和验收标准；不负责技术方案、任务拆分或代码实现 |
| research | product, design, dev | skills/research/SKILL.md | 针对外部技术选型或未知问题收集证据、比较方案并给出结论；不负责理解现有代码库、完整系统设计或代码实现 |
| review | dev | skills/review/SKILL.md | 审查已存在的代码或 diff 是否符合规范与需求并报告问题；不负责专项可访问性、隐私或安全审计，也不负责实现、测试设计、故障定位或最终验证 |
| risk-analysis | product, dev, ops | skills/risk-analysis/SKILL.md | 系统性识别项目的技术、业务、合规、运营、财务和时间风险，评估概率与影响并输出缓解与应急预案；不替代专项隐私、安全或性能审查 |
| roadmap | product | skills/roadmap/SKILL.md | 制定中长期产品或技术方向、阶段和里程碑；不负责单个功能的需求规格或近期任务拆分 |
| security | dev, ops | skills/security/SKILL.md | 审查系统、设计或代码中的安全漏洞、攻击面和保护控制并给出修复建议；不负责个人信息处理必要性与生命周期、通用代码质量或依赖版本维护 |
| skill-authoring | dev | skills/skill-authoring/SKILL.md | 创建或修改 AOS Skill，定义单一职责、description、正负触发边界和执行步骤，并同步岗位标签、路由数据、回归用例、文档与 Manifest 验证；不用于普通技术文档、通用 Prompt 或业务代码实现 |
| summary | general | skills/summary/SKILL.md | 压缩已有文档、代码或对话并保留关键信息；不新增方案、评价或研究结论 |
| support-triage | cs | skills/support-triage/SKILL.md | 对进入的客服工单进行分类、优先级、SLA 和升级判断；不负责撰写回复、客户挽回或 FAQ |
| task | general | skills/task/SKILL.md | 把已确定的目标或方案拆成可追踪、可估算、可分配的执行任务；不负责定义需求或设计方案 |
| testing | dev | skills/testing/SKILL.md | 为确定性软件功能设计测试策略、用例与覆盖方案；不用于 LLM 质量评估、专项可访问性审计、最终交付门禁、代码审查、故障定位或安全审计 |
| user-research | product, design | skills/user-research/SKILL.md | 通过访谈、问卷或可用性测试研究目标用户、行为与需求；不用于竞品比较或产品数据统计 |
| verification | dev, ops | skills/verification/SKILL.md | 在实现完成后运行已有构建、类型检查、lint、测试和验收门禁，以可复现证据判断完成条件；不负责新建 LLM 评估体系、设计测试、审查代码、定位根因或修改实现 |

## Workflows

| Name | 路径 | 触发场景 |
|---|---|---|
| bug-fix | workflows/bug-fix/WORKFLOW.md | 编排多个 Skill |
| code-review | workflows/code-review/WORKFLOW.md | 编排多个 Skill |
| deployment | workflows/deployment/WORKFLOW.md | 编排多个 Skill |
| new-feature | workflows/new-feature/WORKFLOW.md | 编排多个 Skill |
| release | workflows/release/WORKFLOW.md | 编排多个 Skill |

## Knowledge

| Name | 路径 | 领域 |
|---|---|---|
| coding-style | knowledge/coding-style/KNOWLEDGE.md | 被动参考 |
| database-design | knowledge/database-design/KNOWLEDGE.md | 被动参考 |
| git-workflow | knowledge/git-workflow/KNOWLEDGE.md | 被动参考 |
| rest-api-design | knowledge/rest-api-design/KNOWLEDGE.md | 被动参考 |
| security-checklist | knowledge/security-checklist/KNOWLEDGE.md | 被动参考 |
| testing-best-practices | knowledge/testing-best-practices/KNOWLEDGE.md | 被动参考 |

## Templates

| Name | 路径 | 输出类型 |
|---|---|---|
| api-doc | templates/api-doc/TEMPLATE.md | 文档模板 |
| architecture | templates/architecture/TEMPLATE.md | 文档模板 |
| changelog | templates/changelog/TEMPLATE.md | 文档模板 |
| contributing | templates/contributing/TEMPLATE.md | 文档模板 |
| prd | templates/prd/TEMPLATE.md | 文档模板 |
| readme | templates/readme/TEMPLATE.md | 文档模板 |
| test-plan | templates/test-plan/TEMPLATE.md | 文档模板 |
