#!/usr/bin/env python3
from pathlib import Path

HTML = Path("/Users/liujiawei/Desktop/night-four-assets/night-four-the-turn.html")
html = HTML.read_text(encoding="utf-8")

replacements = {
    "const targetOpacity = isActive ? 0.85 * fadeIn * fadeOut : 0.12 * fadeIn * fadeOut;":
        "const targetOpacity = isActive ? 0.85 * fadeIn * fadeOut : 0;",
    "const target = isActive ? 1.0 : 0.45;":
        "const target = isActive ? 1.0 : 0;",
    "const target = isActive ? 0.96 : 0.35;":
        "const target = isActive ? 0.96 : 0;",
    "const targetOpacity = isActive ? 0.95 : 0.30;":
        "const targetOpacity = isActive ? 0.95 : 0;",
}

for old, new in replacements.items():
    if old not in html:
        raise SystemExit(f"Missing expected text: {old}")
    html = html.replace(old, new)

HTML.write_text(html, encoding="utf-8")
print("Inactive room PNGs and falling words are now hidden")
