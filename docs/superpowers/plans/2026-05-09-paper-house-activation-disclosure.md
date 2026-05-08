# Paper-House Activation Disclosure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a short paper-house preflight disclosure so users understand time, dependencies, cost, and lighter alternatives before choosing the template.

**Architecture:** Keep this as template metadata plus SPEC/runtime guidance. Tests assert that the manifest and SPEC contain the user-facing disclosure, full/lightweight/fallback options, and dependency facts; no builder behavior changes are required.

**Tech Stack:** JSON manifest, Markdown SPEC/reference docs, pytest validation.

---

### Task 1: Add disclosure regression tests

**Files:**
- Modify: `tests/test_paper_house_template_schema.py`
- Read: `assets/templates/paper-house/template.json`
- Read: `assets/templates/paper-house/SPEC.md`

- [ ] Add a test that asserts `template.json` has `activation_disclosure` with a short user-facing message mentioning ~150MB bundle, image generation for custom characters/story cards, and lightweight mode.
- [ ] Add a test that asserts `activation_disclosure.options` includes `full`, `lightweight_draft`, and `text_image_fallback`.
- [ ] Add a test that asserts `SPEC.md` includes the exact activation moment and the same three options.
- [ ] Run `python3 -m pytest tests/test_paper_house_template_schema.py -q`; expected before implementation: disclosure tests fail.

### Task 2: Update paper-house activation guidance

**Files:**
- Modify: `assets/templates/paper-house/template.json`
- Modify: `assets/templates/paper-house/SPEC.md`

- [ ] Add manifest `activation_disclosure` metadata with the short recommended user message and options.
- [ ] Add a SPEC section near activation / production checklist telling the agent to show the disclosure before fetching assets or generating images.
- [ ] Clarify that full version uses bundle download, rembg/model/image generation/story cards/iTunes lookup; lightweight draft uses cached/draft assets where possible; text/image fallback skips H5.
- [ ] Run `python3 -m pytest tests/test_paper_house_template_schema.py -q`; expected after implementation: pass.

### Task 3: Audit, commit, and push

**Files:**
- All pending changes from this session.

- [ ] Run paper-house and tooling tests: `python3 -m pytest tests/test_h5_verification_docs.py tests/test_fetch_asset_bundle.py tests/test_runtime_docs_no_hermes.py tests/test_paper_house_template_schema.py tests/test_story_card_generator.py tests/test_paper_house_build.py -q`.
- [ ] Run `python3 -m json.tool assets/templates/paper-house/template.json >/dev/null`.
- [ ] Run `bash -n scripts/fetch-asset-bundle.sh && bash -n scripts/verify-h5.sh`.
- [ ] Run `test -f assets/templates/paper-house/preview.jpg`.
- [ ] Run `git diff --check`.
- [ ] Review status/diff, commit intended files, push to `origin/main`, and verify `HEAD == origin/main`.

---

## Self-Review

- Spec coverage: covers the requested preflight disclosure, dependency/cost warning, three user options, and final paper-house verification before push.
- Placeholder scan: no placeholders.
- Type consistency: `activation_disclosure.options` uses `full`, `lightweight_draft`, and `text_image_fallback` consistently.
