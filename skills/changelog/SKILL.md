---
name: changelog
description: 把 Git 变更整理为面向用户的版本变更日志；不用于通用项目文档或提交操作
---

# Changelog

把零散的 git commits 翻译成面向用户和团队的**结构化变更日志**——按 Keep a Changelog 规范组织，标注版本号、Breaking Changes、升级路径。

**与 `document` 的区别：** `document` 写稳定的技术文档（README、API）；`changelog` 记录**版本间的变化**——是时间的纵切面，不是空间的横切面。

## 何时使用

- 准备发布新版本，需要写 release notes
- 团队成员想知道「这个版本变了什么」
- 用户升级前想知道「会不会破坏我的使用」
- 维护 `CHANGELOG.md` 文件

不要用于：

- 写 README / API 文档（用 `document`）
- 完整版本发布流程（用 `release` workflow，changelog 是其中一步）
- 写 commit message（那是 git 操作的一部分）

---

## 流程

### 1. 锚定范围

明确这次记录什么：

- 版本号（v1.2.0 / v2.0.0）
- 上次发布到这次之间的 commits（默认 `git log <last-tag>..HEAD`）
- 受众：开发者 / 最终用户 / 两者

### 2. 解析 commits

按 Conventional Commits 分类：

```
feat     → Added
fix      → Fixed
refactor → Changed
perf     → Changed
docs     → 文档（一般不进 changelog）
test     → 测试（一般不进 changelog）
chore    → 一般不进 changelog
style    → 一般不进 changelog
revert   → Removed / Fixed
BREAKING → 单独标记
```

无 Conventional Commits 规范的，需要先看 commit 内容判断类别。

### 3. 用户视角重写

每条 commit 不是直接粘贴，而是**翻译成用户视角的描述**：

```
❌ git commit: feat: add JWT refresh token rotation
✅ Added: 登录 Token 自动轮转，提升长期会话安全性

❌ fix: null check in calculateDiscount
✅ Fixed: 修复特殊价格组合下的崩溃问题
```

**用户不关心代码细节，关心行为变化。**

### 4. 组织结构

按 Keep a Changelog 规范：

```markdown
# Changelog

## [Unreleased]

### Added
- ...

### Changed
- ...

## [1.2.0] - 2026-07-20

### Added
- 登录 Token 自动轮转，提升长期会话安全性
- ...

### Changed
- ...

### Deprecated
- 旧版 API `/v1/users` 将在 v2.0.0 移除

### Removed
- ...

### Fixed
- 修复特殊价格组合下的崩溃问题
- ...

### Security
- 升级 bcrypt 到 5.x
```

### 5. 标注 Breaking Changes

任何破坏性变更单独突出：

```markdown
### ⚠️ Breaking Changes

- **API 路径变更**：`/v1/users` → `/v2/users`
- **认证方式变更**：从 Session 改为 JWT
- **最低 Node 版本**：从 14 升到 18

**升级路径：** [UPGRADE.md](UPGRADE.md)
```

### 6. 输出格式

```markdown
# Changelog: v<版本>

**发布日期**：YYYY-MM-DD
**类型**：Major / Minor / Patch
**涵盖 commits**：N 个

## ⚠️ Breaking Changes（如有）
- ...

## ✨ Added
- [用户视角描述]
- ...

## 🔄 Changed
- ...

## 🗑️ Deprecated
- ...

## 🐛 Fixed
- ...

## 🔒 Security
- ...

## 升级指南
[简要步骤，复杂时单独 UPGRADE.md]

## 参考
- Commits: [git log 范围]
- Issue: [#123, #456]
- PR: [#789]
```

---

## Keep a Changelog 类别

只使用这 7 个类别（其它都归到 Changed 或不放进 changelog）：

| 类别 | 含义 | 例子 |
|---|---|---|
| **Added** | 新功能 | 新增导出功能 |
| **Changed** | 现有功能变更 | 改写搜索逻辑 |
| **Deprecated** | 即将移除（但当前还能用） | 旧 API 标记废弃 |
| **Removed** | 已移除 | 删除旧版界面 |
| **Fixed** | Bug 修复 | 修复崩溃 |
| **Security** | 安全相关 | 升级加密算法 |
| **⚠️ Breaking Changes** | 破坏性变更（自定类别，单独突出） | API 不兼容 |

---

## Hard Rules

### 禁止：直接贴 commit message

```
❌ feat: add JWT refresh token rotation
✅ Added: 登录 Token 自动轮转，提升长期会话安全性
```

### 禁止：用户看不到的改动塞进 changelog

```
❌ chore: update dependencies
❌ refactor: extract helper function
（这些用户不关心，不进 changelog）
```

### 禁止：遗漏 Breaking Changes

```
❌ 静默修改 API 不通知用户
✅ 单独列出，标注升级路径
```

### 禁止：版本号不规范

```
❌ 1.2、v1.2、version 1.2
✅ 1.2.0（SemVer 规范）
```

### 禁止：日期格式不统一

```
✅ 2026-07-20（ISO 8601）
❌ 7/20/2026、20/07/2026、July 20
```

### 禁止：把文档 / 测试 commit 当作 feature

```
❌ docs: update README → 列为「Added: 文档更新」
（除非用户可见的文档变化，否则不放进）
```

---

## 行为准则

- **用户视角**：用户不读代码，只读 changelog
- **行为变化 > 实现细节**：改了什么行为，而不是改了哪个函数
- **诚实标注**：不确定的修复用「尝试修复」而非「修复了」
- **可读 > 完整**：宁可少列，不要堆无意义条目
- **每条都可验证**：用户能根据描述验证自己是否受影响

## 不要做的事

- 不要把每次 commit 都列出来（选重要的）
- 不要用技术术语描述用户行为变化
- 不要列内部重构（除非影响用户）
- 不要在没有 Breaking Changes 时硬塞一个空类别
- 不要在 changelog 里夹带营销话术

---

## Conventional Commits 解析规则

```
feat(scope): subject              → Added
feat(scope)!: subject             → Added + Breaking Changes
fix(scope): subject               → Fixed
fix(scope)!: subject              → Fixed + Breaking Changes
refactor(scope): subject          → Changed（如果影响用户行为）
perf(scope): subject              → Changed
docs(scope): subject              → 不进 changelog
test(scope): subject              → 不进 changelog
chore(scope): subject             → 不进 changelog
style(scope): subject             → 不进 changelog
build(scope): subject             → 不进 changelog
ci(scope): subject                → 不进 changelog
revert: ...                       → Removed 或 Fixed
```

无 Conventional Commits 规范的仓库：人工判断每条 commit 的类别。

---

## 与其它 Skill 的协作

| Skill | 关系 |
|---|---|
| `git` | 上游：从 git log 提取 commits |
| `document` | 互补：document 写静态文档，changelog 写动态变化 |
| `release` | 上游：release workflow 包含 changelog 步骤 |
| `migration` | 并行：Breaking Changes 需要 migration 协助升级 |

---

## 风格参考

- [Keep a Changelog](https://keepachangelog.com/) — 规范来源
- [Conventional Commits](https://www.conventionalcommits.org/) — commit 规范
- [Semantic Versioning](https://semver.org/) — 版本号规范

---

## 示例

完整示例：

```markdown
# Changelog: v1.2.0

**发布日期**：2026-07-20
**类型**：Minor
**涵盖 commits**：23 个

## ⚠️ Breaking Changes
- 无

## ✨ Added
- 任务导出功能：支持 CSV 和 JSON 格式
- 暗色模式：跟随系统设置自动切换
- 快捷键面板：按 `?` 查看所有快捷键

## 🔄 Changed
- 任务列表性能优化：1000+ 任务时滚动更流畅
- 重构设置页布局，更易导航

## 🗑️ Deprecated
- 旧版 CSV 导出（不带编码选项）将在 v2.0 移除

## 🐛 Fixed
- 修复中文输入时 IME 卡顿问题
- 修复 Safari 15 下登录按钮无响应
- 修复时区设置在某些情况下不生效

## 🔒 Security
- 升级依赖：修复 jsonwebtoken 已知漏洞
```

简洁版本（用于发布说明）：

```markdown
## v1.2.0 主要更新

🎉 **新功能**
- 任务导出（CSV / JSON）
- 暗色模式
- 快捷键面板

⚡ **改进**
- 任务列表性能优化

🐛 **修复**
- Safari 15 登录问题
- 中文输入卡顿
```
