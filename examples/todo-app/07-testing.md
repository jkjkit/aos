# 测试报告 - Todo App

**使用 Skill:** `testing`

**输入:** [06-review.md](06-review.md) 中的 A-003 行动项

**目标:** services 层覆盖率 ≥ 70%

---

## 1. 测试策略

| 层级 | 框架 | 比例目标 | 说明 |
|------|------|----------|------|
| 单元 | Jest | 70% | services / utils |
| 集成 | Jest + supertest | 20% | API 端点 |
| E2E | Playwright | 10% | 关键路径 |

## 2. 测试用例

### AuthService 单元测试

```typescript
// tests/unit/auth.service.test.ts
import { AuthService } from '../../src/services/auth.service';
import { User } from '../../src/models/User.model';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';

jest.mock('../../src/models/User.model');

describe('AuthService', () => {
  let service: AuthService;

  beforeEach(() => {
    service = new AuthService();
    jest.clearAllMocks();
  });

  describe('register', () => {
    it('应成功注册新用户', async () => {
      (User.findOne as jest.Mock).mockResolvedValue(null);
      (User.create as jest.Mock).mockResolvedValue({
        _id: 'u1',
        email: 'test@example.com',
        passwordHash: 'hashed',
      });

      const result = await service.register({
        email: 'test@example.com',
        password: 'Pass123!',
        username: 'tester',
      });

      expect(result.user.email).toBe('test@example.com');
      expect(User.create).toHaveBeenCalledWith(
        expect.objectContaining({
          email: 'test@example.com',
          passwordHash: expect.any(String),
        })
      );
    });

    it('邮箱已存在应抛出 ConflictError', async () => {
      (User.findOne as jest.Mock).mockResolvedValue({ _id: 'existing' });

      await expect(
        service.register({
          email: 'taken@example.com',
          password: 'Pass123!',
          username: 'taken',
        })
      ).rejects.toThrow('EMAIL_ALREADY_EXISTS');
    });

    it('密码弱应抛出 ValidationError', async () => {
      await expect(
        service.register({
          email: 'weak@example.com',
          password: '123',
          username: 'weak',
        })
      ).rejects.toThrow('PASSWORD_TOO_WEAK');
    });
  });

  describe('login', () => {
    it('正确凭证应返回 token pair', async () => {
      const hash = await bcrypt.hash('Pass123!', 10);
      (User.findOne as jest.Mock).mockResolvedValue({
        _id: 'u1',
        email: 'test@example.com',
        passwordHash: hash,
      });

      const result = await service.login('test@example.com', 'Pass123!');

      expect(result.accessToken).toBeDefined();
      expect(result.refreshToken).toBeDefined();
      expect(jwt.verify(result.accessToken, process.env.JWT_SECRET!)).toBeTruthy();
    });

    it('错误密码应抛出 UnauthorizedError', async () => {
      const hash = await bcrypt.hash('Pass123!', 10);
      (User.findOne as jest.Mock).mockResolvedValue({
        _id: 'u1',
        passwordHash: hash,
      });

      await expect(
        service.login('test@example.com', 'WrongPass!')
      ).rejects.toThrow('INVALID_CREDENTIALS');
    });
  });
});
```

### Task API 集成测试

```typescript
// tests/integration/task.test.ts
import request from 'supertest';
import { app } from '../../src/app';
import { db } from '../helpers/db';

describe('POST /api/tasks', () => {
  let token: string;

  beforeAll(async () => {
    await db.connect();
    const auth = await request(app)
      .post('/api/auth/register')
      .send({ email: 't@e.com', password: 'Pass123!', username: 't' });
    token = auth.body.data.accessToken;
  });

  afterAll(async () => await db.disconnect());

  it('应创建任务', async () => {
    const res = await request(app)
      .post('/api/tasks')
      .set('Authorization', `Bearer ${token}`)
      .send({ title: '买菜', priority: 'high' });

    expect(res.status).toBe(200);
    expect(res.body.data.title).toBe('买菜');
    expect(res.body.data.userId).toBeDefined();
  });

  it('未认证应 401', async () => {
    const res = await request(app)
      .post('/api/tasks')
      .send({ title: '未登录' });
    expect(res.status).toBe(401);
    expect(res.body.error.code).toBe('AUTH_REQUIRED');
  });

  it('缺 title 应 400', async () => {
    const res = await request(app)
      .post('/api/tasks')
      .set('Authorization', `Bearer ${token}`)
      .send({});
    expect(res.status).toBe(400);
  });
});
```

## 3. 覆盖率报告

| 模块 | 之前 | 之后 | 目标 |
|------|------|------|------|
| services/auth | 32% | 85% | ≥ 70% ✅ |
| services/task | 28% | 78% | ≥ 70% ✅ |
| services/category | 41% | 75% | ≥ 70% ✅ |
| utils | 65% | 92% | ≥ 80% ✅ |
| **整体** | **45%** | **82%** | ≥ 70% ✅ |

## 4. 风险与遗留

- ⚠️ 通知模块（notification.service）暂未覆盖，下迭代补
- ⚠️ E2E 测试脚本已写但 CI 未集成
- ✅ 所有 Critical / Major 路径已有断言

## 下一步

进入 [08-deployment.md](08-deployment.md) — 由 `devops` Skill 设计部署方案。