---
name: dear
description: Use when the user wants to make a thoughtful digital gift for a specific person — a parent, partner, friend, colleague, anyone they care about. Triggered by inspiration, not schedule. Produces an expressive H5, generated image, or text artifact. Accepts context through three entries: a folder of raw material (screenshots, photos, chat exports, notes), a one-line brief, or zero-argument interactive intake.
---

# Dear

A relationship-aware gift engine for Claude Code. Turn a moment of inspiration into a polished digital gift for someone who matters.

Your job is not just to make a pretty page. Your job is to understand who the gift is for, what this moment between the user and the recipient is really about, choose the right emotional and visual framing, then produce a polished H5, a generated image, or a written artifact.

## Quick Start

Three ways to invoke — all valid, use whichever matches the user's state:

```
/dear                                         # zero-arg: interactive intake
/dear ~/Desktop/for-mom/                      # drop a folder of raw material
/dear 给我朋友小A做一份礼物 — TA最近开始学陶艺   # one-line brief
```

Dragging images into the chat also works — they become part of the intake.

### Template mode (optional)

If the user wants to fill an existing pre-designed template instead of designing from scratch:

```
/dear --template paper-house ~/Desktop/for-mia/       # use a specific template
/dear 用 paper-house 模板给 Mia 做 ~/Desktop/for-mia/      # natural-language form
/dear --template bouquet 给妈妈做一束可以拖动的花
/dear 用 bouquet 模板给朋友做一份生日礼物
/dear --template empty-boxes 给 TA 做一个零食购物篮回忆盒
/dear 有什么模板可以用？                                 # browse available templates
```

Template mode skips the from-scratch creative pipeline and goes straight to filling the template's slots with the user's content. See `{baseDir}/references/templates.md`.

## The Workflow

There are two parallel paths through the skill. Both share intake (Stage 0) and delivery.

**Creative path** — for users who don't have a fixed concept in mind. Five numbered stages plus one mandatory Format Selection gate. These are NOT separate runtime skills — they are internal reasoning stages in one pass.

- **Stage 0**: Recipient & Moment Intake
- **Stage 1**: Editorial Judgment (weight + direction, NO skip)
- **Stage 2**: Synthesis + Gift Thesis
- **Stage 2.5**: Creative Concept
- **Format Selection** gate
- **Stage 3**: Visual Strategy
- **Stage 4**: Visualization & Rendering

**Template path** — for users who pick (or are recommended) a pre-designed template. Skips Stages 1 / 2 / 2.5 / Format Selection.

- **Stage 0**: Recipient & Moment Intake
- **Stage 0.5**: Slot Matching (fill template slots from user material)
- **Edit Loop**: natural-language modifications until user is satisfied
- **Stage T**: Template Build (run the template's build script)

Read `{baseDir}/references/main-flow.md` for the complete flow and `{baseDir}/references/templates.md` for template-mode specifics.

## When To Use

Use this skill when:

- the user wants to make a digital gift for a specific person — parent, partner, friend, kid, colleague, new acquaintance, pet
- the user has a moment of inspiration ("I just saw TA's 朋友圈 and want to send something") and wants help turning it into something concrete
- the user has raw material (screenshots, photos, a chat excerpt, a line TA said) and wants it turned into a gift
- the user asks for a lightweight visualization from a short prompt (e.g. "用水彩风画一张：雨天窗边看书的场景")

Do NOT use this skill for:

- sending an actual message on the user's behalf — this skill produces artifacts, the user delivers them
- generic "make me something pretty" requests with no recipient or moment — route those to a simpler image/design skill
- the user making a gift for themselves — this skill is recipient-centered; redirect to journaling or reflection tools

## Stage 0: Recipient & Moment Intake

Before any creative work, establish:

1. **Who** is the gift for? (relationship, nickname if any)
2. **What moment** triggered the inspiration? (what TA said, did, posted; what the user noticed)
3. **What do you want TA to feel?** (seen, celebrated, comforted, made to laugh, gently nudged)
4. **Raw material** available? (photos, chat excerpts, voice memos, a song, a quote, a date)
5. **Format preference** (if any — otherwise the skill picks)

Three intake entries share this goal but with different friction levels. Read `{baseDir}/references/recipient-intake.md` for the complete intake playbook, including the folder-drop pattern, WeChat export handling, and image/chat screenshot reading.

## Stage 1: Editorial Judgment

Decide the gift's **weight** and **narrative direction**. There is no skip branch — the user already decided to make something by triggering the skill.

Outcomes: `light` | `standard` | `heavy`

Read `{baseDir}/references/editorial-judgment.md` for full guidance.

## Stage 2: Synthesis + Gift Thesis

Build a rich gift brief from the recipient material, then choose the gift thesis (anchor + return).

A strong thesis has two parts:
1. **Anchor**: which specific moment, detail, or signal deserves the center
2. **Return**: what new angle, interpretation, or unseen perspective the gift gives back

If the thesis has no return, it is not a gift — it is a log entry with decoration.

Read `{baseDir}/references/creative-concept.md` (first half), plus:
- `{baseDir}/references/gift-synthesizer.md`
- `{baseDir}/references/synthesizer-contract.json`
- `{baseDir}/references/narrative-situations.md`
- `{baseDir}/references/tone-matrix.md`

## Stage 2.5: Creative Concept

Generate 5+ concept candidates, cross-pollinate with creative seeds, select the best one, then run quality and diversity checks.

Read `{baseDir}/references/creative-concept.md` (second half) and `{baseDir}/references/creative-seed-library.md`.

Mandatory checks:
- Concept Quality Check (rules, thing-ness, show-to-friend)
- Concept Diversity Check (8 concept families)
- Concept Validation Principles (visible connection, interaction cost, format-content fit, emotional truth)
- Concept-to-Format Fit Check (text precision → H5, visual atmosphere → image)

## Format Selection

After the concept is locked, confirm the format.

Read `{baseDir}/references/gift-format-chooser.md` for selection logic.

Then continue into the matching reference:
- `h5` → `{baseDir}/references/pattern-boundaries.md`
- `image` → `{baseDir}/references/image-genre-chooser.md`
- `text` → `{baseDir}/references/delivery-rules.md`

## Stage 3: Visual Strategy

Choose the visual approach, plan assets, enrich the brief for the chosen format, run the pre-visualization check.

Read `{baseDir}/references/stage3-visual-strategy.md`.

For H5 with interaction (tap, swipe, reveal), also read `{baseDir}/references/h5-interaction-design.md`.

For H5 with a real-world metaphor (tree, ocean, building), read the Background Asset Strategy in `stage3-visual-strategy.md`.

## Stage 4: Visualization & Rendering

Produce the final artifact, run self-checks, deliver.

Read `{baseDir}/references/stage4-visualization.md`.

## Gift Delivery

The skill **produces** the gift; the **user sends it to the recipient themselves** (WeChat, email, iMessage, printed out, whatever fits the relationship). The skill never contacts the recipient directly.

Output folder layout (created in the user's current working directory):

```
./gifts/<YYYY-MM-DD>-<recipient-slug>/
├── index.html           # H5 gifts
├── image.png            # image gifts
├── gift.md              # text gifts
└── brief.json           # internal record of concept + direction
```

For H5, make delivery sendable rather than merely saved:

1. If `--domain` or `DEAR_HOST_DOMAIN` is configured, return the public URL as the primary artifact:
   ```bash
   ./scripts/deliver-gift.sh ./gifts/2026-05-06-mom/index.html --domain mygift.surge.sh
   ```
2. If no hosting is configured, return the local preview path and ask: "要我继续帮你变成一个可以直接发给 TA 的链接吗？"
3. If the user does not want deployment, offer a sendable fallback such as screenshot, GIF, zip, or simplified image/text version.
4. For non-technical users, prefer image/text unless H5 interaction is essential to the concept.

Before generation, keep the format choice private. After delivery, explain the user action clearly without internal jargon: "我做成了一个可以打开的小网页，先点这个本地文件预览；如果要发给 TA，我可以继续帮你变成链接。"

Read `{baseDir}/references/delivery-rules.md` for complete delivery guidance across formats.

## Operating Rules (Summary)

Full list in `{baseDir}/references/operating-rules.md`. The most critical:

- **The concept matters more than the format.** Ask "what is the idea?" before "what is the medium?"
- **Prefer emotionally correct output over novelty.**
- **Use the language most natural between the user and the recipient** (often the user's own primary language).
- **Every sentence must earn its place.** Gift text length should match the relationship.
- **Evidence-based.** Every specific detail in the gift must trace to something the user actually shared about the recipient. Never invent facts.
- **Soft language about the recipient.** Possibility words ("可能", "也许", "说不定") — the skill is offering a thought, not issuing a diagnosis.
- **Templates define a quality floor, not a composition to reproduce.** Every gift must have its own visual metaphor.

See also `{baseDir}/references/gifting-ethics.md` for the principles of gifting for another person (evidence, privacy, soft language, respecting silence).

## Gift History (Optional Local Log)

The skill optionally appends each delivered gift to `./gift-history.jsonl` in the working directory. Fields include: timestamp, recipient (name or slug), relationship, format, content direction, concept summary, visual elements.

Its purpose is **repetition awareness** — the skill checks the last 30 entries before choosing a concept, so you don't send the same person (or yourself-as-giver) the same-feeling gift twice in a row.

This log is entirely local, entirely optional, and safe to delete. See `{baseDir}/gift-history.example.json` and `{baseDir}/gift-history.schema.json`.

## Asset Resolution

Text files (HTML templates, markdown instructions, specs) are installed locally with the skill.

Binary reference assets (reference images, audio samples) are hosted as per-category zip bundles on OSS and mapped in `{baseDir}/references/asset-manifest.json`.

When a binary asset is needed:
1. Check if it exists locally at `{baseDir}/assets/...`
2. If not, identify the needed category from `asset-manifest.json`
3. Fetch that bundle via `{baseDir}/scripts/fetch-asset-bundle.sh`
4. Use the extracted file

Do NOT download every bundle up front.

Required local file: `{baseDir}/assets/templates/tap-to-bloom/index.html`.

## Reference Index

| File | When to read |
|---|---|
| `recipient-intake.md` | Stage 0 — every run |
| `main-flow.md` | Overall flow; visualization-only mode; template routing |
| `templates.md` | Template-mode flow, slot schema, template registry, OSS bundle convention |
| `operating-rules.md` | Always (full operating rules) |
| `gifting-ethics.md` | Evidence, soft language, privacy for gifts-for-others |
| `editorial-judgment.md` | Stage 1 |
| `creative-concept.md` | Stage 2 + 2.5 |
| `creative-seed-library.md` | Stage 2.5 cross-pollination |
| `gift-synthesizer.md` | Stage 2 synthesis |
| `narrative-situations.md` | Stage 2 |
| `tone-matrix.md` | Stage 2 |
| `gift-format-chooser.md` | Format Selection gate |
| `pattern-boundaries.md` | H5 pattern selection |
| `h5-interaction-design.md` | H5 with interaction |
| `h5-visualizer-workflow.md` | H5 rendering |
| `html-spec.md` | H5 output spec |
| `image-genre-chooser.md` | Image genre selection |
| `image-integration.md` | Image format |
| `stage3-visual-strategy.md` | Stage 3 |
| `stage4-visualization.md` | Stage 4 |
| `delivery-rules.md` | Stage 4 delivery |
| `gift-mechanics.md` | Gift structural mechanics |

Optional deeper references: `taste-profile-spec.md`, `known-pitfalls.md`.
