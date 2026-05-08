# dear

中文 · [English](#english)

## 中文

> _"亲爱的 ______，我做了一份小东西想给你。"_

**dear** 是一个给 Claude Code 用的礼物 skill。当你突然想给某个人做一份电子礼物——一张水彩画、一个可以拆开的 H5、一封信、一场 6 轮的小游戏——你把你手头有的素材丢给它，它帮你把那份心意做出来。

不是每日推送，不是自动生成，不是"亲爱的用户，这是您今天的礼物"。是你自己有了灵感的那一刻，顺手跟 Claude Code 说一声：

```
/dear ~/Desktop/for-mom/
```

然后你拿到一份可以发给妈妈的东西。就这么简单。

[它能做什么](#它能做什么) · [安装](#安装) · [三种触发方式](#三种触发方式) · [它怎么做礼物](#它怎么做礼物) · [仓库结构](#仓库结构)

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

## 三种触发方式

每种方式对应一种"此刻想动手做礼物"的状态。都可以，用最省力的那种。

### 1. 扔一个文件夹（推荐）

你看到 TA 朋友圈的一张截图，翻出你们一年前的聊天记录，手机里还有 TA 的几张照片。你把它们全部丢进桌面上一个文件夹：

```
/dear ~/Desktop/for-mom/
```

skill 会读遍文件夹里的所有图片、文字、聊天记录，回你一句"我看到了 ___、___ 和 ___"，然后开始做。你不用组织语言，不用填表。

**支持的素材**：照片、截图（朋友圈/小红书/Instagram/聊天记录都行）、文字笔记、Mac 微信导出的聊天记录（`.txt` 或 `.html`）、PDF。音频和视频只读文件名。

### 2. 一句话说清楚

如果你手头没什么素材，只是心里有个画面：

```
/dear 给我朋友小A做一份礼物 — TA最近开始学陶艺
/dear 明天是我爸60岁生日，他退休一年了
/dear 想安慰一下我室友，她猫走丢三天了
```

skill 会从这句话里读出收礼人、关系、触发瞬间和情绪方向。缺什么会问一两句。

### 3. 纯空手触发

```
/dear
```

什么都没有的时候，它会用 3-4 句对话慢慢问清楚你想给谁做、为什么想做。别担心像填表——它不会问 TA 的 MBTI 和生日的。

---

## 安装

### 作为 Claude Code skill 使用

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
DEAR_HOST_DOMAIN=my-gift.surge.sh /dear ~/Desktop/for-mom/
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
/dear ~/Desktop/for-mom/
```

And getting back something you can actually send.

[What it makes](#what-it-makes) · [Install](#install) · [Three ways to invoke](#three-ways-to-invoke) · [How it works](#how-it-works)

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

## Three Ways to Invoke

### 1. Drop a folder (preferred)

You screenshot their 朋友圈, dig up last year's chat, find a few photos in your phone. Throw them all into a folder:

```
/dear ~/Desktop/for-mom/
```

The skill reads every image, text file, and chat export in the folder, tells you what it saw, and gets to work. No form-filling required.

**Supported material**: photos, screenshots (WeChat, Instagram, 小红书, chat, anything), text notes, Mac WeChat exports (`.txt` or `.html`), PDFs. Audio and video are registered by filename only.

### 2. One-line brief

If you don't have material, just a picture in your head:

```
/dear make something for my friend A — they just started pottery
/dear tomorrow is my dad's 60th birthday, a year into retirement
/dear want to comfort my roommate, her cat has been missing for three days
```

The skill extracts recipient, relationship, moment, and emotional intent from the brief. It asks at most one question if something important is missing.

### 3. Zero-argument intake

```
/dear
```

No context at all. It'll ask 3–4 short questions conversationally. It won't ask for the recipient's MBTI.

---

## Install

### As a Claude Code skill

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
