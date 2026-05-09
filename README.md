# dear

中文 · [English](#english)

## 中文

> _"亲爱的 ______，我做了一份小东西想给你。"_

**dear** 是一个给 Claude Code 用的礼物 skill。当你突然想给某个人做一份电子礼物——一张水彩画、一个可以拆开的 H5、一封信、一场 6 轮的小游戏——你把你手头有的素材丢给它，它帮你把那份心意做出来。

不是每日推送，不是自动生成，不是"亲爱的用户，这是您今天的礼物"。是你自己有了灵感的那一刻，顺手跟 Claude Code 说一声：

```
/dear
```

然后把照片、聊天截图、朋友圈截图直接拖进来，回答一两个问题，就能拿到一份可以发给 TA 的东西。就这么简单。

[它能做什么](#它能做什么) · [最省力用法](#最省力用法) · [安装](#安装) · [三种触发方式](#三种触发方式) · [它怎么做礼物](#它怎么做礼物) · [仓库结构](#仓库结构)

---

## 它能做什么

| 格式 | 举例 |
|---|---|
| **H5 互动页面** | 一个会被手指擦开的雨窗；一台只为 TA 造的复古点唱机；一个每点一下就更歪的陶艺转盘；一封要拆开三层才能看到的信 |
| **AI 生成图片** | 一张把 TA 养的多肉画成水彩的"外婆的花园"；一张写着 TA 名字的假电影票；一张 TA 的情绪气象图 |
| **文字礼物** | 一封仿照 TA 最喜欢那部电影结构写的信；一篇假装是 TA 自己写的日记；一段对 TA 最近状态的温柔观察 |
| **互动文字游戏** | 一场 6 轮的 emoji 猜谜，谜底是 TA 的近况；一个把 TA 变成小剧场主角的一人游戏；一张只在聊天里展开的问答卡 |

格式不是你选的——是 skill 根据你提供的素材和想表达的情感自己决定的。你只负责把你的灵感和素材丢过来。

---

## 最省力用法

如果别人已经帮你安装好了，你只需要：

1. 在 Claude Code 输入 `/dear`
2. 把照片、聊天截图、朋友圈截图直接拖进来
3. 回答 1-2 个问题
4. 等 Claude 做好

素材很多时，再把它们整理成一个文件夹并把路径发给 `/dear`。

---

## 三种触发方式

每种方式对应一种"此刻想动手做礼物"的状态。都可以，用最省力的那种。

### 1. 拖素材进聊天（推荐）

最省力的方式是先输入：

```
/dear
```

然后直接把照片、聊天截图、朋友圈 / 小红书 / Instagram 截图拖进 Claude Code。skill 会把这些图片当作素材读取，回你一句"我看到了 ___、___ 和 ___"，再问最多一两个关键问题。

**支持的素材**：照片、截图（朋友圈/小红书/Instagram/聊天记录都行）、文字片段、文字笔记、Mac 微信导出的聊天记录（`.txt` 或 `.html`）、PDF。音频和视频只读文件名。

### 2. 扔一个文件夹（素材很多时推荐）

如果素材很多，或者已经整理成一批文件，把它们放进桌面上的一个文件夹：

```
/dear ~/Desktop/for-mom/
```

skill 会先列出文件，再读取里面的图片、文字、聊天记录和 PDF。你不用组织语言，不用填表。

### 3. 一句话说清楚

如果你手头没什么素材，只是心里有个画面：

```
/dear 给我朋友小A做一份礼物 — TA最近开始学陶艺
/dear 明天是我爸60岁生日，他退休一年了
/dear 想安慰一下我室友，她猫走丢三天了
```

skill 会从这句话里读出收礼人、关系、触发瞬间和情绪方向。缺什么会问一两句。

### 4. 纯空手触发

```
/dear
```

什么都没有的时候，它会用 3-4 句对话慢慢问清楚你想给谁做、为什么想做。别担心像填表——它不会问 TA 的 MBTI 和生日的。

### 模板模式：直接选一个已经设计好的礼物形状

如果你已经知道想要哪种礼物，可以直接指定模板：

```bash
/dear --template paper-house ~/Desktop/for-mia/
/dear --template bouquet 给妈妈做一束可以拖动的花
/dear 用 bouquet 模板给朋友做一份生日礼物
/dear 有什么模板可以用？
```

当前一等模板：

| 模板 | 适合 | 预览 | 一句话 |
|---|---|---|---|
| `paper-house` | 伴侣、周年、很亲密的朋友、长故事 | `assets/templates/paper-house/preview.jpg` | 四个小房间，每个房间点开一段回忆。 |
| `bouquet` | 生日、母亲节、感谢、朋友安慰、纪念日 | `assets/templates/bouquet/preview.jpg` | 可拖拽花材、自由加宝石、可改小纸片内容的互动花束。 |

`bouquet` 比 paper-house 轻，但比纯图片更可玩；用户不需要理解内部 schema，只要提供收礼人素材、想要的花束感觉和几段可写进小纸片的内容。

---

## 安装

### 如果别人已经帮你安装好了

打开 Claude Code，直接输入：

```
/dear
```

然后把照片、截图或文字拖进聊天里就可以开始。你不需要知道 skill 文件夹在哪，也不需要运行命令。

### 给安装者 / 开发者

把这个文件夹放到 Claude Code 能找到 skill 的位置：

- 全局：`~/.claude/skills/dear/`
- 或者项目内：`.claude/skills/dear/`

让脚本可执行：

```bash
chmod +x scripts/*.sh
```

然后在 Claude Code 里直接：

```
/dear
```

### 可选配置

核心功能不依赖任何外部服务。下面这些都是增强能力：

| 服务 / 环境变量 | 用来做什么 |
|---|---|
| `surge.sh` + `DEAR_HOST_DOMAIN` | H5 礼物一键部署到公网，拿到可以直接丢微信发给 TA 的链接 |
| `OPENROUTER_API_KEY` | 图片生成（OpenRouter 路径） |
| `GEMINI_API_KEY` | 图片生成（Gemini 直连） |
| `GOOGLE_API_KEY` | 图片生成（Google AI） |
| `FREESOUND_API_KEY` | H5 背景音乐搜索 |
| `REMOVE_BG_API_KEY` | 图片抠图 |

没有任何 key 的情况下，skill 会用文字、H5 和互动小游戏完成你的请求。

H5 礼物部署示例：

```bash
DEAR_HOST_DOMAIN=my-gift.surge.sh /dear
```

或者在调用 skill 之后手动运行：

```bash
./scripts/deliver-gift.sh ./gifts/2026-05-06-mom/index.html --domain my-gift.surge.sh
```

---

## 它怎么做礼物

每一份礼物都经过六个内部阶段：

```
0. 素材录入      你扔进来的文件夹 / 一句话 / 对话里提到的事
     ↓
1. 编辑判断      这份礼物应该多重？走哪个叙事方向？
     ↓
2. 素材综合      从素材里找到最值得做成礼物的锚点
     ↓
3. 创意构思      生成 5+ 个创意方向，做质量和多样性检查，选最好的
     ↓
4. 视觉策略      选格式、定风格、准备素材计划
     ↓
5. 渲染交付      生成最终产物、自检、交给你
```

### 有证据

每一个具体细节——TA 喜欢的颜色、你们聊过的一家面馆、TA 说过的一句话——都必须能追溯回你提供的素材。没有凭空发明的 TA。详见 `references/gifting-ethics.md`。

### 不暴露

skill 不会在做的过程中告诉你"我选了 H5 格式，现在在生成，刚才失败了一次，正在重试"。你只会看到：做之前的一句"等我一下～"，做完的礼物，和一两句温柔的话。

### 不代发

skill 只做礼物。发给 TA 这一步永远是你自己做——通过微信、邮件、iMessage，或者打印出来贴在冰箱上。

---

## 仓库结构

```
dear/
├── SKILL.md                       # skill 入口
├── references/                    # 所有子阶段的参考文档
│   ├── recipient-intake.md        # Stage 0：素材录入的三种方式
│   ├── main-flow.md               # 总流程 + 进度播报 + text-play 规则
│   ├── editorial-judgment.md      # Stage 1：重量 + 叙事方向
│   ├── gifting-ethics.md          # 给"别人"做礼物的原则
│   ├── creative-concept.md        # Stage 2 + 2.5
│   ├── creative-seed-library.md
│   ├── gift-format-chooser.md     # 格式选择器
│   ├── delivery-rules.md          # 交付规则
│   ├── stage3-visual-strategy.md
│   ├── stage4-visualization.md
│   ├── pattern-cards/             # H5 pattern 卡
│   └── image-genres/              # 图片风格卡
├── assets/
│   └── templates/                 # H5 模板（p5.js）
├── scripts/
│   ├── deliver-gift.sh            # H5 本地 / 部署分发器
│   ├── deploy.sh                  # surge 部署
│   ├── render-image.sh            # 图片生成
│   ├── remove-bg.sh               # 抠图
│   ├── fetch-music.sh             # 背景音乐
│   └── fetch-asset-bundle.sh      # 按需下载参考素材
├── gift-history.example.json
├── gift-history.schema.json
└── README.md
```

---

## 运行要求

- `bash` · `python3` · `curl` · `unzip`
- 可选：`surge`（H5 在线托管）

---

## 本 skill 的来源

这个 skill 是从一个叫 [hermes-daily-gift](https://github.com/nicekate/hermes-daily-gift) 的项目改造来的——那是一个 Hermes Agent 每天定时给用户送礼物的 skill。dear 保留了它的核心：五阶段创意工作流、创意 seed 库、pattern cards、image genres、H5 templates。但是删掉了所有"agent 自主决策 + 定时任务"的部分，把它改造成了"人类随时可以给另一个人做一份礼物"。感谢原作者让这个脊柱变得如此扎实。

---

---

[中文](#中文) · English

## English

> _"Dear ______, I made something for you."_

**dear** is a gift-crafting skill for Claude Code. When you're hit with inspiration to make a digital gift for someone specific — a watercolor painting for your mom, an interactive H5 for your best friend, a letter shaped like your partner's favorite movie, a 6-turn emoji riddle for a colleague — you hand your raw material to the skill, and it turns the thought into the thing.

No daily pushes. No autonomous schedule. No "Dear user, here is today's gift." Just you, in your own moment of inspiration, telling Claude Code:

```
/dear
```

Then dragging in photos, chat screenshots, or social screenshots, answering one or two questions, and getting back something you can actually send.

[What it makes](#what-it-makes) · [Easiest use](#easiest-use) · [Install](#install) · [Three ways to invoke](#three-ways-to-invoke) · [How it works](#how-it-works)

---

## What It Makes

| Format | Examples |
|---|---|
| **Interactive H5** | A rain-streaked window you wipe clean to read the message; a jukebox built just for one person; a pottery wheel that gets more wobbly with each tap; a letter hidden inside three layers of wrapping |
| **AI-generated image** | A watercolor of your mom's succulent garden; a fake movie ticket with the recipient's name on it; a mood-weather map for the day |
| **Text artifact** | A letter written in the three-act rhythm of your partner's favorite movie; a diary in their voice; a short, specific observation about them |
| **Interactive text-play** | A 6-turn emoji riddle whose answer is your friend's recent week; a tiny one-player play that casts them as the hero; a set of question cards that only unfold in chat |

You don't pick the format. The skill picks based on the material you provide and the emotion you're trying to convey.

---

## Easiest Use

If someone else already installed the skill for you:

1. Type `/dear` in Claude Code
2. Drag in photos, chat screenshots, or social screenshots
3. Answer 1-2 questions
4. Wait for Claude to make the gift

Use a folder path when you have lots of material already organized.

---

## Three Ways to Invoke

### 1. Drag material into chat (preferred)

The lowest-friction path is:

```
/dear
```

Then drag photos, chat screenshots, 朋友圈 / 小红书 / Instagram screenshots directly into Claude Code. The skill treats them as intake material, tells you what it saw, and asks at most one or two key questions.

**Supported material**: photos, screenshots (WeChat, Instagram, 小红书, chat, anything), pasted text, text notes, Mac WeChat exports (`.txt` or `.html`), PDFs. Audio and video are registered by filename only.

### 2. Drop a folder (recommended when there is lots of material)

If you already have a batch of files, put them in a folder:

```
/dear ~/Desktop/for-mom/
```

The skill lists the folder first, then reads the images, text files, chat exports, and PDFs it can use. No form-filling required.

### 3. One-line brief

If you don't have material, just a picture in your head:

```
/dear make something for my friend A — they just started pottery
/dear tomorrow is my dad's 60th birthday, a year into retirement
/dear want to comfort my roommate, her cat has been missing for three days
```

The skill extracts recipient, relationship, moment, and emotional intent from the brief. It asks at most one question if something important is missing.

### 4. Zero-argument intake

```
/dear
```

No context at all. It'll ask 3–4 short questions conversationally. It won't ask for the recipient's MBTI.

### Template mode: choose a pre-designed gift shape

If you already know the shape you want, specify a template directly:

```bash
/dear --template paper-house ~/Desktop/for-mia/
/dear --template bouquet make mom a draggable bouquet
/dear use the bouquet template for a friend's birthday gift
/dear show me templates
```

First-class templates:

| Template | Best for | Preview | One-liner |
|---|---|---|---|
| `paper-house` | anniversaries, partners, very close friends, longer stories | `assets/templates/paper-house/preview.jpg` | Four small rooms, each opening into a memory. |
| `bouquet` | birthdays, Mother's Day, thank-you gifts, friend comfort, anniversaries | `assets/templates/bouquet/preview.jpg` | 可拖拽花材、自由加宝石、可改小纸片内容的互动花束. |

`bouquet` is lighter than paper-house but more playful than a static image. The user does not need to understand the internal schema; they only provide recipient material, bouquet mood, and card-worthy details.

---

## Install

### If someone already installed it for you

Open Claude Code and type:

```
/dear
```

Then drag photos, screenshots, or text into the chat. You do not need to know where the skill folder lives or run any shell commands.

### For installers / developers

Place this folder where Claude Code looks for skills:

- Global: `~/.claude/skills/dear/`
- Or project-scoped: `.claude/skills/dear/`

Make scripts executable:

```bash
chmod +x scripts/*.sh
```

Then in Claude Code:

```
/dear
```

### Optional configuration

Core functionality needs no external services. These just unlock extra capabilities:

| Service / env var | Purpose |
|---|---|
| `surge.sh` + `DEAR_HOST_DOMAIN` | One-command deploy of H5 gifts to a public URL you can paste into chat |
| `OPENROUTER_API_KEY` | Image generation (OpenRouter path) |
| `GEMINI_API_KEY` | Image generation (direct Gemini) |
| `GOOGLE_API_KEY` | Image generation (Google AI) |
| `FREESOUND_API_KEY` | H5 background music search |
| `REMOVE_BG_API_KEY` | Background removal for compositing |

Without any keys, the skill still produces text, H5, and text-play gifts.

Deploy an H5 gift:

```bash
DEAR_HOST_DOMAIN=my-gift.surge.sh /dear ~/Desktop/for-mom/
```

Or after generation:

```bash
./scripts/deliver-gift.sh ./gifts/2026-05-06-mom/index.html --domain my-gift.surge.sh
```

---

## How It Works

Every gift passes through six internal stages:

```
0. Intake            Whatever you handed over — folder, brief, conversation
     ↓
1. Editorial         How heavy? What narrative direction?
     ↓
2. Synthesis         Find the single anchor that deserves the center
     ↓
3. Creative concept  Generate 5+ candidates, quality + diversity check, pick
     ↓
4. Visual strategy   Choose format, style, asset plan
     ↓
5. Render & deliver  Produce the artifact, self-check, hand to you
```

### Evidence-based

Every specific detail — a color TA likes, a place you've been together, a line TA said — must trace back to something you actually provided during intake. The skill never invents facts about the recipient. See `references/gifting-ethics.md`.

### No internal leakage

The skill doesn't narrate format choices, retries, or error recovery. You see: a warm "working on it" line, the gift, and one or two sentences of context. That's it.

### You deliver, not the skill

The skill produces artifacts. You send them — through WeChat, email, iMessage, or printed on the fridge. The skill never contacts the recipient directly.

---

## Repo structure

```
dear/
├── SKILL.md                       # Skill entry
├── references/                    # Stage-by-stage reference docs
│   ├── recipient-intake.md        # Stage 0: three intake modes
│   ├── main-flow.md               # Overall flow + progress rules + text-play
│   ├── editorial-judgment.md      # Stage 1: weight + direction
│   ├── gifting-ethics.md          # Principles for gifts-for-others
│   ├── creative-concept.md        # Stage 2 + 2.5
│   ├── creative-seed-library.md
│   ├── gift-format-chooser.md
│   ├── delivery-rules.md
│   ├── stage3-visual-strategy.md
│   ├── stage4-visualization.md
│   ├── pattern-cards/
│   └── image-genres/
├── assets/
│   └── templates/                 # H5 templates (p5.js)
├── scripts/
│   ├── deliver-gift.sh            # Local/deploy bridge
│   ├── deploy.sh                  # surge deploy
│   ├── render-image.sh
│   ├── remove-bg.sh
│   ├── fetch-music.sh
│   └── fetch-asset-bundle.sh
├── gift-history.example.json
├── gift-history.schema.json
└── README.md
```

---

## Requirements

- `bash` · `python3` · `curl` · `unzip`
- Optional: `surge` (hosted H5 previews)

---

## Origin

This skill is a fork and rework of [hermes-daily-gift](https://github.com/nicekate/hermes-daily-gift), originally built as an autonomous daily-gift engine for the Hermes Agent. The five-stage creative spine, creative seed library, pattern cards, image genres, and H5 templates are all inherited. The autonomous-agent scaffolding (cron, SOUL/USER persona files, long-term memory, scheduled delivery) has been removed and replaced with human-triggered, recipient-centered intake. Thanks to the original author for the depth of the creative pipeline.
