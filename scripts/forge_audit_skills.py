#!/usr/bin/env python3
"""
Forge Skill Auditor — collects skill metadata for LLM-driven overlap analysis.

Outputs a JSON report of all non-system skills with their names, descriptions,
and purpose summaries. The actual overlap judgment is done by the LLM in the
cron job prompt — not by keyword matching here.

Usage:
  python3 forge_audit_skills.py [--output /path/to/report.json]
"""

import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

SKILLS_DIR = Path(os.environ.get("HERMES_SKILLS_DIR", "<hermes-root>/skills"))
OUTPUT_DEFAULT = Path("/tmp/forge_audit_report.json")

# Known system skills — never flag these
KNOWN_SYSTEMS = {
    "ocas-forge", "ocas-mentor", "ocas-custodian", "ocas-elephas",
    "ocas-weave", "ocas-dispatch", "ocas-sift", "ocas-scout",
    "ocas-bower", "ocas-sands", "ocas-styx", "ocas-taste",
    "ocas-vesper", "ocas-vibes", "ocas-look", "ocas-imagine",
    "ocas-inception", "ocas-fellow", "ocas-corvus", "ocas-praxis",
    "ocas-finch", "ocas-lucid", "ocas-multipass", "ocas-reach",
    "ocas-spot", "ocas-voyage", "ocas-haiku", "ocas-bones",
    "ocas-rally",
}


def read_frontmatter(skill_dir: Path) -> dict:
    """Read YAML frontmatter from SKILL.md."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return {}
    content = skill_md.read_text(encoding="utf-8", errors="ignore")
    if not content.startswith("---"):
        return {}
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    result = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if ":" in line and not line.startswith("#"):
            key, _, val = line.partition(":")
            result[key.strip()] = val.strip().strip('"').strip("'")
    return result


def get_purpose(skill_dir: Path) -> str:
    """Extract the purpose/description from a skill's frontmatter and body."""
    fm = read_frontmatter(skill_dir)
    desc = fm.get("description", "")
    if desc and not desc.startswith(">"):
        return desc[:500]

    # Fallback: first meaningful paragraph of body
    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        content = skill_md.read_text(encoding="utf-8", errors="ignore")
        parts = content.split("---", 2)
        body = parts[2] if len(parts) >= 3 else content
        for para in body.split("\n\n"):
            para = para.strip()
            if para and not para.startswith("#") and len(para) > 20:
                return para[:500]
    return ""


def get_skill_files(skill_dir: Path) -> dict:
    """List scripts and references in a skill."""
    result = {"scripts": [], "references": []}
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.exists():
        result["scripts"] = [f.name for f in scripts_dir.iterdir() if f.is_file()]
    refs_dir = skill_dir / "references"
    if refs_dir.exists():
        result["references"] = [f.name for f in refs_dir.iterdir() if f.is_file()]
    return result


def collect_skills() -> list[dict]:
    """Collect metadata for all non-system skills."""
    skills = []
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        name = skill_dir.name
        if name in KNOWN_SYSTEMS or name.startswith("."):
            continue
        if not (skill_dir / "SKILL.md").exists():
            continue

        fm = read_frontmatter(skill_dir)
        skills.append({
            "name": name,
            "description": fm.get("description", ""),
            "version": fm.get("version", ""),
            "category": fm.get("category", ""),
            "purpose": get_purpose(skill_dir),
            "files": get_skill_files(skill_dir),
            "path": str(skill_dir),
        })
    return skills


def main():
    output_path = Path(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else OUTPUT_DEFAULT
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_path = Path(sys.argv[idx + 1])

    skills = collect_skills()
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "skills_dir": str(SKILLS_DIR),
        "known_systems_excluded": sorted(KNOWN_SYSTEMS),
        "skills_scanned": len(skills),
        "skills": skills,
    }

    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Audit report written to {output_path}")
    print(f"Skills scanned: {len(skills)}")
    for s in skills:
        print(f"  - {s['name']}: {s['purpose'][:80]}...")


if __name__ == "__main__":
    main()
