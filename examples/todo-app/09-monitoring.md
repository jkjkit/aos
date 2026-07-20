# 监控配置 - Todo App

**使用 Skill:** `observability`

**输入:** [08-deployment.md](08-deployment.md)

**目标:** RED + USE 指标 + 业务指标 + 告警

---

## 1. 技术选型

| 维度 | 选型 |
|------|------|
| Metrics | Prometheus + Grafana |
| Logs | Loki + Promtail |
| Traces | OpenTelemetry + Tempo |
| Agent | OTel Collector |

## 2. 日志规范

JSON 行结构，必含字段：

```json
{
  "timestamp": "2026-07-20T14:30:00.123Z",
  "level": "info",
  "service": "todo-app",
  "request_id": "abc123",
  "user_id": "u_456",
  "message": "Task created",
  "task_id": "t_789",
  "duration_ms": 45
}
```

**不打印：** 密码、Token、身份证、完整请求体。

**日志中间件示例：**

```typescript
// src/middleware/log.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { v4 as uuid } from 'uuid';
import logger from '../utils/logger';

export const logMiddleware = (req: Request, res: Response, next: NextFunction) => {
  const requestId = req.headers['x-request-id'] as string || uuid();
  req.requestId = requestId;
  res.setHeader('x-request-id', requestId);

  const start = Date.now();

  res.on('finish', () => {
    logger.info('http_request', {
      request_id: requestId,
      method: req.method,
      path: req.path,
      status: res.statusCode,
      duration_ms: Date.now() - start,
      user_id: req.user?._id?.toString(),
    });
  });

  next();
};
```

## 3. 指标清单

### RED（服务级）

| 指标 | 类型 | 说明 |
|------|------|------|
| `http_requests_total{method,route,status}` | counter | 请求总数 |
| `http_request_duration_seconds_bucket{...}` | histogram | 延迟分布 |
| `http_requests_error_total{...}` | counter | 5xx + 业务错误 |

### USE（资源级）

| 指标 | 说明 |
|------|------|
| `process_cpu_seconds_total` | CPU 占用 |
| `process_memory_bytes` | 内存占用 |
| `db_pool_connections_active` | Mongo 连接池 |
| `db_pool_connections_idle` | 空闲连接 |

### 业务级

| 指标 | 说明 |
|------|------|
| `tasks_created_total` | 任务创建数 |
| `tasks_completed_total` | 任务完成数 |
| `users_registered_total` | 用户注册数 |
| `auth_login_success_total` | 登录成功 |
| `auth_login_failure_total` | 登录失败 |

## 4. Prometheus 配置

```yaml
# /etc/prometheus/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'todo-app'
    static_configs:
      - targets: ['app:4000']
    metrics_path: /metrics
```

## 5. 告警规则

```yaml
# /etc/prometheus/rules/todo-app.yml
groups:
  - name: todo-app-alerts
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_error_total[5m]))
          /
          sum(rate(http_requests_total[5m]))
          > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "错误率超过 5%"
          description: "5 分钟错误率 {{ $value | humanizePercentage }}"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))
          > 1.0
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "P95 延迟超过 1s"

      - alert: InstanceDown
        expr: up{job="todo-app"} == 0
        for: 1m
        labels:
          severity: critical

      - alert: DiskSpaceLow
        expr: (node_filesystem_avail_bytes / node_filesystem_size_bytes) < 0.1
        for: 5m
        labels:
          severity: warning
```

## 6. Grafana Dashboard

包含面板：

- **Overview**：QPS / 错误率 / P95 延迟
- **RED**：按 route 拆分
- **USE**：CPU / 内存 / 连接池
- **Business**：注册 / 创建任务趋势
- **Logs**：最近错误日志（接 Loki）

## 7. Trace 集成

```typescript
// src/utils/tracing.ts
import { NodeSDK } from '@opentelemetry/sdk-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';

const sdk = new NodeSDK({
  serviceName: 'todo-app',
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://otel-collector:4318/v1/traces',
  }),
});

sdk.start();
```

**关键 span：** HTTP 入口、DB 调用、外部 API 调用。

## 8. 告警通道

- Critical → PagerDuty / 电话
- Warning → Slack #alerts 频道
- Info → 仅记录，不通知

## 下一步

进入 [10-documentation.md](10-documentation.md) — 由 `document` Skill 编写用户文档。