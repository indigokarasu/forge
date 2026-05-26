# Design Pipeline

The mandatory six-phase pipeline Forge runs before writing any files.

## Phase 1: Existence Gate (HARD GATE — must pass all 3 checks before proceeding)

### Check A — Parent search (mandatory first step)
Call `skills_list` to enumerate all existing skills. For each skill whose domain overlaps the proposed capability, call `skill_view` to read its full content. Ask: "Does this existing skill already own this domain?" If yes → **STOP. Do not create a new skill.** Add the content to the parent as a `references/` doc, `scripts/` file, or new SKILL.md section. Record the decision in `decisions.jsonl`.

### Check B — Standalone test (all 3 must be true)
A new skill is only justified if it has: (a) its own independent invocation path (user or cron triggers it directly by name), (b) its own cron jobs or background tasks, AND (c) its own journal output. If any of these is missing → it's a support file, not a skill. Absorb into parent.

### Check C — Absorption test
Can this content fit as a `references/<topic>.md` or `scripts/<name>.py` inside an existing skill? If yes → **absorb, don't spawn.** Creating a standalone skill for content that fits in a reference file is the #1 cause of skill proliferation. Default to absorption.

**Only proceed to phase 2 if all 3 checks pass.** If the answer is "absorb," execute the absorption immediately: add the content to the parent skill's appropriate subdirectory, update the parent's reference table, and record the decision.

## Phase 2: Classify
Shortcut, workflow, or system?

## Phase 3: Scope
Exact job, explicit non-goals, smallest useful promise.

## Phase 4: Architecture
What goes in SKILL.md vs references vs scripts vs assets?

## Phase 5: Build
Write all files.

## Phase 6: Validate
Routing, structural, usefulness checks.

See `references/package_patterns.md` for package shape guidance and `references/authoring_rules.md` for full authoring standards.
