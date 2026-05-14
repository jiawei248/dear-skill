# Dear Runtime Cleanup And Bundle Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove Hermes runtime persona leftovers, add the missing paper-house preview image, and make asset bundle refresh behavior match the template documentation.

**Architecture:** Runtime reference files should frame every gift as authored by the user for the recipient; Hermes should remain only as README origin attribution. Paper-house preview is a static asset referenced by `template.json`. Asset bundle caching is owned by `scripts/fetch-asset-bundle.sh`, with tests asserting refresh, sha marker, and partial-cache recovery behavior.

**Tech Stack:** Markdown reference docs, shell script, pytest using temporary local HTTP server/zip fixtures, static image asset.

---

### Task 1: Add regression tests for asset bundle refresh

**Files:**
- Create or modify: `tests/test_fetch_asset_bundle.py`
- Read: `scripts/fetch-asset-bundle.sh`

- [ ] Write tests that create a temporary template with `template.json.asset_bundle.url` and `sha256`, serve a zip locally, run `scripts/fetch-asset-bundle.sh --template <id>`, and assert `base/.bundle-sha256` is written.
- [ ] Add a test where `base/.bundle-sha256` matches the manifest sha and `base/` is non-empty; assert the script exits without replacing files.
- [ ] Add a test where the manifest sha changes or `--refresh-template <id>` is used; assert the old `base/` contents are replaced and `.bundle-sha256` is updated.
- [ ] Add a test where `base/` is non-empty but `.bundle-sha256` is missing; assert the script treats it as stale/partial and refreshes.
- [ ] Run `python3 -m pytest tests/test_fetch_asset_bundle.py -q`; expected before implementation: at least marker/refresh tests fail.

### Task 2: Implement bundle marker and refresh behavior

**Files:**
- Modify: `scripts/fetch-asset-bundle.sh`

- [ ] Parse both `--template <id>` and `--refresh-template <id>`.
- [ ] Read expected sha from `assets/templates/<id>/template.json` using Python.
- [ ] If `base/` is non-empty and `base/.bundle-sha256` matches expected sha, skip download.
- [ ] If `--refresh-template` is used, or marker is missing/mismatched, remove and rebuild `base/` from a fresh download.
- [ ] Extract into a temp directory first, then replace `base/` and write `base/.bundle-sha256` only after extraction succeeds.
- [ ] Run `python3 -m pytest tests/test_fetch_asset_bundle.py -q`; expected after implementation: pass.

### Task 3: Remove Hermes runtime persona references

**Files:**
- Modify runtime docs under `references/` and pattern cards as needed
- Do not remove README origin attribution

- [ ] Search `grep -RIn "Hermes\|soul\.md\|SOUL" references assets SKILL.md`.
- [ ] Rewrite runtime instructions that ask Claude to sound like Hermes, compare output to Hermes, or depend on `soul.md`.
- [ ] Replace assistant-persona language with user/recipient relationship language: the gift should sound like something the user could send, grounded in their shared language.
- [ ] Keep README origin attribution unchanged.
- [ ] Re-run the grep and confirm no runtime reference still depends on Hermes persona or `soul.md`; README may still mention project origin.

### Task 4: Add paper-house preview image

**Files:**
- Create: `assets/templates/paper-house/preview.jpg`
- Source: a local preview screenshot supplied by the maintainer
- Verify: `assets/templates/paper-house/template.json`

- [ ] Confirm the local preview screenshot exists.
- [ ] Convert/copy it to `assets/templates/paper-house/preview.jpg` so `template.json.preview` resolves.
- [ ] Add a test or validation command that checks every template `preview` path exists.

### Task 5: Verify and commit

**Files:**
- All modified docs/scripts/tests/assets from Tasks 1-4 plus existing pending README/delivery docs changes

- [ ] Run focused tests: `python3 -m pytest tests/test_fetch_asset_bundle.py tests/test_paper_house_template_schema.py tests/test_story_card_generator.py tests/test_paper_house_build.py -q`.
- [ ] Run `git diff --check`.
- [ ] Run `test -f assets/templates/paper-house/preview.jpg`.
- [ ] Review `git diff --stat` and `git status -sb`.
- [ ] Commit intended files only and push when requested/approved.

---

## Self-Review

- Spec coverage: covers Hermes/soul cleanup, preview image, sha marker refresh, `--refresh-template`, and partial cache recovery.
- Placeholder scan: no TBD/TODO/fill-in placeholders.
- Type consistency: script option names match user request: `--template` and `--refresh-template`; marker path is `base/.bundle-sha256`.
