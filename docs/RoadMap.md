# AOS Development Roadmap

Project：AOS（Agent Operating System）


Version：v0.1.0


Status：Draft


---


# 1. Roadmap Overview


AOS 采用渐进式开发方式。


开发原则：


```

Framework First

↓


Protocol First


↓


Capability Second


↓


Automation Last

```

优先建立稳定基础，再扩展能力。


---


# 2. Version Planning


整体规划：


```

v0.x

基础框架


↓


v1.x


核心能力


↓


v2.x


工作流体系


↓


v3.x


智能化增强

```

---


# 3. Milestone 0


## Project Foundation


版本：


```

v0.1.0
```

目标：


建立 AOS 基础工程。


---


## Deliverables


完成：


```

README.md

VERSION


CHANGELOG.md


docs/


protocols/


目录结构

```

---


## 验收标准


满足：


- 项目结构确定

- 命名规范确定
- 设计理念确定
- 开发流程确定

---


# 4. Milestone 1


## Protocol System


版本：


```

v0.2.0
```

目标：


建立 AOS 核心协议。


---


## Deliverables


完成：


```

protocols/

├── agent.md


├── skill.md


├── workflow.md


├── template.md


├── knowledge.md


├── output.md


└── context.md

```

---


## 验收标准


所有未来模块：


必须可以按照 Protocol 创建。


---


# 5. Milestone 2


## Core Documentation


版本：


```

v0.3.0
```

目标：


完善工程规范。


---


## Deliverables


完成：


```

DEVELOPMENT.md

FAQ.md


Examples

```

---


## 验收标准


新开发者能够：


- 理解 AOS

- 创建 Skill
- 创建 Workflow
- 遵循规范

---


# 6. Milestone 3


## Core Skills


版本：


```

v1.0.0
```

目标：


建立第一批核心能力。


---


## 第一批 Skill


```

summary

requirement


design


coding


review


debug


task


git


document


research

```

---


## 能力覆盖


目标：


覆盖日常研发主要场景。


包括：


需求。


设计。


开发。


测试。


维护。


文档。


研究。


---


# 7. Milestone 4


## Workflow System


版本：


```

v1.5.0
```

目标：


将 Skill 组合为完整工作流程。


---


## 第一批 Workflow


### New Feature


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


### Bug Fix


```

Debug

↓


Coding


↓


Review


↓


Git


↓


Release

```

---


### Research


```

Research

↓


Summary


↓


Document

```

---


### New Project


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


# 8. Milestone 5


## Knowledge System


版本：


```

v2.0.0
```

目标：


建立长期知识沉淀体系。


---


## Knowledge 类型


```

coding-style

architecture-style


database-rule


git-rule


security-rule


company-rule


domain-knowledge

```

---


## 验收标准


Knowledge：


- 可维护

- 可更新
- 可复用

---


# 9. Milestone 6


## Template System


版本：


```

v2.2.0
```

目标：


统一输出质量。


---


## Template


包括：


```

PRD

Design


API


Task


Meeting


Release Note


README


Architecture

```

---


# 10. Milestone 7


## AOS Builder


版本：


```

v3.0.0
```

目标：


让 AOS 可以自我扩展。


---


## Builder 能力


包括：


### Skill Builder


自动生成 Skill。


---


### Workflow Builder


自动生成 Workflow。


---


### Template Builder


自动生成 Template。


---


### Knowledge Builder


自动整理知识。


---


# 11. Milestone 8


## Intelligence Layer


版本：


```

v4.0.0
```

目标：


增强 Agent 自主能力。


---


计划：


- 自动识别工作模式

- 自动推荐 Workflow
- 自动优化 Skill
- 自动发现重复能力
- 自动整理项目知识

---


# 12. 长期目标


最终目标：


建立：


```

Agent Operating System
```

具备：


- 能力管理

- 工作流管理
- 知识管理
- 输出管理
- 生命周期管理

成为 AI Agent 的工程基础设施。


---


# 13. 优先级原则


开发优先级：


```

稳定性

>


可维护性


>


扩展性


>


自动化


>


智能化

```

---


# 14. 不做事项


当前阶段不开发：


- GUI

- 云端服务
- Agent Marketplace
- 多 Agent 调度
- 自动执行危险操作
- 商业化平台

---


# 15. 发布策略


版本规则：


```

Major.Minor.Patch
```

例如：


```

v1.0.0
```

含义：


Major：


架构变化。


Minor：


新增能力。


Patch：


修复优化。


---


# 16. Release Criteria


每个版本发布前：


必须满足：


```

Documentation

↓


Protocol


↓


Implementation


↓


Example


↓


Validation

```

---


# 17. Current Status


当前版本：


```

v0.1.0
```

当前阶段：


```

Foundation Design
```

下一阶段：


```

Protocol Implementation
```

---
