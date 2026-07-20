# AOS Hard Rules

> 不可违反的硬规则。任何 Skill / Workflow / Knowledge / Template / Runtime 入口都必须遵守。

这些规则从 mattpocock/skills 的「Real Engineering」哲学与 taste-skill 的「Anti-Slop」纪律中提炼，是 AOS 的「不可商量」约束。

---

## 1. Skill 编写

### 禁止：万能 Skill

- ❌ 一个 Skill 涵盖需求分析 + 设计 + 编码 + 测试 + 部署
- ✅ 每个 Skill 单一职责

### 禁止：内嵌 Workflow

- ❌ 在 Skill 内部写「步骤 1...2...3...」的完整流程
- ✅ 流程编排由 Workflow 负责，Skill 只描述「怎么做」一件事

### 禁止：内嵌知识

- ❌ 在 Skill 里写「编码规范」「API 最佳实践」等通用规范
- ✅ 这些属于 Knowledge，Skill 只引用 `~/.agents/knowledge/<name>/`

### 禁止：单文件违反规范

- ❌ `skills/<name>/README.md`
- ❌ `skills/<name>/examples/`
- ❌ `skills/<name>/tests/`
- ❌ SKILL.md 末尾写 `# End`
- ✅ 每个 Skill 仅含 `SKILL.md` 单文件

### 禁止：frontmatter 冗余字段

- ❌ `version` / `tags` / `author` / `created` / `updated` / `category`
- ✅ 仅保留 `name` + `description`

### 禁止：模糊 description

- ❌ "处理相关任务"、"提供帮助"
- ✅ 说出**什么时候用**、做什么、产出什么

### 禁止：Skill 之间互相调用

- ❌ Skill A 内部直接调用 Skill B
- ✅ 用 Workflow 编排多个 Skill

---

## 2. Workflow 编写

### 禁止：嵌入业务逻辑

- ❌ "如果需求复杂，则先调研；否则跳过"
- ✅ 流程是线性的，复杂度由 Runtime 决定调哪个 Workflow

### 禁止：动态选择 Skill

- ❌ "根据语言选择不同的 coding skill"
- ✅ 每个 Workflow 明确指定所有 Skill

### 禁止：嵌入 Prompt

- ❌ 在 Workflow 步骤里写大段 Prompt 文本
- ✅ 只写 Skill 名 + 输入 + 输出

### 禁止：嵌套 Workflow

- ❌ Workflow A 里调用 Workflow B
- ✅ 各 Workflow 独立、可组合

### 禁止：单文件违反规范

- ❌ `workflows/<name>/README.md`
- ❌ `workflows/<name>/examples/`
- ❌ WORKFLOW.md 末尾 `# End`

---

## 3. Knowledge 编写

### 禁止：含执行逻辑

- ❌ "如果遇到 X 则执行 Y"
- ✅ Knowledge 只记录规范、经验、术语

### 禁止：含 Prompt 或 Workflow

- ❌ 在 KNOWLEDGE.md 里写完整的执行流程
- ✅ Knowledge 是被动参考资料

### 禁止：含 Skill 调用

- ❌ "请用 coding skill 实现以下功能"
- ✅ Knowledge 只告诉 Agent「怎么做是对的」

---

## 4. Template 编写

### 禁止：含判断逻辑

- ❌ "如果项目复杂则...否则..."
- ✅ Template 只规定结构与字段，不规定如何填写

### 禁止：含 Skill 调用

- ❌ "请调用 requirement skill"
- ✅ Template 是被动占位符

### 禁止：单文件违反规范

- ❌ `templates/<name>/README.md`（冗余）
- ✅ 仅含 `TEMPLATE.md`

---

## 5. Runtime 入口

### 禁止：入口文件含业务

- ❌ 在 CLAUDE.md 里写 Skill 内容
- ✅ 入口文件只声明 AOS Root + 加载策略 + 入口引用

### 禁止：覆盖第三方 Skill

- ❌ deploy 时 `rm -rf ~/.agents/skills/`
- ✅ 增量复制 AOS Skill，保留第三方 Skill

### 禁止：把 docs / examples 部署到 ~/.agents

- ❌ 把开发资料带进 Runtime 目录
- ✅ ~/.agents/ 只含运行时必要内容

---

## 6. MANIFEST 与索引

### 禁止：手写 MANIFEST 后不跑 build 脚本

- ❌ 改了 Skill 目录但忘更新 MANIFEST.md
- ✅ 改完后跑 `bash scripts/build-manifest.sh`

### 禁止：MANIFEST 与实际不同步

- ✅ CI 跑 `build-manifest.sh --check`，发现不同步就失败

---

## 7. 文档（docs/）

### 禁止：开发资料进 MANIFEST

- ❌ 把 Philosophy / PRD / ADR 加进 MANIFEST
- ✅ MANIFEST 只列 Skills / Workflows / Knowledge / Templates

### 禁止：docs/ 跑 build-manifest 包含

- ✅ build 脚本明确只扫 4 个目录

---

## 8. 内容质量（来自 taste-skill Anti-Slop）

### 禁止：营销腔

- ❌ "本系统非常强大"、"非常灵活"、"非常优雅"
- ✅ 用具体能力描述，不用形容词堆砌

### 禁止：空话

- ❌ "进行相关处理"、"做出合理判断"
- ✅ 写出具体步骤

### 禁止：凑数

- ❌ 为了显得完整而虚构示例 / 功能
- ✅ 内容不足就写「未实现」或「TODO」

### 禁止：复制粘贴

- ❌ 多处 Skill 内容大量重复
- ✅ 抽公共内容到 Knowledge，Skill 引用

### 禁止：缺乏示例

- ❌ 只有抽象描述，没有具体例子
- ✅ 关键概念给一个最小示例

---

## 9. 协议稳定性

### 禁止：擅自修改 Protocol

- ❌ 改 `protocols/*.md` 里的定义
- ✅ 修改必须：
  1. 提出 ADR
  2. 团队评审
  3. 更新 VERSION（Major）
  4. 更新 CHANGELOG

### 禁止：Protocol 与 Skill 不一致

- ❌ Skill 实际行为违反 protocol 定义
- ✅ `scripts/lint-skill.sh` 检查

---

## 10. Token 与性能

### 禁止：一次加载全部 Skill

- ❌ 启动时 `cat ~/.agents/skills/*/SKILL.md`
- ✅ 通过 MANIFEST 按需发现 → 只读匹配项

### 禁止：冗余 frontmatter

- ❌ 每个 Skill frontmatter 写 10 个字段
- ✅ 仅 `name` + `description`

### 禁止：测试文件混在 Skill 目录

- ❌ `skills/<name>/tests/`
- ✅ 测试统一在 CI 跑，不进 Skill 目录

---

## 11. 熔断机制（来自一线工程纪律）

### 禁止：同一问题死磕

- ❌ 同一 Bug 连续修改 3 次仍未解决，继续局部尝试
- ✅ 第 3 次失败时停止修改，重新分析问题——可能是「方向错了」而不是「改得不够」

### 强制：失败模式升级

```
第 1 次失败 → 重试，调整假设
第 2 次失败 → 换思路或换工具
第 3 次失败 → 停止，回退到上游（grill / design / requirement）重新审视
```

**核心原则：失败不是「做得不够」的信号，是「方向可能错了」的信号。**

### 禁止：死磕的副作用

- 引入越来越复杂的 workaround
- 掩盖真实问题
- 失去客观判断

---

## 12. 输出规范

### 禁止：开放式提问

- ❌ 「你想怎么做？」「接下来怎么办？」
- ✅ 给具体选项 + 推荐：「有 A、B、C 三种方案，我推荐 B，因为...，你看选哪个？」

### 禁止：先改再说

- ❌ 直接修改代码再解释
- ✅ 先说影响范围（哪些文件、改动大小、风险）→ 等确认 → 再改

### 禁止：模糊形容词

- ❌ 「差不多」「应该可以」「可能没问题」
- ✅ 量化：「覆盖 80%」「P95 < 500ms」「3 个文件改动」

### 强制：读完再改

- ❌ 没读相关代码就开始改
- ✅ 先读（设计文档、已有代码、相关 Skill）→ 分析 → 改动

### 强制：影响先于改动

任何代码改动前必须回答：

1. 影响哪些文件？
2. 是否破坏现有功能？
3. 是否需要更新文档？
4. 是否需要更新测试？

---

## 13. 触发停止（Stop Triggers）

遇到以下情况**立即停止**，等待用户确认后再继续：

```
❌ 继续往下做（基于猜测或惯性）
✅ 停下来汇报 + 列选项 + 等确认
```

触发停止的 6 种情况：

- **需求存在歧义**：用户的描述有多种合理解读
- **多个合理方案**：实现路径不唯一
- **涉及数据库结构修改**：表结构 / 字段 / 索引变化
- **涉及公共 API 修改**：对外暴露的接口变化
- **涉及大量重构**：超过当前任务范围的代码改动
- **可能影响已有功能**：存在回归风险

### 不要做的事

- ❌ 继续按惯性做（猜用户的意图）
- ❌ 「先做着，等用户问起来再说」
- ❌ 在汇报时隐瞒触发了停止条件
- ❌ 等用户问起才说「其实有歧义」

---

## 14. 禁止推测补充（No Hallucination）

Agent 不能根据推测补充以下内容：

- ❌ 业务规则（猜用户公司的业务逻辑）
- ❌ API 参数（猜接口需要哪些字段）
- ❌ 数据结构（猜字段类型 / 关系）
- ❌ 数据库字段（猜 schema 设计）

### 信息不足时

```
❌ 「我推测应该这样...」（瞎补）
✅ 「这个我需要确认：...」（直接问）
```

### 原则

- **问比猜好**：宁可多问 3 句，不可猜错 1 个字段
- **承认不知**：「我信息不足」是合法答案
- **不发明用户没说的**：产品文档没写的功能不要主动加

---

## 15. Definition of Done（完成定义）

任务完成必须满足以下 5 项：

- [ ] 功能完成（按需求全部实现）
- [ ] 无明显 Bug（核心路径通过）
- [ ] 构建通过（若可执行：npm run build / cargo build / ...）
- [ ] 更新文档（README / API / 设计 / Changelog）
- [ ] 更新任务状态（phasetasks.md / progress.md）

### 硬性纪律

- 5 项必须全部勾选才能算「完成」
- 不允许「差不多就行」
- 不允许「构建没跑但应该没问题」

---

## 16. 决策优先级（文档冲突时）

当多份项目文档冲突时，按以下优先级：

```
requirements.md > architecture.md > phasetasks.md > progress.md
```

### 冲突处理

```
❌ 自行决定按哪份文档
✅ 停下来汇报冲突 + 等用户确认
```

### 优先级解释

- **requirements.md** 最高——需求是源头
- **architecture.md** 次之——架构服务于需求
- **phasetasks.md** 再次——任务服从架构
- **progress.md** 最低——进度记录反映前三个

---

## 规则执行

- **lint 自动检查**：`bash scripts/lint-skill.sh` 检查大部分规则
- **CI 强制**：未来加入 GitHub Actions，PR 触发 lint
- **Code Review**：人工复核未自动化的部分（业务纪律、内容质量）

## 规则演化

Hard Rules 本身可以新增，但**修改或删除需要 ADR 记录**。

新增步骤：

1. 在 `docs/adr/` 新建 ADR，解释为什么加这条规则
2. 在本文件加新章节
3. 更新 `scripts/lint-skill.sh`（如可自动检查）
4. 更新 README 引用

---

> **违背 Hard Rules 等于违背 AOS 的设计哲学。** 如果某条规则不合理，应该通过 ADR 调整规则本身，而不是绕过它。