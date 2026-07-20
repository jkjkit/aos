# AOS System Architecture

Project：AOS（Agent Operating System）


Version：v0.1.0


Status：Draft


---


# 1. 架构目标


AOS 不是一个 AI Agent。


AOS 是一套组织 AI Agent 工作能力的工程框架。


AOS 的职责：


- 定义标准

- 组织能力
- 管理知识
- 规范输出

Runtime 的职责：


- 理解用户需求

- 推理
- 调用能力
- 返回结果

AOS 不替代 Runtime。


AOS 增强 Runtime。


---


# 2. 总体架构


```

                User
                  │
                  ▼
      Runtime（Codex / Claude）
                  │
                  ▼
        AGENT / CLAUDE.md
                  │
                  ▼
            ~/.agents/
                  │
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
 Skills      Workflows     Knowledge
    │             │             │
    └─────────────┼─────────────┘
                  ▼
             Templates
                  │
                  ▼
          Final Response
```

---


# 3. Runtime


Runtime 指 AI Agent。


例如：


- Codex

- Claude Code
- Cursor
- Gemini CLI
- Roo Code

Runtime 负责：


- 理解用户输入

- 判断需要哪些能力
- 按需读取能力
- 整合最终结果

Runtime 不负责维护能力。


---


# 4. AGENT


AGENT 是 Runtime 的入口。


例如：


```

~/.codex/AGENT.md
```

```

~/.claude/CLAUDE.md
```

AGENT 职责：


- 指定 AOS 根目录

- 定义加载原则
- 指导 Runtime 调用能力

AGENT 不实现业务。


AGENT 不承担复杂逻辑。


AGENT 保持轻量。


---


# 5. AOS 根目录


统一目录：


```

~/.agents/
```

结构：


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


# 6. 核心模块


## Documentation


保存设计文档。


包括：


- README

- PRD
- Architecture
- Philosophy
- Roadmap
- Development

Documentation 是整个系统的基础。


---


## Protocol


定义所有模块必须遵守的规则。


包括：


- Skill

- Workflow
- Template
- Knowledge
- Output
- Context

Protocol 长期保持稳定。


---


## Skill


Skill 是最小执行单元。


一个 Skill：


只负责一件事情。


例如：


Summary


Coding


Review


Design


Requirement


Debug


Git


Research


---


Skill 特点：


- 单一职责

- 可组合
- 可复用
- 可维护

---


## Workflow


Workflow 用于组织 Skill。


例如：


```

Requirement

↓


Design


↓


Coding


↓


Review


↓


Document

```

Workflow 不负责推理。


Workflow 不负责分析。


Workflow 只组织执行顺序。


---


## Template


Template 定义输出格式。


例如：


PRD


Meeting


Task


Release Note


API


Architecture


Template 不包含业务逻辑。


---


## Knowledge


Knowledge 用于长期沉淀知识。


例如：


- Coding Style

- Git Convention
- Architecture Guide
- Database Guide
- Company Convention

Knowledge 不参与执行。


Knowledge 不负责推理。


---


# 7. 请求生命周期


一个请求在 AOS 中的生命周期：


```

User

↓


Runtime


↓


AGENT


↓


选择 Skill


↓


执行 Skill


↓


应用 Template


↓


输出结果

```

AOS 不增加额外调度层。


Runtime 负责能力选择。


---


# 8. Skill 生命周期


Skill 从设计到发布遵循统一流程。


```

需求

↓


设计


↓


Protocol


↓


实现


↓


Example


↓


Review


↓


Release

```

所有 Skill 必须符合 Protocol。


---


# 9. Workflow 生命周期


Workflow：


```

需求

↓


设计


↓


选择 Skill


↓


定义顺序


↓


测试


↓


发布

```

Workflow 不允许实现业务逻辑。


---


# 10. Knowledge 生命周期


Knowledge：


```

经验

↓


整理


↓


规范


↓


沉淀


↓


持续更新

```

Knowledge 长期维护。


不参与 Runtime 推理。


---


# 11. Template 生命周期


Template：


```

需求

↓


设计格式


↓


验证


↓


发布

```

Template 不实现逻辑。


---


# 12. Documentation 生命周期


Documentation：


```

Proposal

↓


Review


↓


Approved


↓


Release

```

Documentation 优先于实现。


---


# 13. Context


Runtime 自己负责 Context。


AOS 只定义 Context 规范。


避免：


重复读取。


重复解释。


重复分析。


Context 保持最小化。


---


# 14. Output


所有 Skill 输出统一规范。


推荐结构：


```

Summary

Analysis


Recommendation


Next Step

```

保持输出一致。


方便 Workflow 组合。


---


# 15. 目录职责


```

docs/
```

负责文档。


---


```

protocols/
```

负责规范。


---


```

skills/
```

负责能力。


---


```

workflows/
```

负责组织能力。


---


```

templates/
```

负责输出格式。


---


```

knowledge/
```

负责长期知识。


---


```

examples/
```

负责示例。


---


```

playground/
```

负责实验能力。


未经验证能力不得进入正式目录。


---


# 16. Runtime 设计原则


Runtime：


负责：


- 理解

- 推理
- 调用

AOS：


负责：


- 定义

- 组织
- 规范

Runtime 与 AOS 解耦。


---


# 17. 扩展原则


新增 Skill：


无需修改其它 Skill。


新增 Workflow：


无需修改已有 Workflow。


新增 Template：


无需修改已有 Template。


新增 Knowledge：


无需修改已有 Knowledge。


扩展应保持零侵入。


---


# 18. 稳定层


长期稳定：


```

Documentation

↓


Protocol


↓


Directory

```

允许频繁变化：


```

Skill

Workflow


Knowledge


Template

```

稳定层变化必须谨慎。


---


# 19. Token 优化原则


默认：


Runtime 不读取全部目录。


Runtime：


根据用户需求。


按需读取：


- Skill

- Workflow
- Template
- Knowledge

避免一次性加载全部内容。


保持上下文轻量。


---


# 20. 架构原则


AOS 遵循以下原则：


- Documentation First

- Protocol First
- Runtime Agnostic
- Single Responsibility
- Composition Over Coupling
- Convention Over Configuration
- Keep It Simple

---
