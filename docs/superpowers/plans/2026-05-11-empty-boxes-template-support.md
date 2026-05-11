# Empty Boxes Template Support Plan

**Goal:** Add `empty-boxes` as a ready rich template alongside `paper-house` and `bouquet`, with English production docs, a runtime builder, a GitHub Release asset bundle, and tests that lock the integration contract.

**Template principle:** each container controls the composition. Photos, cutouts, stickers, captions, and notes must physically belong inside the box and must be grounded in user-provided details. Final gift copy follows the user's habitual language with the recipient.

## Phase 1 — Template Registry and Documentation

- [x] Create `assets/templates/empty-boxes/`.
- [x] Add `template.json` with slot schema, activation disclosure, asset bundle metadata, and build contract.
- [x] Add English `README.md`, `SPEC.md`, and `RELEASE.md`.
- [x] Add preview assets for template discovery.
- [x] Document the required production rules:
  - photo height and pose must match container subdivisions
  - stickers must stay inside container bounds unless explicitly outside decoration
  - stickers should cluster into readable motifs instead of scattering
  - every box needs a concrete theme and quoted/echoed detail
  - final gift text uses the user's language, not English by default

## Phase 2 — Runtime Builder and Config Hook

- [x] Copy the canonical `tincase-box-loop.html` into `template-source/`.
- [x] Add `window.EMPTY_BOXES_GIFT_CONFIG` support.
- [x] Support runtime overrides for chrome labels, box assets, ambient gems, and per-box collages.
- [x] Implement `template-source/build.py`.
- [x] Ensure the builder writes output separately and does not mutate the canonical HTML.
- [x] Inline locally available assets from the build workdir, the fetched `base/` bundle, or `template-source/`.

## Phase 3 — Asset Bundle and GitHub Release

- [x] Stage the bundle from `~/Desktop/empty_boxes`.
- [x] Include `boxes/`, `stickers/`, `fonts/`, `figures/`, and `generated/`.
- [x] Exclude `.git/`, `.DS_Store`, `__pycache__/`, local API material, and source scripts that are not part of the runtime bundle.
- [x] Zip as `empty-boxes-v1.zip`.
- [x] Compute sha256 and update `template.json`.
- [x] Upload the zip to GitHub Release tag `assets-empty-boxes-v1`.
- [x] Confirm the release asset URL, size, and GitHub-reported sha256 digest match `template.json`.

## Phase 4 — Tests, Registry Copy, and Verification

- [x] Add schema tests for the template manifest and docs.
- [x] Add builder tests for runtime config injection and source immutability.
- [x] Add asset-bundle metadata tests.
- [x] Update `README.md` and `references/templates.md` so users can discover the template.
- [x] Run focused pytest coverage.
- [ ] If a browser environment is available, build a sample H5 and verify the rotating loop and mobile layout.

## Acceptance Criteria

- `assets/templates/empty-boxes/template.json` is valid JSON and references existing local docs/source/preview files.
- `template-source/build.py` can generate an `index.html` from `filled-slots.json`.
- The generated HTML contains `window.EMPTY_BOXES_GIFT_CONFIG`.
- The canonical HTML remains unchanged by builds.
- The release bundle is uploaded and the manifest URL/hash match it.
- The docs are English; gift-facing copy rules explicitly require the user's habitual language.
