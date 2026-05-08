# Delivery Rules

Complete instructions for gift delivery across all supported formats (H5, Image, Text, Text-Play), plus the Gift Self-Sufficiency Rule and Creative Note guidelines.

## Gift Output And Delivery

Gift delivery depends on the chosen output format.

### Format Transparency Rule

Never tell the user which format you chose or are about to use. This applies to all formats.

The user should experience the gift, not be told what kind of gift it is.

For `text-play` specifically:

- start the interaction directly with the opening move
- do not preface it with meta-description of the format
- do not announce the expected number of rounds
- do not explain in advance what is about to happen unless the concept itself naturally includes that explanation in-world

### H5 Path

If the chosen format is `h5`, handle the gift in this order:

1. Generate a single HTML file that follows `html-spec.md`.
2. Save it to `./gifts/<YYYY-MM-DD>-<recipient-slug>/index.html` in the user's working directory.
3. Do one manual review pass of the HTML: verify the self-sufficiency rule, text precision, interaction clarity, and the visual quality floor.
4. If the user has a hosting domain configured (via `--domain` arg or `DEAR_HOST_DOMAIN` env var), run:
   ```
   {baseDir}/scripts/deliver-gift.sh <path-to-index.html>
   ```
   Surface the returned `url` so the user can paste it into WeChat / iMessage / email and send to the recipient themselves.
5. Without a hosting domain, report the local file path and optionally open the file in a browser so the user can preview before deciding how to deliver it.
6. The gift artifact is always the single HTML file. Hosting is a convenience layer; the file itself is the gift.

Notes:

- If deployment fails, `deliver-gift.sh` returns `delivery_mode = local_file` with a warning. Do not block the gift — surface the local path and only mention the hosting failure if it's material to the user.
- `surge` is the default provider because it has the lightest setup for non-technical users. Other providers require the user to wire their own deploy step.
- This skill **never sends the gift to the recipient directly.** The user delivers it through whichever channel fits the relationship.

### Image Path

If the chosen format is `image`, do not generate HTML. Follow:

- `{baseDir}/references/image-integration.md`

Image delivery should return generated image URLs or fallback information rather than an H5 file.

Recommended output handling:

- Save the generated image to `./gifts/<YYYY-MM-DD>-<recipient-slug>/image.png`
- Show the image inline in the chat so the user can preview
- If the provider uses an async job and the result is still pending, surface the tracking URL
- If image generation fails, fall back to rendering the gift as `h5` or `text` with the same anchor-plus-return — do not block the gift

### Proactive Interaction Rule

If the gift concept is inherently interactive (gacha machine, fortune cookie, mystery box, capsule toy, recipe wheel, etc.):

**Format decision tree:**
- Concept needs physical tap/swipe/drag → MUST be H5, not image
- Concept needs chat-based back-and-forth → MUST be text-play
- Concept can resolve in one reveal after a user choice → image + immediate follow-up invitation

**If format is image with an interactive concept:**
- The delivery message MUST include an interaction invitation in the SAME message.
- The invitation should feel like the game has already started, not like instructions.
- Good: [gacha machine image] + "🎰 The gold one on the left is glowing faintly... which one do you want to pull?"
- Bad: [gacha machine image] + [silence, waiting for user to figure out what to do]

NEVER: send an interactive-concept image → wait for user to prompt you. If you built a machine, turn it on.

### Text Path

If the chosen format is `text`, deliver the written artifact directly in the message channel.

Recommended output handling:

- send the full written gift content directly
- if an accompanying image exists, send the image first only when it truly supports the text rather than replacing it
- do not force an image or H5 wrapper around a gift that is already complete as writing

### Text-Play Path

If the chosen format is `text-play`, the gift is the live interaction itself.

Recommended output handling:

- begin with a clear opening move rather than a technical explanation
- keep the experience bounded to roughly `5-10` turns
- keep each Hermes turn to about `3-4` sentences max
- ask for minimal user effort each turn: one word, one emoji, one choice, one short line
- always carry the interaction toward a payoff: reveal, mini ending, callback, punchline, or reframe
- if the user wants to stop, close gracefully and let the existing interaction count as the gift
- do not generate files, links, or fake artifacts around it unless the concept later explicitly converts into another format

Cleanup:

- Generated HTML files are kept in `./gifts/` and are the user's to manage — the skill does not auto-delete them.
- If `./gift-history.jsonl` exists, gifts appended to it remain indexable even if the user later removes the corresponding file.

Reference:

- `{baseDir}/references/html-spec.md`
- `{baseDir}/references/image-integration.md`

### Gift Self-Sufficiency Rule

The gift artifact (image, H5, text, or text-play) must be understandable on its own, without the delivery note.

Self-sufficiency test: if the user sees ONLY the artifact and not the accompanying text, would they understand the core return?

- If yes → the gift is self-sufficient. The delivery note adds context but is not required for comprehension.
- If no → the gift is NOT self-sufficient. Options:
  1. Switch to H5 where text can be precisely controlled
  2. Simplify the concept so fewer text elements are needed
  3. Make the visual metaphor stronger so it communicates without text
  4. Ensure the key text is short enough (under ~15 Chinese characters) that the image model can render it reliably

For image-format gifts specifically:
- The image should communicate the return through visual metaphor, composition, or minimal reliable text — not through paragraphs of embedded Chinese
- If the return requires a specific sentence to land, and that sentence is too long for reliable image generation, use H5 instead
- The delivery note should enhance the gift, not explain it

For `text-play` gifts specifically:
- the interaction should not require an external explanation like "now imagine this is a game"
- the opening move should make the play legible immediately
- if the user leaves after `1-2` turns, the exchange should still feel intentional rather than broken

### Image-Text Coherence Rule

When a gift consists of image + text message (not H5), the image and the text must form a coherent unit. The user sees the image FIRST, then reads the text. If the image has no visible connection to the text, the first impression is confusion.

Coherence levels (aim for A or B):

**A: Image carries the return directly.** The image itself communicates the gift's core message. Text enhances but is not required to understand. Example: uninstall dialog screenshot → text adds "没有取消按钮"

**B: Image is a visual metaphor for the text content.** The image doesn't explain itself, but after reading the text, the user thinks "ah, that's why that image." Example: text about dual-system theory → image shows two trains on parallel tracks, one fast one slow (= system 1 and system 2)

**C: Image sets mood only (weakest, avoid).** The image is just "a nice atmospheric photo" with no connection to the specific content. Could be swapped for any other nice photo without losing meaning. Example: text about dual-system theory → image of a random tea cup on a desk

When the gift's return is primarily textual (extension, utility, curation), the image should visualize the KEY METAPHOR from the text, not just "set a mood."

Ask before generating: "If the user sees only this image and not my text, would they have any idea what this gift is about?" If no, the image needs to be more specific to the content.

### Text-Primary Gift Rule

Some gift concepts are inherently text-primary. The core value is in the written content, not the visual. Common cases include:

- observation diary or journal entries
- letters or notes to the user
- personalized analysis or insight
- story or narrative gifts
- curated recommendations with commentary

For text-primary gifts:

- The written content IS the gift artifact. It must be substantive, personal, and specific to the user.
- An image may accompany the text as atmosphere, but it cannot replace the text.
- Do not generate an image of "someone writing a diary" and call it a diary gift. Write the actual diary, letter, note, story, or commentary.
- The delivery message should contain the full written content. Any image is supplementary.
- In these cases, the self-sufficiency test applies to the written content first. The image does not need to stand alone if the text itself is the real gift.

This rule does not apply to image-primary gifts where the image itself already carries the return and the text only needs to lightly frame or land it.

Quick test:

- If you removed the image and kept only the text, would the gift still feel complete? If yes, that is correct for a text-primary gift.
- If removing the text makes the gift meaningless, but the text was never actually written, the gift is incomplete.

### Creative Note (occasional)

Once every 5-10 gifts, optionally append a brief "创作手记" to the gift delivery message — a 1-2 sentence note about how the gift concept was chosen.

Good examples:
- "今天想了5个方案，最后选了这个因为你上周说过喜欢‘安静的史诗感’"
- "本来想做成一个会动的小页面，但觉得今天的氛围更适合一张安静的图"
- "这个创意其实是从你分享的那张专辑封面来的灵感"

Rules:
- Adapt tone and length to the user's communication style
- Scarcity makes it special — do not attach to every gift
- Never reveal the full creative process or calibration plan — just one small genuine peek
- Never feel forced or performative — only include when there is a genuinely interesting behind-the-scenes detail worth sharing
- Track in recent_gifts whether the last gift included a creative note; avoid including one in consecutive gifts

## Delivery Message Tone

The message accompanying a gift should NOT follow a fixed formula. Match the tone dynamically.

**Signals to read before writing the delivery message:**
1. The user's own language/tone in the intake conversation — match it, don't invent a persona
2. The gift mood — is this gift warm? funny? deep? light?
3. The user's apparent energy — playful and expectant, or quiet and tender?
4. How closely the user already relates to the recipient (casual friend vs. estranged parent vs. new coworker) — this changes how much the delivery message should frame vs. step aside

**Tone range examples:**

Playful/funny gift + user in good spirits:
- "hehe caught you ✧ today's delivery~"
- "🎁 ding dong~ someone's package arrived, sign for it?"
- "wait wait wait, you HAVE to see this ↓↓↓"

Warm/deep gift + user seems tired:
- "for you."
- "today's you deserves this."
- [no text — just deliver the artifact directly]

Casual/light daily gift:
- "passing by, dropping this off~"
- "✨" (a single emoji is enough)

**Anti-patterns:**
- "Here is today's gift that I prepared for you:" ← robot template
- "Based on today's conversation, I have generated..." ← exposes internal process
- Same sentence structure every time ← the worst problem

**Rules:**
- The last 3 delivery messages must NOT share the same sentence structure.
- Emoji frequency should follow the user's own style. If the user uses them freely in intake, use them freely in delivery. If the user is minimal, use sparingly.
- Default to medium warmth when the user's style is unclear.
- Delivery message length range: 0 words (just send the artifact) to 2-3 sentences max. Never longer.
- The delivery language must match the user's primary language, regardless of what language these reference docs are written in.

