#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import io
import json
import re
import shutil
import time
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

import requests
import urllib3
from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
DOCX = Path("/Users/liujiawei/Desktop/资源交付.docx")
OUT = ROOT / "story_cards" / "generated"
OUT.mkdir(parents=True, exist_ok=True)

MODEL = "gemini-3.1-flash-image-preview"
TARGET_SIZE = (1024, 720)
W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"


def litellm_config() -> tuple[str, str]:
    root = ET.fromstring(zipfile.ZipFile(DOCX).read("word/document.xml"))
    texts = [el.text or "" for el in root.iter(W_NS)]
    base_url = texts[texts.index("BaseUrl：") + 1].rstrip("/")
    key_line = next(text for text in texts if text.startswith("Api key"))
    api_key = re.split("[：:]", key_line, 1)[1].strip()
    return base_url, api_key


def data_url(rel_path: str, max_dim: int = 820) -> str:
    path = ROOT / rel_path
    img = Image.open(path).convert("RGBA")
    if max(img.size) > max_dim:
        img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)

    has_alpha = img.getchannel("A").getextrema()[0] < 255
    buf = io.BytesIO()
    if has_alpha:
        img.save(buf, format="PNG", optimize=True)
        mime = "image/png"
    else:
        img.convert("RGB").save(buf, format="JPEG", quality=86, optimize=True)
        mime = "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(buf.getvalue()).decode('ascii')}"


def extract_image_b64(payload: dict) -> str:
    if payload.get("data"):
        item = payload["data"][0]
        if item.get("b64_json"):
            return item["b64_json"]
        url = item.get("url")
        if isinstance(url, str) and url.startswith("data:image"):
            return url.split(",", 1)[1]

    message = payload.get("choices", [{}])[0].get("message", {})
    for image in message.get("images", []):
        url = image.get("image_url", {}).get("url", "")
        if url.startswith("data:image"):
            return url.split(",", 1)[1]
    raise RuntimeError("No image payload returned from litellm response.")


def normalize_image(raw: bytes) -> Image.Image:
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    return ImageOps.fit(img, TARGET_SIZE, method=Image.Resampling.LANCZOS, centering=(0.5, 0.47))


def save_contact_sheet(cards: list[dict]) -> None:
    thumbs = []
    for card in cards:
        path = OUT / f"{card['id']}.png"
        if path.exists():
            thumbs.append((card["id"], Image.open(path).resize((384, 270), Image.Resampling.LANCZOS)))
    if not thumbs:
        return
    rows = (len(thumbs) + 1) // 2
    sheet = Image.new("RGB", (768, rows * 304), "#f5ead7")
    for i, (label, thumb) in enumerate(thumbs):
        x = (i % 2) * 384
        y = (i // 2) * 304
        sheet.paste(thumb, (x, y))
        # Pillow's default font is enough for this private contact sheet.
        Image.Image.getbbox
        from PIL import ImageDraw

        ImageDraw.Draw(sheet).text((x + 12, y + 276), label, fill=(70, 48, 40))
    sheet.save(OUT / "contact-sheet.jpg", quality=88)


CARDS = [
    {
        "id": "kitchen-fridge",
        "images": [
            ("ref_boy.jpg", "boyfriend identity reference"),
            ("ref_girl.jpg", "girlfriend identity reference"),
            ("scene_kitchen.jpg", "warm orange kitchen room mood"),
            ("kitchen/4.png", "cream fridge sticker, main object"),
            ("stickers/food/sticker_25.png", "heart cookie sticker accent"),
        ],
        "prompt": """
Use case: identity-preserve, compositing.
Create a real AI-generated handmade Instagram-style romantic story card image.
Use the first two images only as identity references for the boyfriend and girlfriend; keep their faces, age, and gentle couple feeling recognizable, but do not paste the reference photos flatly.
Scene: a cozy warm orange kitchen. The couple is beside a cream vintage fridge and the girlfriend is opening the main fridge door while the boyfriend smiles as if he found her little secret. The fridge door must obey real-world physics: one single solid door panel, hinged on one vertical edge of the fridge body, swung open outward about 60 degrees. The hinge side must remain attached to the main fridge cabinet. Do not create a folded door, split door, detached panel, accordion door, or two overlapping fridge doors. If the open door is hard, show it only slightly ajar but physically attached.
Inside the fridge are a small cake, a drink, and one tiny blank paper slip. The paper slip must be blank with no readable writing.
Key object: the cream fridge from the reference sticker.
Style: tactile scrapbook photo collage, soft paper grain, washi tape, warm kitchen light, subtle sticker accents, handmade but still photographic and scene-based.
Composition: left image-heavy scene with generous blank paper space on the right and lower edge for a handwritten Chinese note overlay.
Avoid: any readable generated text, letters, captions, handwriting, brand names, watermark, logo, extra people, empty frames, stiff studio portrait, impossible fridge door geometry.
""",
    },
    {
        "id": "rooftop-suitcase",
        "images": [
            ("ref_boy.jpg", "boyfriend identity reference"),
            ("ref_girl.jpg", "girlfriend identity reference"),
            ("scene_rooftop.jpg", "rainy rooftop room mood"),
            ("rooftop/1.png", "blue suitcase sticker, main object"),
            ("stickers/decorations/sticker_103.png", "travel ticket sticker accent"),
        ],
        "prompt": """
Use case: identity-preserve, compositing.
Create a real AI-generated handmade Instagram-style romantic story card image.
Use the first two images only as identity references for the boyfriend and girlfriend; keep them recognizable and natural.
Scene: after-rain rooftop at night, the couple is sharing one umbrella beside blue suitcases, as if they are leaving on a tiny spontaneous trip. A travel ticket and ribbon-like scrapbook details sit around the scene.
Key object: the blue suitcases from the reference sticker.
Style: cool blue-gray paper collage, tender rain glow, instant-photo border, handmade tape and soft shadows, romantic but not fantasy.
Composition: clear left-right layout, the couple and suitcase on the left, airy blank paper note space on the right.
Avoid: readable generated text, watermark, logo, extra people, empty frames.
""",
    },
    {
        "id": "karaoke-camera",
        "images": [
            ("ref_boy.jpg", "boyfriend identity reference"),
            ("ref_girl.jpg", "girlfriend identity reference"),
            ("scene_karaoke_1.jpg", "pink karaoke room mood"),
            ("scene_karaoke_2.jpg", "small photo to appear inside the camera screen"),
            ("karaoke/3.png", "CCD camera frame sticker, must contain a visible little photo inside"),
            ("stickers/household_goods/sticker_75.png", "pink camera sticker accent"),
        ],
        "prompt": """
Use case: identity-preserve, compositing.
Create a real AI-generated handmade Instagram-style romantic story card image.
Use the first two images only as identity references for the boyfriend and girlfriend; keep them recognizable, smiling, and candid.
Scene: playful pink karaoke room. The couple is holding microphones and laughing mid-song, like a candid snapshot from a night out.
Key object: the CCD camera frame sticker. Important: it must not be empty; put a tiny visible photo of the couple or karaoke scene inside its screen, like the camera is displaying the captured moment.
Add the pink camera sticker as a small supporting scrapbook element.
Style: lively Instagram scrapbook, instant-photo layers, paper grain, washi tape, music-night warmth.
Composition: asymmetrical diagonal layout with the main scene and camera frame overlapping, plus a clean blank paper area for handwritten Chinese note overlay.
Avoid: readable generated text, watermark, logo, extra people, empty camera screen, standalone empty frame.
""",
    },
    {
        "id": "couch-chess",
        "images": [
            ("ref_boy.jpg", "boyfriend identity reference"),
            ("ref_girl.jpg", "girlfriend identity reference"),
            ("scene_couch.jpg", "soft lavender sofa room mood"),
            ("couch/6.png", "chessboard sticker, main object"),
            ("stickers/decorations/sticker_102.png", "notebook sticker accent"),
        ],
        "prompt": """
Use case: identity-preserve, compositing.
Create a real AI-generated handmade Instagram-style romantic story card image.
Use the first two images only as identity references for the boyfriend and girlfriend; keep them recognizable and gentle.
Scene: quiet sofa-room evening in a lavender-toned room. The couple sits close together with a chessboard between them; the boyfriend is explaining one move and the girlfriend is smiling at him more than at the board.
Key object: the chessboard from the reference sticker.
Style: cozy lamplight, soft paper collage, notebook and stamp-like scrapbook accents, tactile handmade Instagram mood.
Composition: triangular collage layout, image cluster on the right and lower area, generous blank note space on the left.
Avoid: readable generated text, watermark, logo, extra people, empty frames.
""",
    },
]


def request_card(base_url: str, api_key: str, card: dict) -> bytes:
    content = [{"type": "text", "text": card["prompt"].strip()}]
    for rel_path, role in card["images"]:
        content.append({"type": "text", "text": f"Reference image role: {role}."})
        content.append({"type": "image_url", "image_url": {"url": data_url(rel_path)}})

    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": content}],
    }
    response = requests.post(
        f"{base_url}/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json=body,
        timeout=240,
        verify=False,
    )
    if response.status_code >= 400:
        raise RuntimeError(f"{card['id']} failed: {response.status_code} {response.text[:800]}")
    image_b64 = extract_image_b64(response.json())
    return base64.b64decode(image_b64)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=[card["id"] for card in CARDS])
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    base_url, api_key = litellm_config()
    cards = [card for card in CARDS if args.only in (None, card["id"])]

    for card in cards:
        out_path = OUT / f"{card['id']}.png"
        if out_path.exists() and not args.force:
            print(f"skip {out_path}")
            continue
        print(f"generating {card['id']} with {MODEL}...")
        started = time.time()
        raw = request_card(base_url, api_key, card)
        normalized = normalize_image(raw)
        normalized.save(out_path)
        raw_dir = OUT / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        normalized.save(raw_dir / out_path.name)
        print(f"wrote {out_path} in {time.time() - started:.1f}s")

    save_contact_sheet(CARDS)


if __name__ == "__main__":
    main()
