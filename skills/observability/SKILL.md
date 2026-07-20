---
name: observability
description: 设计日志、指标、链路追踪的结构化方案，让系统可被观察、可被调试
---

# Observability

设计结构化的日志、指标、链路追踪体系，让线上系统能被外部观察和调试。

## 何时使用

- 新服务要从零搭建可观测性
- 现有日志混乱，事故定位靠猜
- 接入 Prometheus / Grafana / OpenTelemetry 之前
- 微服务调用链需要串联

不要用于：

- 性能瓶颈定位（用 `performance`）
- CI/CD 与部署（用 `devops`）
- 告警阈值配置（属于 `devops` 的监控告警部分）

## 三根支柱

| 支柱 | 解决什么 | 典型工具 |
|---|---|---|
| **Logs（日志）** | 离散事件的详细上下文 | 结构化 JSON + ELK / Loki |
| **Metrics（指标）** | 数值随时间变化的趋势 | Prometheus + Grafana |
| **Traces（链路）** | 跨服务调用的因果与耗时 | OpenTelemetry + Jaeger / Tempo |

三者互补，不要只做一种。

## 流程

### 1. 日志规范

- **结构化**：JSON 行；不要拼接字符串
- **必含字段**：`timestamp` / `level` / `service` / `request_id` / `message`
- **上下文字段**：用户 ID、租户 ID、关键业务 ID
- **级别规范**：`debug` / `info` / `warn` / `error`；生产默认 `info`
- **不打印**：密码、Token、身份证、信用卡、完整请求体（除非审计需要）
- **请求生命周期**：进入记 access log（路径、状态、耗时），异常记 error log（含堆栈）

### 2. 指标体系（RED / USE）

- **服务级（RED）**：Rate（每秒请求）/ Errors（错误率）/ Duration（延迟分布）
- **资源级（USE）**：Utilization / Saturation / Errors（CPU、内存、磁盘、连接池）
- **业务级**：关键 KPI（注册数、下单数、转化率）
- **命名规范**：`<namespace>_<subsystem>_<metric>_<unit>`，例：`http_server_requests_duration_seconds`

### 3. 链路追踪

- **trace_id 贯穿**：HTTP 头 `traceparent` 传递
- **span 粒度**：每个外部调用、慢查询、关键计算节点一个 span
- **关键属性**：`http.method` / `db.statement` / `messaging.destination` / `error.type`
- **采样率**：高 QPS 服务 1%-10%；低 QPS 可 100%

### 4. 关联三支柱

- 日志带 `trace_id` → 可从日志跳到 trace
- trace 带 service / status → 可从 trace 跳到指标
- 指标告警带 dashboard 链接 + 错误日志查询

## 输出格式

```markdown
# Observability Plan

## 技术选型
- Logs: [Loki / ELK / ...]
- Metrics: [Prometheus / ...]
- Traces: [OTel + Tempo / Jaeger / ...]
- Agent: [OTel Collector / Vector / ...]

## 日志规范
- 格式：JSON
- 必含字段：timestamp, level, service, request_id, message
- 不打印：密码、Token、身份证
- 级别：生产 info 起

## 指标清单
### RED
- http_requests_total{service, route, status}
- http_request_duration_seconds_bucket{...}
- http_requests_error_total{...}

### USE
- process_cpu_seconds_total
- process_memory_bytes
- db_pool_connections_active

### 业务
- orders_created_total
- payment_amount_sum

## Trace 关键 Span
- HTTP 入口：method, path, status
- DB 调用：statement, rows
- 外部 HTTP：peer, url, status
- 关键业务：cart.calculate, payment.charge

## 关联设计
- 日志含 trace_id
- 指标含 service / route
- Dashboard 链接到 trace 查询

## 实施清单
- [ ] 接入 OTel SDK
- [ ] 配置日志中间件
- [ ] 暴露 /metrics 端点
- [ ] 部署 OTel Collector
- [ ] Grafana 面板初版
```

## 行为准则

- **生产可关 debug**：避免敏感信息泄漏
- **告警分级**：Critical（立即叫人）/ Warning（次日处理）/ Info（仅记录）
- **采样而非全量**：高 QPS 不可能也不应该全量 trace
- **业务指标先于技术指标**：先衡量「系统是否在为业务创造价值」

## 不要做的事

- 不要打印请求体 / 响应体到日志（除非审计）
- 不要在错误日志里只写「出错了」
- 不要为每个函数都加 span（噪音爆炸）
- 不要把 PII（个人识别信息）放进指标标签
- 不要在日志里用 emoji 或控制字符