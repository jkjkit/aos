# 项目文档 - Todo App

**使用 Skill:** `document`

**输入:** [09-monitoring.md](09-monitoring.md)

**输出:** README + API 文档 + 用户指南

---

## 1. README.md

```markdown
# Todo App

简洁高效的任务管理 Web 应用。

## 特性

- 任务的增删改查
- 任务分类与优先级
- 截止日期与提醒
- 多端同步（Web / iOS / Android）
- 暗色模式

## 技术栈

- 前端：React 18 + TypeScript + Vite + Tailwind CSS
- 后端：Node.js + Express + TypeScript
- 数据库：MongoDB + Redis
- 鉴权：JWT + bcrypt

## 快速开始

### 本地开发

```bash
# 启动 MongoDB 与 Redis
docker compose up -d mongo redis

# 后端
cd backend
pnpm install
pnpm dev

# 前端
cd frontend
pnpm install
pnpm dev
```

访问 http://localhost:5173

### Docker 部署

```bash
docker compose up -d
```

访问 http://localhost:4000

## 文档

- [架构设计](docs/design.md)
- [API 文档](docs/api.md)
- [部署指南](docs/deployment.md)
- [贡献指南](CONTRIBUTING.md)
- [更新日志](CHANGELOG.md)

## License

MIT
```

## 2. API 文档（核心端点示例）

### POST /api/auth/register

**描述：** 注册新用户

**鉴权：** 无

**请求：**

```json
{
  "email": "user@example.com",
  "password": "Pass123!",
  "username": "myhandle"
}
```

**响应 200：**

```json
{
  "success": true,
  "data": {
    "user": {
      "id": "u_abc123",
      "email": "user@example.com",
      "username": "myhandle"
    },
    "accessToken": "eyJ...",
    "refreshToken": "eyJ..."
  }
}
```

**错误：**

| Code | HTTP | 含义 |
|------|------|------|
| EMAIL_ALREADY_EXISTS | 409 | 邮箱已注册 |
| PASSWORD_TOO_WEAK | 400 | 密码强度不足 |
| INVALID_INPUT | 400 | 参数校验失败 |

### POST /api/tasks

**描述：** 创建任务

**鉴权：** Bearer Token（必须登录）

**请求：**

```json
{
  "title": "买菜",
  "description": "番茄、鸡蛋",
  "priority": "high",
  "dueDate": "2026-07-21T18:00:00Z",
  "categoryId": "c_xyz"
}
```

**响应 200：**

```json
{
  "success": true,
  "data": {
    "id": "t_123",
    "title": "买菜",
    "status": "pending",
    "priority": "high",
    "userId": "u_abc123",
    "createdAt": "2026-07-20T14:30:00Z"
  }
}
```

### GET /api/tasks

**描述：** 获取任务列表

**鉴权：** Bearer Token

**Query 参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认 1 |
| limit | int | 否 | 每页数量，默认 20，最大 100 |
| status | string | 否 | pending / in-progress / completed |
| categoryId | string | 否 | 按分类筛选 |

**响应 200：**

```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
```

## 3. 用户指南（关键流程）

### 注册与登录

1. 访问首页，点击「注册」
2. 输入邮箱、用户名、密码
3. 收到验证邮件（开发环境自动通过）
4. 登录后进入任务列表

### 创建第一个任务

1. 在任务列表点击「+」
2. 输入标题、选择分类、设置优先级
3. 可选：设置截止日期与提醒
4. 点击保存

### 完成任务

- 列表视图：勾选复选框
- 详情视图：点击「标记完成」按钮

## 4. 常见问题

**Q: 数据会丢失吗？**

不会。所有数据持久化在 MongoDB，每 5 分钟增量备份到对象存储。

**Q: 忘记密码怎么办？**

点击登录页「忘记密码」链接，输入邮箱，会收到重置链接。

**Q: 是否支持多端同步？**

支持。所有设备登录同一账号即可看到最新数据。

## 5. 故障排查

| 现象 | 可能原因 | 解决 |
|------|----------|------|
| 登录失败 | 密码错误 / Token 过期 | 重新登录 |
| 任务列表加载慢 | MongoDB 索引缺失 | 通知运维（参考 runbook） |
| 推送通知不到达 | 浏览器权限未授予 | 检查浏览器设置 |

## 下一步

进入 [11-release.md](11-release.md) — 由 `release` workflow 完成版本发布。