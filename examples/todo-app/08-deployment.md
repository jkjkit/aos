# 部署文档 - Todo App

**使用 Skill:** `devops`

**输入:** [07-testing.md](07-testing.md)

**目标:** 单容器 Docker 部署 + GitHub Actions 自动构建

---

## 1. 部署架构

```
Git Push (tag v*)
       ↓
GitHub Actions
       ↓
Build Frontend (Vite) ──→ Static files
Build Backend  (tsc)  ──→ dist/
Docker Build Multi-stage ──→ Image
       ↓
Push to ghcr.io
       ↓
Deploy to Server (ssh + docker compose)
```

## 2. Dockerfile

多阶段构建，最小运行时镜像。

```dockerfile
# frontend build
FROM node:20-alpine AS frontend-build
WORKDIR /app
COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile
COPY frontend/ ./
RUN pnpm build

# backend build
FROM node:20-alpine AS backend-build
WORKDIR /app
COPY backend/package.json backend/pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile
COPY backend/ ./
RUN pnpm build

# runtime
FROM node:20-alpine
WORKDIR /app
ENV NODE_ENV=production

# 前端产物
COPY --from=frontend-build /app/dist ./public

# 后端依赖（仅 prod）
COPY backend/package.json backend/pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile --prod

# 后端代码
COPY --from=backend-build /app/dist ./dist

# 非 root
USER node
EXPOSE 4000

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget -qO- http://localhost:4000/health || exit 1

CMD ["node", "dist/server.js"]
```

## 3. docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    image: ghcr.io/yourorg/todo-app:${TAG:-latest}
    ports:
      - "4000:4000"
    environment:
      - NODE_ENV=production
      - MONGODB_URI=mongodb://mongo:27017/todoapp
      - REDIS_URL=redis://redis:6379
      - JWT_SECRET=${JWT_SECRET}
    depends_on:
      - mongo
      - redis
    restart: unless-stopped

  mongo:
    image: mongo:6
    volumes:
      - mongo_data:/data/db
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  mongo_data:
  redis_data:
```

## 4. CI Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    tags: ['v*']

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - run: corepack enable
      - run: pnpm install --frozen-lockfile
      - run: pnpm test
      - run: pnpm build

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.ref_name }}

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
      - uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.SSH_USER }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /opt/todo-app
            export TAG=${{ github.ref_name }}
            docker compose pull
            docker compose up -d
            sleep 10
            curl -f http://localhost:4000/health || (docker compose logs && exit 1)
```

## 5. 环境变量

```bash
# .env.production
NODE_ENV=production
MONGODB_URI=mongodb://mongo:27017/todoapp
REDIS_URL=redis://redis:6379
JWT_SECRET=<generated-32-bytes>
JWT_EXPIRES_IN=15m
REFRESH_TOKEN_EXPIRES_IN=7d
LOG_LEVEL=info
PORT=4000
```

## 6. 部署清单

### 部署前
- [ ] 所有测试通过
- [ ] 代码已合并到 main
- [ ] 版本号更新
- [ ] CHANGELOG 已写
- [ ] 数据库迁移已准备
- [ ] 密钥已轮换

### 部署中
- [ ] CI 全绿
- [ ] 镜像已推送到 ghcr.io
- [ ] 服务器拉取成功
- [ ] 容器启动无错误
- [ ] 健康检查通过

### 部署后
- [ ] 烟雾测试通过
- [ ] 监控指标正常
- [ ] 无新增告警
- [ ] 团队已通知

## 7. 回滚策略

```bash
# 服务器上回滚到上一个版本
cd /opt/todo-app
export TAG=v1.2.2  # 上一个稳定版本
docker compose pull
docker compose up -d
```

## 下一步

进入 [09-monitoring.md](09-monitoring.md) — 由 `observability` Skill 配置监控告警。