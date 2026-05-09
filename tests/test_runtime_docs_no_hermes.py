from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCANNED_ROOTS = [
    ROOT / "SKILL.md",
    ROOT / "references",
    ROOT / "assets" / "templates",
]
FORBIDDEN = ["Hermes", "soul.md", "SOUL.md", "USER.md"]
DEFAULT_FLOW_FORBIDDEN = [
    "cron",
    "daily-run",
    "cron-driven",
    "cron-triggered",
    "MEMORY.md",
    "ordinary daily gifts",
    "daily gift",
]


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


def test_default_runtime_docs_do_not_assume_daemon_or_cron_context():
    scanned = [
        ROOT / "references" / "creative-concept.md",
        ROOT / "references" / "delivery-rules.md",
        ROOT / "references" / "image-integration.md",
        ROOT / "references" / "stage3-visual-strategy.md",
        ROOT / "references" / "stage4-visualization.md",
    ]
    offenders = []
    for path in scanned:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for token in DEFAULT_FLOW_FORBIDDEN:
            if token in text:
                offenders.append(f"{path.relative_to(ROOT)} contains {token}")

    assert offenders == []


def test_character_profiles_are_optional_not_default_context():
    stage3 = (ROOT / "references" / "stage3-visual-strategy.md").read_text(encoding="utf-8")
    stage4 = (ROOT / "references" / "stage4-visualization.md").read_text(encoding="utf-8")

    assert "Do not read or apply stored character/persona context by default" in stage3
    assert "Only read character profiles when the recipient brief or user request explicitly makes a recurring character relevant" in stage4
