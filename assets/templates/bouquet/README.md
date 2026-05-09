# Bouquet Template

`bouquet` is an interactive flower-canvas template for dear. It lets the user make a sendable bouquet where flowers can be dragged, gems can be freely added, paper-card positions can be adjusted, and card text can be refined with AI.

## Ready status

This directory contains a runnable template with a runtime builder:

- `template.json` — manifest and slot contract
- `SPEC.md` — production guidance
- `preview.jpg` — lightweight browse preview
- `template-source/mothers-day-blue-bouquet.html` — canonical source HTML, read-only
- `template-source/build.py` — runtime builder that writes a separate output `index.html`
- `RELEASE.md` — asset bundle packaging instructions

The large flowers, greenery, gems, fonts, and original references are intentionally shipped as an asset bundle instead of being committed into the normal repo tree.
