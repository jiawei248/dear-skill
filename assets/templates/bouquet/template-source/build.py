#!/usr/bin/env python3
import argparse
import base64
import json
import mimetypes
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "template-source" / "mothers-day-blue-bouquet.html"
CONFIG_MARKER = "</head>"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slots", type=Path, required=True)
    parser.add_argument("--workdir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    return parser.parse_args()


def read_slots(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def list_from_slot(value):
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        for key in ("items", "selected", "resolved", "resolved_items"):
            if isinstance(value.get(key), list):
                return value[key]
    return []


def normalize_catalog_item(item: dict) -> dict:
    normalized = {
        "id": str(item.get("id") or item.get("catalog") or item.get("name") or "").strip(),
        "name": str(item.get("name") or item.get("label") or item.get("id") or "").strip(),
        "src": str(item.get("src") or item.get("path") or item.get("resolved_path") or "").strip(),
    }
    return {key: value for key, value in normalized.items() if value}


def normalize_gem_item(item: dict) -> dict:
    normalized = normalize_catalog_item(item)
    if "size" in item:
        normalized["size"] = item["size"]
    return normalized


def normalize_style(slots: dict) -> dict:
    value = slots.get("bouquet_style_direction") or {}
    if not isinstance(value, dict):
        return {}
    return {
        key: value[key]
        for key in ("color_palette", "emotional_tone", "occasion", "recipient_language")
        if value.get(key)
    }


def normalize_cards(slots: dict) -> dict:
    raw_cards = slots.get("card_notes") or []
    if isinstance(raw_cards, dict):
        raw_cards = raw_cards.get("items") or raw_cards.get("cards") or []
    cards = {}
    for index, card in enumerate(raw_cards):
        if not isinstance(card, dict):
            continue
        catalog = str(card.get("catalog") or card.get("flower") or card.get("flower_id") or "").strip()
        if not catalog:
            catalog = f"card-{index + 1}"
        normalized = {
            "label": card.get("label") or card.get("title") or catalog,
            "title": card.get("title") or card.get("label") or catalog,
            "text": card.get("text") or card.get("message") or "",
        }
        for key in ("x", "y", "w", "h", "r"):
            if key in card:
                normalized[key] = card[key]
        cards[catalog] = normalized
    return cards


def normalize_layout(slots: dict, cards: dict) -> dict:
    raw_layout = slots.get("layout_editing_contract") or slots.get("layout") or {}
    if not isinstance(raw_layout, dict):
        raw_layout = {}
    stems = raw_layout.get("stems") if isinstance(raw_layout.get("stems"), list) else []
    normalized_stems = []
    for index, stem in enumerate(stems):
        if not isinstance(stem, dict) or not stem.get("catalog"):
            continue
        normalized = {
            "uid": stem.get("uid") or f"stem-{index + 1}",
            "catalog": stem["catalog"],
            "x": stem.get("x", 360),
            "y": stem.get("y", 360),
            "w": stem.get("w", 220),
            "r": stem.get("r", 0),
            "z": stem.get("z", index + 1),
            "flip": stem.get("flip", 1),
        }
        if stem.get("catalog") in cards:
            normalized["note"] = cards[stem["catalog"]]
        normalized_stems.append(normalized)

    placed_gems = []
    raw_gems = slots.get("gem_picks") or {}
    if isinstance(raw_gems, dict) and isinstance(raw_gems.get("placed"), list):
        source_gems = raw_gems["placed"]
    else:
        source_gems = raw_layout.get("placedGems") if isinstance(raw_layout.get("placedGems"), list) else []
    for index, gem in enumerate(source_gems):
        if not isinstance(gem, dict) or not gem.get("gem"):
            continue
        placed_gems.append({
            "uid": gem.get("uid") or f"gem-{index + 1}",
            "gem": gem["gem"],
            "x": gem.get("x", 50),
            "y": gem.get("y", 50),
            "w": gem.get("w", 46),
            "r": gem.get("r", 0),
            "scale": gem.get("scale", 1),
            "z": gem.get("z", index + 1),
            "opacity": gem.get("opacity", .96),
        })

    layout = {}
    if normalized_stems:
        layout["stems"] = normalized_stems
        layout["nextStemId"] = len(normalized_stems) + 1
    if placed_gems:
        layout["placedGems"] = placed_gems
        layout["nextGemId"] = len(placed_gems) + 1
    if "nameOrbits" in raw_layout and isinstance(raw_layout["nameOrbits"], list):
        layout["nameOrbits"] = raw_layout["nameOrbits"]
    return layout


def normalize_gift_copy(slots: dict, cards: dict) -> dict:
    raw = slots.get("gift_copy") or slots.get("giftCopy") or {}
    if not isinstance(raw, dict):
        raw = {}
    copy = {
        key: raw[key]
        for key in ("recipient", "message")
        if raw.get(key)
    }
    if "message" not in copy and cards:
        first_card = next(iter(cards.values()))
        if first_card.get("text"):
            copy["message"] = first_card["text"]
    return copy


def encode_asset(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def resolve_asset_path(workdir: Path, src: str, asset_subdir: str) -> Path | None:
    if not src or src.startswith("data:"):
        return None
    candidates = []
    src_path = Path(src)
    if src_path.is_absolute():
        candidates.append(src_path)
    else:
        candidates.extend([
            workdir / asset_subdir / src,
            workdir / src,
            ROOT / "base" / asset_subdir / src,
            ROOT / "base" / src,
        ])
    return next((path for path in candidates if path.is_file()), None)


def inline_catalog_assets(items: list[dict], workdir: Path, asset_subdir: str) -> list[dict]:
    inlined = []
    for item in items:
        next_item = dict(item)
        path = resolve_asset_path(workdir, next_item.get("src", ""), asset_subdir)
        if path:
            next_item["src"] = encode_asset(path)
        inlined.append(next_item)
    return inlined


def build_runtime_config(slots: dict, workdir: Path) -> dict:
    cards = normalize_cards(slots)
    catalog = [
        item
        for item in (normalize_catalog_item(item) for item in list_from_slot(slots.get("flower_picks")))
        if item.get("id") and item.get("src")
    ]
    gem_catalog = [
        item
        for item in (normalize_gem_item(item) for item in list_from_slot(slots.get("gem_picks")))
        if item.get("id") and item.get("src")
    ]
    config = {
        "template": "bouquet",
        "style": normalize_style(slots),
        "catalog": inline_catalog_assets(catalog, workdir, "transparent-png"),
        "gemCatalog": inline_catalog_assets(gem_catalog, workdir, "gems"),
        "cards": cards,
        "layout": normalize_layout(slots, cards),
        "giftCopy": normalize_gift_copy(slots, cards),
    }
    return {key: value for key, value in config.items() if value not in ({}, [])}


def write_card_text(workdir: Path, cards: dict) -> None:
    cards_dir = workdir / "cards"
    cards_dir.mkdir(parents=True, exist_ok=True)
    (cards_dir / "card_text.json").write_text(json.dumps(cards, ensure_ascii=False, indent=2), encoding="utf-8")


def resolve_relative_asset(workdir: Path, src: str) -> Path | None:
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


def inline_css_urls(html_text: str, workdir: Path) -> str:
    def replace(match: re.Match) -> str:
        quote = match.group("quote") or ""
        src = match.group("src")
        path = resolve_relative_asset(workdir, src)
        if not path:
            if src.startswith("fonts/"):
                return 'local("__dear_missing_bouquet_font__")'
            return match.group(0)
        return f"url({quote}{encode_asset(path)}{quote})"

    return re.sub(r"url\((?P<quote>['\"]?)(?P<src>[^)'\"]+)(?P=quote)\)", replace, html_text)


def inject_config(html_text: str, config: dict) -> str:
    payload = json.dumps(config, ensure_ascii=False, separators=(",", ":"))
    injection = f"<script>window.BOUQUET_GIFT_CONFIG = {payload};</script>"
    if CONFIG_MARKER in html_text:
        return html_text.replace(CONFIG_MARKER, f"  {injection}\n{CONFIG_MARKER}", 1)
    return injection + "\n" + html_text


def main() -> int:
    args = parse_args()
    slots = read_slots(args.slots)
    config = build_runtime_config(slots, args.workdir)
    write_card_text(args.workdir, config.get("cards", {}))
    html_text = inline_css_urls(CANONICAL.read_text(encoding="utf-8"), args.workdir)
    html_text = inject_config(html_text, config)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html_text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
