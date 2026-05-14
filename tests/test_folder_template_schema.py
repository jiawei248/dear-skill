import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "assets" / "templates" / "folder"
TEMPLATE = TEMPLATE_DIR / "template.json"
CANONICAL = TEMPLATE_DIR / "template-source" / "520-folder-gift.html"


PNG_1X1 = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01"
    b"\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)


def load_manifest():
    return json.loads(TEMPLATE.read_text(encoding="utf-8"))


def slot_by_id(manifest, slot_id):
    return {slot["id"]: slot for slot in manifest["slots"]}[slot_id]


def extract_runtime_config(html_text):
    match = re.search(
        r"window\.FOLDER_GIFT_CONFIG\s*=\s*(\{.*?\});\s*</script>",
        html_text,
        re.S,
    )
    assert match, "missing FOLDER_GIFT_CONFIG script"
    return json.loads(match.group(1))


def sample_slots():
    return {
        "folder_copy": {
            "archive": {
                "titleLines": ["FILED UNDER: US", "05/20/2026", "LOCATION: SHANGHAI"],
                "note": "我把那些很小的瞬间，夹进了四个文件夹里。",
            },
            "tabs": [
                {"row": "row1", "title": "01 默契", "subtitle": "一整间超市都变成答案"},
                {"row": "row2", "title": "02 陪伴", "subtitle": "把一半耳机分给你"},
            ],
            "openedFolder": {
                "title": "CHAPTER 01",
                "meta": "520 / SHANGHAI",
                "storyHeading": "关于默契这件小事",
                "storyBodyHtml": "你问我猜猜最想买什么，<mark>旺仔 QQ 糖</mark>就变成了我们的小暗号。",
            },
        },
        "folder_images": {
            ".row1 .photo-main": "folder-work/assets/generated/row1/hero.jpg",
            "[data-open-layout='torn_quote_receipt']": "folder-work/stickers/row1/papers/receipt.png",
        },
        "folder_runtime_overrides": {
            "thumbnailLayoutConfig": {
                "desktop": {
                    "row1": {
                        "photoMain": {"w": 222, "h": 248}
                    }
                }
            },
            "openLayoutConfig": {
                "main_story_paper": {"x": "13%", "y": "61%", "w": "73%"}
            },
        },
    }


def run_folder_builder(tmp_path, slots):
    workdir = tmp_path / "folder-work"
    (workdir / "assets" / "generated" / "row1").mkdir(parents=True)
    (workdir / "assets" / "vendor").mkdir(parents=True)
    (workdir / "stickers" / "row1" / "papers").mkdir(parents=True)
    (workdir / "assets" / "generated" / "row1" / "hero.jpg").write_bytes(b"fake-jpeg")
    (workdir / "stickers" / "row1" / "papers" / "receipt.png").write_bytes(PNG_1X1)
    (workdir / "assets" / "vendor" / "three-global.js").write_text(
        "window.__folderVendorInlineSmoke = true; window.THREE = window.THREE || {};",
        encoding="utf-8",
    )
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


def test_folder_template_manifest_and_files_exist():
    manifest = load_manifest()

    assert manifest["id"] == "folder"
    assert "file-folder" in manifest["aliases"]
    assert manifest["status"] == "ready"
    assert manifest["preview"] == "preview.jpg"
    assert (TEMPLATE_DIR / manifest["preview"]).is_file()
    assert (TEMPLATE_DIR / "demo-preview.png").is_file()
    assert manifest["canonical_html_reference"] == "template-source/520-folder-gift.html"
    assert (TEMPLATE_DIR / manifest["canonical_html_reference"]).is_file()
    assert manifest["build_script"] == "template-source/build.py"
    assert (TEMPLATE_DIR / manifest["build_script"]).is_file()
    assert (TEMPLATE_DIR / "README.md").is_file()
    assert (TEMPLATE_DIR / "SPEC.md").is_file()
    assert (TEMPLATE_DIR / "RELEASE.md").is_file()
    assert (TEMPLATE_DIR / "base" / ".gitkeep").is_file()


def test_folder_asset_bundle_metadata_matches_release_contract():
    bundle = load_manifest()["asset_bundle"]

    assert bundle["local_path"] == "base/"
    assert bundle["url"].endswith("/assets-folder-v1/folder-v1.zip")
    assert bundle["sha256"] == "5e4d030207b7d2529d3ed2c411e9a4ad87c102a1c3a319b9da4c80518cff0f83"
    assert len(bundle["sha256"]) == 64
    assert bundle["size_mb"] == 118
    assert bundle["contents"] == ["assets/", "stickers/", "fonts/"]


def test_folder_base_gitkeep_is_allowed_but_bundle_contents_are_ignored():
    gitkeep = TEMPLATE_DIR / "base" / ".gitkeep"

    assert gitkeep.is_file()
    keep_result = subprocess.run(
        ["git", "check-ignore", "-q", "assets/templates/folder/base/.gitkeep"],
        cwd=ROOT,
    )
    assert keep_result.returncode == 1

    bundle_result = subprocess.run(
        ["git", "check-ignore", "-q", "assets/templates/folder/base/stickers"],
        cwd=ROOT,
    )
    assert bundle_result.returncode == 0


def test_folder_slots_capture_physical_layout_and_content_rules():
    manifest = load_manifest()

    story = slot_by_id(manifest, "folder_story_plan")
    assert story["type"] == "ai_text"
    assert story["count_range"] == [3, 6]
    assert "quoted_or_echoed_detail" in story["output_fields_per_folder"]
    assert "chapter with evidence" in story["rules"][0]

    physical = slot_by_id(manifest, "folder_physical_contract")
    assert physical["type"] == "template_notes"
    assert "front cover" in physical["rules"][1]
    assert "smoothly" in physical["rules"][2]

    photos = slot_by_id(manifest, "folder_photo_generation")
    assert photos["type"] == "ai_generated_image"
    assert "vertical three-strip" in photos["composition_rules"][0]
    assert "polaroid" in photos["composition_rules"][0]

    papers = slot_by_id(manifest, "folder_base_and_paper_picks")
    assert papers["type"] == "asset_picks"
    assert "stickers/base/" in papers["library_subpaths"]
    assert "stickers/tapes_papers/" in papers["library_subpaths"]
    assert "Do not redraw" in papers["purpose"]

    stickers = slot_by_id(manifest, "folder_element_picks")
    assert stickers["type"] == "sticker_picks"
    assert "inside-folder-collage" == stickers["placement_zone"]
    assert "Avoid isolated" in stickers["placement_rules"][2]

    copy = slot_by_id(manifest, "folder_copy")
    assert "user's habitual language" in copy["language_rule"]


def test_folder_docs_describe_four_phase_plan_and_language_rule():
    spec = (TEMPLATE_DIR / "SPEC.md").read_text(encoding="utf-8")
    plan = (ROOT / "docs" / "superpowers" / "plans" / "2026-05-14-folder-template-support.md").read_text(
        encoding="utf-8"
    )
    release = (TEMPLATE_DIR / "RELEASE.md").read_text(encoding="utf-8")

    for phrase in [
        "Preserve the file-folder body",
        "Vary photo formats with intention",
        "Use the bundled base papers and tapes",
        "Sticker groups must stay bounded and meaningful",
        "Gift-facing text follows the user's language",
        "canonical source stays read-only",
    ]:
        assert phrase in spec

    for phase in [
        "Phase 1 — Template Registry and Documentation",
        "Phase 2 — Runtime Builder and Config Hook",
        "Phase 3 — Asset Bundle and GitHub Release",
        "Phase 4 — Tests, Registry Copy, and Verification",
    ]:
        assert phase in plan

    assert "assets-folder-v1" in release
    assert "folder-v1.zip" in release
    assert "shasum -a 256" in release


def test_folder_registry_copy_is_discoverable():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    templates = (ROOT / "references" / "templates.md").read_text(encoding="utf-8")

    for text in [readme, skill, templates]:
        assert "--template folder" in text

    assert "assets/templates/folder/preview.jpg" in readme
    assert "Layered Memory Archive" in templates
    assert "scripts/fetch-asset-bundle.sh --template folder" in templates


def test_folder_builder_injects_runtime_config_inlines_assets_and_preserves_source(tmp_path):
    before = hashlib.sha256(CANONICAL.read_bytes()).hexdigest()

    out, workdir, _ = run_folder_builder(tmp_path, sample_slots())
    html_text = out.read_text(encoding="utf-8")
    config = extract_runtime_config(html_text)

    assert out.is_file()
    assert config["template"] == "folder"
    assert config["archive"]["titleLines"] == ["FILED UNDER: US", "05/20/2026", "LOCATION: SHANGHAI"]
    assert config["archive"]["note"] == "我把那些很小的瞬间，夹进了四个文件夹里。"
    assert config["tabs"][0] == {"row": "row1", "title": "01 默契", "subtitle": "一整间超市都变成答案"}
    assert config["openedFolder"]["storyHeading"] == "关于默契这件小事"
    assert config["openedFolder"]["storyBodyHtml"] == "你问我猜猜最想买什么，<mark>旺仔 QQ 糖</mark>就变成了我们的小暗号。"
    assert config["imageReplacements"][0]["src"].startswith("data:image/jpeg;base64,")
    assert config["imageReplacements"][1]["src"].startswith("data:image/png;base64,")
    assert config["thumbnailLayoutConfig"]["desktop"]["row1"]["photoMain"]["w"] == 222
    assert config["openLayoutConfig"]["main_story_paper"]["x"] == "13%"
    assert "window.FOLDER_GIFT_CONFIG" in html_text
    assert "window.__folderVendorInlineSmoke = true" in html_text
    assert "assets/vendor/three-global.js" not in html_text
    assert "folder-work/assets/generated/row1/hero.jpg" not in html_text
    assert "旺仔 QQ 糖" in html_text

    staged = json.loads((workdir / "runtime_config.json").read_text(encoding="utf-8"))
    assert staged == config
    after = hashlib.sha256(CANONICAL.read_bytes()).hexdigest()
    assert after == before
