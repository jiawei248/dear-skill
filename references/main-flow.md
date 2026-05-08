# Main Flow

The complete flow for a single `/dear` invocation, end to end. This replaces the original skill's separate manual-run, daily-run, and setup flows — there is no daily cron in Claude Code, and the skill is always user-triggered.

## Flow Overview

There are two paths. Both share intake and delivery; the middle differs.

### Creative path (default)

```
invocation
   ↓
Stage 0: Recipient & Moment Intake    → recipient-intake.md
   ↓
Stage 1: Editorial Judgment            → editorial-judgment.md
   ↓
Stage 2: Synthesis + Gift Thesis       → creative-concept.md (first half)
   ↓
Stage 2.5: Creative Concept            → creative-concept.md (second half)
   ↓
Format Selection gate                   → gift-format-chooser.md
   ↓
Stage 3: Visual Strategy               → stage3-visual-strategy.md
   ↓
Stage 4: Visualization & Rendering     → stage4-visualization.md
   ↓
Delivery                                → delivery-rules.md
   ↓
(Optional) Append to ./gift-history.jsonl
```

### Template path

```
invocation with --template <id>  OR  user picks template after browse
   ↓
Stage 0: Recipient & Moment Intake    → recipient-intake.md
   ↓
Stage 0.5: Slot Matching               → templates.md
   ↓
Show fill preview to user
   ↓
Natural-language edit loop             → templates.md
   (user confirms or asks for changes; skill re-fills slots; re-show)
   ↓
Stage T: Template Build                 → templates.md (build pipeline)
   ↓
Delivery                                → delivery-rules.md
   ↓
(Optional) Append to ./gift-history.jsonl
```

Read each stage's reference file **just-in-time** when you reach that stage. Do not pre-load all references up front.

## Path Selection

At the start of every invocation, decide which path to follow:

- If the user explicitly named a template (`--template`, "用 X 模板", or picked one from a browse list) → **template path**
- If the user provided a concrete one-shot creative brief with no recipient ("画一张水彩...") → **visualization-only mode** (a sub-mode of the creative path; see below)
- Otherwise → **creative path**

During the creative path's Format Selection gate, the skill MAY check the template registry: if any template's `best_for` and `tone` strongly match the locked concept, the skill may offer to switch to that template. This is an offer, not a redirect — never override the user's chosen path silently.

## Progress Reporting

The user is present in Claude Code and actively waiting. They benefit from lightweight updates but should NOT see internal reasoning.

Rules:

- Send one brief warm message when gift creation starts ("在做你的礼物～" / "等我一下，有个小东西想给 TA~")
- If the process takes more than about 3 minutes, one optional patience message is allowed ("快好了～")
- Total user-visible messages around the gift should be at most 3: start + optional patience + delivery
- Do NOT reveal the specific concept, format choice, or internal reasoning before delivery
- Do NOT expose technical errors, retries, or self-test results
- The surprise is part of the gift — keep details hidden until delivery
- Delivery message: 1-2 sentences of emotional context about the gift (the "why", not the "how")

Bad progress examples (never do these):

- "创意确定：矛盾体质鉴定报告——体检报告格式，6项矛盾指标+温柔医生评语"
- "方案：H5（CSS模拟体检报告纸质感）"
- "部署失败，重试中"
- any technical details, error recovery, concept names, format decisions, or internal reasoning

Exception: if the user is explicitly debugging the skill ("帮我测试一下", "我要看看流程", "debug模式"), full verbose output is acceptable.

## Single Output Rule

Always deliver exactly ONE final gift to the user. 

Do not:

- generate multiple versions and ask the user to pick
- send two images "看看哪个好"
- offer A/B choices

If you want to self-check quality, do it internally. The user only sees the final chosen result.

Exception: explicit debug or test sessions.

## Real-Time Execution

Because the user is present, execute inline. Do NOT spawn sub-agents for the main gift workflow — sub-agent spawns add latency, remove the user from the feedback loop, and hide failures. Reserve sub-agent use for heavy parallel work like generating multiple image variants in parallel before internal selection.

## Full Creative Workflow

Every `/dear` invocation that isn't visualization-only AND isn't in template path follows the full six-stage pipeline:

1. Stage 0: Recipient & Moment Intake
2. Stage 1: Editorial Judgment
3. Stage 2: Synthesis + Gift Thesis
4. Stage 2.5: Creative Concept (5 candidates → select the best)
5. Format Selection
6. Stage 3: Visual Strategy
7. Stage 4: Render + Deliver

## Template Path Workflow

When the user picks a template:

1. **Stage 0**: standard intake — folder / brief / interactive — same as creative path. The template's own slot schema will guide how the material is interpreted.
2. **Load template manifest** at `{baseDir}/assets/templates/<id>/template.json`. Verify the asset bundle is present locally; if not, fetch from the manifest's `asset_bundle.url`.
3. **Stage 0.5 — Slot Matching**: walk through every slot declared in the manifest, fill it from intake material plus AI generation/composition as the slot type dictates. See `templates.md` for the per-slot-type algorithm.
4. **Fill preview**: render a markdown summary of every filled slot and show it to the user.
5. **Natural-language edit loop**: the user can say anything to adjust anything ("kitchen 的歌词换一首" / "整体感觉太冷了" / "Mia 的照片用另一张"). Skill re-fills affected slots and re-shows the preview. No structured commands. Loop continues until the user says "ok / 可以 / 开始做".
6. **Stage T — Build**: write `filled-slots.json`, run the template's `build_script`, capture the output `index.html`.
7. **Delivery**: same as creative path — drop into `./gifts/<date>-<recipient-slug>/`, optionally deploy via `deliver-gift.sh`.

Template path skips Stages 1, 2, 2.5, and Format Selection. The template ENCODES those decisions.

Stage 3 visual strategy is **partially active** in template mode — only for the per-gift `ai_generated_image` slots, where the skill must produce a coherent, scene-consistent image at the slot's required size. Use `stage3-visual-strategy.md` for guidance on those individual generations, but do NOT redo overall format/visual planning.

## Visualization-Only Mode

When the user invokes the skill with a concrete creative brief instead of a recipient context — e.g.:

```
/dear 用水彩风画一张：雨天窗边看书的场景
/dear 把这首诗做成一个有风吹散效果的H5
/dear 生成一张氛围图：深夜台灯下改代码
```

— treat it as **visualization-only mode**. The user has already done the editorial and concept work themselves; the skill's job is execution, not ideation.

In this mode:

1. Skip Stage 0 intake Q&A. There is no recipient to learn about.
2. Skip Stage 1 editorial judgment. The user decided what to make.
3. Do a lightweight mini-synthesis from the user's brief only.
4. Infer format from the brief if possible: "水彩" / "插画" / "氛围图" / "表情包" → `image`; "H5" / "页面" / "互动" → `h5`; "诗" / "信" / "故事" → `text`. If unclear, default to whichever the brief sounds most like.
5. Run Stage 3 Visual Strategy with the full mandatory checklist.
6. Run the Pre-Visualization Check.
7. Run Stage 4 Visualization with the same visual quality floor as a full gift.
8. Deliver.

Visualization-only still:

- Follows the same visual quality floor
- Reads at least one relevant pattern card or genre reference
- Reads a relevant template when one exists
- Honors `html-spec.md` for H5 output and `image-integration.md` for image output

Visualization-only does NOT:

- Ask recipient questions
- Run the 5-candidate concept comparison (the user already picked)
- Append to `gift-history.jsonl` unless the user is also telling the skill who the gift is for

## Text-Play Path

`text-play` is the live-chat gift format — the interaction itself *is* the gift, with no saved artifact.

Use text-play only when:

- the gift is for the user themselves-and-TA in a synchronous relationship (the user will forward the chat, or plays through it with TA sitting next to them)
- OR the user is the only audience and wants a playful interaction
- the concept becomes better through live unfolding than through a finished artifact
- each turn can stay short and low-friction

Format rules:

- aim for 5-10 turns total
- keep each skill turn to ~3-4 sentences max
- ask for tiny replies: one word, one emoji, one choice, one short line
- do not let the interaction sprawl into open-ended role-play unless the user explicitly asks
- always carry a payoff in mind before starting: reveal, punchline, reframe, mini ending, relational callback
- let the user exit at any time with a graceful line such as "那我们就把这一幕停在这里"
- if the user stops replying, do not chase; end warmly
- never expose the format name or say a `text-play` gift is starting
- do not explain round counts, mechanics, or payoff structure before the first move

### Text-Play Opening Rule

The first message sets the emotional contract.

Good qualities:

- feels like a weird quiz, tiny dare, mystery prompt, or sudden game in chat
- contains an immediate hook, image, or bait
- includes the first choice or action right away
- makes the user's first reply fun to give
- stays under 3 short lines

Good openings:

- `🚪🚪🚪 三扇门。左边传出海浪声，中间有光从门缝漏出来，右边门上贴了张便利贴写着「别选我」。你推哪扇？`
- `刚刚路过一个占卜摊 🔮 她说可以替你算一道感情题。她把签递过来，说：让她自己选。`
- `📦 有个包裹寄到了。没有寄件人，只有一张纸条：关于 TA 的三个事实，其中一个是假的。拆吗？`

Avoid:

- `准备好了吗？回个好就行`
- `我要给你看一样东西`
- `假设有一个平行宇宙的 TA`
- anything that explains the game before it starts
- anything that asks for commitment before giving the first playful move

### Text-Play Transition Rule

Do not use quiz-style meta-language between turns.

Avoid: `下一题。` / `第二个问题：` / `好，最后一题。` / `Round 2:`

Instead: let the story / scene / game world carry the next beat naturally. Use the user's own answer as the bridge into what happens next.

### Text-Play Form Variety

Text-play is NOT limited to quiz structures. Available forms include:

**Quiz / Reading:** pick-and-reveal, `3 facts 1 fake`, taste test, boundary blitz

**Collaborative Storytelling:** co-written story with user choices, alternating perspectives, fortunately/unfortunately chain

**Deduction / Guessing:** character charades, diagnosis game, detective duel, literary forgery

**Language Constraint:** corrupted speech, emoji-only, exactly-5-words, "of course" chicken

**Simulated Scene:** drop user into a tiny fictional scene; simulated text-message thread; fake voicemail

**Puzzle / Trigger:** unlock the agent; river god's choice; sealed envelopes

**Role Swap & Scoring:** role reversal; situation challenge

**Surreal / Open-Ended:** nonsense interview; rapid-fire absurd hypotheticals

**Performance / Show:** fake podcast; standup roast with affection; fake award ceremony

**Do not default to quiz format.** If the last text-play was a quiz, the next one must use a different form.

When choosing the form, consider user energy, topic heaviness, and recent text-play history.

## No Format Downgrade Under Time Pressure

The skill is not allowed to downgrade the chosen format just because the user is waiting, the task feels slow, or a quicker path is available.

Do not do:

- "this should be h5, but image is faster so I'll switch"
- "this should be text, but I'll send a short image because I already have the prompt"
- "the user has waited 2 minutes, so I'll collapse the concept into a cheaper format"

Allowed reasons to change format mid-flight:

- the originally chosen format is genuinely unavailable (missing API key)
- the required capability fails and retry is no longer sensible
- a stricter format-fit check shows the original choice was wrong
- the user explicitly changes preference

If you must change format, preserve the same anchor-plus-return quality bar.

## Post-Delivery (Lightweight)

After the gift is delivered:

1. Write the gift artifact(s) to `./gifts/<YYYY-MM-DD>-<recipient-slug>/`
2. (Optional, recommended) Append a single line to `./gift-history.jsonl` with the gift's metadata — see `gift-history.schema.json`
3. If the artifact is H5 and the user has a hosting domain configured, run `scripts/deliver-gift.sh` and surface the returned URL

That is the complete post-delivery. There is no cron-based reflection, no long-term memory update, no taste-profile heartbeat. Those belonged to the daemon-style original skill and have no equivalent in Claude Code.

If the user wants to capture anything about how this went for future reference, they can ask explicitly — don't do it silently.
