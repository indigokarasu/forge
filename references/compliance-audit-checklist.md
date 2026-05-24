# OCAS Skill Compliance Audit Checklist

## Purpose

Use this checklist when auditing an existing OCAS skill package for architecture compliance. This is the standard gate before publishing or syncing a skill to GitHub.

## File Inventory

Every OCAS skill package must contain these files:

| File | Required | Purpose |
|---|---|---|
| `SKILL.md` | Yes | Operational frontmatter + skill body |
| `README.md` | Yes | Human-readable overview |
| `CHANGELOG.md` | Yes | Version history |
| `skill.json` | Yes | Machine-readable metadata + self-update config |
| `.gitignore` | Yes | Exclude artifacts from git |
| `evals.json` | Yes | Evaluation test cases |

Optional (add only when justified):
- `references/*.md` — session-specific detail, schemas, domain knowledge
- `scripts/*.py/*.sh` — deterministic actions the skill invokes
- `templates/*` — starter files meant to be copied and modified
- `assets/*` — reusable operational artifacts
- `evals/evals.json` — duplicate of root evals.json for package discoverability

## Frontmatter Checklist

SKILL.md YAML frontmatter must include:

- [ ] `name` — hyphenated skill identifier
- [ ] `description` — routing logic with trigger phrases, includes "Not for" exclusions
- [ ] `license` — `MIT` for OCAS skills
- [ ] `metadata.author` — `Indigo Karasu`
- [ ] `metadata.email` — `mx.indigo.karasu@gmail.com`
- [ ] `metadata.version` — semver string (e.g. `"1.1.0"`)
- [ ] `metadata.tags` — list of lowercase tags
- [ ] `metadata.category` — skill category (`ocas`, `infrastructure`, `workflow`, etc.)

## Required SKILL.md Sections

### All Skills

1. **Title** — `# Skill Name — Short Description`
2. **When to use** — concrete trigger conditions
3. **When NOT to use** — explicit exclusions with pointers to other skills
4. **Responsibility Boundary** — what this skill owns, what it does NOT own
5. **Main content** — workflow, commands, configuration
6. **Ontology Types** — declare entity extraction + Signal emission behavior (or explicitly state "does not extract entities / does not emit Signals")
7. **Journal Outputs** — which journal type(s) emitted (Observation, Action, Research), file path pattern
8. **Storage Layout** — `{agent_root}/commons/data/{skill-id}/` and `{agent_root}/commons/journals/{skill-id}/` paths
9. **OKRs** — at least one objective with key results and targets
10. **Background Tasks** — cron jobs and heartbeat entries (omit entirely if purely reactive)
11. **Pitfalls** — known issues, edge cases, gotchas
12. **Support File Map** — table of all `references/` files with one-line descriptions

### System Skills (additional)

13. **Commands** — list of invocable commands
14. **Initialization** — first-run setup steps (create directories, write empty files, register jobs)
15. **Self-update** — `self.update` procedure from GitHub source
16. **Optional Skill Cooperation** — other skills this cooperates with

## skill.json Checklist

```json
{
  "name": "ocas-{skill}",
  "version": "X.Y.Z",
  "description": "...",
  "author": "Indigo Karasu",
  "email": "mx.indigo.karasu@gmail.com",
  "skill_type": "shortcut|workflow|system",
  "filesystem": {
    "read": ["{agent_root}/commons/data/{skill-id}/"],
    "write": ["{agent_root}/commons/data/{skill-id}/"]
  },
  "self_update": {
    "source": "https://github.com/indigokarasu/{repo}",
    "mechanism": "version-checked tarball from GitHub via gh CLI",
    "command": "{skill}.update",
    "requires_binaries": ["gh", "tar", "..."]
  }
}
```

## README.md Checklist

- [ ] Title matching skill name
- [ ] One-line description
- [ ] Overview paragraph
- [ ] Commands list
- [ ] Dependencies
- [ ] Scheduled tasks (if any)
- [ ] Link to CHANGELOG.md

## CHANGELOG.md Checklist

- [ ] Follows semver
- [ ] Dated entries (ISO 8601)
- [ ] Grouped by version: `### Added`, `### Changed`, `### Fixed`, `### Removed`
- [ ] Newest first

## .gitignore Checklist

Exclude at minimum:
- Language artifacts: `__pycache__/`, `*.pyc`, `*.pyo`, `*.pyd`, `*.so`
- Environment: `.env`, `.env.local`, `venv/`, `.venv/`
- OS: `.DS_Store`
- Logs: `*.log`, `*.tmp`

## SKILL.md Body Guidelines (authoring_rules.md Section 8)

- Shortcut skills: 20-120 lines
- Workflow skills: 80-250 lines
- System skills: 150-300 lines
- Code ratio under 15% (fenced-block lines ÷ total lines)
- Under 500 lines absolute maximum
- Extract SQL DDL, Python examples, JSON schemas, default configs, OKR YAML, cron bash, self-update bash into `references/` files
- Replace extracted blocks with one-line pointers

## Required SKILL.md Sections for System Skills (authoring_rules.md end)

System skills must explicitly include:
1. Responsibility boundary
2. Ontology types
3. Commands
4. Domain-specific workflow sections
5. Optional skill cooperation
6. Journal outputs
7. Storage layout (point to `references/config-default.json` for config structure)
8. OKRs
9. Initialization
10. Background tasks (omit if purely reactive)
11. Support file map
12. Self-update command

## GitHub Sync Checklist

- [ ] `gh repo create indigokarasu/{repo} --private --description "..."`
- [ ] `git init` (if no repo) or verify existing remote
- [ ] `git remote add origin https://github.com/indigokarasu/{repo}.git`
- [ ] `git add -A && git commit -m "..."` with conventional commit message
- [ ] `git branch -m main && git push -u origin main`
- [ ] Verify: `gh repo view indigokarasu/{repo} --json visibility` → `PRIVATE`

## Audit Workflow

1. Read SKILL.md — check frontmatter + all required sections
2. Check file inventory — all required files present
3. Check references — every file in `references/` is referenced from SKILL.md
4. Check skill.json — valid JSON, ConfigBase fields, self_update configured
5. Check .gitignore — minimum excludes present
6. Check evals.json — at least 2 eval cases with expected skills_loaded
7. Apply fixes (add missing files, sections, metadata)
8. Create GitHub repo if needed, push
9. Verify push succeeded and repo is private
