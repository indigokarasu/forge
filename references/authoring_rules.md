# Forge Authoring Rules

Reference: `ocas-skill-authoring-rules.md` v2.4.0

## Core Rules
1. A skill must earn its existence — repeated, durable, worth maintaining
2. Every skill needs one sharp promise — "This skill exists to ______"
3. Routing comes first — description is routing logic, not branding
4. SKILL.md is the operational surface — not a tutorial or README
5. Match specificity to failure risk — exact where drift is costly
6. Add complexity only when justified — start minimal

## Responsibility Boundaries
Every new skill must verify it does not conflict with: Scout, Sift, Praxis, Dispatch, Corvus, Mentor, Elephas, Weave, Taste, Voyage, Look, Rally, Relay, Vesper, Forge, Fellow, Thread, Custodian.

## Atomic Skill Principle
Skills perform one clear role. They may cooperate but must never depend on other skills. If a cooperating skill is absent, the skill functions normally.

## Required Structural Sections (System Skills)
Responsibility Boundary, Ontology Types, Optional Skill Cooperation, Journal Outputs, Storage Layout (with ~/openclaw/ paths), Visibility, OKRs (universal + skill-specific), Background Tasks (if applicable).

## Ontology Mapping (Required)
Every system skill must declare which entity types from `spec-ocas-ontology.md` it extracts, manages, or queries. Include a `## Ontology types` section after `## Responsibility boundary`. See `spec-ocas-ontology.md` Skill Entity Extraction Ownership table.

Skills that extract no entities and query none must still include a brief statement: "This skill does not extract entities and does not emit Signals to Elephas."

## Storage Convention
All data under ~/openclaw/data/ocas-{skill}/ and journals under ~/openclaw/journals/ocas-{skill}/. No data inside skill packages.

LadybugDB skills: ~/openclaw/db/ocas-{skill}/

## Journal Convention
Every run writes a journal. journal_spec_version: "1.3". journal_type in run_identity. Ref: spec-ocas-journal.md.

## Inter-Skill Interfaces
All inter-skill communication uses defined intake paths per `spec-ocas-interfaces.md` v1.3. No undocumented interfaces.

Cooperative read-only cross-skill queries (no intake directory) must be documented in:
1. The skill's `## Optional skill cooperation` section
2. `spec-ocas-interfaces.md` Cooperative Query Interfaces section (if load-bearing)

## Variant Naming Convention
Format: `{skill-id}-variant-{YYYYMMDD}` (e.g., `ocas-rally-variant-20260307`).
Multiple same-day variants: append `-2`, `-3`, etc.
Variant skill_version string: `X.Y.Z-variant-{YYYYMMDD}`.

## Bundled Workflow Plans
Skills commonly invoked in multi-step workflows should include bundled plans in `references/plans/`.
Plan format: `spec-ocas-workflow-plans.md` v1.1.
Init command must copy plans to ~/openclaw/data/ocas-mentor/plans/ (skip existing files).

Expected bundled plans:
- ocas-scout: contact-enrichment
- ocas-sift: research-deep-dive
- ocas-rally: portfolio-rebalance
- ocas-voyage: trip-planning
- ocas-taste: preference-scan

## Background Task Registration (Heartbeat)
Standard wording in SKILL.md `## Background tasks`:
> During `{skill}.init`, append to `~/.openclaw/workspace/HEARTBEAT.md` if the entry is not already present (check before appending to ensure idempotence): `{skill-short}:{task-short}: {command}`

## Validation Checklist
- [ ] One sharp promise
- [ ] Responsibility boundary non-overlapping with existing skills
- [ ] Ontology types section present
- [ ] Storage uses ~/openclaw/ root
- [ ] Journal path specified
- [ ] Inter-skill interfaces documented in spec-ocas-interfaces.md
- [ ] Background tasks section present (or absent if purely reactive)
- [ ] Bundled plan in references/plans/ if multi-step workflow skill
