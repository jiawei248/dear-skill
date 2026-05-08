import base64
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "assets/templates/paper-house/template-source/scripts/generate_story_cards_litellm.py"
PNG_BYTES = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
)


def load_generator_module():
    spec = importlib.util.spec_from_file_location("paper_house_story_generator", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules["paper_house_story_generator"] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class StoryCardGeneratorTest(unittest.TestCase):
    def write_prompt_file(self, workdir: Path) -> Path:
        (workdir / "figures").mkdir(parents=True)
        (workdir / "stickers" / "kitchen").mkdir(parents=True)
        (workdir / "figures" / "scene_kitchen.png").write_bytes(PNG_BYTES)
        (workdir / "stickers" / "kitchen" / "4.png").write_bytes(PNG_BYTES)
        prompts = workdir / "story_cards" / "prompts" / "story_card_image_prompts.json"
        prompts.parent.mkdir(parents=True)
        prompts.write_text(
            json.dumps(
                {
                    "cards": [
                        {
                            "id": "kitchen-fridge",
                            "target_output": "story_cards/generated/kitchen-fridge.png",
                            "input_images": [
                                {"path": "figures/scene_kitchen.png", "role": "identity reference"},
                                {"path": "stickers/kitchen/4.png", "role": "hero object"},
                            ],
                            "prompt": "Create a warm handmade story card with blank space.",
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
        return prompts

    def test_auto_provider_falls_back_to_draft_without_api_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            workdir = Path(tmp) / "paper-house-work"
            prompts = self.write_prompt_file(workdir)
            outdir = workdir / "story_cards" / "generated"
            env = os.environ.copy()
            for key in [
                "GEMINI_API_KEY",
                "LITELLM_API_KEY",
                "LITELLM_BASE_URL",
                "OPENROUTER_API_KEY",
            ]:
                env.pop(key, None)

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--prompts",
                    str(prompts),
                    "--workdir",
                    str(workdir),
                    "--outdir",
                    str(outdir),
                    "--provider",
                    "auto",
                    "--force",
                ],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            output = outdir / "kitchen-fridge.png"
            self.assertTrue(output.exists())
            with Image.open(output) as image:
                self.assertEqual(image.size, (1024, 720))
            self.assertIn("draft", result.stdout.lower())

    def test_provider_auto_prefers_gemini_then_litellm_then_openrouter(self):
        module = load_generator_module()
        self.assertEqual(
            module.choose_provider("auto", {"GEMINI_API_KEY": "g"}).name,
            "gemini",
        )
        self.assertEqual(
            module.choose_provider(
                "auto",
                {"LITELLM_API_KEY": "l", "LITELLM_BASE_URL": "https://litellm.example"},
            ).name,
            "litellm",
        )
        self.assertEqual(
            module.choose_provider("auto", {"OPENROUTER_API_KEY": "o"}).name,
            "openrouter",
        )
        self.assertEqual(module.choose_provider("auto", {}).name, "draft")

    def test_default_models_use_best_available_image_models(self):
        module = load_generator_module()
        self.assertEqual(module.default_model_for_provider("gemini"), "gemini-3.1-flash-image-preview")
        self.assertEqual(module.default_model_for_provider("litellm"), "gemini-3.1-flash-image-preview")
        self.assertEqual(module.default_model_for_provider("openrouter"), "google/gemini-3.1-flash-image-preview")
    def test_explicit_provider_requires_matching_api_key(self):
        module = load_generator_module()
        with self.assertRaises(module.StoryCardError):
            module.choose_provider("gemini", {})
        with self.assertRaises(module.StoryCardError):
            module.choose_provider("litellm", {"LITELLM_API_KEY": "key"})
        with self.assertRaises(module.StoryCardError):
            module.choose_provider("openrouter", {})


if __name__ == "__main__":
    unittest.main()
