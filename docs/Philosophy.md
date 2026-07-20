# AOS 设计哲学

Version：v0.1.0

---

# 前言

AOS（Agent Operating System）不是 Prompt 集合。

不是 Skill 集合。

不是 Workflow 集合。

更不是一个大型 Prompt。

AOS 是一套用于组织 AI Agent 工作能力的工程体系。

整个项目所有设计都必须遵循本文档。

任何实现不得违反本文档中的设计原则。

---

# 第一原则

## Documentation First

先有文档。

再有协议。

最后才有实现。

任何模块必须先完成设计，再开始开发。

禁止：

```
想到一个 Prompt

↓

直接开始写 Skill
```

正确流程：

```
需求

↓

设计

↓

协议

↓

实现

↓

测试

↓

发布
```

---

# 第二原则

## Protocol First

Protocol 高于实现。

Skill 可以修改。

Workflow 可以修改。

Template 可以修改。

Knowledge 可以修改。

Protocol 尽量保持长期稳定。

所有模块必须遵守统一协议。

禁止每个 Skill 自己定义规则。

---

# 第三原则

## Runtime Agnostic

AOS 不属于任何 Runtime。

例如：

- Codex
- Claude Code
- Cursor
- Gemini CLI
- Roo Code

这些都是 Runtime。

Runtime 可以变化。

AOS 保持稳定。

AOS 不依赖 Runtime。

Runtime 负责推理。

AOS 提供能力。

---

# 第四原则

## Single Responsibility

每个模块只负责一件事情。

例如：

Summary

负责：

阅读

总结

提炼

禁止：

设计

编码

Review

Git

一个 Skill 做好一件事情，比一个 Skill 做很多事情更容易维护。

---

# 第五原则

## Composition Over Coupling

优先组合。

不要耦合。

例如：

Requirement

↓

Design

↓

Coding

↓

Review

↓

Git

Workflow 只是组合。

Skill 之间不能互相依赖。

任何 Skill 都应该可以单独运行。

---

# 第六原则

## Convention Over Configuration

尽量减少配置。

统一目录。

统一协议。

统一输出。

统一命名。

避免复杂配置文件。

避免维护多个版本。

默认约定优于大量配置。

---

# 第七原则

## Keep It Simple

任何设计必须保持简单。

如果一个功能：

需要很多配置。

需要很多解释。

需要很多规则。

说明设计可能存在问题。

简单。

比复杂更重要。

---

# 第八原则

## Small Skill

Skill 越小越好。

Skill 越独立越好。

不要写：

万能 Skill。

不要写：

超级 Prompt。

不要写：

一个 Skill 做全部工作。

Skill 应该像函数一样。

输入。

处理。

输出。

结束。

---

# 第九原则

## Workflow Is Orchestration

Workflow 不负责思考。

Workflow 不负责分析。

Workflow 不负责业务。

Workflow 只负责组织。

例如：

```
Requirement

↓

Design

↓

Coding

↓

Review
```

Workflow 永远不实现业务逻辑。

---

# 第十原则

## Knowledge Is Passive

Knowledge 永远是被读取。

不是执行者。

Knowledge：

记录：

规范。

经验。

最佳实践。

术语。

历史。

禁止：

Prompt。

执行逻辑。

Workflow。

Skill。

Knowledge 永远保持纯净。

---

# 第十一原则

## Template Is Presentation

Template 只负责表达。

不负责推理。

例如：

PRD 模板。

API 模板。

Meeting 模板。

Release Note 模板。

Template 不参与分析。

---

# 第十二原则

## Runtime Does The Routing

Runtime 自己负责理解用户。

Runtime 自己负责选择 Skill。

AOS 不重新实现 Router。

AGENT 的职责只有：

告诉 Runtime：

能力在哪里。

协议是什么。

如何按需读取。

不要重复实现 Runtime 已有能力。

---

# 第十三原则

## Shared Capability

所有 Runtime 共用同一套能力。

统一目录：

```
~/.agents/
```

所有 Runtime：

共享：

Skills

Workflow

Template

Knowledge

Protocol

避免：

Codex 一套。

Claude 一套。

Cursor 一套。

统一维护。

统一升级。

统一版本。

---

# 第十四原则

## Stable Core

Core 必须稳定。

包括：

Protocol

Documentation

Directory

Naming

这些内容尽量不修改。

变化应该发生在：

Skill。

Workflow。

Knowledge。

保持整个系统长期稳定。

---

# 第十五原则

## Evolution

AOS 必须可以成长。

新增能力：

不影响已有能力。

删除能力：

不影响其它模块。

升级能力：

保持兼容。

AOS 应当像操作系统一样持续演进。

---

# 第十六原则

## Human Readable

所有内容优先保证：

容易阅读。

容易维护。

容易理解。

而不是：

最短。

最炫。

最复杂。

任何人第一次阅读项目，都应该能够快速理解整个系统。

---

# 第十七原则

## AI Friendly

所有文档同时服务：

人类。

AI Agent。

所有协议必须：

明确。

稳定。

可解析。

避免歧义。

避免隐式规则。

---

# 第十八原则

## Long-term Maintainability

项目设计优先考虑：

三个月以后。

半年以后。

一年以后。

而不是今天。

任何设计都应该能够长期维护。

---

# AOS 信条

我们相信：

Documentation 比 Prompt 更重要。

Protocol 比 Skill 更重要。

Skill 比 Workflow 更重要。

Workflow 比大型 Prompt 更重要。

工程化比技巧更重要。

长期维护比短期效率更重要。

简单比复杂更重要。

一致性比灵活性更重要。

---

# AOS 使命

建立一套可以长期维护、持续演进、跨 Runtime 复用的 Agent Operating System。

让 AI Agent 的能力组织方式，从 Prompt Engineering，进入 Software Engineering。