# AOS Feedback System

> AOS 的观察层——记录 Skill 使用数据，让 AOS 具备「自我演化」的基础。不违反 Stable Core 哲学：观察层不进 Skill 目录，不改写 Skill 本身。

---

## 1. 设计原则

AOS 是「描述性的、静态的」。Feedback System 引入的是「观察层」，与静态层严格分离：

| 层 | 位置 | 性质 | 演进 |
|---|---|---|---|
| **静态层** | `~/.agents/skills/`, `~/.agents/workflows/`, `~/.agents/protocols/` | 协议、能力定义 | 随 AOS 版本演进 |
| **观察层** | `~/.agents/feedback/`, `~/.agents/health-report.md` | 使用数据、效果评分 | 随用户使用演进 |

**关键约束：**

- 观察层**不进** Skill 目录——守住 Stable Core
- 观察层**不依赖** Runtime hooks——守住 Runtime Agnostic
- 观察层**不自动改写** Skill——守住 Single Responsibility
- 数据格式**简单固定**——守住 Convention Over Configuration
- 报告输出 **Markdown**——守住 Human Readable

## 2. 数据目录

```
~/.agents/feedback/
├── coding.json
├── review.json
├── design.json
└── ...               ← 每个 Skill 一个 JSON 文件
```

**不进 git**——每个用户的反馈数据独立。

## 3. JSON Schema

```json
{
  "skill": "coding",
  "schema_version": "0.1",
  "created_at": "2026-07-20",
  "updated_at": "2026-07-20",
  "stats": {
    "total_calls": 23,
    "first_match_count": 18,
    "rework_count": 3
  },
  "ratings": {
    "useful": 18,
    "needs_improvement": 3,
    "outdated": 1,
    "mislabeled": 1
  },
  "feedback": [
    {
      "date": "2026-07-20",
      "rating": "useful",
      "note": "清晰的步骤和示例",
      "context": "实现用户认证模块"
    }
  ]
}
```

### 字段定义

| 字段 | 必填 | 类型 | 说明 |
|---|---|---|---|
| `skill` | ✓ | string | Skill 名（与目录名一致） |
| `schema_version` | ✓ | string | 当前 "0.1" |
| `created_at` | ✓ | ISO date | 首次反馈日期 |
| `updated_at` | ✓ | ISO date | 最近更新日期 |
| `stats.total_calls` | ✓ | int | 总调用次数 |
| `stats.first_match_count` | ✓ | int | Runtime 首次匹配成功的次数 |
| `stats.rework_count` | ✓ | int | 用户返工的次数 |
| `ratings.useful` | ✓ | int | 标记为「有用」的次数 |
| `ratings.needs_improvement` | ✓ | int | 标记为「需要改进」的次数 |
| `ratings.outdated` | ✓ | int | 标记为「过时」的次数 |
| `ratings.mislabeled` | ✓ | int | 标记为「描述不准确」的次数 |
| `feedback[]` | - | array | 最近反馈明细，最多保留 50 条 |

### Rating 语义

| Rating | 含义 |
|---|---|
| `useful` | Skill 解决了问题 |
| `needs-improvement` | 解决了但有改进空间（描述不清 / 步骤缺失 / 示例不够） |
| `outdated` | Skill 内容已过时（工具 / 库 / 规范变了） |
| `mislabeled` | Skill 描述与实际能力不符（Runtime 调错了） |

### 计算指标

```
useful_rate = ratings.useful / total_calls
first_match_rate = stats.first_match_count / total_calls
rework_rate = stats.rework_count / total_calls
```

## 4. CLI 命令

### 记录反馈

```bash
aos feedback <skill> --rating <useful|needs-improvement|outdated|mislabeled> [--note "..."] [--context "..."]
```

示例：

```bash
aos feedback coding --rating useful --note "步骤清晰" --context "用户认证模块"
aos feedback design --rating mislabeled --note "和 coding 调混了"
aos feedback review --rating needs-improvement --note "示例不够"
```

### 标记首次匹配 / 返工

```bash
aos feedback <skill> --first-match   # Runtime 一次调对了
aos feedback <skill> --rework        # 用户又改了一轮
```

### 初始化 Skill 的反馈文件

```bash
aos feedback <skill> --init
```

不存在时自动创建空文件。

### 查看单个 Skill 的反馈

```bash
aos feedback <skill> --show
```

### 生成健康度报告

```bash
aos health
```

输出 `~/.agents/health-report.md`。

## 5. 健康度报告

`~/.agents/health-report.md` 自动生成，包含：

```markdown
# AOS Skill 健康度报告

生成时间：2026-07-20

## 总览
- 总调用次数：234
- 整体有用率：87%
- 首次匹配率：78%
- 整体返工率：13%

## Skill 健康度（按调用次数排序）

| Skill | 调用 | 有用率 | 首次匹配 | 返工率 | 状态 |
|-------|------|--------|----------|--------|------|
| coding | 45 | 89% | 91% | 9% | ✅ 健康 |
| review | 38 | 92% | 84% | 8% | ✅ 健康 |
| design | 12 | 67% | 50% | 25% | ⚠️ 关注 |

## 需要关注的 Skill

### design
- 有用率：67%（低于 75%）
- 首次匹配率：50%（说明 description 不够精准）
- 最近反馈：
  - "和 coding 调混了"（mislabeled）
  - "用户分不清 design 和 design-interface"（mislabeled）

**改进建议：**
- 收窄 description 的触发场景
- 区分 design 与 design-interface 的边界

### debug
- ...

## 长期建议
- 每季度 review 一次低有用率 Skill
- 高频低匹配的 Skill 优先改写 description
- 收集 30+ 反馈后再下结论
```

## 6. 不做的事（守住边界）

- ❌ 不自动改写 Skill（必须人工审核）
- ❌ 不上传反馈到任何远端
- ❌ 不依赖 Runtime hooks
- ❌ 不收集 PII（个人信息）
- ❌ 不删除反馈历史（只追加）
- ❌ 不强制用户反馈（完全自愿）

## 7. 隐私与所有权

- 数据**只存在本地** `~/.agents/feedback/`
- **不进 git**（在 `.gitignore` 里）
- **不上传**到任何服务端
- 用户可随时删除

## 8. 演化流程

```
收集反馈（用户主动）
       ↓
生成报告（aos health）
       ↓
人工 review 报告
       ↓
人工改写 Skill（SKILL.md）
       ↓
观察新版本的指标变化
       ↓
循环
```

**关键：所有演化动作都是人工的，反馈只是提供数据。**

## 9. 实施脚本

| 脚本 | 用途 |
|---|---|
| `scripts/aos-feedback.sh` | Linux / macOS / Git Bash |
| `scripts/aos-feedback.ps1` | Windows PowerShell |
| `scripts/skill-health-report.sh` | 生成报告（Linux） |
| `scripts/skill-health-report.ps1` | 生成报告（Windows） |

## 10. 与 AOS 哲学的一致性

| 原则 | 一致性 |
|---|---|
| Runtime Agnostic | ✅ 用 CLI，不依赖 Runtime |
| Stable Core | ✅ 反馈不进 Skill 目录 |
| Single Responsibility | ✅ 不自动改写 Skill |
| Convention Over Configuration | ✅ JSON schema 固定 |
| Human Readable | ✅ 报告是 Markdown |
| Evolution | ✅ 补齐 AOS 自我演化能力 |
| Long-term Maintainability | ✅ 数据驱动维护决策 |

反馈系统是 AOS 哲学的**延伸**，不是违背。