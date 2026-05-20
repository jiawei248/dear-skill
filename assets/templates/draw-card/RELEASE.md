# draw-card Asset Bundle Release

The runtime bundle is intentionally not committed to the repo. It is published as a GitHub Release asset and fetched on first use by:

```bash
scripts/fetch-asset-bundle.sh --template draw-card
```

The alias `draw_card` is accepted by the skill manifest and by `fetch-asset-bundle.sh`, but the release folder id is `draw-card`.

## Bundle v1

- Release tag: `assets-draw-card-v1`
- Asset name: `draw-card-v1.zip`
- Manifest URL: `https://github.com/jiawei248/dear-skill/releases/download/assets-draw-card-v1/draw-card-v1.zip`
- Manifest sha256: `385ab18374edae6417f4b524b42d707c8cb956c94cbfc45dfe7a94a5bae074cf`
- Approx extracted size: `31 MB`
- Approx zip size: `24 MB`

Expected extracted layout:

```text
base/
├── card_materials/
├── generated_stickers/
│   ├── all/
│   └── reference_base/
├── reference/
│   └── sticker.jpg
├── stickers/
│   └── decorations/
├── 轮播图/
├── carousel-photos-data.js
└── lyrics.txt
```

Excluded from the bundle:

- `.DS_Store`
- `__pycache__/`
- `.git/`
- local API keys or environment files
- source-only generation scripts that are not part of the runtime bundle

## Release Steps

From the staged bundle directory:

```bash
python3 -c 'from pathlib import Path; import zipfile; root=Path("."); out=Path("../draw-card-v1.zip"); zf=zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED,compresslevel=9); [zf.write(p,p.relative_to(root).as_posix()) for p in sorted(root.rglob("*")) if p.is_file() and p.name != ".DS_Store" and "__pycache__" not in p.parts and p.suffix != ".pyc"]; zf.close()'
shasum -a 256 draw-card-v1.zip
gh release create assets-draw-card-v1 draw-card-v1.zip --title "draw-card assets v1" --notes "Asset bundle for the dear draw-card template."
```

After upload, update `template.json` with the sha256 and zip size. The test suite locks these values so accidental bundle drift is visible.
