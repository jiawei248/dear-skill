#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import sys
import unicodedata
from io import BytesIO
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageOps
from rembg import new_session, remove


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}


def safe_name(path: Path, index: int) -> str:
    stem = unicodedata.normalize("NFKC", path.stem)
    stem = re.sub(r"[^\w\u4e00-\u9fff.-]+", "_", stem, flags=re.UNICODE)
    stem = re.sub(r"_+", "_", stem).strip("._-")
    if not stem:
        stem = f"sticker_{index:03d}"
    return f"{index:03d}_{stem[:70]}.png"


def soft_clean_alpha(img: Image.Image, threshold: int = 8) -> Image.Image:
    arr = np.array(img.convert("RGBA"))
    alpha = arr[:, :, 3]

    alpha[alpha < threshold] = 0

    if np.any(alpha):
        mask = (alpha > 0).astype(np.uint8) * 255
        kernel = np.ones((2, 2), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        mask = cv2.GaussianBlur(mask, (0, 0), sigmaX=0.45)
        arr[:, :, 3] = np.minimum(alpha, mask)
    else:
        arr[:, :, 3] = alpha

    return Image.fromarray(arr, "RGBA")


def trim_transparent(img: Image.Image, padding: int = 12) -> Image.Image:
    arr = np.array(img.convert("RGBA"))
    alpha = arr[:, :, 3]
    ys, xs = np.where(alpha > 4)
    if len(xs) == 0 or len(ys) == 0:
        return img

    left = max(int(xs.min()) - padding, 0)
    right = min(int(xs.max()) + padding + 1, img.width)
    top = max(int(ys.min()) - padding, 0)
    bottom = min(int(ys.max()) + padding + 1, img.height)
    return img.crop((left, top, right, bottom))


def remove_background(src: Path, session) -> Image.Image:
    with Image.open(src) as raw:
        image = ImageOps.exif_transpose(raw).convert("RGBA")
        buf = BytesIO()
        image.save(buf, format="PNG")

    cut = remove(
        buf.getvalue(),
        session=session,
        alpha_matting=True,
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=10,
        alpha_matting_erode_size=8,
        post_process_mask=True,
    )
    return Image.open(BytesIO(cut)).convert("RGBA")


def process_one(src: Path, dest: Path, session) -> tuple[bool, str]:
    try:
        cutout = remove_background(src, session)
        cutout = soft_clean_alpha(cutout)
        cutout = trim_transparent(cutout)
        dest.parent.mkdir(parents=True, exist_ok=True)
        cutout.save(dest, "PNG", optimize=True)
        return True, ""
    except Exception as exc:  # keep the batch moving; report failed files at the end
        return False, f"{src.name}: {exc}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Batch remove sticker backgrounds with rembg.")
    parser.add_argument("--input", default="stickers/new")
    parser.add_argument("--output", default="stickers/new_cutout_png")
    parser.add_argument("--model", default="isnet-general-use")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    in_dir = (root / args.input).resolve()
    out_dir = (root / args.output).resolve()
    models_dir = root / ".rembg-models"
    os.environ.setdefault("U2NET_HOME", str(models_dir))

    files = sorted(p for p in in_dir.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS)
    if not files:
        print(f"No images found in {in_dir}", file=sys.stderr)
        return 1

    out_dir.mkdir(parents=True, exist_ok=True)
    session = new_session(args.model)

    failures: list[str] = []
    for idx, src in enumerate(files, start=1):
        dest = out_dir / safe_name(src, idx)
        ok, error = process_one(src, dest, session)
        status = "ok" if ok else "fail"
        print(f"[{idx:03d}/{len(files):03d}] {status} {src.name} -> {dest.name}", flush=True)
        if error:
            failures.append(error)

    if failures:
        fail_log = out_dir / "_failed.txt"
        fail_log.write_text("\n".join(failures), encoding="utf-8")
        print(f"\nFinished with {len(failures)} failures. See {fail_log}")
        return 2

    print(f"\nFinished. Wrote {len(files)} PNG cutouts to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
