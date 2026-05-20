import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "assets" / "templates" / "draw-card"
TEMPLATE = TEMPLATE_DIR / "template.json"
CANONICAL = TEMPLATE_DIR / "template-source" / "retro-gacha-card.html"


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
        r"window\.DRAW_CARD_GIFT_CONFIG\s*=\s*(\{.*?\});\s*</script>",
        html_text,
        re.S,
    )
    assert match, "missing DRAW_CARD_GIFT_CONFIG script"
    return json.loads(match.group(1))


def sample_slots():
    return {
        "draw_card_copy": {
            "panelTitle": "给小予抽一张今晚的卡",
            "machine_button": "投递小愿望",
            "delivered": "小卡已经进槽了，转一下旋钮",
        },
        "wish_defaults": {
            "lyric": "今天只做一件事",
            "theme_color": "#ff6699",
            "eason_style": "温柔暴击",
            "card_style": "文艺信笺",
        },
        "lyrics": ["今晚的灯还亮着", "晚霞替你签收"],
        "carousel_photos": ["draw-card-work/轮播图/hero.jpg"],
        "wish_photos": ["draw-card-work/card_materials/card_photo_01.jpg"],
        "decor_stickers": ["draw-card-work/stickers/decorations/sample.png"],
    }


def run_draw_card_builder(tmp_path, slots):
    workdir = tmp_path / "draw-card-work"
    (workdir / "轮播图").mkdir(parents=True)
    (workdir / "card_materials").mkdir(parents=True)
    (workdir / "generated_stickers" / "all").mkdir(parents=True)
    (workdir / "stickers" / "decorations").mkdir(parents=True)
    (workdir / "轮播图" / "hero.jpg").write_bytes(b"fake-jpeg")
    (workdir / "card_materials" / "card_photo_01.jpg").write_bytes(b"fake-jpeg")
    (workdir / "generated_stickers" / "all" / "eason_sticker_01.png").write_bytes(PNG_1X1)
    (workdir / "stickers" / "decorations" / "sample.png").write_bytes(PNG_1X1)
    (workdir / "carousel-photos-data.js").write_text(
        "window.EASON_CAROUSEL_PHOTOS = ['data:image/png;base64,stub'];",
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


def test_draw_card_template_manifest_and_files_exist():
    manifest = load_manifest()

    assert manifest["id"] == "draw-card"
    assert "draw_card" in manifest["aliases"]
    assert manifest["status"] == "ready"
    assert manifest["preview"] == "preview.jpg"
    assert (TEMPLATE_DIR / manifest["preview"]).is_file()
    assert (TEMPLATE_DIR / "demo-preview.png").is_file()
    assert manifest["canonical_html_reference"] == "template-source/retro-gacha-card.html"
    assert (TEMPLATE_DIR / manifest["canonical_html_reference"]).is_file()
    assert manifest["build_script"] == "template-source/build.py"
    assert (TEMPLATE_DIR / manifest["build_script"]).is_file()
    assert (TEMPLATE_DIR / "README.md").is_file()
    assert (TEMPLATE_DIR / "SPEC.md").is_file()
    assert (TEMPLATE_DIR / "RELEASE.md").is_file()
    assert (TEMPLATE_DIR / "base" / ".gitkeep").is_file()


def test_draw_card_asset_bundle_metadata_matches_release_contract():
    bundle = load_manifest()["asset_bundle"]

    assert bundle["local_path"] == "base/"
    assert bundle["url"].endswith("/assets-draw-card-v1/draw-card-v1.zip")
    assert bundle["sha256"] == "385ab18374edae6417f4b524b42d707c8cb956c94cbfc45dfe7a94a5bae074cf"
    assert len(bundle["sha256"]) == 64
    assert bundle["size_mb"] == 24
    assert bundle["contents"] == [
        "card_materials/",
        "generated_stickers/",
        "stickers/",
        "轮播图/",
        "reference/",
        "lyrics.txt",
        "carousel-photos-data.js",
    ]


def test_draw_card_base_gitkeep_is_allowed_but_bundle_contents_are_ignored():
    gitkeep = TEMPLATE_DIR / "base" / ".gitkeep"

    assert gitkeep.is_file()
    keep_result = subprocess.run(
        ["git", "check-ignore", "-q", "assets/templates/draw-card/base/.gitkeep"],
        cwd=ROOT,
    )
    assert keep_result.returncode == 1

    bundle_result = subprocess.run(
        ["git", "check-ignore", "-q", "assets/templates/draw-card/base/stickers"],
        cwd=ROOT,
    )
    assert bundle_result.returncode == 0


def test_draw_card_slots_capture_card_machine_rules():
    manifest = load_manifest()

    story = slot_by_id(manifest, "draw_card_story_plan")
    assert story["type"] == "ai_text"
    assert "core_lyric_or_phrase" in story["output_fields"]
    assert "public figure" in story["rules"][1]

    lyrics = slot_by_id(manifest, "background_lyrics")
    assert lyrics["type"] == "ai_text"
    assert "Do not paste long copyrighted lyrics" in lyrics["rules"][0]

    carousel = slot_by_id(manifest, "carousel_photos")
    assert carousel["type"] == "user_image_processed"
    assert carousel["runtime_mapping"]["runtime_global"] == "window.DRAW_CARD_GIFT_CONFIG.carouselPhotos"

    stickers = slot_by_id(manifest, "decor_sticker_picks")
    assert stickers["type"] == "sticker_picks"
    assert stickers["library_subpaths"] == ["stickers/decorations/"]
    assert "avoid unrelated sticker scatter" in stickers["placement_rules"][0]

    copy = slot_by_id(manifest, "wish_copy")
    assert "user's habitual language" in copy["language_rule"]
    assert "copy.machineButton" in copy["output_fields"]


def test_draw_card_docs_describe_four_phase_plan_and_language_rule():
    spec = (TEMPLATE_DIR / "SPEC.md").read_text(encoding="utf-8")
    plan = (
        ROOT / "docs" / "superpowers" / "plans" / "2026-05-20-draw-card-template-support.md"
    ).read_text(encoding="utf-8")
    release = (TEMPLATE_DIR / "RELEASE.md").read_text(encoding="utf-8")

    for phrase in [
        "Pick one card thesis",
        "fandom language respectful",
        "Lyric use must be short",
        "Photos must survive pixelation",
        "Gift-facing text follows the user's language",
        "canonical HTML",
    ]:
        assert phrase in spec

    for phase in [
        "Phase 1 — Template Registry and Documentation",
        "Phase 2 — Runtime Builder and Config Hook",
        "Phase 3 — Asset Bundle and GitHub Release",
        "Phase 4 — Tests, Registry Copy, and Verification",
    ]:
        assert phase in plan

    assert "assets-draw-card-v1" in release
    assert "draw-card-v1.zip" in release
    assert "shasum -a 256" in release


def test_draw_card_registry_copy_is_discoverable():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    templates = (ROOT / "references" / "templates.md").read_text(encoding="utf-8")

    for text in [readme, skill, templates]:
        assert "--template draw-card" in text

    assert "assets/templates/draw-card/preview.jpg" in readme
    assert "Retro Gacha Wish Machine" in templates
    assert "scripts/fetch-asset-bundle.sh --template draw-card" in templates


def test_draw_card_builder_injects_runtime_config_inlines_assets_and_preserves_source(tmp_path):
    before = hashlib.sha256(CANONICAL.read_bytes()).hexdigest()

    out, workdir, _ = run_draw_card_builder(tmp_path, sample_slots())
    html_text = out.read_text(encoding="utf-8")
    config = extract_runtime_config(html_text)

    assert out.is_file()
    assert config["template"] == "draw-card"
    assert config["copy"]["panelTitle"] == "给小予抽一张今晚的卡"
    assert config["copy"]["machineButton"] == "投递小愿望"
    assert config["wishDefaults"]["themeColor"] == "#ff6699"
    assert config["wishDefaults"]["easonStyle"] == "温柔暴击"
    assert config["lyrics"] == ["今晚的灯还亮着", "晚霞替你签收"]
    assert config["carouselPhotos"][0].startswith("data:image/jpeg;base64,")
    assert config["wishPhotos"][0].startswith("data:image/jpeg;base64,")
    assert config["wishStickers"][0].startswith("data:image/png;base64,")
    assert config["decorStickers"][0].startswith("data:image/png;base64,")
    assert "window.DRAW_CARD_GIFT_CONFIG" in html_text
    assert "window.EASON_CAROUSEL_PHOTOS = ['data:image/png;base64,stub'];" in html_text
    assert 'src="carousel-photos-data.js"' not in html_text
    assert "draw-card-work/轮播图/hero.jpg" not in html_text

    staged = json.loads((workdir / "runtime_config.json").read_text(encoding="utf-8"))
    assert staged == config
    after = hashlib.sha256(CANONICAL.read_bytes()).hexdigest()
    assert after == before
