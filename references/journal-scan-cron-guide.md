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

## Common pitfall: path mismatch in cross-reference

When using `comm` to compare file lists between `proposals/` and `processed/`
directories, **strip the directory prefix first**. `comm` compares lines
literally — `proposals/vp_0625cecd.json` will never match `vp_0625cecd.json`,
making every file appear unprocessed.

**Wrong:**
```bash
comm -23 <(ls proposals/*.json | sort) <(ls processed/*.json | sort)
```

**Right:**
```bash
comm -23 <(ls proposals/*.json | sed 's|proposals/||' | sort) \
         <(ls processed/*.json | sed 's|processed/||' | sort)
```

Or use `basename`:
```bash
comm -23 <(for f in proposals/*.json; do basename "$f"; done | sort) \
         <(for f in processed/*.json; do basename "$f"; done | sort)
```

After running the comparison, **verify with a spot-check**: pick one filename
from the "unprocessed" list and `ls` it in the processed dir to confirm it's
actually missing before taking action.

## Common pitfall: unifying two processed directories for cross-reference

There are TWO processed directories: `intake/processed/` and `processed/`. Both
must be unified into a single deduplicated set before comparing against the
proposals list. If you `ls` both dirs in a single pipeline without dedup, a
file that exists in both processed dirs will appear twice on the right side —
but that's harmless. The real danger is the opposite: if you only check ONE
of the two processed dirs, files that were copied to the other will appear
as false positives (unprocessed).

**Wrong (only checks one processed dir):**
```bash
comm -23 <(ls proposals/*.json | xargs -I{} basename {} | sort) \
         <(ls processed/*.json | xargs -I{} basename {} | sort)
```

**Right (unifies both processed dirs with dedup):**
```bash
comm -23 \
  <(ls proposals/*.json | xargs -I{} basename {} | sort -u) \
  <(cat <(ls intake/processed/*.json 2>/dev/null | xargs -I{} basename {}) \
        <(ls processed/*.json 2>/dev/null | xargs -I{} basename {}) \
   | sort -u)
```

The `2>/dev/null` guards against the case where one of the processed dirs
doesn't exist yet (e.g., fresh Forge install). The `sort -u` on each side
ensures clean comparison even if a file exists in both processed dirs.

## Common pitfall: `config.json` false positive in data root scan

When scanning `{agent_root}/commons/data/ocas-forge/*.json` for unprocessed
proposal/decision files, the `config.json` file (Forge's own config) will appear
as a "new" file if you only check against processed directories. It is NOT a
proposal or decision — skip it.

**Fix:** When scanning the data root, exclude `config.json`:

```bash
find {agent_root}/commons/data/ocas-forge/ -maxdepth 1 -name "*.json" \
  ! -name "config.json" -type f
```

Or filter it out in the cross-reference step: after building the list of
candidate files, remove any filename that is exactly `config.json` before
comparing against processed.

## Common pitfall: `write_file` does not resolve template placeholders in paths

When writing the journal entry with `write_file()`, the `path` parameter is taken
literally -- template placeholders like `{{unix}}`, `{{timestamp}}`, or similar
are **not** auto-resolved. Using `path:
".../r_20260605_journal-scan-{{unix}}.json"` will create a file with a literal
`{{unix}}` in the name, requiring a manual `mv` to fix.

**Always resolve timestamps before calling `write_file`:**

```bash
# Resolve the timestamp first via terminal
TS=$(date +%Y%m%d%H%M%S)
# Then use the resolved value in the write_file path
```

Or get a UNIX timestamp:
```bash
date +%s   # returns e.g. 1780707441
```

**Wrong:**
```
write_file(path=".../journal-scan-{{unix}}.json", ...)
```

**Right:**
```
# Step 1: terminal("date +%s") -> e.g. 1780707441
# Step 2: write_file(path=".../journal-scan-1780707441.json", ...)
```
