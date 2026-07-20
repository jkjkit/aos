# Architecture Decision Records (ADR)

AOS 的重大架构决策都记录在这里。

## 什么是 ADR

ADR（Architecture Decision Record）是记录「我们为什么这样做」的轻量文档。每个 ADR：

- 记录一个具体的架构决策
- 解释上下文与备选方案
- 列出决策的代价与后果
- 一旦写入不可修改——错了就写新的 supersede 它

## 格式

参考 [Michael Nygard 的 ADR 模板](https://github.com/joelparkerhenderson/architecture-decision-record)。

每个 ADR 文件命名：`NNNN-<短横线连接的标题>.md`，例如 `0001-skill-single-file.md`。

## 目录

- [ADR-0001](0001-skill-single-file.md) — Skill 用单文件 SKILL.md，禁止 README.md / examples/
- [ADR-0002](0002-deploy-to-home-agents.md) — AOS 部署到 ~/.agents/，供所有 Runtime 共用
- [ADR-0003](0003-runtime-agnostic.md) — Runtime Agnostic：不绑定任何 AI Runtime

## 如何新增 ADR

1. 复制 `template.md` 到 `NNNN-<标题>.md`
2. 填写所有章节
3. 在本 README 的「目录」加一行
4. 提交 PR（含 ADR 变更需团队 review）

## 如何废弃 ADR

不要修改原文件。新建 `NNNN-<标题>.md`，引用旧 ADR 并解释 supersede 原因。