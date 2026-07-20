# 发布说明 - Todo App v1.0.0

**使用 Workflow:** `release`

**输入:** [10-documentation.md](10-documentation.md)

**版本：** v1.0.0

**发布日期：** 2026-07-20

---

## 发布前检查

- [x] 所有功能完成
- [x] 测试覆盖 ≥ 70%（实际 82%）
- [x] 代码审查通过
- [x] 文档更新
- [x] 监控告警配置完成
- [x] 部署文档完成
- [x] CHANGELOG 已写
- [x] 版本号更新

## 发布流程

### 1. 版本号更新

```bash
# backend/package.json
{ "version": "1.0.0" }

# frontend/package.json
{ "version": "1.0.0" }
```

### 2. Git Tag

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

### 3. CI 触发自动部署

推送 tag 后 GitHub Actions 自动：

1. 运行测试
2. 构建镜像
3. 推送到 ghcr.io
4. SSH 到服务器拉取并启动
5. 运行健康检查

### 4. 烟雾测试

```bash
curl https://api.todoapp.com/health
curl -X POST https://api.todoapp.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"smoke@test.com","password":"Pass123!","username":"smoke"}'
```

### 5. 监控确认

- [x] 错误率 < 0.1%
- [x] P95 延迟 < 500ms
- [x] 无 Critical 告警

## What's New in v1.0.0

### 🎉 主要功能

- 用户注册 / 登录（含 JWT + Refresh Token）
- 任务的 CRUD（创建、查询、更新、删除、标记完成）
- 任务分类（颜色、图标）
- 优先级（高 / 中 / 低）
- 截止日期与提醒
- 任务列表分页、筛选、排序

### 🔒 安全特性

- 密码 bcrypt 加密
- JWT Access Token（15 分钟）+ Refresh Token（7 天）
- 限流防暴力破解
- CORS 白名单
- 输入校验统一

### ⚡ 性能

- 多层缓存（Redis + 内存）
- MongoDB 索引优化
- 静态资源 CDN
- Gzip 压缩

### 📊 可观测性

- 结构化 JSON 日志
- RED + USE 指标
- OpenTelemetry Trace
- Grafana Dashboard
- Prometheus 告警

### 📦 部署

- 多阶段 Docker 镜像
- GitHub Actions CI/CD
- 健康检查
- 一键回滚

### ⚠️ Breaking Changes

无（首个正式版本）

### 🐛 已知问题

- 移动端尚未适配（计划 v1.1.0）
- 第三方分享未实现（计划 v1.2.0）

## 安装与升级

### 新用户

```bash
docker compose up -d
```

### 从旧版本升级（如果有）

```bash
git pull
docker compose pull
docker compose up -d
```

数据库迁移脚本：

```bash
docker compose exec app pnpm migrate
```

## 致谢

- 所有贡献者
- 早期采用者提供的反馈
- 开源社区

## 反馈渠道

- GitHub Issues
- Email: support@todoapp.com
- Discord: discord.gg/todoapp

---

**完整变更日志：** [CHANGELOG.md](CHANGELOG.md)
**升级指南：** [UPGRADE.md](UPGRADE.md)
**下载：** https://github.com/yourorg/todo-app/releases/tag/v1.0.0