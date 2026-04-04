## [2026-04-04] Forge References Synced

### Changes
- Synced authoring_rules.md from ocas-architecture (v2.6.1)
- Updated to reflect all 24 active OCAS skills
- Added ocas-multipass and ocas-vibes to responsibility boundaries

### Validation
- ✓ References synchronized with architecture specifications
- ✓ Version: 2.5.1 → 2.5.2

## [2026-04-04] Spec Compliance Update

### Changes
- Added missing SKILL.md sections per ocas-skill-authoring-rules.md
- Updated skill.json with required metadata fields
- Ensured all storage layouts and journal paths are properly declared
- Aligned ontology and background task declarations with spec-ocas-ontology.md

### Validation
- ✓ All required SKILL.md sections present
- ✓ All skill.json fields complete
- ✓ Storage layout properly declared
- ✓ Journal output paths configured
- ✓ Version: 2.5.0 → 2.5.1

# Changelog

All notable changes to forge are documented here.

## [2.5.0] - 2026-04-02

### Added
- Structured entity observations in journal payloads (`entities_observed`, `relationships_observed`, `preferences_observed`)
- `user_relevance` tagging on journal observations (default `agent_only` for system-internal entities)
- Elephas journal cooperation in skill cooperation section

### Changed
- Removed "does not emit Signals to Elephas" — Forge now records entity observations in journals

## [2.4.4] - 2026-04-02

### Changed
- Updated references to reflect architecture spec sync (v1.5 ontology, v1.5 interfaces, v2.5.0 authoring rules)
- Synced authoring_rules.md, ontology.md, and interfaces.md from ocas-architecture

## [2.4.3] - 2026-04-01

### Changed
- Synced authoring rules with latest OCAS architecture specification
- Updated storage conventions reference
- Added ocas-sands to core skill list

## [2.4.2] - 2026-03-31

### Fixed
- Variant proposal handling improvements

[2.4.3]: https://github.com/indigokarasu/forge/releases/tag/v2.4.3
[2.4.2]: https://github.com/indigokarasu/forge/releases/tag/v2.4.2
