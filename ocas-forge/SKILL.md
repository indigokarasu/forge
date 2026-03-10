---
name: ocas-forge
description: >
  Skill architect and builder. Designs, builds, and validates complete
  Agent Skill packages through a mandatory six-phase pipeline. Default
  output is the finished installable package.
---

# Forge

Forge builds complete, installable Agent Skill packages. Given a capability idea or existing package, it runs a mandatory internal pipeline and returns the finished package.

Default output: the finished package with full file contents. Not a design brief.

## When to use

- Create a new Agent Skill from a goal or capability description
- Review or critique an existing skill package
- Repair broken or defective skill packages
- Classify whether a proposed capability deserves to be a skill
- Validate a skill package against OCAS standards

## When not to use

- Evaluating skill performance — use Mentor
- Running or orchestrating skills — use Mentor
- Web research — use Sift
- Building non-skill artifacts

## Core promise

One command, one finished installable skill package. Mandatory design pipeline ensures quality. No plans instead of packages.

## Commands

- `forge.build` — design, scope, build, and validate a complete skill package
- `forge.critique` — review a package and identify defects
- `forge.repair` — fix broken files in an existing package
- `forge.classify` — classify a proposed skill (shortcut, workflow, system)
- `forge.validate` — run validation checks on a package
- `forge.scaffold` — generate a minimal package skeleton
- `forge.status` — current build state if multi-step build in progress

## Mandatory design pipeline

Run all phases before writing files:

1. **Existence gate** — Is this better as a skill than a one-off prompt?
2. **Classify** — Shortcut, workflow, or system?
3. **Scope** — Exact job, explicit non-goals, smallest useful promise
4. **Architecture** — What goes in SKILL.md vs references vs scripts vs assets?
5. **Build** — Write all files
6. **Validate** — Routing, structural, usefulness checks

## Skill type classification

- **Shortcut** — narrow tool wrapper. 20-120 line SKILL.md.
- **Workflow** — multi-step process. 80-250 line SKILL.md.
- **System** — durable behavior system. 150-300 line SKILL.md, deeper material in references.

## Package rules

Minimum package: skill.json + SKILL.md. Add references/, scripts/, assets/ only when justified.

Read `references/authoring_rules.md` for full authoring standards.
Read `references/package_patterns.md` for package shape guidance by type.
Read `references/examples.md` for good and bad examples.

## Anti-patterns to reject

- Vague or overly broad scope
- Generic descriptions that don't route well
- SKILL.md bloated with background explanation
- Support folders created for aesthetics
- Plans returned instead of packages
- Template residue and placeholders

## Support file map

- `references/authoring_rules.md` — durable authoring rules for quality skill packages
- `references/package_patterns.md` — common package shapes by skill type
- `references/examples.md` — good descriptions, package patterns, anti-patterns

## Storage layout

```
.forge/
  config.json
  build_log.jsonl
  decisions.jsonl
```

## Validation rules

- SKILL.md starts with valid YAML frontmatter on line 1
- skill.json is valid JSON with required fields
- Description routes correctly for trigger and non-trigger cases
- No empty support directories
- No placeholder text remaining
