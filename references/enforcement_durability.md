# Enforcement Durability Patterns

## Problem
When fixing behavioral issues (e.g., "use Forge instead of built-in skill writer"), it's tempting to write the fix as a note in MEMORY.md. This is **advisory only** — it doesn't structurally enforce the behavior and can be skipped or forgotten.

## Rule
**Never rely on MEMORY.md as the sole enforcement mechanism for behavioral rules.**

Enforcement must live in the skill's SKILL.md itself — specifically in the mandatory pipeline phases, anti-patterns, or pitfalls sections. That's the artifact that gets loaded and followed during execution.

## What survives what

| Artifact | Survives hermes core update? | Survives skill update? | Enforces behavior? |
|---|---|---|---|
| MEMORY.md | Yes (in <hermes-root>/) | Yes | No — advisory only |
| Forge SKILL.md | Yes (in <hermes-root>/skills/) | Only if not overwritten by forge.update | Yes — loaded before skill creation |
| skill_manage tool | No — part of hermes core | No | N/A (it's the tool being governed) |

## Pattern
1. Identify the behavioral rule.
2. Encode it as a hard gate or anti-pattern in the relevant skill's SKILL.md.
3. Optionally note it in MEMORY.md for cross-session awareness.
4. The SKILL.md is the enforcement; MEMORY.md is the reminder.

## Example
- **Bad**: MEMORY.md says "always use Forge before creating skills" → easily skipped.
- **Good**: Forge SKILL.md phase 1 has hard gates (checks A/B/C) that must pass before any skill creation proceeds → structurally enforced.
