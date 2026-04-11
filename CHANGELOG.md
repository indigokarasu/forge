## v2.6.6 - 2026-04-11

- **chore:** Sync reference documentation with 2026-04-11 architecture coherence audit
- Updated authoring_rules.md: v2.6.4 → v2.7.0 (reflects current 2-skill active ecosystem)
- Updated ontology.md: v1.5.4 → v2.0.0 (major version update for scope change)
- References now accurately document only active OCAS skills (forge, triage)
- Marked 22 previously-documented skills as archived/historical reference

## v2.6.5 - 2026-04-10

- **feat:** Sync all reference documentation with ocas-architecture spec updates
- Updated authoring_rules.md, ontology.md, interfaces.md, journal.md, schemas.md, storage_conventions.md, workflow_plans.md
- Ensures forge always reflects latest architecture specifications

## v2.6.4 - 2026-04-10

- **feat:** Add skill.json configuration file for OCAS architecture coherence (architecture audit 2026-04-10)

## [2.6.1] - 2026-04-08

### Storage Architecture Update

- Replaced $OCAS_DATA_ROOT variable with platform-native {agent_root}/commons/ convention
- Replaced intake directory pattern with journal payload convention
- Added errors/ as universal storage root alongside journals/
- Inter-skill communication now flows through typed journal payload fields
- No invented environment variables — skills ask the agent for its root directory


## [2.6.0] - 2026-04-08

### Multi-Platform Compatibility Migration

- Adopted agentskills.io open standard for skill packaging
- Replaced skill.json with YAML frontmatter in SKILL.md
- Replaced hardcoded ~/openclaw/ paths with {agent_root}/commons/ for platform portability
- Abstracted cron/heartbeat registration to declarative metadata pattern
- Added metadata.hermes and metadata.openclaw extension points
- Compatible with both OpenClaw and Hermes Agent


## [2.5.5] - 2026-04-07

- Synced authoring_rules.md and ontology.md from ocas-architecture after coherence audit

## [2026-04-05] Sync Architecture Specifications
## [2.5.4] - 2026-04-07

- Patch version update after architecture coherence audit.


### Changes
- Synced all reference files with updated ocas-architecture specs:
  - authoring_rules.md: v2.6.2
  - ontology.md: v1.5.2
  - interfaces.md: v1.5
  - storage_conventions.md: latest
  - journal.md: latest
  - schemas.md: latest
- All changes reflect completion of Ontology Types audit for 24 OCAS skills
- Forge now references finalized Skill Entity Extraction and Signal Emission tables

### Impact
Forge skill developers building new skills will reference the most current architecture specifications and authoring rules.

## [2026-04-05] Sync Architecture Specifications

### Changes
- Synced all reference files with updated ocas-architecture specs:
  - authoring_rules.md: v2.6.2
  - ontology.md: v1.5.2
  - interfaces.md: v1.5
  - storage_conventions.md: latest
  - journal.md: latest
  - schemas.md: latest
- All changes reflect completion of Ontology Types audit for 24 OCAS skills
- Forge now references finalized Skill Entity Extraction and Signal Emission tables

### Impact
Forge skill developers building new skills will reference the most current architecture specifications and authoring rules.

