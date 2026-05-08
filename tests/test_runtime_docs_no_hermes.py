from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCANNED_ROOTS = [
    ROOT / "SKILL.md",
    ROOT / "references",
    ROOT / "assets" / "templates",
]
FORBIDDEN = ["Hermes", "soul.md", "SOUL.md", "USER.md"]


def iter_runtime_files():
    for root in SCANNED_ROOTS:
        if root.is_file():
            yield root
            continue
        for path in root.rglob("*"):
            if path.suffix.lower() in {".md", ".json", ".html"} and path.is_file():
                yield path


def test_runtime_references_do_not_depend_on_hermes_persona():
    offenders = []
    for path in iter_runtime_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for token in FORBIDDEN:
            if token in text:
                offenders.append(f"{path.relative_to(ROOT)} contains {token}")

    assert offenders == []
