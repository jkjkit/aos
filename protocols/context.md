# Context Protocol

Version: v0.2.0

Status: Draft

---

# 1. Purpose

Context Protocol 定义上下文管理的标准规范。

本协议确保：

- 上下文使用高效
- 避免重复加载
- Token 消耗合理
- 信息传递准确

---

# 2. Definition

Context 是 Runtime 执行过程中的信息载体。

Context：

由 Runtime 管理。

遵循最小化原则。

支持模块间传递。

---

# 3. Responsibility

## 3.1 Runtime 职责

Runtime 负责：

- Context 初始化
- Context 维护
- Context 传递
- Context 清理

---

## 3.2 AOS 职责

AOS 负责：

- 定义 Context 规范
- 提供 Context 指导
- 不直接管理 Context

---

# 4. Context Types

## 4.1 User Context

用户提供的输入。

包括：

```
- 用户需求
- 文件路径
- 代码内容
- 配置参数
```

---

## 4.2 Skill Context

Skill 执行所需的上下文。

包括：

```
- Skill 定义
- 输入参数
- 前置条件
- 相关 Knowledge
```

---

## 4.3 Workflow Context

Workflow 执行的上下文。

包括：

```
- Workflow 定义
- 当前步骤
- 前序输出
- 执行状态
```

---

## 4.4 Execution Context

执行过程中的状态。

包括：

```
- 中间结果
- 临时数据
- 错误信息
- 执行日志
```

---

# 5. Context Lifecycle

## 5.1 初始化

```
用户输入
↓
解析需求
↓
初始化 Context
```

---

## 5.2 加载

```
识别所需能力
↓
按需加载 Skill
↓
加载相关 Knowledge
↓
扩展 Context
```

---

## 5.3 传递

```
Step 1 执行
↓
提取关键输出
↓
传递给 Step 2
↓
Step 2 执行
```

---

## 5.4 清理

```
任务完成
↓
清理临时数据
↓
保留必要结果
```

---

# 6. Minimization Principles

## 6.1 按需加载

只加载必需的内容。

```
✅ 
用户需要 Coding Skill
→ 只加载 coding/SKILL.md

❌ 
加载所有 Skills
```

---

## 6.2 增量加载

根据执行阶段逐步加载。

```
✅ 
Step 1 需要 Skill A → 加载 A
Step 2 需要 Skill B → 加载 B

❌ 
一次性加载所有 Skills
```

---

## 6.3 关键信息传递

只传递必要信息。

```
✅ 
Step 1 输出摘要 → Step 2

❌ 
Step 1 完整输出 + 所有中间数据 → Step 2
```

---

## 6.4 定期清理

清理不再需要的数据。

```
✅ 
Step 3 开始时清理 Step 1 的临时数据

❌ 
保留所有历史数据
```

---

# 7. Loading Strategy

## 7.1 Lazy Loading（推荐）

按需加载。

```
伪代码：

if 需要 Skill X:
    load Skill X
    execute
```

优点：

- Token 消耗低
- 加载速度快
- 灵活性高

---

## 7.2 Preloading（可选）

预加载已知需要的内容。

```
伪代码：

preload Workflow definition
for each step in workflow:
    preload skill definition
execute workflow
```

适用场景：

- Workflow 已知
- 步骤固定
- 希望提前验证

---

## 7.3 Caching（推荐）

缓存已加载内容。

```
伪代码：

cache = {}

function load_skill(name):
    if name in cache:
        return cache[name]
    content = read_file(name)
    cache[name] = content
    return content
```

优点：

- 避免重复读取
- 提升性能

---

# 8. Context Structure

## 8.1 推荐结构

```json
{
  "user_input": {
    "request": "用户需求",
    "files": ["文件列表"],
    "parameters": {}
  },
  "execution": {
    "current_skill": "当前 Skill",
    "current_step": "当前步骤",
    "status": "执行状态"
  },
  "results": {
    "step_1": "Step 1 输出摘要",
    "step_2": "Step 2 输出摘要"
  },
  "metadata": {
    "start_time": "开始时间",
    "token_count": "Token 数量"
  }
}
```

---

## 8.2 必需字段

```
- user_input: 用户输入
- execution: 执行状态
```

---

## 8.3 可选字段

```
- results: 中间结果
- metadata: 元数据
- cache: 缓存数据
- errors: 错误信息
```

---

# 9. Information Passing

## 9.1 完整传递

适用于：

- 信息量小
- 全部需要

```
Step 1 完整输出 → Step 2
```

---

## 9.2 摘要传递

适用于：

- 信息量大
- 只需摘要

```
Step 1 输出
↓
提取 Summary 部分
↓
传递给 Step 2
```

---

## 9.3 选择性传递

适用于：

- 信息量大
- 只需部分

```
Step 1 输出
↓
提取 Analysis.Issue 部分
↓
传递给 Step 2 (修复)
```

---

## 9.4 引用传递

适用于：

- 信息量巨大
- 避免重复

```
Step 1 输出保存为文件
↓
传递文件路径给 Step 2
↓
Step 2 按需读取
```

---

# 10. Token Management

## 10.1 Token 预算

设定 Token 预算：

```
Total Budget: 100k tokens

- User Input: 10k
- Skill Loading: 20k
- Execution: 60k
- Output: 10k
```

---

## 10.2 Token 监控

监控 Token 使用：

```
Current: 45k / 100k
Remaining: 55k
```

---

## 10.3 Token 优化

优化策略：

```
1. 压缩中间结果
2. 清理无用数据
3. 使用引用而非复制
4. 缓存重复内容
```

---

# 11. Caching Strategy

## 11.1 缓存内容

推荐缓存：

```
- Skill 定义（变化少）
- Workflow 定义（变化少）
- Knowledge 内容（变化少）
- Template 内容（变化少）
```

不推荐缓存：

```
- 用户输入（每次不同）
- 执行结果（动态生成）
- 临时数据（一次性）
```

---

## 11.2 缓存失效

缓存失效条件：

```
- 文件内容变更
- 版本更新
- 手动清理
- 超时失效
```

---

## 11.3 缓存策略

```
伪代码：

cache_ttl = 3600  # 1 小时

function load_with_cache(path):
    cache_key = path + file_hash(path)
    
    if cache_key in cache and not expired:
        return cache[cache_key]
    
    content = read_file(path)
    cache[cache_key] = {
        "content": content,
        "timestamp": now()
    }
    
    return content
```

---

# 12. Error Context

## 12.1 错误信息

发生错误时记录：

```json
{
  "error": {
    "type": "FileNotFoundError",
    "message": "Skill not found",
    "skill": "non-existent-skill",
    "timestamp": "2026-07-19T10:00:00Z",
    "context": {
      "user_input": "...",
      "current_step": "Step 2",
      "previous_output": "..."
    }
  }
}
```

---

## 12.2 错误恢复

提供足够信息用于恢复：

```
- 错误发生点
- 已完成步骤
- 中间结果
- 恢复建议
```

---

# 13. Workflow Context

## 13.1 步骤追踪

```json
{
  "workflow": "new-feature",
  "steps": [
    {
      "step": 1,
      "skill": "requirement",
      "status": "completed",
      "output_summary": "需求分析完成"
    },
    {
      "step": 2,
      "skill": "design",
      "status": "in_progress",
      "output_summary": null
    }
  ]
}
```

---

## 13.2 依赖追踪

```json
{
  "step": 3,
  "skill": "coding",
  "dependencies": {
    "requirement_output": "来自 Step 1",
    "design_output": "来自 Step 2"
  }
}
```

---

# 14. Multi-Runtime Support

## 14.1 Runtime 差异

不同 Runtime 可能：

- 使用不同的 Context 结构
- 采用不同的管理策略
- 有不同的优化方法

---

## 14.2 统一原则

AOS 只定义原则：

```
- 最小化
- 按需加载
- 增量加载
- 缓存优化
```

具体实现由 Runtime 决定。

---

# 15. Best Practices

## 15.1 最小化加载

```
✅ 只加载需要的内容
❌ 加载所有内容
```

---

## 15.2 智能缓存

```
✅ 缓存不变内容
❌ 缓存所有内容
```

---

## 15.3 及时清理

```
✅ 完成后清理临时数据
❌ 无限制累积
```

---

## 15.4 信息压缩

```
✅ 传递摘要而非全文
❌ 重复传递大量数据
```

---

# 16. Anti-Patterns

## 16.1 一次性加载所有内容

```
❌ 
启动时：
- 加载所有 Skills
- 加载所有 Workflows
- 加载所有 Knowledge
- 加载所有 Templates

Token 消耗巨大
```

---

## 16.2 无限制传递

```
❌ 
Step 1 → Step 2 → Step 3

每个 Step 携带所有历史数据

Context 不断膨胀
```

---

## 16.3 无缓存策略

```
❌ 
每次执行：
- 重新读取 Skill 定义
- 重新解析内容
- 重新加载 Knowledge

浪费 Token 和时间
```

---

## 16.4 过度缓存

```
❌ 
缓存所有内容：
- 用户输入
- 执行结果
- 临时数据

导致缓存污染
```

---

# 17. Monitoring

## 17.1 监控指标

```
- Total Token Count
- Context Size
- Cache Hit Rate
- Loading Time
- Execution Time
```

---

## 17.2 日志记录

```
[INFO] Loading Skill: coding
[INFO] Cache Hit: workflow/new-feature
[INFO] Context Size: 45k tokens
[WARN] Context Size > 80% of budget
```

---

# 18. Optimization

## 18.1 压缩策略

```
1. 移除注释和空行
2. 使用摘要替代全文
3. 引用替代复制
4. 延迟加载详细内容
```

---

## 18.2 分区策略

```
Context 分为：

Hot Zone: 当前使用（内存）
Warm Zone: 近期使用（缓存）
Cold Zone: 可能使用（磁盘）
```

---

## 18.3 优先级策略

```
High Priority:
- 用户输入
- 当前 Skill 定义
- 当前步骤输出

Low Priority:
- 历史执行日志
- 调试信息
- 详细 metadata
```

---

# 19. Examples

## 19.1 简单场景

```
User: "写一个登录功能"

Context:
{
  "user_input": {
    "request": "写一个登录功能"
  },
  "execution": {
    "skill": "coding"
  }
}

加载:
- skills/coding/SKILL.md

Token: ~5k
```

---

## 19.2 Workflow 场景

```
User: "开发新功能：用户认证"

Context:
{
  "user_input": {
    "request": "开发新功能：用户认证"
  },
  "execution": {
    "workflow": "new-feature",
    "current_step": 1
  }
}

加载:
- workflows/new-feature/WORKFLOW.md
- skills/requirement/SKILL.md (Step 1)

执行 Step 1 后:
{
  "results": {
    "step_1": "需求分析完成，识别出 3 个核心功能"
  },
  "execution": {
    "current_step": 2
  }
}

加载:
- skills/design/SKILL.md (Step 2)

Token: 累计 ~20k
```

---

## 19.3 复杂场景

```
User: "基于需求文档开发新功能"

Context:
{
  "user_input": {
    "request": "开发新功能",
    "files": ["requirements.md"]
  },
  "execution": {
    "workflow": "new-feature"
  }
}

加载顺序:
1. requirements.md (15k tokens)
2. workflows/new-feature/WORKFLOW.md (2k)
3. skills/design/SKILL.md (3k) - Step 1
4. knowledge/coding-style/content.md (5k) - Step 2 需要
5. skills/coding/SKILL.md (4k) - Step 2
6. skills/review/SKILL.md (3k) - Step 3

优化:
- requirements.md 读取后生成摘要 (1k)
- 传递摘要而非全文
- Skill 定义缓存
- Knowledge 按需加载部分内容

优化后 Token: ~50k (vs 原始 ~100k)
```

---

# 20. Validation

## 20.1 Context 健康检查

- [ ] Context 大小合理
- [ ] 无重复内容
- [ ] 缓存命中率高
- [ ] Token 使用在预算内
- [ ] 加载时间合理

---

## 20.2 优化检查

- [ ] 使用按需加载
- [ ] 实现缓存策略
- [ ] 及时清理临时数据
- [ ] 传递摘要而非全文
- [ ] 监控 Token 使用
