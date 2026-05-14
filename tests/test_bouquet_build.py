import base64
import hashlib
import json
import re
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "assets" / "templates" / "bouquet"
CANONICAL_HTML = TEMPLATE_DIR / "template-source" / "mothers-day-blue-bouquet.html"
BUILD_SCRIPT = TEMPLATE_DIR / "template-source" / "build.py"
PNG_BYTES = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAFgwJ/luzUKwAAAABJRU5ErkJggg=="
)


def write_minimal_bouquet_assets(workdir):
    flower_dir = workdir / "transparent-png"
    gem_dir = workdir / "gems"
    flower_dir.mkdir()
    gem_dir.mkdir()
    for name in [
        "bouquet-10-white-orchid.png",
        "bouquet-02-violet-iris.png",
        "bouquet-11-blue-hydrangea.png",
    ]:
        (flower_dir / name).write_bytes(PNG_BYTES)
    (gem_dir / "gem2.png").write_bytes(PNG_BYTES)
    (gem_dir / "gem4.png").write_bytes(PNG_BYTES)


def sample_phase4_slots():
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
        "source_path_echo_test": "/tmp/private-should-not-leak",
    }


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
            str(BUILD_SCRIPT),
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


def run_playwright_smoke(script, url):
    result = subprocess.run(
        ["python3", str(script), url],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0 and "PLAYWRIGHT_LAUNCH_UNAVAILABLE" in result.stderr:
        pytest.skip("Playwright browser launch is unavailable in this environment")
    result.check_returncode()
    return result


def test_bouquet_runtime_config_does_not_expose_workdir(tmp_path):
    out, workdir, _ = run_bouquet_builder(tmp_path, sample_phase4_slots())
    html_text = out.read_text(encoding="utf-8")
    config = extract_bouquet_config(html_text)

    assert "workdir" not in config
    assert str(workdir) not in html_text


def test_bouquet_playwright_launch_unavailable_is_skipped(monkeypatch):
    def fake_run(args, **_kwargs):
        return subprocess.CompletedProcess(
            args,
            1,
            stdout="",
            stderr="PLAYWRIGHT_LAUNCH_UNAVAILABLE: browser blocked by sandbox",
        )

    monkeypatch.setattr(subprocess, "run", fake_run)

    with pytest.raises(pytest.skip.Exception):
        run_playwright_smoke(Path("check_bouquet_page.py"), "file:///tmp/index.html")


def test_bouquet_builder_injects_runtime_config(tmp_path):
    out, workdir, _ = run_bouquet_builder(tmp_path, sample_phase4_slots())
    html_text = out.read_text(encoding="utf-8")
    config = extract_bouquet_config(html_text)

    assert out.is_file()
    assert config["template"] == "bouquet"
    assert config["style"]["color_palette"] == "白玫瑰 + 蓝宝石"
    assert [item["id"] for item in config["catalog"]] == ["orchid", "iris", "hydrangea"]
    assert [item["id"] for item in config["gemCatalog"]] == ["gem2", "gem4"]
    assert all(item["src"].startswith("data:image/png;base64,") for item in config["catalog"])
    assert all(item["src"].startswith("data:image/png;base64,") for item in config["gemCatalog"])
    assert [stem["catalog"] for stem in config["layout"]["stems"]] == ["orchid", "iris", "hydrangea"]
    assert config["layout"]["placedGems"][0]["gem"] == "gem2"
    assert config["cards"]["orchid"]["text"] == "你说晒过太阳的被子最像家，这句话我一直记得。"
    assert config["giftCopy"]["message"] == "把今天做成一束可以慢慢看的花。"
    assert "你说晒过太阳的被子最像家" in html_text

    card_text = json.loads((workdir / "cards" / "card_text.json").read_text(encoding="utf-8"))
    assert card_text["orchid"]["title"] == "给你的白蝴蝶兰"


def test_bouquet_builder_does_not_mutate_canonical_html(tmp_path):
    canonical_before = hashlib.sha256(CANONICAL_HTML.read_bytes()).hexdigest()

    out, _, _ = run_bouquet_builder(tmp_path, sample_phase4_slots())

    canonical_after = hashlib.sha256(CANONICAL_HTML.read_bytes()).hexdigest()
    assert canonical_before == canonical_after
    assert out.read_text(encoding="utf-8") != CANONICAL_HTML.read_text(encoding="utf-8")


def test_bouquet_builder_output_has_no_raw_absolute_desktop_paths(tmp_path):
    out, _, _ = run_bouquet_builder(tmp_path, sample_phase4_slots())
    html_text = out.read_text(encoding="utf-8")

    assert "/tmp/private-should-not-leak" not in html_text
    assert "private-should-not-leak" not in html_text


def test_bouquet_generated_html_passes_static_h5_verification(tmp_path):
    out, _, _ = run_bouquet_builder(tmp_path, sample_phase4_slots())

    result = subprocess.run(
        ["bash", "scripts/verify-h5.sh", str(out)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "Static H5 checks passed" in result.stdout


def test_bouquet_generated_html_loads_without_console_errors(tmp_path):
    playwright_available = subprocess.run(
        ["python3", "-c", "import playwright"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if playwright_available.returncode != 0:
        pytest.skip("Playwright is not available in this checkout")

    out, _, _ = run_bouquet_builder(tmp_path, sample_phase4_slots())
    script = tmp_path / "check_bouquet_page.py"
    script.write_text(
        """
import sys
from playwright.sync_api import sync_playwright, Error as PlaywrightError

url = sys.argv[1]
with sync_playwright() as p:
    try:
        browser = p.chromium.launch(headless=True)
    except PlaywrightError as exc:
        raise SystemExit(f"PLAYWRIGHT_LAUNCH_UNAVAILABLE: {exc}")
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

    run_playwright_smoke(script, out.resolve().as_uri())
