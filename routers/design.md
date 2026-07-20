# AOS Router

> 自动生成于 2026-07-20；当前 Profile：`design`；活动 Skill：38。

仅在 Runtime 提供的 Skill 列表无法唯一匹配时读取本文件。不要默认读取完整 `MANIFEST.md`。

## 路由原则

1. 按用户当前要求的最终交付物匹配，不按孤立关键词匹配。
2. 优先选择职责最具体的 Skill；单阶段只加载一个 Skill。
3. 请求明确横跨多个阶段时选择 Workflow。
4. 仍有歧义时对比候选 description；确定后只读取选中的 `SKILL.md`。

## 需求、设计与实现

- `grill`：只需要追问、澄清前提和暴露盲点
- `requirement`：需要范围、用户故事、业务规则或验收标准
- `codebase-exploration`：需要理解现有代码库的结构、入口、模块、调用链和任务相关文件
- `change-impact-analysis`：修改前需要识别调用方、依赖、契约、数据、测试和发布影响
- `design`：需要系统架构、组件边界、技术选型或关键技术流程
- `design-interface`：需要页面或组件的交互流程、布局和视觉规范
- `api-design`：需要端点、字段、错误码、鉴权和版本契约
- `database`：需要 Schema、Migration、索引或查询方案
- `coding`：需要新增或修改实际源代码并执行自检
- `task`：目标和方案已确定，需要拆成执行任务

## 研究、分析与摘要

- `research`：需要查证未知问题、比较技术方案并形成结论
- `competitive-analysis`：需要比较竞品定位、能力、体验和差异化
- `user-research`：需要访谈、问卷、可用性测试或用户洞察
- `data-analysis`：需要分析已有数据并解释趋势、原因或行动
- `summary`：只需压缩已有文档、代码或对话

## 代码质量与问题处理

- `testing`：需要测试策略、用例、边界条件或覆盖计划
- `review`：已有代码或 diff，需要检查规范、缺陷和需求符合度
- `accessibility-audit`：需要审计键盘、焦点、语义、屏幕阅读器、对比度、缩放、表单和动态内容障碍
- `debug`：已经出现错误、异常或回退，需要复现并定位根因
- `security`：需要检查攻击面、漏洞、权限或数据安全
- `performance`：有性能目标或基线，需要测量瓶颈和验证优化
- `verification`：实现完成后需要实际运行质量门禁并按证据判断是否满足完成条件

## 文档、内容与能力定义

- `document`：需要 README、API、架构或用户指南等正式文档
- `skill-authoring`：需要创建或修改 AOS Skill 及其职责边界、路由规则和回归用例
- `changelog`：需要把 Git 变更整理为面向用户的版本日志
- `copywriting`：需要营销、邮件、社媒、广告或品牌表达

## Workflows

- `bug-fix`：复现、定位、修复和回归的完整故障流程
- `code-review`：自动检查、人工审查、修改确认和合并验证
- `deployment`：部署前检查、发布、健康检查、烟测和回滚准备
- `new-feature`：需求到实现与验证的完整新功能流程
- `release`：版本号、变更日志、验证、发布、部署和反馈监控
