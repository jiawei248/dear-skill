import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "assets" / "templates" / "empty-boxes"
TEMPLATE = TEMPLATE_DIR / "template.json"
CANONICAL = TEMPLATE_DIR / "template-source" / "tincase-box-loop.html"


def load_manifest():
    return json.loads(TEMPLATE.read_text(encoding="utf-8"))


def slot_by_id(manifest, slot_id):
    return {slot["id"]: slot for slot in manifest["slots"]}[slot_id]


def extract_runtime_config(html_text):
    match = re.search(
        r"window\.EMPTY_BOXES_GIFT_CONFIG\s*=\s*(\{.*?\});\s*</script>",
        html_text,
        re.S,
    )
    assert match, "missing EMPTY_BOXES_GIFT_CONFIG script"
    return json.loads(match.group(1))


def run_empty_boxes_builder(tmp_path, slots):
    workdir = tmp_path / "empty-boxes-work"
    workdir.mkdir()
    (workdir / "boxes").mkdir(parents=True)
    (workdir / "stickers" / "gems").mkdir(parents=True)
    (workdir / "generated" / "fridge" / "photos").mkdir(parents=True)
    (workdir / "boxes" / "custom-box.png").write_bytes(
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
        b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01"
        b"\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    (workdir / "stickers" / "gems" / "sample.png").write_bytes(
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
        b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01"
        b"\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    (workdir / "generated" / "fridge" / "photos" / "couple.jpg").write_bytes(b"fake-jpeg")
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


def sample_slots():
    return {
        "gift_copy": {
            "recipient": "给小予",
            "occasion": "520快乐",
            "collection_label": "装好啦",
            "object_label": "boxes",
            "memory_label": "我们的小票和冰箱",
        },
        "ambient_gems": [{"src": "stickers/gems/sample.png"}],
        "box_surface_selection": {
            "items": [
                {"src": "empty-boxes-work/boxes/custom-box.png", "boost": 1.2, "collage": "fridgeConflict"}
            ]
        },
        "box_collages": {
            "fridgeConflict": {
                "assets": {
                    "coupleKitchen": "empty-boxes-work/generated/fridge/photos/couple.jpg"
                },
                "layersById": {
                    "main-couple-photo": {
                        "caption": "把冷战放进冰箱"
                    },
                    "fridge-note": {
                        "note": {
                            "lines": [
                                "那天我们终于把声音放轻，",
                                "先把坏情绪冷藏一下。"
                            ],
                            "sign": "下次也慢一点，好好说。"
                        }
                    }
                },
            }
        },
    }


def test_empty_boxes_template_manifest_and_files_exist():
    manifest = load_manifest()

    assert manifest["id"] == "empty-boxes"
    assert "empty_boxes" in manifest["aliases"]
    assert manifest["status"] == "ready"
    assert manifest["preview"] == "preview.jpg"
    assert (TEMPLATE_DIR / manifest["preview"]).is_file()
    assert (TEMPLATE_DIR / "demo-preview.png").is_file()
    assert manifest["canonical_html_reference"] == "template-source/tincase-box-loop.html"
    assert (TEMPLATE_DIR / manifest["canonical_html_reference"]).is_file()
    assert manifest["build_script"] == "template-source/build.py"
    assert (TEMPLATE_DIR / manifest["build_script"]).is_file()
    assert (TEMPLATE_DIR / "README.md").is_file()
    assert (TEMPLATE_DIR / "SPEC.md").is_file()
    assert (TEMPLATE_DIR / "RELEASE.md").is_file()
    assert (TEMPLATE_DIR / "base" / ".gitkeep").is_file()


def test_empty_boxes_asset_bundle_metadata_matches_release_contract():
    bundle = load_manifest()["asset_bundle"]

    assert bundle["local_path"] == "base/"
    assert bundle["url"].endswith("/assets-empty-boxes-v1/empty-boxes-v1.zip")
    assert bundle["sha256"] == "f2e11e0d76fd0779561970ae3b4a9ee0a216fdb2cb7920b89ccbc10ec7517b48"
    assert len(bundle["sha256"]) == 64
    assert bundle["size_mb"] == 113
    assert bundle["contents"] == ["boxes/", "stickers/", "fonts/", "figures/", "generated/"]


def test_empty_boxes_base_gitkeep_is_allowed_but_bundle_contents_are_ignored():
    gitkeep = TEMPLATE_DIR / "base" / ".gitkeep"

    assert gitkeep.is_file()
    keep_result = subprocess.run(
        ["git", "check-ignore", "-q", "assets/templates/empty-boxes/base/.gitkeep"],
        cwd=ROOT,
    )
    assert keep_result.returncode == 1

    bundle_result = subprocess.run(
        ["git", "check-ignore", "-q", "assets/templates/empty-boxes/base/stickers"],
        cwd=ROOT,
    )
    assert bundle_result.returncode == 0


def test_empty_boxes_slots_capture_physical_and_content_rules():
    manifest = load_manifest()

    story = slot_by_id(manifest, "box_story_plan")
    assert story["type"] == "ai_text"
    assert story["count_range"] == [3, 8]
    assert "quoted_or_echoed_detail" in story["output_fields_per_box"]
    assert "micro-scene" in story["rules"][0]

    photos = slot_by_id(manifest, "box_photo_generation")
    assert photos["type"] == "ai_generated_image"
    assert "Photo height must match the container subdivision" in photos["physical_rules"][0]
    assert "shopping basket rim" in photos["identity_rules"][2]

    stickers = slot_by_id(manifest, "sticker_cluster_picks")
    assert stickers["type"] == "sticker_picks"
    assert stickers["placement_zone"] == "inside-current-box-collage"
    assert "stickers/food/" in stickers["library_subpaths"]
    assert "Cluster stickers" in stickers["placement_rules"][1]
    assert "Avoid scattering" in stickers["placement_rules"][2]

    copy = slot_by_id(manifest, "gift_copy")
    assert "user's habitual language" in copy["language_rule"]


def test_empty_boxes_docs_describe_four_phase_plan_and_language_rule():
    spec = (TEMPLATE_DIR / "SPEC.md").read_text(encoding="utf-8")
    plan = (ROOT / "docs" / "superpowers" / "plans" / "2026-05-11-empty-boxes-template-support.md").read_text(
        encoding="utf-8"
    )
    release = (TEMPLATE_DIR / "RELEASE.md").read_text(encoding="utf-8")

    for phrase in [
        "Photos must fit the container geometry",
        "Sticker clusters must form readable motifs",
        "gift copy is not",
        "Use the user's address form",
        "shopping basket",
        "refrigerator",
    ]:
        assert phrase in spec

    for phase in [
        "Phase 1 — Template Registry and Documentation",
        "Phase 2 — Runtime Builder and Config Hook",
        "Phase 3 — Asset Bundle and GitHub Release",
        "Phase 4 — Tests, Registry Copy, and Verification",
    ]:
        assert phase in plan

    assert "assets-empty-boxes-v1" in release
    assert "empty-boxes-v1.zip" in release
    assert "shasum -a 256" in release


def test_empty_boxes_builder_injects_runtime_config_and_preserves_source(tmp_path):
    before = hashlib.sha256(CANONICAL.read_bytes()).hexdigest()

    out, workdir, _ = run_empty_boxes_builder(tmp_path, sample_slots())
    html_text = out.read_text(encoding="utf-8")
    config = extract_runtime_config(html_text)

    assert out.is_file()
    assert config["template"] == "empty-boxes"
    assert config["chrome"]["labels"] == [
        ["520快乐", "label-happy"],
        ["给小予", "label-for"],
        ["装好啦", "label-pick"],
        ["boxes", "label-tincase"],
        ["我们的小票和冰箱", "label-memory"],
    ]
    assert config["gemAssets"][0].startswith("data:image/png;base64,")
    assert config["boxAssets"][0]["src"].startswith("data:image/png;base64,")
    assert config["boxAssets"][0]["boost"] == 1.2
    assert config["boxAssets"][0]["collage"] == "fridgeConflict"
    assert config["collages"]["fridgeConflict"]["assets"]["coupleKitchen"].startswith("data:image/jpeg;base64,")
    assert config["collages"]["fridgeConflict"]["layersById"]["main-couple-photo"]["caption"] == "把冷战放进冰箱"
    assert "window.EMPTY_BOXES_GIFT_CONFIG" in html_text
    assert "把冷战放进冰箱" in html_text

    staged = json.loads((workdir / "runtime_config.json").read_text(encoding="utf-8"))
    assert staged == config
    after = hashlib.sha256(CANONICAL.read_bytes()).hexdigest()
    assert after == before
