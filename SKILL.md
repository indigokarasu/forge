---
name: ocas-forge
description: 'Forge: skill architect and builder. Designs, builds, and validates complete
  Agent Skill packages through a mandatory six-phase pipeline: existence gate, classify,
  scope, architecture, build, validate. Trigger phrases: ''create a new skill'', ''build
  a skill'', ''design a skill'', ''review this skill'', ''repair this skill'', ''validate
  skill package'', ''update forge''. Default output is the finished installable package.
  Do not use for skill evaluation or variant proposals (use Mentor).

  '
license: MIT
metadata:
  author: Indigo Karasu
  version: 3.2.0
---

# Forge

Forge is the system's skill architect — given a capability idea or broken existing package, it runs a mandatory six-phase internal pipeline covering existence gate, classification, scoping, architecture, construction, and validation before writing a single file. The default output is the finished, installable package with all file contents written; Forge never returns design briefs or plans in place of the real artifact.

## When to use

- Create a new Agent Skill from a goal or capability description
- **Before creating:** always check whether the capability belongs inside an existing skill (see phase 1 parent check). Default to absorption unless there's a specific reason it needs independence.
- Review or critique an existing skill package
- Repair broken or defective skill packages
- Classify whether a proposed capability deserves to be a skill
- Validate a skill package against OCAS standards
- Audit existing skills for OCAS compliance and sync to GitHub
- Consolidate orphan or duplicate skills into their natural parent
- Verify whether a skill is up to date against its GitHub source
- Sync local skill changes back to the canonical repository

## When not to use

- Evaluating skill performance — use Mentor
- Running or orchestrating skills — use Mentor (and see `deferred/running-ocas-skills.md`)
- Authentication and service wiring (OAuth, MCP setup) — use the forthcoming `ocas-auth` skill; reference content lives in `deferred/mcp-oauth-setup.md`
- Web research — use Sift
- Building non-skill artifacts

## Responsibility boundary

Forge owns skill design, construction, validation, consolidation, update verification, compliance auditing, and repo-sync.

Forge does not own: skill evaluation or variant testing (Mentor), behavioral pattern analysis (Corvus), behavioral refinement (Praxis), experimentation (Fellow), system health and skill initialization (Custodian), runtime orchestration and delegation (the agent harness), authentication and MCP wiring (ocas-auth).

Forge receives VariantProposal and VariantDecision files from Mentor. It builds variant packages and applies promotion decisions.

## Ontology types

Forge does not extract entities and does not emit Signals to Elephas. Forge operates on skill package data and skill metadata only, not on user entities from Chronicle or Weave.

## Commands

- `forge.build` — design, scope, build, and validate a complete skill package
- `forge.critique` — review a package and identify defects
- `forge.repair` — fix broken files in an existing package
- `forge.classify` — classify a proposed skill (shortcut, workflow, system)
- `forge.validate` — run validation checks on a package
- `forge.scaffold` — generate a minimal package skeleton
- `forge.consolidate` — merge an orphan or duplicate skill into its natural parent
- `forge.verify-update` — check whether a skill is at the latest version from its GitHub source
- `forge.sync` — sync local skill changes to the canonical repository via PR
- `forge.audit` — audit one or more skills for OCAS compliance, apply fixes, and sync to GitHub
- `forge.status` — current build state if multi-step build in progress
- `forge.journal` — write journal for the current run; called at end of every run
- `forge.update` — pull latest from GitHub source; preserves journals and data

## Mandatory design pipeline

Run all phases before writing files:

1. **Existence gate (HARD GATE — must pass all 3 checks before proceeding)**

   **Check A — Parent search (mandatory first step):**
   Call `skills_list` to enumerate all existing skills. For each skill whose domain overlaps the proposed capability, call `skill_view` to read its full content. Ask: "Does this existing skill already own this domain?" If yes → **STOP. Do not create a new skill.** Add the content to the parent as a `references/` doc, `scripts/` file, or new SKILL.md section. Record the decision in `decisions.jsonl`.

   **Check B — Standalone test (all 3 must be true):**
   A new skill is only justified if it has: (a) its own independent invocation path (user or cron triggers it directly by name), (b) its own cron jobs or background tasks, AND (c) its own journal output. If any of these is missing → it's a support file, not a skill. Absorb into parent.

   **Check C — Absorption test:**
   Can this content fit as a `references/<topic>.md` or `scripts/<name>.py` inside an existing skill? If yes → **absorb, don't spawn.** Creating a standalone skill for content that fits in a reference file is the #1 cause of skill proliferation. Default to absorption.

   **Only proceed to phase 2 if all 3 checks pass.** If the answer is "absorb," execute the absorption immediately: add the content to the parent skill's appropriate subdirectory, update the parent's reference table, and record the decision.
2. **Classify** — Shortcut, workflow, or system?
3. **Scope** — Exact job, explicit non-goals, smallest useful promise
4. **Architecture** — What goes in SKILL.md vs references vs scripts vs assets?
5. **Build** — Write all files
6. **Validate** — Routing, structural, usefulness checks

## Naming Rules
- Lowercase, hyphens, max 64 chars.
- **NEVER create new `ocas-*` skills without explicit user authorization.** The `ocas-` prefix is reserved. If a proposed skill name starts with `ocas-`, the user must have explicitly requested it. This prevents accidental proliferation (e.g., `ocas-vpn` created without being asked).
- Domain prefixes: `prism-`, `reflexion-`, `cek-` are unreserved and follow normal existence-gate rules.

## Skill type classification

- **Shortcut** — narrow tool wrapper. 20-120 line SKILL.md.
- **Workflow** — multi-step process. 80-250 line SKILL.md.
- **System** — durable behavior system. 150-300 line SKILL.md, deeper material in references.

## Package rules

Minimum package: SKILL.md with agentskills.io frontmatter. Add references/, scripts/, assets/ only when justified.

Read `references/enforcement_durability.md` for full guidance on how to make rules durable across updates. See also `references/package_patterns.md` for package shape guidance and `references/authoring_rules.md` for full authoring standards.

## Run completion

After every Forge command (build, critique, repair, validate, audit):

1. Check journal payload fields (see interfaces specification) for VariantProposal and VariantDecision files from Mentor; process and move to the consumer's ingestion log
2. Persist build log entries and decisions to local JSONL files
3. Log material decisions to `decisions.jsonl`
4. Write journal via `forge.journal`

## Anti-patterns to reject

- Vague or overly broad scope
- Generic descriptions that don't route well
- SKILL.md bloated with background explanation
- Support folders created for aesthetics
- Plans returned instead of packages
- Template residue and placeholders
- Storage inside skill package directories
- Undocumented inter-skill interfaces
- **`## Integrated:` wrapper sections:** when folding content into a parent skill, do NOT wrap it in `## Integrated: <name>` sections. Refactor the content into the parent's existing section structure instead. If the parent has no matching section, create one with a proper name — not a wrapper header referencing the old skill name.
- **Advisory-only enforcement doesn't work:** writing "use Forge instead of skill_manage" in MEMORY.md is advisory and easily skipped. The hard gates must be in the Forge SKILL.md itself (phase 1 checks A/B/C), because that's the artifact that gets loaded and followed. Never rely on memory notes as the sole enforcement mechanism for behavioral rules. See `references/enforcement_durability.md`.

## Pitfalls

- **Orphan Skills**: Skills that duplicate parent functionality.
- **Overlap**: Multiple skills handling the same task.
- **Bloat**: Skills that grow too large and should be split.
- **Incorrect Naming**: NEVER create new `ocas-*` skills without explicit user authorization. The `ocas-` prefix is reserved. If a proposed skill name starts with `ocas-`, the user must have explicitly requested it. This prevents accidental proliferation (e.g., `ocas-vpn`).
- **Non-durable fixes**: If a fix or rule is added to a skill, ensure it is in the skill's own git repo (e.g., `~/hermes/skills/ocas-forge/`) or in MEMORY.md — not in hermes core, which gets wiped on updates.
- **Skill library organization**: The target shape is CLASS-LEVEL umbrella skills, each with a rich SKILL.md and a `references/` directory for session-specific detail. NOT a long flat list of narrow one-session-one-skill entries. When auditing or restructuring, always prefer absorption into an existing class-level umbrella over creating a new narrow skill.

## Inter-skill interfaces

Forge reads variant proposals and decisions from Mentor journals. journal payload fields (see interfaces specification)

File types received:
- `{proposal_id}.json` — VariantProposal (spec-ocas-shared-schemas.md)
- `{decision_id}.json` — VariantDecision (spec-ocas-shared-schemas.md)

After processing each file, move to the consumer's ingestion log.

See `spec-ocas-interfaces.md` for full handoff contracts.

## Storage layout

```
{agent_root}/commons/data/ocas-forge/
  config.json
  build_log.jsonl
  decisions.jsonl
    {proposal_id}.json
    {decision_id}.json
    processed/

{agent_root}/commons/journals/ocas-forge/
  YYYY-MM-DD/
    {run_id}.json
```

Default config.json:
```json
{
  "skill_id": "ocas-forge",
  "skill_version": "2.3.2",
  "config_version": "1",
  "created_at": "",
  "updated_at": "",
  "validation": {
    "require_routing_tests": true,
    "require_structural_check": true,
    "require_usefulness_check": true
  },
  "retention": {
    "days": 0,
    "max_records": 10000
  }
}
```

## OKRs

Universal OKRs from spec-ocas-journal.md apply to all runs.

```yaml
skill_okrs:
  - name: build_completion_rate
    metric: fraction of forge.build invocations producing a complete package
    direction: maximize
    target: 0.95
    evaluation_window: 30_runs
  - name: validation_pass_rate
    metric: fraction of built packages passing all three validation checks
    direction: maximize
    target: 0.90
    evaluation_window: 30_runs
  - name: variant_build_success
    metric: fraction of VariantProposal journal payloads successfully built
    direction: maximize
    target: 0.90
    evaluation_window: 30_runs
```

## Optional skill cooperation

- Mentor — receives VariantProposal and VariantDecision files via journal payload
- Fellow — Forge may build experiment harnesses for Fellow benchmarks
- Custodian — initializes skills built by Forge during system health passes; Forge-built packages should include conformant Background tasks tables so Custodian can register them automatically
- Elephas — journal entity observations consumed during Chronicle ingestion

## Journal outputs

Action Journal — every build, critique, repair, validation, audit, and variant processing run.

When entities are encountered during a run, include the following fields in `decision.payload`:

- `entities_observed` — entities encountered (e.g. Entity/AI for skills being built, Thing/DigitalArtifact for skill packages and code artifacts, Concept/Idea for design patterns and architectures)
- `relationships_observed` — relationships between observed entities
- `preferences_observed` — any preferences inferred from observations

Each entity observation must include a `user_relevance` field: `user` if the entity is directly related to the user's world, `agent_only` if encountered incidentally during internal operations, `unknown` if unclear. Most Forge entities are `agent_only` since they are system internals.

## Initialization

On first invocation of any Forge command, run `forge.init`:

1. Create `{agent_root}/commons/data/ocas-forge/` and subdirectories (journal entries, the consumer's ingestion log)
2. Write default `config.json` with ConfigBase fields if absent
3. Create empty JSONL files: `build_log.jsonl`, `decisions.jsonl`
4. Create `{agent_root}/commons/journals/ocas-forge/`
5. ~~Register heartbeat entry~~ — Hermes has no heartbeat mechanism. forge:journal-scan runs via cron only.
6. Register cron job `forge:update` if not already present (check the platform scheduling registry first)
7. Log initialization as a DecisionRecord in `decisions.jsonl`

## Background tasks

| Job name | Mechanism | Schedule | Command |
|---|---|---|---|
| `forge:journal-scan` | cron | `*/5 * * * *` (every 5 min) | Check journal payload fields (see interfaces specification) for VariantProposal and VariantDecision files from Mentor; process and move to the consumer's ingestion log |
| `forge:update` | cron | `0 0 * * *` (midnight daily) | `forge.update` |
| `forge:skill-audit` | cron | `0 6 * * 1` (Monday 6am) | Run `scripts/forge_audit_skills.py --dry-run` to scan for orphan skills. If orphans found, review and consolidate into parent skills. Report results. |


```
# Check platform scheduling registry for existing tasks
# Task declared in SKILL.md frontmatter metadata.{platform}.cron
```

## Self-update

`forge.update` pulls the latest package from the `source:` URL in this file's frontmatter. Runs silently — no output unless the version changed or an error occurred.

1. Read `source:` from frontmatter → extract `{owner}/{repo}` from URL
2. Read local version from SKILL.md frontmatter `metadata.version`
3. Fetch remote version from SKILL.md frontmatter: `gh api "repos/{owner}/{repo}/contents/SKILL.md" --jq '.content' | base64 -d | grep 'version:' | head -1 | sed 's/.*"\(.*\)".*/\1/'`
4. If remote version equals local version → stop silently
5. Download and install:
   ```bash
   TMPDIR=$(mktemp -d)
   gh api "repos/{owner}/{repo}/tarball/main" > "$TMPDIR/archive.tar.gz"
   mkdir "$TMPDIR/extracted"
   tar xzf "$TMPDIR/archive.tar.gz" -C "$TMPDIR/extracted" --strip-components=1
   cp -R "$TMPDIR/extracted/"* ./
   rm -rf "$TMPDIR"
   ```
6. On failure → retry once. If second attempt fails, report the error and stop.
7. Output exactly: `I updated Forge from version {old} to {new}`

This skill self-updates every 24 hours via `forge.update`, which pulls the latest version from GitHub and restarts the skill's background tasks if applicable.

### Update verification (`forge.verify-update`)

When a skill's self-update command fails or you need to confirm a skill is at the latest version without mutating it, verify manually: read `metadata.version` from local `SKILL.md`, fetch the remote tarball or release (`curl https://api.github.com/repos/{owner}/{repo}/releases/latest`), read its `metadata.version`, and compare. If versions match, stop silently; if they differ, copy extracted files over, log a decision, and clean up.

See `references/builder_workflows.md` for the full procedure, file-level diff steps, git-state verification, and pitfalls.

## Skill consolidation

`forge.consolidate` merges an orphan or duplicate skill into its natural parent to reduce skill-list sprawl and invocation confusion.

**Use when:** a skill duplicates functionality already in a parent skill; a skill is "glue" or a "patch" that logically belongs inside an existing one; the skill list has grown unwieldy with overlapping concerns; a `## Integrated:` wrapper section exists that should be refactored into the parent's proper structure.

**Core rule:** fold merged content into the parent's existing section structure. **Do not** wrap it in `## Integrated: <name>` sections — that bloats SKILL.md, duplicates headings, and defeats progressive disclosure. Identify the parent section that matches the orphan's concern and refactor the content in, resolving redundancy as you go.

**Pre-build default:** before `forge.build` creates any new skill, phase 1 (existence check) requires a parent search. If a parent exists, absorb into it as `references/` or `scripts/` — do not create a standalone. Creation is the exception, absorption is the default.

**Shape of the workflow:** audit → map orphan to parent → pull latest → fold content → commit on a `merge/` branch → PR → delete orphan locally → update memory.

See `references/builder_workflows.md` for the full command sequence, branch-naming convention, and pitfalls (stash conflicts, divergent branches, non-repo skill dirs, for-loop `cd` gotcha).

## Skill sync

`forge.sync` identifies local skill changes in `{agent_root}/skills` and syncs them to the canonical `hermes-agent` repository via a fork-and-PR workflow.

**Use when:** pushing local skill changes to GitHub; persisting a round of local iterations into the main codebase.

**Shape of the workflow:** enumerate local SKILL.md files → diff each against its repo counterpart (NEW or CHANGED) → copy changes into the repo tree → branch `skill-updates-YYYYMMDD` → commit, push to fork, open PR against `NousResearch/hermes-agent:main`.

See `references/builder_workflows.md` for the exact `find | diff` loops, the `gh pr create` invocation, and pitfalls.

## Skill audit

`forge.audit` audits one or more existing OCAS skills for architecture compliance, applies fixes, and syncs to GitHub.

**Use when:** user asks to "check X against forge standards", "audit X skill", "make sure X meets OCAS standards", or "review and fix X".

**Shape of the workflow:** see `references/compliance-audit-checklist.md` for the full 7-phase procedure (inventory → frontmatter → sections → references → skill.json → fixes → GitHub sync).

## Support file map

| File | When to read |
|------|-------------|
| `references/enforcement_durability.md` | Before writing rules that must survive skill updates; when designing enforcement mechanisms |
| `references/package_patterns.md` | Before structuring a new skill package; when deciding what goes in SKILL.md vs references vs scripts |
| `references/authoring_rules.md` | Before writing or editing any skill SKILL.md; authoring standards reference |
| `references/compliance-audit-checklist.md` | Before auditing an existing skill for OCAS compliance; file inventory, section checklist, GitHub sync steps |
| `references/builder_workflows.md` | Before forge.verify-update, forge.consolidate, forge.sync, or forge.audit; contains command sequences and pitfalls |