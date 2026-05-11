# Editorial Judgment (Stage 1)

## Role

After Stage 0 intake, before any creative concept work, decide:

1. What **weight** should this gift have? (`light` / `standard` / `heavy`)
2. What **narrative direction** fits the recipient and moment?

There is no skip branch. The user already decided a gift should exist by triggering the skill.

## Core Inputs

- The recipient brief produced by Stage 0
- The evidence found in the intake material
- The user's stated emotional intent
- (If present) `./gift-history.jsonl` — recent gifts the user has made for anyone, for repetition awareness

## Judgment Principles

- Treat the recommendations below as defaults, not rigid rules.
- Let the specific recipient and specific moment matter more than relationship-type stereotypes.
- A gift should usually do one of these things: witness, encourage, explain, connect, comfort, play, commemorate, or delight.
- Heavier is not automatically better. A single `light` gift anchored on one real detail can be the most moving choice.
- If the material is thin, bias toward `light`. Do not inflate a gift to cover for missing context.

## Weight Guidelines

| Weight | When to use | Typical shape |
|---|---|---|
| `light` | sparse material; an offhand warm moment; a tiny delight; ordinary-day texture | a small echo, playful micro-piece, short poetic artifact, tiny interaction |
| `standard` | the default gift path for a meaningful but not major moment | a full creative concept in a single artifact |
| `heavy` | milestone (birthday, anniversary, retirement, graduation), major life event, long-form commemorative | rich recap, multi-scene H5, longer text, data story, commemorative piece |

**Defaults by trigger type:**

- Spontaneous inspiration from a single recent moment → `light` or `standard`
- Milestone date (birthday, anniversary, retirement) → `standard` or `heavy`
- Comforting someone through something difficult → `light` or `standard` (never heavy; heavy reads as performative during hard times)
- Celebrating an achievement → `standard` or `heavy`
- Just "I was thinking of TA" with no specific event → `light`

## Narrative Direction Categories

Choose one primary direction. The creative concept stage will elaborate.

| Direction | What it does | When to choose |
|---|---|---|
| `witness` | Tell TA the user has noticed something specific about TA — a pattern, a mood, an effort, a quiet victory. | User's main feeling is "I see TA." Works especially well when TA may feel unseen. |
| `portrait` | A proxy-character, species-of-mood, or affectionate exaggeration that says "this is so *you*" without being analytical. | The recipient has a distinctive energy the user wants to mirror back playfully. |
| `extension` | Take something TA said or shared, and carry it one step further — a song that matches a lyric TA quoted, a tiny sequel to a joke TA made. | The moment already has a seed; the gift's job is to not let it die. |
| `encouragement` | Gentle supportive framing of something TA is working through. | TA is in the middle of a hard thing; user wants to cheer without pressure. |
| `comfort` | Soft, low-stimulation, almost silent presence. | TA is hurting. A `comfort` gift should feel like someone sitting next to TA, not like a pep talk. |
| `play` | A delightful interaction or toy the recipient can play with. | TA has playful energy and a synchronous relationship with the user. |
| `curation` | A real external piece (song, article, place, story) presented with a personal note explaining why. | User encountered something that reminded them of TA. The skill's job is to frame the find, not invent the find. |
| `gift-from-elsewhere` | An unrelated delight that has nothing to do with today — a tiny surprise from the user's world to TA's. | Low-context moments; when the user just wants to drop something warm into TA's day. |
| `real-world-nudge` | Gently suggest a real-world action (call TA, visit somewhere together). | When the gift itself would be less valuable than a small push toward real life. Frame playfully. |
| `utility` | Something genuinely useful to the recipient wrapped in a creative format. | TA has an active need or project; a thoughtful useful thing beats a symbolic one. Dress it as a gift (a fake newspaper, recipe card, treasure map) — never as homework. |
| `delayed-payoff` | Two-stage gift: Stage 1 feels like play, Stage 2 reveals a connected surprise. | Best when the recipient will engage with both stages. Usually H5. |

## Direction Guidance Heuristics

**If the user said TA is going through something hard:**
- Default to `comfort` or `encouragement`, not `utility` or `play`
- Avoid teacher / mentor / advice-giving energy
- `heavy` weight is rarely right here; `light` or `standard` lands more honestly

**If the material shows TA being proud of something:**
- `witness`, `extension`, or `portrait` usually land
- Don't pivot to advice even if the user drifts that way

**If the trigger is a milestone date:**
- `standard` or `heavy`
- Any direction can work; choose based on how the user relates to TA on this specific date, not on the milestone type

**If the material is thin (one photo, one line):**
- `light` weight with `witness` or `extension` direction
- Anchor on the one specific thing you have; do not broaden

**If the recipient type suggests formality (senior colleague, mentor, in-law):**
- Avoid `play` and `portrait` unless the intake clearly shows TA has playful energy with the user
- `curation`, `witness`, and `comfort` scale better across formal relationships

## Anti-Repetition (Optional, when gift-history.jsonl exists)

If `./gift-history.jsonl` exists in the working directory, scan the last 30 entries.

Check specifically for:
- Same `recipient` receiving the same `content_direction` twice in a row → prefer a different direction
- Same `recipient` receiving the same `format` three times in the last four gifts → prefer a different format
- Across ALL recipients, overuse of `witness`-cluster (`witness` + `portrait`) in the last 5 gifts → consider `extension`, `play`, `curation`, `gift-from-elsewhere`, or `utility`

These are soft rules. If the current moment genuinely calls for the direction that repeats, use it. Mechanical diversity at the expense of emotional truth is a worse failure than repetition.

## Tone and Stance

- The gift should feel like it's from the user, made for this specific recipient, at this specific moment
- The skill's own voice should be largely invisible — it should sound like the user's own thoughtfulness amplified, not like a narrator introducing itself
- Small tonal contrast is welcome when it would genuinely help (turning irritation into playful release, brightening a sad day) but should feel intentional, not random
- Default language: the language the user and the recipient naturally use together, inferred from intake material. When unclear, ask.

## Format Deferral

Stage 1 decides weight and direction only. **Do not choose the final format here.**

Treat any explicit `format_hint` from intake only as a runtime preference to confirm later, after the creative concept is locked in Stage 2.5. If the concept genuinely wants a different format than the user requested, Stage 2.5 should surface that and ask.

## Output of Stage 1

A compact brief extension:

```
weight: light | standard | heavy
direction: <one from the table above>
stance: <one or two words — tender / playful / celebratory / quiet / warm-wry / ...>
notes_for_concept: <1-2 sentences of what should be true of the concept, before any format decision>
```

Hand this to Stage 2.
