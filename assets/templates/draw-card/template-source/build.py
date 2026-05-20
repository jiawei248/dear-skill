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
CANONICAL = ROOT / "template-source" / "retro-gacha-card.html"
CONFIG_MARKER = "</head>"
ASSET_PREFIXES = ("card_materials/", "generated_stickers/", "stickers/", "轮播图/", "reference/")
SCRIPT_ASSETS = ("carousel-photos-data.js",)
WORKDIR_ASSET_PREFIX = "draw-card-work/"


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
        for key in ("items", "selected", "resolved", "photos", "stickers", "lines"):
            if isinstance(value.get(key), list):
                return value[key]
    return []


def normalize_source_list(value: Any) -> list[str]:
    result: list[str] = []
    for item in as_list(value):
        if isinstance(item, str):
            result.append(item)
        elif isinstance(item, dict):
            src = item.get("src") or item.get("path") or item.get("resolved_path")
            if src:
                result.append(str(src))
    return result


def normalize_copy(slots: dict[str, Any]) -> dict[str, Any]:
    raw = slots.get("draw_card_copy") or slots.get("gift_copy") or slots.get("wish_copy") or {}
    if not isinstance(raw, dict):
        return {}
    key_map = {
        "panel_title": "panelTitle",
        "panel_subtitle": "panelSubtitle",
        "lyric_label": "lyricLabel",
        "lyric_placeholder": "lyricPlaceholder",
        "color_label": "colorLabel",
        "memo_label": "memoLabel",
        "memo_placeholder": "memoPlaceholder",
        "style_label": "styleLabel",
        "card_style_label": "cardStyleLabel",
        "cancel_label": "cancelLabel",
        "submit_label": "submitLabel",
        "insert_title": "insertTitle",
        "default_lyric": "defaultLyric",
        "knob_hint": "knobHint",
        "knob_hint_sub": "knobHintSub",
        "close_label": "closeLabel",
        "result_alt": "resultAlt",
        "save_label": "saveLabel",
        "download_prefix": "downloadPrefix",
        "fallback_card_title": "fallbackCardTitle",
        "fallback_photo_text": "fallbackPhotoText",
        "machine_button": "machineButton",
    }
    return {key_map.get(key, key): value for key, value in raw.items() if value is not None}


def normalize_wish_defaults(slots: dict[str, Any]) -> dict[str, Any]:
    raw = slots.get("wish_defaults") or slots.get("wishDefaults") or slots.get("default_wish") or {}
    if not isinstance(raw, dict):
        return {}
    key_map = {
        "theme_color": "themeColor",
        "eason_style": "easonStyle",
        "card_style": "cardStyle",
    }
    return {key_map.get(key, key): value for key, value in raw.items() if value is not None}


def split_lyrics(text: str) -> list[str]:
    lines = []
    for line in text.splitlines():
        cleaned = re.sub(r"^\s*\d+[）).]\s*", "", line).strip()
        if cleaned:
            lines.append(cleaned)
    return lines


def strip_workdir_prefix(workdir: Path, src_path: Path) -> Path | None:
    parts = src_path.parts
    if parts and parts[0] in {workdir.name, "draw-card-work"} and len(parts) > 1:
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


def normalize_lyrics(slots: dict[str, Any], workdir: Path) -> list[str]:
    raw = slots.get("lyrics") or slots.get("lyric_lines") or slots.get("background_lyrics")
    if isinstance(raw, dict):
        if isinstance(raw.get("lines"), list):
            return [str(item).strip() for item in raw["lines"] if str(item).strip()]
        if raw.get("text"):
            return split_lyrics(str(raw["text"]))
        src = raw.get("src") or raw.get("path")
        if src:
            path = resolve_asset_path(workdir, str(src))
            if path:
                return split_lyrics(path.read_text(encoding="utf-8"))
    if isinstance(raw, list):
        return [str(item).strip() for item in raw if str(item).strip()]
    if isinstance(raw, str):
        path = resolve_asset_path(workdir, raw)
        if path:
            return split_lyrics(path.read_text(encoding="utf-8"))
        return split_lyrics(raw)

    for candidate in (workdir / "lyrics.txt", ROOT / "base" / "lyrics.txt"):
        if candidate.is_file():
            return split_lyrics(candidate.read_text(encoding="utf-8"))
    return []


def default_sources(workdir: Path, rel_dir: str, pattern: str) -> list[str]:
    for base in (workdir, ROOT / "base"):
        directory = base / rel_dir
        if directory.is_dir():
            return [f"{rel_dir}/{path.name}" for path in sorted(directory.glob(pattern))]
    return []


def build_runtime_config(slots: dict[str, Any], workdir: Path) -> dict[str, Any]:
    config: dict[str, Any] = {"template": "draw-card"}

    copy = normalize_copy(slots)
    if copy:
        config["copy"] = copy
    defaults = normalize_wish_defaults(slots)
    if defaults:
        config["wishDefaults"] = defaults

    lyrics = normalize_lyrics(slots, workdir)
    if lyrics:
        config["lyrics"] = lyrics

    media_fields = {
        "carouselPhotos": ("carousel_photos", "carouselPhotos"),
        "wishPhotos": ("wish_photos", "wishPhotos"),
        "wishStickers": ("wish_stickers", "wishStickers"),
        "decorStickers": ("decor_stickers", "decorStickers"),
    }
    for output_key, input_keys in media_fields.items():
        for input_key in input_keys:
            normalized = normalize_source_list(slots.get(input_key))
            if normalized:
                config[output_key] = normalized
                break

    if "wishStickers" not in config:
        default_stickers = default_sources(workdir, "generated_stickers/all", "eason_sticker_*.png")
        if default_stickers:
            config["wishStickers"] = default_stickers

    passthrough_fields = {
        "decorStickerGroups": ("decor_sticker_groups", "decorStickerGroups"),
        "easonStyleOptions": ("eason_style_options", "easonStyleOptions"),
        "cardStyleOptions": ("card_style_options", "cardStyleOptions"),
        "wishStyleCandidates": ("wish_style_candidates", "wishStyleCandidates"),
        "cardTemplates": ("card_templates", "cardTemplates"),
    }
    for output_key, input_keys in passthrough_fields.items():
        for input_key in input_keys:
            value = slots.get(input_key)
            if value:
                config[output_key] = value
                break

    return inline_config_assets(config, workdir)


def encode_asset(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def looks_like_asset_path(value: str, workdir: Path) -> bool:
    return (
        value in SCRIPT_ASSETS
        or value.startswith(ASSET_PREFIXES)
        or value.startswith(f"{workdir.name}/")
        or value.startswith(WORKDIR_ASSET_PREFIX)
    )


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
        r"<script\s+src=(?P<quote>['\"])(?P<src>carousel-photos-data\.js)(?P=quote)\s*></script>"
    )

    def replace(match: re.Match[str]) -> str:
        src = match.group("src")
        path = resolve_asset_path(workdir, src)
        if not path:
            return match.group(0)
        return f"<script>\n{path.read_text(encoding='utf-8')}\n</script>"

    return pattern.sub(replace, html_text)


def inline_css_urls(html_text: str, workdir: Path) -> str:
    pattern = re.compile(
        r"url\((?P<quote>['\"]?)(?P<src>(?:card_materials|generated_stickers|stickers|轮播图|reference)/[^'\")]+)(?P=quote)\)"
    )

    def replace(match: re.Match[str]) -> str:
        src = match.group("src")
        path = resolve_asset_path(workdir, src)
        if not path:
            return match.group(0)
        return f'url("{encode_asset(path)}")'

    return pattern.sub(replace, html_text)


def inline_quoted_asset_paths(html_text: str, workdir: Path) -> str:
    pattern = re.compile(
        r"(?P<quote>['\"])(?P<src>(?:card_materials|generated_stickers|stickers|轮播图|reference)/[^'\"\n]+)(?P=quote)"
    )

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
    injection = f"<script>window.DRAW_CARD_GIFT_CONFIG = {payload};</script>"
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
