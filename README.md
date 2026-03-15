# 🔨 forge

Agent skill builder and optimizer. Transforms natural prompts into production-ready agent capabilities with architecture validation.

---

## 📖 Overview

Forge builds Agent Skills. Takes capability ideas through a 6-phase pipeline (existence, classify, scope, architecture, build, validate) to produce complete, installable skill packages.

---

## 🚀 Quick Start

### 📦 Installation

```bash
git clone https://github.com/indigokarasu/forge.git
```

### 🛠️ Tool Surface

```
forge.build_skill(capability, ...)          🔨 Build new skill
forge.validate_package(skill_path, ...)     ✓ Validate skill package
forge.review_skill(skill_path, ...)         🔍 Review existing skill
forge.optimize_description(skill, ...)      ✨ Optimize routing
forge.generate_package(spec, ...)           📦 Generate complete package
```

### 📤 Output

- **forge_package** — Complete skill directory structure
- **forge_validation** — Validation report and fixes
- **forge_summary** — Package completeness summary

---

## ⚙️ Configuration

Read `SKILL.md` for operational details, build pipeline, and cooperation with other skills.

Read `references/` for schemas and examples.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
