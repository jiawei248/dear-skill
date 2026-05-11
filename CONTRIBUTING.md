# Contributing

Thanks for wanting to contribute to `dear`.

This repo is part workflow engine, part prompt library, part creative toolkit. Good contributions usually improve one of these:

- gift quality
- visual quality
- reliability
- freshness and variety
- contributor friendliness

## Good Contribution Types

Especially welcome:

- new `pattern cards` for H5 gift mechanics
- new `image genres` or stronger image guidance
- new `creative seeds`, especially content-strategy seeds
- better onboarding, synthesis, or delivery rules
- rendering/runtime bug fixes
- focused tests for scripts or contracts
- docs improvements for public users and contributors

## Contribution Principles

Before adding anything, keep these project rules in mind:

- `Gift = anchor + return.` If the change only makes gifts look nicer but does not improve return, be careful.
- Treat templates and examples as references, not things to copy literally.
- Prefer additions that create new expressive territory, not near-duplicates of existing cards or genres.
- Keep the user's experience warm and non-technical. Avoid turning gift flows into setup funnels.
- Preserve the current supported formats: `h5`, `image`, and `text`.

## Where To Add Things

### New H5 Pattern Card

Add the pattern doc under:

- `references/pattern-cards/`

If the pattern deserves a reusable implementation, also add:

- `assets/templates/<pattern-name>/index.html`
- `assets/templates/<pattern-name>/notes.md`
- `assets/templates/<pattern-name>/template-schema.json`

### New Image Genre

Add the genre doc under:

- `references/image-genres/`

If you use reference assets, make sure they fit the existing asset-bundle flow rather than assuming all binaries live in git.

### New Creative Seed

Add it to:

- `references/creative-seed-library.md`

Prefer seeds that clearly strengthen either:

- form
- content / return

The best additions usually help cross-pollination create less generic gifts.

## Style Guidelines

- Keep docs direct and practical.
- Prefer concrete rules over vague encouragement.
- Use examples to clarify behavior, not to become templates that agents blindly copy.
- Keep comments and prose concise.
- Avoid introducing technical steps into user-facing flows unless absolutely necessary.

## Safety And Privacy

- Never commit secrets, `.env` files, raw tokens, or personal credentials.
- Do not add real user photos, personal chat logs, or other sensitive artifacts.
- Keep examples anonymized and portable.

## Verification

Run the smallest relevant verification for your change.

Examples:

- docs-only change: check formatting and consistency
- script/runtime change: run the targeted test or command for that path

Current example test:

```bash
python3 -m unittest tests.test_render_image_brief_contract
```

If your change affects another script or workflow, add or run the most focused verification you can.

## Pull Requests

Good pull requests usually include:

- what changed
- why it improves the gift system
- how you verified it
- screenshots or sample outputs when the change is highly visual

Small, sharp PRs are much easier to review than giant mixed ones.
