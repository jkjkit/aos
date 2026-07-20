---
name: git
description: 处理日常 Git 操作：分支、提交、合并、冲突解决、撤销与历史改写
---

# Git

封装日常 Git 操作的纪律性做法。**不替你跑命令**——只产出准确的命令清单和判断。

## 何时使用

- 要新建、切换、合并分支
- 要提交、推送、回退
- 遇到 rebase / merge 冲突
- 需要按 Conventional Commits 规范写提交
- 想撤销某次操作但不确定 `reset` / `revert` / `restore` 该用哪个

## 流程

任何操作前都先做这三步：

1. **明确目标**：用户想要的结果是什么
2. **看现状**：`git status`、`git branch --show-current`、`git log -n 5 --oneline`、`git remote -v`
3. **给出命令**：按顺序列出，每条命令说明它在做什么；破坏性命令（`reset --hard`、`push -f`、删除分支）单独标红并先问

## 常用模式

### 新功能分支

```bash
git fetch origin
git switch -c feat/<short-name> origin/main
```

### 提交

- 一次提交做一件事
- 消息遵循 Conventional Commits：`type(scope): subject`
- 类型：`feat` / `fix` / `refactor` / `docs` / `test` / `chore` / `perf`
- subject 不超过 50 字符，不写句末句号
- body 说明「为什么」，不是「做了什么」

### 同步主分支

优先 rebase 而不是 merge：

```bash
git fetch origin
git rebase origin/main
```

合并冲突时，逐文件 `git status` 看冲突标记，一次解决一个文件，`git add` 后 `git rebase --continue`。

### 撤销

| 想要的结果 | 命令 |
|-----------|------|
| 撤销工作区修改（未暂存） | `git restore <file>` |
| 撤销已暂存 | `git restore --staged <file>` |
| 改写最近一次未推送的提交 | `git commit --amend` |
| 反转已推送的提交（保留历史） | `git revert <sha>` |
| 回到某次提交（丢弃之后所有改动） | `git reset --hard <sha>`——推送过则不可用 |

### 历史改写

推送前可用 `git rebase -i HEAD~n` 整理。**已推送的分支不要 force push**——除非团队明确允许。

### 临时保存

`git stash push -m "<why>"` 暂存未提交的工作；恢复用 `git stash pop`。不要把 stash 当长期分支用。

## 输出格式

```markdown
# Git 操作

## 目标
[用户想达成什么]

## 现状
- 当前分支：xxx
- 与 main 差异：N 个提交 / M 个未跟踪文件

## 命令
1. `git ...` — 说明
2. `git ...` — 说明（⚠️ 破坏性，先确认）

## 风险
- [可能的副作用与回滚方式]
```

## 行为准则

- **先看再动**：永远先 `git status`
- **破坏性操作必须确认**：`reset --hard`、`push -f`、删除分支、`clean -fd`
- **不替你执行**：输出命令清单让用户确认
- **解释每条命令**：不是默写，是说它在做什么

## 不要做的事

- 不要建议 `git push --force` 到 main / master
- 不要用 `git commit -m "fix"` 这种空消息
- 不要把无关改动塞进一个提交
- 不要跳过 `git fetch` 直接 rebase / merge

## 提交前自检清单（Pre-commit Checklist）

每次 `git commit` 前必须做：

```bash
# 1. 查看改动
git diff --stat
git diff
```

确认以下**都不存在**：

- [ ] **调试代码**：`debugger` / `console.log` / `print()` / `var_dump` 等
- [ ] **临时文件**：`temp/`、`*.tmp`、`*.bak`、`*.swp`
- [ ] **无关修改**：超出本次任务范围的改动（即使「顺手修了」也要拆出来）
- [ ] **注释掉的代码**：大段 `// ...` / `/* ... */`
- [ ] **密钥 / 凭证**：`.env`、`*.pem`、`*.key`、API Token
- [ ] **依赖与构建产物**：`node_modules/`、`dist/`、`build/`、`.next/`
- [ ] **IDE 配置**：`.idea/`、`.vscode/`（除非项目要求）
- [ ] **测试覆盖率快照**：`coverage/`、`*.lcov`

### 自检命令

```bash
# 看改动文件列表
git diff --name-only

# 找调试代码
git diff | grep -E "console\.|debugger|TODO|FIXME|XXX"

# 找密钥（注意 false positive）
git diff | grep -iE "password|secret|token|api[_-]?key"
# ↑ 仔细看每行匹配是否真是密钥

# 看行数变化
git diff --shortstat
```

### 命中任何一项怎么办

- 调试代码 → 删掉
- 临时文件 → 不 `git add`
- 无关修改 → `git restore` 或拆成另一个提交
- 密钥 → **立即删除 + 轮换密钥**（已泄漏）
- 依赖 / 构建产物 → 不应被追踪；加进 `.gitignore`

### 不要做的事

- ❌ 「等发现了再说」——必须每次 commit 前都检查
- ❌ 「只是几行调试代码没事」——调试代码就是调试代码
- ❌ 「反正本地仓库没人看到」——本地 commit 也会被 push
- ❌ 跳过自检直接 `git commit -m "..."`