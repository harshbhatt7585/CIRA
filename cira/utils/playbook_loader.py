"""Load and parse incident playbooks from Markdown files."""

import json
import re
from pathlib import Path

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
_CATEGORIES_FILE = _DATA_DIR / "categories.json"
_PLACEHOLDER_MARKER = "_Content pending — to be added by operator._"


def _load_categories_data() -> dict:
    with open(_CATEGORIES_FILE, encoding="utf-8") as f:
        return json.load(f)


def _find_subcategory(subcategory_id: str) -> dict | None:
    data = _load_categories_data()
    for sub in data["subcategories"]:
        if sub["id"] == subcategory_id:
            return sub
    return None


def _parse_markdown_sections(content: str) -> dict[str, str]:
    """Parse markdown into sections keyed by ## header text."""
    sections: dict[str, str] = {}
    current_header: str | None = None
    current_lines: list[str] = []

    for line in content.splitlines():
        if line.startswith("## "):
            if current_header is not None:
                sections[current_header] = "\n".join(current_lines).strip()
            current_header = line[3:].strip()
            current_lines = []
        elif current_header is not None:
            current_lines.append(line)

    if current_header is not None:
        sections[current_header] = "\n".join(current_lines).strip()

    return sections


def _is_placeholder_only(sections: dict[str, str]) -> bool:
    if not sections:
        return True
    return all(_PLACEHOLDER_MARKER in body for body in sections.values())


def load_playbook(subcategory_id: str) -> dict:
    """
    Load playbook for a subcategory.

    Returns dict keyed by section header, or a not-available structure
    if the file is missing or contains only placeholder content.
    """
    sub = _find_subcategory(subcategory_id)
    if sub is None:
        return {
            "available": False,
            "subcategory_id": subcategory_id,
            "message": f"Unknown subcategory: {subcategory_id}",
            "sections": {},
        }

    playbook_path = Path(__file__).resolve().parent.parent / sub["playbook_path"]
    if not playbook_path.exists():
        return {
            "available": False,
            "subcategory_id": subcategory_id,
            "subcategory_name": sub["name"],
            "message": "Playbook not yet available for this incident type.",
            "sections": {},
        }

    content = playbook_path.read_text(encoding="utf-8")
    sections = _parse_markdown_sections(content)

    if _is_placeholder_only(sections):
        return {
            "available": False,
            "subcategory_id": subcategory_id,
            "subcategory_name": sub["name"],
            "message": "Playbook content is pending — operator has not yet added guidance.",
            "sections": sections,
        }

    return {
        "available": True,
        "subcategory_id": subcategory_id,
        "subcategory_name": sub["name"],
        "sections": sections,
    }
