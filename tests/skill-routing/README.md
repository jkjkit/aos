# Skill Routing Regression Tests

这套测试用于防止新增或修改 Skill 后，Runtime 再次出现职责重叠和匹配退化。

## 文件

- `cases.json`：真实用户表达、预期 Skill / Workflow、易混淆候选和判断理由
- `scripts/test-skill-routing.py`：静态契约校验与 Runtime 预测评分器

当前语料包含：

- 66 条 Skill 用例
- 5 条 Workflow 用例
- 33 个高混淆 Skill，每个至少 2 条用例
- 5 个 Workflow，每个至少 1 条用例

## 静态回归

Windows：

```powershell
.\scripts\test-skill-routing.ps1
```

macOS / Linux：

```bash
bash scripts/test-skill-routing.sh
```

也可以直接执行：

```bash
python scripts/test-skill-routing.py
```

静态检查会验证：

- 用例 ID 和用户表达没有重复
- 预期 Skill / Workflow 确实存在
- 高混淆 Skill 已登记在 `data/skill-routing.json`
- 每条 Skill 用例至少包含一个同组易混淆候选
- 每个路由 Skill 和 Workflow 都达到最低用例覆盖
- `MANIFEST.md` 包含全部 Skill，且不再承载 Runtime 快速路由
- `ROUTER.md` 与默认 Profile Router 完全一致
- `routers/*.md` 只包含各 Profile 激活的路由 Skill，并覆盖全部 Workflow

## 测试真实 Runtime 的决策

先生成不包含预期答案的盲测输入，以及空预测模板：

```powershell
python .\scripts\test-skill-routing.py --write-eval .\tmp\routing-eval.json
python .\scripts\test-skill-routing.py --write-template .\tmp\routing-predictions.json
```

把 `routing-eval.json` 交给待测试 Runtime。Runtime 应独立处理每条 `input`，并把选择结果填入预测模板：

```json
{
  "design-01": "design",
  "workflow-bug-fix-01": "bug-fix"
}
```

也支持显式类型：

```json
{
  "design-01": {
    "kind": "skill",
    "name": "design"
  },
  "workflow-bug-fix-01": {
    "kind": "workflow",
    "name": "bug-fix"
  }
}
```

最后评分：

```powershell
python .\scripts\test-skill-routing.py --predictions .\tmp\routing-predictions.json
```

测试会输出：

- 总体准确率
- Skill 和 Workflow 分项准确率
- 缺失或多余的用例 ID
- 每条失败用例的预期值和实际值
- 最常见的混淆方向

默认回归标准是全部用例精确匹配；存在缺失、未知 ID 或错误匹配时退出码为 1。

## 新增用例规则

每条用例包含：

```json
{
  "id": "design-01",
  "input": "设计多租户权限系统的服务边界、组件关系和关键调用链。",
  "expected": {
    "kind": "skill",
    "name": "design"
  },
  "confusable_with": [
    "design-interface",
    "api-design",
    "coding"
  ],
  "reason": "要求的是系统架构和组件边界。"
}
```

要求：

1. 一条用例只表达一个主要交付物；多阶段请求应指向 Workflow。
2. 使用接近真实用户的自然表达，不要直接说“请调用 design Skill”。
3. `confusable_with` 至少包含一个同路由组的相邻 Skill。
4. 不要通过堆砌唯一关键词让答案变得显而易见。
5. 修复一次真实误匹配后，至少补一条能够复现该问题的回归用例。