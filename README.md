# 🔨 Forge

> **Skill architect and builder — six-phase pipeline from idea to installable package.**

## Why Forge?

Building agent skills is harder than it looks. Most skills are either too thin to be useful or so bloated they're unmaintainable. Forge solves this with a mandatory six-phase pipeline — existence gate, classification, scoping, architecture, construction, validation — that ensures every skill is built to standard. The output is always the finished, installable package, never a design brief.

Skill packages follow the [agentskills.io](https://agentskills.io/specification) open standard and are compatible with OpenClaw, Hermes Agent, Claude, and any agentskills.io-compliant client.

## Quick Start

```
# Build a new skill
"Build me a skill that monitors RSS feeds and sends summaries to Slack"

# Critique an existing package
"Review the ocas-bower package for defects"
```

Forge auto-initializes on first use.

## What It Does

Forge is the only place where new OCAS skills are designed and built. Rather than generating a plan or brief, it runs a mandatory six-phase internal pipeline before writing a single file. Skills are classified by type — shortcut (20-120 lines), workflow (80-250 lines), or system (150-300 lines) — and each type has its own structural expectations. Mentor routes improvement proposals to Forge via journal payloads.

## Commands

| Command | Description |
|---|---|
| `forge.build` | Design, scope, build, and validate a complete skill package |
| `forge.critique` | Review a package and identify defects |
| `forge.repair` | Fix broken files in an existing package |
| `forge.classify` | Classify a proposed skill |
| `forge.validate` | Run validation checks on a package |
| `forge.scaffold` | Generate a minimal package skeleton |
| `forge.status` | Current build state |
| `forge.journal` | Write journal for the current run |
| `forge.update` | Self-update from GitHub source |

## Dependencies

- [Mentor](https://github.com/indigokarasu/mentor) — receives VariantProposal and VariantDecision files

## Scheduled Tasks

| Job | Schedule | Command |
|---|---|---|
| `forge:journal-scan` | Every heartbeat | Process incoming proposals from Mentor |
| `forge:update` | `0 0 * * *` | Self-update |

## Changelog

### v2.7.1 — April 26, 2026
- Version alignment per publishing spec

### v2.6.10 — April 15, 2026
- Synced reference docs with ocas-architecture

### v2.6.8 — April 12, 2026
- Added `{agent_root}/skills/` to filesystem write paths

---

*Forge is part of the [OCAS Agent Suite](https://github.com/indigokarasu).*