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
CANONICAL = ROOT / "template-source" / "tincase-box-loop.html"
CONFIG_MARKER = "</head>"
ASSET_PREFIXES = ("boxes/", "stickers/", "generated/", "figures/", "fonts/")


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
        for key in ("items", "selected", "resolved", "boxes", "labels"):
            if isinstance(value.get(key), list):
                return value[key]
    return []


def normalize_chrome(slots: dict[str, Any]) -> dict[str, Any]:
    raw = slots.get("gift_copy") or slots.get("chrome") or {}
    if not isinstance(raw, dict):
        raw = {}
    labels = raw.get("labels")
    if not isinstance(labels, list):
        recipient = raw.get("recipient") or raw.get("for") or "For you"
        occasion = raw.get("occasion") or raw.get("title") or "Happy"
        labels = [
            [str(occasion), "label-happy"],
            [str(recipient), "label-for"],
            [raw.get("collection_label") or "Curated", "label-pick"],
            [raw.get("object_label") or "tincase", "label-tincase"],
            [raw.get("memory_label") or "Our memories", "label-memory"],
        ]
    chrome = {"labels": labels}
    if raw.get("ticker_text"):
        chrome["tickerText"] = raw["ticker_text"]
    return chrome


def normalize_box_assets(slots: dict[str, Any]) -> list[dict[str, Any]]:
    assets = as_list(slots.get("box_assets"))
    normalized = []
    for item in assets:
        if not isinstance(item, dict):
            continue
        src = item.get("src") or item.get("path")
        if not src:
            continue
        normalized.append(
            {
                "src": str(src),
                "boost": item.get("boost", 1.08),
                **({"collage": item["collage"]} if "collage" in item else {}),
            }
        )
    return normalized


def normalize_gem_assets(slots: dict[str, Any]) -> list[str]:
    gems = as_list(slots.get("ambient_gems"))
    result = []
    for item in gems:
        if isinstance(item, str):
            result.append(item)
        elif isinstance(item, dict) and (item.get("src") or item.get("path")):
            result.append(str(item.get("src") or item.get("path")))
    return result


def normalize_collages(slots: dict[str, Any]) -> dict[str, Any]:
    raw = slots.get("box_collages") or slots.get("collages") or {}
    if isinstance(raw, list):
        mapped: dict[str, Any] = {}
        for item in raw:
            if isinstance(item, dict) and item.get("id"):
                mapped[str(item["id"])] = {key: value for key, value in item.items() if key != "id"}
        return mapped
    return raw if isinstance(raw, dict) else {}


def build_runtime_config(slots: dict[str, Any], workdir: Path) -> dict[str, Any]:
    config: dict[str, Any] = {
        "template": "empty-boxes",
        "chrome": normalize_chrome(slots),
    }
    box_assets = normalize_box_assets(slots)
    if box_assets:
        config["boxAssets"] = box_assets
    gem_assets = normalize_gem_assets(slots)
    if gem_assets:
        config["gemAssets"] = gem_assets
    collages = normalize_collages(slots)
    if collages:
        config["collages"] = collages
    return inline_config_assets(config, workdir)


def encode_asset(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def looks_like_asset_path(value: str) -> bool:
    return value.startswith(ASSET_PREFIXES)


def resolve_asset_path(workdir: Path, src: str) -> Path | None:
    if not src or src.startswith(("data:", "http:", "https:", "file:", "blob:")):
        return None
    src_path = Path(src)
    if src_path.is_absolute():
        return src_path if src_path.is_file() else None
    candidates = [
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
    if isinstance(value, str) and looks_like_asset_path(value):
        path = resolve_asset_path(workdir, value)
        if path:
            return encode_asset(path)
    return value


def inline_quoted_asset_paths(html_text: str, workdir: Path) -> str:
    pattern = re.compile(r"(?P<quote>['\"])(?P<src>(?:boxes|stickers|generated|figures|fonts)/[^'\"]+)(?P=quote)")

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
    injection = f"<script>window.EMPTY_BOXES_GIFT_CONFIG = {payload};</script>"
    if CONFIG_MARKER in html_text:
        return html_text.replace(CONFIG_MARKER, f"  {injection}\n{CONFIG_MARKER}", 1)
    return injection + "\n" + html_text


def main() -> int:
    args = parse_args()
    slots = read_slots(args.slots)
    args.workdir.mkdir(parents=True, exist_ok=True)
    config = build_runtime_config(slots, args.workdir)
    (args.workdir / "runtime_config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    html_text = inline_quoted_asset_paths(CANONICAL.read_text(encoding="utf-8"), args.workdir)
    html_text = inject_config(html_text, config)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html_text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
