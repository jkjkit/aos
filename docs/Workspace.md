# AOS Workspace Convention

## Purpose

Keep AOS separate from business projects. AOS provides shared Skills, Workflows, and deployment scripts; every business project keeps its own source code, dependencies, and Git history.

## Recommended layout

```text
D:\AOS/                 # AOS source repository or maintenance directory
D:\Work/                # Project container only; not a Git repository
|-- Project-1/            # A real project; its own Git repository
|-- Project-2/            # Another real project; its own Git repository
`-- ...

~/.agents/               # Shared AOS runtime files deployed from D:\AOS
```

## Ownership boundaries

| Location | Put here | Do not put here |
|---|---|---|
| `D:\AOS` | AOS source, Skills, Workflows, deployment, and maintenance documentation | Business projects or their build artifacts |
| `D:\Work\Project-*` | Business code, dependencies, project tests, and project documentation | Copied AOS shared-capability source |
| `~/.agents` | Shared runtime files maintained by the AOS deployment scripts | Business-project source code |

## Daily workflow

1. Maintain AOS in `D:\AOS` and run its deployment script to update `~/.agents`.
2. Enter the real project before working:

   ```powershell
   Set-Location D:\Work\Project-1
   ```

3. Run Git, package management, builds, tests, and Agents from that project directory.
4. Add a short `AGENTS.md` in a project root only if the project has special constraints, such as its tech stack, test command, or release restrictions.

## Minimal project-level `AGENTS.md`

```md
# Project-1

- Run `npm test` before submitting changes.
- Update migrations before changing database models.
- Do not commit `.env` files.
```

This file describes only project-specific rules. Shared AOS capabilities still come from `~/.agents`, so they do not need to be copied into every project.

## Four rules that prevent confusion

- Do not initialize `D:\Work` as one umbrella Git repository.
- Do not create business project directories inside `D:\AOS`.
- Do not run a business project's build or tests from `D:\AOS`.
- Do not copy AOS-wide `AGENTS.md` or `CLAUDE.md` files into business projects; keep only project-specific additions there.
