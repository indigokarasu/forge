# Journal Scan — Cron Mode Guide

The `forge:journal-scan` cron job (`*/5 * * * *`) runs without a user present.
This means **`execute_code` is blocked at runtime**. Do not call it.

## What to use instead

| Task | Tool | Example |
|------|------|---------|
| Scan directories for JSON files | `terminal()` with `find`, `ls` | `find ... -name "*.json"` |
| Read proposal/decision file contents | `read_file()` | Read individual `.json` files |
| Compare file lists (intake vs processed) | `terminal()` with shell `grep` | Loop + `grep -q` |
| Write journal entry | `write_file()` | Write JSON journal to `commons/journals/ocas-forge/` |
| Apply fixes to target skills | `patch()` | Targeted edits to target skill files |
| Append to decisions.log | `terminal()` with `echo >>` | `echo '{...}' >> decisions.jsonl` |

## Where proposals can land

Mentor drops VariantProposal and VariantDecision files in multiple locations.
Check ALL of these during a scan:

1. `{agent_root}/commons/data/ocas-forge/intake/` — primary intake directory
2. `{agent_root}/commons/data/ocas-forge/proposals/` — subdirectory where newer proposals may land
3. `{agent_root}/commons/data/ocas-forge/` (data root) — stale copies can linger here

## Cross-reference against processed

Check BOTH locations for already-processed filenames:
- `{agent_root}/commons/data/ocas-forge/intake/processed/`
- `{agent_root}/commons/data/ocas-forge/processed/`

Any `.json` file in the scan locations above that is NOT in either processed
directory is unprocessed and should be handled.

## After processing

1. Copy (don't move) processed files to `processed/` — originals may stay in `proposals/`
2. Write journal to `{agent_root}/commons/journals/ocas-forge/YYYY-MM-DD/`
3. Append decision to `decisions.jsonl` via `echo >>`

## Common pitfall: proposals/ not intake/

As of May 2026, Mentor dropped proposals into `proposals/` subdirectory rather
than `intake/`. If you only check `intake/` and the data root, you will miss
these. Always include `proposals/` in the scan.
