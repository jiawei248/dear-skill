# Folder Template Support Plan

**Goal:** Add `folder` as a ready rich template alongside `paper-house`, `bouquet`, and `empty-boxes`, with English production docs, a runtime builder, a GitHub Release asset bundle, registry copy, and tests that lock the integration contract.

**Template principle:** the file folder controls the physical logic. It must keep a believable back cover, front cover, and smoothly connected tab; photos, papers, tapes, stickers, and gift-facing text must be grounded in user-provided details. Final gift copy follows the user's habitual language with the recipient.

## Phase 1 — Template Registry and Documentation

- [x] Create `assets/templates/folder/`.
- [x] Add `template.json` with slot schema, activation disclosure, asset bundle metadata, and build contract.
- [x] Add English `README.md`, `SPEC.md`, and `RELEASE.md`.
- [x] Add preview assets for template discovery.
- [x] Document the required production rules:
  - file-folder shell must preserve back cover, front cover, and connected tab
  - every folder needs a larger chapter theme plus concrete details or quotes
  - photo formats should vary across vertical strips, four-grids, polaroids, framed photos, and bordered mini photos
  - base papers and tapes should be used for writing/photo surfaces before drawing new SVG papers
  - stickers should be clustered inside folder bounds, not scattered
  - final gift text uses the user's language, not English by default

## Phase 2 — Runtime Builder and Config Hook

- [x] Copy the canonical `520-folder-gift.html` into `template-source/`.
- [x] Add `window.FOLDER_GIFT_CONFIG` support.
- [x] Support runtime overrides for archive copy, tabs, opened-folder copy, selector image replacements, selector text replacements, and layout config.
- [x] Implement `template-source/build.py`.
- [x] Ensure the builder writes output separately and does not mutate the canonical HTML.
- [x] Inline locally available assets from the build workdir, the fetched `base/` bundle, or `template-source/`.

## Phase 3 — Asset Bundle and GitHub Release

- [x] Stage the bundle from `~/Desktop/folder`.
- [x] Include `assets/`, `stickers/`, and `fonts/`.
- [x] Exclude `.git/`, `.DS_Store`, `__pycache__/`, local API material, and source-only files that are not part of the runtime bundle.
- [x] Zip as `folder-v1.zip`.
- [x] Compute sha256 and update `template.json`.
- [x] Upload the zip to GitHub Release tag `assets-folder-v1`.
- [x] Confirm the release asset URL and sha256 digest match `template.json`.

## Phase 4 — Tests, Registry Copy, and Verification

- [x] Add schema tests for the template manifest and docs.
- [x] Add builder tests for runtime config injection, workdir-prefixed asset inlining, vendor JS inlining, and source immutability.
- [x] Add asset-bundle metadata tests.
- [x] Update `README.md`, `SKILL.md`, and `references/templates.md` so users can discover the template.
- [x] Run focused pytest coverage.
- [ ] If a browser environment is available, build a sample H5 and verify folder opening, desktop layout, and mobile tab/caption fit.

## Acceptance Criteria

- `assets/templates/folder/template.json` is valid JSON and references existing local docs/source/preview files.
- `template-source/build.py` can generate an `index.html` from `filled-slots.json`.
- The generated HTML contains `window.FOLDER_GIFT_CONFIG`.
- The canonical HTML remains unchanged by builds.
- The release bundle is uploaded and the manifest URL/hash match it.
- The docs are English; gift-facing copy rules explicitly require the user's habitual language.
