# Dossier Folder Template Notes

An interactive skeuomorphic "personnel file" folder on a dark desk background. Click to open reveals a two-page vertical spread with a soft fold crease at the viewport center. Inside: a pile of overlapping document cards (profile, evidence exhibits, message) with CSS-only decorative stationery elements.

It implements a `borrowed-media` + `interactive-object` pattern: the conceit is a confidential file that catalogs what the person has done and who they are, presented as physical artifacts in a folder.

## Reference Use

Treat as reference. the skill should change ALL text content, profile fields, evidence cards, tags, photos, and decorative details. The core idea: a "being seen" gift disguised as an official dossier — someone cataloged your quiet impact and filed it as evidence.

## What To Change Per Use

- document.title
- File number and cover title/subtitle
- Profile name, fields (Type/Role/Trait/Risk/Class), and persona tags
- All evidence card content (EXH-A/B/C text, sticky note comments)
- Bottom message text
- Profile photo (generate Q-version/chibi or stylized portrait, compress to ~20KB JPEG base64)
- Polaroid landscape photo (generate ins-aesthetic scene, compress to ~12KB JPEG base64)
- Polaroid caption
- Cassette tape label text
- Floppy disk label text
- Stamp text (VERIFIED → could be CLASSIFIED, APPROVED, etc.)
- Star sticker colors (currently gold/silver/coffee — could match any palette)
- Dog sign text and emoji

## What Not To Copy Blindly

- the exact evidence card content (these are specific to one user)
- the exact profile fields and tags
- the INTJ-A type (personalize to actual user)
- the specific file number 0428

## Best Fit

- "being seen" gifts — cataloging someone's quiet impact
- personality profile / character study gifts
- achievement or milestone showcases
- "evidence of your awesomeness" concept
- professional appreciation wrapped in playful format
- birthday or anniversary "file on you"

## Watch Outs

- Base64 photos: keep profile photo ≤25KB, polaroid ≤15KB after JPEG compression. Larger images bloat the single HTML file.
- DO NOT use regex to replace base64 strings — it will corrupt the HTML. Use exact string matching (find the old base64, splice in the new one).
- The closed folder is 500px tall, designed for 720px wide viewport. Test vertical centering.
- Card pile min-height is 540px — if adding more cards, increase this.
- Cassette and floppy are CSS-only (no images needed), but they have many nested divs — don't accidentally delete inner elements.
- The fold crease uses multi-layer gradients, not a hard line. Don't simplify it.
- Star stickers use inline SVG — keep opacity at 0.6, vary sizes 14-36px.

## Delivery Note

Single HTML file. Google Fonts CDN (Caveat, Special Elite, Courier Prime, Inter). All images inline as base64. Deploy via surge.sh or deliver as file.
