# Bouquet Phase 3 Runtime Builder Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the bouquet template builder turn `filled-slots.json` into a standalone, readable, interactive `index.html` without mutating the canonical HTML source.

**Architecture:** Add a minimal runtime config hook to the canonical bouquet HTML and make `template-source/build.py` normalize filled slots into `window.BOUQUET_GIFT_CONFIG`. The canonical HTML keeps its default catalog, gems, layout, and stories, then applies the injected per-gift config only when present. Builder tests cover generated config shape, source immutability, and static H5 validity.

**Tech Stack:** Python 3 standard library, pytest, single-file HTML/JavaScript runtime, existing `scripts/verify-h5.sh`.

---

## Files and Responsibilities

- Modify `assets/templates/bouquet/template-source/build.py`
  - Read `--slots`, `--workdir`, and `--out`.
  - Normalize bouquet slots into a runtime config.
  - Inject `window.BOUQUET_GIFT_CONFIG` into the generated final HTML only.
  - Optionally write derived staging artifacts under `--workdir/cards/card_text.json`.

- Modify `assets/templates/bouquet/template-source/mothers-day-blue-bouquet.html`
  - Add a minimal config hook that reads `window.BOUQUET_GIFT_CONFIG`.
  - Merge configured flower/gem catalogs, card text, initial layout, and gift copy into existing defaults.
  - Keep the current default page working when no config is injected.

- Modify `tests/test_bouquet_template_schema.py`
  - Add Phase 3 tests for builder output, config injection, canonical source immutability, slot normalization, and H5 static verification.

- Modify `assets/templates/bouquet/SPEC.md`
  - Document the Phase 3 runtime config shape and verification requirement.

- Optionally modify `assets/templates/bouquet/template.json`
  - Update `status` or `build_contract` wording only if tests need manifest-level Phase 3 assertions.

---

### Task 1: Add failing builder tests for Phase 3 config injection

**Files:**
- Modify: `tests/test_bouquet_template_schema.py`
- Modify later: `assets/templates/bouquet/template-source/build.py`

- [ ] **Step 1: Add imports and helper functions**

Append these imports near the top of `tests/test_bouquet_template_schema.py`:

```python
import hashlib
import re
import subprocess
```

Append these helper functions after `slot_by_id()`:

```python
def run_bouquet_builder(tmp_path, slots):
    workdir = tmp_path / "bouquet-work"
    workdir.mkdir()
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
```

- [ ] **Step 2: Add failing test for config injection and staging output**

Append this test to `tests/test_bouquet_template_schema.py`:

```python
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
```

- [ ] **Step 3: Run the test to verify it fails**

Run:

```bash
pytest tests/test_bouquet_template_schema.py::test_bouquet_phase3_builder_injects_runtime_config -v
```

Expected: FAIL because current `build.py` injects raw `slots` instead of normalized `style`, `catalog`, `gemCatalog`, `layout`, `cards`, and `giftCopy`.

---

### Task 2: Implement builder-side slot normalization

**Files:**
- Modify: `assets/templates/bouquet/template-source/build.py`
- Test: `tests/test_bouquet_template_schema.py`

- [ ] **Step 1: Replace `build.py` with focused helpers**

Replace `assets/templates/bouquet/template-source/build.py` with:

```python
#!/usr/bin/env python3
import argparse
import json
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


def build_runtime_config(slots: dict, workdir: Path) -> dict:
    cards = normalize_cards(slots)
    config = {
        "template": "bouquet",
        "workdir": str(workdir),
        "style": normalize_style(slots),
        "catalog": [
            item
            for item in (normalize_catalog_item(item) for item in list_from_slot(slots.get("flower_picks")))
            if item.get("id") and item.get("src")
        ],
        "gemCatalog": [
            item
            for item in (normalize_gem_item(item) for item in list_from_slot(slots.get("gem_picks")))
            if item.get("id") and item.get("src")
        ],
        "cards": cards,
        "layout": normalize_layout(slots, cards),
        "giftCopy": normalize_gift_copy(slots, cards),
    }
    return {key: value for key, value in config.items() if value not in ({}, [])}


def write_card_text(workdir: Path, cards: dict) -> None:
    cards_dir = workdir / "cards"
    cards_dir.mkdir(parents=True, exist_ok=True)
    (cards_dir / "card_text.json").write_text(json.dumps(cards, ensure_ascii=False, indent=2), encoding="utf-8")


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
    html_text = inject_config(CANONICAL.read_text(encoding="utf-8"), config)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html_text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Run the focused builder test**

Run:

```bash
pytest tests/test_bouquet_template_schema.py::test_bouquet_phase3_builder_injects_runtime_config -v
```

Expected: PASS.

---

### Task 3: Add failing tests for canonical immutability and H5 static validity

**Files:**
- Modify: `tests/test_bouquet_template_schema.py`
- Modify later: `assets/templates/bouquet/template-source/mothers-day-blue-bouquet.html`

- [ ] **Step 1: Add source immutability test**

Append this test:

```python
def test_bouquet_phase3_builder_does_not_mutate_canonical_html(tmp_path):
    canonical = TEMPLATE_DIR / "template-source" / "mothers-day-blue-bouquet.html"
    before = hashlib.sha256(canonical.read_bytes()).hexdigest()

    out, _, _ = run_bouquet_builder(tmp_path, sample_phase3_slots())

    after = hashlib.sha256(canonical.read_bytes()).hexdigest()
    assert before == after
    assert out.read_text(encoding="utf-8") != canonical.read_text(encoding="utf-8")
```

- [ ] **Step 2: Add static H5 verification test**

Append this test:

```python
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
```

- [ ] **Step 3: Run the tests**

Run:

```bash
pytest tests/test_bouquet_template_schema.py::test_bouquet_phase3_builder_does_not_mutate_canonical_html tests/test_bouquet_template_schema.py::test_bouquet_phase3_generated_html_passes_static_h5_verification -v
```

Expected: PASS for immutability and static H5 checks. If H5 verification fails, fix builder output before touching runtime behavior.

---

### Task 4: Add failing runtime hook tests

**Files:**
- Modify: `tests/test_bouquet_template_schema.py`
- Modify later: `assets/templates/bouquet/template-source/mothers-day-blue-bouquet.html`

- [ ] **Step 1: Add test that final HTML includes the runtime hook code**

Append this test:

```python
def test_bouquet_phase3_html_contains_runtime_config_hook(tmp_path):
    out, _, _ = run_bouquet_builder(tmp_path, sample_phase3_slots())
    html_text = out.read_text(encoding="utf-8")

    assert "const giftConfig = window.BOUQUET_GIFT_CONFIG || {};" in html_text
    assert "configuredCatalog" in html_text
    assert "configuredGemCatalog" in html_text
    assert "configuredLayout" in html_text
    assert "configuredCards" in html_text
    assert "applyGiftCopy" in html_text
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
pytest tests/test_bouquet_template_schema.py::test_bouquet_phase3_html_contains_runtime_config_hook -v
```

Expected: FAIL because the canonical HTML does not yet read the injected config.

---

### Task 5: Implement the minimal HTML runtime hook

**Files:**
- Modify: `assets/templates/bouquet/template-source/mothers-day-blue-bouquet.html`
- Test: `tests/test_bouquet_template_schema.py`

- [ ] **Step 1: Add config variables before default catalogs**

In `assets/templates/bouquet/template-source/mothers-day-blue-bouquet.html`, inside the main `<script>`, immediately before the current `const ASSET_BASE = "transparent-png/";`, replace:

```javascript
    const ASSET_BASE = "transparent-png/";
    const GEM_ASSET_BASE = "gems/";
```

with:

```javascript
    const giftConfig = window.BOUQUET_GIFT_CONFIG || {};
    const configuredCatalog = Array.isArray(giftConfig.catalog) ? giftConfig.catalog : null;
    const configuredGemCatalog = Array.isArray(giftConfig.gemCatalog) ? giftConfig.gemCatalog : null;
    const configuredLayout = giftConfig.layout && typeof giftConfig.layout === "object" ? giftConfig.layout : null;
    const configuredCards = giftConfig.cards && typeof giftConfig.cards === "object" ? giftConfig.cards : {};
    const configuredGiftCopy = giftConfig.giftCopy && typeof giftConfig.giftCopy === "object" ? giftConfig.giftCopy : {};
    const ASSET_BASE = giftConfig.assetBase || "transparent-png/";
    const GEM_ASSET_BASE = giftConfig.gemAssetBase || "gems/";
```

- [ ] **Step 2: Make catalogs configurable**

Replace:

```javascript
    const catalogById = new Map(catalog.map((item) => [item.id, item]));
    const gemCatalogById = new Map(gemCatalog.map((item) => [item.id, item]));
```

with:

```javascript
    const activeCatalog = configuredCatalog && configuredCatalog.length ? configuredCatalog : catalog;
    const activeGemCatalog = configuredGemCatalog && configuredGemCatalog.length ? configuredGemCatalog : gemCatalog;
    const catalogById = new Map(activeCatalog.map((item) => [item.id, item]));
    const gemCatalogById = new Map(activeGemCatalog.map((item) => [item.id, item]));
```

Replace `catalog.forEach((item) => {` in `renderPalette()` with:

```javascript
      activeCatalog.forEach((item) => {
```

Replace `gemCatalog.forEach((item) => {` in `renderGemPalette()` with:

```javascript
      activeGemCatalog.forEach((item) => {
```

- [ ] **Step 3: Make initial layout configurable**

Replace:

```javascript
    const savedLayout = hashLayout || loadSavedLayout();
```

with:

```javascript
    const injectedLayout = configuredLayout ? hydrateLayout(configuredLayout) : null;
    const savedLayout = hashLayout || injectedLayout || loadSavedLayout();
```

- [ ] **Step 4: Make card text configurable**

Replace the first line of `createFlowerNote(stem)`:

```javascript
      const placement = pickNotePlacement(stem);
```

with:

```javascript
      const configured = configuredCards[stem.catalog] || null;
      const placement = configured && Number.isFinite(Number(configured.x)) && Number.isFinite(Number(configured.y))
        ? {
            x: Number(configured.x),
            y: Number(configured.y),
            w: Number(configured.w) || 124,
            h: Number(configured.h) || 38,
            r: Number(configured.r) || 0
          }
        : pickNotePlacement(stem);
```

Replace the returned note object in `createFlowerNote(stem)`:

```javascript
      return {
        id: `note-${stem.uid}`,
        label: item.name,
        title: `给妈妈的${item.name}`,
        text: flowerStories[item.id] || `妈妈，这支${item.name}让我想起很多平凡的小事：你把热汤放到我手边，也把安心放进我每天的生活里。母亲节快乐。`,
        ...placement
      };
```

with:

```javascript
      return {
        id: `note-${stem.uid}`,
        label: configured && configured.label ? configured.label : item.name,
        title: configured && configured.title ? configured.title : `给妈妈的${item.name}`,
        text: configured && configured.text ? configured.text : flowerStories[item.id] || `妈妈，这支${item.name}让我想起很多平凡的小事：你把热汤放到我手边，也把安心放进我每天的生活里。母亲节快乐。`,
        ...placement
      };
```

- [ ] **Step 5: Make injected layout notes survive hydration**

In `hydrateLayout(parsed)`, after `const savedStems = parsed.stems...map((stem) => makeStem(stem));`, add:

```javascript
      savedStems.forEach((stem) => {
        if (!stem.note && configuredCards[stem.catalog]) {
          stem.note = createFlowerNote(stem);
        }
      });
```

- [ ] **Step 6: Add gift copy applier**

Before `renderStems();` near the end of the script, add:

```javascript
    function applyGiftCopy() {
      const recipient = configuredGiftCopy.recipient;
      const message = configuredGiftCopy.message;
      if (!recipient && !message) return;
      document.querySelectorAll(".trophy-plaque span:first-child, .plaque-large-message span:first-child").forEach((element) => {
        if (recipient) element.textContent = recipient;
      });
      document.querySelectorAll(".gift-card .message, .trophy-plaque span:last-child, .plaque-large-message span:last-child").forEach((element) => {
        if (message) element.textContent = message;
      });
    }
```

Then replace:

```javascript
    renderStems();
```

with:

```javascript
    applyGiftCopy();
    renderStems();
```

- [ ] **Step 7: Run runtime hook test**

Run:

```bash
pytest tests/test_bouquet_template_schema.py::test_bouquet_phase3_html_contains_runtime_config_hook -v
```

Expected: PASS.

---

### Task 6: Add browser-load smoke test that checks the final HTML remains viewable

**Files:**
- Modify: `tests/test_bouquet_template_schema.py`

- [ ] **Step 1: Add a Playwright availability helper and smoke test**

Append this test:

```python
def test_bouquet_phase3_generated_html_loads_without_console_errors(tmp_path):
    playwright_available = subprocess.run(
        ["npx", "playwright", "--version"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if playwright_available.returncode != 0:
        pytest.skip("Playwright is not available in this checkout")

    out, _, _ = run_bouquet_builder(tmp_path, sample_phase3_slots())
    script = tmp_path / "check_bouquet_page.mjs"
    script.write_text(
        """
import { chromium } from 'playwright';
const url = process.argv[2];
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
const errors = [];
page.on('console', (message) => {
  if (message.type() === 'error') errors.push(message.text());
});
page.on('pageerror', (error) => errors.push(error.message));
await page.goto(url);
await page.waitForSelector('.bouquet-stage');
await page.waitForSelector('.stem-item');
await page.waitForSelector('.gift-card .message');
const stageBox = await page.locator('.bouquet-stage').boundingBox();
const stemCount = await page.locator('.stem-item').count();
const cardText = await page.locator('.gift-card .message').innerText();
await browser.close();
if (!stageBox || stageBox.width < 250 || stageBox.height < 300) {
  throw new Error('bouquet stage is not visibly sized');
}
if (stemCount < 3) {
  throw new Error(`expected at least 3 stems, found ${stemCount}`);
}
if (!cardText.includes('把今天做成一束可以慢慢看的花')) {
  throw new Error(`gift card text was not applied: ${cardText}`);
}
if (errors.length) {
  throw new Error(errors.join('\n'));
}
""".strip(),
        encoding="utf-8",
    )

    result = subprocess.run(
        ["node", str(script), out.resolve().as_uri()],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert result.returncode == 0
```

Also add `import pytest` near the top of the test file.

- [ ] **Step 2: Run the smoke test**

Run:

```bash
pytest tests/test_bouquet_template_schema.py::test_bouquet_phase3_generated_html_loads_without_console_errors -v
```

Expected: PASS if Playwright is available, SKIP if Playwright is not installed in this checkout. If it fails with console errors, fix the runtime hook before continuing.

---

### Task 7: Document Phase 3 runtime mapping

**Files:**
- Modify: `assets/templates/bouquet/SPEC.md`
- Test: `tests/test_bouquet_template_schema.py`

- [ ] **Step 1: Add failing documentation assertions**

Append these assertions to `test_bouquet_spec_documents_phase2_slot_matching_rules()` or add a new test:

```python
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
```

- [ ] **Step 2: Run the documentation test to verify it fails**

Run:

```bash
pytest tests/test_bouquet_template_schema.py::test_bouquet_spec_documents_phase3_runtime_mapping -v
```

Expected: FAIL because Phase 3 runtime mapping is not documented yet.

- [ ] **Step 3: Add Phase 3 section to SPEC**

Insert this section before `## Build Contract` in `assets/templates/bouquet/SPEC.md`:

```markdown
## Phase 3 Runtime Mapping

`template-source/build.py` reads `filled-slots.json`, normalizes bouquet slots, and injects a single `window.BOUQUET_GIFT_CONFIG` script into the generated `index.html`. The builder does not modify the canonical HTML source; it only reads `template-source/mothers-day-blue-bouquet.html` and writes the requested `--out` file.

Runtime config fields:

- `style` captures `color_palette`, `emotional_tone`, `occasion`, and `recipient_language` from `bouquet_style_direction`.
- `catalog` optionally narrows or extends the flower palette shown in the H5.
- `gemCatalog` optionally narrows or extends the gem palette shown in the H5.
- `layout.stems` seeds the initial draggable flowers.
- `layout.placedGems` seeds the initial freely placed gems.
- `cards` maps flower catalog ids to paper-card label/title/text and optional card positions.
- `giftCopy` sets the visible recipient line and primary gift-card message.

The default H5 remains openable without injected config. When config is present, it overrides only the relevant runtime data and preserves the existing drag, gem placement, note modal, save, and mobile scaling behavior.

Verification for every generated bouquet H5:

```bash
scripts/verify-h5.sh ./gifts/<slug>/index.html
```

Then open the page in a browser or Playwright and check that the page loads, flowers render and can be dragged in edit mode, gems can be added, paper-card chips are readable and movable, card text opens in the modal, the 390x844 mobile viewport is not visually cropped, and the console has no errors.
```

- [ ] **Step 4: Run documentation test**

Run:

```bash
pytest tests/test_bouquet_template_schema.py::test_bouquet_spec_documents_phase3_runtime_mapping -v
```

Expected: PASS.

---

### Task 8: Run full bouquet verification

**Files:**
- No code changes unless verification fails.

- [ ] **Step 1: Run all bouquet schema tests**

Run:

```bash
pytest tests/test_bouquet_template_schema.py -v
```

Expected: all tests PASS, with the Playwright smoke test either PASS or SKIP only if Playwright is unavailable.

- [ ] **Step 2: Generate a sample standalone HTML manually**

Run:

```bash
python3 assets/templates/bouquet/template-source/build.py \
  --slots /tmp/bouquet-filled-slots.json \
  --workdir /tmp/bouquet-work \
  --out /tmp/bouquet-index.html
```

Before running that command, create `/tmp/bouquet-filled-slots.json` with the same structure as `sample_phase3_slots()` from the tests.

Expected: `/tmp/bouquet-index.html` exists and contains `window.BOUQUET_GIFT_CONFIG`.

- [ ] **Step 3: Run static H5 verifier on the sample HTML**

Run:

```bash
scripts/verify-h5.sh /tmp/bouquet-index.html
```

Expected: `Static H5 checks passed`.

- [ ] **Step 4: Open the generated HTML in a browser and verify viewability**

Run a local server:

```bash
python3 -m http.server 4173 --directory /tmp
```

Open:

```text
http://127.0.0.1:4173/bouquet-index.html
```

Check:

- Page opens without a blank screen.
- Bouquet stage is visible and centered.
- At least three configured flowers render.
- Gift card text is readable.
- Paper-card callouts are visible and can open the modal.
- On 390x844 mobile viewport, the bouquet remains visible and not fatally cropped.
- Console has no JavaScript errors.

- [ ] **Step 5: If browser verification cannot be completed**

Do not claim the HTML is fully verified. Report exactly which automated checks passed and which browser/manual checks could not be run.

---

## Self-Review

- Spec coverage: The plan covers builder creation/normalization, canonical read-only policy, flowers, gems, cards, initial layout, color/style metadata, runtime config JSON, staging card output, H5 static verification, and browser viewability.
- Placeholder scan: No `TBD`, `TODO`, or undefined follow-up steps remain.
- Type consistency: Runtime fields are consistently named `style`, `catalog`, `gemCatalog`, `layout`, `cards`, and `giftCopy`; test fixtures and HTML hook use the same names.
