# AOS Frequently Asked Questions

Project：AOS（Agent Operating System）


Version：v0.1.0


Status：Draft


---


# 1. AOS 是什么？


AOS（Agent Operating System）是一套用于组织 AI Agent 工作能力的工程框架。


它通过：


- Skill

- Workflow
- Template
- Knowledge
- Protocol

帮助 AI Agent 形成可维护、可复用、可扩展的工作体系。


---


# 2. AOS 是不是一个新的 AI Agent？


不是。


AOS 不提供模型。


不替代：


- ChatGPT

- Codex
- Claude
- Gemini

AOS 运行在 Agent 之上。


关系：


```

Model

↓


Runtime


↓


AOS


↓


Skills

```

---


# 3. 为什么不直接写 Prompt？


因为 Prompt 不适合长期维护。


单个 Prompt：


适合一次性任务。


但是长期工作需要：


- 版本管理

- 模块化
- 复用
- 组合
- 测试

这些属于软件工程问题。


AOS 将 Prompt 能力工程化。


---


# 4. AOS 和 Skill 有什么区别？


Skill 是 AOS 中的一种能力模块。


AOS 是整体系统。


关系：


```

AOS

├── Skill


├── Workflow


├── Template


├── Knowledge


└── Protocol

```

Skill 只是其中一部分。


---


# 5. 为什么不用一个超级 Skill？


因为超级 Skill 会导致：


- 责任不清

- 难以维护
- 上下文过大
- 输出不稳定

AOS 使用：


小 Skill + Workflow


替代：


超级 Skill。


---


# 6. 为什么不用 Router？


AOS 不重新实现 Router。


原因：


现代 Runtime 已经具备：


- 理解能力

- 推理能力
- 工具选择能力

AOS 负责提供：


规范。


能力。


知识。


Runtime 负责选择。


---


# 7. 为什么所有 Runtime 共用 ~/.agents？


因为能力应该独立于 Runtime。


例如：


同一个 Coding Skill：


应该可以被：


Codex


Claude


Cursor


调用。


避免：


重复维护。


---


# 8. 为什么不用 ~/.aos？


AOS 不需要额外抽象层。


使用：


```

~/.agents
```

原因：


- 简单

- 兼容现有 Agent 生态
- 减少配置
- 降低维护成本

---


# 9. AGENT.md 的作用是什么？


AGENT 是 Runtime 入口。


负责告诉 Runtime：


- AOS 在哪里

- 如何读取能力
- 遵守哪些规范

例如：


```

~/.codex/AGENT.md
```

---


# 10. Skill 是否需要全部加载？


不需要。


AOS 推荐：


按需加载。


流程：


```

用户需求

↓


识别能力


↓


读取 Skill


↓


执行

```

避免：


一次加载所有内容。


---


# 11. 多个 Skill 联动是否消耗更多 Token？


会。


但是合理设计可以降低消耗。


例如：


不推荐：


```

读取全部 Skill

↓


全部分析

```

推荐：


```

识别需求

↓


读取必要 Skill


↓


执行 Workflow

```

---


# 12. Workflow 会不会增加复杂度？


不会。


Workflow 的作用：


减少重复组合。


例如：


没有 Workflow：


每次：


```

需求分析

设计


开发


Review

```

都重新组织。


有 Workflow：


一次定义。


多次复用。


---


# 13. Template 为什么独立？


因为：


内容结构


和


内容生成


是两个问题。


例如：


PRD：


结构固定。


内容变化。


所以：


Template 独立。


---


# 14. Knowledge 为什么不放 Skill？


因为知识生命周期不同。


Skill：


执行能力。


Knowledge：


长期积累。


例如：


代码规范。


数据库规范。


项目经验。


应该独立维护。


---


# 15. 如何新增 Skill？


流程：


```

发现需求

↓


设计 Skill


↓


编写 Protocol


↓


创建目录


↓


实现 SKILL.md


↓


添加 Example


↓


Review


↓


发布

```

---


# 16. 如何判断是否应该新增 Skill？


询问：


## 是否重复使用？


如果只用一次：


不需要。


---


## 是否独立能力？


如果不能独立：


可能应该属于 Workflow。


---


## 是否有明确输入输出？


如果没有：


需要重新设计。


---


# 17. Skill 和 Workflow 如何区分？


Skill：


回答：


“怎么做？”


例如：


总结文档。


---


Workflow：


回答：


“什么时候做什么？”


例如：


开发新功能。


---


# 18. AOS 是否支持企业使用？


支持。


企业可以增加：


Knowledge：


- 编码规范

- 架构规范
- 流程规范

Template：


- PRD

- 设计文档
- 发布文档

Workflow：


- 开发流程

- Review 流程

---


# 19. AOS 是否支持个人使用？


支持。


个人可以建立：


自己的：


- 编程习惯

- 工作流程
- 知识库
- 模板

---


# 20. AOS 是否绑定某个模型？


不绑定。


只依赖：


Runtime 能够读取文件并执行任务。


---


# 21. AOS 是否需要编程语言？


V0：


不需要。


核心内容：


Markdown。


未来：


可以增加：


- CLI

- Builder
- Validator

---


# 22. AOS 最大目标是什么？


不是替代 Agent。


而是：


让 Agent 的能力像软件一样：


可以：


设计。


开发。


复用。


测试。


维护。


升级。


---
