# Testing Best Practices

测试的最佳实践和规范。


---


## 测试金字塔


```

       ┌─────────────┐
       │   E2E Tests │  少量（慢、脆弱）
       └─────────────┘
      ┌───────────────┐
      │Integration Tests│  适量（较慢）
      └───────────────┘
    ┌───────────────────┐
    │   Unit Tests      │  大量（快速、稳定）
    └───────────────────┘
```

**推荐比例：** 70% 单元测试，20% 集成测试，10% E2E 测试


---


## 单元测试


### 什么是单元测试


测试独立的函数、类或模块。


### 原则


**F.I.R.S.T 原则：**


- **Fast** - 快速执行

- **Independent** - 独立运行
- **Repeatable** - 可重复
- **Self-Validating** - 自我验证
- **Timely** - 及时编写

### 示例


```javascript

// utils.js
export function add(a, b) {
  return a + b;
}

export function divide(a, b) {

  if (b === 0) {
    throw new Error('Cannot divide by zero');
  }
  return a / b;
}
```

```javascript

// utils.test.js
import { add, divide } from './utils';

describe('add', () => {

  it('should add two positive numbers', () => {
    expect(add(2, 3)).toBe(5);
  });

  it('should add negative numbers', () => {

    expect(add(-1, -2)).toBe(-3);
  });

  it('should add zero', () => {

    expect(add(5, 0)).toBe(5);
  });
});

describe('divide', () => {

  it('should divide two numbers', () => {
    expect(divide(10, 2)).toBe(5);
  });

  it('should throw error when dividing by zero', () => {

    expect(() => divide(10, 0)).toThrow('Cannot divide by zero');
  });
});
```

---


## 集成测试


### 什么是集成测试


测试多个模块的交互。


### 示例


```javascript

// user.service.test.js
import { UserService } from './user.service';
import { Database } from './database';

describe('UserService', () => {

  let service;
  let db;

  beforeEach(async () => {

    db = new Database();
    await db.connect();
    service = new UserService(db);
  });

  afterEach(async () => {

    await db.clear();
    await db.disconnect();
  });

  it('should create and retrieve user', async () => {

    const user = await service.createUser({
      email: 'test@example.com',
      password: 'password123'
    });

    expect(user.id).toBeDefined();

    expect(user.email).toBe('test@example.com');

    const retrieved = await service.getUserById(user.id);

    expect(retrieved).toEqual(user);
  });
});
```

---


## E2E 测试


### 什么是 E2E 测试


测试完整的用户流程。


### 示例（Cypress）


```javascript

// login.spec.js
describe('Login', () => {
  beforeEach(() => {
    cy.visit('/login');
  });

  it('should login successfully', () => {

    cy.get('input[name="email"]').type('user@example.com');
    cy.get('input[name="password"]').type('password123');
    cy.get('button[type="submit"]').click();

    cy.url().should('include', '/dashboard');

    cy.contains('Welcome back');
  });

  it('should show error for invalid credentials', () => {

    cy.get('input[name="email"]').type('invalid@example.com');
    cy.get('input[name="password"]').type('wrong');
    cy.get('button[type="submit"]').click();

    cy.contains('Invalid credentials');

  });
});
```

---


## 测试结构


### AAA 模式


**Arrange** - 准备  

**Act** - 执行  
**Assert** - 断言

```javascript

describe('ShoppingCart', () => {
  it('should calculate total price', () => {
    // Arrange - 准备
    const cart = new ShoppingCart();
    cart.addItem({ price: 10 });
    cart.addItem({ price: 20 });

    // Act - 执行

    const total = cart.getTotal();

    // Assert - 断言

    expect(total).toBe(30);
  });
});
```

### Given-When-Then


BDD 风格的测试结构。


```javascript

describe('User authentication', () => {
  it('should authenticate valid user', () => {
    // Given - 给定条件
    const user = createUser({ email: 'test@example.com', password: 'pass' });
    
    // When - 当执行某操作
    const result = authenticateUser('test@example.com', 'pass');
    
    // Then - 那么应该
    expect(result.success).toBe(true);
    expect(result.user).toEqual(user);
  });
});
```

---


## 测试命名


### 命名规范


✅ **正确：**

```javascript
it('should return user when valid ID is provided', () => {});
it('should throw error when user not found', () => {});
it('should update user email successfully', () => {});
```

❌ **错误：**

```javascript
it('test1', () => {});
it('works', () => {});
it('getUserById', () => {});
```

### 命名模式


**should + 动作 + 条件**


```javascript

describe('User', () => {
  describe('create', () => {
    it('should create user with valid data', () => {});
    it('should throw error when email is invalid', () => {});
    it('should throw error when email already exists', () => {});
  });
});
```

---


## Mock 和 Stub


### Mock（模拟）


```javascript

// jest.mock
jest.mock('./emailService');

import { EmailService } from './emailService';

import { UserService } from './userService';

describe('UserService', () => {

  it('should send welcome email on signup', async () => {
    const emailService = new EmailService();
    emailService.send = jest.fn();

    const userService = new UserService(emailService);

    await userService.signup('test@example.com');

    expect(emailService.send).toHaveBeenCalledWith({

      to: 'test@example.com',
      subject: 'Welcome'
    });
  });
});
```

### Stub（桩）


```javascript

// 使用 sinon
import sinon from 'sinon';

describe('PaymentService', () => {

  it('should process payment', async () => {
    const gateway = {
      charge: sinon.stub().resolves({ success: true })
    };

    const service = new PaymentService(gateway);

    const result = await service.processPayment(100);

    expect(result.success).toBe(true);

    expect(gateway.charge.calledWith(100)).toBe(true);
  });
});
```

---


## 测试覆盖率


### 覆盖率指标


- **语句覆盖率** - 每条语句是否执行

- **分支覆盖率** - 每个条件分支是否执行
- **函数覆盖率** - 每个函数是否调用
- **行覆盖率** - 每行代码是否执行

### 目标


- **最低要求：** 70%

- **推荐目标：** 80%
- **核心业务逻辑：** 90%+

### 查看覆盖率


```bash

# Jest
npm test -- --coverage

# 生成 HTML 报告

npm test -- --coverage --coverageReporters=html
```

### 配置


```json

// package.json
{
  "jest": {
    "collectCoverageFrom": [
      "src/**/*.{js,ts}",
      "!src/**/*.test.{js,ts}",
      "!src/**/*.spec.{js,ts}"
    ],
    "coverageThreshold": {
      "global": {
        "branches": 80,
        "functions": 80,
        "lines": 80,
        "statements": 80
      }
    }
  }
}
```

---


## 测试数据


### 使用工厂函数


```javascript

// factories.js
export function createUser(overrides = {}) {
  return {
    id: '123',
    email: 'test@example.com',
    username: 'testuser',
    role: 'user',
    ...overrides
  };
}

export function createOrder(overrides = {}) {

  return {
    id: '456',
    userId: '123',
    total: 100,
    status: 'pending',
    ...overrides
  };
}
```

```javascript

// user.test.js
import { createUser } from './factories';

describe('User', () => {

  it('should validate admin user', () => {
    const admin = createUser({ role: 'admin' });
    expect(isAdmin(admin)).toBe(true);
  });
});
```

### 使用 Faker


```javascript

import { faker } from '@faker-js/faker';

function createRandomUser() {

  return {
    id: faker.string.uuid(),
    email: faker.internet.email(),
    username: faker.internet.userName(),
    avatar: faker.image.avatar(),
    createdAt: faker.date.past()
  };
}
```

---


## 异步测试


### Promises


```javascript

it('should fetch user data', () => {
  return fetchUser(123).then(user => {
    expect(user.id).toBe(123);
  });
});
```

### Async/Await


```javascript

it('should fetch user data', async () => {
  const user = await fetchUser(123);
  expect(user.id).toBe(123);
});
```

### 测试错误


```javascript

it('should throw error when user not found', async () => {
  await expect(fetchUser(999)).rejects.toThrow('User not found');
});
```

---


## 测试钩子


### beforeEach / afterEach


```javascript

describe('Database', () => {
  let db;

  beforeEach(async () => {

    db = new Database();
    await db.connect();
  });

  afterEach(async () => {

    await db.clear();
    await db.disconnect();
  });

  it('should insert record', async () => {

    await db.insert({ name: 'test' });
    const records = await db.findAll();
    expect(records).toHaveLength(1);
  });
});
```

### beforeAll / afterAll


```javascript

describe('API', () => {
  let server;

  beforeAll(async () => {

    server = await startServer();
  });

  afterAll(async () => {

    await server.close();
  });

  it('should respond to GET /users', async () => {

    const response = await fetch(`${server.url}/users`);
    expect(response.status).toBe(200);
  });
});
```

---


## 参数化测试


### test.each


```javascript

describe('add', () => {
  test.each([
    [1, 1, 2],
    [2, 3, 5],
    [5, 5, 10],
    [-1, 1, 0]
  ])('add(%i, %i) should return %i', (a, b, expected) => {
    expect(add(a, b)).toBe(expected);
  });
});
```

### describe.each


```javascript

describe.each([
  { role: 'admin', canDelete: true },
  { role: 'user', canDelete: false },
  { role: 'guest', canDelete: false }
])('Permissions for $role', ({ role, canDelete }) => {
  it(`should ${canDelete ? 'allow' : 'deny'} delete`, () => {
    const user = { role };
    expect(hasDeletePermission(user)).toBe(canDelete);
  });
});
```

---


## TDD（测试驱动开发）


### Red-Green-Refactor


1. **Red** - 写一个失败的测试

2. **Green** - 写最少的代码让测试通过
3. **Refactor** - 重构代码

### 示例


**Step 1: Red - 写测试**


```javascript

describe('Calculator', () => {
  it('should add two numbers', () => {
    const calc = new Calculator();
    expect(calc.add(2, 3)).toBe(5);
  });
});

// 运行测试 → 失败（Calculator 不存在）

```

**Step 2: Green - 实现代码**


```javascript

class Calculator {
  add(a, b) {
    return a + b;
  }
}

// 运行测试 → 通过

```

**Step 3: Refactor - 重构（如需要）**


```javascript

class Calculator {
  add(...numbers) {
    return numbers.reduce((sum, n) => sum + n, 0);
  }
}

// 运行测试 → 仍然通过

```

---


## 测试最佳实践


### 1. 一个测试只测一件事


✅ **正确：**

```javascript
it('should return user when ID exists', () => {
  const user = getUserById(123);
  expect(user.id).toBe(123);
});

it('should throw error when ID does not exist', () => {

  expect(() => getUserById(999)).toThrow();
});
```

❌ **错误：**

```javascript
it('should handle user retrieval', () => {
  const user = getUserById(123);
  expect(user.id).toBe(123);
  
  expect(() => getUserById(999)).toThrow();
});
```

---


### 2. 测试行为而非实现


✅ **正确：**

```javascript
it('should validate email format', () => {
  expect(isValidEmail('test@example.com')).toBe(true);
  expect(isValidEmail('invalid')).toBe(false);
});
```

❌ **错误：**

```javascript
it('should use regex to validate email', () => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  expect(emailValidator.regex).toEqual(regex);
});
```

---


### 3. 使用有意义的断言


✅ **正确：**

```javascript
expect(user.email).toBe('test@example.com');
expect(user.role).toBe('admin');
```

❌ **错误：**

```javascript
expect(user).toBeTruthy();
expect(user.email).toBeDefined();
```

---


### 4. 避免测试私有方法


只测试公共 API。


---


### 5. 保持测试独立


每个测试应该能独立运行。


❌ **错误：**

```javascript
let userId;

it('should create user', () => {

  userId = createUser().id;  // 依赖顺序
});

it('should delete user', () => {

  deleteUser(userId);  // 依赖前一个测试
});
```

✅ **正确：**

```javascript
it('should create and delete user', () => {
  const userId = createUser().id;
  deleteUser(userId);
  expect(getUser(userId)).toBeNull();
});
```

---


### 6. 使用描述性的错误消息


```javascript

expect(user.age).toBeGreaterThan(18);  // 默认消息

expect(user.age).toBeGreaterThan(18, 'User must be adult');  // 自定义消息

```

---


### 7. 不要测试框架或库


只测试你自己的代码。


---


### 8. 保持测试简单


测试代码应该比业务代码更简单。


---


## 测试工具


### 测试框架


- **Jest** - 功能全面的测试框架

- **Mocha** - 灵活的测试框架
- **Vitest** - 快速的 Vite 测试框架
- **Jasmine** - BDD 测试框架

### 断言库


- **Jest** - 内置

- **Chai** - 表达式断言
- **Should.js** - BDD 风格

### Mock 库


- **Jest** - 内置

- **Sinon** - 功能强大的 Mock 库
- **testdouble.js** - 替代 Sinon

### E2E 工具


- **Cypress** - 现代 E2E 测试

- **Playwright** - 跨浏览器测试
- **Selenium** - 经典自动化工具
- **Puppeteer** - Chrome 自动化

---


## CI/CD 集成


### GitHub Actions


```yaml

name: Tests

on: [push, pull_request]


jobs:

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm test
      - run: npm run test:coverage
      - uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
```

---


## 性能测试


### 基准测试


```javascript

import { performance } from 'perf_hooks';

describe('Performance', () => {

  it('should complete within 100ms', () => {
    const start = performance.now();
    
    // 执行操作
    processLargeArray(data);
    
    const duration = performance.now() - start;
    expect(duration).toBeLessThan(100);
  });
});
```

---


## 快照测试


```javascript

import { render } from '@testing-library/react';
import { Button } from './Button';

it('should match snapshot', () => {

  const { container } = render(<Button>Click me</Button>);
  expect(container).toMatchSnapshot();
});
```

更新快照：


```bash

npm test -- -u
```

---


## 常见错误


### 1. 测试实现细节


❌ 测试内部状态  

✅ 测试外部行为

### 2. 脆弱的测试


过度依赖实现细节，代码小改动就失败。


### 3. 测试过多


不必要的重复测试。


### 4. 测试过少


关键路径没有覆盖。


### 5. 慢测试


测试运行时间过长影响开发效率。


---


## 参考资源


- [Jest Documentation](https://jestjs.io/)

- [Testing Library](https://testing-library.com/)
- [Cypress Best Practices](https://docs.cypress.io/guides/references/best-practices)
- [Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)

---


## 版本历史


- **v1.0.0** - 2026-07-19 - 初始版本


---
