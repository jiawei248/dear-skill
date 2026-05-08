# Paper-House Schema Normalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Normalize the paper-house template manifest to the common slot schema while keeping paper-house-specific details in supplemental metadata.

**Architecture:** This is a manifest/documentation change, not a builder change. `template.json` keeps common slot fields canonical; paper-house details move into `runtime_mapping`, `physical_rules`, placement hints, and template notes. Tests assert the manifest shape so future template work does not regress into template-specific base fields.

**Tech Stack:** JSON manifest, Markdown docs, Python pytest for schema assertions.

---

### Task 1: Add manifest schema regression test

**Files:**
- Create: `tests/test_paper_house_template_schema.py`
- Read: `assets/templates/paper-house/template.json`

- [ ] **Step 1: Write the failing test**

Create `tests/test_paper_house_template_schema.py` with tests that load `template.json`, index slots by id, and assert:
- `scene_decorations` uses `library_subpaths`, `count_range`, `placement_zone`, `selection_hint`, and `runtime_mapping`.
- `scene_decorations` no longer uses `source_library`, `library_categories`, or `count_range_per_scene`.
- `character_reference` exists as `user_image_processed` and is optional.
- `scene_figure_image` references `character_reference`, writes under `figures/`, and does not own `pre_process_pipeline`.
- `room_walls_and_floor` keeps `ai_generated_image` but has prompt/style/consistency/runtime mapping fields.

- [ ] **Step 2: Run the focused test and verify it fails**

Run: `python3 -m pytest tests/test_paper_house_template_schema.py -q`
Expected before implementation: fails because the current manifest has no `character_reference`, decorations still use old fields, and room walls lack `runtime_mapping`.

### Task 2: Normalize manifest slots

**Files:**
- Modify: `assets/templates/paper-house/template.json`
- Test: `tests/test_paper_house_template_schema.py`

- [ ] **Step 1: Update `scene_decorations`**

Replace template-specific library fields with common slot fields:
- `library_subpaths`
- `count_range`
- `placement_zone`
- `selection_hint`
- `runtime_mapping`
Keep physical placement details in `placement_rules` and hero behavior in `hero_item_rule`.

- [ ] **Step 2: Split character reference from final scene figures**

Insert a `character_reference` slot before `scene_figure_image` with `type: user_image_processed`, optional count `0-2`, purpose, pipeline, and runtime mapping. Update `scene_figure_image` to keep only final generated sprite semantics and point at `reference_slot: character_reference`.

- [ ] **Step 3: Enrich `room_walls_and_floor`**

Keep it as `ai_generated_image`, retain components, and add common fields: `approx_size`, `aspect_ratio`, `prompt_hint`, `runtime_mapping.output_paths`, plus existing `style_anchor` and `consistency_group`.

- [ ] **Step 4: Run focused manifest test and verify it passes**

Run: `python3 -m pytest tests/test_paper_house_template_schema.py -q`
Expected after implementation: all tests pass.

### Task 3: Update docs

**Files:**
- Modify: `references/templates.md`
- Modify: `assets/templates/paper-house/SPEC.md`

- [ ] **Step 1: Update general template guidance**

Add a short note that template-specific details belong in `template_notes`, `runtime_mapping`, `physical_rules`, or similar supplemental fields, while base slot fields should stay aligned with the common schema.

- [ ] **Step 2: Update paper-house spec wording**

Explain that the flow first collects/processes `character_reference`, then produces final `scene_figure_image` sprites under `paper-house-work/figures/`.

### Task 4: Verify, commit, and push

**Files:**
- All modified files from Tasks 1-3

- [ ] **Step 1: Run verification**

Run:
- `python3 -m pytest tests/test_paper_house_template_schema.py tests/test_story_card_generator.py tests/test_paper_house_build.py -q`
- `python3 -m json.tool assets/templates/paper-house/template.json >/dev/null`
- `git diff --check`

- [ ] **Step 2: Commit intended files only**

Stage only:
- `assets/templates/paper-house/template.json`
- `assets/templates/paper-house/SPEC.md`
- `references/templates.md`
- `tests/test_paper_house_template_schema.py`
- this plan file

- [ ] **Step 3: Push `main` to `origin`**

Run: `git push origin main`

---

## Self-Review

- Spec coverage: all user-requested manifest/doc changes are covered; builder, canonical HTML, and asset bundle are explicitly untouched.
- Placeholder scan: no TBD/TODO/implement-later placeholders remain.
- Type consistency: field names match the requested schema (`library_subpaths`, `count_range`, `runtime_mapping`, `reference_slot`, `character_reference`).
