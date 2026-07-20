---
name: dependency-audit
description: 扫描依赖漏洞、分析影响面、产出修复与缓解方案
---

# Dependency Audit

对项目依赖做漏洞扫描与影响评估，产出修复优先级和具体动作。

## 何时使用

- 收到漏洞公告（CVE / GHSA）
- 周期性安全巡检
- 新引入依赖后的安全检查
- 大版本升级前确认漏洞状态

不要用于：

- 依赖引入与升级策略（用 `dependency-management`）
- 业务代码漏洞（用 `security`）

## 与「dependency-management」的区别

| 维度 | dependency-management | dependency-audit |
|------|----------------------|------------------|
| 视角 | 长期策略 | 一次性扫描 |
| 关注点 | 引入 / 升级 / 淘汰 | 漏洞与影响 |
| 频率 | 周期性 | 触发式 + 周期性 |

## 流程

### 1. 选择扫描工具

按生态：

| 生态 | 工具 |
|------|------|
| npm / Node | `npm audit` / `yarn audit` / Snyk |
| pip / Python | `pip-audit` / `safety` / Snyk |
| go | `govulncheck` |
| cargo / Rust | `cargo audit` |
| maven / JVM | OWASP Dependency-Check |
| 通用 | Dependabot / Renovate（持续监控） |

### 2. 执行扫描

- 全量扫描：`npm audit --json` 等
- 持续监控：Dependabot 在 GitHub 自动开 PR
- CI 集成：扫描失败阻断合并

### 3. 解析报告

每条漏洞关注：

| 维度 | 含义 |
|------|------|
| **CVE / GHSA ID** | 唯一标识 |
| **严重等级** | Critical / High / Medium / Low |
| **CVSS 评分** | 0-10 量化 |
| **影响范围** | 哪些版本受影响 |
| **利用条件** | 网络可达 / 需要认证 / 默认配置 |
| **修复版本** | 哪个版本开始修复 |
| **修复方式** | 升级 / 补丁 / 缓解配置 |

### 4. 影响面评估

不是所有漏洞都要立刻修：

- **依赖是否真被使用**：tree-shake 后是否还在
- **是否在暴露面**：生产 HTTP 服务 vs 仅 dev 工具
- **是否有兜底**：WAF / 鉴权 / 网络隔离
- **可利用性**：PoC 是否公开；实际利用难度

### 5. 决定响应

| 严重等级 | 默认响应时间 | 动作 |
|----------|--------------|------|
| Critical | 24h 内 | 必须修复（升级 / 替换 / 紧急缓解） |
| High | 7d 内 | 必须修复或缓解 |
| Medium | 30d 内 | 排入下个迭代 |
| Low | 下次巡检 | 记录，不阻塞 |

### 6. 执行修复

修复方式优先级：

1. **升级到修复版本**：最干净
2. **替换为替代库**：库不再维护时
3. **打补丁**：`patch-package` 等本地修改
4. **配置缓解**：临时禁功能、改配置
5. **网络隔离**：把服务挪到受限网络
6. **接受风险**：记录在案，监控利用迹象

## 输出格式

```markdown
# Dependency Audit Report

**扫描时间**：2026-07-20
**范围**：[包名范围 / lockfile 范围]
**工具**：[npm audit / Snyk / Dependabot]

## 总览
- 总依赖：N
- 漏洞：Critical X / High Y / Medium Z / Low W
- 直接依赖漏洞：A
- 传递依赖漏洞：B

## 必须立即处理（Critical）

### CVE-2026-12345：lodash prototype pollution
- 严重等级：Critical
- 影响：[production / dev / build]
- 路径：直接依赖 lodash@4.17.20
- 利用条件：HTTP 输入
- 修复版本：lodash@4.17.21
- 动作：升级并验证
- 负责人：[name]
- 截止：2026-07-21

## 本周处理（High）

### ...

## 下迭代处理（Medium）

### ...

## 风险接受

### CVE-XXX：xxx 库 XX 漏洞
- 理由：[不暴露在生产 / 不在调用路径]
- 接受人：[security owner]
- 监控：[日志 / 告警规则]

## 长期建议

- 引入 Dependabot 自动 PR
- 在 CI 跑 audit（失败阻断）
- 季度巡检纳入 release checklist
- 评估 [依赖] 是否需要替换
```

## 行为准则

- **Critical 不放过夜**：哪怕半夜叫人
- **知道不修要写理由**：风险接受要有 owner + 监控
- **CI 自动阻断**：避免漏洞合入主干
- **响应有 SLA**：明确每级的响应时间
- **定期复盘**：是否引入新漏洞 / 是否有同类依赖需要清查

## 不要做的事

- 不要忽略传递依赖的漏洞（占比往往最高）
- 不要在 lock 文件里手动改版本绕过
- 不要把 `npm audit fix --force` 当默认（会升 major）
- 不要只扫 production 依赖（dev 依赖也会被供应链攻击）
- 不要把漏洞修复拖到下个季度

## 与其它 Skill 的协作

- 漏洞需要整体替换库 → 用 `migration`
- 漏洞需要重写调用代码 → 用 `coding`
- 漏洞涉及业务代码安全 → 用 `security` 一起审
- 引入新依赖规避漏洞 → 用 `dependency-management` 决策