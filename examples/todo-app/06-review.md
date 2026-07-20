# 代码审查报告 - Todo App

**使用 Skill:** `review`

**输入:** [05-coding.md](05-coding.md)

**基线:** `main` 分支 vs `feat/todo-app-v1`

---

## 双轴审查

### Standards 轴（编码规范）

| 严重度 | 文件:行 | 问题 | 建议 |
|--------|---------|------|------|
| Major | `auth.service.ts:23` | 错误信息暴露数据库细节 | 用业务错误码代替 |
| Minor | `task.service.ts:45` | 复杂条件未拆函数 | 提取 `buildTaskFilter` |
| Nit | 多个文件 | 注释使用「// TODO」却没有 TODO 编号 | 改用 issue 编号 |

#### 详细分析

**S-001: 错误信息泄露内部结构**

- 当前：`throw new Error('Cast to ObjectId failed for value "xyz"')`
- 风险：暴露 ORM 类型，攻击者可探测接口
- 修复：用统一错误码 `INVALID_INPUT`

**S-002: N+1 风险**

- 位置：`task.service.ts:list` 方法
- 描述：循环调用 `populate` 可能在某些情况退化为 N+1
- 修复：检查 `.populate('categoryId', 'name color')` 是否生效

**S-003: 缺少 rate limit**

- 位置：`auth.routes.ts`
- 风险：登录接口可被暴力破解
- 修复：接入 `express-rate-limit`

### Spec 轴（需求符合度）

| 严重度 | 需求点 | 状态 | 备注 |
|--------|--------|------|------|
| ✅ | 用户注册 / 登录 | 完成 | - |
| ✅ | 任务的 CRUD | 完成 | - |
| ✅ | 任务分类 | 完成 | - |
| ⚠️ | 任务提醒（FR-005） | 部分 | 已建 job，未接 Web Notification |
| ❌ | 数据导出（FR-008，扩展功能） | 缺失 | 本期不做，但需在 README 说明 |

#### 详细分析

**需求 §5.3（性能）要求 P95 < 500ms：**

- 当前：未做压测
- 行动：交给 `performance` Skill

**需求 §6.1（验收标准 - 测试覆盖 ≥ 70%）：**

- 当前：仅核心模块有测试
- 缺口：services 层覆盖率约 45%
- 行动：交给 `testing` Skill

## 总结

- **Standards：** 1 Major / 1 Minor / 1 Nit
- **Spec：** 2 项需跟进
- **建议：** Major 项修复后即可合并；覆盖率与性能问题单独跟进

## 后续行动项

| ID | 内容 | 负责人 | Skill |
|----|------|--------|-------|
| A-001 | 修复错误信息泄露 | dev | `coding` |
| A-002 | 接入 rate limit | dev | `devops` |
| A-003 | 补齐 services 测试 | dev | `testing` |
| A-004 | P95 性能压测 | dev | `performance` |
| A-005 | 任务提醒 Web Notification | dev | `coding` + `document` |

## 下一步

进入 [07-testing.md](07-testing.md) — 由 `testing` Skill 补齐测试覆盖。