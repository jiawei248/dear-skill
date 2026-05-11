# Creative Concept & Synthesis

Complete instructions for Stage 2 (Synthesis + Gift Thesis) and Stage 2.5 (Creative Concept generation, quality checks, diversity checks, collision checks, and format selection). Read this after editorial judgment decides a gift is warranted.

### Stage 2: Synthesis

If a gift is warranted, build a rich gift brief before thinking about visual execution.

You must preserve the full synthesis logic described in:

- `{baseDir}/references/gift-synthesizer.md`
- `{baseDir}/references/synthesizer-contract.json`
- `{baseDir}/references/narrative-situations.md`
- `{baseDir}/references/tone-matrix.md`

Important synthesis expectations:

- work from the recipient brief produced in Stage 0 — that is the primary source
- preserve specific quotes from the recipient material when they earned their place in the gift
- keep image references if they are crucial to the gift concept
- capture what matters about this moment and how it connects to what the user knows about the recipient
- keep the brief rich enough for downstream rendering, not just emotionally correct but materially useful
- prefer one strong anchor detail over many weak scattered ones

The synthesis should usually retain at most these six content slots:

1. `today_theme`
2. `emotion_peaks`
3. `historical_echo`
4. `open_loop`
5. `lobster_judgment`
6. `preference_hint`

### Gift Thesis

After completing the six content slots, choose exactly `ONE` or `TWO` of them as the gift thesis.

The thesis is not just which event or detail to focus on.

The thesis is what the user wants to give the recipient through that event: a feeling, perspective, or recognition the recipient did not already fully have.

A strong thesis has two parts:

1. the anchor: which moment, detail, or signal deserves the center
2. the return: what new angle, interpretation, reframe, knowledge, or unseen perspective the user wants to give back

Good theses combine anchor and return.

Bad theses stop at anchor and only replay, recap, or decorate what already happened.

If the thesis has no return, it is not a gift. It is a log entry with decoration.

### Return Deletion Test (MANDATORY)

After writing the thesis, mentally delete the user's original words from the gift. Does the gift still say something the user didn't already know/have/see?

FAILS (recap with decoration — the user gains nothing new):
- User said "I want to stay home this weekend" → gift lists stay-home activities (user already knows those)
- User mentioned three hobbies → gacha machine dispenses those same three hobbies (just repackaged)
- User said "I'm so tired" → gift says "you worked hard today" (user already knows that)
- User described weekend plans → gift restates those plans in a prettier format (no new perspective)

PASSES (genuine return — the user receives something they did not have before):
- User said "I want to stay home this weekend" → gift notices user has stayed home every weekend for a month, makes a "your radius of motion" map with one gentle note: "but those new shoes are still unworn"
- User mentioned three hobbies → gift finds a hidden pattern connecting all three ("everything you chose is something you do alone — is that rest or retreat?")
- User said "I'm so tired" → gift distinguishes THIS tiredness from last week's ("last week was 'too much to do' tired; this week is 'don't want to do it' tired — different animal")
- User described weekend plans → gift picks ONE plan, does actual research, and returns a specific recommendation the user wouldn't have found alone

If the test fails, go back and find the return. A gift without return is a voicemail, not a gift.

Use more than two only when:

- every part is genuinely equally important
- the day is a special memory or ritual node, such as anniversary, onboarding, or another major commemorative moment

The remaining slots are context.

They may survive as:

- subtle details
- captions
- background references
- small easter eggs

But they must not compete with the thesis for attention.

The gift should not feel like all six slots received equal visual billing.

If none of the six slots yields a thesis with a meaningful return, rethink which angle deserves a gift at all. A smaller, sharper gift is better than a beautiful memory dump. If needed, choose a lighter framing or an extension-like angle rather than forcing every slot into the artifact.

Tone policy during synthesis:

- Default to the user’s natural voice with this recipient, inferred from the provided material.
- Adjust for the event type and the user's usual way of speaking with the recipient.
- Avoid humor in moments that are sad, raw, or destabilizing unless there is clear evidence that humor would feel loving rather than evasive.
- Avoid making happy or playful moments sound overly solemn.
- Allow occasional deliberate contrast only when it increases surprise and intimacy without violating emotional truth.

### Stage 2.5: Creative Concept

After synthesis produces the anchor and return, but before choosing any format, genre, or pattern, generate the gift's creative concept.

Before generating concepts, reread the recipient brief from Stage 0 — especially the `emotional_intent` and `material_inventory` — and if `./gift-history.jsonl` exists, scan the last ~5 entries for the same recipient to avoid repeating a concept family or visual style you already used for TA.

The creative concept is one sentence describing a concrete, specific, novel gift idea that carries the return.

It should sound like a concrete idea the user could get excited to make: `我要做一个 XXX！`

A strong concept should feel like a small world with its own logic, not just content plus decoration.

#### Step 1: Generate 5 Candidates

This full creative concept workflow applies to every user-triggered gift that reaches Stage `2.5`. Invocation style changes progress reporting, not concept quality standards. Do not skip the `5`-candidate generation step for speed. A single unjustified concept is more likely to miss than one selected from evaluated alternatives.

Use these thinking angles to spark ideas:

- `metaphor flip`: what familiar object or experience could become this gift if twisted
- `format mashup`: what two unrelated formats could collide productively
- `impossible action`: what physically impossible but emotionally true action could happen
- `scale shift`: what should become tiny, huge, pocket-sized, or monumental
- `role reversal`: what happens if the usual social direction flips
- `time distortion`: what happens if the concept bends future, replay, speed, or countdown logic
- `cultural remix`: what familiar cultural container could carry the return unexpectedly

Generate at least `5` candidate concepts using different thinking angles. Each candidate should be one sentence.

#### Step 2: Seed Cross-Pollination

After generating `5` initial candidates, decide whether cross-pollination is needed.

If one of the initial candidates already has a very strong small-world feeling, you may lock it directly.

If the candidates still feel too close to `a nice [format] with [content]`, do one round of cross-pollination:

1. Read the full `{baseDir}/references/creative-seed-library.md` library.
2. Pick `1` or `2` seeds that are unrelated to the current thesis.
3. When possible, ensure the chosen seeds include at least:
   - one `Form Seed`
   - one `Content Strategy Seed`
4. Ask: what if I combined my best candidate with this unrelated seed's structure

Example:

- thesis: user had a tough day at work
- initial candidate: an office building the user can destroy
- unrelated seed: emotion cocktail
- cross-pollination: mix today's work stress into a cocktail, ingredients are each annoyance from the day, shaking animation, final drink equals tonight's decompression plan

This often produces the most surprising results because it forces structural novelty rather than just metaphorical novelty.

Add any strong cross-pollinated concepts to the candidate list.

Important distinction:

- `pattern cards` are about how to make an experience or interaction land
- `creative seeds` are about what kind of small world, invention, or playful format the gift could become

Do not confuse them.

#### Step 3: Select the Best Concept

From all candidates, pick the ONE that is:

- most surprising: the user has probably never received something like this
- most world-like: it feels like a small invention with its own rules, not just content plus decoration
- most distinct from recent gifts in `recent_gifts`, both in `output_shape` and in concept family
- emotionally fitting for the anchor-plus-return pair
- achievable in the available formats

#### Return Substance Check

Before running the Concept Quality Check, verify the gift's return substance.

Use this sentence:

`After receiving this gift, the user will know, feel, discover, or wonder ____ that they did not already fully have.`

If the blank can only be filled with any of these:

- their own answers in a new format
- that the skill can make cute artifacts
- a generic positive sentiment
- `you're doing great`
- `you're brave`
- simple acknowledgement of a situation the user already described
- a flatter version of `you're scared of launching but doing it anyway` when the user already knows that

then the concept still has weak or zero return.

Treat these as FAIL conditions:

- the gift only paraphrases what the user already told the skill
- the emotional message is generic encouragement that could fit almost anyone
- the return is only acknowledgment, validation, or sympathy with no new angle
- the gift merely mirrors the user's stated situation without adding inference, reframe, connection, question, or perspective

Good return usually comes from at least one of these:

- a non-obvious inference
- a specific external connection
- a perspective the user can plausibly offer from the relationship
- a real reframe
- a question that opens something new
- a relational signal that suggests the skill was actually thinking, not just responding

Treat these as PASS conditions:

- the gift surfaces a pattern the user has not named
- the gift connects to something outside the user's stated context
- the gift reframes something familiar into something genuinely new
- the gift asks a question the user has not considered
- the agent contributes a real perspective rather than just mirroring

If no candidate concept passes this test, do not continue to format selection yet.

Go back and regenerate with explicit attention to `Content Strategy Seeds`.

#### Content Direction Balance Check

If `./gift-history.jsonl` exists, check the last 5 entries (regardless of recipient).

This is mandatory when history is available, not advisory.

If 3 or more of those 5 are in any combination of:

- `witness`
- `portrait`
- `comfort`

then actively choose a concept in one of these directions unless there is a strong case not to:

- `extension`
- `play`
- `utility`
- `curation`
- `gift-from-elsewhere`

Freshness of content direction is part of gift quality. Don't default to `witness`-cluster just because it's easy to execute from a single photo or quote.

If `gift-history.jsonl` doesn't exist yet, skip this check.

#### Concept Quality Check

Before locking the concept, verify:

- Does this concept have its own RULES? For example, `pour compliments into soil and mushrooms grow` has rules. `A warm animation with text` does not.
- Could someone describe it as a THING, not just an EFFECT? For example, `it's an emotion cocktail machine` is a thing. `It's a nice interactive page` is not.
- Would someone want to SHOW it to a friend because the concept itself is interesting, not just because the content is personal?
- Is this concept genuinely different from the last `3` gifts the user received?

If the concept fails these checks, go back and pick a different candidate or run another cross-pollination round.

#### Concept Diversity Check

After selecting the best concept, classify it into one of these concept families:

- `borrowed-media`: gift borrows the SHELL of an existing real-world format — the format itself is the joke or the frame. Content is loaded into a recognizable container (report, app UI, ticket, newspaper, certificate, weather app, notification, receipt, album cover). The medium changes how the content FEELS. If the final artifact looks like a SCREENSHOT of something that exists in the real world, it is borrowed-media.
- `interactive-object`: gift is a virtual object the user interacts with (fish tank, piano, cocktail machine, gacha, etc.)
- `transformation`: gift takes the user's emotion or situation and transforms it into a DIFFERENT SUBSTANCE or ORGANISM — not into a document or UI. The transformation is physical/organic, not typographic. Examples: emotion becomes a cocktail being mixed, stress becomes steam being released, growth becomes a tree growing, sadness becomes rain that waters a garden, worries become laundry in a washing machine. If the result looks like a screenshot of an app or a printed document, it is borrowed-media, NOT transformation. Quick test: does it look like a SCREENSHOT? → borrowed-media. Does it look like a SCENE where something is physically happening? → transformation.
- `narrative`: gift tells a story, sends a letter, or creates a character scene (bedtime story, movie scene, imagined inner life, etc.)
- `data-viz`: gift visualizes the user's patterns as data (chat-log analysis, mood chart, personal museum, etc.)
- `game-puzzle`: gift is a lightweight game or discovery experience (mad-libs, puzzle, gacha, lucky draw, etc.)
- `real-world`: gift connects to the physical world (nudge, curation, weekend plan, etc.)
- `poetic-literary`: gift uses literary form (visual poem, haiku, book cover as art, calligraphy, etc.)

Rules:
- Do not use the same concept family more than 2 times in the last 5 gifts.
- If `borrowed-media` has been used in either of the last 2 gifts, do NOT choose borrowed-media again unless no other family can carry the return.
- Record `concept_family` in recent_gifts for tracking.
- When generating the initial 5 candidates in Step 1, ensure at least 3 different concept families are represented. If all 5 candidates fall into the same family, discard 2 and regenerate from underrepresented families.

#### Visual Element Collision Check

After deciding the concept AND the visual approach, run these two collision checks:

**Visual Element Collision (window: last 5 gifts):**

Extract the planned `visual_elements` list and compare it against the last **5** gifts in `recent_gifts`. If more than half of the planned visual elements overlap with ANY of those 5 gifts, the gift will feel visually repetitive to the user regardless of how different the concept is.

**Concept Theme Collision (window: last 7 gifts):**

Extract the planned `concept_theme` (e.g. "airport", "medical", "government") and compare it against the last **7** gifts. If the same theme appears anywhere in that window, it is a thematic collision even if visual_elements are completely different. Example: "boarding pass" and "flight delay board" both have theme "airport" → collision.

Resolution options for either collision:
- change the visual treatment entirely (e.g. from paper-document to digital-screen, from table-layout to flowing-text, from stamp-and-seal to sticker-chaos)
- change the color palette dramatically (e.g. from warm-cream to dark-terminal, from red-accent to neon-blue)
- change the concept theme (e.g. from another airport metaphor to a cooking metaphor, weather metaphor, or game metaphor)
- change the format (e.g. if the last gift was also a borrowed-media document, make this one an image or an interactive H5 with completely different visual language)

Both checks apply to every user-triggered gift. Manual invocation does not get a free pass on repetition.

Example visual collision:
- last gift visual_elements: [paper-texture, red-stamp, table-rows, handwriting-blue, cream-background]
- this gift visual_elements: [paper-texture, red-stamp, table-rows, handwriting-blue, cream-background]
- overlap: 5/5 = 100% → BLOCKED.

Example theme collision:
- gift 5 days ago concept_theme: "airport" (boarding pass)
- this gift concept_theme: "airport" (flight delay board)
- same theme within 7-gift window → BLOCKED.

#### Concept Validation Principles

Before locking the concept, check these principles:

##### 1. Visible Connection

Even if the content direction is `gift-from-elsewhere`, `play`, or `extension`, the gift must have at least one visible thread connecting it to today's conversation.

The user should feel `they heard me` not `they ignored me and sent something random`.

A light touch is enough. The connection does not need to be the main theme, but it must be present.

Example:

- user talked about work stress all day
- gift is a fun pixel fish tank under `gift-from-elsewhere`
- bad: just a fish tank with no connection
- good: one fish has a tiny tie and looks exhausted, or the fish food label says `解压饲料`

If the concept has zero connection to anything the user said or experienced today, add one before proceeding.

##### 2. Interaction Cost Must Match Energy

Rate the concept's required user effort:

- `zero`: open and receive, such as auto-play, static image or text
- `micro`: tap, swipe, or drag with one gesture type
- `low`: choose from presets or make a simple selection
- `high`: type, think, create, or answer questions

Rules:

- when the user's day was emotionally heavy, stressful, or exhausting, use only `zero` or `micro`
- when the user is in a good mood, playful, or bored, `low` or even `high` can be fine
- if unsure about the user's energy, default to `zero` or `micro`

Gifts that require the user to input their own feelings, such as typing worries, writing compliments, or answering reflective questions, can start to feel like tasks rather than gifts.

Default to giving, not asking.

If the concept requires `high` interaction, provide rich presets so the user can still just tap instead of typing.

Good concepts tend to sound like:

- `一个把今天的情绪调成鸡尾酒的调酒台，展示调制过程和最终结果`
- `一个像素风鱼缸，撒鱼食让不同颜色的小鱼来吃`
- `一个文学时钟，用文学作品里提到的时间来报时`
- `一个赛博钢琴，按提示弹出和心情匹配的小曲子`
- `一个UFO飞来把写了烦恼的文字都抓走`
- `一个奖杯花，每朵花瓣是一个成就，点击飘出文字像香气`

Bad concepts tend to sound like:

- `一个温暖的卡片上面写着鼓励的话`
- `一张好看的氛围感壁纸`
- `一段治愈的小动画`
- `一个可爱的手办形象`

The concept should make the user think `哇这个有意思`, not merely `嗯还挺好看的`.

Do not use external search to lazily source generic ideas.

Exception:

- if a world-bridging concept is already forming and needs one precise real-world connection, external search may be used to source that specific bridge

The concept should come from the collision between:

- the anchor
- the return
- the skill's judgment
- the thinking angles above
- the expanded creative seed library when cross-pollination is needed

#### Step 4: Choose the Format

After the concept is locked, choose the format that best serves it.

Format serves concept. Concept does not serve format.

If `gift_mode` is `hybrid`, decide the output format here: `h5`, `image`, or `text`.

If `gift_mode` is `h5`, `image`, or `text`, confirm that the configured format genuinely serves this concept.

For format selection, read `{baseDir}/references/gift-format-chooser.md`.

#### Format Balance Awareness

After the concept is locked and format is being chosen, glance at the last 5 gifts' formats in recent_gifts.

If all 5 are the same format (e.g. all H5, or all image), consider whether the current concept could work equally well in an underrepresented format.

This is a soft nudge, not a hard rule. If the concept genuinely needs H5, use H5 even if the last 5 were also H5. But if the concept is format-flexible and a different format would work just as well, prefer the underrepresented one for variety.

#### Concept-to-Format Fit Check

Before finalizing format, verify:

- How many distinct text blocks carry meaning in this concept? If more than 3, lean toward H5.
- Does wrong, missing, or garbled text destroy the return? If yes, must use H5 or direct text.
- Is specific date, name, number, or structured data accuracy required? If yes, must use H5.
- Is the return primarily visual or atmospheric? If yes, image is fine.
- Is the return primarily textual or structural (reports, documents, tables, multi-line annotations)? If yes, H5 is the right choice.
- Does the return depend on authored interaction, tiny choices, or paced progression? If yes, choose `h5`.

Image models cannot reliably render: correct dates, correct names, specific Chinese text beyond approximately 20 characters, multiple table rows with distinct content, or handwritten annotations alongside printed text. When the concept is text-precision-critical, H5 can simulate the same borrowed-media aesthetic (paper texture, stamps, handwriting fonts, table layouts) via CSS while guaranteeing every character is correct. When the concept is conversation-precision-critical, prefer direct `text` or an authored H5 interaction instead of forcing it into an image shell.

This check overrides speed convenience. A perfect concept delivered in the wrong format is a failed gift.

### Creative Stage Exit Gate

Before proceeding to rendering, confirm ALL of these in one pass:

Concept quality:
- [ ] `5` candidates were generated, not just one
- [ ] the chosen concept has its own rules and feels like a `thing`
- [ ] the concept family is not overused in `recent_gifts`
- [ ] the concept theme has no collision in the last `7` gifts
- [ ] the planned `visual_elements` have no greater-than-`50%` overlap with the last `5` gifts

Format fit:
- [ ] the format matches the concept and return
- [ ] the format is not over-concentrated relative to the recent format balance window
- [ ] content-direction balance has been checked against the last `5` gifts, and reflective overuse has been actively corrected when triggered

Assets ready:
- [ ] at least one relevant reference image or asset has been reviewed locally or fetched first when needed
- [ ] if the format is `h5`, the template code has been read
- [ ] if the format is `h5` and the mood is emotional, atmospheric, poetic, or contemplative, `audio_plan` is explicit
- [ ] all `text_blocks` are finalized
- [ ] `gift_context` has been written in `2-3` sentences

If any box is unchecked, do that step NOW before proceeding to rendering.

Then continue into the matching local reference:

- `h5` -> `{baseDir}/references/pattern-boundaries.md`
- `image` -> `{baseDir}/references/image-genre-chooser.md`
- `text` -> `{baseDir}/references/delivery-rules.md`

