import base64
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "assets/templates/paper-house/template-source/build.py"
CANONICAL_HTML = ROOT / "assets/templates/paper-house/template-source/night-four-the-turn.html"
PNG_BYTES = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
)


class PaperHouseBuildTest(unittest.TestCase):
    def test_runtime_build_writes_output_without_modifying_canonical_html(self):
        canonical_before = hashlib.sha256(CANONICAL_HTML.read_bytes()).hexdigest()

        with tempfile.TemporaryDirectory() as tmp:
            workdir = Path(tmp)
            (workdir / "scene-kitchen.png").write_bytes(PNG_BYTES)
            (workdir / "story-kitchen.png").write_bytes(PNG_BYTES)
            slots_path = workdir / "filled-slots.json"
            out_path = workdir / "index.html"
            slots_path.write_text(
                json.dumps(
                    {
                        "rooms": {
                            "kitchen": {
                                "title": "测试厨房",
                                "eyebrow": "今天 · 运行时",
                                "note": "这是一句从 filled-slots.json 注入的房间说明。",
                                "song": {
                                    "title": "Runtime Song",
                                    "artist": "Runtime Artist",
                                    "previewUrl": "https://example.com/runtime.m4a",
                                },
                                "lyrics": ["第一句运行时歌词", "第二句运行时歌词"],
                                "fallWords": ["运行时", "不改模板", "写到输出"],
                            }
                        },
                        "images": {
                            "scene_kitchen": "scene-kitchen.png"
                        },
                        "stories": {
                            "kitchen_4": {
                                "title": "运行时小卡",
                                "kicker": "厨房 / 测试",
                                "text": "这段记忆来自运行时 slots，而不是原始模板。",
                                "image": "story-kitchen.png",
                                "layout": "layout-note",
                                "paper": "#fff5dd",
                                "accent": "#c66a33",
                                "decals": [],
                            }
                        },
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(BUILD_SCRIPT),
                    "--slots",
                    str(slots_path),
                    "--workdir",
                    str(workdir),
                    "--out",
                    str(out_path),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertTrue(out_path.exists())
            output_html = out_path.read_text(encoding="utf-8")
            self.assertIn("测试厨房", output_html)
            self.assertIn("Runtime Song", output_html)
            self.assertIn("第一句运行时歌词", output_html)
            self.assertIn("运行时小卡", output_html)
            self.assertIn("这段记忆来自运行时 slots，而不是原始模板。", output_html)
            self.assertIn("data:image/png;base64," + base64.b64encode(PNG_BYTES).decode("ascii"), output_html)

        canonical_after = hashlib.sha256(CANONICAL_HTML.read_bytes()).hexdigest()
        self.assertEqual(canonical_before, canonical_after)

    def test_template_native_slot_groups_inject_into_html(self):
        canonical_before = hashlib.sha256(CANONICAL_HTML.read_bytes()).hexdigest()

        with tempfile.TemporaryDirectory() as tmp:
            workdir = Path(tmp)
            for name in [
                "kitchen-left.png",
                "kitchen-right.png",
                "kitchen-floor.png",
                "figure-kitchen.png",
                "deco-kitchen-1.png",
                "story-kitchen.png",
            ]:
                (workdir / name).write_bytes(PNG_BYTES)

            slots_path = workdir / "filled-slots.json"
            out_path = workdir / "index.html"
            slots_path.write_text(
                json.dumps(
                    {
                        "scene_theme": {
                            "kitchen": {
                                "theme": "运行时厨房主题",
                                "eyebrow": "五月八日 · 原生 slot",
                                "note": "scene_theme 注入的说明。",
                                "palette": {
                                    "bg": "#111111",
                                    "wall2": "#222222",
                                    "floor": "#333333",
                                    "ink": "#444444",
                                    "accent": "#555555",
                                    "glow": "#666666",
                                    "figureA": "#777777",
                                    "figureB": "#888888",
                                },
                            }
                        },
                        "room_walls_and_floor": {
                            "kitchen": {
                                "wall_left": "kitchen-left.png",
                                "wall_right": "kitchen-right.png",
                                "floor": "kitchen-floor.png",
                            }
                        },
                        "scene_figure_image": {
                            "kitchen": "figure-kitchen.png"
                        },
                        "scene_decorations": {
                            "kitchen": ["deco-kitchen-1.png"]
                        },
                        "scene_hero_items": {
                            "kitchen": {
                                "hotspot_id": "kitchen_4",
                                "item": "teapot",
                                "title": "原生热点标题",
                                "kicker": "厨房 / 茶壶",
                                "text": "scene_hero_items 注入的卡片文字。",
                                "layout": "layout-note",
                                "paper": "#ffeecc",
                                "accent": "#bb6633",
                                "decals": [],
                            }
                        },
                        "story_cards": {
                            "kitchen": "story-kitchen.png"
                        },
                        "scene_song": {
                            "kitchen": {
                                "title": "Native Song",
                                "artist": "Native Artist",
                                "previewUrl": "https://example.com/native.m4a",
                            }
                        },
                        "scene_lyrics": {
                            "kitchen": ["原生歌词第一句", "原生歌词第二句"]
                        },
                        "scene_fall_words": {
                            "kitchen": ["原生词", "完整注入", "模板不变"]
                        },
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(BUILD_SCRIPT),
                    "--slots",
                    str(slots_path),
                    "--workdir",
                    str(workdir),
                    "--out",
                    str(out_path),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            output_html = out_path.read_text(encoding="utf-8")
            self.assertIn("运行时厨房主题", output_html)
            self.assertIn("scene_theme 注入的说明。", output_html)
            self.assertIn("#111111", output_html)
            self.assertIn("Native Song", output_html)
            self.assertIn("原生歌词第一句", output_html)
            self.assertIn("原生词", output_html)
            self.assertIn("原生热点标题", output_html)
            self.assertIn("scene_hero_items 注入的卡片文字。", output_html)
            self.assertIn("teapot", output_html)
            self.assertGreaterEqual(output_html.count("data:image/png;base64," + base64.b64encode(PNG_BYTES).decode("ascii")), 5)

        canonical_after = hashlib.sha256(CANONICAL_HTML.read_bytes()).hexdigest()
        self.assertEqual(canonical_before, canonical_after)

    def test_runtime_build_reports_missing_asset_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            workdir = Path(tmp)
            slots_path = workdir / "filled-slots.json"
            out_path = workdir / "index.html"
            slots_path.write_text(
                json.dumps({"images": {"scene_kitchen": "missing.png"}}),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(BUILD_SCRIPT),
                    "--slots",
                    str(slots_path),
                    "--workdir",
                    str(workdir),
                    "--out",
                    str(out_path),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("asset file does not exist", result.stderr)
            self.assertIn("missing.png", result.stderr)
            self.assertFalse(out_path.exists())
    def test_runtime_build_reports_too_many_decorations_for_existing_layout(self):
        with tempfile.TemporaryDirectory() as tmp:
            workdir = Path(tmp)
            for index in range(7):
                (workdir / f"deco-{index}.png").write_bytes(PNG_BYTES)
            slots_path = workdir / "filled-slots.json"
            out_path = workdir / "index.html"
            slots_path.write_text(
                json.dumps(
                    {"scene_decorations": {"kitchen": [f"deco-{index}.png" for index in range(7)]}},
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(BUILD_SCRIPT),
                    "--slots",
                    str(slots_path),
                    "--workdir",
                    str(workdir),
                    "--out",
                    str(out_path),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("current layout supports at most 6", result.stderr)
            self.assertFalse(out_path.exists())
    def test_standard_paper_house_work_layout_resolves_default_assets(self):
        canonical_before = hashlib.sha256(CANONICAL_HTML.read_bytes()).hexdigest()

        with tempfile.TemporaryDirectory() as tmp:
            gift_dir = Path(tmp) / "2026-05-08-mia"
            workdir = gift_dir / "paper-house-work"
            (workdir / "walls").mkdir(parents=True)
            (workdir / "floors").mkdir(parents=True)
            (workdir / "figures").mkdir(parents=True)
            (workdir / "stickers" / "kitchen").mkdir(parents=True)
            (workdir / "story_cards" / "generated").mkdir(parents=True)
            (workdir / "walls" / "kitchen_left.jpg").write_bytes(PNG_BYTES)
            (workdir / "walls" / "kitchen_right.jpg").write_bytes(PNG_BYTES)
            (workdir / "floors" / "kitchen_floor.jpg").write_bytes(PNG_BYTES)
            (workdir / "figures" / "scene_kitchen.png").write_bytes(PNG_BYTES)
            (workdir / "stickers" / "kitchen" / "1.png").write_bytes(PNG_BYTES)
            (workdir / "story_cards" / "generated" / "kitchen-fridge.png").write_bytes(PNG_BYTES)

            slots_path = workdir / "filled-slots.json"
            out_path = gift_dir / "index.html"
            slots_path.write_text(
                json.dumps(
                    {
                        "room_walls_and_floor": {"kitchen": {}},
                        "scene_figure_image": {"kitchen": {}},
                        "scene_decorations": {"kitchen": [{}]},
                        "story_cards": {"kitchen": {}},
                        "scene_hero_items": {
                            "kitchen": {
                                "title": "默认路径卡片",
                                "text": "这些图片都来自 paper-house-work 标准目录。",
                                "decals": [],
                            }
                        },
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(BUILD_SCRIPT),
                    "--slots",
                    str(slots_path),
                    "--out",
                    str(out_path),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertTrue(out_path.exists())
            output_html = out_path.read_text(encoding="utf-8")
            self.assertIn("默认路径卡片", output_html)
            self.assertIn("这些图片都来自 paper-house-work 标准目录。", output_html)
            encoded_png = base64.b64encode(PNG_BYTES).decode("ascii")
            self.assertGreaterEqual(output_html.count(encoded_png), 6)

        canonical_after = hashlib.sha256(CANONICAL_HTML.read_bytes()).hexdigest()
        self.assertEqual(canonical_before, canonical_after)


if __name__ == "__main__":
    unittest.main()
