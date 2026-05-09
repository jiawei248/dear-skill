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


def test_bouquet_spec_describes_ready_scope_and_runtime_builder():
    spec = (TEMPLATE_DIR / "SPEC.md").read_text(encoding="utf-8")

    assert "## Ready Scope" in spec
    assert "## Slot Mapping Contract" in spec
    assert "## Runtime Builder Contract" in spec
    assert "Phase 1 Scope" not in spec
    assert "Later phases" not in spec
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
        "Runtime Builder Contract",
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


def test_readme_uses_human_template_demo_copy():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    for phrase in [
        "把每一次分享欲都变成一份有仪式感的电子礼物",
        "一张有趣的照片、一段 TA 可能会喜欢的音乐、一句突然想起的话",
        "作为实体礼物之外的另一层惊喜",
        "你可以直接指定 H5、图片、文字或互动文字游戏",
        "### 模板模式：直接选一个精调礼物模板",
        "当前精调模板：",
        "把你们的回忆变成四个可爱的小房间，每个房间都有一首专属 BGM。",
        "给妈妈做一张赛博奖杯花束插画，每一朵花都藏着一个你们的故事。",
        "给妈妈做一个赛博奖杯插画",
        "每一朵花都蕴藏着一个你们的故事",
        "turns every small spark of sharing into a ceremonial digital gift",
        "a funny photo, a song they might love, or a tiny memory that suddenly comes back",
        "an extra layer of surprise alongside a physical gift",
        "You can choose H5, image, text, or text-play yourself",
        "### Template mode: choose a polished gift template",
        "Polished templates:",
        "Turns your shared memories into four charming little rooms, each with its own BGM.",
        "Makes mom a cyber-trophy bouquet illustration where every flower holds one of your stories.",
        "Makes mom a cyber-trophy illustration",
        "every flower carries one story between you",
        "![paper-house demo](assets/templates/paper-house/demo-preview.png)",
        "![bouquet demo](assets/templates/bouquet/demo-preview.png)",
        "![Paper-house demo](assets/templates/paper-house/demo-preview.png)",
        "![Bouquet demo](assets/templates/bouquet/demo-preview.png)",
    ]:
        assert phrase in readme

    for forbidden in [
        "最省力",
        "填表",
        "就这么简单",
        "都可以，用最省力的那种",
        "你不用组织语言，不用填表",
        "格式不是你选的",
        "礼物形状",
        "当前一等模板",
        "不需要理解内部 schema",
        "如果别人已经帮你安装好了",
        "本 skill 的来源",
        "hermes-daily-gift",
        "把一段共同唱过的歌",
        "蓝白花送给妈妈",
        "Easiest use",
        "lowest-friction",
        "No form-filling required",
        "You don't pick the format",
        "pre-designed gift shape",
        "First-class templates",
        "If someone else already installed it for you",
        "Turns a song you shared",
        "blue-white bouquet",
        "Origin",
    ]:
        assert forbidden not in readme

    assert (ROOT / "assets" / "templates" / "paper-house" / "demo-preview.png").is_file()
    assert (ROOT / "assets" / "templates" / "bouquet" / "demo-preview.png").is_file()


def test_bouquet_status_docs_describe_ready_builder_not_skeleton():
    manifest = load_manifest()
    readme = (TEMPLATE_DIR / "README.md").read_text(encoding="utf-8")
    templates = (ROOT / "references" / "templates.md").read_text(encoding="utf-8")

    assert manifest["status"] == "ready"
    for text in [readme, templates]:
        assert "phase-1-skeleton" not in text
        assert "phase-3-runtime-builder" not in text
        assert "build stub" not in text
    assert "runtime builder" in readme
    assert "Status: ready" in templates


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
        "给妈妈做一张赛博奖杯花束插画",
    ]:
        assert phrase in readme

    for phrase in [
        "给妈妈做一张赛博奖杯花束插画",
        "适合生日、母亲节、感谢、朋友安慰、纪念日",
        "/dear --template bouquet 给妈妈做一束可以拖动的花",
        "/dear 用 bouquet 模板给朋友做一份生日礼物",
    ]:
        assert phrase in templates
