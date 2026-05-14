# folder Asset Bundle Release

The runtime bundle is intentionally not committed to the repo. It is published as a GitHub Release asset and fetched on first use by:

```bash
scripts/fetch-asset-bundle.sh --template folder
```

## Bundle v1

- Release tag: `assets-folder-v1`
- Asset name: `folder-v1.zip`
- Manifest URL: `https://github.com/jiawei248/dear-skill/releases/download/assets-folder-v1/folder-v1.zip`
- Manifest sha256: `bd79a859e8627b93a5be011ffe5b9a0bc7b15d1835814d631b28745201a35fa8`
- Approx extracted size: `139 MB`
- Approx zip size: `118 MB`

Expected extracted layout:

```text
base/
├── assets/
│   ├── generated/
│   └── vendor/
├── fonts/
└── stickers/
    ├── base/
    ├── decorations/
    ├── electronic_devices/
    ├── frames/
    ├── study_utilities/
    └── tapes_papers/
```

Excluded from the bundle:

- `.DS_Store`
- `__pycache__/`
- `.git/`
- local API keys or environment files
- source-only docs that belong in the repo

## Release Steps

From the staged bundle directory:

```bash
zip -qr folder-v1.zip assets fonts stickers -x '*.DS_Store' '*/__pycache__/*' '*.pyc'
shasum -a 256 folder-v1.zip
gh release create assets-folder-v1 folder-v1.zip --title "folder assets v1" --notes "Asset bundle for the dear folder template."
```

After upload, update `template.json` with the sha256 and zip size. The test suite locks these values so accidental bundle drift is visible.
