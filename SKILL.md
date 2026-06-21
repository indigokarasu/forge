---
name: ocas-forge
description: 'Skill architect and builder. Designs, builds, and validates complete Agent Skill packages through a mandatory six-phase pipeline: existence gate, classify, scope, architecture, build, validate. Default output is the finished installable package. Do NOT use for skill evaluation (use skilllab''s Critique procedure) or variant proposals (use ocas-mentor).'
license: MIT
source: https://github.com/indigokarasu/forge
includes:
- references/**
- scripts/**
metadata:
  author: Indigo Karasu (indigokarasu)
  version: 3.4.1
tags:
- skill-builder
- architecture
- design
- OCAS-core
triggers:
- build a skill
- create skill
- skill architecture
- design skill package
- skill builder
---
## Interactive Menu

When invoked interactively, present a two-level menu. See `references/interactive-menu.md` for the full menu structure.



Forge is the system's skill architect — given a capability idea or broken existing package, it runs a mandatory six-phase internal pipeline covering existence gate, classification, scoping, architecture, construction, and validation before writing a single file. The default output is the finished, installable package with all file contents written; Forge never returns design briefs or plans in place of the real artifact.

## When to Use

- Building new OCAS skills from scratch
- Skill architecture and design review
- Bulk skill library updates and synchronization
- Skill consolidation and deprecation
- When a new capability needs a permanent skill home
- Create a new Agent Skill from a goal or capability description
- Review or critique an existing skill package
- Repair broken or defective skill packages
- Validate a skill package against OCAS standards

## When NOT to Use

- One-off task execution (use the appropriate existing skill)
- Skill evaluation/scoring (use Mentor or skilllab)
- Content generation or research
- System health monitoring (use Custodian)
- Authentication and service wiring (use ocas-auth)
- Building non-skill artifacts
- Web research — use Sift

## Responsibility boundary

Forge owns skill design, construction, consolidation, update verification,
compliance auditing, and repo-sync. Forge's `forge.validate` handles quick
structural checks; deep quality scoring and iterative improvement is now
owned by `skilllab` (Critique procedure, merged from ocas-critique).

Forge does not own: skill quality scoring and iteration (skilllab), skill
evaluation or variant testing (Mentor), behavioral pattern analysis (Corvus),
behavioral refinement (Praxis), experimentation (Fellow), system health and
skill initialization (Custodian), runtime orchestration and delegation (the
agent harness), authentication and MCP wiring (ocas-auth).

**Note on `review-skill` vs skilllab's Critique:** The 3rd-party `review-skill`
(agentskill-sh) provides lightweight quick-check scoring. skilllab's Critique
procedure is the full OCAS quality engine with 6-phase pipeline, batch mode,
iteration loops, and autonomous improvement. Use skilllab for all OCAS skill
scoring. Use `review-skill` only for quick structural checks on non-OCAS
skills. Never
push `review-skill` to GitHub — it's 3rd-party.

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

Run all phases before writing files. Full phase detail including existence gates
(parent search, standalone test, absorption test), classification, scoping,
architecture, build, and validation procedures: see
`references/design_pipeline.md`.

Key rule: **absorption first.** If an existing skill already owns the domain,
add content to it as a `references/` doc or `scripts/` file — do not create a
new skill. See `references/enforcement_durability.md` for the absorption
decision framework.

## Naming and Authorship Rules

See `references/naming-and-authorship.md` for the full naming convention and authorship tagging rules. Key points:

- **Never create `ocas-*` or rename to `ocas-*`/`util-*` without explicit user authorization.**
- **Auto-generated skills** must use `author: autogenerated` in metadata.
- **Auto-generated thin wrappers** are candidates for deletion — see references for criteria.

## Skill type classification

- **Shortcut** — narrow tool wrapper. 20-120 line SKILL.md.
- **Workflow** — multi-step process. 80-250 line SKILL.md.
- **System** — durable behavior system. 150-300 line SKILL.md, deeper material in references.

## Package rules

Minimum package: SKILL.md with agentskills.io frontmatter. Add references/, scripts/, assets/ only when justified. Read `references/enforcement_durability.md` for full guidance on how to make rules durable across updates. See also `references/package_patterns.md` for package shape guidance and `references/authoring_rules.md` for full authoring standards.

## Run completion

After every Forge command (build, critique, repair, validate, audit):

1. Check `{agent_root}/commons/data/ocas-forge/` for unprocessed VariantProposal and VariantDecision JSON files. Cross-reference proposal IDs against `intake/processed/` and `processed/` directories to skip already-processed files. Process any new files — build variant packages, apply fixes, or queue for Mentor evaluation as appropriate. After processing, move files to `processed/`.
2. Check journal payload fields (see interfaces specification) for VariantProposal and VariantDecision files from Mentor received via journal; process and move to the consumer's ingestion log.
3. Persist build log entries and decisions to local JSONL files.
4. Log material decisions to `decisions.jsonl`.
5. Write journal via `forge.journal`.

**When to apply fixes directly vs. build variants:** If a proposal has strong evidence (≥3 consecutive proposals for the same issue, ≥50 runs analyzed, ≥7 days of consistent data, and the fix is low-risk), Forge may apply the fix directly without a full A/B evaluation cycle. Otherwise, queue for Fellow evaluation. Document the rationale in the action journal.

## Cross-platform portability

Skills that hardcode `~/.hermes/` paths will NOT work on other agent harnesses (OpenClaw, Claude Code, Cursor, etc.). When building a new skill:

- **Use `{agent_root}`** as the base for all paths inside the skill's storage layout diagrams. This variable resolves to whatever harness the skill runs on.
- **NEVER hardcode `~/.hermes/`** in file paths, storage diagrams, or operational descriptions. Even for Hermes-native skills, use `{agent_root}/sessions/`, `{agent_root}/skills/`, `{agent_root}/references/` instead.
- **Mention the target harness** in the frontmatter with a `requires:` field if the skill depends on Hermes-specific tools (`memory`, `skill_manage`, `session_search`, `cronjob`). Example: `requires: hermes`. This tells other harnesses to skip the skill.
- **Document Hermes-specific tool dependencies** in a "Required tools" section so future porters know what to adapt.

## Anti-patterns to reject

- Vague or overly broad scope
- Generic descriptions that don't route well
- SKILL.md bloated with background explanation
- Support folders created for aesthetics
- Plans returned instead of packages
- Template residue and placeholders
- Storage inside skill package directories
- Undocumented inter-skill interfaces
- **`## Integrated:` wrapper sections:** when folding content into a parent skill, do NOT wrap it in `## Integrated:` sections. Refactor the content into the parent's existing section structure instead.
- **Advisory-only enforcement doesn't work:** writing "use Forge instead of skill_manage" in MEMORY.md is advisory and easily skipped. The hard gates must be in the Forge SKILL.md itself (phase 1 checks A/B/C), because that's the artifact that gets loaded and followed. Never rely on memory notes as the sole enforcement mechanism for behavioral rules.

## Gotchas

- **Duplicate file entries cause patch failures**: Before patching a skill file, always check for duplicate entries (especially in Gotchas sections). The `patch` tool's `old_string` must be unique — if a Gotcha appears twice, expand the surrounding context to make the match unique, or use `replace_all=true` intentionally. When patching skill files you haven't read in full this session, scan for duplicates first.
- **Stale files in `processed/` vs `intake/processed/`**: The Forge journal-scan cross-references proposals against `intake/processed/` first. Files can accumulate in `processed/` without being mirrored to `intake/processed/`. During `forge:journal-scan`, always check both locations. Newly found files in `processed/` should be copied to `intake/processed/` after processing to keep the two directories in sync.

- **Non-proposal/decision files in data root are not work items**: Files like `config.json`, `decisions.jsonl`, and other non-`.json` or non-proposal/decision-named files in the Forge data root are not unprocessed work. The journal scan should only flag files matching the VariantProposal (`vp_*.json`) or VariantDecision (`vd_*.json`) naming patterns, or files in `proposals/` / `intake/` subdirectories. Skip everything else.
- **Missing `includes:` in frontmatter**: When a skill has a `references/` or `scripts/` directory, the frontmatter must include `includes: [references/**]`. Without it, the agent won't auto-discover support files.
- **Scope boundary for sync**: `forge.sync` and `forge.audit` must ONLY operate on `ocas-*` skills. Never upload, sync, or publish non-OCAS skills to the indigokarasu GitHub account or agentskill.sh. Before any sync operation, verify each skill name starts with `ocas-`. If a non-OCAS skill is encountered, skip it and report to the user.
- **Doing more than asked**: When the user says "review these skills," review them — don't also rewrite, restructure, or push to GitHub unless explicitly asked. When the user says "fix this one thing," fix that one thing — don't also refactor unrelated sections. Match your work to the scope of the request.
- **Over-structuring responses**: Don't present a table of findings, severity ratings, and recommendations when the user asked you to just do something. Execute first, report concisely after. Match complexity to the question.
- **Orphan Skills**: Skills that duplicate parent functionality.
- **Overlap**: Multiple skills handling the same task.
- **Bloat**: Skills that grow too large and should be split.
- **Incorrect Naming**: NEVER create new `ocas-*` or rename to `ocas-*`/`util-*` without explicit user authorization. See `references/naming-and-authorship.md`.
- **Non-durable fixes**: If a fix or rule is added to a skill, ensure it is in the skill's own git repo or in MEMORY.md — not in hermes core, which gets wiped on updates.
- **Skill library organization**: The target shape is CLASS-LEVEL umbrella skills. Session-specific artifacts should be absorbed into existing umbrellas, not created as standalone skills.
- **Frontend anti-slop reference**: When building any skill that produces or evaluates frontend UI, load the anti-slop rules from the taste-skill reference at `~/.hermes/references/design/taste-skill/anti-slop-rules.md` and the pre-flight checklist at `~/.hermes/references/design/taste-skill/anti-slop-preflight.md`. These are the canonical AI-frontend anti-pattern references. See `~/.hermes/references/design/INDEX.md` §6 for the full taste-skill integration.
- **Runaway repo creation (`forge.sync`)**: The `forge.sync` and `forge.consolidate` workflows call `gh repo create` for any skill they process, and default to `--public`. Before creating any GitHub repo, check whether the skill is a known 3rd-party skill (hermes-agent bundled skills, agentskill.sh skills, hub-installed skills, etc.). If it is, **do NOT create a repo for it**. Creating repos for 3rd-party skills pollutes the user's GitHub and can accidentally publish code that isn't theirs. Keep 3rd-party skills local-only unless the user explicitly asks to publish.
- **Panic reporting**: When checking for the existence of skills or repos, verify the actual state (local directory, git remote, GitHub API) before reporting catastrophic findings like "lost and deleted with no copy." Incorrect panic reports erode trust and waste investigation time.
- **Duplicate repos**: Before creating a new repo, always check if one already exists with `gh repo list`. If a repo with the same or similar name exists, use the existing one.
- **Re-applying fixes that are already done**: Before patching a skill to address a scanner finding or audit issue, CHECK THE CURRENT STATE. Read the skill file first. If the fix is already applied, don't re-apply.
- **YAML block scalar truncation**: `description: >` and `description: |` block scalars contain embedded newlines. `execute_code` with `content.split('---')` WILL truncate the file at the first `---` inside the block scalar, destroying body content. Always use `read_file` for exact line ranges, then `patch` with precise old_string. After any frontmatter edit, verify line count, YAML parse, and body start heading.

- **`action` field is polymorphic in forge journals — guard with `isinstance` before every access** — Forge scan journals store `action` as one of three types: (1) **dict** with `result` + `findings` keys; (2) **string** containing a human-readable result message; (3) **empty list** `[]` with no `result` key. Inline ingest scripts must branch: `isinstance(action, dict)` → `action.get("result")`; `isinstance(action, str)` → `startswith` against `FORGE_NO_OP_RESULTS`; `isinstance(action, list)` → check `findings.unprocessed_proposals == 0`. A bare `action.get("result")` crashes on string/list. Confirmed 2026-06-21.
- **Don't change repo visibility**: When updating or syncing a skill that already has a GitHub repo, never change its visibility unless the user explicitly tells you to.
- **Appending to JSONL files**: When appending to `.jsonl` files (e.g., `decisions.jsonl`), ALWAYS use `echo '{"key": "val"}' >> file.jsonl`. NEVER use heredoc redirection (`cat > file << 'EOF'`) — the `>` operator truncates the file first, destroying all existing entries.
- **Stale proposal duplicates in data root**: After Mentor drops VariantProposal files, copies can remain in `{agent_root}/commons/data/ocas-forge/` (data root) even after processing. During `forge:journal-scan`: (1) Check if `intake/processed/` exists — if so, cross-reference each data-root `.json` `proposal_id` against filenames there; skip any already present. (2) If `intake/processed/` does NOT exist, check for a `processed/` subdirectory within the data root itself. (3) If neither processed directory exists, all `.json` files in the data root are unprocessed. After processing, move files to `processed/` (create it if needed).
- **Path mismatch in `comm` cross-reference**: When using `comm` to compare file lists between `proposals/` and `processed/` directories, strip directory prefixes first — `comm` compares lines literally, so `proposals/vp_0625cecd.json` never matches `vp_0625cecd.json`, making every file appear unprocessed. Use `sed 's|proposals/||'` or `basename` on both sides. After running the comparison, spot-check: pick one filename from the "unprocessed" list and verify it's actually missing from the processed dir before taking action.
- **`write_file` escapes quotes in Python files**: When writing `.py` files via `write_file`, inner double quotes in Python string/dict literals get backslash-escaped, producing `SyntaxError: unterminated string literal` pointing to the wrong line. This is especially insidious with dict literals. **Workaround**: For Python scripts, use `terminal()` with a single-quoted heredoc: `cat > /tmp/script.py << 'SCRIPTEOF'` ... `SCRIPTEOF`, then run with `python3 /tmp/script.py`. Always verify with `python3 -c "compile(open(f).read(), f, 'exec')"` first. For non-Python files (markdown, JSON, YAML), `write_file` is safe.

## Inter-skill interfaces

Forge reads variant proposals and decisions from Mentor journals.

File types received:
- `{proposal_id}.json` — VariantProposal
- `{decision_id}.json` — VariantDecision

After processing each file, move to the consumer's ingestion log.

See `references/interfaces.md` for full handoff contracts.

## Storage layout

See `references/storage-layout.md`.

## OKRs

See `references/okrs.md`.

## Optional skill cooperation

- Critique (skilllab) — the evaluation complement to Forge's build pipeline
- Mentor — receives VariantProposal and VariantDecision files via journal payload
- Fellow — Forge may build experiment harnesses for Fellow benchmarks
- Custodian — initializes skills built by Forge during system health passes
- **Elephas** — journal entity observations consumed during Chronicle ingestion

## Journal outputs

Action Journal — every build, critique, repair, validation, audit, and variant processing run.

## Initialization

On first invocation of any Forge command, run `forge.init`. Creates data
directories, writes default config, registers the `forge.update` cron job, and
logs the initialization decision. See `references/init_procedure.md` for the
exact sequence.

## Dispatch / Cron Integration

When triggered by the dispatcher (`dispatcher.py`) or the `forge:journal-scan` cron:

1. Check `{agent_root}/commons/data/ocas-forge/` for unprocessed `vp_*.json` (VariantProposal) or `vd_*.json` (VariantDecision) files in the data root, `proposals/`, and `intake/` directories
2. Cross-reference against `intake/processed/` and `processed/` to skip already-processed files
3. Process any new files: build variant packages, apply fixes, or queue for Mentor evaluation
4. After processing, move files to `processed/`
5. If no unprocessed files: scan is clean, write journal entry and exit

The most recent forge scan journal should show `result: "no_op"` with `findings.unprocessed_proposals: 0` when the queue is empty.

**Multi-skill dispatch pattern:** When the dispatcher triggers multiple skills in one dispatch (e.g., Forge + Mentor + Praxis), each pipeline runs independently. Forge's job is to scan for unprocessed variants and write its journal. If nothing found, write a no-op journal and exit. Don't block on sibling skills.

**Multi-skill dispatch pattern:** When the dispatcher triggers multiple skills in one dispatch (e.g., Forge + Mentor + Praxis), each pipeline runs independently. Forge's job is to scan for unprocessed variants and write its journal. If nothing found, write a no-op journal and exit. Don't block on sibling skills.

## Self-update

`forge.update` pulls the latest package from the `source:` URL in frontmatter.
Runs silently unless version changed or error.

## Skill consolidation

`forge.consolidate` merges an orphan or duplicate skill into its natural parent.
See `references/builder_workflows.md` for the full workflow.

**Core rule:** fold merged content into the parent's existing section structure.
Do NOT wrap in `## Integrated:` sections.

## GitHub repo creation

Before creating any GitHub repo, verify the skill is OCAS-authored. See
`references/github_repo_guardrails.md` for the full guardrail checklist.

## Skill library sync audit

When asked to audit sync state of all OCAS skills, or when running a scheduled
sync check, use the workflow in `references/sync_audit_procedure.md`.

## Skill audit

`forge.audit` audits one or more existing OCAS skills for architecture compliance,
applies fixes, and syncs to GitHub.

## Platform notes

Forge uses the `memory` tool lightly — only for build state during multi-step builds.

## Support File Map

| File | When to read |
|------|-------------|
| `references/design_pipeline.md` | Before running forge.build — the mandatory 6-phase pipeline |
| `references/init_procedure.md` | On first invocation of any Forge command |
| `references/sync_audit_procedure.md` | Before forge.sync-audit |
| `references/enforcement_durability.md` | Before writing rules that must survive skill updates |
| `references/package_patterns.md` | Before structuring a new skill package |
| `references/authoring_rules.md` | Before writing or editing any skill SKILL.md |
| `references/compliance-audit-checklist.md` | Before auditing an existing skill |
| `references/builder_workflows.md` | Before forge.verify-update, forge.consolidate, forge.sync, or forge.audit |
| `references/github_repo_guardrails.md` | Before creating any GitHub repo or PR |
| `references/synthesis-methodology.md` | When synthesizing a new skill from multiple source skills |
| `references/examples.md` | When looking for concrete examples of OCAS skill patterns |
| `references/schemas.md` | Before creating or validating data structures |
| `references/storage_conventions.md` | When designing storage layouts |
| `references/ontology.md` | When determining which entity types to use |
| `references/journal.md` | Before calling forge.journal; at end of every run |
| `references/workflow_plans.md` | Before creating or executing workflow plans |
| `references/interfaces.md` | When designing inter-skill communication |
| `references/skill-script-organization.md` | When organizing scripts within a skill package |
| `references/consolidation_pattern_diagnosis.md` | When diagnosing skill overlap or redundancy |
| `references/recovery-standardization-pattern.md` | When implementing recovery contracts |
| `references/script-placement-convention.md` | When deciding where to place scripts |
| `references/frontmatter-editing-pitfalls.md` | Before editing any skill frontmatter |
| `references/storage-layout.md` | When debugging data path issues or managing disk |
| `references/okrs.md` | When reviewing skill performance against targets |
| `references/naming-and-authorship.md` | Before naming, renaming, or setting author on any skill; before deleting auto-generated skills |
| `references/dojo-skill-cleanup.md` | Before deleting auto-generated skills; when identifying auto-generated skill candidates |
| `references/journal-scan-cron-guide.md` | Before running forge:journal-scan — cron mode procedures and pitfalls |
| `references/session-20260621-dispatch.md` | Session-specific: dispatch-triggered clean scan, multi-skill dispatch pattern (Forge+Mentor+Praxis) |
| `references/interactive-menu.md` | When invoked interactively via `/` command — two-level menu layout, response parsing, platform adaptation |
