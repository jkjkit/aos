# 架构设计 - Todo App

**使用 Skill:** design

**创建时间:** 2026-07-19

**架构师:** AOS Team

---

## 1. 设计概述

基于需求分析和技术研究，设计 Todo App 的系统架构。

**参考文档：**
- [01-requirement.md](01-requirement.md) - 需求分析
- [02-tasks.md](02-tasks.md) - 任务分解
- [03-research.md](03-research.md) - 技术研究

---

## 2. 系统架构

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                         用户界面层                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  React App (SPA)                                     │   │
│  │  - React 18 + TypeScript                            │   │
│  │  - Tailwind CSS + Headless UI                       │   │
│  │  - Zustand (State Management)                       │   │
│  │  - React Query (Data Fetching)                      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ↓ HTTP/HTTPS
┌─────────────────────────────────────────────────────────────┐
│                         API 网关层                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Nginx (Reverse Proxy)                              │   │
│  │  - 负载均衡                                          │   │
│  │  - SSL 终止                                          │   │
│  │  - 静态文件服务                                       │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                       应用服务层                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Node.js API Server (Express)                       │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐    │   │
│  │  │   Auth     │  │   Tasks    │  │  Categories│    │   │
│  │  │  Service   │  │  Service   │  │   Service  │    │   │
│  │  └────────────┘  └────────────┘  └────────────┘    │   │
│  │  ┌────────────┐  ┌────────────┐                    │   │
│  │  │   Users    │  │Notifications│                    │   │
│  │  │  Service   │  │   Service   │                    │   │
│  │  └────────────┘  └────────────┘                    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        数据持久层                            │
│  ┌────────────────────┐         ┌────────────────────┐      │
│  │   MongoDB 6+       │         │   Redis            │      │
│  │   - 主数据存储      │         │   - 会话管理        │      │
│  │   - 副本集          │         │   - 缓存            │      │
│  │   - 索引优化        │         │   - 限流            │      │
│  └────────────────────┘         └────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

### 2.2 架构特点

**优点：**
- ✅ **前后端分离** - 独立开发和部署
- ✅ **无状态设计** - 易于水平扩展
- ✅ **分层清晰** - 职责明确，易维护
- ✅ **可扩展** - 支持微服务演进
- ✅ **高性能** - 多层缓存策略

**技术选型依据：**
- 基于 [03-research.md](03-research.md) 的技术研究结果
- React + Express + MongoDB 的经典组合
- 成熟稳定、生态丰富、易于招聘

---

## 3. 前端架构

### 3.1 目录结构

```
frontend/
├── src/
│   ├── components/          # 组件
│   │   ├── common/          # 通用组件
│   │   │   ├── Button/
│   │   │   ├── Input/
│   │   │   ├── Modal/
│   │   │   └── ...
│   │   ├── layout/          # 布局组件
│   │   │   ├── Header/
│   │   │   ├── Sidebar/
│   │   │   └── Footer/
│   │   └── features/        # 功能组件
│   │       ├── auth/
│   │       ├── tasks/
│   │       ├── categories/
│   │       └── notifications/
│   │
│   ├── pages/               # 页面
│   │   ├── Home/
│   │   ├── Login/
│   │   ├── Register/
│   │   ├── Tasks/
│   │   └── Settings/
│   │
│   ├── hooks/               # 自定义 Hooks
│   │   ├── useAuth.ts
│   │   ├── useTasks.ts
│   │   └── useCategories.ts
│   │
│   ├── store/               # 状态管理 (Zustand)
│   │   ├── authStore.ts
│   │   ├── taskStore.ts
│   │   └── uiStore.ts
│   │
│   ├── services/            # API 服务
│   │   ├── api.ts           # API 客户端配置
│   │   ├── auth.service.ts
│   │   ├── task.service.ts
│   │   └── category.service.ts
│   │
│   ├── utils/               # 工具函数
│   │   ├── format.ts
│   │   ├── validation.ts
│   │   └── helpers.ts
│   │
│   ├── types/               # TypeScript 类型定义
│   │   ├── task.types.ts
│   │   ├── user.types.ts
│   │   └── api.types.ts
│   │
│   ├── constants/           # 常量
│   │   └── index.ts
│   │
│   ├── App.tsx
│   └── main.tsx
│
├── public/
├── tests/
│   ├── unit/
│   └── e2e/
├── vite.config.ts
├── tailwind.config.js
├── tsconfig.json
└── package.json
```

---

### 3.2 组件设计原则

**Atomic Design 方法论：**

```
Atoms (原子)
  └─> Button, Input, Label, Icon

Molecules (分子)
  └─> FormField, SearchBar, TaskItem

Organisms (组织)
  └─> TaskList, LoginForm, Header

Templates (模板)
  └─> TaskPage, AuthPage

Pages (页面)
  └─> HomePage, TasksPage
```

---

### 3.3 状态管理策略

**分层状态管理：**

1. **服务端状态 (React Query)**
   - 任务列表
   - 用户信息
   - 分类数据

2. **全局状态 (Zustand)**
   - 认证状态
   - UI 状态（侧边栏、模态框）
   - 主题设置

3. **本地状态 (useState)**
   - 表单输入
   - 临时 UI 状态

```typescript
// 示例：Zustand Store
interface AuthStore {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
}

const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  
  login: async (email, password) => {
    const { user, token } = await authService.login(email, password);
    set({ user, token, isAuthenticated: true });
  },
  
  logout: () => {
    set({ user: null, token: null, isAuthenticated: false });
  },
  
  refreshToken: async () => {
    const { token } = await authService.refreshToken();
    set({ token });
  },
}));
```

---

### 3.4 路由设计

```typescript
// React Router 配置
const routes = [
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'tasks', element: <TasksPage /> },
      { path: 'tasks/:id', element: <TaskDetailPage /> },
      { path: 'categories', element: <CategoriesPage /> },
      { path: 'settings', element: <SettingsPage /> },
    ],
  },
  {
    path: '/auth',
    element: <AuthLayout />,
    children: [
      { path: 'login', element: <LoginPage /> },
      { path: 'register', element: <RegisterPage /> },
    ],
  },
  { path: '*', element: <NotFoundPage /> },
];
```

---

## 4. 后端架构

### 4.1 目录结构

```
backend/
├── src/
│   ├── config/              # 配置
│   │   ├── database.ts
│   │   ├── redis.ts
│   │   └── env.ts
│   │
│   ├── controllers/         # 控制器
│   │   ├── auth.controller.ts
│   │   ├── task.controller.ts
│   │   ├── category.controller.ts
│   │   └── user.controller.ts
│   │
│   ├── services/            # 业务逻辑
│   │   ├── auth.service.ts
│   │   ├── task.service.ts
│   │   ├── category.service.ts
│   │   ├── user.service.ts
│   │   └── notification.service.ts
│   │
│   ├── models/              # 数据模型 (Mongoose)
│   │   ├── User.model.ts
│   │   ├── Task.model.ts
│   │   └── Category.model.ts
│   │
│   ├── middleware/          # 中间件
│   │   ├── auth.middleware.ts
│   │   ├── validation.middleware.ts
│   │   ├── error.middleware.ts
│   │   └── rateLimit.middleware.ts
│   │
│   ├── routes/              # 路由
│   │   ├── auth.routes.ts
│   │   ├── task.routes.ts
│   │   ├── category.routes.ts
│   │   └── user.routes.ts
│   │
│   ├── utils/               # 工具函数
│   │   ├── jwt.util.ts
│   │   ├── password.util.ts
│   │   ├── validator.util.ts
│   │   └── logger.util.ts
│   │
│   ├── types/               # TypeScript 类型
│   │   ├── express.d.ts
│   │   └── models.types.ts
│   │
│   ├── jobs/                # 定时任务
│   │   └── notification.job.ts
│   │
│   ├── app.ts               # Express 应用
│   └── server.ts            # 服务器入口
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── .env.example
├── tsconfig.json
└── package.json
```

---

### 4.2 分层架构

```
Routes (路由)
  ↓ HTTP Request
Controllers (控制器) - 处理请求和响应
  ↓ 调用服务
Services (服务) - 业务逻辑
  ↓ 数据操作
Models (模型) - 数据访问层
  ↓ 数据库操作
Database (数据库)
```

**职责划分：**

| 层级 | 职责 | 示例 |
|------|------|------|
| Routes | 定义 API 端点 | `POST /api/tasks` |
| Controllers | 请求验证、响应格式化 | 验证请求参数 |
| Services | 业务逻辑 | 创建任务、权限检查 |
| Models | 数据定义、CRUD | Mongoose Schema |

---

### 4.3 API 设计

**RESTful API 规范：**

```typescript
// 任务 API
GET    /api/tasks              # 获取任务列表
GET    /api/tasks/:id          # 获取任务详情
POST   /api/tasks              # 创建任务
PUT    /api/tasks/:id          # 更新任务
DELETE /api/tasks/:id          # 删除任务
PATCH  /api/tasks/:id/complete # 完成任务

// 分类 API
GET    /api/categories         # 获取分类列表
POST   /api/categories         # 创建分类
PUT    /api/categories/:id     # 更新分类
DELETE /api/categories/:id     # 删除分类

// 用户 API
GET    /api/users/me           # 获取当前用户
PUT    /api/users/me           # 更新用户信息
PUT    /api/users/me/password  # 修改密码

// 认证 API
POST   /api/auth/register      # 注册
POST   /api/auth/login         # 登录
POST   /api/auth/logout        # 登出
POST   /api/auth/refresh       # 刷新 Token
```

**响应格式：**

```typescript
// 成功响应
{
  "success": true,
  "data": { ... },
  "message": "操作成功"
}

// 错误响应
{
  "success": false,
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "任务不存在"
  }
}

// 分页响应
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

---

### 4.4 中间件设计

**中间件链：**

```typescript
// 请求处理流程
Request
  ↓
CORS 中间件
  ↓
日志中间件
  ↓
限流中间件
  ↓
认证中间件 (可选)
  ↓
验证中间件 (可选)
  ↓
路由处理器
  ↓
错误中间件
  ↓
Response
```

**示例：认证中间件**

```typescript
export const authenticate = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  try {
    const token = req.headers.authorization?.split(' ')[1];
    
    if (!token) {
      throw new UnauthorizedError('未提供认证令牌');
    }
    
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = await User.findById(decoded.userId);
    
    if (!req.user) {
      throw new UnauthorizedError('用户不存在');
    }
    
    next();
  } catch (error) {
    next(error);
  }
};
```

---

## 5. 数据库设计

### 5.1 数据模型

**User (用户)**

```typescript
interface IUser {
  _id: ObjectId;
  email: string;           // 唯一，索引
  password: string;        // bcrypt 哈希
  username: string;
  avatar?: string;
  createdAt: Date;
  updatedAt: Date;
}
```

**Task (任务)**

```typescript
interface ITask {
  _id: ObjectId;
  title: string;           // 必填
  description?: string;
  status: 'pending' | 'in-progress' | 'completed';
  priority: 'low' | 'medium' | 'high';
  dueDate?: Date;          // 索引
  reminder?: Date;
  categoryId?: ObjectId;   // 外键，索引
  userId: ObjectId;        // 外键，索引
  tags: string[];
  createdAt: Date;
  updatedAt: Date;
  completedAt?: Date;
}
```

**Category (分类)**

```typescript
interface ICategory {
  _id: ObjectId;
  name: string;            // 必填
  color: string;           // 十六进制颜色
  icon?: string;
  userId: ObjectId;        // 外键，索引
  createdAt: Date;
  updatedAt: Date;
}
```

---

### 5.2 索引设计

```typescript
// User 索引
User.index({ email: 1 }, { unique: true });

// Task 索引
Task.index({ userId: 1, createdAt: -1 });
Task.index({ userId: 1, status: 1 });
Task.index({ userId: 1, dueDate: 1 });
Task.index({ categoryId: 1 });

// 复合索引
Task.index({ userId: 1, status: 1, dueDate: 1 });

// Category 索引
Category.index({ userId: 1 });
```

---

### 5.3 数据关系

```
User (1) ──── (N) Task
User (1) ──── (N) Category
Category (1) ──── (N) Task
```

---

## 6. 安全设计

### 6.1 认证流程

```
1. 用户注册
   ├─> 验证邮箱格式
   ├─> 验证密码强度
   ├─> 密码 bcrypt 加密
   └─> 保存到数据库

2. 用户登录
   ├─> 验证邮箱和密码
   ├─> 生成 Access Token (15分钟)
   ├─> 生成 Refresh Token (7天)
   └─> 返回 Token Pair

3. API 请求
   ├─> 验证 Access Token
   ├─> Token 有效 → 处理请求
   └─> Token 过期 → 返回 401

4. 刷新 Token
   ├─> 验证 Refresh Token
   ├─> Token 有效 → 生成新 Access Token
   └─> Token 无效 → 要求重新登录
```

---

### 6.2 安全措施

**应用层安全：**

| 措施 | 实现 |
|------|------|
| 密码加密 | bcrypt, salt rounds = 10 |
| JWT 签名 | HS256 算法 |
| HTTPS | TLS 1.3 |
| CORS | 白名单配置 |
| 限流 | express-rate-limit |
| 输入验证 | Joi / Zod |
| SQL 注入防护 | Mongoose (参数化查询) |
| XSS 防护 | helmet.js |

---

### 6.3 权限控制

**权限模型：**

```typescript
// 基于所有权的访问控制
function checkTaskOwnership(taskId: string, userId: string) {
  const task = await Task.findById(taskId);
  
  if (task.userId.toString() !== userId) {
    throw new ForbiddenError('无权访问此任务');
  }
  
  return task;
}
```

---

## 7. 性能优化

### 7.1 缓存策略

**多层缓存：**

```typescript
// 1. 浏览器缓存 (HTTP Cache)
res.setHeader('Cache-Control', 'private, max-age=300');

// 2. Redis 缓存
const cacheKey = `user:${userId}:tasks`;
const cached = await redis.get(cacheKey);

if (cached) {
  return JSON.parse(cached);
}

const tasks = await Task.find({ userId });
await redis.setex(cacheKey, 300, JSON.stringify(tasks));

// 3. 数据库查询优化
Task.find({ userId })
  .select('title status dueDate')  // 字段过滤
  .limit(20)                        // 限制返回数量
  .lean();                          // 返回 Plain Object
```

---

### 7.2 数据库优化

**查询优化：**

```typescript
// ❌ 不好：N+1 查询
const tasks = await Task.find({ userId });
for (const task of tasks) {
  task.category = await Category.findById(task.categoryId);
}

// ✅ 好：使用 populate
const tasks = await Task.find({ userId })
  .populate('categoryId', 'name color');
```

---

### 7.3 分页设计

```typescript
interface PaginationParams {
  page: number;      // 页码，从 1 开始
  limit: number;     // 每页数量，默认 20
}

async function getPaginatedTasks(
  userId: string,
  { page = 1, limit = 20 }: PaginationParams
) {
  const skip = (page - 1) * limit;
  
  const [tasks, total] = await Promise.all([
    Task.find({ userId })
      .skip(skip)
      .limit(limit)
      .sort({ createdAt: -1 }),
    Task.countDocuments({ userId }),
  ]);
  
  return {
    data: tasks,
    pagination: {
      page,
      limit,
      total,
      pages: Math.ceil(total / limit),
    },
  };
}
```

---

## 8. 部署架构

### 8.1 Docker 容器化

**Docker Compose 配置：**

```yaml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    environment:
      - REACT_APP_API_URL=http://backend:4000

  backend:
    build: ./backend
    ports:
      - "4000:4000"
    depends_on:
      - mongodb
      - redis
    environment:
      - MONGODB_URI=mongodb://mongodb:27017/todoapp
      - REDIS_URL=redis://redis:6379
      - JWT_SECRET=${JWT_SECRET}

  mongodb:
    image: mongo:6
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend

volumes:
  mongodb_data:
  redis_data:
```

---

### 8.2 CI/CD 流程

```
Git Push
  ↓
GitHub Actions 触发
  ↓
┌─────────────────┐
│   Build Stage   │
│  - 安装依赖       │
│  - 运行 Lint     │
│  - 运行测试       │
│  - 构建镜像       │
└─────────────────┘
  ↓
┌─────────────────┐
│   Test Stage    │
│  - 单元测试       │
│  - 集成测试       │
│  - E2E 测试      │
└─────────────────┘
  ↓
┌─────────────────┐
│  Deploy Stage   │
│  - 推送镜像       │
│  - 部署到服务器   │
│  - 健康检查       │
└─────────────────┘
```

---

## 9. 监控和日志

### 9.1 日志设计

```typescript
// Winston 日志配置
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
  ],
});

// 日志级别
logger.error('错误信息', { error, userId, taskId });
logger.warn('警告信息', { context });
logger.info('信息日志', { action, userId });
logger.debug('调试信息', { details });
```

---

### 9.2 性能监控

**监控指标：**

- API 响应时间
- 数据库查询时间
- 缓存命中率
- 错误率
- 并发用户数

---

## 10. 扩展性设计

### 10.1 水平扩展

**无状态设计：**

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│ API 实例 1│     │ API 实例 2│     │ API 实例 3│
└──────────┘     └──────────┘     └──────────┘
      ↓                 ↓                 ↓
┌─────────────────────────────────────────────┐
│          负载均衡器 (Nginx)                  │
└─────────────────────────────────────────────┘
      ↓                                   ↓
┌──────────┐                        ┌──────────┐
│ MongoDB  │                        │  Redis   │
│  副本集   │                        │   集群    │
└──────────┘                        └──────────┘
```

---

## 11. 设计决策记录

### ADR-001: 使用 MongoDB 而非 PostgreSQL

**决策：** 选择 MongoDB 作为主数据库

**理由：**
- Todo 数据结构灵活，适合文档存储
- 与 Node.js 集成更自然
- 水平扩展更简单
- 团队熟悉度高

**权衡：** 放弃了关系型数据库的 ACID 特性，但 MongoDB 6+ 已支持事务

---

### ADR-002: 使用 JWT 而非 Session

**决策：** 选择 JWT + Refresh Token 方案

**理由：**
- 无状态，易于水平扩展
- 移动端友好
- 跨域支持好

**权衡：** 无法主动失效 Token，但通过短期 Access Token + Refresh Token 机制缓解

---

## 12. 下一步

- [ ] 评审架构设计
- [ ] 搭建开发环境
- [ ] 初始化项目结构
- [ ] 开始编码实现

---

**使用的 AOS 组件：**
- design skill
- architecture template (参考)

**参考资料：**
- [design skill README](../../skills/design/README.md)
- [requirement 文档](01-requirement.md)
- [research 文档](03-research.md)

---

**Build Once. Run Everywhere.**

**AOS - Agent Operating System**
