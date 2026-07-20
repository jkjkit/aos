---
name: devops
description: 设计 CI/CD 流水线、容器化、部署与监控告警的配置
---

# DevOps

为应用搭建从代码到生产的交付链路：CI/CD、容器化、部署策略、监控告警。

## 何时使用

- 新项目需要搭建交付流水线
- 现有部署手工化，要改自动化
- 引入容器或迁移到 K8s
- 上线前需要交付清单与回滚方案
- 监控告警体系建立或补齐

不要用于：

- 业务功能未实现（先 coding 与 testing）
- 仅排查线上故障（用 debug）
- 性能调优（用 performance）

## 流程

1. **明确交付链路**：构建 → 测试 → 打包 → 部署；触发条件（push / tag / 手动）；环境（dev / staging / prod）
2. **CI 配置**：装依赖 → lint → test → build → 产物归档；失败即阻断
3. **容器化**：写 Dockerfile（多阶段、最小基础镜像、非 root、固定版本）；建镜像并推镜像仓库
4. **部署策略**：滚动 / 蓝绿 / 金丝雀；健康检查 + 就绪探针；回滚命令与触发条件
5. **配置与密钥**：环境变量管理；敏感信息走密钥管理服务；不写进镜像
6. **监控告警**：基础指标（QPS / 延迟 / 错误率 / 资源）+ 业务关键指标；日志采集；告警阈值与通道
7. **Runbook**：部署步骤、回滚步骤、常见问题

## 输出格式

```markdown
# DevOps Plan

## 链路总览
[从 push 到生产的完整路径]

## CI
- File: `.github/workflows/ci.yml`
- Stages: lint / test / build
- Trigger: push / PR / tag

## Container
- Dockerfile: [路径]
- Image: registry/repo:tag
- 策略: 多阶段 / distroless / 非 root

## Deployment
- Strategy: rolling / blue-green / canary
- Health Check: [路径或命令]
- Rollback: [命令 + 触发条件]

## 配置与密钥
- Env Vars: [列表]
- Secrets: [管理方式]

## 监控告警
- Metrics: QPS / Latency / Error / Resource
- Logs: [采集方式]
- Alerts: [阈值 + 通道]

## Runbook
- Deploy: [步骤]
- Rollback: [步骤]
- Common Issues: [列表]
```

## Dockerfile 要点

- 多阶段构建：构建阶段装完整工具链，运行阶段只保留产物
- 最小基础镜像：`alpine` / `distroless` / `scratch`
- 非 root 运行：USER 指令
- 锁定版本：不要 `latest` 标签
- HEALTHCHECK：内置健康检查命令
- `.dockerignore`：排除 node_modules、.git、tests

## CI 要点

- **缓存依赖**：pip / npm / pnpm / go mod 都有官方缓存策略
- **矩阵测试**：跨语言版本、跨 OS
- **失败阻断**：lint / test 失败不进入 build 阶段
- **产物归档**：构建产物上传 artifacts，避免重复构建

## 部署策略选择

| 场景 | 推荐策略 |
|------|----------|
| 普通服务 | 滚动更新 |
| 关键交易 | 蓝绿 |
| 体验型更新 | 金丝雀（10% → 50% → 100%） |
| 数据库迁移 | 先双写、再切读、最后切写 |

## 行为准则

- **不直接部署到生产**：所有变更先到预发验证
- **回滚先于修复**：上线出问题先回滚，再定位原因
- **配置即代码**：部署脚本、流水线、Dockerfile 进版本控制
- **承认依赖风险**：基础镜像漏洞、第三方 API 变更都需要监控

## 不要做的事

- 不要把密钥写进 Dockerfile 或镜像
- 不要用 `latest` 标签部署
- 不要跳过健康检查
- 不要让部署脚本无法回滚