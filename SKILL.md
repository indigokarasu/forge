---
name: ocas-forge
description: >
  Forge: skill architect and builder. Designs, builds, and validates complete
  Agent Skill packages through a mandatory six-phase pipeline: existence gate,
  classify, scope, architecture, build, validate. Trigger phrases: 'create a
  new skill', 'build a skill', 'design a skill', 'review this skill', 'repair
  this skill', 'validate skill package', 'update forge'. Default output is the
  finished installable package. Do not use for skill evaluation or variant
  proposals (use Mentor).
metadata:
  author: Indigo Karasu
  email: mx.indigo.karasu@gmail.com
  version: "2.6.8"
  hermes:
    tags: [skill-building, architecture, validation]
    category: evolution
    cron:
      - name: "forge:update"
        schedule: "0 0 * * *"
        command: "forge.update"
  openclaw:
    skill_type: system
    visibility: public
    filesystem:
      read:
        - "{agent_root}/commons/data/ocas-forge/"
        - "{agent_root}/commons/journals/ocas-forge/"
      write:
        - "{agent_root}/commons/data/ocas-forge/"
        - "{agent_root}/commons/journals/ocas-forge/"
        - "{agent_root}/skills/"
    self_update:
      source: "https://github.com/indigokarasu/forge"
      mechanism: "version-checked tarball from GitHub via gh CLI"
      command: "forge.update"
      requires_binaries: [gh, tar, python3]
    cron:
      - name: "forge:update"
        schedule: "0 0 * * *"
        command: "forge.update"
---

# Forge

Forge is the system's skill architect — given a capability idea or broken existing package, it runs a mandatory six-phase internal pipeline covering existence gate, classification, scoping, architecture, construction, and validation before writing a single file. The default output is the finished, installable package with all file contents written; Forge never returns design briefs or plans in place of the real artifact.


## When to use

- Create a new Agent Skill from a goal or capability description
- Review or critique an existing skill package
- Repair broken or defective skill packages
- Classify whether a proposed capability deserves to be a skill
- Validate a skill package against OCAS standards


## When not to use

- Evaluating skill performance — use Mentor
- Running or orchestrating skills — use Mentor
- Web research — use Sift
- Building non-skill artifacts


## Responsibility boundary

Forge owns skill design, construction, and validation.

Forge does not own: skill evaluation or variant testing (Mentor), behavioral pattern analysis (Corvus), behavioral refinement (Praxis), experimentation (Fellow), system health and skill initialization (Custodian).

Forge receives VariantProposal and VariantDecision files from Mentor. It builds variant packages and applies promotion decisions.

## Ontology types

Forge operates on skill package data. Entities encountered during builds and reviews are recorded as entity observations in journals for downstream consumption.

## Commands

- `forge.build` — design, scope, build, and validate a complete skill package
- `forge.critique` — review a package and identify defects
- `forge.repair` — fix broken files in an existing package
- `forge.classify` — classify a proposed skill (shortcut, workflow, system)
- `forge.validate` — run validation checks on a package
- `forge.scaffold` — generate a minimal package skeleton
- `forge.status` — current build state if multi-step build in progress
- `forge.journal` — write journal for the current run; called at end of every run
- `forge.update` — pull latest from GitHub source; preserves journals and data


## Mandatory design pipeline

Run all phases before writing files:

1. **Existence gate** — Is this better as a skill than a one-off prompt?
2. **Classify** — Shortcut, workflow, or system?
3. **Scope** — Exact job, explicit non-goals, smallest useful promise
4. **Architecture** — What goes in SKILL.md vs references vs scripts vs assets?
5. **Build** — Write all files
6. **Validate** — Routing, structural, usefulness checks


## Skill type classification

- **Shortcut** — narrow tool wrapper. 20-120 line SKILL.md.
- **Workflow** — multi-step process. 80-250 line SKILL.md.
- **System** — durable behavior system. 150-300 line SKILL.md, deeper material in references.


## Package rules

Minimum package: SKILL.md with agentskills.io frontmatter. Add references/, scripts/, assets/ only when justified.

Read `references/authoring_rules.md` for full authoring standards.
Read `references/package_patterns.md` for package shape guidance by type.
Read `references/examples.md` for good and bad examples.


## Run completion

After every Forge command (build, critique, repair, validate):

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

Action Journal — every build, critique, repair, validation, and variant processing run.

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
5. Register heartbeat entry `forge:journal-scan` in `HEARTBEAT.md` if not already present
6. Register cron job `forge:update` if not already present (check the platform scheduling registry first)
7. Log initialization as a DecisionRecord in `decisions.jsonl`


## Background tasks

| Job name | Mechanism | Schedule | Command |
|---|---|---|---|
| `forge:journal-scan` | heartbeat | every heartbeat pass | Check journal payload fields (see interfaces specification) for VariantProposal and VariantDecision files from Mentor; process and move to the consumer's ingestion log |
| `forge:update` | cron | `0 0 * * *` (midnight daily) | `forge.update` |

Heartbeat registration: append `forge:journal-scan` entry to `{agent_root}/HEARTBEAT.md` if not already present.

Registration during `forge.init`:
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


## Visibility

public


## Support file map

| File | When to read |
|---|---|
| `references/authoring_rules.md` | Before any build, critique, or validation |
| `references/package_patterns.md` | When deciding package shape by skill type |
| `references/examples.md` | When reviewing descriptions or detecting anti-patterns |
| `references/journal.md` | Before forge.journal; at end of every run |

## Integrated: skill-adaptation

Adapt third-party agent skills (OpenClaw, etc.) to work with Hermes by swapping path references, command references, and metadata.

### When to use this skill
A user shares a GitHub repo containing a `SKILL.md` or `skill.json` designed for a different agent framework (typically OpenClaw/OCAS).

### Steps
#### 1. Clone the repo
```bash
git clone https://github.com/<user>/<skill-repo>.git ~/.hermes/skills/<skill-name>/
```

#### 2. Find all framework-specific references
```python
import os
for root, dirs, files in os.walk('~/.hermes/skills/<skill-name>'):
    dirs[:] = [d for d in dirs if d != '.git']
    for f in files:
        fpath = os.path.join(root, f)
        with open(fpath) as fh:
            content = fh.read()
        if 'openclaw' in content.lower() or '~/openclaw' in content:
            print(fpath)
```

#### 3. Swap references
Use this comprehensive replacement list (order matters):
```python
replacements = [
    ('~/openclaw/', '~/.hermes/'),
    ('~/openclaw', '~/.hermes'),
    ('openclaw skill install', 'skill_view'),
    ('openclaw ', 'hermes '),
    ('OpenClaw', 'Hermes'),
    ('ocas-', 'hermes-'),
    ('OCAS ', 'Hermes '),
    ('OCAS_', 'hermes_'),
    ('OpenClaw Agent', 'Hermes Agent'),
    ('openclaw-agent', 'hermes-agent'),
    ('openclaw/', '.hermes/'),
    ('openclaw:', 'hermes:'),
    ('openclaw', 'hermes'),  # catch-all for any remaining lowercase
]
```
**Important**: Use `errors='replace'` when reading to handle binary files like `.DS_Store` that may get caught in `os.walk()`.

#### 4. Verify no references remain
Run the scan from Step 2 again — should return zero results.

#### 5. Create required directories
Check for `~/` paths referenced in the skill and create them under `~/.hermes/`:
- `~/.hermes/data/<skill-dir>/`
- `~/.hermes/journals/<skill-dir>/`
- Any other paths referenced in storage layout sections

#### 6. Fix skill name in frontmatter
**Important**: The bulk `ocas-` → `hermes-` replacement will rename `name: ocas-skillname` to `name: hermes-skillname`. This is wrong — the Hermes skill name should just be the directory name (e.g., `name: bower`, `name: sands`). Always do:
```python
# After bulk replacements, fix the name
content = content.replace(f'name: hermes-{skill_name}', f'name: {skill_name}', 1)
```
Also fix the metadata tag: `metadata: {"openclaw":...}` → `metadata: {"hermes":...}`

#### 7. Write default config
If the skill references a config file, create it with sensible defaults.

#### 8. Register cron jobs
If the skill defines scheduled tasks, register them with the Hermes `cronjob` tool:
```
cronjob(action='create', name=..., prompt=..., schedule=..., skill='<skill-name>', deliver='origin')
```

### Pitfalls
- **skill.json vs SKILL.md**: Skills from other frameworks often use `skill.json` which has a different schema. The SKILL.md YAML frontmatter is what Hermes reads — make sure the SKILL.md `name` field is correct.
- **OpenClaw cron commands**: References to `openclaw cron list` won't work. Replace with instructions to use the Hermes `cronjob` tool (`action='list'`).
- **Signal emission paths**: Skills that emit to other ecosystem tools (like Elephas, Vesper) write to `~/openclaw/db/` — change to `~/.hermes/db/`. The target tools may not exist in Hermes, but the paths should still be consistent.
- **Don't touch .git**: When walking directories for replacements, always skip `.git` directories.
- **Verify with case-insensitive search**: Some references may be `OpenClaw`, `openclaw`, or `OPENCLAW`. Search case-insensitively.
- **Environment variables in JS/Node scripts**: Skills with `.js` or `.sh` scripts may reference env vars like `OPENCLAW_MODEL`, `OC_VERSION`. Update these to `HERMES_MODEL`, `HERMES_VERSION` etc.
- **install: frontmatter line becomes invalid**: After bulk replacements, `install: openclaw skill install ...` becomes `install: hermes skill install ...` which isn't a valid Hermes command. Remove these lines entirely:
```python
import re
content = re.sub(r'^install:.*$', '', content, flags=re.MULTILINE)
content = re.sub(r'\\n{3,}', '\\n\\n', content)  # clean up double blank lines
```
- **source: frontmatter line is worth keeping**: The `source: https://github.com/...` field survives replacement and remains useful metadata for self-update commands.
- **Cron job prompts must be self-contained**: When registering cron jobs, the prompt argument must fully describe what to do — no context from the current session is available. Include the skill name and key steps.

### Batch multi-skill adaptation
When installing multiple skills from the same author, do them all at once:
```bash
cd ~/.hermes/skills
git clone https://github.com/<user>/<skill1>.git && \
git clone https://github.com/<user>/<skill2>.git && \
...
```
Then run the replacement script across all skills in a single pass:
```python
import os
skill_names = ['skill1', 'skill2', 'skill3', ...]  # directory names
for name in skill_names:
    skill_path = os.path.join('~/.hermes/skills', name)
    for root, dirs, files in os.walk(skill_path):
        dirs[:] = [d for d in dirs if d != '.git']
        for fname in files:
            fpath = os.path.join(root, fname)
            # Apply replacements... (see Step 3 replacements list)
            
    # Fix skill name after bulk replacement
    skill_md = f'~/.hermes/skills/{name}/SKILL.md'
    with open(skill_md) as f:
        content = f.read()
    content = content.replace(f'name: hermes-{name}', f'name: {name}', 1)
    content = content.replace(f'name: ocas-{name}', f'name: {name}', 1)
    # ... also fix metadata: {"openclaw": -> {"hermes":
```
Verify all skills in a single pass:
```python
for name in skill_names:
    # Check each file for remaining openclaw/OCAS references
    # Confirm name: field is correct in SKILL.md
```

### Non-standard repo naming
Some skills use `ocas-` prefix in the repo name (e.g., `ocas-spot` in `https://github.com/indigokarasu/ocas-spot`). Clone to the plain name:
```bash
git clone https://github.com/<user>/ocas-<skill>.git ~/.hermes/skills/<skill>/
```
This avoids having nested `ocas-` prefixes in paths like `~/.hermes/skills/ocas-spot/`.

### Post-adaptation cleanup checklist for indigokarasu skills
When adapting skills from github.com/indigokarasu, these `install:` lines appear in 6 of 7 skills and must be removed:
- sands, rally, scout, taste, voyage, vesper — all have `install: openclaw skill install https://github.com/indigokarasu/<skill>`
- bower and haiku do NOT have install lines (already clean)
