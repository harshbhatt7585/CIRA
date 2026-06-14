# Script to generate placeholder playbook markdown files from categories.json
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data" / "categories.json").read_text(encoding="utf-8"))

PLACEHOLDER = "_Content pending — to be added by operator._"

SECTIONS = [
    "Identification",
    "Immediate Actions (0-30 Minutes)",
    "Containment Actions",
    "Evidence Preservation",
    "Reporting Resources",
    "Recovery Actions",
    "Prevention Guidance",
    "Official Links",
    "Notes",
]

for sub in DATA["subcategories"]:
    content = f"# {sub['name']}\n\n"
    for section in SECTIONS:
        content += f"## {section}\n{PLACEHOLDER}\n\n"
    path = ROOT / sub["playbook_path"]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Created {path.relative_to(ROOT)}")

print(f"\nTotal playbooks: {len(DATA['subcategories'])}")
