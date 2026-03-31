# Forge Package Patterns

## Shortcut
```
ocas-{name}/
  skill.json
  SKILL.md
```
SKILL.md: 20-120 lines. Quick actions, inputs, caveats.

## Workflow
```
ocas-{name}/
  skill.json
  SKILL.md
  references/
    schemas.md (if needed)
```
SKILL.md: 80-250 lines. Trigger, inputs, workflow, outputs, boundaries.

## System
```
ocas-{name}/
  skill.json
  SKILL.md
  references/
    schemas.md
    {domain_detail}.md
    journal.md
    plans/
      {plan_id}.plan.md  (if skill has bundled workflow plans)
  scripts/ (if needed)
  assets/ (if needed)
```
SKILL.md: 150-300 lines. Trigger, purpose, decision model, execution loop, support file map, validation.

## System Skill Required Sections (SKILL.md)
1. Responsibility boundary
2. Ontology types
3. Commands
4. [domain-specific workflow sections]
5. Optional skill cooperation
6. Journal outputs
7. Storage layout
8. OKRs
9. Initialization
10. Background tasks (omit if purely reactive)
11. Support file map
12. Update command

## references/plans/ convention
Plans follow `spec-ocas-workflow-plans.md` format.
Filename must match plan_id: `{plan_id}.plan.md`.
Init command must copy plans to ~/openclaw/data/ocas-mentor/plans/ (skip existing).
