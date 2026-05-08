#!/usr/bin/env python3
from __future__ import annotations

import random
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "story_cards" / "generated"
RAW = GEN / "raw"
RAW.mkdir(parents=True, exist_ok=True)


def noisy_paper(size: tuple[int, int], color: tuple[int, int, int], seed: int, alpha: int = 238) -> Image.Image:
    rng = random.Random(seed)
    img = Image.new("RGBA", size, (*color, alpha))
    px = img.load()
    for y in range(size[1]):
        for x in range(size[0]):
            n = rng.randint(-5, 5)
            r, g, b, a = px[x, y]
            px[x, y] = (
                max(0, min(255, r + n)),
                max(0, min(255, g + n)),
                max(0, min(255, b + n)),
                a,
            )
    return img.filter(ImageFilter.GaussianBlur(0.12))


def add_patch(base: Image.Image, box: tuple[int, int, int, int], color: tuple[int, int, int], seed: int, angle: float = 0) -> None:
    x, y, w, h = box
    patch = noisy_paper((w, h), color, seed)
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=22, fill=255)
    patch.putalpha(mask.point(lambda v: int(v * 0.98)))
    shadow = Image.new("RGBA", patch.size, (55, 36, 24, 0))
    shadow.putalpha(mask.point(lambda v: min(80, int(v * 0.45))))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    if angle:
        patch = patch.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
        shadow = shadow.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    base.alpha_composite(shadow, (x + 10, y + 12))
    base.alpha_composite(patch, (x, y))


def add_tape(base: Image.Image, center: tuple[int, int], color: tuple[int, int, int], angle: float) -> None:
    strip = Image.new("RGBA", (124, 28), (*color, 150))
    d = ImageDraw.Draw(strip)
    for x in range(0, 140, 18):
        d.line([(x, 0), (x - 10, 28)], fill=(255, 255, 255, 46), width=2)
    strip = strip.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    base.alpha_composite(strip, (center[0] - strip.width // 2, center[1] - strip.height // 2))


def preserve_raw(path: Path) -> Path:
    raw_path = RAW / path.name
    if not raw_path.exists():
        shutil.copy2(path, raw_path)
    return raw_path


def polish_one(name: str, patches: list[tuple[tuple[int, int, int, int], tuple[int, int, int], int, float]], tapes: list[tuple[tuple[int, int], tuple[int, int, int], float]]) -> None:
    out = GEN / name
    src = preserve_raw(out)
    img = Image.open(src).convert("RGBA")
    for patch in patches:
        add_patch(img, *patch)
    for tape in tapes:
        add_tape(img, *tape)
    img.convert("RGB").save(out, quality=94)


def contact_sheet() -> None:
    names = ["kitchen-fridge.png", "rooftop-suitcase.png", "karaoke-camera.png", "couch-chess.png"]
    sheet = Image.new("RGB", (768, 600), "#f5ead7")
    d = ImageDraw.Draw(sheet)
    for i, name in enumerate(names):
        img = Image.open(GEN / name).resize((384, 270), Image.Resampling.LANCZOS)
        x = (i % 2) * 384
        y = (i // 2) * 300
        sheet.paste(img, (x, y))
        d.text((x + 12, y + 276), name.replace(".png", ""), fill=(70, 48, 40))
    sheet.save(GEN / "contact-sheet.jpg", quality=88)


def main() -> None:
    polish_one(
        "kitchen-fridge.png",
        [((526, 70, 430, 508), (247, 231, 205), 11, -2.4), ((562, 486, 416, 210), (250, 235, 213), 12, 1.5)],
        [((570, 82), (224, 172, 118), -11), ((862, 540), (224, 172, 118), 8)],
    )
    polish_one(
        "rooftop-suitcase.png",
        [((724, 50, 238, 530), (229, 238, 245), 21, 0.8)],
        [((748, 74), (176, 199, 220), 8)],
    )
    polish_one(
        "karaoke-camera.png",
        [((426, 548, 424, 112), (248, 233, 238), 31, -1.2), ((702, 562, 244, 96), (250, 232, 240), 32, 1.8)],
        [((555, 548), (233, 164, 196), -6), ((834, 566), (233, 164, 196), 7)],
    )
    polish_one(
        "couch-chess.png",
        [((54, 86, 358, 620), (238, 226, 239), 41, -1.6), ((414, 548, 198, 96), (240, 229, 240), 42, 2.4)],
        [((112, 110), (199, 178, 212), -9), ((508, 552), (199, 178, 212), 9)],
    )
    contact_sheet()


if __name__ == "__main__":
    main()
