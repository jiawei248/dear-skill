#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import io
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests
from PIL import Image, ImageDraw, ImageOps


ROOT = Path(__file__).resolve().parents[1]
TARGET_SIZE = (1024, 720)
DEFAULT_PROMPTS = ROOT / "story_cards" / "prompts" / "story_card_image_prompts.json"
DEFAULT_OUTDIR = ROOT / "story_cards" / "generated"


class StoryCardError(Exception):
    pass


@dataclass(frozen=True)
class ProviderConfig:
    name: str
    model: str
    base_url: str | None = None
    api_key: str | None = None


def default_model_for_provider(provider: str) -> str:
    if provider == "gemini":
        return os.environ.get("GEMINI_IMAGE_MODEL", "gemini-3.1-flash-image-preview")
    if provider == "litellm":
        return os.environ.get("LITELLM_IMAGE_MODEL", "gemini-3.1-flash-image-preview")
    if provider == "openrouter":
        return os.environ.get("OPENROUTER_IMAGE_MODEL", "google/gemini-3.1-flash-image-preview")
    if provider == "draft":
        return "draft"
    raise StoryCardError(f"unknown provider: {provider}")


def choose_provider(provider: str, env: dict[str, str] | None = None) -> ProviderConfig:
    env = env or os.environ
    if provider == "auto":
        if env.get("GEMINI_API_KEY"):
            provider = "gemini"
        elif env.get("LITELLM_API_KEY") and env.get("LITELLM_BASE_URL"):
            provider = "litellm"
        elif env.get("OPENROUTER_API_KEY"):
            provider = "openrouter"
        else:
            provider = "draft"

    if provider == "gemini":
        api_key = env.get("GEMINI_API_KEY")
        if not api_key:
            raise StoryCardError("GEMINI_API_KEY is required for --provider gemini")
        return ProviderConfig("gemini", default_model_for_provider("gemini"), api_key=api_key)
    if provider == "litellm":
        api_key = env.get("LITELLM_API_KEY")
        base_url = env.get("LITELLM_BASE_URL")
        if not api_key or not base_url:
            raise StoryCardError("LITELLM_API_KEY and LITELLM_BASE_URL are required for --provider litellm")
        return ProviderConfig("litellm", default_model_for_provider("litellm"), base_url=base_url.rstrip("/"), api_key=api_key)
    if provider == "openrouter":
        api_key = env.get("OPENROUTER_API_KEY")
        if not api_key:
            raise StoryCardError("OPENROUTER_API_KEY is required for --provider openrouter")
        base_url = env.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").rstrip("/")
        return ProviderConfig("openrouter", default_model_for_provider("openrouter"), base_url=base_url, api_key=api_key)
    if provider == "draft":
        return ProviderConfig("draft", default_model_for_provider("draft"))
    raise StoryCardError(f"unknown provider: {provider}")


def resolve_path(path: str, workdir: Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return workdir / candidate


def data_url(path: Path, max_dim: int = 820) -> str:
    if not path.exists():
        raise StoryCardError(f"input image does not exist: {path}")
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


def load_cards(prompts_path: Path) -> list[dict[str, Any]]:
    payload = json.loads(prompts_path.read_text(encoding="utf-8"))
    cards = payload.get("cards") if isinstance(payload, dict) else None
    if not isinstance(cards, list) or not cards:
        raise StoryCardError(f"prompt file must contain a non-empty cards array: {prompts_path}")
    for card in cards:
        if not isinstance(card, dict):
            raise StoryCardError("each card entry must be an object")
        if not card.get("id"):
            raise StoryCardError("each card entry must include id")
        if not card.get("prompt"):
            raise StoryCardError(f"card {card.get('id')} must include prompt")
    return cards


def extract_image_b64(payload: dict[str, Any]) -> str:
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
    content = message.get("content")
    if isinstance(content, list):
        for part in content:
            image_url = part.get("image_url", {}) if isinstance(part, dict) else {}
            url = image_url.get("url", "")
            if url.startswith("data:image"):
                return url.split(",", 1)[1]
    raise StoryCardError("No image payload returned from image provider response.")


def normalize_image(raw: bytes) -> Image.Image:
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    return ImageOps.fit(img, TARGET_SIZE, method=Image.Resampling.LANCZOS, centering=(0.5, 0.47))


def request_openai_compatible_card(config: ProviderConfig, card: dict[str, Any], workdir: Path, verify_tls: bool) -> bytes:
    content: list[dict[str, Any]] = [{"type": "text", "text": card["prompt"].strip()}]
    for image in card.get("input_images", []):
        rel_path = image.get("path")
        if not rel_path:
            continue
        role = image.get("role", "reference image")
        content.append({"type": "text", "text": f"Reference image role: {role}."})
        content.append({"type": "image_url", "image_url": {"url": data_url(resolve_path(rel_path, workdir))}})

    body = {
        "model": config.model,
        "messages": [{"role": "user", "content": content}],
    }
    response = requests.post(
        f"{config.base_url}/v1/chat/completions",
        headers={"Authorization": f"Bearer {config.api_key}"},
        json=body,
        timeout=240,
        verify=verify_tls,
    )
    if response.status_code >= 400:
        raise StoryCardError(f"{card['id']} failed: {response.status_code} {response.text[:800]}")
    return base64.b64decode(extract_image_b64(response.json()))


def gemini_part_from_path(path: Path) -> dict[str, Any]:
    uri = data_url(path)
    header, encoded = uri.split(",", 1)
    mime = header.split(";", 1)[0].removeprefix("data:")
    return {"inline_data": {"mime_type": mime, "data": encoded}}


def request_gemini_card(config: ProviderConfig, card: dict[str, Any], workdir: Path, verify_tls: bool) -> bytes:
    parts: list[dict[str, Any]] = [{"text": card["prompt"].strip()}]
    for image in card.get("input_images", []):
        rel_path = image.get("path")
        if not rel_path:
            continue
        role = image.get("role", "reference image")
        parts.append({"text": f"Reference image role: {role}."})
        parts.append(gemini_part_from_path(resolve_path(rel_path, workdir)))

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{config.model}:generateContent"
    response = requests.post(
        url,
        params={"key": config.api_key},
        json={"contents": [{"role": "user", "parts": parts}]},
        timeout=240,
        verify=verify_tls,
    )
    if response.status_code >= 400:
        raise StoryCardError(f"{card['id']} failed: {response.status_code} {response.text[:800]}")
    payload = response.json()
    for candidate in payload.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            inline_data = part.get("inlineData") or part.get("inline_data")
            if inline_data and inline_data.get("data"):
                return base64.b64decode(inline_data["data"])
    raise StoryCardError("No image payload returned from Gemini response.")


def make_draft_card(card: dict[str, Any]) -> Image.Image:
    img = Image.new("RGB", TARGET_SIZE, "#f5ead7")
    draw = ImageDraw.Draw(img)
    draw.rectangle((28, 28, TARGET_SIZE[0] - 28, TARGET_SIZE[1] - 28), outline="#d6b98f", width=4)
    draw.rectangle((72, 86, 626, 590), fill="#ead3ad", outline="#c9a978", width=3)
    draw.rectangle((668, 118, 940, 558), fill="#fff7e9", outline="#d6b98f", width=2)
    draw.text((96, 112), "draft story card", fill="#6d4b30")
    draw.text((96, 152), str(card["id"]), fill="#6d4b30")
    draw.text((696, 146), "image provider", fill="#8a6742")
    draw.text((696, 178), "not configured", fill="#8a6742")
    return img


def generate_card(config: ProviderConfig, card: dict[str, Any], workdir: Path, verify_tls: bool) -> Image.Image:
    if config.name == "draft":
        return make_draft_card(card)
    if config.name == "gemini":
        return normalize_image(request_gemini_card(config, card, workdir, verify_tls))
    return normalize_image(request_openai_compatible_card(config, card, workdir, verify_tls))


def output_path_for_card(card: dict[str, Any], workdir: Path, outdir: Path) -> Path:
    target = card.get("target_output")
    if target:
        path = Path(target)
        if path.is_absolute():
            return path
        try:
            return resolve_path(target, workdir)
        except StoryCardError:
            pass
    return outdir / f"{card['id']}.png"


def save_contact_sheet(cards: list[dict[str, Any]], out_paths: list[Path], outdir: Path) -> None:
    thumbs = []
    for card, path in zip(cards, out_paths):
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
        ImageDraw.Draw(sheet).text((x + 12, y + 276), label, fill=(70, 48, 40))
    outdir.mkdir(parents=True, exist_ok=True)
    sheet.save(outdir / "contact-sheet.jpg", quality=88)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompts", type=Path, default=DEFAULT_PROMPTS)
    parser.add_argument("--workdir", type=Path, default=ROOT)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--provider", choices=["auto", "gemini", "litellm", "openrouter", "draft"], default="auto")
    parser.add_argument("--only")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--insecure-skip-verify", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workdir = args.workdir.resolve()
    outdir = args.outdir.resolve()
    try:
        cards = load_cards(args.prompts.resolve())
        if args.only:
            cards = [card for card in cards if card["id"] == args.only]
            if not cards:
                raise StoryCardError(f"card id not found in prompt file: {args.only}")
        config = choose_provider(args.provider)
    except StoryCardError as exc:
        print(f"story-card generation error: {exc}", flush=True)
        return 1

    out_paths: list[Path] = []
    verify_tls = not args.insecure_skip_verify
    for card in cards:
        out_path = output_path_for_card(card, workdir, outdir)
        out_paths.append(out_path)
        if out_path.exists() and not args.force:
            print(f"skip {out_path}")
            continue
        out_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"generating {card['id']} with {config.name}:{config.model}...")
        started = time.time()
        try:
            image = generate_card(config, card, workdir, verify_tls)
        except Exception as exc:
            if args.strict:
                print(f"story-card generation error: {exc}", flush=True)
                return 1
            print(f"provider failed for {card['id']}; writing draft fallback: {exc}")
            image = make_draft_card(card)
        image.save(out_path)
        print(f"wrote {out_path} in {time.time() - started:.1f}s")

    save_contact_sheet(cards, out_paths, outdir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
