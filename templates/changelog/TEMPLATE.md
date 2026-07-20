# Changelog Template

标准的变更日志模板，遵循 [Keep a Changelog](https://keepachangelog.com/) 规范。


---


# Changelog


All notable changes to this project will be documented in this file.


The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),

and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---


## [Unreleased]


### Added

- 待发布的新功能

### Changed

- 待发布的功能变更

### Fixed

- 待发布的 Bug 修复

---


## [1.2.0] - 2026-07-19


### Added

- 新增用户认证系统，支持 JWT token
- 新增数据导出功能，支持 CSV 和 JSON 格式
- 新增邮件通知功能
- 新增多语言支持（中文、英文）
- 新增暗黑模式

### Changed

- 优化数据库查询性能，响应时间减少 50%
- 改进错误提示信息，更加用户友好
- 更新依赖包到最新版本
- 重构用户界面，提升用户体验
- 调整 API 响应格式，更符合 REST 规范

### Deprecated

- `oldApi()` 函数标记为废弃，将在 v2.0.0 中移除，请使用 `newApi()` 替代
- `/api/v1/legacy` 端点将在下个主版本中移除

### Removed

- 移除了已废弃的 `deprecatedFunction()`
- 移除了不再使用的旧 UI 组件
- 删除了过时的依赖包

### Fixed

- 修复登录页面在移动端的样式问题 (#123)
- 修复数据导出时中文乱码的问题 (#124)
- 修复并发访问时的数据不一致问题 (#125)
- 修复内存泄漏问题
- 修复时区显示错误

### Security

- 修复了 SQL 注入漏洞 (CVE-2026-12345)
- 更新了有安全漏洞的依赖包
- 增强了密码加密强度
- 修复了 XSS 漏洞

---


## [1.1.0] - 2026-06-15


### Added

- 新增搜索功能
- 新增用户头像上传
- 新增数据统计图表

### Changed

- 优化首页加载速度
- 改进搜索算法

### Fixed

- 修复分页显示错误 (#120)
- 修复上传文件大小限制问题 (#121)

---


## [1.0.1] - 2026-05-20


### Fixed

- 修复生产环境配置错误 (#118)
- 修复缓存失效问题 (#119)

### Security

- 更新依赖包修复安全漏洞

---


## [1.0.0] - 2026-05-01


### Added

- 初始版本发布
- 用户注册和登录功能
- 基本的 CRUD 操作
- 用户权限管理
- RESTful API
- 响应式用户界面

---


## 类别说明


### Added

新增的功能。

**示例：**

- 新增用户认证功能
- 新增数据导出功能
- 新增 API 端点 `/api/users`

---


### Changed

已有功能的变更。

**示例：**

- 优化数据库查询性能
- 改进用户界面
- 更新依赖包

---


### Deprecated

即将废弃的功能，但当前版本仍可用。

**示例：**

- `oldFunction()` 将在 v2.0.0 中移除
- 旧的 API 端点将在下个主版本中移除

---


### Removed

已删除的功能。

**示例：**

- 移除了已废弃的 `oldFunction()`
- 删除了不再使用的配置项

---


### Fixed

Bug 修复。

**示例：**

- 修复登录页面样式问题
- 修复数据导出乱码问题
- 修复内存泄漏

---


### Security

安全相关的修复。

**示例：**

- 修复 SQL 注入漏洞
- 更新有安全漏洞的依赖包
- 修复 XSS 漏洞

---


## 版本号格式


遵循语义化版本规范：`MAJOR.MINOR.PATCH`


- **MAJOR**: 不兼容的 API 变更

- **MINOR**: 向后兼容的功能新增
- **PATCH**: 向后兼容的问题修复

**示例：**

- `1.0.0` → `2.0.0`: 主版本（破坏性变更）
- `1.0.0` → `1.1.0`: 次版本（新功能）
- `1.0.0` → `1.0.1`: 补丁版本（Bug 修复）

---


## 日期格式


使用 ISO 8601 格式：`YYYY-MM-DD`


**示例：** `2026-07-19`


---


## Issue 引用


使用 GitHub Issue 编号引用相关问题。


**示例：**

- 修复登录问题 (#123)
- 实现新功能 (#124)
- 关闭 #125

---


## 链接


在文档底部添加版本对比链接。


```markdown

[Unreleased]: https://github.com/user/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/user/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/user/repo/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/user/repo/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/user/repo/releases/tag/v1.0.0
```

---


## 自动化生成


可以使用工具自动生成变更日志：


### conventional-changelog


```bash

npm install -g conventional-changelog-cli

# 生成变更日志

conventional-changelog -p angular -i CHANGELOG.md -s
```

### auto-changelog


```bash

npm install -g auto-changelog

# 生成变更日志

auto-changelog
```

### GitHub Release Notes


GitHub 可以自动生成 Release Notes：


1. 创建新 Release

2. 点击 "Auto-generate release notes"
3. GitHub 会基于 PR 和 commits 生成

---


## 最佳实践


### 1. 及时更新


每次发布新版本时更新变更日志。


### 2. 用户视角


从用户视角描述变更，而不是技术细节。


✅ 正确：

```markdown
- 修复登录页面在手机上显示不正常的问题
```

❌ 错误：

```markdown
- 修复 LoginComponent 的 CSS flex 布局问题
```

### 3. 分组清晰


使用标准的类别（Added, Changed, Fixed 等）。


### 4. 引用 Issue


对于重要的变更，引用相关的 GitHub Issue。


### 5. 破坏性变更


对于破坏性变更，使用明显的标记：


```markdown

### Changed
- **BREAKING:** API 响应格式已变更，从 `{ data: ... }` 改为 `{ result: ... }`
```

### 6. 安全问题


安全修复应该有专门的 Security 类别。


---


## 模板示例


### 空白模板


```markdown

## [版本号] - YYYY-MM-DD

### Added

- 

### Changed

- 

### Deprecated

- 

### Removed

- 

### Fixed

- 

### Security

- 
```

### 快速记录模板


```markdown

## [Unreleased]

- [ ] #123 - 新增功能 A

- [ ] #124 - 修复 Bug B
- [ ] #125 - 优化性能 C
```

发布时整理为标准格式。


---


## 工具集成


### package.json scripts


```json

{
  "scripts": {
    "changelog": "conventional-changelog -p angular -i CHANGELOG.md -s",
    "version": "npm run changelog && git add CHANGELOG.md"
  }
}
```

### Git Hooks


使用 husky 在版本升级时自动更新：


```bash

npm install --save-dev husky

# package.json

{
  "husky": {
    "hooks": {
      "post-version": "npm run changelog && git add CHANGELOG.md"
    }
  }
}
```

---


## 参考资源


- [Keep a Changelog](https://keepachangelog.com/)

- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [conventional-changelog](https://github.com/conventional-changelog/conventional-changelog)

---


## 版本历史


- **v1.0.0** - 2026-07-19 - 初始模板


---
