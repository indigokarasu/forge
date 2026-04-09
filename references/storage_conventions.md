# OCAS Storage Conventions

Spec Version: 2.0
Author: Indigo Karasu

Changes from 1.2: replaced $OCAS_DATA_ROOT variable with platform-native {agent_root}/commons/ convention; eliminated all invented environment variables; added errors/ as a universal storage root alongside journals/; removed intake directory convention (inter-skill communication now uses journal payloads); updated initialization, validation, and cross-skill access sections.

---

## Purpose

This document defines the standard storage conventions for OCAS skills. All skills that persist state must follow these conventions to ensure consistency, auditability, and interoperability across the suite.

---

## Storage Root

All shared OCAS data lives under `{agent_root}/commons/`.

`{agent_root}` is the agent platform's home directory. Every agent platform has one:

- OpenClaw: `~/openclaw/`
- Hermes Agent: `~/.hermes/`
- Claude Code: `~/.claude/`

At init time, the skill asks the agent for its root directory, then creates or uses `commons/` one level down — the same level as `skills/`, `memory/`, and other platform directories.

Four sub-roots, one per data class:

```
{agent_root}/commons/
  data/       — skill-private state, configuration, and JSONL logs
  journals/   — per-run journal files (shared, read by meta-skills)
  errors/     — per-run error records (shared, read by meta-skills)
  db/         — LadybugDB graph databases (Elephas and Weave only)
```

No skill writes outside `{agent_root}/commons/`. No skill writes inside the skill package directory.

### What goes where

- **If only your skill reads it** → `commons/data/{skill-name}/`
- **If other skills read it** → `commons/journals/`, `commons/errors/`, or `commons/db/`

---

## Data Directory

### Location

```
{agent_root}/commons/data/{skill-name}/
```

The `{skill-name}` must match the skill's hyphenated identifier exactly: `ocas-scout`, `ocas-elephas`, `ocas-weave`.

### Required Structure

```
{agent_root}/commons/data/{skill-name}/
  config.json
```

### Typical Full Structure

```
{agent_root}/commons/data/{skill-name}/
  config.json
  {primary_log}.jsonl
  decisions.jsonl
  reports/
  artifacts/
  staging/       — temporary import/export files (for skills that bulk-process data)
```

---

## Journal Directory

### Location

```
{agent_root}/commons/journals/{skill-name}/YYYY-MM-DD/{run_id}.json
```

One file per run. Date directory created automatically. File named by `run_id`.

### Structure

```
{agent_root}/commons/journals/ocas-scout/
  2026-03-17/
    r_a7f2c1.json
    r_b3e8d2.json
  2026-03-18/
    r_c91f4a.json
```

Champion and challenger runs for the same comparison group live in the same date directory:

```
{agent_root}/commons/journals/ocas-rally/
  2026-03-17/
    cg_5cfa2c1/
      champion.json
      challenger.json
```

### Conventions

- Journal files are written atomically (write to `.tmp`, then rename).
- Journal files are immutable after write. Never edit.
- Runs missing journal files are invalid per the journal specification.
- Journals are shared records. Meta-skills (Mentor, Elephas, Corvus, Custodian) read all skill journals.

### Inter-skill payloads in journals

Journals carry typed payload fields that consuming skills filter on:

| Journal field | Consumer | Meaning |
|---|---|---|
| `briefing.surface: true` | Vesper | Include in next briefing |
| `signal.entities: [...]` | Elephas | Entities to ingest into Chronicle |
| `variant_proposal: {...}` | Forge | Skill improvement to build |
| `experiment_request: {...}` | Fellow | Experiment to run |
| `cycle_result: {...}` | Mentor | Experiment results |
| `behavioral_signal: {...}` | Praxis | Behavioral pattern to evaluate |

Each consumer owns its filtering logic and tracks which `run_id`s it has consumed via an ingestion log in its own `data/` directory.

---

## Error Directory

### Location

```
{agent_root}/commons/errors/{skill-name}/YYYY-MM-DD/{run_id}.json
```

Same structure as journals. One file per failed run. Every skill writes error records universally.

### Conventions

- Error files follow the same atomic write and immutability rules as journals.
- Custodian reads all skill error directories during health scans.
- A run may produce both a journal and an error record (partial success).

---

## Database Directory

### Location

```
{agent_root}/commons/db/{skill-name}/
```

Only for skills that maintain LadybugDB graph databases. Currently: `ocas-elephas` and `ocas-weave`.

### Structure

```
{agent_root}/commons/db/ocas-elephas/
  chronicle.lbug
  config.json
  staging/

{agent_root}/commons/db/ocas-weave/
  weave.lbug
  config.json
  staging/
```

The `.lbug` file is managed exclusively by LadybugDB. Never read or modify `.lbug`, `.wal`, `.shadow`, or `.tmp` files directly.

---

## File Types and Conventions

### config.json

Every skill's configuration file. Must include `ConfigBase` fields from the shared schemas specification: `skill_id`, `skill_version`, `config_version`, `created_at`, `updated_at`.

Config is the only mutable JSON file in the data directory. All other data files are append-only.

### JSONL Files (Append-Only Logs)

Primary data storage uses JSON Lines format: one complete JSON object per line.

Conventions:
- Extension: `.jsonl`
- Append-only. Lines must not be edited or deleted after write.
- Each record includes a unique `id` field and a `timestamp` field in ISO 8601 format.
- Records are ordered chronologically.

Common files:
- `decisions.jsonl` — DecisionRecord entries
- `events.jsonl` or `{domain}_events.jsonl` — log events
- `signals.jsonl` — emitted signals
- `candidates.jsonl` — proposed Chronicle candidates

### reports/ Directory

Human-readable output artifacts. Any format (Markdown, JSON, PDF). Generated artifacts, not source-of-truth data.

### artifacts/ Directory (Optional)

Stored evidence, drafts, or intermediate outputs supporting decision traceability.

### staging/ Directory (Optional)

Temporary files for bulk operations (CSV imports, export buffers). Contents are transient and may be deleted after the operation completes.

---

## Naming Conventions

Files: `snake_case`. Descriptive names indicating content: `research_events.jsonl` not `data.jsonl`.

Directories: `snake_case`.

Record IDs: short prefix indicating record type, underscore, unique hash or UUID. Examples: `sig_a7f2c1`, `dec_91d28e1`, `r_5cfa2c1`.

Skill names: hyphenated, matching the skill's declared identifier. `ocas-scout` not `scout` or `ocas.scout`.

---

## Retention and Cleanup

Skills define retention policies in `config.json`.

Standard retention fields:
- `retention.days` — days to retain log entries (0 = indefinite)
- `retention.max_records` — maximum records per JSONL file before rotation

When a JSONL file exceeds `max_records`, rotate it:
1. Rename current file with date suffix: `events.jsonl` → `events.2026-03-10.jsonl`
2. Create new empty `events.jsonl` for new records
3. Archived files remain until retention period expires

Skills must not silently delete data. Expired data is removed by explicit maintenance operations only.

---

## Cross-Skill Access

Skills must not read or write another skill's private data directory (`commons/data/{other-skill}/`).

Cross-skill data sharing uses only:
- **Journals** — shared records in `commons/journals/`, readable by any skill
- **Errors** — shared records in `commons/errors/`, readable by any skill
- **Chronicle queries** — via `elephas.query` against `commons/db/ocas-elephas/`
- **Weave queries** — read-only against `commons/db/ocas-weave/`
- **Journal payloads** — typed fields in journal entries consumed by designated skills

---

## Initialization

When a skill's storage does not exist on first run:
1. Resolve `{agent_root}` by asking the agent platform for its home directory
2. Create `{agent_root}/commons/data/{skill-name}/`
3. Write default `config.json` with ConfigBase fields and skill-specific defaults
4. Create required empty JSONL files
5. Create `{agent_root}/commons/journals/{skill-name}/` directory
6. Create `{agent_root}/commons/errors/{skill-name}/` directory
7. Log initialization as a DecisionRecord

Skills initialize automatically rather than failing on missing storage.

---

## Validation

Skills with validation scripts check:
- Data root exists at `{agent_root}/commons/data/{skill-name}/`
- Journal root exists at `{agent_root}/commons/journals/{skill-name}/`
- Error root exists at `{agent_root}/commons/errors/{skill-name}/`
- `config.json` is valid JSON with required ConfigBase fields
- JSONL files contain valid JSON on every line
- No orphaned references
- Retention policies are being respected
- No data written outside the skill's own directories (except shared journals/errors)
