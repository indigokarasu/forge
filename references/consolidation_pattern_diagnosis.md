# Consolidation Pattern Diagnosis — May 2026

## Problem identified by user (May 22, 2026)

Forge kept creating standalone skills for content that belonged inside existing parent skills. Six standalone skills were identified and consolidated:

| Standalone (deleted) | Absorbed into | As |
|---|---|---|
| financial-sync | ocas-styx | references/financial-sync.md |
| system-maintenance | ocas-custodian | references/system-maintenance.md |
| ocas-expansion | ocas-weave | already in SKILL.md |
| bower-mempalace-ingest | ocas-bower | already in scripts/ |
| dispatch-status-from-files | ocas-dispatch | references/status_from_files.md |
| weave-db-maintenance | ocas-weave | references/database_maintenance.md |

## Root cause

1. Phase 1 (existence gate) was too weak — did NOT mandate checking whether a parent skill already owns the domain.
2. No parent-search before creation. The default output of forge.build is a new skill package.
3. ## Integrated: wrappers are a band-aid — content bolted on with wrapper headers instead of refactored into parent's proper structure.
4. Rule 7 in authoring_rules.md already said "prefer absorption" but wasn't enforced at build time.

## Fix applied (v2.9.0)

- Phase 1 now includes mandatory parent check
- Added standalone test (own invocation path + cron + journal = standalone justified)
- ## Integrated: wrappers added as explicit anti-pattern
- Pre-build default: absorption is default, creation is the exception
