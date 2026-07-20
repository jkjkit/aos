# Agent Protocol

Version: v0.2.0

Status: Draft

---

# 1. Purpose

Agent Protocol 定义 Runtime 如何与 AOS 集成。

本协议规范：

- Runtime 入口文件结构
- AOS 根目录定义
- 能力加载规则
- 调用约定

---

# 2. Scope

## 适用对象

所有需要使用 AOS 的 Runtime：

- Codex
- Claude Code
- Cursor
- Gemini CLI
- Roo Code
- 其它 AI Agent Runtime

---

# 3. Agent Entry File

## 3.1 文件命名

每个 Runtime 拥有独立入口文件。

推荐命名：

```
~/.codex/AGENT.md
~/.claude/CLAUDE.md
~/.cursor/AGENT.md
~/.gemini/AGENT.md
```

命名规则：

使用 Runtime 自身配置目录。

文件名：大写。

格式：Markdown。

---

## 3.2 文件结构

入口文件必须包含：

```markdown
# Agent Name

# AOS Root

# Loading Strategy

# Skill Discovery

# Workflow Discovery

# Knowledge Discovery

# Template Discovery

# Protocol Version
```

---

## 3.3 内容要求

### AOS Root

必须明确指定 AOS 根目录。

示例：

```markdown
# AOS Root

~/.agents/
```

---

### Loading Strategy

定义能力加载策略。

推荐：

```markdown
# Loading Strategy

按需加载（On-Demand）

流程：
1. 理解用户需求，并确定当前要求的最终交付物
2. 从 MANIFEST 的快速匹配规则识别候选能力
3. 比较候选 Skill 的选择条件、排除条件和 description
4. 优先选择职责最具体的 Skill，并只读取对应 Skill
5. 多阶段任务改用 Workflow
6. 执行任务并返回结果
```

禁止：

一次性加载全部能力。

---

### Skill Routing

能力匹配必须遵守：

- 先判断用户要的最终交付物，不只匹配关键词
- 专用 Skill 优先于通用 Skill
- 区分澄清、需求、设计、实现、测试、审查和调试
- 同时命中多个 Skill 时，先使用 MANIFEST 的选择条件和排除条件消歧
- 单阶段任务只加载一个主 Skill；明确的多阶段任务使用 Workflow
- 只有交付物确实无法判断时才询问用户

典型边界：

- 系统架构和技术方案 → `design`
- 界面交互和视觉规范 → `design-interface`
- API 契约 → `api-design`
- 数据模型与 Migration → `database`
- 实际源文件修改 → `coding`

禁止因为用户使用了“设计”“分析”“写一下”等宽泛词语，就直接匹配同名或通用 Skill。

### Skill Discovery

定义如何发现 Skill。

示例：

```markdown
# Skill Discovery

位置：~/.agents/skills/

结构：
skills/
├── skill-name/
│   ├── SKILL.md
│   ├── README.md
│   └── examples/

读取规则：
- 读取 skills/ 目录
- 查找 SKILL.md
- 按需加载内容
```

---

### Workflow Discovery

定义如何发现 Workflow。

示例：

```markdown
# Workflow Discovery

位置：~/.agents/workflows/

结构：
workflows/
├── workflow-name/
│   ├── WORKFLOW.md
│   └── examples/

读取规则：
- 读取 workflows/ 目录
- 查找 WORKFLOW.md
- 识别触发条件
- 按序执行 Skill
```

---

### Knowledge Discovery

定义如何使用 Knowledge。

示例：

```markdown
# Knowledge Discovery

位置：~/.agents/knowledge/

读取时机：
- Skill 执行前
- 需要特定规范时
- 需要领域知识时

使用原则：
- Knowledge 不参与推理
- Knowledge 只提供参考
- Knowledge 不触发执行
```

---

### Template Discovery

定义如何使用 Template。

示例：

```markdown
# Template Discovery

位置：~/.agents/templates/

使用时机：
- 输出结构化内容
- 生成文档
- 格式化报告

使用原则：
- Template 定义结构
- Skill 生成内容
- 内容填充 Template
```

---

### Protocol Version

必须声明遵循的协议版本。

示例：

```markdown
# Protocol Version

AOS Protocol: v0.2.0
```

---

# 4. Runtime Responsibilities

Runtime 负责：

## 4.1 理解需求

解析用户输入。

识别意图。

确定目标。

---

## 4.2 能力选择

根据需求选择：

- 单个 Skill
- 多个 Skill
- 完整 Workflow

---

## 4.3 执行管理

控制执行流程。

处理异常情况。

管理上下文。

---

## 4.4 结果返回

整合执行结果。

格式化输出。

返回用户。

---

# 5. AOS Responsibilities

AOS 负责：

## 5.1 提供标准

定义：

- Skill 协议
- Workflow 协议
- Template 协议
- Knowledge 协议
- Output 协议

---

## 5.2 组织能力

维护：

- Skills
- Workflows
- Templates
- Knowledge

---

## 5.3 保持稳定

确保：

- 协议稳定
- 接口稳定
- 目录稳定
- 命名稳定

---

# 6. 集成要求

## 6.1 必须支持

Runtime 必须能够：

- 读取文件系统
- 解析 Markdown
- 理解 YAML Frontmatter（如果使用）
- 按需加载内容

---

## 6.2 推荐支持

Runtime 推荐能够：

- 缓存已读取内容
- 并行加载多个 Skill
- 支持 Skill 组合
- 记录执行历史

---

## 6.3 禁止行为

Runtime 禁止：

- 修改 AOS 目录结构
- 自动修改 Skill 内容
- 绕过协议直接执行
- 混淆 Skill 边界

---

# 7. Context Management

## 7.1 原则

Context 由 Runtime 自行管理。

AOS 只定义最小化原则：

- 避免重复加载
- 避免冗余解析
- 避免无效传递

---

## 7.2 推荐策略

```
首次加载：完整读取
后续引用：使用缓存
跨 Skill：最小传递
```

---

# 8. Error Handling

## 8.1 Skill 不存在

行为：

提示用户 Skill 未找到。

建议相似 Skill。

---

## 8.2 Protocol 版本不匹配

行为：

警告版本差异。

尝试兼容执行。

记录版本信息。

---

## 8.3 文件读取失败

行为：

记录错误。

提示用户检查路径。

回退到默认行为。

---

# 9. Security

## 9.1 路径限制

Runtime 只应读取：

```
~/.agents/
~/.runtime-name/
```

禁止读取：

系统敏感目录。

---

## 9.2 执行限制

Skill 不应包含：

- 可执行代码
- Shell 命令
- 系统调用

Skill 只包含：

Prompt 和指导。

---

# 10. Versioning

## 10.1 协议版本

格式：

```
Major.Minor.Patch
```

Major：

不兼容变更。

Minor：

新增功能。

Patch：

修复优化。

---

## 10.2 兼容性

Runtime 应该：

向后兼容至少一个 Major 版本。

---

# 11. Examples

## 11.1 Codex Integration

```markdown
# Codex Agent

# AOS Root
~/.agents/

# Loading Strategy
按需加载

# Skill Discovery
读取 ~/.agents/skills/

# Protocol Version
v0.2.0
```

---

## 11.2 Claude Integration

```markdown
# Claude Code Agent

# AOS Root
~/.agents/

# Loading Strategy
智能按需加载

# Protocol Version
v0.2.0
```

---

# 12. Validation

Runtime 集成后应验证：

- [ ] 能够读取 AOS 目录
- [ ] 能够发现 Skills
- [ ] 能够发现 Workflows
- [ ] 能够按需加载
- [ ] 能够正确执行
- [ ] 能够处理错误

---

# 13. Migration

从 Prompt 迁移到 AOS：

```
旧方式：
大型 System Prompt

↓

新方式：
AGENT.md + AOS Skills
```

优势：

- 模块化
- 可维护
- 可复用
- 可扩展
