---
name: ocas-forge
description: 'Skill architect and builder. Designs, builds, and validates complete Agent Skill packages through a mandatory eight-phase pipeline: existence gate, research, classify, scope, architecture, plan, build, validate. Default output is the finished installable package. Not for skill evaluation (use skilllab''s Critique procedure) or variant proposals (use ocas-mentor).'
license: MIT
source: https://github.com/indigokarasu/forge
includes:
- references/**
- scripts/**
metadata:
  author: Indigo Karasu (indigokarasu)
  version: 3.7.1
  hermes:
    category: software-development
    tags:
    - skill-builder
    - architecture
    - design
    - OCAS-core
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
- **`nargs='[]'` is invalid in argparse** — When defining command-line arguments, `nargs='[]'` is not a valid option and will cause a ValueError. To accept zero or more arguments, use `nargs='*'` instead. This caused the run_dispatch_pipeline.py script to fail until corrected.


Forge is the system's skill architect — given a capability idea or broken existing package, it runs a mandatory eight-phase internal pipeline covering existence gate, research, classification, scoping, architecture, planning, construction, and validation before writing a single file. The default output is the finished, installable package with all file contents written; Forge never returns design briefs or plans in place of the real artifact.

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
- **Skill structure reference / frontmatter template lookup** — use `write-a-skill` for quick
  reference on field requirements, file layout, and description conventions. Forge is for building.

## Responsibility boundary

Forge owns skill design, construction, consolidation, update verification,
compliance auditing, and repo-sync. Forge's `forge.validate` handles quick
structural checks; deep quality scoring and iterative improvement is now
owned by `skilllab` (Critique procedure, merged from ocas-critique).

Forge does not own: skill quality scoring and iteration (skilllab), skill
evaluation or variant testing (Mentor), behavioral pattern analysis,
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

- **Concept/Event** — projects, tasks, skill performance evaluations, OKR cycles
- **Concept/Idea** — improvement proposals, behavioral patterns
- **Thing/DigitalArtifact** — project state records, task graphs, evaluation reports

Mentor does not emit entity signals directly. Journal outputs are ingested by Chronicle for knowledge persistence.

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
(parent search, standalone test, absorption test), **research (skill library → GitHub search → deep-read → compare)**,
classification, scoping, architecture, plan, build, and validation procedures: see
`references/design_pipeline.md`.

Key rule: **absorption first.** If an existing skill already owns the domain,
add content to it as a `references/` doc or `scripts/` file — do not create a
new skill. See `references/enforcement_durability.md` for the absorption
decision framework.

**Research rule:** After the existence gate passes, you MUST research before
classifying. Search GitHub repos (via `gh search repos`) AND search the skill
library (via the APIs below) to understand what already exists. The goal is
NOT to copy existing skills but to **understand how they work** and **synthesize**
that knowledge into a new, better skill. Review at least 10 repos or skills
before deciding to build.

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

- **Skipping research on skill improvement.** Phase 1.5 (Research) is mandatory for ALL forge operations — not just new builds. When asked to "improve" or "update" an existing skill, you MUST still research external sources (GitHub, arxiv, community patterns) to find new patterns, techniques, and taxonomies that could improve the skill. The user correction "did you do the research phase?" is a signal that you skipped Phase 1.5. Research is not optional just because the skill already exists — the whole point of improvement is to find what you don't already know.
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

- **Fixed argparse nargs error in run_dispatch_pipeline.py** — Changed `nargs='[]'` to `nargs='*'` for the --new-files argument to accept zero or more arguments. This fixed a ValueError that occurred when the script was called during dispatch processing.
- **Stale files in `processed/` vs `intake/processed/`** — check both locations during journal-scan
- **`proposals/` is a SOURCE MIRROR, not pending work (confirmed 2026-07-13):** When scanning for unprocessed variant proposals (`vp_*.json` / `vd_*.json`), do NOT count files under `commons/data/ocas-forge/proposals/`. Those are source mirrors already copied into `intake/processed/` (and `processed/`). A naive glob/recursive count of `proposals/` overcounts and falsely flips a `routine_no_op` dispatch into a `genuine` variant-build dispatch. Unprocessed = files in `intake/` NOT yet in `intake/processed/`. Cross-check the count against the prior `forge-scan-*.json` journal's `unprocessed_proposals` field; if the prior scan said 0 and no new variant work arrived, the real count is 0. Confirmed 2026-07-13: a scan counted 11 `vp_*.json` in `proposals/` and wrote `unprocessed_proposals: 11` / `action: genuine` — all 11 were mirrored in `intake/processed/`, so the correct value was 0 and the dispatch was `routine_no_op`. Fix by patching the forge-scan journal to 0 before bridging.
- **Missing `includes:` in frontmatter** — required when references/ or scripts/ dir exists
- **Scope boundary for sync** — `forge.sync`/`forge.audit` only on `ocas-*` skills
- **Doing more than asked** — match work to the scope of the request
- **Incorrect Naming** — NEVER create/rename `ocas-*` without user authorization
- **Non-durable fixes** — put rules in skill's own git repo or MEMORY.md, not hermes core
- **Runaway repo creation** — check for 3rd-party skills before `gh repo create`
- **YAML block scalar truncation** — `description: >` / `|` contain newlines; use `read_file` + `patch`
- **`action` field is polymorphic in forge journals** — guard with `isinstance` before every access
- **Dispatcher `new_files` paths lack prefix** — check both profile-scoped and commons paths
- **Appending to JSONL files** — ALWAYS use `echo >>`, NEVER heredoc with `>`
- **`write_file` escapes quotes in Python files** — use `terminal()` with heredoc for .py files
- **Placeholder-then-patch anti-pattern** — never write placeholder strings intending to fix later
- **Heredoc `$(date)` timestamp mismatch** — compose TS into a variable first, use for both filename and content
- **Research is not optional for improvements** — MUST run Phase 1.5 research before touching files
- **`forge.update` vs `git pull` divergence** — cross-check git log against SKILL.md version field
- **`forge_audit_skills.py` is now functional (corrected 2026-07-14)** — The script at `scripts/forge_audit_skills.py` is a REAL compliance audit: it scans every `ocas-*` skill's `scripts/` for forbidden non-secret env-var config reads (`GENIE_*`, `<NAME>_MAX_AGE_DAYS`, `<NAME>_PATH`, `<NAME>_ENABLED`, etc.) and its `SKILL.md` body for env-var config tables, and exits non-zero on any blocking (ERROR) issue. Run `python3 scripts/forge_audit_skills.py` (or `--skill ocas-<name>` for one). It skips `.bak` files. When `forge.audit` is invoked, run this first — it is the standing gate, not a manual-only task. The pre-2026-07-14 stub note is obsolete.
- **`nargs='[]'` is invalid in argparse** — When defining command-line arguments, `nargs='[]'` is not a valid option and will cause a ValueError. To accept zero or more arguments, use `nargs='*'` instead. This caused the run_dispatch_pipeline.py script to fail until corrected.

The Forge build pipeline:

- [ ] Existence gate — check if skill already exists
- [ ] Research — search GitHub, arxiv, skill registries for patterns
- [ ] Classify — determine skill type and scope
- [ ] Scope — define boundaries and interfaces
- [ ] Architecture — design the package structure
- [ ] Plan — create implementation plan
- [ ] Build — implement the skill
- [ ] Validate — run critique and verify 50/50

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
- **Chronicle** — skill metadata and journal entries ingested for knowledge persistence

## Journal outputs

Action Journal — every build, critique, repair, validation, audit, and variant processing run.

## Initialization

On first invocation of any Forge command, run `forge.init`. Creates data
directories, writes default config, registers the `forge.update` cron job, and
logs the initialization decision. See `references/init_procedure.md` for the
exact sequence.

## Dispatch / Cron Integration

When triggered by dispatcher or `forge:journal-scan` cron, run these steps (full operational detail + all recovery/closure gotchas in `references/dispatch-integration-detail.md`; canonical decision procedure in `references/dispatch-pipeline-guide.md`):

- [ ] Check for unprocessed `vp_*.json` / `vd_*.json` in data root, `proposals/`, `intake/`
- [ ] Cross-reference against `intake/processed/` and `processed/` to skip already-processed files
- [ ] Process new files: build variants, apply fixes, queue for Mentor
- [ ] Move processed files to `processed/`
- [ ] If no unprocessed files: write no-op journal and exit
- [ ] Perform phantom file cleanup: after every dispatch run, `ls` journal dirs and fix empty/double/malformed timestamps (see `references/phantom-file-cleanup.md`)

**Critical dispatch rules (all detailed in the references file):** explicit-run prompt overrides the no-op shortcut; second-wave = add gaps + advance state, never write new journals; bridge all output journals into BOTH eval stores idempotently by full relative path (never basename); advance `last_ingest_run` past max mtime of ALL touched journals INCLUDING post-dispatch mentor-cron heartbeats, then RE-SWEEP to GENUINE GAP = 0; recoveries REWRITE the existing wave journal (never mint a new one); for post-state closure, iterate `scripts/closure_convergence_sweep.py --date <DATE>` to 0 additions then assert `GENUINE GAP = 0` via `scripts/verify_genuine_gap_profile.py --date <DATE>` (both confirmed present on disk 2026-07-15; the prior note that `reconcile_*`/`verify_*`/`closure_*` helpers "do NOT exist on disk" is obsolete for these two — see `references/dispatch-closure-sequence.md`). NEVER `rm -rf` the `home/` tree — only the doubled `home/.hermes` node.
- **Pipeline scripts do NOT advance `ingest_state.json` (confirmed 2026-07-13 explicit-run dispatch):** Neither `ocas-praxis/scripts/praxis_ingest_run.py` nor `ocas-mentor/scripts/cron-heartbeat-light.py` writes `ingest_state.json` — verified by grepping both for `write_state` / `last_ingest_run` / `json.dump(.*state)` (only `json.dumps` for evidence serialization appears). `run_dispatch_pipeline.py` DOES advance state in its second-wave branch, but under the explicit-run override you skip that script and run the real heartbeat + ingest yourself — so state advancement becomes the caller's job. **State-advance rules (both re-detection-closure AND explicit-run branches):** (1) Set `last_ingest_run` to a timestamp strictly greater than the max mtime of **ALL** journals the walk touches — every output journal you wrote, every gap/residual journal the convergence sweep bridged, **AND** any post-dispatch mentor-cron heartbeat that landed during the bridge (the mentor-cron loop writes a `mentor-light-*.json` ~every 5 min, including inside the state-write window). Do NOT derive it from only the 4 named output journals — a heartbeat bridged by the sweep but below `last_ingest_run` coverage re-fires the dispatcher every cycle (confirmed 2026-07-15 re-detection run: advanced to the max mtime across all 117 today-dated journals, not just `new_files`). (2) **RE-SWEEP after advancing state:** the advance is a separate `json.load`+`write_file`; a heartbeat can land between your pre-advance sweep and the write. Run `scripts/closure_convergence_sweep.py --date <DATE>` again and iterate to 0 additions, THEN run `verify_genuine_gap_profile.py --date <DATE>` and assert `GENUINE GAP = 0`. Declaring closure between the state write and the post-advance sweep silently leaves a gap that re-fires the next scan. (3) Resync `journals_evaluated_count` / `last_eval_file_line` to the actual eval-file line count (the scripts' own counters drift). Forgetting (1)/(2) leaves `last_ingest_run` stale and the next scan re-detects the same files as gaps. See `references/session-20260713-dispatch-explicit-run.md` for the verified end-to-end caller-side bridge procedure, and `references/session-20260715-mixed-wave-closure.md` § "Closure ordering refinement" for the post-advance re-sweep.

**Multi-skill dispatch:** Forge runs independently — scan for variants, write no-op if clean. Don't block on sibling skills.

**Explicit dispatch prompt overrides the no-op shortcut (confirmed 2026-07-07):** When the dispatcher's `type` is `new_journals` and its `prompt` contains an EXPLICIT instruction to run the pipelines (e.g., "run Forge journal scan", "run Mentor light heartbeat", "run Praxis journal ingest"), that instruction takes precedence over the dispatch-pipeline-guide's genuine-no-op shortcut. Even if every `new_file` is already content-evaluated in praxis eval and all content is routine, the pipelines must still be executed — the run itself is the deliverable. Expected outcome: all resolve to no-op (Forge: 0 unprocessed proposals → forge-scan no_op journal; Mentor: self-referencing heartbeat; Praxis: only Bug-2 noise lessons + no_signal events). After running, still write the pipeline output journals (forge-scan, praxis-dispatch, the heartbeat's mentor-light) and apply third-wave eval mitigation — do NOT suppress them, because the pipelines actually executed and produced real output journals. The shortcut applies only to routine re-detections (second-wave / `dispatch.wave` meta-journals) with no explicit run instruction.

**EXCEPTION — explicit-run wave that is itself a completed re-detection (confirmed 2026-07-13T14:50Z):** If a PRIOR identical explicit-run wave already executed the three pipelines, wrote its `forge-scan-*` journal, ran the real Mentor heartbeat + Praxis ingest, and bridged everything except a residual one-sided gap, then the CURRENT explicit-run wave is a re-detection of an ALREADY-COMPLETED run. Detect this pre-flight: (a) all dispatcher `new_files` already present in BOTH eval files, (b) a `forge-scan-*.json` for the wave's timestamp window already exists, (c) `ingest_state.last_ingest_run` already past all `new_file` timestamps. When all three hold, DO NOT re-run Forge/Mentor/Praxis — re-running writes duplicate journals and violates the anti-journalization hard gate (confirmed failure mode 2026-06-28/06-29). Instead: close ONLY the residual one-sided eval gaps (bounded per-skill `os.listdir` walk of `commons/journals/ocas-*/YYYY-MM-DD/` — NOT recursive `glob`/`os.walk`, which descends into self-nested `journals/journals/...` symlinks and emits dozens of false-positive "gap" hits per `references/dispatch-verify-closure-pitfalls.md`; bridge any live on-disk file present in praxis-eval but absent from dispatch-eval, OR present in dispatch-eval but absent from praxis-eval, OR absent from BOTH), advance `last_ingest_run`, and exit. Note: a genuine (non-re-detection) dispatch can leave its two `new_files` split across the two eval files in OPPOSITE directions at once — one present only in praxis-eval, the other present only in dispatch-eval (confirmed 2026-07-13T16:47Z: `ocas-custodian/.../esc-loop-...json` praxis-only, `ocas-mentor/.../mentor-light-...json` dispatch-only). The bridge Step 4 per-file both-eval idempotent append handles this; the re-detection shortcut's one-sided-gap list must enumerate BOTH orientations. Verify GENUINE GAP = 0 via bounded per-skill `os.listdir` (NOT recursive `glob`/`os.walk`) compared against the profile-scoped dispatch + praxis eval membership sets, matching the recipe in `references/dispatch-verify-closure-pitfalls.md`.

**EXCEPTION pre-flight false-negative — `forge-<TS>.json` naming + wave-journal-content check (confirmed 2026-07-14T12:21Z):** The EXCEPTION re-detection shortcut requires condition (b) "a `forge-scan-*.json` for the wave's timestamp window already exists." BUT some waves emit the Forge output as `forge-<DATE>T<ts>Z.json` (NO `-scan` suffix) instead of `forge-scan-<ts>.json`. When (b) is FALSE, do NOT immediately conclude the full 3-pipeline must re-run. Read the prior `dispatch-wave-*.json` journal's `outcome`/`notes`: if it records real pipeline execution (e.g. "GENUINE GAP=0", "Path A verify_evidence_threads", explicit "bridged … as cross_skill_mitigation", with `forge-*`/`praxis-*` output journals present on disk), the pipelines ALREADY ran — treat as a completed re-detection and SKIP re-run (re-running double-writes journals, violating the anti-journalization hard gate). Correct action: bridge residual gaps + advance `last_ingest_run` + rewrite the existing wave journal (`state_updated:true`). At 12:21Z, the wave had NO `forge-scan-12:19*` yet its `forge-20260714T121430Z.json` + `praxis-20260714T121430Z.json` outputs were on disk and its notes said "GENUINE GAP=0" — a completed re-detection, not a fresh wave.

**Convergence sweep MUST be UNGATED (confirmed 2026-07-15):** `verify_genuine_gap_profile.py` walks ALL today-dated journals with NO mtime filter. Any convergence sweep that gates on `mtime > cutoff` (e.g. `os.path.getmtime(fpath) <= max_mtime: continue`) will SKIP journals missing from the dispatch-eval store but written BEFORE the cutoff — they then surface as genuine gaps on the final assertion (this session: two `mentor-light` heartbeats at 03:48/03:50, present in praxis-eval but missing from dispatch-eval, reported as GENUINE GAP=2). **Fix:** run `scripts/closure_convergence_sweep.py` (ungated, mirrors verify's walk) and iterate until it bridges 0; do NOT use a cutoff-gated sweep. Loop: sweep → assert → repeat if still >0.

**Mentor-cron heartbeat convergence loop (confirmed 2026-07-14T12:21Z):** The `ocas-mentor` light heartbeat cron writes `mentor-light-*.json` roughly every ~5 minutes. Any recovery spanning >5 min will see a NEW heartbeat land AFTER the wave closed (post-dispatch-cron-gap pattern #155, occurring DURING recovery). After bridging gaps and advancing `last_ingest_run`, RE-SWEEP once more; if any new cron journal with mtime above the prior cutoff appears, bridge it into BOTH eval stores and re-advance, then sweep again. Iterate until a sweep yields 0 gaps. In this recovery, `mentor-light-20260714T122113Z.json` (12:21:13) appeared after the prior wave closed, and a SECOND `mentor-light-20260714T122538Z.json` (12:25:38) appeared during the recovery itself — both bridged across two convergence passes. Declaring closure after a single pass re-fires the dispatcher on the next scan.

**Self-consistency rule (confirmed 2026-07-13T18:55Z):** Every explicit-run wave MUST complete Step 1 (write its own `forge-scan-*.json` for the wave's timestamp window) AND Step 4 (advance `ingest_state.last_ingest_run` past the max mtime of all processed journals). If a PRIOR explicit-run wave misclassifies itself — e.g. writes "No pipeline re-runs" / second-wave, skips BOTH its forge-scan journal AND the state advance — then the CURRENT wave's pre-flight conditions (b) `forge-scan-*.json for the window exists` and (c) `last_ingest_run` past new_file timestamps will BOTH be FALSE even though (a) all new_files in both eval files is TRUE. The EXCEPTION shortcut will NOT fire and the full 3-pipeline run executes again — a redundant re-run that also double-writes dispatch-wave journals. At 18:55Z this exact situation occurred: the 18:53Z wave had left `last_ingest_run` at 18:16:16 and written no `forge-scan-*.json` for the 18:5x window, forcing a full re-run. The fix is upstream of the EXCEPTION check: an explicit-run wave must NEVER exit without its own `forge-scan-*.json` and an advanced `last_ingest_run`, regardless of how it classified the new_files. If you are the CURRENT wave recovering such a prior misclassification: the prior wave likely already wrote AND self-registered a `dispatch-wave-<TS>.json` in both eval stores — do NOT mint a second wave journal, REWRITE that existing file (same Run ID) to reflect the genuine pipeline you ran (`classification: routine_no_op`, full `journal_pipeline` + `email_triage` notes, `state_updated: true`), since it is already idempotently registered. Minting a new `dispatch-wave-<NEWTS>.json` orphans the old one and can re-fire the dispatcher. Detection signals that a prior wave misclassified: `dispatch-wave-<TS>.json` on disk + registered in both eval stores, but `find commons/journals/ocas-forge/<DATE>/ -name 'forge-scan-*'` shows no scan for the wave's window AND `ingest_state.last_ingest_run` predates the `new_files` mtimes. Confirmed 2026-07-13T21:19Z: prior sibling wrote `dispatch-wave-20260713T211948Z.json` (all_second_wave) with no `forge-scan` and stale `last_ingest_run`; recovery ran full caller-side pipeline, advanced state, rewrote the existing wave journal, closed with GENUINE GAP: 0. See `ocas-dispatch` `references/dispatch-wave-execution-cron.md` § Recovering a prior wave that misclassified itself as `all_second_wave`.

- **RECOVERY PITFALL — `gap_backfill.py` gives a FALSE all-clear during recovery (confirmed 2026-07-14T07:58Z):** The ocas-praxis post-ingest checklist MANDATES `gap_backfill.py` to catch post-ingest gaps. But gap_backfill is **mtime-based** (`mtime > last_ingest_run`), and the ~7h12m mtime-lag gotcha (ocas-mentor #100) means the just-run genuine ingest's outputs (`mentor-light-*`, `forge-scan-*`) carry file-mtimes far behind their content timestamps. After a recovery ingest, gap_backfill prints `Found 0 unevaluated journals (mtime > last_ingest_run)` even though those outputs are **missing from the DISPATCH eval store** — the real Praxis ingest populates only the praxis-eval store, never the dispatch-eval store. A `0` from gap_backfill during recovery is NOT trustworthy. **Override it:** after the genuine ingest, run a full **two-store on-disk reconciliation** (glob `commons/journals/ocas-*/YYYY-MM-DD/*.json`, skip `dispatch-wave-*`; require every file in BOTH the praxis-eval store (key `journal_id`) AND the dispatch-eval store (key `filename`); bridge any missing one into BOTH. PREFER the now-WORKING `scripts/bridge_eval_inline.py` (`python3 scripts/bridge_eval_inline.py REL1 REL2 --require-exists --action my_label`) — it performs the idempotent dual-store append with a phantom guard. It was created 2026-07-15 and the long-standing "does NOT exist on disk" note in this gotcha is now OBSOLETE; use the script, falling back to the manual `append_unique_eval` helper (in `references/mixed-wave-redetection-closure.md`) only if the script is absent. Only a verified GENUINE GAP = 0 across both stores closes the re-fire loop. See `references/dispatch-recovery-gap-reconciliation.md` for the exact reconciliation pattern.

- **REWRITE-TARGET SELECTION (confirmed 2026-07-14T08:40Z):** A recovery must pick WHICH existing `dispatch-wave-*.json` to rewrite when 20+ candidates exist. Deterministic filter: among waves registered in BOTH eval stores for the date, keep those whose content `timestamp` `>=` max(mtime of detected `new_files`), then pick the MINIMUM such timestamp. That wave ran after the files appeared (so it could have processed them) but left `state_updated` unset / `last_ingest_run` stale — the misclassified one. Waves with `timestamp` BEFORE a new_file's mtime cannot have processed it; exclude them. Never mint a new wave. Detail in `references/session-20260714-dispatch-recovery.md`.

- **RECOVERY REWRITE journal is dispositive proof of pipeline execution (confirmed 2026-07-14T13:45Z):** When pre-flighting a re-detection, the existing `dispatch-wave-<TS>.json` for the run_id may itself be a RECOVERY REWRITE — recognizable by a `rewritten_at` field, a `summary` beginning `RECOVERY REWRITE…`, and a populated `journal_pipeline` block recording `forge.ran` / `mentor.ran` / `praxis.ran` (with bridge counts) plus `actions_taken.state_updated: true`. This ALONE proves the three pipelines already executed for this wave — you do NOT need to independently locate a `forge-scan-*.json` or re-run them. Two cheap confirms before declaring closure: (1) the output journals named in `journal_pipeline.forge.journal` and `journal_pipeline.mentor.heartbeat_journal` exist on disk; (2) both dispatcher `new_files` are present in BOTH eval stores and `ingest_state.last_ingest_run` (read via `json.load`, NEVER `read_file`) is past their timestamps. If both hold → apply the EXCEPTION closure (bounded per-skill `os.listdir` gap walk; bridge residual one-sided / post-dispatch cron gaps into BOTH eval stores idempotently; advance `last_ingest_run`; convergence re-sweep to 0 gaps) and exit. Do NOT mint a new wave journal — the rewrite already exists and is idempotently registered. **Closure phantom-guard scoping:** when verifying closure, scope the on-disk-existence check to CURRENT-WAVE entries (source == this run's tag). A full-store walk will re-flag pre-existing mis-anchored `commons/journals/…` eval entries from earlier same-day waves — do NOT auto-fix those (unscoped historical cleanup is forbidden by the cleanup rule). In the 2026-07-14T13:45Z wave, 6 such legacy entries (05:34 / 09:59 / 10:05) were correctly left untouched.

- **Newer concurrent wave already closed this detection (confirmed 2026-07-14T14:59Z):** A re-detection may be redundant because a DIFFERENT, LATER dispatch wave (timestamp AFTER the current dispatcher's `detected_at`) already fully processed the same `new_files` (same journal paths + same email threads) — not because the same wave's prior run left it half-done. Detection: grep `dispatch-wave-*.json` for entries with `timestamp > detected_at` whose `summary`/`notes` reference the same files/threads (e.g. a Kyra Jones `<thread-id>` thread, the same `mentor-light-*.json` paths). If such a wave recorded `genuine_gap=0` / email `action:none`, the current wave is doing already-done work. **Do NOT re-run Forge/Mentor/Praxis. Do NOT mint or rewrite a wave journal** (it orphans the existing one and can re-fire). Execute closure-only: (1) bridge residual post-wave cron gaps with the **manual dual-store append** (key `journal_id` for praxis-eval, `filename` for dispatch-eval) — OR PREFER the now-WORKING `scripts/bridge_eval_inline.py` (`python3 scripts/bridge_eval_inline.py REL1 REL2 --require-exists --action my_label`); it performs the same idempotent dual-store append with a phantom guard and was created 2026-07-15 (the "does NOT exist on disk" note here is OBSOLETE). The mentor-cron convergence loop is CONTINUOUS (a heartbeat lands every ~5 min), so bridge then RE-SWEEP with a bounded `os.listdir` loop that advances `last_ingest_run` to the newest bridged mtime, iterating until a sweep adds 0 — a single pass is never permanently stable. INCLUDE the post-wave heartbeat journal. (2) verify `last_ingest_run` via `json.load` (NEVER `read_file` — it can return a cached/stale copy) — if stale despite the prior wave's claimed `state_updated:true`, advance it past ALL journal mtimes in the wave INCLUDING post-wave cron heartbeats; use full-file `json.load` + `write_file` (do NOT use `patch`: its fuzzy matcher skips intermediate lines and can insert a duplicate key, yielding malformed JSON — confirmed 2026-07-14T17:04Z), and resync `journals_evaluated_count` + `last_eval_file_line` to the actual eval-file line count, (3) fix the email state file (`commons/data/ocas-dispatch/owner/last_email_check.json`) — the bridge script NEVER touches it, so a stale `last_dispatch` re-fires the email item indefinitely. The stale `last_ingest_run` (not the journals) is what keeps the dispatcher re-firing. **Conditional-rewrite refinement (confirmed 2026-07-15):** only rewrite the email state file if it is ACTUALLY STALE — i.e. its `last_dispatch` does NOT match the current wave's `detected_at`/`timestamp`, or `verified_second_wave` is not already `true`. In a re-detection where the earlier wave already set `verified_second_wave:true` with `last_dispatch` = this wave's timestamp, the file is already correct — do NOT rewrite it; a needless full-file `write_file` rewrite of an already-correct state file risks the duplicate-key JSON corruption pitfall (confirmed 2026-07-14T17:04Z) for zero benefit. Re-read the file first and skip the rewrite when it already reflects this wave. Then run `scripts/verify_genuine_gap_profile.py --date <DATE>` and assert GENUINE GAP = 0. See `references/session-20260714-dispatch-1459Z-redetection-closure.md`.

- **`bridge_explicit_run.py` writes a wrong-account `email_triage` stub (confirmed 2026-07-14):** The dispatch-wave journal template hardcodes `"email_triage": {"indigo_inbox": {"threads_reviewed": 0, "actionable": 0}}`. For a mixed `new_journals` + `new_emails` wave this is wrong on two counts: (1) the account is usually `owner`, not `indigo`; (2) for an email second-wave (all threads `is_new:false`) the correct record is `actionable: 0, classification: "second-wave"` with a note that no triage/sends occurred. **After the script returns `DONE`, patch the dispatch-wave journal's `email_triage` block** to name the real account and record the email second-wave classification. **Separately, update the AUTHORITATIVE email state file** at the **account-subdirectory** path — `<hermes-home>/commons/data/ocas-dispatch/owner/last_email_check.json` (or `indigo/` for my mailbox). Do NOT write to the legacy flat files: the `commons/data/ocas-dispatch/last_email_check_owner.json` root copy is a STALE snapshot, and `scripts/last_email_check_owner.json` is a dead legacy file from before the account-subdirectory migration. Writing either leaves the real state un-updated and the next scan re-detects the threads. Set `last_dispatch` to the dispatch `detected_at` (or current time), `last_dispatch_wave` to the wave run_id, `last_dispatch_note` (e.g. `"second-wave, 0 actionable, N threads re-detected (is_new=false) — no triage, no sends"`), and `verified_second_wave: true`. **Stale-read guard (2026-07-14):** the profile `commons` tree is reachable both as the real path and via the symlink target it resolves to (`<hermes-root>/commons/...`). A relative read through a symlinked cwd returned a STALE June-28 copy while the real file already held the July-14 structure. ALWAYS address the state file by its FULL ABSOLUTE profile path, re-read IMMEDIATELY before writing (a prior/concurrent wave may have changed it). When the change touches MULTIPLE NON-CONTIGUOUS fields inside a JSON state file, do NOT use `patch` — its fuzzy matcher aligns the old_string's first/last lines but SKIPS the lines between, and if the replacement re-introduces a key already present elsewhere (e.g. `timestamp`), it produces a DUPLICATE KEY (confirmed 2026-07-14T17:04Z: patching `owner/last_email_check.json` dropped `last_check_ts` and inserted a second `"timestamp"` line, yielding malformed JSON). Instead, re-read the full file with `read_file`, then `write_file` the complete corrected object — the JSON lint validates it and prevents duplicate/displaced keys. Reserve `patch` for SINGLE contiguous localized edits on markdown/journal files. In a single cron run (no concurrent writer of that exact file) `write_file` is safe. The bridge script does NOT touch email state files; the agent must. See `references/dispatch-pipeline-guide.md` § Complete Second-Wave, `skills/ocas-dispatch/references/email-second-wave.md`, and `references/session-20260714-dispatch-1706Z-closure.md` for the full closure recipe + the `patch`-corruption repro.

  - **PHANTOM `dispatch-wave` filename in `os.listdir` (confirmed 2026-07-14 live recovery):** When pre-flighting a recovery, a `dispatch-wave-<detected_at_TS>.json` may appear in `os.listdir(commons/journals/ocas-dispatch/<DATE>/)` — its name matches the dispatcher's `detected_at` — but the file is **NOT on disk**: `read_file` fails "File not found" and `ls` confirms absence. This is a transient phantom entry, NOT the real rewrite target. **Do NOT trust the `os.listdir` name to pick the rewrite target.** Instead, find the genuine prior-wave journal by eval-store membership: the `dispatch-wave-<TS>.json` present in BOTH `journals_evaluated.jsonl` stores (praxis `journal_id` + dispatch `filename`) whose run corresponds to the misclassified wave IS the file to `write_file`-rewrite (it is already idempotently registered, so rewriting it is safe). In this session the phantom `*065523Z` (matching detected_at 06:55:22) was ignored and the real `dispatch-wave-20260714T064843Z.json` (in both eval stores) was rewritten. Always `ls`/`os.path.exists` verify any wave filename surfaced only by `os.listdir` before acting on it.

**Mixed `new_journals`(dispatch-eval gap) + `new_emails`(second-wave) in ONE wave (confirmed 2026-07-14T21:50Z):** A single dispatcher fire can carry BOTH a `new_journals` item whose journal is in the PRAXIS eval store but **absent** from the DISPATCH eval store (a one-sided eval gap = the genuine re-fire cause) AND a `new_emails` item whose threads are ALL `is_new:false` with the account-state file already `verified_second_wave:true`. Resolve as: (1) `new_journals` = GENUINE dispatch-eval gap → run the FULL explicit-run pipeline (Forge no-op scan, real Mentor heartbeat, real Praxis ingest) and bridge ALL pipeline outputs + the genuine-gap journal + any sibling post-dispatch cron journals (e.g. later `mentor-light-*`) into BOTH eval stores (idempotent, phantom-guarded). (2) `new_emails` = REDUNDANT re-detection → do NOT re-triage; the prior wave already closed any Path-B gaps and recorded them in its triage evidence journal (`ocas-dispatch/<DATE>/triage-*.json`). That triage journal is itself a genuine dispatch-eval gap (praxis-eval present, dispatch-eval absent) — bridge IT too so it cannot re-fire, using the now-WORKING `scripts/bridge_eval_inline.py` (`python3 scripts/bridge_eval_inline.py REL1 REL2 --require-exists --action my_label`) which performs the idempotent dual-store append with a phantom guard (created 2026-07-15; the earlier "does NOT exist on disk" note is OBSOLETE), or the manual `append_unique_eval` helper in `references/mixed-wave-redetection-closure.md`. (3) Re-affirm the account state file's `verified_second_wave:true` for THIS wave via full-file `write_file` rewrite (re-read immediately before writing; never `patch` — see the duplicate-key corruption pitfall) WITHOUT touching the inbox. Emails in a second-wave obey the hard rule 2026-06-24: no inbox changes, no drafts, no sends. CLOSING THE DISPATCH-EVAL GAPS (not the email re-detection) is what stops the dispatcher re-firing. Verify GENUINE GAP = 0 via bounded per-skill `os.listdir` (NOT recursive `glob`/`os.walk` — self-nested symlinks); the ~15 residual gaps are custodian self-bridged cron journals, excluded by design. Full recipe: `references/session-20260714-dispatch-2150Z-mixed-gap-secondwave.md`.

**Second-wave detection:** If journal timestamp is BEFORE dispatch `detected_at` → second-wave. Write no-op. If ANY `new_file` not in eval file → genuine dispatch, run full pipeline.

**Consolidated reference:** The multi-skill dispatch workflow is now documented in `references/dispatch-pipeline-guide.md`. Read this before running any dispatch pipeline for the canonical decision procedure.

  - **Eval file gap edge case (confirmed 2026-06-26 dispatch #142):** Even when `last_ingest_run` is set to a timestamp AFTER a journal's file timestamp, that journal can still be MISSING from the eval file. The Praxis state's `last_ingest_run` is updated at the END of a dispatch wave, but individual journals from that wave may not have been added if the eval check was skipped. **Fix:** During second-wave handling, ALWAYS check each dispatcher `new_file` individually against the eval file with `grep -q "filename" eval_file` — never assume `last_ingest_run` coverage. If a journal is missing from eval file, add it before writing no-op journals. .
  - **Cron journal eval gap (confirmed 2026-06-26 dispatch #143):** Cron pipeline journals (`praxis-cron-*`, `mentor-light-*` from cron source) can also be missing from the eval file during second-wave detection. These are NOT dispatch-output journals — they're written by the cron pipeline between dispatch waves. One journal from a cron cycle may be present while another from the same cycle is absent (e.g., `mentor-light-063212Z` in eval but `praxis-cron-063348Z` missing). **Fix:** During second-wave, check ALL `new_file` entries against the eval file regardless of `source` field (dispatcher vs cron). Add any missing cron journals before writing no-op journals. **Third-wave scope for this pattern:** Add 7+ journals — 3 from current dispatch wave, 3 from detected dispatch wave, plus all missing cron journals from prior cycles. .
  - **Partial cycle gap between sibling pipelines (confirmed 2026-06-26 dispatch #146):** A sub-variant of the cron journal gap where one cron pipeline's journal is in the eval file but another cron pipeline's journal from the SAME cycle is absent. Example: `mentor-light-20260626T073205Z` present in eval, but `praxis-cron-20260626T073343Z` (written 90 seconds later by the cron pipeline) missing. Root cause: Praxis cron ingest processed the mentor journal but completed before the praxis-cron journal was written, or the eval check only covered journals already in the state's `last_ingest_run` window. **Fix:** Same universal rule — `grep -q "filename" journals_evaluated.jsonl` for EVERY `new_file` individually, regardless of whether sibling journals from the same cycle are already present. Never infer that "if mentor-light is evaluated, praxis-cron from the same cycle must be too."
  - **Dispatch-output eval gap (confirmed 2026-06-26 dispatch #144):** Prior dispatch wave's own output journals (`forge-scan-*`, `praxis-dispatch-*`) can be missing from the eval file even when a sibling journal from the same wave IS present (e.g., `mentor-light-070339Z` in eval but `forge-scan-070643Z` and `praxis-dispatch-070643Z` missing). **Root cause:** The prior wave's Praxis ingest may evaluate only the mentor-light journal but not the forge-scan/praxis-dispatch journals before the ingest completes. `last_ingest_run` timestamp (07:06:55) is AFTER journal file timestamps (07:06:43), creating false confidence of coverage. **Fix:** During second-wave, always grep each `new_file` individually against the eval file — never assume same-wave journals share eval status. Add missing dispatch-output journals before writing no-op journals. .
  - **Post-ingest cron gap (confirmed 2026-06-26 dispatch #145):** Cron journals created AFTER `last_ingest_run` but BEFORE the next dispatch wave are missing from the eval file. The state's `last_ingest_run` reflects the last ingest OPERATION timestamp, not the last journal CREATION. Between waves, the cron pipeline continues writing new journals that the state doesn't know about. **Fix:** Same as other eval gap variants — grep each `new_file` individually against the eval file. This is the same root cause as the cron journal gap (#141, #143) but with a different trigger timing. .
  - **Hybrid second-wave with stale cron gap (confirmed 2026-06-26 dispatch #152):** A second-wave dispatch can contain BOTH self-referential dispatch-output journals (correctly in eval) AND stale cron journals from prior cycles that were missed by ALL prior waves. Example: 4 of 5 "new" files are our own dispatch-output (in eval), but 1 is `mentor-light-20260626T084028Z.json` from a prior cron cycle — NOT in eval. **Response:** Add the missing cron journal(s) to eval file, advance `last_ingest_run`, but do NOT write additional dispatch-output journals (that would create third-wave noise). The rule: second-wave = add gaps + advance state, never write new journals. .
  - **Combined before-ingest + dispatch-output gap (confirmed 2026-06-26 dispatch #159):** A genuine dispatch where the dispatcher's `new_files` are BEFORE `last_ingest_run` (pattern #4) AND a prior wave's dispatch-output journal is ALSO missing from eval (pattern #6). Both are caught by the per-journal grep. The broader `find` scan may reveal additional post-ingest cron gaps (pattern #3). **Response:** Full pipeline execution. Backfill ALL gaps found (dispatcher new_files + prior wave output + cron gaps). Apply third-wave mitigation for current dispatch output. This combination is normal when a prior wave's Praxis ingest completed before the forge-scan/praxis-dispatch journals were written. .
  - **Third-wave mitigation scope:**
- **Third-wave self-referential pattern (confirmed 2026-06-22):** After a multi-skill dispatch, the dispatcher re-scans and detects journals written by the dispatch's own run (forge-scan, praxis-dispatch, mentor-light). This is the **second wave** — expected and harmless if journals are already in Praxis's eval file. But a **third wave** can occur when the forge-scan or praxis-dispatch journal is written AFTER the Praxis ingest updates `last_ingest_run`. These journals have mtimes after the state timestamp, so the dispatcher detects them as "new" again. **Mitigation:** After the Praxis ingest completes, the caller must also add all dispatch-output journals (especially forge-scan) to `journals_evaluated.jsonl` and advance `last_ingest_run` past their mtimes. See `references/session-20260622-dispatch.md`.
- **Phantom file cleanup pattern (confirmed 2026-06-25 dispatch #100, 2026-06-26 dispatch #150):** When writing JSON journals via `python3 -c` inside `terminal()`, f-string curly braces `{}` can be silently consumed by bash's `${}` expansion, producing files with empty or corrupted names (e.g., `forge-scan-.json`). Double timestamps can also occur (e.g., `dispatch-20260626T20260626T082335Z.json`) when shell variable interpolation duplicates the timestamp. After every dispatch run, `ls` the journal directory and check for files with empty timestamp fields, double timestamps, or malformed names. Rename/fix any phantom files before they get detected as "new" by the next dispatcher scan. **Beware false positives:** during 2026, timestamps in the 20:xx:xx hour range (e.g., `T202602Z` = 20:26:02) will contain "2026" in the time portion — this is valid, not a phantom. See `references/phantom-file-cleanup.md`.
- **Path typo: `oras-praxis` vs `ocas-praxis` (confirmed 2026-06-29 dispatch):** When constructing the Praxis data directory path, a single-character typo (`oras-praxis` instead of `ocas-praxis`) causes `cp` and `python3` to fail with "No such file or directory". **Fix:** The canonical path is `<hermes-home>/commons/data/ocas-praxis/` — always verify with `ls -d <hermes-home>/commons/data/oca*` before constructing script paths. The skill name is `ocas-` (with `s`), not `ora-`. Confirmed: `cp template /root/.../oras-praxis/script.py` failed silently, then `python3 /root/.../oras-praxis/script.py` raised FileNotFoundError. When using `cat > file << EOF` inside `terminal()`, any commands placed AFTER the JSON/YAML content but BEFORE the `EOF` delimiter are treated as heredoc body text and written into the file. Example: `cat > "$DIR/file.json" << EOF\n{...json...}\necho "Written: ..."\ncat "$DIR/file.json" | python3 -c "..."\nEOF` — the `echo` and `cat` lines end up inside the JSON file, corrupting it. **Fix:** Never place commands after the file content in a heredoc. If you need to verify the file, do it in a SEPARATE `terminal()` call. Better yet, use `write_file` for JSON/YAML — it's atomic, validates syntax, and can't leak trailing commands. Confirmed 2026-06-26: `forge-scan-20260626T014859Z.json` contained valid JSON followed by `echo "Written: ..."` and `cat ... | python3 ...` lines.
- **`execute_code` is blocked in cron mode** — When running as a scheduled cron job, `execute_code` is rejected with: "BLOCKED: execute_code runs arbitrary local Python (including subprocess calls that bypass shell-string approval checks). Cron jobs run without a user present to approve it." **Fix:** Use `terminal()` with a heredoc Python script instead: `python3 << 'PYEOF'\n...code...\nPYEOF`. This is the cron-safe way to run multi-step Python that walks filesystems, builds sets, or processes JSON. Confirmed 2026-06-26 dispatch: Praxis journal ingest scan (walk 10k+ files, compute set difference) had to use `terminal()` heredoc instead of `execute_code`.
- **`skill_view`/`search_files`/`read_file` can ALL fault with the same transient backend API error in cron (refined 2026-07-15T23:50Z):** In one live dispatch run, `skill_view(name=...)`, `search_files`, AND `read_file` each returned `Error during OpenAI-compatible API call #N: 'DaemonThreadPoolExecutor' object has no attribute '_initializer'`. All three route through the same LLM-backed tool path, so when one faults the others usually do too. Only the pure-shell `terminal()` tool stayed reliable (`cat` the SKILL.md, or `python3 << 'PYEOF'` heredoc for JSON). An autonomous dispatch must NOT abort when the skill-read fails. **Fix:** if any of those three error, go STRAIGHT to `terminal()` — `find <hermes-home>/skills -name SKILL.md | grep <name>` then `cat` the file (or `python3` for JSON state) — and proceed from the on-disk SKILL.md + `scripts/`. Do NOT substitute `read_file` as the fallback; it can hit the same fault. The pipeline is fully runnable without `skill_view`; the verified `references/mixed-wave-closure-one-shot.md` runbook is a plain file you can `cat`. Treat this as a retry/fallback path, NOT a permanent "tool is broken" conclusion — the backend error is likely transient (it cleared mid-session).
- **FALSE "stale `last_ingest_run`" diagnosis when verifying closure (confirmed 2026-07-15T23:37Z):** If you independently recompute max journal mtime across `commons/journals/<skill>/<DATE>/*.json` to check whether `last_ingest_run` is advanced far enough, you WILL see a file newer than `last_ingest_run` — your OWN `dispatch-wave-<TS>.json` meta-journal (written/edited during the run, so it is the run's max mtime). `dispatch_redetection_close.py` deliberately EXCLUDES `dispatch-wave-*` from its mtime computation (the `fn.startswith('dispatch-wave-'): continue` guard sits BEFORE the `mt > max_mtime` line), and the dispatcher never re-detects `dispatch-wave-*` as new work. So a `dispatch-wave-*.json` being newer than `last_ingest_run` is EXPECTED and SAFE — do NOT treat it as a re-fire risk or re-advance state to cover it. CORRECT CHECK: max mtime over all NON-`dispatch-wave-*.json` journals must be `<= last_ingest_run`; a genuine non-meta journal (mentor-light, custodian, forge-scan) newer than the state IS the real gap. Full pre-flight recipe + this pitfall in `references/dispatch-explicitrun-closure-recipe.md`.
- **`write_file` line-wrapping corrupts Python (confirmed 2026-06-30T10:20Z)** — The `write_file` tool silently wraps long lines (~80 chars), splitting Python string literals and variable assignments mid-token. Example: `"<hermes-home>/..."` becomes `"/rootfiles/indigo/..."` and two separate `VAR = "..."` assignments merge into one corrupted line. **Fix:** After writing Python via `write_file`, run `python3 -c "import py_compile; py_compile.compile('/tmp/script.py', doraise=True)"` before executing. For scripts >30 lines, write to `/tmp/`, compile-check, then run. See `references/dispatch-pipeline-guide.md` § write_file line-wrapping corrupts Python.
- **`run_dispatch_pipeline.py` Python 3.14 compatibility** — Previously experienced issues related to argparse nargs configuration (fixed by using `nargs='*'` instead of invalid `nargs='[]'`). Verified working correctly on Python 3.14 in dispatch scenarios as of 2026-06-30.
- **Praxis-cron double-Z timestamp bug still active** — The Praxis cron ingest script continues to produce journals with double-Z suffixes (e.g., `praxis-cron-20260630T092758ZZ.json`). Root cause is `ts.rstrip('Z') + 'Z'` applied to a value already ending in Z. **Mitigation:** dispatch pipeline treats these filenames as-is for eval registration. Fix needed in `praxis_ingest_run.py` / `praxis_common.py`. Confirmed 2026-06-30.
- **Inline Python blocks compose their own timestamps independently of prior shell `TS` variables** — When a Forge/Mentor/Praxis pipeline writes journals in one `terminal()` call (using a shell `TS=$(date ...)` variable) and then runs eval/third-wave logic in a SEPARATE `terminal()` call with inline Python, the Python block's `datetime.now()` diverges from the shell `TS`. Third-wave eval entries then use the Python timestamp for journal IDs that were written with the shell timestamp — producing phantom entries referencing non-existent files. **Fix:** Compose ALL timestamps inside the SAME Python block, or write actual journal filenames to a temp file so subsequent steps read them verbatim. Never carry a shell `TS` across `terminal()` boundaries and assume inline Python will match it. Confirmed 2026-06-29 dispatch.
- **Hand-written verification-closure path traps (confirmed 2026-07-14):** When you write your OWN post-dispatch verify/closure step (phantom guard + post-dispatch gap walk), two path bugs produce false alarms. (1) **Phantom-guard base segment** — journals live under `commons/journals/<skill>/...`, NOT `commons/<skill>/...`; `os.path.join(COMMONS, rel)` (COMMONS=`.../commons`) resolves to a non-existent path and flags every bridged journal a phantom. Anchor on `.../commons/journals/`. (2) **Recursive-glob nesting artifact** — `glob(..., recursive=True)` over the journals tree descends into self-nested `journals/journals/...` symlink self-references and returns the same file under mangled relpaths, producing dozens of false "gap" hits. Walk per-skill with a bounded `os.listdir` instead. Full recipe in `references/dispatch-verify-closure-pitfalls.md`.
- **`bridge_eval_inline.py` `--action` value leaks as a path (confirmed 2026-07-14T19:22Z):** The script's original parser built `rels = [a for a in argv if not a.startswith("--")]`, which KEEPS the token that follows `--action` (it does not start with `--`). Passing `--action post_dispatch_convergence_gap REL2 REL3` therefore writes a BOGUS eval entry `"filename": "post_dispatch_convergence_gap"` into BOTH eval stores, and the next gap sweep re-flags it as a phantom (the exact phantom-entry failure mode the skill warns against). Fixed 2026-07-14 by skipping the value index in the parser (`scripts/bridge_eval_inline.py` — `main()` now walks argv and consumes the value after `--action`). If a post-bridge sweep reports a non-path token as `filename`/`journal_id`, strip that line (`grep '"filename": "<token>"`) and re-bridge only the intended relative paths — do not leave the bogus entry. Safest invocation: put `--action <label>` at the END of the arg list: `python3 scripts/bridge_eval_inline.py REL1 REL2 --action my_label`.
- **Dispatch-wave journal filename must use full `YYYYmmddTHHMMSSZ` format (confirmed 2026-07-14T12:40Z):** When writing the wave journal, derive the filename from `TS=$(date -u +%Y%m%dT%H%M%SZ)` — the complete 14-digit + `Z` form. A truncated timestamp like `dispatch-wave-20260714T1244.json` (missing seconds AND `Z`) creates a malformed filename whose `run_id` no longer matches the dispatcher's expected `YYYYmmddTHHMMSSZ` pattern, and risks a name collision / broken traceability. If you write the wave JSON in a SEPARATE Python step (not under the shell `TS` variable), do NOT recompose a shortened timestamp — reuse the exact `TS` string from the Forge/Mentor steps, or read back the filename the prior step actually wrote and echo its `run_id` verbatim into the wave journal. This session wrote `dispatch-wave-20260714T1244.json` and had to rename it to `dispatch-wave-20260714T124439Z.json`. See `references/session-20260714-dispatch-1240Z-forge.md`.
- **Dispatcher new_file vs heartbeat output journal divergence (confirmed 2026-06-29T04:40Z):** When a dispatch triggers a Mentor heartbeat, two mentor-light journals exist: (1) the dispatcher's `new_file` (e.g., `mentor-light-043547Z` — written by a prior cron heartbeat) and (2) the current heartbeat's output (e.g., `mentor-light-044551Z` — written by the script we just ran). Third-wave mitigation typically registers only journal #2 because it scans for recently-written files. Journal #1 (the dispatcher's original `new_file`) is a DIFFERENT file that also needs eval registration. **Fix:** After third-wave mitigation, ALWAYS re-grep each dispatcher `new_file` individually against the eval file. If any are missing, register them with `action_taken: "dispatch_new_journal_registration"`. Do NOT assume that registering the heartbeat's output covers the dispatcher's input — they are distinct files with distinct timestamps. Confirmed: `mentor-light-043547Z` was missed on first pass and caught by verification grep.
- **Post-dispatch cleanup can trigger massive legacy backfill** — The post-dispatch cleanup does a full `os.walk` of the journals directory and registers every `.json` file not in the eval file. If the eval file was created after journals started accumulating (mid-June 2026), the first cleanup will register hundreds or thousands of legacy files at once. This is a **one-time event** — after the initial backfill, only new journals will be caught. The eval file growing by 800+ entries in a single dispatch is normal for the first cleanup after eval tracking begins. Do NOT treat this as an error or re-processing event. Confirmed 2026-06-26 dispatch #160: 865 legacy files backfilled.
- **State file timestamp double-Z suffix** — When composing a timestamp like `20260626T%H%M%SZ` in Python and appending `"Z"`, the result can be `20260626T103652ZZ` if the format string already included `Z`. **Fix:** `ts.rstrip('Z') + 'Z'`. **Prevention:** Compose the timestamp once in a shell variable (`TS=$(date -u +%Y%m%dT%H%M%SZ)`) and reuse it for both filename and content. Never embed the timestamp in two separate string compositions. Confirmed 2026-06-26 dispatch #160: `ingest_state.json` had `last_ingest_run: "20260626T103652ZZ"`.
- **Cross-skill journal gap (confirmed 2026-06-26 dispatch #154):** After completing the standard Praxis ingest (processing the dispatcher's `new_files`), a broader gap can exist: journals from skills NOT in the dispatcher's detection scope, written by cron pipelines with non-standard filename conventions (e.g., `ocas-rally` uses `jrn_YYYYMMDD_HHMMSS.json`, `ocas-finch` uses `scan-NNNN.json` — both confirmed live non-standard naming a convergence sweep will encounter — instead of `*-dispatch-*` or `*-light-*`). These journals have timestamps between `last_ingest_run` and "now" but were never detected by the dispatcher. **Fix:** After the standard ingest completes, run a final `find` for ANY `.json` file in `{agent_root}/commons/journals/` with mtime after `last_ingest_run` that is NOT in the eval file. This catches cross-skill journals the dispatcher missed. Always do this before writing the dispatch-output journals (third-wave mitigation). .
- **Post-dispatch cron journal gap (confirmed 2026-06-26 dispatch #155):** After completing all 3 pipelines, backfilling eval gaps, AND applying third-wave mitigation, a cron pipeline can write additional journals between our eval backfill and our third-wave mitigation. These journals are NOT in the eval file and WILL be detected as "new" by the next dispatch. **Root cause:** The cron pipeline runs independently of the dispatch pipeline. Between the moment we read the eval file and the moment we add own-output journals, the cron pipeline can write new journals. **Detection:** After writing all dispatch-output journals and third-wave mitigation entries, do ONE MORE `find` for any `.json` file with mtime after `last_ingest_run` that is NOT in the eval file. **Response:** Add any found entries to the eval file with source `post-dispatch-cleanup`. Do NOT trigger another dispatch or re-processing — just append to eval and advance `last_ingest_run`. .
- **Complete eval gap pattern catalog (7 patterns, confirmed 2026-06-26):**

  | # | Pattern | Journal vs last_ingest_run | Gap Cause |
  |---|---------|---------------------------|-----------|
  | 1 | Cron journal gap (#143) | AFTER | Ingest ran before journal was written |
  | 2 | Tight eval gap (#151) | AFTER | Ingest ran between cron cycles |
  | 3 | Post-ingest cron gap (#145) | AFTER | Cron writes after ingest completes |
  | 4 | Before-ingest cron gap (#153) | BEFORE | Ingest didn't re-evaluate pre-existing journals |
  | 5 | Cross-skill gap (#154) | ANY | Dispatcher misses non-standard naming |
  | 6 | Dispatch-output gap (#144) | AFTER | Prior wave's own journals missed |
  | 7 | Post-dispatch cron gap (#155) | AFTER | Cron writes between our backfill and third-wave mitigation |

- **Eval file entries must use relative paths** — When writing to `journals_evaluated.jsonl`, the `journal` and `filename` fields MUST be relative to `{agent_root}/commons/journals/` (e.g., `ocas-forge/2026-06-26/forge-scan-TS.json`). Never use absolute paths (`<hermes-home>/commons/journals/...`). Absolute paths break the dispatcher's grep-based eval checks and cause false "gap" detection on subsequent dispatches. Confirmed 2026-06-26: third-wave mitigation wrote 3 entries with absolute paths, which had to be post-hoc corrected.
- **`grep -c` in shell conditionals produces unexpected exit codes** — `grep -c` returns count `0` AND exit code 1 when no matches found. In `count=$(grep -c ...) ; if [ "$count" -eq 0 ]`, the `[` test may behave unexpectedly with newline in output. **Fix:** Use `grep -q "pattern" file` for boolean checks (no output, correct exit code). Or use `grep "pattern" file > /dev/null 2>&1` then check `$?`. Never parse `grep -c` output as a variable for arithmetic comparison. Confirmed 2026-06-26 dispatch #142: `grep -c` returned `0\n0` (two lines) due to shell quoting, causing `[ "0\n0" -eq 0 ]` to fail with "integer expected".
- **Verification grep false negative from `$(date)` micro-differences** — When verifying that dispatch-output journals are in the eval file, the eval entry's timestamp may differ from the journal filename's timestamp by seconds (each is generated by a separate `$(date)` call). A `grep "forge-scan-20260626T092740Z"` check fails if the eval entry has `T092806Z`. **Fix:** Use partial timestamp matching for verification: `grep "forge-scan-20260626T0927"` (drop the last 2-3 chars of the timestamp). Or use `grep -q "dispatch-third-wave-mitigation"` to find all third-wave entries regardless of timestamp. Confirmed 2026-06-26 dispatch #156.
- **`ingest_state.json` in dispatcher `new_files` is not a journal** — The dispatcher lists `ocas-praxis/ingest_state.json` in `new_files` on every genuine dispatch because its mtime updates when state advances. This is NOT a journal that needs eval tracking — it's a state file. The eval file should already have an entry for it from the first dispatch that processed it. If grep confirms it's already in the eval file, skip it. If somehow missing, add it with source `state-file-init` but do NOT treat its presence as evidence of a genuine dispatch — it's always "new" because it's always being updated. Confirmed 2026-06-26 dispatch #157.
- **Eval entry path base: `commons/journals/` not profile root** — When constructing `journal_id` for `journals_evaluated.jsonl`, use `os.path.relpath(fpath, "commons/journals")` NOT `os.path.relpath(fpath, ".")`. The latter produces paths prefixed with `commons/journals/` which fail all grep lookups and cause false "gap" detection on every subsequent dispatch. Confirmed 2026-06-26: post-dispatch cleanup wrote a mismatched entry that had to be manually corrected. .
- **`read_file` returns stale/wrong state content — ALWAYS use Python `json.load()` for state files** — The `read_file` tool may return the commons-scoped copy, a cached version, or a file with a different schema than the profile-scoped `ingest_state.json`. In dispatch ~#161, `read_file` showed `last_ingest_run: "20260626T104320Z"` with fields like `dispatch_wave` and `eval_file_total`, while Python `json.load()` on the same path returned `last_ingest_run: "2026-06-26T10:36:03.950989+00:00"` with completely different fields (`journals_evaluated_count`, `note`, etc.). Trusting `read_file` would have caused misclassification as second-wave and missed 11 genuine journals. **Fix:** Always read state files via `python3 << 'PYEOF'` heredoc with `json.load()`. Never use `read_file` for JSON state that drives dispatch decisions. Cron-safe pattern: `python3 -c "import json; s=json.load(open('<hermes-home>/commons/data/ocas-praxis/ingest_state.json')); print(s['last_ingest_run'])"`. Confirmed 2026-06-26 dispatch ~#161.
- **`journals_evaluated_count` drift (confirmed 2026-06-26 dispatch ~#165)** — The `ingest_state.json` `journals_evaluated_count` and `last_eval_file_line` fields only increment by what the current dispatch explicitly adds. Post-dispatch cleanup entries (source `post-dispatch-cleanup`) are appended to the eval file without updating these counters. Over multiple dispatches, the state counter diverges from the actual eval file line count (e.g., state said 39603 while eval file had 39737 lines — a 134-entry drift). **Fix:** After post-dispatch cleanup completes, do a final `wc -l` (or Python line count) of the eval file and set both `journals_evaluated_count` and `last_eval_file_line` to the actual count. Not critical for correctness (grep checks are authoritative), but keeps diagnostics accurate.
- **`~` does NOT expand in `cd` inside `terminal()`** — When using `terminal()`, the tilde `~` is NOT expanded by bash in `cd ~/path` commands. Use absolute paths: `cd <hermes-home>/skills/ocas-forge`. Confirmed 2026-06-29: `cd ~/.hermes/...` failed with "No such file or directory".
- **Inline Python typo pitfall (`state_count` truncation + import shadowing + double-assignment)** — When writing multi-step gap backfill scripts as inline Python in `terminal()`, three specific errors have bitten the pipeline: (1) Truncated dict key like `state_count']` instead of `state['journals_evaluated_count']` causes SyntaxError. (2) Mixing `import datetime` with `from datetime import datetime` causes `AttributeError` on `datetime.now()`. (3) Chained dict assignment like `state["k1"] =["k2"] = val` → `SyntaxError: cannot assign to literal` (cannot chain-assign to dict keys — use one line per assignment). **Fix**: Local variables for dict keys; only `from datetime import datetime, timezone`; never chain-assign to dict keys. Confirmed 2026-06-30T10:35Z dispatch.
- **JSON journal writing in cron: prefer shell heredoc — When writing JSON journal files, inline Python heredocs (`python3 << 'PYEOF'` with dict literals containing double-quotes) suffer from (1) smart-quote corruption by the heredoc parser, (2) variable name truncation when identifiers appear immediately after closing quotes, (3) `SyntaxError: invalid decimal literal` from mangled dict literals. **Fix:** For output, use shell heredoc with pre-composed `TS=$(date -u +%Y%m%dT%H%M%SZ)` and `$NOW` variables. Reserve Python heredocs for eval file reads/writes where content is built programmatically (no raw double-quoted JSON). Confirmed 2026-06-30T11:25Z dispatch (6 consecutive failures before switching to shell heredoc). .
- **Pure eval-registration dispatch (confirmed 2026-06-30T11:25Z)** — A dispatch variant where ALL `new_files` need eval registration but NONE require pipeline skill loading. Detection: all `new_files` are either (a) already in praxis eval but missing from dispatch eval (bridge case), or (b) prior-wave dispatch-wave artifacts (timestamp < detected_at). **Response:** Grep each `new_file` against both eval files → register missing entries directly → write dispatch-wave journal with `classification: "mixed_genuine_no_op"` → advance `last_ingest_run` → skip all pipeline skills. Do NOT load Forge/Mentor/Praxis or run `praxis_ingest_run.py`. The `journals_evaluated_count` in state does NOT change (no praxis eval entries added). .

## Self-update

`forge.update` pulls the latest package from the `source:` URL in frontmatter.
Runs silently unless version changed or error.

**Drift detection procedure** (added 2026-06-23, extended 2026-06-29): Two distinct drift scenarios exist — handle BOTH:

**Scenario A — Origin ahead (upstream has new commits):** Dev installs can accumulate local commits that diverge from origin, causing `git pull` to falsely report "Already up to date." Before declaring up-to-date: (1) `git fetch origin`, (2) `git log --oneline HEAD..origin/main` — any output = upstream ahead, (3) `git diff --stat origin/main` — any diff = content drift regardless of commit history, (4) cross-check SKILL.md `version:` field against `git log origin/main --oneline -1` — frontmatter can lag commit messages. See Gotchas for conflict resolution when local modifications contradict upstream direction.

**Scenario B — Local drift (working tree dirty, origin NOT ahead):** When `git log HEAD..origin/main` is EMPTY but `git diff --stat origin/main` shows changes, OR when `git status` lists untracked files, the local working tree has accumulated modifications that origin doesn't have. This commonly happens when: session journals are written into `references/`, SKILL.md gets edited locally without committing, or new support files are added but not pushed. **Diagnostic:** `git status --short` — if output is non-empty with origin at same commit, you have local drift. **Response:** (1) Separate operational artifacts (session journals in `references/`) from skill content changes (SKILL.md edits, new reference docs). (2) Session journals should be moved to `commons/data/ocas-forge/journals/` — they do NOT belong in the skill repo. (3) Skill content changes should be committed and pushed, or stashed if experimental. (4) NEVER `git add .` blindly — this commits operational logs into the skill's git history. Confirmed 2026-06-29: 100+ session journals accumulated in `references/` over 7 days, causing `git diff --stat` to show 100+ untracked files with origin at same commit.

## Skill consolidation

`forge.consolidate` merges an orphan or duplicate skill into its natural parent.
See `references/builder_workflows.md` for the full workflow.

**Core rule:** fold merged content into the parent's existing section structure.
Do NOT wrap in `## Integrated:` sections.

**Consolidation hazard — a SKILL.md-less `ocas-*` dir is NOT automatically a removable orphan (confirmed 2026-07-13):** When auditing for orphans, finding a directory named `ocas-*` or `util-*` WITHOUT a `SKILL.md` does NOT mean it is safe to delete. It may be **live state storage** hard-coded as a `STATE_FILE` (or similar) by a sibling skill. Before removing any such dir: (1) `grep -rln "skills/<name>" . --include=*.py --include=*.json` across the whole tree — if any script references the path, it is load-bearing; (2) check the dir's contents' mtime — a recently-modified `*.json` inside means a running cron writes there. Real case from this audit: `ocas-critique/` had NO `SKILL.md` (already merged into `ocas-skilllab`, confirmed by `merged-from: ocas-critique` in skilllab's frontmatter) yet `ocas-skilllab/scripts/critique_10khr_runner.py` hard-codes `STATE_FILE = os.path.join(_HERMES_ROOT, "skills", "ocas-critique", "commons", "data", "ocas-critique", "10khr-state.json")`, and that file's mtime was 2026-07-12 (written by a cron) — deleting the dir would have broken the 10khr engine. Contrast the genuine orphan found same session: `ocas-10xeng-autofix/` (top-level) had no SKILL.md, only a stale `last_run.json` dated 2026-07-01, ZERO path references anywhere, and a real canonical copy at `software-development/ocas-10xeng-autofix/` — safe to move to `.archive/`. **Decision rule: only remove a SKILL.md-less `ocas-*` dir after BOTH grep-for-path returns no script/config references AND the dir's contents are not recently written by a cron.** Session detail: `references/session-20260713-audit-orphan-state-storage.md`.

## GitHub repo creation

Before creating any GitHub repo, verify the skill is OCAS-authored. See
`references/github_repo_guardrails.md` for the full guardrail checklist.

## Skill library search APIs

When Phase 1.5 triggers skill library research, use these APIs to understand approaches and patterns — not to copy verbatim.

- **SkillsMP** — `sk_liv...370I` key, https://skillsmp.com/docs/api
- **AgentSkill.sh** — `agentskill` CLI, https://agentskill.sh
- **LobeHub** — `lobehub` CLI, https://lobehub.com/cli
- **Skills.sh** — https://www.skills.sh/docs/api
- **OpenClaw** — `clawhub` CLI, https://docs.openclaw.ai/clawhub/cli
- **GitHub OCAS repos** — `gh search repos "ocas-* user:indigokarasu" --json fullName,description,url`

**Output of library search:** For each relevant skill found, note: name, description, how it works (architecture), what patterns it uses, and what the new skill can learn from it. Synthesize — don't clone.

When asked to audit sync state of all OCAS skills, or when running a scheduled
sync check, use the workflow in `references/sync_audit_procedure.md`.

## Skill audit

`forge.audit` audits one or more existing OCAS skills for architecture compliance,
applies fixes, and syncs to GitHub.

**Mandatory Configuration Policy gate (blocks submission to the Nous optional-skills catalog):** behavioral settings (thresholds, retention windows, feature flags, display prefs, paths) MUST NOT be read from environment variables — the hermes-sweeper auto-closes such PRs under the `env-var-for-config` policy. Correct mechanism: declare each setting in `metadata.hermes.config`, read it at runtime from `$HERMES_HOME/config.yaml` under `skills.config.<key>` (via PyYAML — `telephony.py` is the reference impl), document `skills.config.<key>` in SKILL.md (never env-var names), and let CLI flags override. Only secrets go in `.env`; only `HERMES_HOME`/`HERMES_PROFILE` locate the runtime.

Run the automated check first:
```bash
python3 scripts/forge_audit_skills.py --skill <ocas-name>   # 0 exit = clean
```
It flags any `GENIE_*` / non-secret env-var config read in `scripts/` or env-var config table in `SKILL.md`. The full written standard lives in `ocas-skilllab`'s `references/nous-skill-requirements.md` (Configuration Policy section) and `references/compliance-audit-checklist.md`.

## Platform notes
Forge uses the `memory` tool lightly — only for build state during multi-step builds.

## Support File Map

| File | When to read |
|------|-------------|
| `references/design_pipeline.md` | Before forge.build — the mandatory 8-phase pipeline |
| `references/init_procedure.md` | On first invocation of any Forge command |
| `references/sync_audit_procedure.md` | Before forge.sync-audit |
| `references/package_patterns.md` | Before structuring a new skill package |
| `references/authoring_rules.md` | Before writing or editing any skill SKILL.md |
| `references/builder_workflows.md` | Before forge.verify-update, forge.consolidate, forge.sync, or forge.audit |
| `references/github_repo_guardrails.md` | Before creating any GitHub repo or PR |
| `references/synthesis-methodology.md` | When synthesizing a new skill from multiple source skills |
| `references/schemas.md` | Before creating or validating data structures |
| `references/storage-layout.md` | When debugging data path issues or managing disk |
| `references/naming-and-authorship.md` | Before naming, renaming, or setting author on any skill |
| `references/journal-scan-cron-guide.md` | Before running forge:journal-scan — cron mode procedures |
| `references/frontmatter-editing-pitfalls.md` | Before editing any skill frontmatter |
| `references/dispatch-pipeline-guide.md` | **Multi-skill dispatch workflow (Forge+Mentor+Praxis)** — genuine vs second-wave decision procedure, 7 eval gap patterns, cross-directory relpath false positive, journal writing standards, third-wave mitigation, post-dispatch cleanup, phantom file prevention. CONSOLIDATES 60+ dispatch patterns. Load BEFORE running any dispatch pipeline. |
| `references/dispatch-bridge-rerun-pitfalls.md` | **Caller-side bridge re-run pitfalls** — duplicate-journal-on-rerun (later-turn timestamp collision), phantom-guard `None` journal_id crash, and the split write/bridge fix. Read after any dispatch bridge run that writes its own journals. |
| `references/stale-proposal-backlog.md` | Before scanning proposals — handling stale unprocessed proposals |
| `references/journal-file-path-construction.md` | Before writing any journal — correct path pattern with date subdirectory, recovery from misplaced files |
| `references/phantom-file-cleanup.md` | After writing journals via `terminal()` — empty timestamps, double timestamps, malformed filenames |
| `references/interactive-menu.md` | When invoked interactively via `/` command — two-level menu layout, response parsing, platform adaptation |
| `references/session-20260713-dispatch-explicit-run.md` | **Dispatch 2026-07-13:** Explicit-run override verified end-to-end. Caller-side bridge recipe (Forge no-op + real Mentor heartbeat + real Praxis ingest → bridge to BOTH eval files). Confirms the pipeline scripts do NOT write `ingest_state.json`, so the caller must advance `last_ingest_run` + resync counters. |
| `references/session-20260714-dispatch-recovery.md` | **Dispatch 2026-07-14 (TWO recovery passes):** (1) Prior-wave-misclassification RECOVERY — do NOT run `bridge_explicit_run.py` (mints a 2nd wave journal, re-fires dispatcher); hand-run pipeline, rewrite EXISTING dispatch-wave (same run_id). (2) Plain re-detection closure — EXCEPTION pre-flight false-negative when wave emits `forge-<TS>.json` (no `-scan`); mentor-cron heartbeat convergence loop (re-sweep to 0 gaps). |
| `references/recover-dispatch-wave.md` | **Verbatim recovery command sequence** for the prior-wave-misclassification case: confirm trigger, caller-side bridge (Forge + Mentor + Praxis), rewrite EXISTING wave journal, then MANDATORY `reconcile_dispatch_eval_today.py --apply` + `verify_genuine_gap_profile.py` gap assertion. Read this instead of reconstructing the steps from the SKILL.md bullet. |
| `references/session-20260714-dispatch-1240Z-forge.md` | **Dispatch 2026-07-14T12:40Z:** Explicit-run override fires even when named `new_file` already evaluated — NEW post-prior-wave cron heartbeat requires full pipeline + bridge. Pitfalls: malformed wave filename from truncated `TS`; legacy bare-filename eval entries are NOT phantoms. |
| `references/dispatch-recovery-gap-reconciliation.md` | **Recovery gap pitfall:** `gap_backfill.py` gives a FALSE `0` during recovery (mtime-lag masks real dispatch-eval gaps). Use the two-store on-disk reconciliation pattern instead. |
| `references/session-20260713-audit-orphan-state-storage.md` | **Audit 2026-07-13:** SKILL.md-less `ocas-*` dir is NOT automatically removable — may be live `STATE_FILE` storage for a sibling skill. The orphan-vs-load-bearing decision rule for `forge.consolidate`/`forge.audit`. |
| `scripts/bridge_explicit_run.py` | **Caller-side bridge for explicit-run `new_journals`-only dispatch waves.** Runs Forge scan + real Mentor heartbeat (subprocess stdin, not shell pipe) + idempotent dual-eval bridge + dispatch-wave journal + state advance in one atomic run. USE THIS INSTEAD of the broken `run_dispatch_pipeline.py` for pure `new_journals` explicit-run overrides. **INCOMPLETE for MIXED waves (confirmed 2026-07-15):** it does NOT run the Praxis ingest (`ocas-praxis/scripts/praxis_ingest_run.py --mode dispatch`) and does NOT re-affirm the email second-wave state file (`commons/data/ocas-dispatch/<acct>/last_email_check.json` `verified_second_wave`). For a mixed `new_journals`+`new_emails` explicit-run wave, run the full pipeline by hand per `references/session-20260715-mixed-wave-closure.md` — or extend this script. All timestamps composed once; phantom-entry guard via on-disk existence check. |
| `scripts/bridge_eval_inline.py` | **Working** idempotent dual-store eval bridge (created 2026-07-15). Appends relpaths to BOTH praxis-eval (`journal_id`) and dispatch-eval (`filename`) stores, skipping present entries. Corrected `--action` handling (value consumed, never treated as a relpath). Use `--require-exists` to skip relpaths whose file is missing on disk (prevents phantom eval entries). Usage: `python3 scripts/bridge_eval_inline.py REL1 REL2 --action my_label`. Fills the gap left by the long-documented-but-missing `bridge_eval_inline.py`. |
| `scripts/verify_genuine_gap_profile.py` | **Working** bounded per-skill `os.listdir` two-store reconciliation — replaces the phantom `verify_genuine_gap_profile.py`/`reconcile_dispatch_eval_today.py` the doc once referenced. Assert GENUINE GAP=0 before declaring a dispatch-wave closure. UNGATED (walks ALL today-dated journals, no mtime filter). |
| `scripts/closure_convergence_sweep.py` | **Working** ungated two-store BRIDGE (not just report) that mirrors `verify_genuine_gap_profile.py`'s walk and appends any missing journal into the store(s) it is absent from. Run iteratively (loop until it adds 0) immediately BEFORE the verify assertion. Exits 1 while it still bridges gaps, 0 when stable. |
| `scripts/verify_eval_no_phantoms.py` | Detector for phantom eval entries (journal_id pointing at a non-existent file). Bounded/current-wave scope preferred over unscoped historical `--fix`. |
| `scripts/run_dispatch_pipeline.py` | Broken (argparse nargs='[]', no dispatch-eval bridge). Consult only for routine second-wave; use `bridge_explicit_run.py` for explicit-run overrides. |
| `references/session-20260715-mixed-wave-closure.md` | **Mixed explicit-run wave closure (2026-07-15):** A dispatcher fire carrying BOTH `new_journals` (explicit-run override) AND `new_emails` (all `is_new:false` = email second-wave). Verified caller-side sequence: run Forge scan + real Mentor heartbeat + **Praxis ingest** (which `bridge_explicit_run.py` omits), bridge all outputs into BOTH eval stores, advance `ingest_state.last_ingest_run`, re-affirm email `verified_second_wave` via full-file `write_file`, then post-dispatch mentor-cron convergence sweep → assert GENUINE GAP=0. Includes the manual eval-append fallback (since `bridge_eval_inline.py` is missing). |
| `references/mixed-wave-closure-one-shot.md` | **One-shot closure runbook** — the runnable `/tmp/run_pipeline.py` orchestration pattern (timestamps-once, Forge→Mentor→Praxis→bridge→state→email→sweep→verify) that actually closed a live mixed wave, PLUS the dispatch-wave phantom-purge gap the closure walk excludes. Read alongside `session-20260715-mixed-wave-closure.md`. |
| `references/mixed-wave-preflight-triage.md` | **Mixed-wave PRE-FLIGHT triage (2026-07-15):** DECIDE which mode BEFORE touching anything. Copy-pasteable read-only Python pre-flight that distinguishes Mode A (fresh explicit-run → mint new wave journal), Mode B (prior-wave-misclassification recovery → REWRITE existing wave journal, same run_id, run genuine pipeline, advance state), Mode C (re-detection closure → no re-run). Run this FIRST — it tells you whether `session-20260715-mixed-wave-closure.md` is a full-write or a rewrite path. |
| `references/mixed-wave-redetection-closure.md` | **Mixed-wave RE-DETECTION closure (closure-only, 2026-07-15):** When a LATER wave already fully processed the same `new_files` + email threads — do NOT re-run pipelines or mint a wave journal. Verified: bridge residual one-sided gaps (manual dual-store append; `bridge_eval_inline.py` absent), run the continuous mentor-cron convergence `os.listdir` re-sweep until 0 additions, advance `last_ingest_run` via full-file `json.load`+`write_file`, re-affirm email `verified_second_wave`, then assert GENUINE GAP=0. Distinguishes re-detection from prior-wave-misclassification recovery (which rewrites the existing wave). |
| `references/dispatch-explicitrun-closure-recipe.md` | **Explicit-run new_journals dispatch recipe (2026-07-15):** Copy-pasteable pre-flight (a/b/c) decision tree + genuine-run + combined-wave repair + closure steps for an explicit-run `new_journals` (optionally `+new_emails`) wave. Includes the FALSE "stale `last_ingest_run`" diagnosis pitfall (own `dispatch-wave-*.json` excluded from closure mtime) and the cron `execute_code`-block workaround. |
| `references/dispatch-closure-sequence.md` | **Post-state closure sequence (2026-07-16):** exact caller-side commands after `bridge_explicit_run.py` — iterate `closure_convergence_sweep.py` to 0 additions, then assert `verify_genuine_gap_profile.py` GENUINE GAP=0. Confirms both scripts exist on disk (obsoletes the "do NOT exist on disk" note). |
- **Re-detection closure PITFALL (2026-07-15):** a no_op/second-wave closure that bridges siblings but SKIPS advancing `last_ingest_run` past the processed file mtimes leaves `last_ingest_run` BELOW the files → dispatcher re-fires the SAME files every ~5 min forever. Closure MUST advance `last_ingest_run` to the MAX mtime across ALL today's journals (incl. mid-run mentor-cron heartbeats). **CRITICAL sub-trap:** `dispatch_redetection_close.py` once advanced state to **epoch 0** on a 0-gap re-sweep — see `references/redetection-epoch0-pitfall.md` for the bug, the fix, and the mandatory post-closure state-verification discipline (`GENUINE GAP=0` does NOT prove state was advanced).
| `scripts/forge_audit_skills.py` | **Functional** OCAS compliance audit (2026-07-14): scans all `ocas-*` skills for forbidden non-secret env-var config reads + env-var config docs; exits non-zero on violations. Run before any submission. |
| `scripts/update.sh` | Local update helper. |
