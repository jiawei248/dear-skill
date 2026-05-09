# Bouquet Asset Bundle Release

The bouquet template uses a release asset bundle for large flowers, greenery, gems, fonts, and original style references.

## Bundle contents

```text
bouquet-v1/
├── flowers/
├── greenery/
├── gems/
├── fonts/
└── reference/
    └── original-png/
```

## Prepared v1 bundle

Local prepared artifact:

```bash
/tmp/bouquet-v1.zip
```

Compute SHA-256 with:

```bash
shasum -a 256 bouquet-v1.zip
```

Current SHA-256:

```text
c9e424ccc0c0b7447d50f9b450b7d663b6d6a927c22e1ce14715ab0b1fbff726
```

Approximate size: 97 MB.

## Publish steps

1. Create a GitHub Release tag named `assets-bouquet-v1`.
2. Upload `bouquet-v1.zip` as a release asset.
3. Confirm the final URL matches:

```text
https://github.com/jiawei248/dear-skill/releases/download/assets-bouquet-v1/bouquet-v1.zip
```

4. Keep `template.json.asset_bundle.sha256` equal to the SHA above.

## Refreshing assets

When adding new flowers or gems:

1. Build a new `bouquet-v2.zip` with the same directory layout.
2. Publish a new release tag such as `assets-bouquet-v2`.
3. Update `template.json.asset_bundle.url`.
4. Update `template.json.asset_bundle.sha256`.

Users refresh with:

```bash
scripts/fetch-asset-bundle.sh --refresh-template bouquet
```
