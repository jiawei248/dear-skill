# Recipient & Moment Intake (Stage 0)

Before any creative work, establish who the gift is for and what moment triggered the inspiration. This stage replaces the original skill's reliance on an always-on agent with long-term memory — in Claude Code, context must come from what the user provides *right now*.

There are three entries. All three converge on the same goal: produce a **recipient brief** the rest of the pipeline can work from. Pick the entry with the lowest friction for the user's current state.

## Three Intake Entries

### Entry A: Folder Drop (preferred for rich inspiration moments)

The user collects raw material into a folder, then invokes:

```
/dear ~/Desktop/for-mom/
```

In Claude Code, do not try to `Read` the directory itself. First list the files, then read individual supported files. Default to one level of recursion; do not recurse indefinitely.

Folder-reading procedure:

1. Use `find` or `ls` to list files in the folder, including one nested level by default.
2. Read in priority order: images/screenshots first, text/chat exports second, PDFs third, structured notes after that.
3. If the folder contains many files or very large files, summarize the inventory first and ask which ones matter before reading everything.
4. For unsupported files, be explicit: "I can see the filename, but I could not read the content."

Readable formats:

| File type | How to read | What to extract |
|---|---|---|
| `.png` `.jpg` `.jpeg` `.webp` `.heic` | `Read` (Claude is multimodal) | Chat screenshots → OCR + sentiment; photos of TA → appearance notes, setting; 朋友圈/小红书/Instagram screenshots → what TA cares about lately |
| `.txt` `.md` | `Read` | Chat exports, notes the user typed, quotes |
| `.html` | `Read` | WeChat HTML exports, saved web pages |
| `.pdf` | `Read` (up to 20 pages) | Articles, saved posts, long-form |
| `.json` | `Read` | If the user prepped structured notes |
| Audio / video | Skip content; use filename + `ffprobe` if available for metadata only | Treat as reference material the user is aware of, not to be directly analyzed |

After reading, always:

1. Produce a short "I see..." readback for the user (2–4 sentences), listing the concrete evidence the skill found. Example:

   > 我在这个文件夹里看到了：三张你妈在院子里种多肉的照片（其中一张她笑得特别开心），一段你和她两周前的微信聊天（她在抱怨膝盖），还有一张你截的她朋友圈——她转了一篇关于"空巢老人怎么找乐子"的文章。

2. Ask at most ONE clarifying question:

   - If recipient relationship is unclear → "这是给谁的？"
   - If trigger moment is ambiguous → "你想让这份礼物回应的是哪件事？"
   - If emotional intent is unclear → "你主要想让 TA 感到什么——被看见 / 被逗笑 / 被惦记？"

   If all three are inferrable from the material, skip the question and proceed.

3. Proceed to Stage 1 without further Q&A.

### Entry B: One-Line Brief

```
/dear 给我朋友小A做一份礼物 — TA最近开始学陶艺
/dear 明天是我爸60岁生日，他退休一年了
/dear 想安慰一下我室友，她猫走丢三天了
```

Parse the brief for: recipient, relationship, moment, emotional intent.

If any of the four is missing, ask ONE question to fill the most important gap. Do not turn this into a four-question form. If the user wanted to answer four questions they would have used Entry C.

If the brief is rich enough, proceed directly to Stage 1.

### Entry C: Zero-Argument Interactive Intake

```
/dear
```

No context at all — the user just triggered. Ask 3–4 short questions conversationally, one at a time, waiting for each answer:

1. "这份礼物是给谁的？和 TA 是什么关系？"
2. "是什么瞬间让你想给 TA 做一份礼物的？"（open-ended — let the user vent, TA will leak signal naturally）
3. "你主要想让 TA 感到什么？"（or suggest 2–3 options: 被看见 / 被逗笑 / 被惦记 / 被安慰）
4. (Optional) "你手头有什么素材吗？可以截图、照片、一句TA说过的话、一首歌名——任何都可以，没有也完全没关系。"

Keep tone warm and conversational, not form-like. Do NOT ask follow-ups like "TA的爱好是什么"「TA是什么性格」— the point of this skill is to **work from a single concrete moment**, not build a profile.

After Q&A, if the user mentioned raw material but didn't provide files, suggest the lowest-friction path first:

> 你可以直接把截图 / 照片拖到这里；如果素材很多，也可以告诉我文件夹路径，我会先列出文件再逐个读取。

## Mixed Entries

Users often mix: "/dear ~/Desktop/for-mom/ 主要是想安慰她一下，她最近身体不太好"

Always honor both: read the folder AND absorb the inline hint.

Dragging images into the Claude Code chat also counts as raw material — treat inline images the same as folder images.

## WeChat Chat Export (macOS)

If the user says "我想用和 TA 的微信聊天记录做一份"：

1. **Mac WeChat**: Right-click the conversation → `导出聊天记录` → save as `.txt` or `.html`. Point the skill at the resulting file.
2. **No export option available**: user can screenshot the relevant parts of the chat. The skill reads screenshots natively — this is often the lowest-friction path. Even 3-5 screenshots is enough signal.
3. **iMessage on Mac**: no easy export; screenshots are the practical path.
4. **Instagram / Twitter / 小红书 / 朋友圈**: screenshot. Claude reads the image content + any visible text directly.

When reading a chat export:
- Focus on messages that carry emotional or factual weight (TA shared something, complained about something, celebrated something, asked about the user)
- Ignore scheduling chatter, small talk, "哈哈哈" chains
- Pay attention to what TA talked about *most recently* — recency often signals what TA has headspace for

## The Recipient Brief (Internal)

After intake, the skill should have an internal working brief roughly this shape (no need to serialize unless helpful):

```
recipient:
  name_or_nickname: "妈" / "小A" / "Ren" ...
  relationship: parent | partner | friend | colleague | kid | ...
  language: the language TA and the user use together
moment:
  trigger: what the user just noticed / saw / felt that made them want to make this
  evidence: concrete things pulled from the material — direct quotes, visible facts, specific details
emotional_intent:
  primary: seen | celebrated | comforted | amused | remembered | nudged | ...
  stance: how the user relates to TA right now (tender / playful / frustrated-but-caring / ...)
material_inventory:
  photos: [...]
  chat_excerpts: [...]
  other: [...]
format_hint:
  explicit: h5 | image | text | none
  suggested: based on material (e.g. lots of photos → leans image; text-heavy → leans text or h5)
```

This brief becomes the input to Stage 1 and beyond. Every later stage that invents a specific detail must be able to point to one of the `evidence` entries. That is the evidence rule enforced by `gifting-ethics.md`.

## Evidence Readback (recommended before Stage 1)

If the material is rich (folder drop), show the user the 3-5 most gift-worthy signals you extracted before committing to a direction. One line each, like:

> 我感觉最值得做成礼物的几个细节是：
> - TA 在那张照片里笑得特别松弛，和你上次提到"TA 最近压力大"形成一个温柔的对比
> - TA 转的那篇文章里一句话："其实我也想找点喜欢的事做"
> - 你们聊天最后你没回 TA 那条"我膝盖又疼了"

This gives the user a chance to redirect before the skill commits creative energy to the wrong anchor. Keep it short — don't turn it into a report.

## What NOT to do at intake

- Do NOT ask the user to fill out a structured recipient profile (age, birthday, hobbies, aesthetic preferences, MBTI...). That is a CRM, not a gift.
- Do NOT ask more than 4 questions total in Entry C.
- Do NOT infer a rich personality portrait from thin material. If the material is thin, make the gift accordingly modest — a `light` weight gift with a specific, small anchor is better than a `heavy` gift built on guesses.
- Do NOT treat inline profanity, venting, or emotional complaints about the recipient as material for the gift itself. Those tell you about the user's relationship, not about what the recipient would enjoy receiving. See `gifting-ethics.md`'s privacy section.
