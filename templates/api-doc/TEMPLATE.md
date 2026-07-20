# API Documentation Template

用于创建 RESTful API 文档的标准模板。


---


## API 概述


**项目名称：** [项目名称]


**版本：** v1.0.0


**基础 URL：** `https://api.example.com`


**文档版本：** 2026-07-19


---


## 认证


### 认证方式


使用 JWT Bearer Token 进行认证。


**获取 Token：**


```http

POST /api/auth/login
Content-Type: application/json

{

  "email": "user@example.com",
  "password": "password"
}
```

**响应：**


```json

{
  "success": true,
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresIn": 3600
  }
}
```

**使用 Token：**


```http

GET /api/users
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---


## 端点


### 用户管理


#### 获取用户列表


```http

GET /api/users
```

**描述：** 获取系统中的所有用户（分页）


**认证：** 必需


**权限：** admin


**查询参数：**


| 参数 | 类型 | 必需 | 默认值 | 说明 |

|------|------|------|--------|------|
| page | integer | 否 | 1 | 页码 |
| limit | integer | 否 | 20 | 每页数量 |
| sort | string | 否 | createdAt | 排序字段 |
| order | string | 否 | desc | 排序顺序（asc/desc）|
| search | string | 否 | - | 搜索关键词 |

**请求示例：**


```http

GET /api/users?page=1&limit=20&sort=createdAt&order=desc
Authorization: Bearer <token>
```

**响应示例（200 OK）：**


```json

{
  "success": true,
  "data": {
    "users": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "user@example.com",
        "username": "johndoe",
        "role": "user",
        "status": "active",
        "createdAt": "2026-01-01T00:00:00Z",
        "updatedAt": "2026-07-19T00:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 100,
      "totalPages": 5
    }
  }
}
```

**错误响应：**


```json

// 401 Unauthorized
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required"
  }
}

// 403 Forbidden

{
  "success": false,
  "error": {
    "code": "FORBIDDEN",
    "message": "Insufficient permissions"
  }
}
```

**状态码：**

- 200: 成功
- 401: 未认证
- 403: 无权限
- 500: 服务器错误

---


#### 获取单个用户


```http

GET /api/users/:id
```

**描述：** 根据 ID 获取用户详情


**认证：** 必需


**路径参数：**


| 参数 | 类型 | 说明 |

|------|------|------|
| id | string | 用户 ID（UUID）|

**请求示例：**


```http

GET /api/users/550e8400-e29b-41d4-a716-446655440000
Authorization: Bearer <token>
```

**响应示例（200 OK）：**


```json

{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "username": "johndoe",
    "role": "user",
    "status": "active",
    "profile": {
      "firstName": "John",
      "lastName": "Doe",
      "avatar": "https://example.com/avatars/johndoe.jpg"
    },
    "createdAt": "2026-01-01T00:00:00Z",
    "updatedAt": "2026-07-19T00:00:00Z"
  }
}
```

**错误响应：**


```json

// 404 Not Found
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "User not found"
  }
}
```

**状态码：**

- 200: 成功
- 401: 未认证
- 404: 用户不存在
- 500: 服务器错误

---


#### 创建用户


```http

POST /api/users
```

**描述：** 创建新用户


**认证：** 必需


**权限：** admin


**请求体：**


```json

{
  "email": "newuser@example.com",
  "username": "newuser",
  "password": "SecurePass123",
  "role": "user"
}
```

**字段说明：**


| 字段 | 类型 | 必需 | 说明 |

|------|------|------|------|
| email | string | 是 | 邮箱地址（唯一）|
| username | string | 是 | 用户名（唯一，3-20字符）|
| password | string | 是 | 密码（至少8字符）|
| role | string | 否 | 角色（user/admin），默认 user |

**响应示例（201 Created）：**


```json

{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "email": "newuser@example.com",
    "username": "newuser",
    "role": "user",
    "status": "active",
    "createdAt": "2026-07-19T10:00:00Z"
  }
}
```

**错误响应：**


```json

// 400 Bad Request
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": {
      "email": "Email already exists",
      "password": "Password must be at least 8 characters"
    }
  }
}

// 409 Conflict

{
  "success": false,
  "error": {
    "code": "CONFLICT",
    "message": "User already exists"
  }
}
```

**状态码：**

- 201: 创建成功
- 400: 参数错误
- 401: 未认证
- 403: 无权限
- 409: 用户已存在
- 500: 服务器错误

---


#### 更新用户


```http

PUT /api/users/:id
```

**描述：** 更新用户信息


**认证：** 必需


**路径参数：**


| 参数 | 类型 | 说明 |

|------|------|------|
| id | string | 用户 ID |

**请求体：**


```json

{
  "email": "updated@example.com",
  "username": "updateduser",
  "role": "admin"
}
```

**响应示例（200 OK）：**


```json

{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "updated@example.com",
    "username": "updateduser",
    "role": "admin",
    "updatedAt": "2026-07-19T11:00:00Z"
  }
}
```

**状态码：**

- 200: 更新成功
- 400: 参数错误
- 401: 未认证
- 403: 无权限
- 404: 用户不存在
- 500: 服务器错误

---


#### 删除用户


```http

DELETE /api/users/:id
```

**描述：** 删除用户（软删除）


**认证：** 必需


**权限：** admin


**路径参数：**


| 参数 | 类型 | 说明 |

|------|------|------|
| id | string | 用户 ID |

**响应示例（200 OK）：**


```json

{
  "success": true,
  "message": "User deleted successfully"
}
```

**状态码：**

- 200: 删除成功
- 401: 未认证
- 403: 无权限
- 404: 用户不存在
- 500: 服务器错误

---


## 错误处理


### 标准错误格式


所有错误响应遵循统一格式：


```json

{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": {
      // 可选的详细信息
    }
  }
}
```

### 错误代码


| 代码 | HTTP 状态 | 说明 |

|------|-----------|------|
| VALIDATION_ERROR | 400 | 参数验证失败 |
| UNAUTHORIZED | 401 | 未认证 |
| FORBIDDEN | 403 | 无权限 |
| NOT_FOUND | 404 | 资源不存在 |
| CONFLICT | 409 | 资源冲突 |
| RATE_LIMIT_EXCEEDED | 429 | 超过速率限制 |
| INTERNAL_ERROR | 500 | 服务器内部错误 |

---


## 速率限制


API 实施速率限制以防止滥用。


**限制规则：**


| 端点 | 限制 |

|------|------|
| POST /api/auth/login | 5 次 / 15 分钟 |
| POST /api/users | 10 次 / 小时 |
| 其他端点 | 100 次 / 分钟 |

**响应头：**


```http

X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1626789600
```

**超过限制时：**


```http

HTTP/1.1 429 Too Many Requests

{

  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests, please try again later"
  }
}
```

---


## 版本控制


API 版本通过 URL 路径指定：


```

v1: /api/v1/users
v2: /api/v2/users
```

当前版本：**v1**


---


## 分页


### 请求参数


- `page`: 页码（从 1 开始）

- `limit`: 每页数量（最大 100）

### 响应格式


```json

{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "totalPages": 5
  }
}
```

---


## 排序


使用 `sort` 和 `order` 参数：


```

GET /api/users?sort=createdAt&order=desc
```

**支持的排序字段：**

- createdAt
- updatedAt
- email
- username

---


## 搜索和过滤


### 搜索


```

GET /api/users?search=john
```

搜索范围：username, email


### 过滤


```

GET /api/users?role=admin&status=active
```

---


## 示例代码


### JavaScript (axios)


```javascript

const axios = require('axios');

// 登录获取 Token

const login = async () => {
  const response = await axios.post('https://api.example.com/api/auth/login', {
    email: 'user@example.com',
    password: 'password'
  });
  return response.data.data.accessToken;
};

// 获取用户列表

const getUsers = async (token) => {
  const response = await axios.get('https://api.example.com/api/users', {
    headers: {
      Authorization: `Bearer ${token}`
    },
    params: {
      page: 1,
      limit: 20
    }
  });
  return response.data.data.users;
};
```

### cURL


```bash

# 登录
curl -X POST https://api.example.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'

# 获取用户列表

curl -X GET "https://api.example.com/api/users?page=1&limit=20" \
  -H "Authorization: Bearer <token>"
```

---


## 变更日志


### v1.0.0 (2026-07-19)


- 初始版本

- 用户管理 API
- 认证和授权

---
