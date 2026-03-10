# build.ocas-forge.v1.0.0

## Skill identity
- Name: Forge
- Package ID: ocas-forge
- Version: 1.1.0
- Author: Indigo Karasu
- Email: mx.indigo.karasu@gmail.com

## Build objective
Build a complete, ready-to-install Agent Skill package named `ocas-forge` that enables an OpenClaw agent to design, scope, plan, build, and validate other Agent Skills through a mandatory internal pipeline. The default product of Forge is the finished installable skill package itself, not a design brief, not a build handoff, and not a planning worksheet.

## External standard
Use Anthropic Agent Skills best practices as the public reference point for package quality, especially around strong descriptions, narrow scope, progressive disclosure, and keeping `SKILL.md` operational rather than bloated.

## Required product behavior
Forge must act as a skill architect and builder.

On every skill-building task, Forge must internally perform these phases in order:
1. Determine whether the proposed skill should exist as a skill at all.
2. Classify the skill type.
3. Define the skill’s scope and trigger boundary.
4. Decide the package architecture.
5. Plan the contents of each file.
6. Build the actual package.
7. Validate the result against the package standard.

These phases are mandatory internal behavior. They are not optional and they are not merely advisory.

## Default output model
Forge must return the complete ready-to-install Agent Skill package by default.

Forge must not default to returning:
- a build spec
- a design brief
- a research memo
- a package outline
- a critique without files

Design notes, scoping notes, build planning, and validation notes may be generated internally during execution, but they are process artifacts rather than the default saved output. Only expose or save those intermediate artifacts when the user explicitly asks for them.

## Skill purpose
Forge exists to let an OpenClaw agent build high-quality Agent Skills without relying on vague planning documents, hidden context, or ad hoc structure. Forge should improve both judgment and package quality by forcing disciplined design before generation.

## Skill type model
Forge must classify every requested skill into one of these types before building:

### 1. Shortcut skill
Use for narrow command wrappers, tool helpers, or single-surface utilities.
Characteristics:
- small surface area
- short `SKILL.md`
- mostly examples, commands, and caveats
- limited branching logic

### 2. Workflow skill
Use for multi-step tasks with repeatable process and some decision points.
Characteristics:
- moderate complexity
- explicit process flow
- stronger trigger guidance
- possible references and templates

### 3. System skill
Use for durable operating behaviors, evaluators, memory loops, orchestration layers, or complex domain systems.
Characteristics:
- highest complexity
- strong package architecture
- possible references and scripts
- most rigorous validation expectations

Forge must use this classification to control scope, package size, and supporting file decisions.

## Mandatory design pipeline
Before generating files, Forge must internally produce answers to the following design questions:

### Existence gate
- Is this actually better as an Agent Skill than as a one-off prompt, script, or normal conversation pattern?
- Is the task durable and repeatable enough to justify a skill?
- Is the task narrow enough to remain legible and maintainable?

If the answer is no, Forge must say so clearly instead of forcing a bad skill.

### Scope gate
- What exact job does the skill do?
- What does it explicitly not do?
- What adjacent capabilities should remain outside the skill?
- What is the smallest useful promise this skill can make?

### Trigger gate
- What user asks should trigger the skill?
- What adjacent asks should not trigger it?
- What language belongs in the description so routing works reliably?

### Architecture gate
- What belongs in `SKILL.md`?
- What belongs in `references/`?
- What belongs in `scripts/`?
- What belongs in `assets/`?
- Which of those folders are unnecessary and should be omitted?

### Validation gate
- How will the finished package be checked for scope clarity, routing quality, structure, and usefulness?
- What would count as failure even if the files technically exist?

Forge must use the results of these gates to shape the package before writing it.

## Package rules Forge must enforce
Forge must generate a real Agent Skill package. At minimum, every generated package must include:
- `skill.json`
- `SKILL.md`

Forge may add:
- `references/`
- `scripts/`
- `assets/`

Forge must not add support folders by default. Each additional folder must be justified by actual package needs.

### skill.json requirements
Forge must generate a valid `skill.json` with accurate metadata and a high-quality description.

The description must:
- clearly state what the skill does
- indicate when it should be used
- include realistic trigger phrasing where useful
- avoid vague branding language
- avoid generic claims like “helps with many tasks”

### SKILL.md requirements
Forge must generate a `SKILL.md` that is:
- operational
- concise relative to the skill type
- structured for scanability
- focused on what changes behavior
- free of process-template residue

`SKILL.md` must not read like:
- a meta-template
- an internal memo
- a planning worksheet
- a changelog
- an essay about why the skill matters

It must read like the actual instruction surface for the installed skill.

## Length and density rules
Forge must keep the main file proportional to complexity.

Recommended targets:
- shortcut skill: roughly 20–120 lines
- workflow skill: roughly 80–250 lines
- system skill: roughly 150–300 lines in `SKILL.md`, with deeper material moved outward if needed

These are targets, not hard caps, but Forge must treat unnecessary length as a quality defect.

## Progressive disclosure rules
Forge must keep only load-bearing behavior in `SKILL.md`.

Use `references/` only when the package needs:
- long-form examples
- reusable templates
- schemas or lookup tables
- domain detail that would bloat the main file

Use `scripts/` only when the package needs:
- deterministic file generation
- validation
- brittle or repetitive transforms
- exact operations that are unsafe to leave entirely to model judgment

Use `assets/` only when the package needs:
- reusable output artifacts
- examples intended as packaged resources
- starter files that the installed skill should reference directly

If a support folder exists, `SKILL.md` must explicitly tell the model when and why to use it.

## Visibility Classification

Forge must assign a visibility flag to every generated skill package.

visibility:
  public — safe for open distribution
  private — contains system architecture or personal data integrations

Rules:
- Dispatch must always be visibility: private
- Skills that handle personal data integrations or system internals should default to private
- Skills that are safe for open distribution should be public

The visibility flag must appear in the skill frontmatter or skill.json.

---

## Anti-patterns Forge must reject
Forge must actively avoid generating packages with these defects:
- vague or overly broad scope
- description that is too generic to route well
- `SKILL.md` that contains large amounts of background explanation with little operational value
- support folders that exist only for aesthetics or completeness theater
- duplicated guidance across files
- leftover template placeholders
- references to hidden context, prior build docs, or upstream internal documents
- treating local naming conventions as universal technical standards
- packaging multiple unrelated capabilities into one skill without a clear unifying surface
- returning plans instead of the actual package when a package was requested

## Commands

The built Forge skill must implement these commands:

- `forge.build` — design, scope, plan, build, and validate a complete Agent Skill package from a goal or build spec
- `forge.critique` — review an existing skill package and identify routing, scope, structure, and packaging defects
- `forge.repair` — rewrite or fix broken files in an existing skill package
- `forge.classify` — classify a proposed skill into shortcut, workflow, or system type
- `forge.validate` — run validation checks on a skill package (routing, structural, usefulness)
- `forge.scaffold` — generate a minimal skill package skeleton from basic parameters
- `forge.status` — return current build state if a multi-step build is in progress

---

## Required SKILL.md Sections for Forge Itself

The markdown body must contain these sections in this order:

1. `# Forge`
2. `## When to use`
3. `## When not to use`
4. `## Core promise`
5. `## Commands`
6. `## Mandatory design pipeline`
7. `## Skill type classification`
8. `## Package rules`
9. `## Anti-patterns to reject`
10. `## Support file map`
11. `## Validation rules`

---

## Storage Layout

Forge does not maintain persistent state between builds by default.

If build history tracking is enabled:

```text
.forge/
  config.json
  build_log.jsonl
  decisions.jsonl
```

### Config

File: `.forge/config.json`

Required fields:
- `build.default_skill_type`: default skill type if not specified (workflow)
- `build.auto_validate`: whether to run validation automatically after build (default true)
- `build.history_enabled`: whether to log build decisions (default false)
- `authoring.max_skillmd_lines`: soft target for SKILL.md length by type

---

## Forge’s own package architecture
Build `ocas-forge` itself as a system skill.

The generated `ocas-forge` package should likely include:
- `skill.json`
- `SKILL.md`
- `references/authoring_rules.md`
- `references/package_patterns.md`
- `references/examples.md`
- optional `scripts/validate_skill.py`
- optional `scripts/create_skill_stub.py`

### Content expectations for Forge itself
#### skill.json
Must describe Forge as a skill that builds complete ready-to-install Agent Skill packages through a mandatory design → scope → plan → build → validate pipeline.

#### SKILL.md
Must contain the operational behavior of Forge itself, including:
- when Forge should be used
- how Forge evaluates whether a skill should exist
- how Forge classifies skill type
- how Forge decides package structure
- how Forge writes packages
- how Forge validates them
- what Forge returns by default

#### references/authoring_rules.md
Distilled durable rules for good Agent Skill authoring.
Should cover:
- narrow scope
- strong descriptions
- proportional length
- progressive disclosure
- file-role separation
- common anti-patterns

#### references/package_patterns.md
Concrete package-shape guidance by skill type.
Should show common folder choices and what belongs where.

#### references/examples.md
Compact good examples of:
- strong descriptions
- small shortcut package patterns
- workflow package patterns
- system package patterns
- what not to do

#### scripts/validate_skill.py (optional but recommended)
A lightweight validator that checks for:
- required files
- valid JSON in `skill.json`
- missing description
- suspicious placeholder text
- empty support directories

#### scripts/create_skill_stub.py (optional)
A helper that can scaffold a minimal skill package skeleton from a small set of parameters.

## Required behavior when the user asks Forge for a skill
When asked to create a skill, Forge must:
1. infer the intended job of the skill
2. test whether the idea deserves to exist as a skill
3. classify skill type
4. define the smallest strong scope
5. derive the package structure
6. generate the package files
7. validate the package
8. return the complete package

Forge should ask follow-up questions only when essential information is truly missing and cannot be reasonably inferred.

## Required behavior when the user asks Forge to critique or repair a skill
Forge must be able to:
- review an existing package
- identify routing, scope, structure, and packaging defects
- propose a corrected architecture
- rewrite broken files
- remove decorative or redundant package elements
- tighten descriptions and `SKILL.md`

When repairing a skill, Forge should prefer direct correction over abstract advice.

## Output requirements for the coder building Forge
Build the real `ocas-forge` skill package and provide the full contents of every file created.

The final result must be installable as an Agent Skill package without requiring any additional hidden context.

Do not return only:
- a summary
- a design brief
- pseudocode
- a package outline
- partial file stubs

Return the actual package contents.

## Completion standard
The build is complete only if:
- the package includes all required files
- the package is coherent and installable
- Forge’s default product is clearly the finished skill package
- intermediate process artifacts are clearly treated as internal by default
- the package meaningfully improves the quality of future skill creation
- the files do not contain template residue, hidden-pipeline assumptions, or invented standards

---

## Responsibility Boundary

Forge designs, builds, and validates Agent Skill packages.

Forge does not evaluate skill performance or propose improvements. Skill evaluation and variant proposals belong to Mentor.

Forge does not execute skills or orchestrate workflows. Runtime orchestration belongs to Mentor.

---

## Optional Skill Cooperation

This skill may cooperate with other skills when present but must never depend on them.
If a cooperating skill is absent, this skill must still function normally.

- Mentor — receive variant proposals and promotion decisions that trigger skill rebuilds.
- All skills — analyze any existing skill package for critique, repair, or improvement.

---

## Journal Outputs

This skill emits the following journal types as defined in the OCAS Journal Specification (spec-ocas-Journals.md):

- Action Journal

Forge emits Action Journal entries recording skill build decisions, validation outcomes, and package generation events.

---

## Universal OKRs

This skill must implement the universal OKRs defined in the OCAS Journal Specification (spec-ocas-Journals.md).

Required universal OKRs:

- Reliability: success_rate >= 0.95, retry_rate <= 0.10
- Validation Integrity: validation_failure_rate <= 0.05
- Efficiency: latency trending downward, repair_events <= 0.05
- Context Stability: context_utilization <= 0.70
- Observability: journal_completeness = 1.0

Skill-specific OKRs should be defined in the built SKILL.md to measure domain-relevant outcomes.

---

## Visibility

visibility: public

---

## Final Response Format for the Coder

Return:

1. package tree
2. full contents of every file
3. brief validation summary

Do not return planning commentary, process narration, or references to absent documents.
