# Release Workflow

版本发布的标准工作流程。

---

## 适用场景

- 主版本发布（Major Release）
- 次版本发布（Minor Release）
- 补丁版本发布（Patch Release）
- 热修复发布（Hotfix Release）

---

## 版本规范

采用 **语义化版本（Semantic Versioning）**：`MAJOR.MINOR.PATCH`

- **MAJOR**：不兼容的 API 变更
- **MINOR**：向后兼容的功能新增
- **PATCH**：向后兼容的问题修复

**示例：**
- `v1.0.0` → `v2.0.0`：Major（破坏性变更）
- `v1.0.0` → `v1.1.0`：Minor（新功能）
- `v1.0.0` → `v1.0.1`：Patch（Bug 修复）

---

## 工作流程

```
规划发布
    ↓
Step 1: 发布准备
    ↓
Step 2: 版本升级
    ↓
Step 3: 变更日志
    ↓
Step 4: 测试验证
    ↓
Step 5: 创建发布
    ↓
Step 6: 部署发布
    ↓
Step 7: 发布通知
    ↓
Step 8: 监控反馈
```

---

## 详细步骤

### Step 1: 发布准备

**确认发布内容：**

- [ ] 所有计划功能已完成
- [ ] 所有已知 Bug 已修复
- [ ] 代码冻结（Code Freeze）
- [ ] 文档已更新

**检查依赖：**

```bash
# 检查过时的依赖
npm outdated

# 更新依赖（如需要）
npm update

# 审计安全漏洞
npm audit
npm audit fix
```

**运行完整测试：**

```bash
# 单元测试
npm test

# 集成测试
npm run test:integration

# E2E 测试
npm run test:e2e

# 代码覆盖率
npm run test:coverage
```

---

### Step 2: 版本升级

**更新版本号：**

```bash
# 使用 npm version（自动更新 package.json 和创建 git tag）
npm version patch   # 1.0.0 → 1.0.1
npm version minor   # 1.0.0 → 1.1.0
npm version major   # 1.0.0 → 2.0.0

# 或手动更新
# 编辑 package.json
# 编辑 VERSION 文件
```

**更新相关文件：**

- `package.json` - version 字段
- `VERSION` - 版本文件
- `README.md` - 安装说明中的版本
- `docs/` - 文档中的版本引用

---

### Step 3: 变更日志

**编写 CHANGELOG.md：**

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2026-07-19

### Added
- 新增用户认证功能
- 新增数据导出功能
- 新增邮件通知功能

### Changed
- 优化数据库查询性能
- 改进错误提示信息
- 更新依赖包到最新版本

### Fixed
- 修复登录页面的样式问题
- 修复数据导出时的乱码问题
- 修复并发访问时的数据不一致问题

### Deprecated
- `oldApi()` 函数将在 v2.0.0 中移除

### Removed
- 移除了不再使用的旧代码

### Security
- 修复了 SQL 注入漏洞
- 更新了有安全漏洞的依赖包
```

**变更日志类别：**

- **Added** - 新功能
- **Changed** - 功能变更
- **Deprecated** - 即将废弃
- **Removed** - 已删除
- **Fixed** - Bug 修复
- **Security** - 安全修复

---

### Step 4: 测试验证

**最终测试：**

- [ ] 所有自动化测试通过
- [ ] 手动回归测试完成
- [ ] 性能测试通过
- [ ] 安全测试通过
- [ ] 兼容性测试通过

**预发布测试：**

```bash
# 部署到预发布环境
npm run deploy:staging

# 运行烟雾测试
npm run test:smoke -- --env=staging

# 邀请团队测试
```

---

### Step 5: 创建发布

**创建 Git Tag：**

```bash
# 创建带注释的 tag
git tag -a v1.2.0 -m "Release version 1.2.0"

# 推送 tag 到远程
git push origin v1.2.0

# 推送所有 tags
git push origin --tags
```

**创建 GitHub Release：**

```bash
# 使用 GitHub CLI
gh release create v1.2.0 \
  --title "v1.2.0" \
  --notes-file CHANGELOG.md \
  --draft

# 或手动在 GitHub 上创建
```

**Release Notes 模板：**

```markdown
## What's New in v1.2.0

### ✨ New Features
- User authentication system
- Data export functionality
- Email notifications

### 🐛 Bug Fixes
- Fixed login page styling issues
- Fixed encoding issues in data export
- Fixed data consistency issues under concurrent access

### 📈 Improvements
- Optimized database query performance
- Improved error messages
- Updated dependencies

### 📚 Documentation
- Added API documentation
- Updated user guide
- Added migration guide

### ⚠️ Breaking Changes
None

### 🔒 Security
- Fixed SQL injection vulnerability
- Updated vulnerable dependencies

## Installation

```bash
npm install myapp@1.2.0
```

## Upgrade Guide

See [UPGRADE.md](UPGRADE.md) for detailed upgrade instructions.

## Contributors

Thanks to all contributors who made this release possible!

- @user1
- @user2
- @user3
```

---

### Step 6: 部署发布

**部署到生产环境：**

参考 **deployment workflow**

```bash
# 使用 deployment workflow
# 确保所有检查通过后部署
```

**发布到包管理器：**

```bash
# npm
npm publish

# Docker
docker build -t myapp:v1.2.0 .
docker push registry.example.com/myapp:v1.2.0
docker tag myapp:v1.2.0 registry.example.com/myapp:latest
docker push registry.example.com/myapp:latest
```

---

### Step 7: 发布通知

**通知渠道：**

1. **内部通知**
   - 团队聊天工具（Slack, 企业微信）
   - 邮件列表

2. **外部通知**
   - 官网公告
   - 博客文章
   - 社交媒体
   - 用户邮件

**通知模板：**

```markdown
📢 v1.2.0 已发布！

我们很高兴地宣布 MyApp v1.2.0 正式发布！

🎉 主要更新：
• 新增用户认证系统
• 新增数据导出功能
• 性能优化 50%

📦 立即更新：
npm install myapp@1.2.0

📖 完整更新日志：
https://github.com/myorg/myapp/releases/tag/v1.2.0

感谢所有贡献者和用户的支持！
```

---

### Step 8: 监控反馈

**监控指标：**

- [ ] 部署成功率
- [ ] 错误率
- [ ] 性能指标
- [ ] 用户反馈

**收集反馈：**

- 监控错误报告
- 查看用户反馈
- 跟踪社交媒体讨论
- 分析使用数据

**问题处理：**

如果发现严重问题：
1. 评估影响范围
2. 决定是否回滚
3. 准备热修复
4. 尽快发布 Patch 版本

---

## 发布类型

### Major Release (1.0.0 → 2.0.0)

**何时使用：**
- 破坏性变更
- 重大架构调整
- API 不兼容变更

**注意事项：**
- 提前通知用户（至少 1 个月）
- 提供迁移指南
- 保留旧版本维护一段时间
- 提供自动化迁移工具（如可能）

---

### Minor Release (1.0.0 → 1.1.0)

**何时使用：**
- 新功能添加
- 向后兼容的改进

**注意事项：**
- 确保向后兼容
- 充分测试
- 更新文档

---

### Patch Release (1.0.0 → 1.0.1)

**何时使用：**
- Bug 修复
- 小的改进
- 安全修复

**注意事项：**
- 快速发布
- 专注于修复
- 最小化变更

---

### Hotfix Release

**紧急修复流程：**

```
发现严重 Bug
    ↓
从 main 创建 hotfix 分支
    ↓
修复并测试
    ↓
快速发布 Patch 版本
    ↓
合并回 main 和 develop
```

**示例：**

```bash
# 创建 hotfix 分支
git checkout -b hotfix/v1.0.1 v1.0.0

# 修复问题
# ...

# 提交修改
git commit -m "fix: critical security issue"

# 更新版本
npm version patch

# 合并到 main
git checkout main
git merge hotfix/v1.0.1

# 合并到 develop
git checkout develop
git merge hotfix/v1.0.1

# 推送
git push origin main develop --tags

# 立即发布
npm publish
```

---

## 发布清单

### 发布前

- [ ] 所有功能已完成
- [ ] 所有测试通过
- [ ] 代码审查完成
- [ ] 文档已更新
- [ ] 版本号已更新
- [ ] CHANGELOG 已编写
- [ ] 依赖已更新和审计
- [ ] 预发布测试完成

### 发布中

- [ ] Git tag 已创建
- [ ] GitHub Release 已创建
- [ ] 包已发布
- [ ] 部署已完成
- [ ] 烟雾测试通过

### 发布后

- [ ] 通知已发送
- [ ] 监控正常
- [ ] 文档网站已更新
- [ ] 反馈已收集
- [ ] 下一版本已规划

---

## 回滚策略

**何时回滚：**
- 发现严重 Bug
- 性能严重下降
- 安全漏洞
- 大量用户报错

**回滚步骤：**

```bash
# Kubernetes
kubectl rollout undo deployment/myapp -n production

# npm（发布新的 Patch 版本）
# 不能撤销已发布的 npm 包，只能发布新版本
npm version patch
npm publish

# Docker
# 回滚到之前的镜像
kubectl set image deployment/myapp \
  myapp=registry.example.com/myapp:v1.1.0 \
  -n production
```

---

## 自动化发布

### GitHub Actions

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          registry-url: 'https://registry.npmjs.org'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
      
      - name: Build
        run: npm run build
      
      - name: Publish to npm
        run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
      
      - name: Create GitHub Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          body_path: CHANGELOG.md
          draft: false
          prerelease: false
      
      - name: Deploy to production
        run: |
          kubectl set image deployment/myapp \
            myapp=registry.example.com/myapp:${GITHUB_REF_NAME} \
            -n production
```

---

## 最佳实践

### 1. 定期发布

- 建立定期发布节奏（如每 2 周）
- 避免发布太大的版本

### 2. 向后兼容

- 尽可能保持向后兼容
- 废弃而不是删除（先标记 deprecated）

### 3. 充分测试

- 自动化测试覆盖
- 预发布环境验证

### 4. 清晰沟通

- 详细的 Release Notes
- 及时通知用户

### 5. 快速反馈

- 监控发布后的指标
- 快速响应问题

---

## 相关 Skills

- **testing** - 最终回归
- **security** - 发布前安全检查
- **performance** - 性能基线对比
- **devops** - CI/CD 与部署
- **deployment workflow** - 部署流程
- **changelog template** - 变更日志模板

---

## 版本历史

- **v1.0.0** - 2026-07-19 - 初始版本

---
