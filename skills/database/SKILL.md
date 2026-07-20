---
name: database
description: 设计或变更数据模型、Migration、索引和查询方案；不负责系统总体架构或业务代码实现
---

# Database

负责数据建模、Schema 设计、Migration 编写与查询 / 索引优化。

## 何时使用

- 新业务需要建模
- 老表结构要调整
- 慢查询需要分析
- 需要评审现有 Schema

不要用于：

- 业务需求还没清楚（先 requirement）
- 仅查询优化中的 SQL 改写建议（属于 performance）

## 流程

1. **梳理业务实体**：生命周期、关系（一对一 / 一对多 / 多对多）
2. **识别访问模式**：主要查询条件、排序、JOIN 路径
3. **设计模型**：表、字段、主键、外键、约束、审计字段
4. **规划索引**：为高频查询建索引；避免在大量写入表上过度索引
5. **写 Schema / Migration**：可执行的 DDL，向后兼容；高风险变更提供回滚
6. **验证**：用 EXPLAIN 跑核心查询；填入估算数据量级做基线
7. **输出设计文档**：表 + 关系 + 索引 + 风险

## 输出格式

```markdown
# Database Design

## 实体
### <entity>
- 字段：...
- 主键：...
- 外键：...
- 索引：...

## 关系
- A (1) → (N) B
- ...

## Migration
### 001_<action>.sql
```sql
[DDL]
```

## 索引
- idx_<table>_<col>：[purpose]

## 风险与权衡
- [破坏性变更 / 锁表风险 / 回滚方案]
```

## 命名规范（默认）

- 表名：复数小写下划线（`users`、`order_items`）
- 列名：小写下划线（`created_at`）
- Boolean：`is_` / `has_` 前缀
- 外键：`<table_singular>_id`
- 时间戳：`created_at` / `updated_at` / `deleted_at`，类型 `TIMESTAMPTZ`
- 主键：`id`，UUID 或自增（团队约定）

## 行为准则

- **Migration 永远向后兼容**：先加后删；列加默认值；不删还在用的列
- **回滚方案**：每个破坏性变更必须能回退
- **索引有理由**：列出每个索引对应的查询路径
- **审计字段**：几乎每张表都加 `created_at` / `updated_at`

## 不要做的事

- 不要执行生产 DDL——只产出脚本与建议
- 不要在事务里做可能锁表的大批量修改
- 不要把金额存成 FLOAT
- 不要用字符串存日期
