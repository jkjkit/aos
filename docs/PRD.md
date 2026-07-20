# Product Requirement Document

Project：AOS（Agent Operating System）


Version：v0.1.0


Status：Draft


---


# 1. 项目概述


## 1.1 项目名称


AOS（Agent Operating System）


---


## 1.2 项目定位


AOS 是一套面向 AI Agent 的工程化工作框架。


AOS 不属于某一个 AI 产品。


AOS 提供统一的能力组织方式，使不同 Runtime 可以共享同一套工作能力。


Runtime 示例：


- Codex

- Claude Code
- Cursor
- Gemini CLI
- Roo Code
- Cline

---


## 1.3 产品愿景


建立一套长期维护、持续演进、跨 Runtime 复用的 Agent Operating System。


让 Agent 的能力组织方式从 Prompt Engineering 演进到 Software Engineering。


---


# 2. 背景


随着 AI Agent 深入研发流程，Prompt 数量不断增长。


目前普遍存在以下问题：


- Prompt 无法管理

- Skill 命名混乱
- 能力重复建设
- 输出格式不一致
- 工作流程无法复用
- 项目经验无法沉淀
- Token 消耗不断增加
- 不同 Runtime 无法共享能力

AOS 希望通过统一规范解决上述问题。


---


# 3. 产品目标


## V0


完成工程框架。


输出：


- 文档体系

- 协议体系
- 目录结构
- 开发规范

---


## V1


建立核心能力。


覆盖：


- 文档处理

- 软件开发
- 需求分析
- 架构设计
- 代码 Review
- Bug 修复
- Git 管理
- 技术研究

覆盖率目标：


80%


---


## V2


建立完整 Workflow。


完善：


- Template

- Knowledge
- Context
- Output

覆盖率目标：


90%


---


## V3


建立完整 AOS。


新增：


- Builder

- 自动生成能力
- 自动组合 Workflow
- 自动优化 Prompt
- 项目知识沉淀

覆盖率目标：


95%+


---


# 4. 产品边界


AOS 提供：


- Skill

- Workflow
- Template
- Knowledge
- Protocol
- Documentation

AOS 不提供：


- Runtime

- AI Model
- Shell 执行器
- IDE
- GUI

---


# 5. 用户


目标用户：


- 软件工程师

- 架构师
- 产品经理
- 技术负责人
- AI 开发者
- Agent 开发者

---


# 6. 使用场景


## 文档处理


包括：


- 阅读

- 总结
- 提炼
- 翻译
- 整理
- 分类

---


## 软件研发


包括：


- Requirement

- Design
- Coding
- Review
- Debug
- Refactor

---


## 项目管理


包括：


- Task

- Planning
- Sprint
- Release
- Roadmap
- Meeting

---


## 技术研究


包括：


- Research

- Compare
- Investigation
- Benchmark

---


## 工程维护


包括：


- Git

- Release Note
- Changelog
- Documentation

---


# 7. 核心能力


AOS 能力由多个 Skill 组成。


第一阶段计划：


| Skill       | 状态    |

| ----------- | ------- |
| Summary     | Planned |
| Requirement | Planned |
| Design      | Planned |
| Coding      | Planned |
| Review      | Planned |
| Debug       | Planned |
| Task        | Planned |
| Git         | Planned |
| Document    | Planned |
| Research    | Planned |

---


# 8. Workflow


V1 提供：


## New Feature


```

Requirement

↓


Design


↓


Coding


↓


Review


↓


Git


↓


Document

```

---


## Bug Fix


```

Debug

↓


Coding


↓


Review


↓


Git


↓


Release Note

```

---


## Research


```

Research

↓


Summary


↓


Document

```

---


## New Project


```

Research

↓


Architecture


↓


Scaffold


↓


Coding


↓


README

```

---


# 9. Template


第一阶段提供：


- PRD

- Design
- API
- Task
- Meeting
- Release Note
- README
- Architecture

---


# 10. Knowledge


Knowledge 用于沉淀：


- Coding Style

- Git Flow
- Architecture Style
- Database Convention
- Best Practice
- Glossary

Knowledge 不参与推理。


Knowledge 不参与执行。


---


# 11. Protocol


所有模块必须遵守统一协议。


包括：


- Skill Protocol

- Workflow Protocol
- Template Protocol
- Knowledge Protocol
- Context Protocol
- Output Protocol

Protocol 是整个系统最高规范。


---


# 12. 目录规范


```

~/.agents/

docs/


protocols/


skills/


workflows/


templates/


knowledge/


examples/


playground/

```

所有 Runtime 使用同一目录。


---


# 13. Runtime


Runtime 负责：


- 理解需求

- 加载能力
- 调用能力
- 输出结果

Runtime 不维护 Skill。


Runtime 不维护 Workflow。


Runtime 不维护 Knowledge。


---


# 14. AGENT


每个 Runtime 都有自己的入口文件。


例如：


```

~/.codex/AGENT.md
```

```

~/.claude/CLAUDE.md
```

AGENT 负责：


- 指定 AOS 根目录

- 定义加载规则
- 指导 Runtime 按需读取

AGENT 不负责业务实现。


---


# 15. 非目标


当前版本不考虑：


- GUI

- Web 平台
- Plugin Marketplace
- 自动执行系统命令
- 自动修改远程仓库
- 多 Agent 编排
- 云端同步

---


# 16. 成功标准


## 工程目标


新增 Skill：


无需修改已有 Skill。


新增 Workflow：


无需修改已有 Workflow。


统一协议长期稳定。


---


## 使用目标


覆盖：


95%+


软件研发工作。


---


## 维护目标


Skill 保持单一职责。


Workflow 保持轻量。


Protocol 长期稳定。


Documentation 持续完善。


---


# 17. 版本规划


## v0.x


完成框架。


---


## v1.x


完成核心 Skill。


---


## v2.x


完成 Workflow。


完善 Knowledge。


---


## v3.x


形成完整 Agent Operating System。


---


# 18. 验收标准


AOS v1.0 发布时应满足：


- 完整文档体系

- 完整协议体系
- 完整开发规范
- ≥10 个核心 Skill
- ≥4 个 Workflow
- ≥8 个 Template
- 统一目录
- 统一命名
- 统一输出规范
- 可运行于多个 Runtime

---
