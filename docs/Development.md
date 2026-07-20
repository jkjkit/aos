# AOS Development Guide

Project：AOS（Agent Operating System）


Version：v0.1.0


Status：Draft


---


# 1. 文档说明


本文档定义 AOS 的开发规范。


所有贡献：


包括：


- Skill

- Workflow
- Template
- Knowledge
- Protocol

必须遵守本文档。


---


# 2. 开发原则


AOS 开发遵循：


```

Documentation First

↓


Protocol First


↓


Implementation


↓


Validation


↓


Release

```

禁止：


直接创建能力。


---


# 3. 项目目录规范


```

~/.agents/

├── docs/


├── protocols/


├── skills/


├── workflows/


├── templates/


├── knowledge/


├── examples/


└── playground/

```

---


# 4. 命名规范


## 4.1 文件命名


统一：


小写。


使用：


```

kebab-case
```

例如：


正确：


```

code-review.md
```

错误：


```

CodeReview.md
```

---


## 4.2 Skill 命名


使用：


动词或动作描述。


推荐：


```

summary

coding


review


debug


design

```

避免：


```

super-ai-helper

ultimate-agent

```

---


## 4.3 Workflow 命名


使用：


业务流程名称。


例如：


```

new-feature

bug-fix


project-init

```

---


# 5. Skill 开发规范


每个 Skill 必须包含：


```

skill-name/

├── SKILL.md


├── README.md


├── examples/


└── tests/

```

---


# 6. Skill 必须包含内容


SKILL.md 必须包含：


```

# Name

# Purpose


# When To Use


# Input


# Process


# Output


# Quality Check


# Limitations


# Examples

```

---


# 7. Skill 设计要求


## 单一职责


一个 Skill：


只解决一个问题。


---


## 输入明确


必须说明：


输入：


- 类型

- 格式
- 前置条件

---


## 输出明确


必须说明：


输出：


- 格式

- 结构
- 标准

---


## 可组合


Skill 不应该依赖固定 Workflow。


---


## 可独立运行


任何 Skill：


应该可以单独调用。


---


# 8. Skill 禁止事项


禁止：


## 创建万能 Skill


例如：


```

AI Assistant Skill
```

包含：


编码。


设计。


测试。


部署。


---


## 隐藏 Workflow


Skill 内禁止：


定义复杂流程。


---


## 内嵌大量知识


Skill 不应该保存：


公司规范。


项目知识。


行业知识。


这些属于 Knowledge。


---


# 9. Workflow 开发规范


Workflow 目录：


```

workflow-name/

├── WORKFLOW.md


├── examples/


└── tests/

```

---


# 10. Workflow 内容要求


必须包含：


```

# Name

# Purpose


# Trigger


# Steps


# Input


# Output


# Failure Handling


# Examples

```

---


# 11. Workflow 设计原则


Workflow 只负责：


```

Skill A

↓


Skill B


↓


Skill C

```

禁止：


包含大量 Prompt。


禁止：


实现业务逻辑。


---


# 12. Template 开发规范


目录：


```

template-name/

├── TEMPLATE.md


├── example.md

```

---


Template 负责：


输出结构。


格式。


展示。


---


Template 禁止：


包含：


- 判断逻辑

- 执行逻辑
- Skill 调用逻辑

---


# 13. Knowledge 开发规范


目录：


```

knowledge-name/

├── KNOWLEDGE.md


├── examples/

```

---


Knowledge 内容：


包括：


- 规则

- 标准
- 经验
- 术语

---


Knowledge 禁止：


包含：


- Prompt

- Workflow
- 操作流程

---


# 14. Protocol 修改规范


Protocol 是 AOS 稳定层。


修改必须：


1. 提出原因

2. 评估影响
3. 更新相关文档
4. 更新示例
5. 更新版本

---


# 15. Version 管理


采用：


```

Major.Minor.Patch
```

---


Major：


架构变化。


例如：


```

v1.x → v2.x
```

---


Minor：


新增能力。


例如：


新增 Skill。


```

v1.1 → v1.2
```

---


Patch：


修复。


例如：


```

v1.1.1
```

---


# 16. Git Commit 规范


格式：


```

type(scope): message
```

---


类型：


```

docs

feat


fix


refactor


test


chore

```

---


示例：


```

docs(protocol): add skill specification

feat(skill): add summary skill


fix(template): update PRD format

```

---


# 17. Review 标准


新增模块必须检查：


## 必要性


是否真的需要？


---


## 独立性


是否可以独立运行？


---


## 重复性


是否已有类似能力？


---


## 维护成本


未来是否容易维护？


---


## 协议符合度


是否符合 Protocol？


---


# 18. 测试规范


测试不是验证代码。


测试验证：


能力质量。


---


Skill 测试：


包括：


- 输入测试

- 输出测试
- 边界测试
- 示例测试

---


Workflow 测试：


包括：


- 顺序测试

- 输出测试
- 异常测试

---


# 19. Playground 使用规范


playground：


用于实验。


目录：


```

playground/

skills/


workflows/


templates/

```

未经验证内容：


禁止进入正式目录。


---


# 20. 发布流程


正式发布：


```

Development

↓


Review


↓


Documentation Update


↓


Version Update


↓


Changelog


↓


Release

```

---


# 21. 贡献原则


所有贡献者必须遵守：


```

Keep Simple

Keep Consistent


Keep Maintainable

```

---
