---
name: skill-authoring
description: 创建或修改 AOS Skill，定义单一职责、description、正负触发边界和执行步骤，并同步岗位标签、路由数据、回归用例、文档与 Manifest 验证；不用于普通技术文档、通用 Prompt 或业务代码实现
---

# Skill Authoring

把一项可复用能力写成职责清晰、可按需加载、能被 Runtime 稳定匹配并可回归验证的 AOS Skill。

## 何时使用

- 新增一个 `skills/<name>/SKILL.md`
- 修改现有 Skill 的触发条件、职责边界或执行流程
- 修复两个或多个 Skill 之间的误匹配
- 为 Skill 补充岗位标签、路由规则和匹配回归用例

不要用于：

- 编写 README、API 文档或普通项目说明（用 `document`）
- 编写通用 system prompt、few-shot 或图像 Prompt（用 `prompt-writing`）
- 实现应用功能或普通源码修改（用 `coding`）
- 只安装一个已经存在的第三方 Skill（使用安装能力）

## 核心标准

- **单一职责**：一个 Skill 只产生一种主要交付物或完成一个主要阶段
- **描述即路由**：frontmatter 的 `description` 同时表达动作、交付物、使用场景和最关键排除边界
- **正负对称**：说明何时选择，也说明相邻场景应选择哪个 Skill
- **步骤可验收**：每个关键步骤有可检查的完成条件，避免“分析一下”“确保质量”等空指令
- **单一事实源**：路由规则维护在 `data/skill-routing.json`，岗位标签维护在 `data/skill-roles.json`，`MANIFEST.md` 只通过脚本生成
- **渐进披露**：默认只创建 `SKILL.md`；只有确有复用价值时才增加 scripts、references 或 assets

## 流程

1. **确认能力缺口**：读取 `MANIFEST.md` 并检查相邻 Skill，证明新职责不能由现有能力清晰承担
2. **定义边界契约**：写出目标交付物、正向触发、负向触发、上游输入、下游用途和停止条件
3. **选择名称**：使用唯一、简短的 kebab-case 名称；名称表达稳定动作或能力，不使用宽泛的 helper、assistant 等词
4. **编写 frontmatter**：只保留 `name` 与 `description`；description 前置核心动作，并包含最容易混淆的排除边界
5. **编写执行指南**：使用祈使式步骤，保留会改变行为的规则；为流程、输出和失败处理设置检查标准
6. **处理相邻能力**：必要时同步修改相邻 Skill 的 description 或匹配边界，避免新能力只靠唯一关键词触发
7. **登记元数据**：更新 `data/skill-roles.json`；高混淆能力更新 `data/skill-routing.json` 的选择条件、排除条件和示例
8. **补充回归语料**：每个路由 Skill 至少增加 2 条自然语言用例，包含预期能力、易混淆候选和选择理由
9. **更新维护文档**：同步 README、选择指南、测试统计和 CHANGELOG 中受影响的事实
10. **生成并验证**：重新生成 Manifest，运行 Skill lint 与路由回归；修复所有错误和警告后交付

完成标准：Skill 文件、岗位标签、必要的路由与回归数据、文档和生成物保持一致，完整验证结果为零错误、零警告。

## SKILL.md 骨架

```markdown
---
name: skill-name
description: <动作 + 交付物 + 触发场景>；不负责 <相邻职责>
---

# Skill Name

[一句话目的]

## 何时使用
- [正向触发]

不要用于：
- [相邻场景]（用 `other-skill`）

## 流程
1. **动作**：[可执行说明]

完成标准：[可检查条件]

## 输出格式
[稳定的输出结构]

## 行为准则
- **原则**：[真正改变执行行为的规则]
```

## 验证命令

Windows：

```powershell
python .\scripts\build-manifest.py
.\scripts\lint-skill.ps1 .
.\scripts\test-skill-routing.ps1
```

macOS / Linux：

```bash
python3 scripts/build-manifest.py
bash scripts/lint-skill.sh .
bash scripts/test-skill-routing.sh
```

## 交付格式

```markdown
# Skill Authoring Report

## 新增 / 修改
- `skills/<name>/SKILL.md` — [职责]

## 路由边界
- 选择：...
- 排除：...
- 相邻 Skill：...

## 同步项
- 岗位标签：...
- 路由数据：...
- 回归用例：...
- 文档：...

## 验证
- Manifest：Passed / Failed
- Lint：Passed / Failed
- Routing：Passed / Failed
```

## 行为准则

- **不复制相邻 Skill**：职责重叠时先收窄边界，不靠描述堆砌解决
- **不手改 Manifest**：它是生成物，修改源文件后重新生成
- **不以示例代替规则**：示例用于验证边界，执行规则必须写清楚
- **不自动部署**：除非用户明确要求，否则不要运行部署脚本或写入用户的 `~/.agents/`