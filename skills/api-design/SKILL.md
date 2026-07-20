---
name: api-design
description: 为已明确的业务需求定义 RESTful 或 GraphQL API 契约、错误码与版本策略；不负责系统总体架构或调用实现
---

# API Design

设计对外 API 契约——端点、字段、错误码、鉴权、分页、版本。聚焦在「契约层」，不重复 `design` 的系统架构。

## 何时使用

- 新服务要定义对外 API
- 现有 API 需要重构或扩版本
- 多端（Web / iOS / Android / 第三方）需要统一接口约定
- 写 OpenAPI / GraphQL Schema / AsyncAPI 文档之前

不要用于：

- 系统架构设计（用 `design`）
- 对接别人的 API（用 `api-integration`）
- 数据库 Schema（用 `database`）

## 流程

1. **明确资源与动作**：用「资源 + 方法」的思路列出实体（`User` / `Order`）与操作（`create` / `get` / `list` / `update` / `delete`）
2. **选择风格**：
   - REST + JSON（最常见）
   - GraphQL（多端聚合、Schema 优先）
   - RPC（gRPC / Thrift，内部服务）
   - WebSocket / SSE（实时推送）
3. **设计端点**：路径、HTTP 方法、Query / Body 参数；命名统一复数、kebab-case
4. **设计字段**：请求 / 响应都用强类型；命名保持一致（驼峰或下划线，团队统一）
5. **错误体系**：用统一错误码（`AUTH_REQUIRED` / `INVALID_INPUT` / `NOT_FOUND` / `RATE_LIMITED` 等）；HTTP 状态码与业务码分层
6. **鉴权与权限**：OAuth2 / API Key / JWT；明确每个端点的权限要求
7. **分页与过滤**：列表接口必须支持；统一游标或页码约定
8. **幂等性**：POST 是否要 Idempotency-Key；DELETE 默认幂等
9. **版本策略**：URL 路径（`/v1/`）/ Header / 内容协商；破坏性变更走新版本
10. **限流与配额**：明确每个端点的限流阈值与降级策略
11. **输出 OpenAPI / Schema 文件**：机器可读的契约源

## 输出格式

```markdown
# API Design

## 概述
[风格、版本、目标客户端]

## 资源列表
| 资源 | 端点 | 说明 |
|------|------|------|

## 端点详情

### GET /api/v1/users/:id
- 鉴权：Bearer JWT，必须登录
- 路径参数：id (UUID)
- Query：fields (可选，字段过滤)
- 响应 200：User 完整对象
- 响应 401：AUTH_REQUIRED
- 响应 404：USER_NOT_FOUND

### POST /api/v1/orders
...

## 错误码
| 码 | HTTP | 含义 |
|----|------|------|
| AUTH_REQUIRED | 401 | 未登录或 Token 失效 |
| INVALID_INPUT | 400 | 参数校验失败 |
| ...

## 通用约定
- 时间字段统一 ISO 8601（UTC）
- 列表默认 limit=20，max=100
- 软删除字段 `deleted_at`
- 分页：cursor-based，response.next_cursor
```

## 设计原则

- **资源优先**：URL 表达资源，HTTP 方法表达动作
- **可预测**：相同资源在所有端点的字段名一致
- **可演进**：新增字段默认不破坏老客户端
- **可调试**：每个响应带 `request_id` 便于链路追踪
- **文档先行**：OpenAPI 是契约源，不是事后补

## 行为准则

- **破坏性变更 = 新版本**：不要在原版本偷偷改字段语义
- **错误信息面向开发者**：给清楚的下一步建议，不是「出错了」
- **鉴权逐端点标注**：不让客户端猜哪个端点要登录
- **先写 Schema 再写代码**：契约是单一事实源

## 不要做的事

- 不要在 URL 中放动词（`/getUser` 是错的，`GET /users/:id` 是对的）
- 不要用 HTTP 状态码 200 表达业务错误
- 不要返回完整堆栈或 SQL 错误到响应里
- 不要混用驼峰和下划线
- 不要让列表接口返回全表
