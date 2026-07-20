# 代码实现 - Todo App

**使用 Skill:** `coding`、`database`

**输入:** [04-design.md](04-design.md)

**输出:** 项目骨架 + 核心实现

---

## 1. 实现概述

基于架构设计文档，进入编码阶段。本阶段遵循以下原则：

- 先骨架后细节
- 测试与代码同步
- 错误处理统一
- 日志规范统一

## 2. 项目结构

### 后端 (Node.js + TypeScript)

```
backend/
├── src/
│   ├── config/
│   │   ├── env.ts
│   │   ├── database.ts
│   │   └── redis.ts
│   ├── controllers/
│   │   ├── auth.controller.ts
│   │   ├── task.controller.ts
│   │   └── category.controller.ts
│   ├── services/
│   │   ├── auth.service.ts
│   │   ├── task.service.ts
│   │   ├── category.service.ts
│   │   └── notification.service.ts
│   ├── models/
│   │   ├── User.model.ts
│   │   ├── Task.model.ts
│   │   └── Category.model.ts
│   ├── middleware/
│   │   ├── auth.middleware.ts
│   │   ├── error.middleware.ts
│   │   └── rateLimit.middleware.ts
│   ├── routes/
│   │   ├── auth.routes.ts
│   │   ├── task.routes.ts
│   │   └── category.routes.ts
│   ├── utils/
│   │   ├── jwt.util.ts
│   │   ├── password.util.ts
│   │   └── logger.util.ts
│   ├── types/
│   │   └── express.d.ts
│   ├── jobs/
│   │   └── reminder.job.ts
│   ├── app.ts
│   └── server.ts
├── tests/
│   ├── unit/
│   └── integration/
├── package.json
├── tsconfig.json
└── .env.example
```

### 前端 (React + TypeScript)

```
frontend/
├── src/
│   ├── components/
│   │   ├── common/         # Button / Input / Modal
│   │   ├── layout/         # Header / Sidebar
│   │   └── features/       # auth / tasks / categories
│   ├── pages/
│   │   ├── Login/
│   │   ├── Tasks/
│   │   └── Settings/
│   ├── hooks/
│   ├── store/              # Zustand
│   ├── services/           # API client
│   ├── utils/
│   ├── types/
│   ├── App.tsx
│   └── main.tsx
├── package.json
├── vite.config.ts
└── tailwind.config.js
```

## 3. 核心代码示例

### 认证中间件

```typescript
// src/middleware/auth.middleware.ts
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { User } from '../models/User.model';
import { UnauthorizedError } from '../utils/errors';

export const authenticate = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  try {
    const authHeader = req.headers.authorization;
    if (!authHeader?.startsWith('Bearer ')) {
      throw new UnauthorizedError('Missing token');
    }

    const token = authHeader.substring(7);
    const decoded = jwt.verify(token, process.env.JWT_SECRET!) as { userId: string };

    const user = await User.findById(decoded.userId);
    if (!user) {
      throw new UnauthorizedError('User not found');
    }

    req.user = user;
    next();
  } catch (error) {
    next(error);
  }
};
```

### Task Service

```typescript
// src/services/task.service.ts
import { Task, ITask } from '../models/Task.model';
import { ForbiddenError, NotFoundError } from '../utils/errors';

export class TaskService {
  async create(userId: string, data: Partial<ITask>): Promise<ITask> {
    const task = await Task.create({ ...data, userId });
    return task;
  }

  async list(userId: string, query: ListQuery): Promise<PaginatedResult<ITask>> {
    const { page = 1, limit = 20, status, categoryId } = query;
    const filter: any = { userId };
    if (status) filter.status = status;
    if (categoryId) filter.categoryId = categoryId;

    const [items, total] = await Promise.all([
      Task.find(filter)
        .sort({ createdAt: -1 })
        .skip((page - 1) * limit)
        .limit(limit)
        .populate('categoryId', 'name color')
        .lean(),
      Task.countDocuments(filter),
    ]);

    return {
      items,
      pagination: { page, limit, total, pages: Math.ceil(total / limit) },
    };
  }

  async complete(userId: string, taskId: string): Promise<ITask> {
    const task = await Task.findById(taskId);
    if (!task) throw new NotFoundError('Task not found');
    if (task.userId.toString() !== userId) {
      throw new ForbiddenError('No access to this task');
    }

    task.status = 'completed';
    task.completedAt = new Date();
    await task.save();
    return task;
  }
}
```

### 错误处理中间件

```typescript
// src/middleware/error.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { AppError } from '../utils/errors';
import logger from '../utils/logger';

export const errorHandler = (
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  if (err instanceof AppError) {
    logger.warn('Business error', {
      code: err.code,
      message: err.message,
      path: req.path,
      userId: req.user?._id,
    });
    return res.status(err.statusCode).json({
      success: false,
      error: { code: err.code, message: err.message },
    });
  }

  logger.error('Unhandled error', {
    message: err.message,
    stack: err.stack,
    path: req.path,
  });

  return res.status(500).json({
    success: false,
    error: { code: 'INTERNAL_ERROR', message: 'Internal server error' },
  });
};
```

## 4. 验证清单

- [ ] 后端骨架创建完成
- [ ] 前端骨架创建完成
- [ ] 认证流程跑通
- [ ] CRUD 跑通
- [ ] 错误处理统一
- [ ] 日志接入
- [ ] 环境变量模板就绪
- [ ] 基础 TypeScript 类型检查通过

## 5. 下一步

进入 [06-review.md](06-review.md) — 由 `review` Skill 做双轴代码审查。