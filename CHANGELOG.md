## [2.6.0] - 2026-04-08

### Multi-Platform Compatibility Migration

- Adopted agentskills.io open standard for skill packaging
- Replaced skill.json with YAML frontmatter in SKILL.md
- Replaced hardcoded ~/openclaw/ paths with $OCAS_DATA_ROOT/ for platform portability
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

