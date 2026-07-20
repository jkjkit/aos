# Contributing Guide

感谢你考虑为本项目做贡献！


---


## 目录


- [行为准则](#行为准则)

- [如何贡献](#如何贡献)
- [开发流程](#开发流程)
- [提交规范](#提交规范)
- [代码规范](#代码规范)
- [测试要求](#测试要求)
- [文档要求](#文档要求)
- [Pull Request 流程](#pull-request-流程)
- [Issue 指南](#issue-指南)

---


## 行为准则


本项目遵循 [Contributor Covenant](https://www.contributor-covenant.org/) 行为准则。参与本项目即表示你同意遵守其条款。


### 我们的承诺


为了营造开放和友好的环境，我们承诺：


- 使用友好和包容的语言

- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

---


## 如何贡献


有很多方式可以为项目做贡献：


### 报告 Bug


发现 Bug？请通过 [GitHub Issues](https://github.com/username/repo/issues/new?template=bug_report.md) 报告。


提交 Bug 报告时，请包含：

- 清晰的标题和描述
- 详细的重现步骤
- 预期行为和实际行为
- 环境信息（版本、操作系统等）
- 截图或错误日志（如适用）

### 提出功能建议


有新想法？请通过 [GitHub Issues](https://github.com/username/repo/issues/new?template=feature_request.md) 提出。


提交功能建议时，请包含：

- 功能的详细描述
- 为什么需要这个功能
- 可能的实现方案
- 是否愿意实现这个功能

### 改进文档


文档改进永远欢迎：

- 修正错别字
- 补充缺失的文档
- 改进示例代码
- 翻译文档

### 提交代码


准备好贡献代码？请遵循以下流程。


---


## 开发流程


### 1. Fork 仓库


点击 GitHub 页面右上角的 "Fork" 按钮。


### 2. 克隆你的 Fork


```bash

git clone https://github.com/YOUR_USERNAME/repo.git
cd repo
```

### 3. 添加上游仓库


```bash

git remote add upstream https://github.com/original/repo.git
```

### 4. 创建分支


```bash

git checkout -b feature/your-feature-name
```

**分支命名规范：**

- `feature/xxx` - 新功能
- `fix/xxx` - Bug 修复
- `docs/xxx` - 文档更新
- `refactor/xxx` - 代码重构
- `test/xxx` - 测试相关

### 5. 安装依赖


```bash

npm install
```

### 6. 进行开发


编写代码、测试、文档...


### 7. 保持同步


定期同步上游仓库的变更：


```bash

git fetch upstream
git rebase upstream/main
```

### 8. 提交变更


```bash

git add .
git commit -m "feat: add new feature"
```

### 9. 推送到 Fork


```bash

git push origin feature/your-feature-name
```

### 10. 创建 Pull Request


在 GitHub 上创建 Pull Request。


---


## 提交规范


我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范。


### 提交消息格式


```

<type>(<scope>): <subject>

<body>


<footer>

```

### Type 类型


| Type | 描述 |

|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档变更 |
| `style` | 代码格式（不影响代码运行） |
| `refactor` | 重构（既不是新功能也不是 Bug 修复） |
| `perf` | 性能优化 |
| `test` | 测试相关 |
| `build` | 构建系统或外部依赖变更 |
| `ci` | CI 配置文件和脚本变更 |
| `chore` | 其他不修改 src 或 test 的变更 |
| `revert` | 回滚之前的提交 |

### 示例


**简单示例：**

```
feat: add user authentication
```

**完整示例：**

```
feat(auth): add JWT token support

- Implement JWT token generation

- Add token verification middleware
- Update authentication tests

Closes #123

```

**破坏性变更：**

```
feat!: change API response format

BREAKING CHANGE: The API response format has changed from

{ data: ... } to { result: ... }
```

---


## 代码规范


### JavaScript/TypeScript


我们使用 ESLint 和 Prettier 进行代码检查和格式化。


**运行检查：**


```bash

npm run lint
```

**自动修复：**


```bash

npm run lint:fix
npm run format
```

### 编码风格


- 使用 2 空格缩进

- 使用单引号
- 行尾不加分号
- 最大行长度 100 字符
- 使用驼峰命名法
- 常量使用大写下划线命名

**示例：**


```javascript

// ✅ 正确
const userName = 'John'
const MAX_RETRY_COUNT = 3

function getUserById(id) {

  return users.find(user => user.id === id)
}

// ❌ 错误

const user_name = "John";
const maxRetryCount = 3;

function get_user_by_id(id) {

  return users.find(user => user.id === id);
}
```

---


## 测试要求


所有代码变更必须包含测试。


### 运行测试


```bash

# 运行所有测试
npm test

# 运行特定测试

npm test -- path/to/test

# 测试覆盖率

npm run test:coverage
```

### 测试要求


- 新功能必须有单元测试

- Bug 修复必须有回归测试
- 测试覆盖率不能降低
- 所有测试必须通过

### 编写测试


**示例：**


```javascript

describe('User', () => {
  describe('create', () => {
    it('should create a new user', async () => {
      const user = await User.create({
        email: 'test@example.com',
        password: 'password123'
      })
      
      expect(user).toBeDefined()
      expect(user.email).toBe('test@example.com')
    })
    
    it('should throw error for duplicate email', async () => {
      await User.create({ email: 'test@example.com', password: 'pass' })
      
      await expect(
        User.create({ email: 'test@example.com', password: 'pass' })
      ).rejects.toThrow('Email already exists')
    })
  })
})
```

---


## 文档要求


### 代码注释


为复杂逻辑添加注释：


```javascript

/**
 * Calculate the total price including tax and discount
 * @param {number} price - The base price
 * @param {number} taxRate - Tax rate (e.g., 0.1 for 10%)
 * @param {number} discount - Discount amount
 * @returns {number} The final price
 */
function calculateTotal(price, taxRate, discount) {
  // Apply discount first
  const discountedPrice = price - discount
  
  // Then calculate tax
  const tax = discountedPrice * taxRate
  
  return discountedPrice + tax
}
```

### API 文档


为公共 API 添加 JSDoc：


```javascript

/**
 * User class representing a user entity
 */
class User {
  /**
   * Create a new user
   * @param {Object} data - User data
   * @param {string} data.email - User email
   * @param {string} data.password - User password
   * @returns {Promise<User>} The created user
   */
  static async create(data) {
    // ...
  }
}
```

### README 更新


如果你的变更影响到用户使用方式，请更新 README.md。


---


## Pull Request 流程


### PR 标题


使用与 commit message 相同的格式：


```

feat: add user authentication
```

### PR 描述


使用 PR 模板，包含：


```markdown

## 描述
[简要描述这个 PR 的目的]

## 变更类型

- [ ] Bug 修复
- [ ] 新功能
- [ ] 破坏性变更
- [ ] 文档更新

## 相关 Issue

Closes #123

## 变更内容

- 添加了 X 功能
- 修复了 Y 问题
- 重构了 Z 模块

## 测试

- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 手动测试通过

## 截图（如适用）


## 检查清单

- [ ] 代码遵循项目规范
- [ ] 添加了测试
- [ ] 更新了文档
- [ ] 自我审查完成
```

### 审查流程


1. **自动检查**

   - CI/CD 必须通过
   - 代码覆盖率不能降低
   - 没有 lint 错误

2. **人工审查**

   - 至少 1 个维护者批准
   - 所有评论已解决

3. **合并**

   - 使用 "Squash and merge"
   - 维护者会合并你的 PR

### 审查时间


我们会在 48 小时内审查你的 PR。


---


## Issue 指南


### 提交 Bug


使用 Bug 报告模板：


```markdown

**描述 Bug**
简短清晰地描述 Bug

**重现步骤**

1. 访问 '...'
2. 点击 '....'
3. 滚动到 '....'
4. 看到错误

**预期行为**

清晰描述预期发生什么

**截图**

如适用，添加截图

**环境**

 - OS: [e.g. macOS]
 - Browser [e.g. chrome, safari]
 - Version [e.g. 22]

**其他上下文**

任何其他相关信息
```

### 请求功能


使用功能请求模板：


```markdown

**功能与问题相关吗？**
清晰简洁地描述问题

**描述你想要的解决方案**

清晰简洁地描述你想要什么

**描述你考虑过的替代方案**

清晰简洁地描述任何替代解决方案

**其他上下文**

任何其他相关信息
```

---


## 获取帮助


需要帮助？


- 📖 查看[文档](https://docs.example.com)

- 💬 加入 [Discussions](https://github.com/username/repo/discussions)
- 💌 发送邮件到 maintainers@example.com

---


## 认可贡献者


我们认可所有贡献者的努力：


- 贡献者会出现在 README 中

- 重大贡献会在 Release Notes 中特别感谢

---


## 许可证


通过贡献，你同意你的贡献将以与本项目相同的许可证（MIT）发布。


---


**感谢你的贡献！🎉**


---
