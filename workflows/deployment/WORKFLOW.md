# Deployment Workflow

应用部署的标准工作流程。

---

## 适用场景

- 部署到测试环境
- 部署到预发布环境
- 部署到生产环境

---

## 工作流程

```
准备部署
    ↓
Step 1: 部署前检查
    ↓
Step 2: 构建和打包
    ↓
Step 3: 环境准备
    ↓
Step 4: 执行部署
    ↓
Step 5: 健康检查
    ↓
Step 6: 烟雾测试
    ↓
Step 7: 监控和验证
    ↓
Step 8: 回滚准备
```

---

## 详细步骤

### Step 1: 部署前检查

**检查清单：**

- [ ] 代码已合并到目标分支
- [ ] 所有测试通过
- [ ] 代码审查完成
- [ ] 版本号已更新
- [ ] 变更日志已更新
- [ ] 数据库迁移已准备
- [ ] 配置文件已检查
- [ ] 依赖版本已锁定

**环境检查：**

```bash
# 检查目标环境状态
kubectl get nodes
kubectl get pods -n production

# 检查资源使用情况
kubectl top nodes
kubectl top pods -n production

# 检查当前版本
kubectl get deployment myapp -n production -o yaml | grep image:
```

**通知相关人员：**

- 通知团队部署开始
- 通知 QA 团队准备测试
- 通知运维团队监控

---

### Step 2: 构建和打包

**构建应用：**

```bash
# 清理旧的构建产物
npm run clean
# 或
make clean

# 安装依赖
npm ci
# 或
yarn install --frozen-lockfile

# 运行测试
npm test

# 构建生产版本
npm run build:production
# 或
make build
```

**构建 Docker 镜像：**

```bash
# 构建镜像
docker build -t myapp:v1.2.3 .

# 标记镜像
docker tag myapp:v1.2.3 registry.example.com/myapp:v1.2.3
docker tag myapp:v1.2.3 registry.example.com/myapp:latest

# 推送到镜像仓库
docker push registry.example.com/myapp:v1.2.3
docker push registry.example.com/myapp:latest
```

**验证构建：**

```bash
# 检查镜像大小
docker images myapp:v1.2.3

# 扫描安全漏洞
docker scan myapp:v1.2.3
# 或
trivy image myapp:v1.2.3
```

---

### Step 3: 环境准备

**备份当前状态：**

```bash
# 备份数据库
pg_dump -h db.example.com -U user mydb > backup-$(date +%Y%m%d-%H%M%S).sql

# 备份 Kubernetes 配置
kubectl get deployment myapp -n production -o yaml > deployment-backup.yaml
```

**准备配置：**

```bash
# 更新 ConfigMap
kubectl create configmap myapp-config \
  --from-file=config.json \
  --dry-run=client -o yaml | kubectl apply -f -

# 更新 Secret
kubectl create secret generic myapp-secrets \
  --from-literal=db-password=$DB_PASSWORD \
  --dry-run=client -o yaml | kubectl apply -f -
```

**数据库迁移：**

```bash
# 检查迁移状态
npm run migrate:status

# 执行迁移（如需要）
npm run migrate:up
```

---

### Step 4: 执行部署

**滚动更新（推荐）：**

```bash
# 更新镜像
kubectl set image deployment/myapp \
  myapp=registry.example.com/myapp:v1.2.3 \
  -n production

# 或使用 apply
kubectl apply -f deployment.yaml

# 查看部署进度
kubectl rollout status deployment/myapp -n production
```

**蓝绿部署：**

```bash
# 部署新版本（green）
kubectl apply -f deployment-green.yaml

# 等待新版本就绪
kubectl wait --for=condition=available deployment/myapp-green -n production

# 切换流量
kubectl patch service myapp -n production -p '{"spec":{"selector":{"version":"green"}}}'

# 保留旧版本（blue）一段时间以便回滚
```

**金丝雀部署：**

```bash
# 部署金丝雀版本（10% 流量）
kubectl apply -f deployment-canary.yaml

# 观察指标
# 如果正常，逐步增加流量到 50%、100%

# 完全切换后删除旧版本
kubectl delete deployment myapp-old -n production
```

---

### Step 5: 健康检查

**检查 Pod 状态：**

```bash
# 查看 Pod 状态
kubectl get pods -n production -l app=myapp

# 查看 Pod 详情
kubectl describe pod <pod-name> -n production

# 查看日志
kubectl logs -f deployment/myapp -n production
```

**检查端点：**

```bash
# 健康检查端点
curl https://api.example.com/health

# 就绪检查端点
curl https://api.example.com/ready

# 版本信息
curl https://api.example.com/version
```

**预期响应：**

```json
{
  "status": "healthy",
  "version": "v1.2.3",
  "uptime": 120,
  "checks": {
    "database": "ok",
    "redis": "ok",
    "external_api": "ok"
  }
}
```

---

### Step 6: 烟雾测试

**手动测试：**

- [ ] 登录功能正常
- [ ] 核心功能可用
- [ ] API 响应正常
- [ ] 页面加载正常

**自动化测试：**

```bash
# 运行烟雾测试套件
npm run test:smoke -- --env=production

# 或使用 curl
./scripts/smoke-test.sh production
```

**示例烟雾测试：**

```bash
#!/bin/bash
# smoke-test.sh

BASE_URL="https://api.example.com"

echo "Testing health endpoint..."
curl -f $BASE_URL/health || exit 1

echo "Testing authentication..."
TOKEN=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test"}' \
  | jq -r '.data.accessToken')

echo "Testing protected endpoint..."
curl -f -H "Authorization: Bearer $TOKEN" \
  $BASE_URL/users/me || exit 1

echo "All smoke tests passed!"
```

---

### Step 7: 监控和验证

**监控指标：**

```bash
# CPU 和内存使用
kubectl top pods -n production -l app=myapp

# 查看事件
kubectl get events -n production --sort-by='.lastTimestamp'
```

**应用指标：**

- 响应时间
- 错误率
- 吞吐量
- 活跃连接数

**检查日志：**

```bash
# 查看应用日志
kubectl logs -f deployment/myapp -n production --tail=100

# 查看错误日志
kubectl logs deployment/myapp -n production | grep ERROR

# 查看访问日志
kubectl logs deployment/myapp -n production | grep "HTTP/1.1"
```

**告警检查：**

- 查看监控面板（Grafana, Datadog）
- 检查告警系统（PagerDuty, 企业微信）
- 确认无新增告警

---

### Step 8: 回滚准备

**回滚条件：**

触发回滚的情况：
- 错误率超过阈值（> 5%）
- 响应时间显著增加（> 2x）
- 健康检查失败
- 严重功能问题

**快速回滚：**

```bash
# Kubernetes 回滚
kubectl rollout undo deployment/myapp -n production

# 回滚到特定版本
kubectl rollout undo deployment/myapp -n production --to-revision=2

# 查看回滚状态
kubectl rollout status deployment/myapp -n production
```

**蓝绿部署回滚：**

```bash
# 切换回旧版本
kubectl patch service myapp -n production -p '{"spec":{"selector":{"version":"blue"}}}'
```

**数据库回滚：**

```bash
# 回滚迁移
npm run migrate:down

# 或恢复备份
psql -h db.example.com -U user mydb < backup-20260719-100000.sql
```

---

## 环境策略

### 开发环境

- **频率：** 每次提交
- **自动化：** 完全自动化
- **审批：** 无需审批
- **回滚：** 自动

### 测试环境

- **频率：** 每日
- **自动化：** 大部分自动化
- **审批：** 无需审批
- **回滚：** 自动

### 预发布环境

- **频率：** 每周或按需
- **自动化：** 半自动化
- **审批：** Tech Lead
- **回滚：** 手动触发

### 生产环境

- **频率：** 按计划或紧急
- **自动化：** 半自动化
- **审批：** 多人审批
- **回滚：** 立即可用

---

## 部署时间窗口

### 推荐时间

- **生产环境：** 工作日上午（10:00-12:00）或下午（14:00-16:00）
- **避免时间：** 周五下午、节假日前、业务高峰期

### 维护窗口

如需停机维护：
- 提前通知用户（至少 24 小时）
- 选择业务低峰期
- 准备回滚方案

---

## 部署清单

### 部署前

- [ ] 代码已合并
- [ ] 测试全部通过
- [ ] 代码审查完成
- [ ] 版本号已更新
- [ ] 配置已检查
- [ ] 依赖已锁定
- [ ] 备份已完成
- [ ] 团队已通知

### 部署中

- [ ] 构建成功
- [ ] 镜像已推送
- [ ] 配置已更新
- [ ] 迁移已执行
- [ ] 部署已完成
- [ ] Pod 状态正常

### 部署后

- [ ] 健康检查通过
- [ ] 烟雾测试通过
- [ ] 监控指标正常
- [ ] 日志无异常
- [ ] 功能验证通过
- [ ] 团队已通知

---

## 故障处理

### 部署失败

**问题：** Pod 启动失败

```bash
# 查看 Pod 状态
kubectl describe pod <pod-name> -n production

# 常见原因：
# - 镜像拉取失败
# - 配置错误
# - 健康检查失败
# - 资源不足
```

**解决方案：**
1. 检查错误信息
2. 修复问题
3. 重新部署或回滚

---

### 性能下降

**问题：** 响应时间增加

**排查步骤：**
1. 查看资源使用情况
2. 检查数据库性能
3. 查看日志中的慢查询
4. 检查外部依赖

---

### 错误率上升

**问题：** 错误率超过阈值

**排查步骤：**
1. 查看错误日志
2. 检查新增代码
3. 验证配置
4. 考虑回滚

---

## 最佳实践

### 1. 自动化部署

使用 CI/CD 工具自动化部署流程

### 2. 灰度发布

重要更新使用金丝雀或蓝绿部署

### 3. 监控告警

设置完善的监控和告警

### 4. 快速回滚

确保随时可以快速回滚

### 5. 文档记录

记录每次部署的详细信息

### 6. 团队协作

部署时保持团队沟通

---

## CI/CD 集成

### GitHub Actions

```yaml
name: Deploy to Production

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build and push Docker image
        run: |
          docker build -t myapp:${GITHUB_REF_NAME} .
          docker push registry.example.com/myapp:${GITHUB_REF_NAME}
      
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/myapp \
            myapp=registry.example.com/myapp:${GITHUB_REF_NAME} \
            -n production
      
      - name: Wait for rollout
        run: |
          kubectl rollout status deployment/myapp -n production
      
      - name: Run smoke tests
        run: npm run test:smoke
```

---

## 相关 Skills

- **devops** - CI/CD、容器化、部署配置
- **security** - 镜像与依赖扫描
- **performance** - 上线后基线对比
- **release workflow** - 发布流程

---

## 版本历史

- **v1.0.0** - 2026-07-19 - 初始版本

---
