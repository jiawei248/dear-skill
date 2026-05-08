import json
from pathlib import Path


TEMPLATE = Path("assets/templates/paper-house/template.json")


def load_slots():
    manifest = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    return {slot["id"]: slot for slot in manifest["slots"]}


def test_scene_decorations_uses_common_sticker_pick_fields():
    decorations = load_slots()["scene_decorations"]

    assert decorations["type"] == "sticker_picks"
    assert decorations["library_subpaths"] == [
        "stickers/decorations/",
        "stickers/food/",
        "stickers/furnitures/",
        "stickers/household_goods/",
        "stickers/music_player/",
        "stickers/pets/",
        "stickers/plants/",
        "stickers/transportation/",
    ]
    assert decorations["count_range"] == [5, 7]
    assert decorations["placement_zone"] == "paper-house-room-quadrants"
    assert "selection_hint" in decorations
    assert decorations["runtime_mapping"] == {
        "output_paths": "paper-house-work/stickers/{scene_id}/{1..6}.png",
        "layout_source": "DECOR_LAYOUT in canonical HTML",
    }
    assert "source_library" not in decorations
    assert "library_categories" not in decorations
    assert "count_range_per_scene" not in decorations


def test_character_reference_is_separate_from_scene_figure_sprite():
    slots = load_slots()
    character_reference = slots["character_reference"]
    figure = slots["scene_figure_image"]

    assert character_reference["type"] == "user_image_processed"
    assert character_reference["count"] == "0-2"
    assert character_reference["required"] is False
    assert character_reference["pipeline"][0]["step"] == "stylize-character"
    assert character_reference["runtime_mapping"]["output_paths"] == "paper-house-work/character_reference/{n}.png"

    assert figure["type"] == "ai_generated_image"
    assert figure["reference_slot"] == "character_reference"
    assert figure["filename_pattern"] == "figures/scene_{scene_id}[_{n}].png"
    assert "pre_process_pipeline" not in figure


def test_room_walls_and_floor_has_common_generation_metadata():
    walls = load_slots()["room_walls_and_floor"]

    assert walls["type"] == "ai_generated_image"
    assert walls["approx_size"] == [1280, 1280]
    assert walls["aspect_ratio"] == "source-dependent"
    assert "prompt_hint" in walls
    assert "style_anchor" in walls
    assert walls["consistency_group"] == "paper-house-{scene_id}-walls-and-floor"
    assert walls["runtime_mapping"] == {
        "output_paths": {
            "wall_left": "paper-house-work/walls/{scene_id}_left.jpg",
            "wall_right": "paper-house-work/walls/{scene_id}_right.jpg",
            "floor": "paper-house-work/floors/{scene_id}_floor.jpg",
        }
    }


def test_template_preview_path_exists():
    manifest = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    preview = manifest["preview"]

    assert (TEMPLATE.parent / preview).is_file()


def test_paper_house_activation_disclosure_sets_expectations():
    manifest = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    disclosure = manifest["activation_disclosure"]

    message = disclosure["message"]
    assert "150MB" in message
    assert "图片生成" in message
    assert "轻量版" in message

    options = disclosure["options"]
    assert [option["id"] for option in options] == [
        "full",
        "lightweight_draft",
        "text_image_fallback",
    ]
    assert any("rembg" in item for item in disclosure["cost_notes"])
    assert any("iTunes" in item for item in disclosure["cost_notes"])


def test_paper_house_spec_documents_activation_choices():
    spec = (TEMPLATE.parent / "SPEC.md").read_text(encoding="utf-8")

    assert "Activation disclosure" in spec
    assert "第一次会下载约 150MB 素材" in spec
    assert "full version" in spec
    assert "lightweight draft version" in spec
    assert "text/image fallback" in spec
