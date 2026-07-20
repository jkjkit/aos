# REST API Design Guidelines

RESTful API 设计最佳实践和规范。


---


## 基本原则


### 1. 使用名词而非动词


✅ **正确：**

```
GET    /users          获取用户列表
GET    /users/123      获取单个用户
POST   /users          创建用户
PUT    /users/123      更新用户
DELETE /users/123      删除用户
```

❌ **错误：**

```
GET  /getUsers
POST /createUser
POST /updateUser
POST /deleteUser
```

---


### 2. 使用复数形式


✅ **正确：**

```
/users
/orders
/products
```

❌ **错误：**

```
/user
/order
/product
```

---


### 3. 使用层级关系


✅ **正确：**

```
GET /users/123/orders          获取用户的订单
GET /users/123/orders/456      获取用户的特定订单
```

❌ **错误：**

```
GET /getUserOrders?userId=123
GET /orders?userId=123
```

---


## HTTP 方法


### GET - 获取资源


**特性：**

- 安全（不修改数据）
- 幂等（多次调用结果相同）
- 可缓存

**示例：**

```http
GET /users              获取用户列表
GET /users/123          获取单个用户
GET /users/123/orders   获取用户的订单
```

---


### POST - 创建资源


**特性：**

- 非幂等（多次调用创建多个资源）
- 不可缓存

**示例：**

```http
POST /users
Content-Type: application/json

{

  "email": "user@example.com",
  "username": "johndoe"
}
```

**响应：**

```http
HTTP/1.1 201 Created
Location: /users/123

{

  "id": "123",
  "email": "user@example.com",
  "username": "johndoe"
}
```

---


### PUT - 完整更新资源


**特性：**

- 幂等（多次调用结果相同）
- 替换整个资源

**示例：**

```http
PUT /users/123
Content-Type: application/json

{

  "email": "newemail@example.com",
  "username": "newusername",
  "profile": {
    "firstName": "John",
    "lastName": "Doe"
  }
}
```

---


### PATCH - 部分更新资源


**特性：**

- 幂等
- 只更新指定字段

**示例：**

```http
PATCH /users/123
Content-Type: application/json

{

  "email": "newemail@example.com"
}
```

---


### DELETE - 删除资源


**特性：**

- 幂等

**示例：**

```http
DELETE /users/123
```

**响应：**

```http
HTTP/1.1 204 No Content
```

或


```http

HTTP/1.1 200 OK

{

  "message": "User deleted successfully"
}
```

---


## URL 设计


### 使用小写字母和短横线


✅ **正确：**

```
/user-profiles
/shopping-carts
```

❌ **错误：**

```
/UserProfiles
/shopping_carts
/shoppingCarts
```

---


### 避免深层嵌套


✅ **正确：**

```
GET /users/123/orders       最多 2 层
```

❌ **错误：**

```
GET /users/123/orders/456/items/789/reviews
```

**替代方案：**

```
GET /order-items/789/reviews
```

---


### 使用查询参数进行过滤、排序和分页


✅ **正确：**

```
GET /users?status=active&sort=createdAt&order=desc&page=1&limit=20
```

❌ **错误：**

```
GET /users/active
GET /users/sorted-by-date
```

---


## 查询参数


### 分页


```

GET /users?page=1&limit=20
```

**响应：**

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


### 过滤


```

GET /users?status=active&role=admin
GET /products?category=electronics&price_min=100&price_max=500
```

---


### 排序


```

GET /users?sort=createdAt&order=desc
GET /products?sort=price&order=asc
```

---


### 搜索


```

GET /users?search=john
GET /products?q=laptop
```

---


### 字段选择


```

GET /users?fields=id,email,username
```

**响应：**

```json
{
  "data": [
    {
      "id": "123",
      "email": "user@example.com",
      "username": "johndoe"
    }
  ]
}
```

---


## 状态码


### 成功响应 (2xx)


| 状态码 | 含义 | 使用场景 |

|--------|------|----------|
| 200 OK | 成功 | GET, PUT, PATCH, DELETE |
| 201 Created | 已创建 | POST 创建资源 |
| 204 No Content | 无内容 | DELETE 成功但无返回内容 |

---


### 客户端错误 (4xx)


| 状态码 | 含义 | 使用场景 |

|--------|------|----------|
| 400 Bad Request | 请求错误 | 参数验证失败 |
| 401 Unauthorized | 未认证 | 需要登录 |
| 403 Forbidden | 无权限 | 权限不足 |
| 404 Not Found | 未找到 | 资源不存在 |
| 409 Conflict | 冲突 | 资源已存在 |
| 422 Unprocessable Entity | 无法处理 | 语义错误 |
| 429 Too Many Requests | 请求过多 | 超过速率限制 |

---


### 服务器错误 (5xx)


| 状态码 | 含义 | 使用场景 |

|--------|------|----------|
| 500 Internal Server Error | 服务器错误 | 未预期的错误 |
| 502 Bad Gateway | 网关错误 | 上游服务错误 |
| 503 Service Unavailable | 服务不可用 | 维护中 |

---


## 响应格式


### 成功响应


```json

{
  "success": true,
  "data": {
    "id": "123",
    "email": "user@example.com"
  }
}
```

**列表响应：**

```json
{
  "success": true,
  "data": {
    "users": [...],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 100
    }
  }
}
```

---


### 错误响应


```json

{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": {
      "email": "Email is required",
      "password": "Password must be at least 8 characters"
    }
  }
}
```

---


## 版本控制


### 方法 1: URL 路径（推荐）


```

/api/v1/users
/api/v2/users
```

---


### 方法 2: 请求头


```http

GET /api/users
Accept: application/vnd.api.v1+json
```

---


### 方法 3: 查询参数（不推荐）


```

/api/users?version=1
```

---


## 认证和授权


### Bearer Token（推荐）


```http

GET /api/users
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---


### API Key


```http

GET /api/users
X-API-Key: your-api-key-here
```

---


## 速率限制


**响应头：**

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1626789600
```

**超过限制：**

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 3600

{

  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests"
  }
}
```

---


## HATEOAS


为响应添加相关链接：


```json

{
  "id": "123",
  "email": "user@example.com",
  "_links": {
    "self": {
      "href": "/users/123"
    },
    "orders": {
      "href": "/users/123/orders"
    },
    "profile": {
      "href": "/users/123/profile"
    }
  }
}
```

---


## 最佳实践


### 1. 使用 HTTPS


所有 API 都应该通过 HTTPS 访问


---


### 2. 提供完善的文档


- API 端点列表

- 请求/响应示例
- 错误代码说明
- 使用示例代码

---


### 3. 实现适当的错误处理


- 统一的错误格式

- 有意义的错误消息
- 不暴露敏感信息

---


### 4. 支持分页


大数据集必须分页，避免一次返回过多数据


---


### 5. 允许字段过滤


允许客户端选择需要的字段，减少数据传输


---


### 6. 使用标准的数据格式


- ISO 8601 日期时间：`2026-07-19T10:00:00Z`

- UUID：`550e8400-e29b-41d4-a716-446655440000`

---


### 7. 实现幂等性


PUT, DELETE, GET 应该是幂等的


---


### 8. 缓存策略


```http

Cache-Control: max-age=3600, private
ETag: "686897696a7c876b7e"
```

---


### 9. 压缩响应


```http

Accept-Encoding: gzip
Content-Encoding: gzip
```

---


### 10. CORS 支持


```http

Access-Control-Allow-Origin: https://example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
```

---


## 反模式


### ❌ 使用动词


```

GET /getUser
POST /createUser
```

---


### ❌ 在 URL 中包含文件扩展名


```

GET /users.json
GET /users.xml
```

**正确：** 使用 Accept 头

```http
Accept: application/json
```

---


### ❌ 混合使用单复数


```

GET /user
GET /users
```

---


### ❌ 返回不一致的数据结构


```json

// 有时返回数组
[{...}, {...}]

// 有时返回对象

{"users": [{...}, {...}]}
```

---


## 工具推荐


- **文档生成：** Swagger/OpenAPI

- **测试：** Postman, Insomnia
- **Mock：** JSON Server, Mockoon
- **验证：** API Blueprint

---


## 参考资源


- [REST API Tutorial](https://restfulapi.net/)

- [HTTP Status Codes](https://httpstatuses.com/)
- [OpenAPI Specification](https://swagger.io/specification/)

---


## 版本历史


- **v1.0.0** - 2026-07-19 - 初始版本


---
