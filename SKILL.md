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
- **`proposals/` AND top-level `processed/` are SOURCE MIRRORS, not pending work (confirmed 2026-07-13, RE-CONFIRMED 2026-07-16):** When scanning for unprocessed variant proposals (`vp_*.json` / `vd_*.json`), count ONLY files in `commons/data/ocas-forge/intake/` that are NOT already in `intake/processed/`. Do NOT count files under `commons/data/ocas-forge/proposals/` (a source mirror already copied into `intake/processed/`) NOR the top-level `commons/data/ocas-forge/processed/` dir (another mirror). A naive recursive `find` / `os.walk` over the WHOLE `ocas-forge` tree sweeps up BOTH mirrors and overcounts, falsely flipping a `routine_no_op` dispatch into a `genuine` variant-build dispatch — this bit a 2026-07-16 closure orchestrator that recursive-walked the whole tree, found 11 copies in `proposals/` + 11 in top-level `processed/`, and wrote `unprocessed_proposals: 11` / `action: genuine` when the true value was 0. **USE `scripts/forge_count_unprocessed.py`** (bounded walk of `intake/` only) instead of any hand-rolled recursive count. After counting, cross-check against the prior `forge-scan-*.json` journal's `unprocessed_proposals` field; if the prior scan said 0 and no new variant work arrived, the real count is 0. If you already wrote a false-positive journal, patch it to `unprocessed_proposals: 0` / `action: routine_no_op` BEFORE bridging.
- **Missing `includes:` in frontmatter** — required when references/ or scripts/ dir exists
- **Scope boundary for sync** — `forge.sync`/`forge.audit` only on `ocas-*` skills
- **Doing more than asked** — match work to the scope of the request
- **Incorrect Naming** — NEVER create/rename `ocas-*` without user authorization
- **Non-durable fixes** — put rules in skill's own git repo or MEMORY.md, not hermes core
- **Runaway repo creation** — check for 3rd-party skills before `gh repo create`
- **YAML block scalar truncation** — `description: >` / `|` contain newlines; use `read_file` + `patch`
- **`action` field is polymorphic in forge journals** — guard with `isinstance` before every access
- **Dispatcher `new_files` paths lack prefix — AND the dispatch-wave journal resolves to the WRONG tree (confirmed 2026-07-16)** — The dispatcher's `details.new_files` prints `ocas-dispatch/2026-07-16/dispatch-wave-20260716T195230Z.json`. Treated as profile-relative, that resolves to `commons/data/ocas-dispatch/<DATE>/` — but that directory holds only LEGACY mirror dispatch-wave JSONs (2026-06 era). The LIVE on-disk journal is at `commons/journals/ocas-dispatch/2026-07-16/dispatch-wave-20260716T195230Z.json`. A `read_file` on the dispatcher-printed path returns "File not found." Route all dispatch-wave journal reads to the `commons/journals/` tree (the same tree `verify_genuine_gap_profile.py` / `closure_convergence_sweep.py` walk). Use `find <hermes-home> -name 'dispatch-wave-*.json'` to locate the real path.
- **`verify_eval_no_phantoms.py` reports PRE-EXISTING historical phantoms — NEVER run destructive `--fix` during a closure pass (confirmed 2026-07-16)** — The script walks the ENTIRE eval store (not date-scoped) and reports 1,800+ phantoms: historical 2026-06 → 2026-07-14 entries, malformed arg-flag leaks (`--help`, `--apply`, `--path`), and mis-namespaced relpaths (e.g. `ocas-dispatch/dispatch-wave-20260716T012901Z.json` missing its date dir). NONE belong to the current wave. Running `--fix` would mass-delete historical eval lines — OUT OF SCOPE and RISKY during a dispatch closure. Correct scope check for a closure: (a) verify every entry THIS run bridged was `os.path.exists()`-confirmed BEFORE bridging, and (b) assert `GENUINE GAP = 0` via `verify_genuine_gap_profile.py --date <DATE>`. Leave historical phantom cleanup to a dedicated audit, not a closure pass.
- **Appending to JSONL files** — ALWAYS use `echo >>`, NEVER heredoc with `>`
- **`write_file` escapes quotes in Python files** — use `terminal()` with heredoc for .py files
- **Programmatic SKILL.md surgery can delete the frontmatter `---` fence (confirmed 2026-07-16 grind):** When you use a Python slice to delete/replace a block of `SKILL.md` — e.g. extracting inline operational detail into `references/` to cut the line count — a stray `del lines[a:b]` or a `header + pointer + rest` reassembly that accidentally includes the frontmatter's closing `---` will silently remove the YAML delimiter. The next parse treats the body as frontmatter (or raises `yaml.ScannerError`), and the 10khr scorer drops **D1 → 1** (name/description unparseable) and **D2 → 3**. This is invisible until you re-score. **Fix:** (1) After ANY programmatic SKILL.md edit, immediately re-run `scripts/critique_10khr_runner.py --report-only` (or call `score_skill()`) and watch D1/D2 — a sudden drop from 5 to ≤3 means the fence is gone. (2) Guard the slice to stop before the `---` line; if eaten, re-insert `---` at the frontmatter/body boundary. (3) Verify before declaring done: `yaml.safe_load(content.split('---')[1])` must succeed and return `name`/`description`. The same guard applies to `forge.build`/`forge.repair` edits done via `terminal()` heredoc slices.
- **Eval-store manual grep must use the BARE relpath — NOT `commons/journals/`-prefixed** — When you manually `grep` the praxis eval store (`commons/data/ocas-praxis/journals_evaluated.jsonl`, key `journal_id`) to check whether a journal was already evaluated, grep with the bare relpath `ocas-mentor/2026-07-16/mentor-light-XXXX.json`, NOT the prefix-inclusive `commons/journals/ocas-mentor/2026-07-16/...` path. The store keys by the bare relpath (matching what `bridge_eval_inline.py` / `closure_convergence_sweep.py` write). Grepping with the `commons/journals/` prefix returns ABSENT even for journals that ARE present, which mis-diagnoses a clean re-detection as a genuine gap and can trigger spurious re-bridging. Confirmed 2026-07-16 residual-gap closure: a prefix-inclusive grep reported ABSENT; the bare-relpath grep (and the closure scripts) confirmed the journal was already in both stores. Always use `grep -c 'ocas-mentor/2026-07-16/<file>.json'` (no leading dir) for manual verification; the closure scripts (`verify_genuine_gap_profile.py`, `bridge_eval_inline.py`) parse JSON and never hallucinate key-format gaps, so prefer them over raw grep.
- **Placeholder-then-patch anti-pattern** — never write placeholder strings intending to fix later
- **Heredoc `$(date)` timestamp mismatch** — compose TS into a variable first, use for both filename and content
- **Research is not optional for improvements** — MUST run Phase 1.5 research before touching files
- **`forge.update` vs `git pull` divergence** — cross-check git log against SKILL.md version field
- **`forge_audit_skills.py` is now functional (corrected 2026-07-14)** — The script at `scripts/forge_audit_skills.py` is a REAL compliance audit: it scans every `ocas-*` skill's `scripts/` for forbidden non-secret env-var config reads (`GENIE_*`, `<NAME>_MAX_AGE_DAYS`, `<NAME>_PATH`, `<NAME>_ENABLED`, etc.) and its `SKILL.md` body for env-var config tables, and exits non-zero on any blocking (ERROR) issue. Run `python3 scripts/forge_audit_skills.py` (or `--skill ocas-<name>` for one). It skips `.bak` files. When `forge.audit` is invoked, run this first — it is the standing gate, not a manual-only task. The pre-2026-07-14 stub note is obsolete.
- **`nargs='[]'` is invalid in argparse** — When defining command-line arguments, `nargs='[]'` is not a valid option and will cause a ValueError. To accept zero or more arguments, use `nargs='*'` instead. This caused the run_dispatch_pipeline.py script to fail until corrected.
- **Tool-layer flake: `skill_view` / `read_file` / `write_file` / `search_files` all return `DaemonThreadPoolExecutor` API error (observed 2026-07-16 dispatch + this session's mixed-wave closure)** — When loading a skill (`skill_view`), reading a `SKILL.md` / journal JSON (`read_file`), OR writing a file (`write_file`), the tool layer can intermittently fail with `Error during OpenAI-compatible API call #N: 'DaemonThreadPoolExecutor' object has no attribute '_initializer'`. `terminal()` is NOT affected. **Read fallback:** read the same file directly with `terminal()` — use `find <dir> -name '*.md'` / `-name '*.json'` to locate it, then `cat <path>`. **Write fallback:** use `terminal()` `cat > file << 'EOF'` heredoc (JSON) or `cat > script.py << 'PYEOF'` heredoc — the same pattern ocas-mentor/ocas-praxis already mandate for their cron JSON/journal writes. Avoid `${...}` / `$(...)` inside heredocs (bash expansion pitfall) and watch for the Praxis double-Z filename trap. **Search fallback:** once `search_files` flakes, route around it with terminal `find <dir> -name '*.py'` (file search) or `grep -rn 'PATTERN' <dir>` (content search) — do NOT burn 3+ retries. **Do NOT burn 3–4 retries** on `skill_view`/`write_file`/`search_files`; after 1–2 identical failures, switch to terminal. When the flake hits MULTIPLE skills in one run, don't retry each individually — batch-read ALL remaining needed SKILL.md files in ONE terminal `cat` (e.g. `cd skills && for s in ocas-mentor ocas-praxis ocas-dispatch; do echo "== $s =="; cat $s/SKILL.md; done`) instead of burning N `skill_view` retries; the 2026-07-16 dispatch wave closed a combined re-detection this way after `skill_view` succeeded once then failed 3× in a row. CRITICAL non-determinism: the flake is NOT consistent even within one session — `write_file` succeeded for several `/tmp/*.py` writes earlier in 2026-07-16 closure, then failed twice in a row on a later `/tmp/update_state.py` + `last_email_check.json` write before the `terminal() cat >` fallback succeeded. So neither a prior success nor a prior failure predicts the next call; route around it on first flake. Skill files live under `~/.hermes/profiles/indigo/skills/<name>/` and journals under `~/.hermes/profiles/indigo/commons/journals/<skill>/<date>/` — the filesystem path is authoritative. The flake is in the tool layer, not the skill content; treat it as transient and route around it. (Confirmed live 2026-07-16: `skill_view` ×3 and `read_file` ×4 all failed identically; `terminal() cat`/`cat >`/`find`/`grep` succeeded on every attempt. The flake had cleared by the review pass, so it is genuinely intermittent, not persistent.)

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

**Monitor gate state is a SEPARATE file — and it has TWO copies (confirmed 2026-07-16 closure):** the journal re-fire is gated by `monitor_journals.py` reading the PROFILE-relative monitor state at `~/.hermes/profiles/indigo/commons/data/monitor_state/journal_ingest_state.json` (`latest_mtime`) — NOT `ocas-praxis/ingest_state.json`. Closing a re-detection MUST advance BOTH monitor copies AND the praxis `last_ingest_run`, all past the max journal mtime. Always `json.load`+overwrite BOTH copies (`<hermes-home>/commons/data/monitor_state/journal_ingest_state.json` and `<hermes-home>/profiles/indigo/commons/data/monitor_state/journal_ingest_state.json`). **CORRECTED 2026-07-17:** `scripts/closure_closeout_check.py` (an ocas-FORGE script, lives only in `ocas-forge/scripts/`, NOT ocas-dispatch) was updated to read BOTH monitor copies and to assert gate [2] against the profile copy (the load-bearing one); the old version read only the root copy and gave a false "closed". The verifier's gate [2] reporting True IS now proof the monitor is satisfied (both copies checked). **Email gate fix (2026-07-17):** the verifier no longer requires the two top-level GWS-snapshot files (`last_email_check.json`, `last_email_check_<account-identity>_gmail_com.json`) — those stay `null` under the monitor re-fire bug and are the known un-closeable gate; it now REQUIRES only the dispatch-owned account copies (`owner/last_email_check.json`, `last_email_check_owner.json`, indigo equivalents) and WARNs on the top-level snapshots. See `references/redetection-stale-state-closure-oneshot.md` (Monitor gate state section).
- **Never recursive-glob `commons/journals/**/*.json` during closure diagnosis (confirmed 2026-07-16):** a symlink/dir loop nests `commons/journals/journals/journals/...` to arbitrary depth, so a recursive `**/` glob over the journals tree returns millions of duplicate paths and can dump 30+ MB into one tool result, burying the real answer. The closure scripts (`closure_convergence_sweep.py`, `verify_genuine_gap_profile.py`) already use a BOUNDED per-skill `os.listdir(skill)/<DATE>` walk — copy that pattern. For ad-hoc discovery, glob `commons/journals/<skill>/<DATE>/*.json` per skill, never `**`.
- **Re-detection recurs because the wave writer doesn't advance gates atomically (07-13→07-14→07-15→07-16 all re-fired):** each `dispatch-wave-*.json` is written but the monitor `latest_mtime` + praxis `last_ingest_run` are left at pre-wave values, so `monitor_journals.py` re-enqueues the same files next cycle until a manual closure runs. Real fix: have the wave writer advance both gates in the same transaction as the journal write (or invoke the closure Closeout at wave end). Manual `closure_closeout_check.py` + dual-copy state advance is the stopgap, not the cure — note it in any closure journal so the recurring pattern is visible. **Mtime-advance truncation trap (confirmed 2026-07-16 closure):** when advancing these gates, NEVER hand-type the float/ISO mtime literal — a hand-typed `1784232657.4915` TRUNCATES below the true `1784232657.4915047` (4.7e-6 under), so `state < max_journal_mtime`, `closure_closeout_check.py` reports `monitor>=max: False`, and the dispatcher RE-FIRES forever. This is the SAME failure class as `redetection-epoch0-pitfall.md` (state < max) but a DIFFERENT cause (hand-typed literal truncation vs. bad arithmetic on a 0-gap sweep). ALWAYS recompute `max(os.path.getmtime(p) for p in glob('commons/journals/*/<DATE>/*.json'))` programmatically and add `>= 1.0s` pad so any heartbeat landing during the write is also covered. See `references/redetection-mtime-truncation-pitfall.md`.
- **Scheduled dispatcher RE-FIRES mid-closure and CLOBBERS the two top-level GWS-snapshot email-state files (confirmed 2026-07-16T2145Z):** a manual Mode-C closure re-flagging `verified_second_wave=True` on `commons/data/ocas-dispatch/last_email_check.json` + `last_email_check_<account-identity>_gmail_com.json` got overwritten ~60s later when the scheduled `dispatcher.py`/`monitor_email.py` fired AGAIN during the run, rewriting those two files as pure gws snapshots (raw `new_threads`) with `verified_second_wave` dropped to Null. The dispatch-OWNED owner copies (`owner/last_email_check.json`, `last_email_check_owner.json`) survive intact (True). **Mitigation:** after re-flagging, immediately re-run `scripts/closure_closeout_check.py` in the SAME script (subprocess) so the verifier reads the flag before the next dispatcher tick (minimize clobber window); if `[3]` still shows None, the dispatcher landed between your write and the verifier — just re-flag the two top-level files and re-verify. Do NOT chase a permanently-green `[3]` on those two files; they are the known un-closeable gate under the monitor re-fire bug (see `references/dispatch-wave-email-state-topology.md`, Caveat). The LOAD-BEARING gates are `[1]` (named journal in both eval stores) and `[2]` (state advanced past max mtime), which DO stay green once advanced. Full recipe in `references/closure-email-state-refire-pitfalls.md`.
- **Recursive `**/last_email_check*.json` glob OVER-PERTAINS `indigo/last_email_check.json` during a single-account closure (confirmed 2026-07-16T2145Z):** that file's basename is `last_email_check.json` (identical to the owner top-level snapshot), so a blanket recursive glob + flip-to-True wrongly set indigo's `verified_second_wave` to True, corrupting indigo's genuine `false` state (it was a real `action:none` triage from 20260716T161444Z, not second-wave). This is the REVERSE of the `dispatch-wave-email-state-topology.md` "key on path not account" advice. **Mitigation:** during a owner-specific closure, target owner's files by EXPLICIT paths only — `last_email_check.json`, `last_email_check_<account-identity>_gmail_com.json`, `owner/last_email_check.json`, `last_email_check_owner.json` — never a recursive `**/last_email_check*.json` blanket. If you over-flip, restore the other account's file from its prior true value. Full detail in `references/closure-email-state-refire-pitfalls.md`.

**The expanded critical dispatch rules, recovery recipes, and the full 7-pattern eval-gap catalog** are in `references/dispatch-integration-pitfalls-skillmd.md` — read it before running any dispatch pipeline or recovery. It is the companion to the summary above and the canonical `references/dispatch-pipeline-guide.md`.


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
| `references/dispatch-integration-pitfalls-skillmd.md` | **Dispatch integration inline detail** — expanded critical dispatch rules, recovery recipes, and the full 7-pattern eval-gap catalog extracted from SKILL.md. Read BEFORE running any dispatch pipeline or `forge:journal-scan` cron run (companion to `dispatch-pipeline-guide.md`). |
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
| `scripts/bridge_explicit_run.py` | **Caller-side bridge for explicit-run `new_journals`-only dispatch waves.** Runs Forge scan + real Mentor heartbeat (subprocess stdin, not shell pipe) + idempotent dual-eval bridge + dispatch-wave journal + state advance in one atomic run. USE THIS INSTEAD of the broken `run_dispatch_pipeline.py` for pure `new_journals` explicit-run overrides. **INCOMPLETE for MIXED waves (confirmed 2026-07-15):** it does NOT run the Praxis ingest (`ocas-praxis/scripts/praxis_ingest_run.py --mode dispatch`) and does NOT re-affirm the email second-wave state file (`commons/data/ocas-dispatch/<acct>/last_email_check.json` `verified_second_wave`). For a mixed `new_journals`+`new_emails` explicit-run wave, run the full pipeline by hand per `references/session-20260715-mixed-wave-closure.md` — or extend this script. All timestamps composed once; phantom-entry guard via on-disk existence check. **TWO WAVE JOURNALS EXPECTED (confirmed 2026-07-16):** when the email pass runs separately (genuine OR second-wave), it writes its OWN `dispatch-wave-*.json` — so a single mixed dispatcher fire legitimately yields TWO wave journals: one from this script (at the forge-scan TS) and one from the email triage (at its own TS). Both must be bridged into BOTH eval stores (`commons/data/ocas-praxis/journals_evaluated.jsonl` + `commons/data/ocas-dispatch/journals_evaluated.jsonl`). This is NOT a duplication defect and the second journal is NOT a phantom — do not purge it in closure. |
| `scripts/bridge_eval_inline.py` | **Working** idempotent dual-store eval bridge (created 2026-07-15). Appends relpaths to BOTH praxis-eval (`journal_id`) and dispatch-eval (`filename`) stores, skipping present entries. Corrected `--action` handling (value consumed, never treated as a relpath). Use `--require-exists` to skip relpaths whose file is missing on disk (prevents phantom eval entries). Usage: `python3 scripts/bridge_eval_inline.py REL1 REL2 --action my_label`. Fills the gap left by the long-documented-but-missing `bridge_eval_inline.py`. |
| `scripts/verify_genuine_gap_profile.py` | **Working** bounded per-skill `os.listdir` two-store reconciliation — replaces the phantom `verify_genuine_gap_profile.py`/`reconcile_dispatch_eval_today.py` the doc once referenced. Assert GENUINE GAP=0 before declaring a dispatch-wave closure. UNGATED (walks ALL today-dated journals, no mtime filter). |
| `scripts/closure_convergence_sweep.py` | **Working** ungated two-store BRIDGE (not just report) that mirrors `verify_genuine_gap_profile.py`'s walk and appends any missing journal into the store(s) it is absent from. Run iteratively (loop until it adds 0) immediately BEFORE the verify assertion. Exits 1 while it still bridges gaps, 0 when stable. |
| `scripts/closure_closeout_check.py` | **Close-out verifier** (added 2026-07-16, CORRECTED 2026-07-17): asserts ALL closure gates in one pass — named journal in both eval stores, both state gates (`praxis last_ingest_run` + `monitor latest_mtime`) >= max today-journal mtime, and dispatch-owned email `verified_second_wave` flags. Replaces the inline hardcoded close-out heredoc in `references/redetection-stale-state-closure-oneshot.md`. Run `python3 scripts/closure_closeout_check.py --named <rel> --date <DATE>`; exits 1 if any gate is stale. **NOTE this is an ocas-FORGE script — invoked from ocas-forge, NOT ocas-dispatch** (`skills/ocas-dispatch/scripts/closure_closeout_check.py` does NOT exist; confirmed 2026-07-17). **2026-07-17 correction:** (a) reads BOTH monitor copies — root `<hermes-home>/commons/data/monitor_state/journal_ingest_state.json` AND profile-relative `<hermes-home>/profiles/indigo/commons/data/monitor_state/journal_ingest_state.json` (the profile copy is what `monitor_journals.py` actually gates on; the prior version read only the root copy and falsely reported "closed" while the profile copy stayed stale, re-firing the wave); (b) REQUIRES the dispatch-owned account copies (`owner/last_email_check.json`, `last_email_check_owner.json`, and the indigo equivalents) and only WARNs on the two top-level GWS-snapshot files (`last_email_check.json`, `last_email_check_<account-identity>_gmail_com.json`) which stay `null` under the monitor re-fire bug — the prior version required those and so every <operator> closure failed gate [3] regardless of real state. |
| `scripts/verify_eval_no_phantoms.py` | Detector for phantom eval entries (journal_id pointing at a non-existent file). Bounded/current-wave scope preferred over unscoped historical `--fix`. |
| `scripts/run_dispatch_pipeline.py` | Broken (argparse nargs='[]', no dispatch-eval bridge). Consult only for routine second-wave; use `bridge_explicit_run.py` for explicit-run overrides. |
| `references/session-20260715-mixed-wave-closure.md` | **Mixed explicit-run wave closure (2026-07-15):** A dispatcher fire carrying BOTH `new_journals` (explicit-run override) AND `new_emails` (all `is_new:false` = email second-wave). Verified caller-side sequence: run Forge scan + real Mentor heartbeat + **Praxis ingest** (which `bridge_explicit_run.py` omits), bridge all outputs into BOTH eval stores, advance `ingest_state.last_ingest_run`, re-affirm email `verified_second_wave` via full-file `write_file`, then post-dispatch mentor-cron convergence sweep → assert GENUINE GAP=0. Includes the manual eval-append fallback (since `bridge_eval_inline.py` is missing). |
| `references/mixed-wave-closure-one-shot.md` | **One-shot closure runbook** — the runnable `/tmp/run_pipeline.py` orchestration pattern (timestamps-once, Forge→Mentor→Praxis→bridge→state→email→sweep→verify) that actually closed a live mixed wave, PLUS the dispatch-wave phantom-purge gap the closure walk excludes. Read alongside `session-20260715-mixed-wave-closure.md`. |
| `references/mixed-wave-preflight-triage.md` | **Mixed-wave PRE-FLIGHT triage (2026-07-15):** DECIDE which mode BEFORE touching anything. Copy-pasteable read-only Python pre-flight that distinguishes Mode A (fresh explicit-run → mint new wave journal), Mode B (prior-wave-misclassification recovery → REWRITE existing wave journal, same run_id, run genuine pipeline, advance state), Mode C (re-detection closure → no re-run). Run this FIRST — it tells you whether `session-20260715-mixed-wave-closure.md` is a full-write or a rewrite path. |
- **Mixed-wave RE-DETECTION closure (closure-only, 2026-07-15; email-evidence gate added 2026-07-17):** When a LATER wave already fully processed the same `new_files` + email threads — do NOT re-run pipelines or mint a wave journal. **MANDATORY pre-close email gate:** `closure_closeout_check.py` gate [3] (`verified_second_wave: True` on dispatch-owned files) is NOT proof of work — the flag can be a false positive from a prior wave that asserted verification without producing it (email-evidence-verification-gap failure, 2026-07-14). Before re-affirming or advancing state, run `python3 skills/ocas-dispatch/scripts/verify_evidence_threads.py --evidence commons/data/ocas-dispatch/evidence.jsonl <thread_id...>` on every dispatch thread in the wave; any thread printing `NOT_IN_EVIDENCE` or `in_evidence(structured)` with NO `action=` token is a genuine Path B gap — triage it (per `ocas-dispatch` `references/cron-triage-workflow.md`) BEFORE closing. Only after evidence is confirmed present with `action=` tokens, continue: bridge residual one-sided gaps (manual dual-store append; `bridge_eval_inline.py` absent), run the continuous mentor-cron convergence `os.listdir` re-sweep until 0 additions, advance `last_ingest_run` via full-file `json.load`+`write_file`, re-affirm email `verified_second_wave`, then assert `GENUINE GAP=0`. Distinguishes re-detection from prior-wave-misclassification recovery (which rewrites the existing wave). See `references/mixed-wave-closure-email-evidence-gate.md`.
| `references/redetection-stale-state-closure-oneshot.md` | **MODE C re-detection stale-state closure — one-shot runbook (2026-07-16):** Date-agnostic copy-paste pre-flight + closure sequence for the PURE stale-state loop (journal already in BOTH eval stores). Covers BOTH `last_ingest_run < named-journal-mtime` (named file is the gap) AND `last_ingest_run == named-journal-mtime` (named file is bridged; LATER mentor-cron heartbeats are the real gap — re-fire is NOT a misclassification). Includes the mandatory POST-ADVANCE re-sweep loop (a mentor-cron heartbeat lands between the pre-advance sweep and the state write), the `json.load`-not-`read_file` guard, the REAL eval-store paths (`commons/data/ocas-*/journals_evaluated.jsonl`, NOT `commons/journals/ocas-dispatch/...`), and the email second-wave re-affirm block (incl. the **account-mislabel pitfall** — a <operator> file carrying `account: <third-party-or-user-email>` OR `account: null`; the overwrite guard `if s.get("account") != exp_acct` catches BOTH — confirmed 2026-07-16T19:52Z). For the final gate assertion, prefer `scripts/closure_closeout_check.py --named <rel> --date <DATE>` over the inline heredoc. Use this for a plain `new_journals` re-fire that is NOT a mixed wave. |
| `references/mixed-wave-closure-email-evidence-gate.md` | **Mixed-wave closure email-evidence gate (2026-07-17):** The `closure_closeout_check.py` gate [3] `verified_second_wave: True` is NOT proof of email work (2026-07-14 false-positive incident). Before re-affirming/advancing state on ANY mixed wave, run `verify_evidence_threads.py` on every dispatch thread; only close when all print `in_evidence(structured)  action=...`. Full command, authoritative evidence path, and the 2026-07-17 confirmation (10 <operator> threads all genuinely `action=none`). |
| `references/dispatch-explicitrun-closure-recipe.md` | **Explicit-run new_journals dispatch recipe (2026-07-15):** Copy-pasteable pre-flight (a/b/c) decision tree + genuine-run + combined-wave repair + closure steps for an explicit-run `new_journals` (optionally `+new_emails`) wave. Includes the FALSE "stale `last_ingest_run`" diagnosis pitfall (own `dispatch-wave-*.json` excluded from closure mtime) and the cron `execute_code`-block workaround. |
| `references/dispatch-closure-sequence.md` | **Post-state closure sequence (2026-07-16):** exact caller-side commands after `bridge_explicit_run.py` — iterate `closure_convergence_sweep.py` to 0 additions, then assert `verify_genuine_gap_profile.py` GENUINE GAP=0. Confirms both scripts exist on disk (obsoletes the "do NOT exist on disk" note). |
| `references/dispatch-wave-email-state-topology.md` | **Email-state file topology (2026-07-16):** the 7 email-state files under `commons/data/ocas-dispatch/`, which 4 the closeout verifier actually inspects, and why re-affirm `verified_second_wave` via a full glob (key on path, not the often-null `account` field). |
| `references/closure-email-state-refire-pitfalls.md` | **Closure email-state pitfalls (2026-07-16T2145Z):** (A) scheduled dispatcher re-fires mid-closure and clobbers the two top-level GWS-snapshot files' `verified_second_wave` — re-flag + re-verify in one script; (B) recursive `**/last_email_check*.json` over-pertains `indigo/last_email_check.json` during a owner closure and corrupts indigo's state — use explicit per-account paths. Companion to `dispatch-wave-email-state-topology.md`. |
- **Re-detection closure PITFALL (2026-07-15):** a no_op/second-wave closure that bridges siblings but SKIPS advancing `last_ingest_run` past the processed file mtimes leaves `last_ingest_run` BELOW the files → dispatcher re-fires the SAME files every ~5 min forever. Closure MUST advance `last_ingest_run` to the MAX mtime across ALL today's journals (incl. mid-run mentor-cron heartbeats). **CRITICAL sub-trap:** `dispatch_redetection_close.py` once advanced state to **epoch 0** on a 0-gap re-sweep — see `references/redetection-epoch0-pitfall.md` for the bug, the fix, and the mandatory post-closure state-verification discipline (`GENUINE GAP=0` does NOT prove state was advanced).
- **Closure script does NOT advance the monitor `latest_mtime` copies (CONFIRMED LIVE 2026-07-17):** `dispatch_redetection_close.py` advances ONLY `ingest_state.last_ingest_run` (the praxis copy). It does NOT touch the two monitor `journal_ingest_state.json` copies (`<hermes-home>/commons/data/monitor_state/` root + `<hermes-home>/profiles/indigo/commons/data/monitor_state/` profile-relative). Gate [2] in `closure_closeout_check.py` reads BOTH monitor copies, so after the closure script runs, gate [2] stays False and the wave re-fires forever. MANDATORY extra step after any closure run: recompute `max_mt = max(os.path.getmtime(p) for p in glob of ALL today-journals EXCLUDING ocas-custodian + dispatch-wave-*)`, set `new = max_mt + 2.0` (≥2s pad, NEVER hand-typed literal — see `redetection-mtime-truncation-pitfall.md`), and `json.load`+overwrite BOTH monitor copies with `latest_mtime = new`. Then re-run `closure_closeout_check.py` and confirm `=== gates ALL CLOSED ===`. This applies even when you ran the genuine pipeline via `bridge_explicit_run.py` (which also leaves monitor copies stale). CONFIRMED LIVE 2026-07-17: a genuine-run wave (bridge_explicit_run.py + dispatch_redetection_close.py) left gate [2] False (monitor copies at 06:40:41Z vs max journal 06:48:43Z) until both copies were advanced by hand.
- **Pre-flight must scan ALL today-journals, not just the dispatcher's `new_files` (CONFIRMED LIVE 2026-07-17):** the dispatcher flags only files present at its `detected_at`. A journal that LANDS AFTER detection (mtime > detected_at) but is missing from BOTH eval stores is GENUINE work even when the dispatcher-named file is already bridged (a re-detection). The `dispatch-explicitrun-closure-recipe.md` pre-flight (a/b/c) checks only the named `new_files`; extend it with a (d) step: `glob` every `commons/journals/<skill>/2026-07-17/*.json`, check each against BOTH eval stores; if ANY today-journal is absent from either store, run the GENUINE pipeline (do NOT closure-only). CONFIRMED LIVE 2026-07-17: wave detected at 06:40:37Z flagged `063755Z` (already in both stores = re-detection), but `064536Z` landed at 06:45:36Z AFTER detection and was genuinely missing from both stores. Scanning only the named file would have skipped the real gap.
| `scripts/forge_audit_skills.py` | **Functional** OCAS compliance audit (2026-07-14): scans all `ocas-*` skills for forbidden non-secret env-var config reads + env-var config docs; exits non-zero on violations. Run before any submission. |
| `scripts/forge_count_unprocessed.py` | **Safe bounded count** of unprocessed Forge variant proposals (`vp_*`/`vd_*`). Walks ONLY `commons/data/ocas-forge/intake/`, excluding `intake/processed/`, the `proposals/` mirror, and top-level `processed/`. Prints the integer count. USE INSTEAD of any recursive `find`/`os.walk` over the whole tree (which overcounts both mirrors and falsely flips `routine_no_op`→`genuine`). Re-confirmed 2026-07-16. |
| `scripts/update.sh` | Local update helper. |
| `references/redetection-mtime-truncation-pitfall.md` | **MODE C mtime-advance truncation trap (2026-07-16 closure):** when advancing monitor latest_mtime + praxis last_ingest_run, NEVER hand-type the float/ISO literal — it truncates below the true max journal mtime and silently leaves state < max, so the verifier reports False and the wave re-fires forever. Recompute max(os.path.getmtime(...)) programmatically + >=1s pad. Re-fires-forever = same class as redetection-epoch0-pitfall.md but different cause (literal truncation, not bad arithmetic). |
| `references/closure-post-ingest-mtime-trap.md` | **Post-ingest caller-journal mtime trap (2026-07-17):** the Praxis ingest template sets `last_ingest_run` to its OWN NOW mid-pipeline, so caller-written `praxis-cron-*.json` + `dispatch-wave-*.json` (later mtimes) exceed it — verifier gate [2] praxis-half goes False even when `GENUINE GAP=0`, re-firing forever. After writing those journals, RE-ADVANCE `last_ingest_run` past max today-journal mtime (+>=5s pad), then re-sweep/verify/closeout. Distinct cause from the hand-typed truncation trap above. |