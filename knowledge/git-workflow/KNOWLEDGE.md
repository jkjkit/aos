# Git Workflow

Git 工作流程和最佳实践。


---


## 工作流模型


### Git Flow


适用于定期发布的项目。


```

main (生产)
    │
    ├─── release/v1.0 (发布分支)
    │
develop (开发)
    │
    ├─── feature/user-auth (功能分支)
    ├─── feature/dashboard (功能分支)
    │
    └─── hotfix/critical-bug (热修复分支)
```

**分支说明：**


- **main** - 生产分支，只包含发布版本

- **develop** - 开发分支，最新开发代码
- **feature/** - 功能分支，从 develop 创建
- **release/** - 发布分支，从 develop 创建
- **hotfix/** - 热修复分支，从 main 创建

---


### GitHub Flow


适用于持续部署的项目。


```

main
    │
    ├─── feature/add-login
    ├─── fix/bug-123
    └─── docs/update-readme
```

**流程：**

1. 从 main 创建分支
2. 提交变更
3. 创建 Pull Request
4. 代码审查
5. 合并到 main
6. 自动部署

**优点：**

- 简单易懂
- 持续部署
- 适合团队协作

---


### GitLab Flow


结合了 Git Flow 和 GitHub Flow 的优点。


```

main
    │
    ├─── feature/xxx
    │
    └─── production (生产环境)
         └─── staging (预发布环境)
```

**特点：**

- 环境分支（production, staging）
- 功能分支合并到 main
- main 推送到环境分支部署

---


## 分支命名规范


### 命名格式


```

<type>/<description>
```

**Type 类型：**


| Type | 说明 | 示例 |

|------|------|------|
| feature | 新功能 | feature/user-authentication |
| fix | Bug 修复 | fix/login-error |
| hotfix | 紧急修复 | hotfix/critical-security-issue |
| release | 发布准备 | release/v1.2.0 |
| docs | 文档更新 | docs/api-documentation |
| refactor | 代码重构 | refactor/user-service |
| test | 测试相关 | test/add-unit-tests |
| chore | 杂项任务 | chore/update-dependencies |

### 命名规则


✅ **正确：**

```
feature/user-authentication
fix/login-button-style
docs/update-readme
```

❌ **错误：**

```
new_feature
fix_bug
my-branch
```

---


## 提交规范


### Conventional Commits


格式：


```

<type>(<scope>): <subject>

<body>


<footer>

```

### Type 类型


| Type | 说明 |

|------|------|
| feat | 新功能 |
| fix | Bug 修复 |
| docs | 文档 |
| style | 代码格式 |
| refactor | 重构 |
| perf | 性能优化 |
| test | 测试 |
| build | 构建系统 |
| ci | CI 配置 |
| chore | 其他 |
| revert | 回滚 |

### 示例


**简单提交：**

```bash
git commit -m "feat: add user authentication"
```

**完整提交：**

```bash
git commit -m "feat(auth): add JWT token support

- Implement JWT token generation

- Add token verification middleware
- Update authentication tests

Closes #123"

```

**破坏性变更：**

```bash
git commit -m "feat!: change API response format

BREAKING CHANGE: The API response format has changed.

Old: { data: ... }
New: { result: ... }"
```

---


## 基本工作流程


### 1. 克隆仓库


```bash

git clone https://github.com/username/repo.git
cd repo
```

### 2. 创建功能分支


```bash

# 确保在最新的 main
git checkout main
git pull origin main

# 创建新分支

git checkout -b feature/user-auth
```

### 3. 开发和提交


```bash

# 查看状态
git status

# 添加文件

git add src/auth.js
# 或添加所有变更
git add .

# 提交

git commit -m "feat(auth): implement login function"
```

### 4. 推送分支


```bash

git push origin feature/user-auth
```

### 5. 创建 Pull Request


在 GitHub 上创建 Pull Request。


### 6. 代码审查和合并


审查通过后，合并到 main。


### 7. 删除分支


```bash

# 删除本地分支
git branch -d feature/user-auth

# 删除远程分支

git push origin --delete feature/user-auth
```

---


## 常用命令


### 查看状态


```bash

# 查看工作区状态
git status

# 查看提交历史

git log
git log --oneline --graph

# 查看差异

git diff
git diff --staged
```

### 分支操作


```bash

# 查看分支
git branch                    # 本地分支
git branch -r                 # 远程分支
git branch -a                 # 所有分支

# 创建分支

git branch feature/new-feature

# 切换分支

git checkout feature/new-feature
# 或
git switch feature/new-feature

# 创建并切换

git checkout -b feature/new-feature
# 或
git switch -c feature/new-feature

# 删除分支

git branch -d feature/old-feature    # 安全删除
git branch -D feature/old-feature    # 强制删除

# 重命名分支

git branch -m old-name new-name
```

### 暂存操作


```bash

# 暂存变更
git stash
git stash save "work in progress"

# 查看暂存列表

git stash list

# 应用暂存

git stash apply              # 保留暂存
git stash pop                # 应用并删除

# 删除暂存

git stash drop stash@{0}
git stash clear              # 清空所有
```

### 撤销操作


```bash

# 撤销工作区修改
git checkout -- file.txt
# 或
git restore file.txt

# 撤销暂存

git reset HEAD file.txt
# 或
git restore --staged file.txt

# 撤销提交（保留变更）

git reset --soft HEAD~1

# 撤销提交（丢弃变更）

git reset --hard HEAD~1

# 回滚特定提交

git revert <commit-hash>
```

### 合并操作


```bash

# 合并分支
git merge feature/new-feature

# 变基

git rebase main

# 交互式变基

git rebase -i HEAD~3
```

### 远程操作


```bash

# 查看远程仓库
git remote -v

# 添加远程仓库

git remote add origin https://github.com/user/repo.git

# 获取远程更新

git fetch origin

# 拉取并合并

git pull origin main

# 推送

git push origin feature/new-feature

# 强制推送（慎用）

git push --force-with-lease
```

---


## Pull Request 流程


### 1. 创建 PR


```bash

# 推送分支
git push origin feature/user-auth

# 在 GitHub 上创建 PR

```

### 2. PR 描述


```markdown

## 描述
实现用户认证功能

## 变更类型

- [x] 新功能
- [ ] Bug 修复
- [ ] 破坏性变更

## 相关 Issue

Closes #123

## 测试

- [x] 单元测试通过
- [x] 手动测试通过

## 截图

[如适用]

## 检查清单

- [x] 代码符合规范
- [x] 添加了测试
- [x] 更新了文档
```

### 3. 代码审查


- 审查者留下评论

- 作者修改代码
- 推送更新

### 4. 合并策略


**Merge Commit（保留历史）：**

```bash
git merge --no-ff feature/user-auth
```

**Squash and Merge（压缩提交）：**

```bash
git merge --squash feature/user-auth
git commit -m "feat: add user authentication"
```

**Rebase and Merge（线性历史）：**

```bash
git rebase main
git push --force-with-lease
```

---


## 冲突解决


### 发生冲突


```bash

git merge feature/new-feature
# Auto-merging file.txt
# CONFLICT (content): Merge conflict in file.txt
```

### 解决步骤


1. **查看冲突文件**


```bash

git status
```

2. **编辑冲突文件**


```javascript

<<<<<<< HEAD
const version = '1.0.0';
=======
const version = '1.1.0';
>>>>>>> feature/new-feature
```

修改为：


```javascript

const version = '1.1.0';
```

3. **标记为已解决**


```bash

git add file.txt
```

4. **完成合并**


```bash

git commit -m "merge: resolve conflicts"
```

---


## 最佳实践


### 1. 提交频率


- 频繁提交小的变更

- 每个提交是一个逻辑单元
- 避免大量文件的单次提交

### 2. 提交信息


- 使用有意义的提交信息

- 遵循提交规范
- 引用相关 Issue

### 3. 分支管理


- 及时删除已合并的分支

- 保持分支名称清晰
- 避免长期存在的功能分支

### 4. 代码审查


- 所有代码都应该经过审查

- 提供建设性的反馈
- 及时响应审查意见

### 5. 保持同步


```bash

# 定期同步主分支
git checkout main
git pull origin main

# 更新功能分支

git checkout feature/my-feature
git rebase main
```

### 6. 避免直接推送到主分支


```bash

# 保护主分支
# 在 GitHub 设置中启用分支保护
```

---


## Git 钩子


### 客户端钩子


**pre-commit** - 提交前检查


```bash

#!/bin/sh
# .git/hooks/pre-commit

npm run lint

npm test
```

**commit-msg** - 检查提交信息


```bash

#!/bin/sh
# .git/hooks/commit-msg

commit_msg=$(cat "$1")

pattern="^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .{1,50}"

if ! echo "$commit_msg" | grep -qE "$pattern"; then

    echo "Error: Invalid commit message format"
    exit 1
fi
```

### 使用 Husky


```bash

npm install --save-dev husky

# 初始化

npx husky install

# 添加 pre-commit 钩子

npx husky add .husky/pre-commit "npm test"
```

---


## Git 别名


添加到 `~/.gitconfig`：


```ini

[alias]
    # 常用简写
    st = status
    co = checkout
    br = branch
    ci = commit
    
    # 日志
    lg = log --oneline --graph --all
    last = log -1 HEAD
    
    # 撤销
    undo = reset --soft HEAD~1
    unstage = reset HEAD --
    
    # 分支
    branches = branch -a
    tags = tag -l
```

使用：


```bash

git st
git lg
git undo
```

---


## 问题排查


### 误删文件


```bash

# 恢复文件
git checkout HEAD -- file.txt
```

### 提交到错误分支


```bash

# 1. 保存提交
git log  # 记下 commit hash

# 2. 切换到正确分支

git checkout correct-branch

# 3. 应用提交

git cherry-pick <commit-hash>

# 4. 切换回错误分支

git checkout wrong-branch

# 5. 撤销提交

git reset --hard HEAD~1
```

### 推送被拒绝


```bash

# 远程有更新，先拉取
git pull --rebase origin main

# 解决冲突后推送

git push origin main
```

---


## .gitignore


常见忽略模式：


```gitignore

# 依赖
node_modules/
vendor/

# 构建产物

dist/
build/
*.min.js

# 环境变量

.env
.env.local

# 日志

logs/
*.log

# IDE

.vscode/
.idea/
*.swp

# OS

.DS_Store
Thumbs.db

# 临时文件

tmp/
temp/
*.tmp
```

---


## 工具推荐


- **GitKraken** - 图形化 Git 客户端

- **SourceTree** - 免费 Git 客户端
- **GitHub Desktop** - GitHub 官方客户端
- **Git Lens** - VS Code 插件
- **Oh My Zsh** - Git 别名和提示

---


## 参考资源


- [Pro Git Book](https://git-scm.com/book)

- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)

---
---

---

## 提交消息格式（来自一线工程实践）

### 格式：`[Day X-T Y] 功能描述`

- `[Day X]` 是日期序号（第几天）
- `[T Y]` 是任务序号（第几个任务）
- `功能描述` 是具体做了什么

### 示例

```
[Day 1-T1] 项目初始化与依赖安装
[Day 1-T2] 数据库 schema 设计
[Day 2-T1] 用户注册接口实现
[Day 2-T2] 用户登录接口实现
[Day 3] 当日完成功能汇总（可选日终追加）
```

### 纪律

- **一次一事**：一个 commit 只做一件事
- **具体描述**：用「实现」「修复」「添加」开头，禁用「update」「fix bug」「改一下」
- **构建检查**：commit 前跑 `npm run build` 等构建命令
- **未获要求不自动 commit/push**：默认 `git add` + `git commit`，`push` 必须显式执行
- **禁止 force push**：不改写已共享历史

### 与 Conventional Commits 的关系

| 风格 | 适合场景 |
|------|----------|
| `[Day X-T Y]` | 个人 / 团队内部项目，强进度感 |
| `feat(scope): subject` | 开源项目，便于自动生成 changelog |

两者可结合：

```
[Day 1-T1] feat: 项目初始化与依赖安装
[Day 1-T2] feat(db): 数据库 schema 设计
```

---

## .gitignore 必备项

任何项目都应忽略这些文件：

```gitignore
# 密钥与凭证（绝对不能提交）
.env
.env.*
*.pem
*.key
*.crt
secrets/

# 依赖目录
node_modules/
venv/
.venv/
__pycache__/
*.pyc

# 构建产物
dist/
build/
.next/
out/
target/

# 用户上传媒体
uploads/
videos/
media/

# 临时与调试
temp/
*.log
*.swp
.DS_Store
.idea/
.vscode/

# 测试与覆盖率
coverage/
.nyc_output/

# 框架特定
.cache/
.parcel-cache/
```

### 提交前自检

每次 `git commit` 前：

- [ ] 没有 `.env` / 密钥文件
- [ ] 没有 `node_modules/` / `dist/`
- [ ] 没有 `temp/` / 日志
- [ ] 没有 IDE 配置（.idea / .vscode）

---

## 版本历史

- **v1.1.0** - 2026-07-20 - 新增提交消息格式与 .gitignore 必备项
- **v1.0.0** - 2026-07-19 - 初始版本## 版本历史

- **v1.1.0** - 2026-07-20 - 新增提交消息格式与 .gitignore 必备项
- **v1.0.0** - 2026-07-19 - 初始版本
