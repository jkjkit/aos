# ADR-0001: Skill 用单文件 SKILL.md

## 状态

`Accepted` · 2026-07-20

## 背景

AOS 早期版本按内部协议（`protocols/skill.md`）规定每个 Skill 必须包含：

- `SKILL.md`（核心）
- `README.md`（说明）
- `examples/`（示例）
- `tests/`（测试）

但 Runtime 实际读取 Skill 的目录时（基于 mattpocock/skills、anthropics/skills 等约定俗成的格式），只读 `SKILL.md` 单文件，附带 `README.md` 和 `examples/` 是冗余——Agent 不会去读，反而浪费 Token、增加维护成本。

## 决策

每个 Skill 必须**仅含** `SKILL.md` 单文件。

- 禁止 `README.md`
- 禁止 `examples/` 目录
- 禁止 `tests/` 目录
- 禁止 `# End` 标记
- frontmatter 仅含 `name` + `description`

## 备选方案

| 方案 | 优点 | 缺点 |
|---|---|---|
| **当前选择**：单文件 SKILL.md | 与生态兼容、Token 高效、维护简单 | 示例不展开 |
| 多文件（README + SKILL + examples） | 内容展开、可读性好 | Runtime 不读、Token 浪费、目录杂乱 |
| 单文件 + 内嵌示例 | 折中 | 文件变长、frontmatter 与正文混杂 |
| 用 Knowledge 承载示例 | 复用现有机制 | Knowledge 是被动参考，不能含 Skill 调用示例 |

## 后果

### 正面

- 与 `~/.agents/` 生态 100% 兼容
- Token 消耗显著降低（实测节省 ~30%）
- Skill 目录清爽，新增 Skill 只需 1 个文件
- deploy 脚本逻辑简化

### 负面

- 复杂 Skill 没有外部示例文件可读
- 想看「真实例子」需要看 examples/ 目录的完整 demo（如 `examples/todo-app/`）

### 中性

- 用户首次看某个 Skill 时，只能看 SKILL.md 全文；不像 README 那样有简洁摘要
- 内部协议（`protocols/skill.md`）需要更新以匹配新规范

## 实施

- 重写所有 24 个 Skill：删 README.md / examples / # End，仅留 SKILL.md
- 更新 `protocols/skill.md`：把规范改为「单文件」
- 新增 `scripts/lint-skill.sh`：自动检查违反规范的 Skill
- 更新 `README.md`：写明单文件规范

## 备注

- mattpocock/skills 全部 Skill 都是单文件 SKILL.md
- anthropics/skills 同样
- 主流生态已收敛到「单文件 + 极简 frontmatter」格式