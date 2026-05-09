import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "assets" / "templates" / "bouquet" / "template.json"
TEMPLATE_DIR = TEMPLATE.parent


def load_manifest():
    return json.loads(TEMPLATE.read_text(encoding="utf-8"))


def test_bouquet_template_manifest_and_preview_exist():
    manifest = load_manifest()

    assert manifest["id"] == "bouquet"
    assert manifest["preview"] == "preview.jpg"
    assert (TEMPLATE_DIR / manifest["preview"]).is_file()
    assert manifest["canonical_html_reference"] == "template-source/mothers-day-blue-bouquet.html"
    assert (TEMPLATE_DIR / manifest["canonical_html_reference"]).is_file()
    assert manifest["build_script"] == "template-source/build.py"
    assert (TEMPLATE_DIR / manifest["build_script"]).is_file()
    assert (TEMPLATE_DIR / "SPEC.md").is_file()
    assert (TEMPLATE_DIR / "README.md").is_file()
    assert (TEMPLATE_DIR / "RELEASE.md").is_file()
    assert (TEMPLATE_DIR / "base").is_dir()


def test_bouquet_asset_bundle_metadata_matches_phase_one_contract():
    manifest = load_manifest()
    bundle = manifest["asset_bundle"]

    assert bundle["local_path"] == "base/"
    assert bundle["url"].endswith("/assets-bouquet-v1/bouquet-v1.zip")
    assert len(bundle["sha256"]) == 64
    assert bundle["size_mb"] > 0
    assert bundle["contents"] == [
        "flowers/",
        "greenery/",
        "gems/",
        "fonts/",
        "reference/",
    ]


def test_bouquet_bundle_artifact_is_prepared_but_not_expanded_in_repo():
    bundle = ROOT / "assets" / "templates" / "bouquet" / "RELEASE.md"
    text = bundle.read_text(encoding="utf-8")

    assert "assets-bouquet-v1" in text
    assert "bouquet-v1.zip" in text
    assert "shasum -a 256" in text
    assert not (TEMPLATE_DIR / "base" / "flowers").exists()
    assert not (TEMPLATE_DIR / "base" / "gems").exists()
    assert not (TEMPLATE_DIR / "base" / "fonts").exists()


def test_bouquet_spec_describes_phase_one_readonly_source_and_bundle():
    spec = (TEMPLATE_DIR / "SPEC.md").read_text(encoding="utf-8")

    assert "canonical HTML is read-only" in spec
    assert "template-source/mothers-day-blue-bouquet.html" in spec
    assert "template-source/build.py" in spec
    assert "flowers can be dragged" in spec
    assert "gems can be freely added" in spec
    assert "cards can be edited interactively" in spec
    assert "asset bundle" in spec


def slot_by_id(manifest, slot_id):
    return {slot["id"]: slot for slot in manifest["slots"]}[slot_id]


def test_bouquet_phase2_slot_schema_matches_common_template_contract():
    manifest = load_manifest()

    recipient = slot_by_id(manifest, "recipient_material")
    assert recipient["type"] == "user_context"
    assert recipient["accepted_inputs"] == ["photos", "chat_screenshots", "social_screenshots", "text", "notes"]
    assert "original language" in recipient["grounding_rules"][0]
    assert "generic blessing" in recipient["grounding_rules"][2]

    style = slot_by_id(manifest, "bouquet_style_direction")
    assert style["type"] == "ai_text"
    assert style["output_fields"] == {
        "color_palette": "requested or inferred flower/gem color combination",
        "emotional_tone": "the relationship mood this bouquet should carry",
        "occasion": "why the user is making the bouquet now",
        "recipient_language": "the language the user and recipient naturally use together",
    }
    assert "白玫瑰 + 蓝宝石" in style["user_can_specify"]

    flowers = slot_by_id(manifest, "flower_picks")
    assert flowers["type"] == "asset_picks"
    assert flowers["library_subpaths"] == ["flowers/", "greenery/"]
    assert flowers["placement_zone"] == "bouquet-canvas"
    assert flowers["runtime_mapping"]["output_paths"] == "bouquet-work/flowers/{n}.png"
    assert flowers["style_rules"] == [
        "film-textured floral cutouts",
        "transparent PNG with soft hand-cut edges",
        "flowers may include gem or subtle sparkle accents",
        "must stay close to existing bouquet asset texture, not clean generic AI stickers",
    ]
    assert flowers["extension_policy"]["user_can_add_new_florals"] is True
    assert flowers["extension_policy"]["generation_model"] == "general image generation model"
    assert flowers["extension_policy"]["style_references"] == ["base/flowers/", "base/reference/original-png/"]

    gems = slot_by_id(manifest, "gem_picks")
    assert gems["type"] == "asset_picks"
    assert gems["library_subpaths"] == ["gems/"]
    assert gems["placement_zone"] == "free-canvas-accents"
    assert "freely added" in gems["purpose"]

    cards = slot_by_id(manifest, "card_notes")
    assert cards["type"] == "ai_text"
    assert cards["per_card"] is True
    assert "user-provided original language" in cards["rules"][0]
    assert "one concrete memory or emotion" in cards["rules"][1]
    assert "愿你天天开心" in cards["rules"][2]
    assert cards["interactive_editing"] is True

    layout = slot_by_id(manifest, "layout_editing_contract")
    assert layout["type"] == "template_notes"
    assert layout["opening_notice"] == [
        "flowers can be dragged",
        "gems can be freely added",
        "paper card positions can be changed",
        "card content can be revised interactively with AI",
    ]


def test_bouquet_activation_disclosure_is_lightweight_but_explicit():
    disclosure = load_manifest()["activation_disclosure"]

    assert "互动花束模板" in disclosure["message"]
    assert "花材素材" in disclosure["message"]
    assert "图片生成能力" in disclosure["message"]
    assert "内置花材" in disclosure["message"]
    assert [option["id"] for option in disclosure["options"]] == [
        "built_in_assets",
        "custom_florals",
        "text_image_fallback",
    ]


def test_bouquet_spec_documents_phase2_slot_matching_rules():
    spec = (TEMPLATE_DIR / "SPEC.md").read_text(encoding="utf-8")

    for phrase in [
        "recipient_material",
        "bouquet_style_direction",
        "flower_picks",
        "gem_picks",
        "card_notes",
        "layout_editing_contract",
        "白玫瑰 + 蓝宝石",
        "愿你天天开心",
        "base/reference/original-png/",
    ]:
        assert phrase in spec


def test_bouquet_spec_documents_phase3_runtime_mapping():
    spec = (TEMPLATE_DIR / "SPEC.md").read_text(encoding="utf-8")

    for phrase in [
        "Phase 3 Runtime Mapping",
        "window.BOUQUET_GIFT_CONFIG",
        "catalog",
        "gemCatalog",
        "layout.stems",
        "layout.placedGems",
        "cards",
        "giftCopy",
        "scripts/verify-h5.sh",
        "does not modify the canonical HTML",
    ]:
        assert phrase in spec


def test_bouquet_phase4_is_documented_as_first_class_template():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    templates = (ROOT / "references" / "templates.md").read_text(encoding="utf-8")

    for phrase in [
        "/dear --template bouquet 给妈妈做一束可以拖动的花",
        "/dear 用 bouquet 模板给朋友做一份生日礼物",
    ]:
        assert phrase in skill

    for phrase in [
        "bouquet",
        "paper-house",
        "preview.jpg",
        "可拖拽花材、自由加宝石、可改小纸片内容的互动花束",
    ]:
        assert phrase in readme

    for phrase in [
        "可拖拽花材、自由加宝石、可改小纸片内容的互动花束",
        "适合生日、母亲节、感谢、朋友安慰、纪念日",
        "比 paper-house 轻，但比纯图片更可玩",
        "/dear --template bouquet 给妈妈做一束可以拖动的花",
        "/dear 用 bouquet 模板给朋友做一份生日礼物",
    ]:
        assert phrase in templates
