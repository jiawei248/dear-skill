#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "template-source" / "520-folder-gift.html"
CONFIG_MARKER = "</head>"
ASSET_PREFIXES = ("assets/", "stickers/", "fonts/")
WORKDIR_ASSET_PREFIX = "folder-work/"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slots", type=Path, required=True)
    parser.add_argument("--workdir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    return parser.parse_args()


def read_slots(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        for key in ("items", "selected", "resolved", "folders", "chapters", "replacements", "photos"):
            if isinstance(value.get(key), list):
                return value[key]
    return []


def normalize_archive(raw: dict[str, Any]) -> dict[str, Any]:
    archive_raw = raw.get("archive") if isinstance(raw.get("archive"), dict) else raw
    archive: dict[str, Any] = {}
    title_lines = archive_raw.get("titleLines") or archive_raw.get("title_lines") or archive_raw.get("archive_title_lines")
    if isinstance(title_lines, list):
        archive["titleLines"] = [str(item) for item in title_lines[:3]]
    elif archive_raw.get("recipient") or archive_raw.get("occasion"):
        archive["titleLines"] = [
            str(archive_raw.get("occasion") or "FILED UNDER: US"),
            str(archive_raw.get("date") or archive_raw.get("folder_date") or ""),
            str(archive_raw.get("location") or archive_raw.get("place") or ""),
        ]
    note = archive_raw.get("note") or archive_raw.get("archive_note")
    if note:
        archive["note"] = str(note)
    return archive


def normalize_tabs(raw: dict[str, Any], slots: dict[str, Any]) -> list[dict[str, str]]:
    tabs = raw.get("tabs") or slots.get("folder_tabs")
    plans = as_list(slots.get("folder_story_plan"))
    if not tabs and plans:
        tabs = [
            {
                "row": item.get("row") or f"row{index + 1}",
                "title": item.get("tab_title") or item.get("title") or item.get("theme"),
                "subtitle": item.get("tab_subtitle") or item.get("subtitle") or item.get("memory_anchor"),
            }
            for index, item in enumerate(plans)
            if isinstance(item, dict)
        ]
    if isinstance(tabs, dict):
        iterable = [{"row": key, **value} for key, value in tabs.items() if isinstance(value, dict)]
    else:
        iterable = tabs if isinstance(tabs, list) else []
    normalized: list[dict[str, str]] = []
    for index, item in enumerate(iterable):
        if not isinstance(item, dict):
            continue
        tab: dict[str, str] = {"row": str(item.get("row") or f"row{index + 1}")}
        if item.get("title") is not None:
            tab["title"] = str(item["title"])
        if item.get("subtitle") is not None:
            tab["subtitle"] = str(item["subtitle"])
        normalized.append(tab)
    return normalized


def normalize_opened_folder(raw: dict[str, Any]) -> dict[str, Any]:
    opened = raw.get("openedFolder") or raw.get("opened_folder") or raw.get("open") or {}
    if not isinstance(opened, dict):
        return {}
    key_map = {
        "story_heading": "storyHeading",
        "story_body": "storyBody",
        "story_body_html": "storyBodyHtml",
        "cover_title": "coverTitle",
        "cover_subtitle": "coverSubtitle",
        "main_caption": "mainCaption",
        "grid_caption": "gridCaption",
    }
    normalized: dict[str, Any] = {}
    for key, value in opened.items():
        normalized[key_map.get(key, key)] = value
    return normalized


def normalize_text_replacements(slots: dict[str, Any], raw: dict[str, Any]) -> list[dict[str, Any]]:
    replacements = raw.get("textReplacements") or raw.get("text_replacements") or slots.get("text_replacements")
    if isinstance(replacements, dict):
        return [{"selector": key, "value": value} for key, value in replacements.items()]
    if isinstance(replacements, list):
        return [item for item in replacements if isinstance(item, dict)]
    return []


def normalize_image_replacements(slots: dict[str, Any]) -> list[dict[str, Any]]:
    raw = slots.get("folder_images") or slots.get("image_replacements") or slots.get("photos") or {}
    if isinstance(raw, dict) and isinstance(raw.get("replacements"), list):
        raw = raw["replacements"]
    if isinstance(raw, dict):
        normalized = []
        for selector, value in raw.items():
            if selector in {"replacements", "items", "selected", "resolved", "photos"}:
                continue
            if isinstance(value, str):
                normalized.append({"selector": selector, "src": value})
            elif isinstance(value, dict):
                normalized.append({"selector": selector, **value})
        return normalized
    if isinstance(raw, list):
        return [item for item in raw if isinstance(item, dict)]
    return []


def normalize_layout_config(slots: dict[str, Any]) -> dict[str, Any]:
    raw = slots.get("folder_layout") or slots.get("layout_overrides") or slots.get("folder_runtime_overrides") or {}
    if not isinstance(raw, dict):
        return {}
    key_map = {
        "thumbnail": "thumbnailLayoutConfig",
        "thumbnail_layout": "thumbnailLayoutConfig",
        "open": "openLayoutConfig",
        "open_layout": "openLayoutConfig",
        "closed": "closedPreviewConfig",
        "closed_preview": "closedPreviewConfig",
    }
    normalized: dict[str, Any] = {}
    for key, value in raw.items():
        normalized[key_map.get(key, key)] = value
    return normalized


def build_runtime_config(slots: dict[str, Any], workdir: Path) -> dict[str, Any]:
    raw_copy = slots.get("folder_copy") or slots.get("gift_copy") or slots.get("archive_copy") or {}
    if not isinstance(raw_copy, dict):
        raw_copy = {}

    config: dict[str, Any] = {"template": "folder"}
    archive = normalize_archive(raw_copy)
    if archive:
        config["archive"] = archive
    tabs = normalize_tabs(raw_copy, slots)
    if tabs:
        config["tabs"] = tabs
    opened = normalize_opened_folder(raw_copy)
    if opened:
        config["openedFolder"] = opened
    image_replacements = normalize_image_replacements(slots)
    if image_replacements:
        config["imageReplacements"] = image_replacements
    text_replacements = normalize_text_replacements(slots, raw_copy)
    if text_replacements:
        config["textReplacements"] = text_replacements
    config.update(normalize_layout_config(slots))
    return inline_config_assets(config, workdir)


def encode_asset(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def looks_like_asset_path(value: str, workdir: Path) -> bool:
    return (
        value.startswith(ASSET_PREFIXES)
        or value.startswith(f"{workdir.name}/")
        or value.startswith(WORKDIR_ASSET_PREFIX)
    )


def strip_workdir_prefix(workdir: Path, src_path: Path) -> Path | None:
    parts = src_path.parts
    if parts and parts[0] in {workdir.name, "folder-work"} and len(parts) > 1:
        return workdir.joinpath(*parts[1:])
    return None


def resolve_asset_path(workdir: Path, src: str) -> Path | None:
    if not src or src.startswith(("data:", "http:", "https:", "file:", "blob:")):
        return None
    src_path = Path(src)
    if src_path.is_absolute():
        return src_path if src_path.is_file() else None
    workdir_relative_path = strip_workdir_prefix(workdir, src_path)
    candidates = [
        *([workdir_relative_path] if workdir_relative_path else []),
        workdir / src,
        ROOT / "base" / src,
        ROOT / "template-source" / src,
    ]
    return next((path for path in candidates if path.is_file()), None)


def inline_config_assets(value: Any, workdir: Path) -> Any:
    if isinstance(value, dict):
        return {key: inline_config_assets(item, workdir) for key, item in value.items()}
    if isinstance(value, list):
        return [inline_config_assets(item, workdir) for item in value]
    if isinstance(value, str) and looks_like_asset_path(value, workdir):
        path = resolve_asset_path(workdir, value)
        if path:
            return encode_asset(path)
    return value


def inline_script_tags(html_text: str, workdir: Path) -> str:
    pattern = re.compile(
        r"<script\s+src=(?P<quote>['\"])(?P<src>(?:assets|stickers|fonts)/[^'\"]+)(?P=quote)\s*></script>"
    )

    def replace(match: re.Match[str]) -> str:
        src = match.group("src")
        path = resolve_asset_path(workdir, src)
        if not path or path.suffix.lower() != ".js":
            return match.group(0)
        return f"<script>\n{path.read_text(encoding='utf-8')}\n</script>"

    return pattern.sub(replace, html_text)


def inline_css_urls(html_text: str, workdir: Path) -> str:
    pattern = re.compile(r"url\((?P<quote>['\"]?)(?P<src>(?:assets|stickers|fonts)/[^'\")]+)(?P=quote)\)")

    def replace(match: re.Match[str]) -> str:
        src = match.group("src")
        path = resolve_asset_path(workdir, src)
        if not path:
            return match.group(0)
        return f'url("{encode_asset(path)}")'

    return pattern.sub(replace, html_text)


def inline_quoted_asset_paths(html_text: str, workdir: Path) -> str:
    pattern = re.compile(r"(?P<quote>['\"])(?P<src>(?:assets|stickers|fonts)/[^'\"]+)(?P=quote)")

    def replace(match: re.Match[str]) -> str:
        quote = match.group("quote")
        src = match.group("src")
        path = resolve_asset_path(workdir, src)
        if not path:
            return match.group(0)
        return f"{quote}{encode_asset(path)}{quote}"

    return pattern.sub(replace, html_text)


def inject_config(html_text: str, config: dict[str, Any]) -> str:
    payload = json.dumps(config, ensure_ascii=False, separators=(",", ":"))
    injection = f"<script>window.FOLDER_GIFT_CONFIG = {payload};</script>"
    if CONFIG_MARKER in html_text:
        return html_text.replace(CONFIG_MARKER, f"  {injection}\n{CONFIG_MARKER}", 1)
    return injection + "\n" + html_text


def main() -> int:
    args = parse_args()
    slots = read_slots(args.slots)
    args.workdir.mkdir(parents=True, exist_ok=True)
    config = build_runtime_config(slots, args.workdir)
    (args.workdir / "runtime_config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")

    html_text = CANONICAL.read_text(encoding="utf-8")
    html_text = inline_script_tags(html_text, args.workdir)
    html_text = inline_css_urls(html_text, args.workdir)
    html_text = inline_quoted_asset_paths(html_text, args.workdir)
    html_text = inject_config(html_text, config)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html_text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
