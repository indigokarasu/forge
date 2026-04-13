# OCAS Skill Authoring Rules

Version: 2.7.1
Author: Indigo Karasu

Changes from 2.7.0: architecture coherence audit 2026-04-12 discovered only 1 active OCAS skill repository (ocas-forge); ocas-triage design specs retained but no GitHub repository instantiated; updated Responsibility Boundaries list to remove ocas-triage and move it to legacy reference; clarified Background Tasks section to reflect only ocas-forge as active; patch version bump due to scope refinement within existing active skill count.

Changes from 2.6.4: architecture coherence audit 2026-04-11 discovered only 2 active OCAS skill repositories (ocas-forge, ocas-triage); updated Responsibility Boundaries and Background Tasks sections to reflect current active skills; other 22 previously-documented skills marked as archived/non-existent; major version bump due to scope change from 24 skills to 2 active implementations.

Changes from 2.6.3: added explicit Background tasks sections to ocas-multipass, ocas-triage, and ocas-vibes documenting that they have no operational background tasks; created skill.json files for all 24 OCAS skills; architecture coherence audit 2026-04-09.

Changes from 2.6.2: removed ocas-relay from Responsibility Boundaries list (skill does not exist as OCAS architecture component); confirmed all 24 active OCAS skills in boundaries list; architecture coherence audit 2026-04-07.

Changes from 2.6.1: verified all 24 OCAS skills have Ontology types sections per requirements; documented that each skill explicitly declares entity extraction behavior and Signal emission policy; completed comprehensive audit on 2026-04-05.

Changes from 2.6.0: added ocas-multipass and ocas-vibes to Responsibility Boundaries list; updated to reflect all 24 active OCAS skills as of 2026-04-04.

Changes from 2.5.0: updated Background Tasks skill lists to reflect current state (added ocas-sands, ocas-haiku, ocas-custodian, ocas-dispatch to cron list); clarified universal self-update cron is not counted as operational background task; updated cron CLI syntax to match openclaw cron add specification (--session, --message, --light-context, --tz flags); removed ocas-dispatch from purely reactive list.

---

## Purpose

These rules define how OCAS Agent Skills should be designed, packaged, and validated. The standard is disciplined minimalism: build the smallest skill that reliably improves agent behavior.

---

## Core Rules

### 1. A skill must earn its existence

Create a skill only when at least one of these is true:
- The task depends on a repeated tool or command surface
- The task has repeated structure worth encoding
- The task needs domain-specific workflow the base model will not reliably infer
- The task benefits from reusable templates, schemas, or validators
- The task is frequent or valuable enough to justify maintenance

Do not create a skill when:
- The behavior is already ordinary model behavior with no special workflow
- The scope cannot be reduced to one sharp promise
- The task is too rare to maintain
- The package would mostly contain generic explanation

### 2. Every skill needs one sharp promise

Complete this sentence: "This skill exists to ______."

If the answer sounds like a platform, department, or product suite, the scope is too broad.

### 3. Routing comes first

The description is routing logic, not branding copy.

A good description:
- Says what the skill does
- Says when to use it
- Uses realistic request language where helpful
- Distinguishes trigger from nearby non-trigger cases

### 4. SKILL.md is the operational surface

SKILL.md contains:
- When to use the skill
- What the skill is responsible for
- How to execute the task
- When to consult any support file

SKILL.md does not become:
- A tutorial for beginners
- A README substitute
- A changelog or design diary
- A knowledge dump

Every skill package requires a `README.md` and `CHANGELOG.md`. Structure and format are defined in `spec-ocas-skill-publishing.md` in the architecture repo. Follow that spec exactly — it is the single source of truth for README sections, CHANGELOG entry format, versioning rules, and GitHub release convention.

### 5. Match specificity to failure risk

Use general guidance when multiple approaches are acceptable. Use exact instructions, schemas, or scripts where drift is costly.

High-risk areas: command syntax, file paths, metadata fields, package structure, validation logic.

### 6. Add complexity only when justified

Minimum package:
```
ocas-{skill}/
  skill.json
  SKILL.md
```

Add `references/`, `scripts/`, or `assets/` only when they materially improve correctness, maintainability, or output quality.

---

## Skill Types

### Shortcut
Narrow tool wrapper or repeated small action.

Typical SKILL.md size: 20–120 lines.

Sections: title, when to use, quick actions or commands, inputs/options, caveats.

### Workflow
Multi-step process with moderate branching.

Typical SKILL.md size: 80–250 lines.

Sections: title, when to use, inputs/assumptions, ordered workflow, output requirements, boundaries and pitfalls.

### System
Meta-skill or durable behavior system with broader internal logic.

Typical SKILL.md size: 150–300 lines. Move secondary detail into references/.

Sections: title, trigger conditions, purpose and boundaries, decision model, execution loop, support file map, validation rules.

---

## Storage Requirements

Every skill with persistent state stores data centrally. No data inside the skill package directory.

```
~/openclaw/data/{skill-name}/   — state, config, JSONL logs
~/openclaw/journals/{skill-name}/YYYY-MM-DD/{run_id}.json  — journal files
```

LadybugDB skills only:
```
~/openclaw/db/{skill-name}/     — LadybugDB database files
```

Config file location: `~/openclaw/data/{skill-name}/config.json`
Config must include ConfigBase fields from `spec-ocas-shared-schemas.md`.

See `spec-ocas-storage-conventions.md` for the full standard.

---

## Journal Requirements

Every skill run writes a journal. Runs missing journals are invalid.

Journal file location: `~/openclaw/journals/{skill-name}/YYYY-MM-DD/{run_id}.json`

Select journal type based on whether the run executes external side effects:
- **Observation Journal** — no external side effects (reading, analyzing, discovering)
- **Action Journal** — external side effects occurred (sending, writing, booking, syncing)
- **Research Journal** — structured multi-source research session

Some skills emit multiple types depending on the command (e.g., Rally emits Observation during research and Action during trade execution).

See `spec-ocas-journal.md` for the full specification.

---

## Inter-Skill Communication Requirements

Skills communicate through defined intake directories, not direct calls.

If a skill sends signals to another skill or receives signals from another skill, it must reference `spec-ocas-interfaces.md` for the path and format.

Do not create undocumented inter-skill interfaces.

---

## Background Tasks

Some skills require work to happen on a schedule, independent of user invocation. These are background tasks. Most skills do not need them.

### Decision rule: cron vs. heartbeat

Use **cron** when:
- Exact timing matters (briefing at 7am, market open)
- The task is heavyweight (journal ingestion, deep consolidation)
- The task should run in isolation with no main session history
- Output should be delivered to a channel

Use **heartbeat** (entry in `HEARTBEAT.md`) when:
- The task is a lightweight poll or check (scan an intake directory, update an aggregate)
- Timing can drift slightly without consequence
- The task can batch with other monitoring checks

### Which skills need background tasks

**Note:** All skills have a `{skill}:update` cron job at midnight for self-updates from GitHub. This universal update task is not counted below — the lists below refer to skills with _operational_ background tasks beyond self-update.

**Current active OCAS skills:**

Skills with heartbeat entries only: ocas-forge (intake poll).

**Note:** This reflects the current OCAS ecosystem as of 2026-04-12. Additional skills (ocas-elephas, ocas-mentor, ocas-corvus, ocas-vesper, ocas-rally, ocas-thread, ocas-sands, ocas-haiku, ocas-custodian, ocas-dispatch, ocas-weave, ocas-scout, ocas-sift, ocas-look, ocas-taste, ocas-voyage, ocas-fellow, ocas-multipass, ocas-vibes, ocas-bower, ocas-spot, ocas-praxis, ocas-triage) are documented in these specs for historical reference and architecture integrity, but are not currently instantiated as repositories or released packages.

### Idempotent registration

Background tasks are registered during `{skill}.init` (which runs automatically on first use). Before calling `cron.add`, always check existing jobs first to avoid duplicates:

```bash
openclaw cron list   # check before registering
```

In agent tool calls: list existing jobs, check for the target name, add only if absent.

Job names follow the pattern `{skill-short}:{task-short}` for stable identification. Example: `elephas:ingest`, `vesper:morning`.

### SKILL.md declaration

Every skill that has background tasks must include a `## Background tasks` section in SKILL.md declaring:
- Job name
- Mechanism (cron or heartbeat)
- Schedule
- What command or action it triggers

Skills with no background tasks omit this section entirely.

### Cron job conventions

All isolated cron jobs use these flags with `openclaw cron add`:
- `--session isolated` — dedicated fresh agent session
- `--light-context` — skip workspace bootstrap to minimize token cost
- `--tz America/Los_Angeles` — timezone for schedule evaluation (update once user's timezone is known)

For main-session jobs, use `--session main --system-event "text"` with `--wake now` or `--wake next-heartbeat`.

Registration syntax:
```bash
openclaw cron add --name "{skill}:{task}" --cron "M H D Mo DoW" \
  --session isolated --message "{skill}.{command}" --light-context --tz America/Los_Angeles
```

One-shot jobs use `--at "ISO8601"` instead of `--cron`. Interval jobs use `--every "duration"`.

Manage existing jobs: `openclaw cron list`, `openclaw cron edit <id>`, `openclaw cron rm <id>`, `openclaw cron run <id>` (manual trigger).

### HEARTBEAT.md

The workspace `HEARTBEAT.md` at `~/.openclaw/workspace/HEARTBEAT.md` is the coordination point for all lightweight heartbeat tasks. Skills that contribute heartbeat entries register during `{skill}.init`.

**Standard registration pattern (use this exact wording in every SKILL.md):**

> During `{skill}.init`, append to `~/.openclaw/workspace/HEARTBEAT.md` if the entry is not already present (check before appending to ensure idempotence):
> ```
> {skill-short}:{task-short}: {command}
> ```

Example for Corvus:
```
corvus:light: corvus.analyze.light
```

Every skill that uses heartbeat must include this pattern verbatim in its SKILL.md `## Background tasks` section, substituting `{skill-short}:{task-short}` and `{command}` with the actual values.

If `HEARTBEAT.md` is empty (only blank lines and headers), OpenClaw skips heartbeat runs entirely. Keep it non-empty if any skill needs heartbeat execution.

---

## Package Structure Rules

### Base package
```
ocas-{skill}/
  skill.json
  SKILL.md
```

### references/
Use only when material is useful but too secondary or detailed for SKILL.md: longer examples, schemas, tables, templates, review checklists.

Rule: if a reference file exists, SKILL.md must state when and why to read it.

### scripts/
Use only when deterministic help materially improves reliability: validation, scaffolding, transformation, linting.

Rule: do not add scripts for ornament or theoretical completeness.

### assets/
Use only when the skill ships reusable operational artifacts: starter files, canonical examples, templates.

---

## Required SKILL.md Sections for System Skills

System skills must include:

**Responsibility Boundary** — what the skill does, what it does not do, which other skill owns the adjacent responsibility.

**Optional Skill Cooperation** — other skills this skill may cooperate with when present, but never depend on.

**Ontology Mapping** — which entity types from `spec-ocas-ontology.md` this skill extracts, manages, or queries. Skills that extract no entities and query none may omit this section.

**Journal Outputs** — which journal type(s) this skill emits.

**Storage Layout** — the skill's data and journal paths under `~/openclaw/`.

**Background Tasks** — cron jobs and heartbeat entries required by this skill, with job names, schedules, and registration commands. Omit if the skill has no background tasks.

---

## Responsibility Boundaries

Before creating a new skill, verify it does not conflict with the following active OCAS skills:

ocas-forge

Legacy reference (archived/non-existent): ocas-scout, ocas-sift, ocas-praxis, ocas-dispatch, ocas-corvus, ocas-mentor, ocas-elephas, ocas-weave, ocas-taste, ocas-voyage, ocas-look, ocas-rally, ocas-vesper, ocas-fellow, ocas-thread, ocas-custodian, ocas-haiku, ocas-bower, ocas-spot, ocas-sands, ocas-multipass, ocas-vibes, ocas-triage

Each skill build spec includes a Responsibility Boundary section.

---

## Authoring Style

- Prefer concise, operational language
- Prefer examples over exposition
- Avoid repeating the same rule across files
- Define non-public terminology locally if it appears
- Write build specs as if they will be the only file a coder LLM sees
- Avoid negative instructions that merely mention absent resources

---

## Atomic Skill Principle

Skills perform one clear role. They may cooperate with other skills when present but must never depend on them.

If a cooperating skill is absent, the skill must still function normally.

---

## Anti-Patterns

- Vague names: `helper`, `utils`, `tools`
- Descriptions that state only a broad category with no trigger condition
- SKILL.md that contains every rule, example, and edge case
- Support directories created "just in case"
- Build specs referencing prior drafts, hidden memory, or internal process documents
- Template residue: placeholders never concretized
- Storage inside the skill package directory
- Undocumented inter-skill interfaces

---

## Variant Naming Convention

Skill variants follow a standardized naming format for identification in journals, OKR evaluations, and promotion decisions.

### Format

```
{skill-id}-variant-{YYYYMMDD}
```

Examples:
- `ocas-rally-variant-20260307`
- `ocas-scout-variant-20260315`
- `ocas-sift-variant-20260401`

### Rules

- The date is the date the variant was created (not proposed or promoted).
- If multiple variants of the same skill exist on the same date, append `-2`, `-3`, etc.: `ocas-rally-variant-20260307-2`.
- Variant IDs appear in: VariantProposal, VariantDecision, CycleResult, and journal entries for that variant's runs.
- The variant's `skill_version` field in its journals should reflect its version string (e.g., `1.2.0-variant-20260307`), distinct from the champion's version.

---

## Bundled Workflow Plans

Skills that are commonly invoked as part of multi-step cross-skill workflows should ship bundled plans. Plans are stored at `references/plans/` in the skill package and copied to `~/openclaw/data/ocas-mentor/plans/` during Mentor initialization.

Skills expected to bundle plans:

| Skill | Plan ID | Description |
|---|---|---|
| ocas-scout | `contact-enrichment` | Full research pipeline for a known contact |
| ocas-sift | `research-deep-dive` | Multi-source research on a topic or entity |
| ocas-rally | `portfolio-rebalance` | Signal refresh → scoring → allocation review |
| ocas-voyage | `trip-planning` | Destination research → itinerary → accommodation |
| ocas-taste | `preference-scan` | Ingest recent activity → update preference model |

To add a bundled plan:
1. Create `references/plans/{plan_id}.plan.md` following `spec-ocas-workflow-plans.md` format.
2. Add a row to the skill's Support file map in SKILL.md referencing the plan.
3. Add plan copying to the skill's `init` command: copy `references/plans/*.plan.md` to `~/openclaw/data/ocas-mentor/plans/`, skipping files already present.

See `spec-ocas-workflow-plans.md` for the plan file format and parameter specification.

---

## Validation Standard

A skill is not ready until it passes all three checks.

### Routing Check
Test realistic requests that should trigger the skill and realistic requests that should not. The description must plausibly separate those cases.

### Structural Check
Verify:
- Required files exist
- Filenames are consistent
- Support files exist only when justified
- SKILL.md points to any support file it depends on
- Major duplication has been removed
- Storage paths use `~/openclaw/` root
- Journal path is specified
- Background tasks section present if skill has cron or heartbeat requirements; absent if purely reactive

### Usefulness Check
Verify:
- The skill has one sharp promise
- First useful action is obvious
- Precision is concentrated where failure is costly
- The package is concise enough to maintain

---

## Preferred Design Sequence

1. Define the candidate capability
2. Decide whether it deserves to be a skill
3. Classify the skill type
4. Define the sharp promise and responsibility boundary
5. Identify inter-skill interfaces needed (check `spec-ocas-interfaces.md`)
6. Determine if the skill needs background tasks — if so, choose cron vs. heartbeat and define job names and schedules
7. Choose the smallest viable package
8. Decide what belongs in SKILL.md versus support files
9. Define routing tests and structural checks
10. Write the self-contained build spec for the coder LLM

---

## Metadata Requirements

Every skill includes consistent author metadata:
- Author: Indigo Karasu
- Email: mx.indigo.karasu@gmail.com

Descriptions are optimized for discovery, not brand voice.
