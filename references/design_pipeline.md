# Design Pipeline

The mandatory pipeline Forge runs before writing any files. Seven phases total.

## Phase 1: Existence Gate (HARD GATE — must pass all 3 checks before proceeding)

### Check A — Parent search (mandatory first step)
Call `skills_list` to enumerate all existing skills. For each skill whose domain overlaps the proposed capability, call `skill_view` to read its full content. Ask: "Does this existing skill already own this domain?" If yes → **STOP. Do not create a new skill.** Add the content to the parent as a `references/` doc, `scripts/` file, or new SKILL.md section. Record the decision in `decisions.jsonl`.

### Check B — Standalone test (all 3 must be true)
A new skill is only justified if it has: (a) its own independent invocation path (user or cron triggers it directly by name), (b) its own cron jobs or background tasks, AND (c) its own journal output. If any of these is missing → it's a support file, not a skill. Absorb into parent.

### Check C — Absorption test
Can this content fit as a `references/<topic>.md` or `scripts/<name>.py` inside an existing skill? If yes → **absorb, don't spawn.** Creating a standalone skill for content that fits in a reference file is the #1 cause of skill proliferation. Default to absorption.

**Only proceed to phase 2 if all 3 checks pass.** If the answer is "absorb," execute the absorption immediately: add the content to the parent skill's appropriate subdirectory, update the parent's reference table, and record the decision.

## Phase 1.5: Research (MANDATORY before Classify)

**Trigger:** Phase 1 passed — no local parent owns the domain. Before classifying and scoping a new skill, research whether the capability already exists externally.

**Goal:** Avoid building what already exists. A skill that duplicates an existing GitHub repo or published skill package is waste.

### Step A — GitHub Search (via `gh` CLI, NEVER browser search)

Search GitHub for repos that solve the proposed capability. Use `gh search repos` with multiple query variants for broad coverage:

```bash
# Primary search with the capability name / key terms
gh search repos "<capability keywords>" --sort stars --limit 10 --json fullName,description,url,stargazersCount,language,updatedAt

# Secondary search with alternative terms
gh search repos "<alternative keywords>" --sort stars --limit 5 --json fullName,description,url,stargazersCount,language,updatedAt
```

**Selection criteria:** Pick top 10 repos by relevance + stars. Prioritize:
- Updated within last 6 months (active maintenance)
- ≥10 stars (community validation)
- Direct domain overlap (not tangential)

### Step B — Deep-read repos (via `gh` API, NEVER browser)

For each selected repo, fetch structure and key files using `gh api`:

```bash
# Get repo README
gh api repos/{owner}/{repo}/readme --jq '.content' | base64 -d

# Get top-level file structure
gh api repos/{owner}/{repo}/git/trees/main?recursive=1 --jq '.tree[].path' 2>/dev/null || \
gh api repos/{owner}/{repo}/git/trees/master?recursive=1 --jq '.tree[].path'

# Fetch key source files for comparison (limit to 5-8 files per repo)
gh api repos/{owner}/{repo}/contents/{path} --jq '.content' | base64 -d
```

**What to read:** README, main entry point, core logic files, package.json/pyproject.toml/setup.py for dependencies. Do NOT browser-scrape. Do NOT clone to disk. Use `gh api` exclusively.

### Step C — Compare and Decide

For each repo, assess on three axes:

| Axis | Question |
|------|----------|
| **Coverage** | Does this repo solve ≥80% of the proposed capability? |
| **Quality** | Is it actively maintained, well-documented, production-ready? |
| **Compatibility** | Can it be wrapped/integrated into an OCAS skill cleanly? (license, language, dependencies) |

**Decision matrix:**

- **≥80% coverage + high quality + compatible** → **WRAP, don't build.** Create the new skill as a thin wrapper/adapter around the existing repo. Credit the source in the skill's `references/` and frontmatter.
- **50-80% coverage** → **Fork/adapt.** Use the repo as a foundation, extend it for the remaining gap. Credit the source.
- **<50% coverage OR incompatible license OR unmaintained** → **Build fresh.** Proceed to Phase 2. Record why existing repos were insufficient.

**Record all findings** in `decisions.jsonl`: which repos were reviewed, their scores, and the final decision (wrap/fork/build). This prevents re-researching the same repos on future builds.

### Step D — Skill Library Search

In addition to GitHub, search the OCAS skill library and other skill registries:

- Check `https://github.com/indigokarasu` for OCAS skills that may already cover the domain
- Search AgentSkill hub (https://agentskill.sh) for published packages
- Check Hermes bundled skills via `skills_list`

If a published skill package covers the domain → evaluate whether to install it directly instead of building new. Record the decision.

**Research is complete when:** At least 10 GitHub repos have been reviewed OR the search conclusively shows no adequate existing solution. Proceed to Phase 2.

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
