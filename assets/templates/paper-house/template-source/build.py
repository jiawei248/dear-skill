#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import re
import sys
from pathlib import Path
from typing import Any


TEMPLATE_DIR = Path(__file__).resolve().parent
CANONICAL_HTML = TEMPLATE_DIR / "night-four-the-turn.html"
SCENE_IDS = ("kitchen", "rooftop", "karaoke", "couch")
ROOM_WALL_IMAGE_KEYS = {
    "wall_left": "{scene}_left",
    "left": "{scene}_left",
    "wall_right": "{scene}_right",
    "right": "{scene}_right",
    "floor": "{scene}_floor",
}
WALL_STAGING_PATHS = {
    "wall_left": "walls/{scene}_left.jpg",
    "left": "walls/{scene}_left.jpg",
    "wall_right": "walls/{scene}_right.jpg",
    "right": "walls/{scene}_right.jpg",
    "floor": "floors/{scene}_floor.jpg",
}
DEFAULT_STORY_IDS = {
    "kitchen": "kitchen_4",
    "rooftop": "rooftop_1",
    "karaoke": "karaoke_3",
    "couch": "couch_6",
}
DEFAULT_STORY_CARD_IMAGE_KEYS = {
    "kitchen": "kitchen_4",
    "rooftop": "rooftop_1",
    "karaoke": "karaoke_3",
    "couch": "couch_6",
}


class BuildError(Exception):
    pass


def js(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=6)


def data_uri(path: Path) -> str:
    if not path.exists():
        raise BuildError(f"asset file does not exist: {path}")
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def resolve_asset(value: Any, workdir: Path, field_name: str) -> str:
    if isinstance(value, dict):
        value = value.get("path") or value.get("resolved_path") or value.get("src")
    if not isinstance(value, str) or not value:
        raise BuildError(f"{field_name} must be a non-empty asset path or data URI")
    if value.startswith(("data:", "http://", "https://")):
        return value
    return data_uri((workdir / value).resolve())


def find_matching(text: str, open_index: int, open_char: str, close_char: str) -> int:
    depth = 0
    quote = ""
    escaped = False
    for i in range(open_index, len(text)):
        ch = text[i]
        if quote:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                quote = ""
            continue
        if ch in "'\"`":
            quote = ch
        elif ch == open_char:
            depth += 1
        elif ch == close_char:
            depth -= 1
            if depth == 0:
                return i
    raise BuildError(f"could not find matching {close_char} for {open_char} at offset {open_index}")


def find_rooms_array(html: str) -> tuple[int, int]:
    marker = "const ROOMS = ["
    marker_index = html.find(marker)
    if marker_index == -1:
        raise BuildError("could not find const ROOMS array in template HTML")
    array_start = html.find("[", marker_index)
    array_end = find_matching(html, array_start, "[", "]")
    return array_start, array_end


def find_room_object(html: str, room_id: str) -> tuple[int, int]:
    array_start, array_end = find_rooms_array(html)
    i = array_start + 1
    while i < array_end:
        obj_start = html.find("{", i, array_end)
        if obj_start == -1:
            break
        obj_end = find_matching(html, obj_start, "{", "}")
        obj = html[obj_start : obj_end + 1]
        if re.search(rf"\bid\s*:\s*['\"]{re.escape(room_id)}['\"]", obj):
            return obj_start, obj_end + 1
        i = obj_end + 1
    raise BuildError(f"room '{room_id}' was not found in const ROOMS")


def find_sticker_interactions_object(html: str) -> tuple[int, int]:
    marker = "const STICKER_INTERACTIONS = {"
    marker_index = html.find(marker)
    if marker_index == -1:
        raise BuildError("could not find const STICKER_INTERACTIONS object in template HTML")
    obj_start = html.find("{", marker_index)
    obj_end = find_matching(html, obj_start, "{", "}")
    return obj_start, obj_end + 1


def find_story_object(html: str, story_id: str) -> tuple[int, int]:
    interactions_start, interactions_end = find_sticker_interactions_object(html)
    pattern = re.compile(rf"(?m)^\s*{re.escape(story_id)}\s*:\s*\{{")
    match = pattern.search(html, interactions_start, interactions_end)
    if not match:
        raise BuildError(f"story hotspot '{story_id}' was not found in STICKER_INTERACTIONS")
    obj_start = html.find("{", match.start())
    obj_end = find_matching(html, obj_start, "{", "}")
    return obj_start, obj_end + 1


def read_identifier(text: str, index: int) -> tuple[str, int] | None:
    if index >= len(text):
        return None
    if text[index] in "'\"":
        quote = text[index]
        end = index + 1
        escaped = False
        while end < len(text):
            ch = text[end]
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                return text[index + 1 : end], end + 1
            end += 1
        raise BuildError("unterminated quoted property name")
    match = re.match(r"[A-Za-z_$][A-Za-z0-9_$]*", text[index:])
    if not match:
        return None
    return match.group(0), index + len(match.group(0))


def top_level_property_span(obj: str, property_name: str) -> tuple[int, int] | None:
    if not obj.startswith("{") or not obj.rstrip().endswith("}"):
        raise BuildError("expected a JavaScript object literal")
    i = 1
    while i < len(obj) - 1:
        while i < len(obj) - 1 and obj[i].isspace():
            i += 1
        prop = read_identifier(obj, i)
        if not prop:
            i += 1
            continue
        name, after_name = prop
        j = after_name
        while j < len(obj) - 1 and obj[j].isspace():
            j += 1
        if j >= len(obj) or obj[j] != ":":
            i = after_name
            continue
        value_start = j + 1
        depth = 1
        quote = ""
        escaped = False
        k = value_start
        while k < len(obj):
            ch = obj[k]
            if quote:
                if escaped:
                    escaped = False
                elif ch == "\\":
                    escaped = True
                elif ch == quote:
                    quote = ""
            else:
                if ch in "'\"`":
                    quote = ch
                elif ch in "[{(":
                    depth += 1
                elif ch in "]})":
                    depth -= 1
                    if depth == 0:
                        value_end = k
                        break
                elif ch == "," and depth == 1:
                    value_end = k
                    break
            k += 1
        else:
            raise BuildError(f"could not find end of property '{name}'")
        if name == property_name:
            return value_start, value_end
        i = value_end + 1
    return None


def replace_top_level_property(obj: str, property_name: str, rendered_value: str) -> str:
    span = top_level_property_span(obj, property_name)
    if span is None:
        raise BuildError(f"property '{property_name}' was not found")
    start, end = span
    prefix = " " if obj[start - 1] == " " else ""
    suffix = "" if rendered_value.startswith("\n") else " "
    return obj[:start] + prefix + rendered_value + suffix + obj[end:]


def replace_image_data(html: str, image_key: str, uri: str) -> str:
    pattern = re.compile(rf'("{re.escape(image_key)}"\s*:\s*")([^"]*)(")')
    html, count = pattern.subn(lambda match: match.group(1) + uri + match.group(3), html, count=1)
    if count != 1:
        raise BuildError(f"image key '{image_key}' was not found in template image data")
    return html


def apply_room_slots(html: str, rooms: dict[str, Any]) -> str:
    allowed = {"title", "eyebrow", "note", "palette", "lyricColor", "lyricShadow", "song", "lyrics", "fallWords"}
    for room_id, fields in rooms.items():
        if room_id not in SCENE_IDS:
            raise BuildError(f"unknown room id '{room_id}'")
        if not isinstance(fields, dict):
            raise BuildError(f"rooms.{room_id} must be an object")
        obj_start, obj_end = find_room_object(html, room_id)
        obj = html[obj_start:obj_end]
        for key, value in fields.items():
            if key not in allowed:
                raise BuildError(f"unsupported rooms.{room_id}.{key}; supported fields: {', '.join(sorted(allowed))}")
            obj = replace_top_level_property(obj, key, js(value))
        html = html[:obj_start] + obj + html[obj_end:]
    return html


def apply_image_slots(html: str, images: dict[str, Any], workdir: Path) -> str:
    for image_key, value in images.items():
        uri = resolve_asset(value, workdir, f"images.{image_key}")
        html = replace_image_data(html, image_key, uri)
    return html


def apply_story_slots(html: str, stories: dict[str, Any], workdir: Path) -> str:
    allowed = {"item", "title", "kicker", "image", "layout", "paper", "accent", "decals", "text"}
    for story_id, fields in stories.items():
        if not isinstance(fields, dict):
            raise BuildError(f"stories.{story_id} must be an object")
        obj_start, obj_end = find_story_object(html, story_id)
        obj = html[obj_start:obj_end]
        for key, value in fields.items():
            if key not in allowed:
                raise BuildError(f"unsupported stories.{story_id}.{key}; supported fields: {', '.join(sorted(allowed))}")
            if key == "image":
                value = resolve_asset(value, workdir, f"stories.{story_id}.image")
            obj = replace_top_level_property(obj, key, js(value))
        html = html[:obj_start] + obj + html[obj_end:]
    return html


def merge_mapping(target: dict[str, Any], key: str, value: Any) -> None:
    if key in target and isinstance(target[key], dict) and isinstance(value, dict):
        target[key].update(value)
    else:
        target[key] = value


def explicit_asset_value(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value)
    if isinstance(value, dict):
        return any(value.get(key) for key in ("path", "resolved_path", "src"))
    return value is not None


def default_wall_asset(scene_id: str, component: str) -> str:
    try:
        return WALL_STAGING_PATHS[component].format(scene=scene_id)
    except KeyError as exc:
        raise BuildError(f"unknown wall/floor component '{component}' for scene '{scene_id}'") from exc


def default_figure_asset(scene_id: str, index: int = 1) -> str:
    suffix = "" if index == 1 else f"_{index}"
    return f"figures/scene_{scene_id}{suffix}.png"


def default_decoration_asset(scene_id: str, index: int) -> str:
    return f"stickers/{scene_id}/{index}.png"


def default_story_card_asset(scene_id: str, story_id: str | None = None) -> str:
    default_items = {"kitchen": "fridge", "rooftop": "suitcase", "karaoke": "camera", "couch": "chess"}
    if scene_id in default_items and (story_id is None or story_id == DEFAULT_STORY_IDS.get(scene_id)):
        item = default_items[scene_id]
    elif story_id and "_" in story_id:
        item = story_id.split("_", 1)[1]
    else:
        item = default_items.get(scene_id)
    if not item:
        raise BuildError(f"cannot infer default story card asset for scene '{scene_id}'")
    return f"story_cards/generated/{scene_id}-{item}.png"


def normalize_scene_theme(slots: dict[str, Any], rooms: dict[str, Any]) -> None:
    scene_theme = slots.get("scene_theme")
    if scene_theme is None:
        return
    if not isinstance(scene_theme, dict):
        raise BuildError("scene_theme must be an object keyed by scene id")
    for scene_id, value in scene_theme.items():
        if not isinstance(value, dict):
            raise BuildError(f"scene_theme.{scene_id} must be an object")
        fields: dict[str, Any] = {}
        if "theme" in value:
            fields["title"] = value["theme"]
        for key in ("title", "eyebrow", "note", "palette", "lyricColor", "lyricShadow"):
            if key in value:
                fields[key] = value[key]
        merge_mapping(rooms, scene_id, fields)


def normalize_room_walls_and_floor(slots: dict[str, Any], images: dict[str, Any]) -> None:
    walls = slots.get("room_walls_and_floor")
    if walls is None:
        return
    if not isinstance(walls, dict):
        raise BuildError("room_walls_and_floor must be an object keyed by scene id")
    for scene_id, value in walls.items():
        if not isinstance(value, dict):
            raise BuildError(f"room_walls_and_floor.{scene_id} must be an object")
        for input_key, image_key_template in ROOM_WALL_IMAGE_KEYS.items():
            if input_key in value:
                image_value = value[input_key] if explicit_asset_value(value[input_key]) else default_wall_asset(scene_id, input_key)
                images[image_key_template.format(scene=scene_id)] = image_value
            elif input_key in ("wall_left", "wall_right", "floor"):
                images[image_key_template.format(scene=scene_id)] = default_wall_asset(scene_id, input_key)
        components = value.get("components")
        if components is not None:
            if not isinstance(components, dict):
                raise BuildError(f"room_walls_and_floor.{scene_id}.components must be an object")
            for input_key, image_key_template in ROOM_WALL_IMAGE_KEYS.items():
                if input_key in components:
                    image_value = components[input_key] if explicit_asset_value(components[input_key]) else default_wall_asset(scene_id, input_key)
                    images[image_key_template.format(scene=scene_id)] = image_value


def normalize_scene_figure_image(slots: dict[str, Any], images: dict[str, Any]) -> None:
    figures = slots.get("scene_figure_image")
    if figures is None:
        return
    if not isinstance(figures, dict):
        raise BuildError("scene_figure_image must be an object keyed by scene id")
    for scene_id, value in figures.items():
        if isinstance(value, list):
            if not value:
                continue
            images[f"scene_{scene_id}"] = value[0] if explicit_asset_value(value[0]) else default_figure_asset(scene_id)
            for index, extra in enumerate(value[1:], start=2):
                images[f"scene_{scene_id}_{index}"] = extra if explicit_asset_value(extra) else default_figure_asset(scene_id, index)
        elif isinstance(value, dict):
            if "images" in value:
                image_values = value["images"]
                if not isinstance(image_values, list) or not image_values:
                    raise BuildError(f"scene_figure_image.{scene_id}.images must be a non-empty list")
                images[f"scene_{scene_id}"] = image_values[0] if explicit_asset_value(image_values[0]) else default_figure_asset(scene_id)
                for index, extra in enumerate(image_values[1:], start=2):
                    images[f"scene_{scene_id}_{index}"] = extra if explicit_asset_value(extra) else default_figure_asset(scene_id, index)
            elif "path" in value or "resolved_path" in value or "src" in value:
                images[f"scene_{scene_id}"] = value
            elif not value:
                images[f"scene_{scene_id}"] = default_figure_asset(scene_id)
            else:
                for key, asset in value.items():
                    suffix = "" if str(key) in ("1", "primary", "main") else f"_{key}"
                    index = 1 if suffix == "" else int(key) if str(key).isdigit() else 1
                    images[f"scene_{scene_id}{suffix}"] = asset if explicit_asset_value(asset) else default_figure_asset(scene_id, index)
        else:
            images[f"scene_{scene_id}"] = value if explicit_asset_value(value) else default_figure_asset(scene_id)


def normalize_scene_decorations(slots: dict[str, Any], images: dict[str, Any]) -> None:
    decorations = slots.get("scene_decorations")
    if decorations is None:
        return
    if not isinstance(decorations, dict):
        raise BuildError("scene_decorations must be an object keyed by scene id")
    for scene_id, value in decorations.items():
        if isinstance(value, list):
            items = value
        elif isinstance(value, dict):
            items = value.get("items") or value.get("resolved_paths") or value.get("paths")
            if items is None:
                items = value
        else:
            raise BuildError(f"scene_decorations.{scene_id} must be a list or object")
        if isinstance(items, list):
            if len(items) > 6:
                raise BuildError(f"scene_decorations.{scene_id} has {len(items)} items; the current layout supports at most 6")
            for index, item in enumerate(items, start=1):
                images[f"{scene_id}_{index}"] = item if explicit_asset_value(item) else default_decoration_asset(scene_id, index)
        elif isinstance(items, dict):
            for key, item in items.items():
                image_key = str(key) if str(key).startswith(f"{scene_id}_") else f"{scene_id}_{key}"
                index = int(str(image_key).split("_")[-1]) if str(image_key).split("_")[-1].isdigit() else 1
                images[image_key] = item if explicit_asset_value(item) else default_decoration_asset(scene_id, index)
        else:
            raise BuildError(f"scene_decorations.{scene_id} must resolve to a list or object")


def story_id_for_scene(scene_id: str, value: Any = None) -> str:
    if isinstance(value, dict):
        explicit = value.get("hotspot_id") or value.get("id")
        if explicit:
            return str(explicit)
    try:
        return DEFAULT_STORY_IDS[scene_id]
    except KeyError as exc:
        raise BuildError(f"unknown scene id '{scene_id}'") from exc


def normalize_scene_hero_items(slots: dict[str, Any], stories: dict[str, Any]) -> None:
    hero_items = slots.get("scene_hero_items")
    if hero_items is None:
        return
    if not isinstance(hero_items, dict):
        raise BuildError("scene_hero_items must be an object keyed by scene id or hotspot id")
    for key, value in hero_items.items():
        if not isinstance(value, dict):
            raise BuildError(f"scene_hero_items.{key} must be an object")
        story_id = story_id_for_scene(key, value) if key in SCENE_IDS else key
        fields = {k: v for k, v in value.items() if k not in {"hotspot_id", "id"}}
        merge_mapping(stories, story_id, fields)


def normalize_story_cards(slots: dict[str, Any], stories: dict[str, Any]) -> None:
    story_cards = slots.get("story_cards")
    if story_cards is None:
        return
    if not isinstance(story_cards, dict):
        raise BuildError("story_cards must be an object keyed by scene id or hotspot id")
    for key, value in story_cards.items():
        story_id = story_id_for_scene(key) if key in SCENE_IDS else key
        if isinstance(value, dict) and not any(k in value for k in ("path", "resolved_path", "src")):
            fields = dict(value)
            if "image" not in fields:
                scene_id = key if key in SCENE_IDS else next((scene for scene, default_story_id in DEFAULT_STORY_IDS.items() if default_story_id == story_id), "")
                fields["image"] = default_story_card_asset(scene_id, story_id)
        else:
            fields = {"image": value if explicit_asset_value(value) else default_story_card_asset(key, story_id)}
        merge_mapping(stories, story_id, fields)


def normalize_per_scene_room_field(slots: dict[str, Any], slot_key: str, room_field: str, rooms: dict[str, Any]) -> None:
    values = slots.get(slot_key)
    if values is None:
        return
    if not isinstance(values, dict):
        raise BuildError(f"{slot_key} must be an object keyed by scene id")
    for scene_id, value in values.items():
        merge_mapping(rooms, scene_id, {room_field: value})


def normalize_native_slots(slots: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    rooms = dict(slots.get("rooms", {}))
    images = dict(slots.get("images", {}))
    stories = dict(slots.get("stories", {}))

    normalize_scene_theme(slots, rooms)
    normalize_room_walls_and_floor(slots, images)
    normalize_scene_figure_image(slots, images)
    normalize_scene_decorations(slots, images)
    normalize_scene_hero_items(slots, stories)
    normalize_story_cards(slots, stories)
    normalize_per_scene_room_field(slots, "scene_song", "song", rooms)
    normalize_per_scene_room_field(slots, "scene_lyrics", "lyrics", rooms)
    normalize_per_scene_room_field(slots, "scene_fall_words", "fallWords", rooms)

    return rooms, images, stories


def build(slots_path: Path, workdir: Path, out_path: Path) -> None:
    try:
        slots = json.loads(slots_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise BuildError(f"invalid slots JSON at {slots_path}: {exc}") from exc
    if not isinstance(slots, dict):
        raise BuildError("filled-slots.json must contain a JSON object")

    rooms, images, stories = normalize_native_slots(slots)

    html = CANONICAL_HTML.read_text(encoding="utf-8")
    html = apply_room_slots(html, rooms)
    html = apply_image_slots(html, images, workdir)
    html = apply_story_slots(html, stories, workdir)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a paper-house gift without modifying template-source HTML.")
    parser.add_argument("--slots", required=True, type=Path, help="Path to filled-slots.json")
    parser.add_argument("--workdir", type=Path, help="Directory containing per-gift assets; defaults to the slots file directory")
    parser.add_argument("--out", required=True, type=Path, help="Output index.html path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    slots_path = args.slots.resolve()
    workdir = (args.workdir or slots_path.parent).resolve()
    out_path = args.out.resolve()
    try:
        build(slots_path, workdir, out_path)
    except BuildError as exc:
        print(f"paper-house build error: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {out_path}")
    print(f"source template unchanged: {CANONICAL_HTML}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
