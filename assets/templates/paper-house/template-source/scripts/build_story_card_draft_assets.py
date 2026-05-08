#!/usr/bin/env python3
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "story_cards" / "drafts"
OUT.mkdir(parents=True, exist_ok=True)


def load(path: str) -> Image.Image:
    return Image.open(ROOT / path).convert("RGBA")


def fit(path: str, size: tuple[int, int]) -> Image.Image:
    return ImageOps.fit(load(path), size, method=Image.Resampling.LANCZOS)


def paper(size: tuple[int, int], base: str, seed: int) -> Image.Image:
    rng = random.Random(seed)
    img = Image.new("RGBA", size, base)
    px = img.load()
    for y in range(size[1]):
        for x in range(size[0]):
            n = rng.randint(-7, 7)
            r, g, b, a = px[x, y]
            px[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n)), max(0, min(255, b + n)), a)
    return img.filter(ImageFilter.GaussianBlur(0.18))


def shadow(img: Image.Image, blur: int = 18, alpha: int = 95) -> Image.Image:
    a = img.getchannel("A")
    sh = Image.new("RGBA", img.size, (40, 24, 20, 0))
    sh.putalpha(a.point(lambda v: min(alpha, v)))
    return sh.filter(ImageFilter.GaussianBlur(blur))


def paste_center(base: Image.Image, layer: Image.Image, xy: tuple[int, int], scale: float = 1, angle: float = 0, sh: bool = True) -> None:
    w = max(1, int(layer.width * scale))
    h = max(1, int(layer.height * scale))
    layer = layer.resize((w, h), Image.Resampling.LANCZOS)
    if angle:
        layer = layer.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    x = int(xy[0] - layer.width / 2)
    y = int(xy[1] - layer.height / 2)
    if sh:
        base.alpha_composite(shadow(layer), (x + 8, y + 10))
    base.alpha_composite(layer, (x, y))


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=255)
    return mask


def photo(path: str, size: tuple[int, int], radius: int = 28) -> Image.Image:
    im = fit(path, size)
    im.putalpha(rounded_mask(size, radius))
    frame = Image.new("RGBA", (size[0] + 34, size[1] + 46), (255, 250, 240, 255))
    frame.alpha_composite(im, (17, 16))
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle([0, 0, frame.width - 1, frame.height - 1], radius=radius + 8, outline=(126, 94, 72, 42), width=2)
    return frame


def tape(base: Image.Image, xy: tuple[int, int], size=(112, 28), angle=-8, color=(245, 218, 168, 160)) -> None:
    strip = Image.new("RGBA", size, color)
    d = ImageDraw.Draw(strip)
    for x in range(0, size[0], 16):
        d.line([(x, 0), (x - 10, size[1])], fill=(255, 255, 255, 42), width=2)
    strip = strip.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    base.alpha_composite(strip, (int(xy[0] - strip.width / 2), int(xy[1] - strip.height / 2)))


def label_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for rel in ["fonts/我爱万伟伟手写体.ttf", "fonts/荷塘月色手写体+Regular.ttf"]:
        try:
            return ImageFont.truetype(str(ROOT / rel), size=size)
        except Exception:
            pass
    return ImageFont.load_default()


def hand_label(base: Image.Image, text: str, xy: tuple[int, int], color=(96, 66, 54, 210), size=32, angle=-3) -> None:
    font = label_font(size)
    tmp = Image.new("RGBA", (360, 80), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    d.text((10, 8), text, font=font, fill=color)
    tmp = tmp.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    base.alpha_composite(tmp, xy)


def paste_camera_with_photo(base: Image.Image, center: tuple[int, int], scale: float, angle: float) -> None:
    """The CCD sticker is a frame, so put a tiny photo behind its screen."""
    inside = photo("scene_karaoke_2.jpg", (172, 112), 12)
    inside = inside.resize((int(inside.width * scale * 0.92), int(inside.height * scale * 0.92)), Image.Resampling.LANCZOS)
    inside = inside.rotate(angle - 1, expand=True, resample=Image.Resampling.BICUBIC)
    base.alpha_composite(shadow(inside, 10, 55), (int(center[0] - 100 * scale), int(center[1] - 62 * scale)))
    base.alpha_composite(inside, (int(center[0] - 106 * scale), int(center[1] - 72 * scale)))
    paste_center(base, load("karaoke/3.png"), center, scale, angle)


def kitchen() -> None:
    base = paper((1024, 720), "#f4dfbf", 11)
    bg = fit("kitchen_right.jpg", (770, 620)).filter(ImageFilter.GaussianBlur(0.25))
    bg.putalpha(rounded_mask(bg.size, 34))
    base.alpha_composite(shadow(bg, 20, 70), (65, 42))
    base.alpha_composite(bg, (56, 32))
    paste_center(base, load("kitchen/4.png"), (805, 405), 0.58, 0)
    paste_center(base, load("scene_kitchen.png"), (455, 420), 0.52, 0)
    paste_center(base, load("stickers/food/sticker_28.png"), (214, 600), 0.28, -10)
    paste_center(base, load("stickers/food/sticker_25.png"), (830, 145), 0.42, 7)
    paste_center(base, load("stickers/decorations/sticker_142.png"), (690, 640), 0.44, 4)
    tape(base, (168, 70), angle=-6)
    tape(base, (765, 64), angle=7)
    hand_label(base, "fridge notes", (94, 80), size=30)
    base.save(OUT / "kitchen-fridge-draft.png")


def rooftop() -> None:
    base = paper((1024, 720), "#e5edf3", 22)
    p = photo("rooftop_right.jpg", (500, 610), 30).rotate(-3, expand=True, resample=Image.Resampling.BICUBIC)
    base.alpha_composite(shadow(p, 22, 75), (42, 40))
    base.alpha_composite(p, (34, 28))
    paste_center(base, load("scene_rooftop.png"), (390, 440), 0.45, 0)
    paste_center(base, load("rooftop/1.png"), (642, 474), 0.52, 4)
    paste_center(base, load("stickers/decorations/sticker_103.png"), (775, 152), 0.64, 6)
    paste_center(base, load("stickers/decorations/sticker_104.png"), (860, 278), 0.8, 12, sh=False)
    paste_center(base, load("stickers/decorations/sticker_113.png"), (780, 600), 0.48, -10)
    tape(base, (470, 72), angle=8, color=(195, 218, 235, 170))
    hand_label(base, "rainy tickets", (650, 82), color=(62, 84, 118, 220), size=30, angle=4)
    base.save(OUT / "rooftop-suitcase-draft.png")


def karaoke() -> None:
    base = paper((1024, 720), "#f6dce9", 33)
    left = photo("karaoke_right.jpg", (455, 500), 26).rotate(4, expand=True, resample=Image.Resampling.BICUBIC)
    right = photo("scene_karaoke_1.jpg", (455, 500), 26).rotate(-4, expand=True, resample=Image.Resampling.BICUBIC)
    base.alpha_composite(shadow(left, 18, 65), (66, 70))
    base.alpha_composite(left, (55, 58))
    base.alpha_composite(shadow(right, 18, 65), (430, 75))
    base.alpha_composite(right, (420, 62))
    paste_camera_with_photo(base, (330, 536), 0.48, -5)
    paste_center(base, load("stickers/household_goods/sticker_75.png"), (778, 556), 0.42, 10)
    paste_center(base, load("stickers/decorations/sticker_161.png"), (160, 176), 0.7, -6, sh=False)
    paste_center(base, load("stickers/decorations/sticker_145.png"), (860, 155), 0.46, 6)
    tape(base, (512, 52), angle=-3, color=(244, 190, 214, 170))
    hand_label(base, "one more song", (402, 596), color=(129, 57, 96, 225), size=32, angle=-4)
    base.save(OUT / "karaoke-camera-draft.png")


def couch() -> None:
    base = paper((1024, 720), "#ece3f0", 44)
    bg = fit("couch_right.jpg", (620, 540))
    bg.putalpha(rounded_mask(bg.size, 32))
    base.alpha_composite(shadow(bg, 22, 75), (300, 56))
    base.alpha_composite(bg, (288, 46))
    paste_center(base, load("scene_couch.png"), (500, 454), 0.48, 0)
    paste_center(base, load("couch/6.png"), (610, 586), 0.42, 7)
    paste_center(base, load("stickers/decorations/sticker_102.png"), (216, 186), 0.58, -6)
    paste_center(base, load("stickers/decorations/sticker_130.png"), (176, 560), 0.42, 9)
    paste_center(base, load("stickers/decorations/sticker_149.png"), (826, 158), 0.5, -7)
    paste_center(base, load("stickers/decorations/sticker_142.png"), (812, 620), 0.5, 5)
    tape(base, (676, 66), angle=7, color=(214, 196, 229, 170))
    hand_label(base, "quiet evening", (86, 78), color=(86, 62, 98, 220), size=32, angle=-4)
    base.save(OUT / "couch-chess-draft.png")


def main() -> None:
    kitchen()
    rooftop()
    karaoke()
    couch()
    print(OUT)


if __name__ == "__main__":
    main()
