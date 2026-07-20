# AOS - Agent Operating System

## Root

`~/.agents/`

## Progressive Loading

按需加载，禁止预加载完整能力目录。

1. 先判断用户当前要求的最终交付物。
2. 如果 Runtime 已提供 Available Skills，直接根据 `name + description` 选择职责最具体的能力。
3. 只有候选无法唯一确定时，才读取 `~/.agents/ROUTER.md`。
4. 确定 Skill 后，只读取 `~/.agents/skills/<name>/SKILL.md`。
5. 请求明确横跨多个阶段时，读取对应 `~/.agents/workflows/<name>/WORKFLOW.md`，再按阶段加载 Skill。
6. `MANIFEST.md` 仅用于能力发现、维护和排障；日常请求不要读取。
7. `knowledge/` 与 `templates/` 仅在已选 Skill 或 Workflow 明确需要时加载。

## Routing Rules

- 按最终交付物匹配，不按孤立关键词匹配。
- 专用 Skill 优先于通用 Skill；单阶段只选一个主 Skill。
- 不为“保险”读取所有候选 `SKILL.md`。
- 只有交付物确实无法从上下文判断时才询问用户。

## Locations

- Skills: `~/.agents/skills/`
- Workflows: `~/.agents/workflows/`
- Router: `~/.agents/ROUTER.md`
- Full catalog: `~/.agents/MANIFEST.md`
- Knowledge: `~/.agents/knowledge/`
- Templates: `~/.agents/templates/`

## Protocol Version

AOS v0.2.0