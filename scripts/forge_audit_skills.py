#!/usr/bin/env python3
"""
Forge Skill Auditor — scans for orphan skills and consolidates them.

Runs as a cron job. For each skill in the skills directory:
1. Reads the skill's description and purpose.
2. Checks if its functionality overlaps with an existing parent skill.
3. If overlap found: absorbs content into parent's references/scripts, removes orphan.
4. Logs all decisions to forge's decisions.jsonl.

Exit codes:
  0 — no orphans found, or all consolidated cleanly
  1 — orphans found and need human review
  2 — error during audit
"""

import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

# --- Configuration ---
SKILLS_DIR = Path(os.environ.get("HERMES_SKILLS_DIR", "<hermes-root>/skills"))
FORGE_DATA_DIR = Path(os.environ.get("FORGE_DATA_DIR", "/root/indigo-repo/commons/data/ocas-forge"))
DECISIONS_FILE = FORGE_DATA_DIR / "decisions.jsonl"
AUDIT_LOG_FILE = FORGE_DATA_DIR / "audit_log.jsonl"

# Skills that are known parents — never flag these as orphans
KNOWN_SYSTEMS = {
    # All ocas-* skills are known parents — never auto-consolidate these
    "ocas-forge", "ocas-mentor", "ocas-custodian", "ocas-elephas",
    "ocas-weave", "ocas-dispatch", "ocas-sift", "ocas-scout",
    "ocas-bower", "ocas-sands", "ocas-styx", "ocas-taste",
    "ocas-vesper", "ocas-vibes", "ocas-look", "ocas-imagine",
    "ocas-inception", "ocas-fellow", "ocas-corvus", "ocas-praxis",
    "ocas-finch", "ocas-lucid", "ocas-multipass", "ocas-reach",
    "ocas-spot", "ocas-voyage", "ocas-haiku", "ocas-bones",
    "ocas-rally",
}

# Naming guard: NEVER create new ocas-* skills without explicit user authorization
# If a proposed skill name starts with "ocas-", it must be explicitly requested by the user
RESERVED_PREFIXES = ("ocas-",)

# Keywords that suggest a skill is a helper/patch for a known system
PARENT_KEYWORDS = {
    "ocas-weave": ["weave", "contact", "google contacts", "sync", "ladybug", "database", "db"],
    "ocas-dispatch": ["dispatch", "email", "gmail", "message", "send", "inbox", "triage"],
    "ocas-sift": ["sift", "search", "research", "web", "scout", "searxng"],
    "ocas-bower": ["bower", "drive", "google drive", "organize", "file", "folder"],
    "ocas-sands": ["sands", "calendar", "event", "schedule", "appointment"],
    "ocas-styx": ["styx", "financial", "transaction", "money", "sync"],
    "ocas-elephas": ["elephas", "chronicle", "knowledge graph", "kg", "entity"],
    "ocas-vesper": ["vesper", "briefing", "daily", "digest", "summary"],
    "ocas-vibes": ["vibes", "voice", "writing", "style", "tone", "prose"],
    "ocas-look": ["look", "image", "screenshot", "visual"],
    "ocas-imagine": ["imagine", "image gen", "text-to-image", "art"],
    "ocas-inception": ["inception", "simulation", "environment", "sandbox"],
    "ocas-fellow": ["fellow", "experiment", "benchmark", "test"],
    "ocas-custodian": ["custodian", "health", "monitor", "log", "maintenance"],
    "ocas-finch": ["finch", "improvement", "evolution", "adapt"],
    "ocas-lucid": ["lucid", "journal", "nightly", "curator"],
    "ocas-multipass": ["multipass", "delegate", "tool", "access"],
    "ocas-reach": ["reach", "real-time", "live", "query", "external"],
    "ocas-spot": ["spot", "booking", "appointment", "service"],
    "ocas-voyage": ["voyage", "travel", "itinerary", "trip"],
    "ocas-haiku": ["haiku", "bluesky", "social", "post"],
    "ocas-bones": ["bones", "bet", "prediction", "market", "odds"],
    "ocas-rally": ["rally", "portfolio", "stock", "invest", "financial"],
    "ocas-taste": ["taste", "preference", "behavior", "consumption"],
    "ocas-corvus": ["corvus", "pattern", "analysis", "exploratory"],
    "ocas-praxis": ["praxis", "refinement", "behavioral", "loop"],
}


def read_skill_frontmatter(skill_dir: Path) -> dict:
    """Read YAML frontmatter from SKILL.md."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return {}
    content = skill_md.read_text(encoding="utf-8", errors="ignore")
    if not content.startswith("---"):
        return {}
    # Extract frontmatter between first two --- markers
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    raw = match.group(1)
    result = {}
    for line in raw.splitlines():
        line = line.strip()
        if ":" in line and not line.startswith("#"):
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            result[key] = val
    return result


def get_skill_purpose(skill_dir: Path) -> str:
    """Extract the purpose/description from a skill."""
    fm = read_skill_frontmatter(skill_dir)
    # Check description field
    desc = fm.get("description", "")
    if desc:
        return desc.lower()
    # Fallback: read first few lines of body
    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        content = skill_md.read_text(encoding="utf-8", errors="ignore")
        # Skip frontmatter
        parts = content.split("---", 2)
        if len(parts) >= 3:
            body = parts[2]
        else:
            body = content
        # Get first non-empty paragraph
        for para in body.split("\n\n"):
            para = para.strip()
            if para and not para.startswith("#"):
                return para[:300].lower()
    return ""


def check_overlap(orphan_name: str, orphan_purpose: str) -> list[str]:
    """Check if an orphan's purpose overlaps with known parent skills."""
    candidates = []
    combined_text = f"{orphan_name} {orphan_purpose}".lower()

    for parent, keywords in PARENT_KEYWORDS.items():
        if parent == orphan_name:
            continue
        match_count = sum(1 for kw in keywords if kw in combined_text)
        if match_count >= 2:
            candidates.append(parent)
        elif match_count == 1 and any(kw in orphan_name.lower() for kw in keywords):
            candidates.append(parent)

    return candidates


def consolidate_orphan(orphan_dir: Path, parent_name: str, candidates: list[str]) -> dict:
    """Absorb orphan content into parent skill. Returns decision record."""
    parent_dir = SKILLS_DIR / parent_name
    if not parent_dir.exists():
        return {"error": f"Parent {parent_name} not found", "orphan": orphan_dir.name}

    ref_dir = parent_dir / "references"
    ref_dir.mkdir(exist_ok=True)

    orphan_name = orphan_dir.name
    timestamp = datetime.now(timezone.utc).isoformat()

    # Copy SKILL.md content into a reference file
    orphan_skill_md = orphan_dir / "SKILL.md"
    ref_file = ref_dir / f"{orphan_name}.md"

    if orphan_skill_md.exists():
        content = orphan_skill_md.read_text(encoding="utf-8", errors="ignore")
        # Strip frontmatter for the reference doc
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                content = parts[2].strip()
        ref_file.write_text(
            f"# {orphan_name}\n\n_Absorbed from standalone skill on {timestamp}_\n\n{content}\n",
            encoding="utf-8",
        )

    # Copy any scripts/
    orphan_scripts = orphan_dir / "scripts"
    if orphan_scripts.exists():
        parent_scripts = parent_dir / "scripts"
        parent_scripts.mkdir(exist_ok=True)
        for script in orphan_scripts.iterdir():
            if script.is_file():
                dest = parent_scripts / f"{orphan_name}_{script.name}"
                shutil.copy2(script, dest)

    # Copy any references/
    orphan_refs = orphan_dir / "references"
    if orphan_refs.exists():
        for ref in orphan_refs.iterdir():
            if ref.is_file():
                dest = ref_dir / f"{orphan_name}_{ref.name}"
                shutil.copy2(ref, dest)

    # Remove orphan directory
    shutil.rmtree(orphan_dir)

    return {
        "action": "consolidated",
        "orphan": orphan_name,
        "parent": parent_name,
        "candidates": candidates,
        "timestamp": timestamp,
        "ref_file": str(ref_file),
    }


def run_audit(dry_run: bool = False) -> list[dict]:
    """Run the full audit. Returns list of decisions."""
    decisions = []

    if not SKILLS_DIR.exists():
        print(f"Skills directory not found: {SKILLS_DIR}")
        return decisions

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        name = skill_dir.name

        # Skip known systems and non-skill directories
        if name in KNOWN_SYSTEMS:
            continue
        if name.startswith("."):
            continue
        if not (skill_dir / "SKILL.md").exists():
            continue

        purpose = get_skill_purpose(skill_dir)
        candidates = check_overlap(name, purpose)

        if candidates:
            parent = candidates[0]  # Best match
            if dry_run:
                decisions.append({
                    "action": "would_consolidate",
                    "orphan": name,
                    "parent": parent,
                    "candidates": candidates,
                    "purpose_snippet": purpose[:200],
                })
                print(f"[DRY RUN] {name} → {parent}")
            else:
                decision = consolidate_orphan(skill_dir, parent, candidates)
                decisions.append(decision)
                print(f"Consolidated: {name} → {parent}")
        else:
            print(f"OK: {name} (no overlap detected)")

    return decisions


def main():
    dry_run = "--dry-run" in sys.argv
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    print(f"Forge Skill Auditor — {'DRY RUN' if dry_run else 'LIVE'}")
    print(f"Skills dir: {SKILLS_DIR}")
    print(f"Known systems excluded: {len(KNOWN_SYSTEMS)}")
    print("---")

    FORGE_DATA_DIR.mkdir(parents=True, exist_ok=True)

    decisions = run_audit(dry_run=dry_run)

    # Log decisions
    with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as f:
        for d in decisions:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")

    if not dry_run:
        with open(DECISIONS_FILE, "a", encoding="utf-8") as f:
            for d in decisions:
                record = {
                    "timestamp": d.get("timestamp", datetime.now(timezone.utc).isoformat()),
                    "type": "audit_consolidation",
                    "payload": d,
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # Summary
    orphans = [d for d in decisions if d.get("action") in ("consolidated", "would_consolidate")]
    print(f"\n--- Summary ---")
    print(f"Skills scanned: {len(decisions)}")
    print(f"Orphans found: {len(orphans)}")
    if orphans:
        for o in orphans:
            print(f"  {o['orphan']} → {o['parent']}")

    sys.exit(1 if orphans else 0)


if __name__ == "__main__":
    main()
