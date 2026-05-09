import base64
import hashlib
import json
import re
import subprocess
from pathlib import Path

import pytest


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


def write_minimal_bouquet_assets(workdir):
    png = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAFgwJ/luzUKwAAAABJRU5ErkJggg=="
    )
    flower_dir = workdir / "transparent-png"
    gem_dir = workdir / "gems"
    flower_dir.mkdir()
    gem_dir.mkdir()
    for name in [
        "bouquet-10-white-orchid.png",
        "bouquet-02-violet-iris.png",
        "bouquet-11-blue-hydrangea.png",
    ]:
        (flower_dir / name).write_bytes(png)
    (gem_dir / "gem2.png").write_bytes(png)
    (gem_dir / "gem4.png").write_bytes(png)


def run_bouquet_builder(tmp_path, slots):
    workdir = tmp_path / "bouquet-work"
    workdir.mkdir()
    write_minimal_bouquet_assets(workdir)
    slots_path = workdir / "filled-slots.json"
    slots_path.write_text(json.dumps(slots, ensure_ascii=False), encoding="utf-8")
    out = tmp_path / "index.html"

    result = subprocess.run(
        [
            "python3",
            str(TEMPLATE_DIR / "template-source" / "build.py"),
            "--slots",
            str(slots_path),
            "--workdir",
            str(workdir),
            "--out",
            str(out),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return out, workdir, result


def extract_bouquet_config(html_text):
    match = re.search(
        r"window\.BOUQUET_GIFT_CONFIG\s*=\s*(\{.*?\});\s*</script>",
        html_text,
        re.S,
    )
    assert match, "missing BOUQUET_GIFT_CONFIG script"
    return json.loads(match.group(1))


def sample_phase3_slots():
    return {
        "bouquet_style_direction": {
            "color_palette": "白玫瑰 + 蓝宝石",
            "emotional_tone": "像朋友之间的礼物",
            "occasion": "生日",
            "recipient_language": "zh-CN",
        },
        "flower_picks": {
            "items": [
                {"id": "orchid", "name": "白蝴蝶兰", "src": "bouquet-10-white-orchid.png"},
                {"id": "iris", "name": "紫鸢尾", "src": "bouquet-02-violet-iris.png"},
                {"id": "hydrangea", "name": "蓝绣球", "src": "bouquet-11-blue-hydrangea.png"},
            ]
        },
        "gem_picks": {
            "items": [
                {"id": "gem2", "name": "蓝宝石", "src": "gem2.png", "size": 50},
                {"id": "gem4", "name": "小星光", "src": "gem4.png", "size": 42},
            ],
            "placed": [
                {"gem": "gem2", "x": 55, "y": 42, "w": 52, "r": -6, "z": 2},
                {"gem": "gem4", "x": 43, "y": 34, "w": 38, "r": 11, "z": 3},
            ],
        },
        "card_notes": [
            {
                "catalog": "orchid",
                "label": "晒好的被子",
                "title": "给你的白蝴蝶兰",
                "text": "你说晒过太阳的被子最像家，这句话我一直记得。",
                "x": 92,
                "y": 154,
                "r": -5,
            },
            {
                "catalog": "iris",
                "label": "蓝紫色小信",
                "title": "给你的紫鸢尾",
                "text": "这束蓝紫色，想替我把那些没说出口的谢谢说完。",
                "x": 468,
                "y": 178,
                "r": 4,
            },
        ],
        "layout_editing_contract": {
            "stems": [
                {"catalog": "orchid", "x": 450, "y": 322, "w": 252, "r": 12, "z": 40, "flip": -1},
                {"catalog": "iris", "x": 342, "y": 306, "w": 292, "r": 1, "z": 38},
                {"catalog": "hydrangea", "x": 260, "y": 348, "w": 268, "r": -13, "z": 25},
            ]
        },
        "gift_copy": {
            "recipient": "亲爱的朋友",
            "message": "把今天做成一束可以慢慢看的花。",
        },
    }


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


def test_bouquet_phase3_builder_injects_runtime_config(tmp_path):
    out, workdir, _ = run_bouquet_builder(tmp_path, sample_phase3_slots())
    html_text = out.read_text(encoding="utf-8")
    config = extract_bouquet_config(html_text)

    assert out.is_file()
    assert config["template"] == "bouquet"
    assert config["style"] == {
        "color_palette": "白玫瑰 + 蓝宝石",
        "emotional_tone": "像朋友之间的礼物",
        "occasion": "生日",
        "recipient_language": "zh-CN",
    }
    assert [item["id"] for item in config["catalog"]] == ["orchid", "iris", "hydrangea"]
    assert [item["id"] for item in config["gemCatalog"]] == ["gem2", "gem4"]
    assert [stem["catalog"] for stem in config["layout"]["stems"]] == ["orchid", "iris", "hydrangea"]
    assert config["layout"]["placedGems"][0]["gem"] == "gem2"
    assert config["cards"]["orchid"]["text"] == "你说晒过太阳的被子最像家，这句话我一直记得。"
    assert config["giftCopy"]["recipient"] == "亲爱的朋友"
    assert config["giftCopy"]["message"] == "把今天做成一束可以慢慢看的花。"
    assert "window.BOUQUET_GIFT_CONFIG" in html_text
    assert "你说晒过太阳的被子最像家" in html_text

    card_text = json.loads((workdir / "cards" / "card_text.json").read_text(encoding="utf-8"))
    assert card_text["orchid"]["title"] == "给你的白蝴蝶兰"


def test_bouquet_phase3_builder_does_not_mutate_canonical_html(tmp_path):
    canonical = TEMPLATE_DIR / "template-source" / "mothers-day-blue-bouquet.html"
    before = hashlib.sha256(canonical.read_bytes()).hexdigest()

    out, _, _ = run_bouquet_builder(tmp_path, sample_phase3_slots())

    after = hashlib.sha256(canonical.read_bytes()).hexdigest()
    assert before == after
    assert out.read_text(encoding="utf-8") != canonical.read_text(encoding="utf-8")


def test_bouquet_phase3_generated_html_passes_static_h5_verification(tmp_path):
    out, _, _ = run_bouquet_builder(tmp_path, sample_phase3_slots())

    result = subprocess.run(
        ["bash", "scripts/verify-h5.sh", str(out)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "Static H5 checks passed" in result.stdout


def test_bouquet_phase3_html_contains_runtime_config_hook(tmp_path):
    out, _, _ = run_bouquet_builder(tmp_path, sample_phase3_slots())
    html_text = out.read_text(encoding="utf-8")

    assert "const giftConfig = window.BOUQUET_GIFT_CONFIG || {};" in html_text
    assert "configuredCatalog" in html_text
    assert "configuredGemCatalog" in html_text
    assert "configuredLayout" in html_text
    assert "configuredCards" in html_text
    assert "applyGiftCopy" in html_text


def test_bouquet_phase3_generated_html_loads_without_console_errors(tmp_path):
    playwright_available = subprocess.run(
        ["python3", "-c", "import playwright"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if playwright_available.returncode != 0:
        pytest.skip("Playwright is not available in this checkout")

    out, _, _ = run_bouquet_builder(tmp_path, sample_phase3_slots())
    script = tmp_path / "check_bouquet_page.py"
    script.write_text(
        """
import sys
from playwright.sync_api import sync_playwright

url = sys.argv[1]
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 390, "height": 844})
    errors = []
    page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(url)
    page.wait_for_load_state("networkidle")
    page.wait_for_selector(".bouquet-stage")
    page.wait_for_selector(".stem-item")
    page.wait_for_selector(".flower-note-chip")
    stage_box = page.locator(".bouquet-stage").bounding_box()
    stem_count = page.locator(".stem-item").count()
    chip_text = page.locator(".flower-note-chip").first.inner_text()
    page.locator(".flower-note-chip").first.click()
    page.wait_for_selector(".flower-note-modal.open")
    note_text = page.locator("#noteCardText").inner_text()
    loaded_images = page.evaluate('''() => Array.from(document.images).filter((img) => img.closest('.stem-item') || img.closest('.placed-gem')).map((img) => ({src: img.getAttribute('src'), width: img.naturalWidth, height: img.naturalHeight}))''')
    browser.close()

if not stage_box or stage_box["width"] < 250 or stage_box["height"] < 300:
    raise SystemExit("bouquet stage is not visibly sized")
if stem_count < 3:
    raise SystemExit(f"expected at least 3 stems, found {stem_count}")
if "晒好的被子" not in chip_text:
    raise SystemExit(f"paper-card chip text was not applied: {chip_text}")
if "你说晒过太阳的被子最像家" not in note_text:
    raise SystemExit(f"note text was not applied: {note_text}")
if not loaded_images:
    raise SystemExit("no bouquet images rendered")
missing_images = [image["src"] for image in loaded_images if image["width"] <= 0 or image["height"] <= 0]
if missing_images:
    raise SystemExit("bouquet images failed to load: " + ", ".join(missing_images[:5]))
if errors:
    raise SystemExit("\\n".join(errors))
""".strip(),
        encoding="utf-8",
    )

    result = subprocess.run(
        ["python3", str(script), out.resolve().as_uri()],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert result.returncode == 0


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
