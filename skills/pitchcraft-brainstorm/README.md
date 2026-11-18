# pitchcraft-brainstorm

Turn a rough idea into a finished session title and abstract for a conference, meetup, internal event or academic venue. Your agent works with you in short rounds of multiple-choice questions, so it feels like tapping through a quick questionnaire, not filling in a long form.

It works for talks, workshops, panels, keynotes and lightning talks. You can start from scratch, or from an existing talk, slide deck, paper, blog post or rough draft.

> Not installed yet? See [Installation](../../README.md#installation) in the main README.

## Starting a session

Just describe what you need. Any of these will trigger the skill:

- "Help me write a CFP abstract for my talk on platform engineering."
- "I have a blog post about Rust in embedded systems. Turn it into a workshop submission for EmbeddedConf."
- "My title is boring. Can you help me rework it?"

In Claude Code you can also call it directly with `/pitchcraft-brainstorm`, and in Codex with `$pitchcraft-brainstorm`.

**Tip:** the more you put in your first message (event name, audience, word limits, a link to your draft), the fewer questions you'll get. The skill never asks for something you've already told it.

## How a session works

### 1. Context (about 3 short rounds)

| Round | What it asks |
| --- | --- |
| **A. The basics** | Event type, session type, starting point, audience level |
| **B. Voice and limits** | Tone, title and abstract length limits, an optional past session to copy the style of, style guardrails (no buzzwords, no emojis, ...) |
| **C. The facts** | One short message asking for what only you know: event name and theme, your idea in a sentence or two, and any source material |

The agent then sums up what it gathered, including the language it will write in, and asks you to confirm.

### 2. Title

You get **4 candidates**, each from a different angle: benefit-led, curiosity, bold claim and plain descriptive. Each one shows its character count. Pick the closest one (or mix several), say what to change (shorter, more specific, more playful, less jargon, add a subtitle, ...) and iterate until you choose **Lock this title**.

### 3. Abstract

First you pick the length, the structure (hook, what it covers, takeaways, who it's for, speaker bio, call to action) and the formatting (plain text, Markdown, Markdown with links, or whatever the event's form accepts). The agent then drafts the abstract and you refine it round by round until you choose **Looks good, finalize**.

The full current draft is always shown, both as a message and inside the question, so you never have to answer about text you can't see.

### 4. Final delivery

You get the final title and abstract in one copy-ready block, plus a one-line limits check:

```
# Kubernetes Is Lying to You   (26 chars)

<your abstract>   (142 words)

Title 26/80 chars, abstract 142/150 words
```

From there you can stop, ask for a shorter version, ask for a version in another tone, or export it as Markdown, plain text or Word.

## Answering questions

- **Pick options.** If your agent has a question tool (Claude Code, Codex and others), you'll get clickable options. Otherwise you'll see a numbered list and can reply with something like `1a, 2c`.
- **Or just type.** Free text always counts as a full answer: "make it funnier and drop the bullet points" works anywhere.
- **Recommended options** are listed first and marked **(Recommended)**.
- Every round starts with a status line so you can see your progress:
  `Round 3 · Title (locked): "..." · Abstract draft v2 · 112/150 words`

## Saving and resuming

Sessions are saved automatically as plain JSON files, so you can stop and pick up later in a new conversation, or even with a different agent.

**Where they're saved**, from highest to lowest priority:

1. A folder you name in the chat ("save my sessions in `./cfp`")
2. The `PITCHCRAFT_DIR` environment variable
3. `~/.pitchcraft/sessions/` (the default)

Each session is a single file named after the date and topic, for example `2026-11-18-ai-agents-keynote.json`.

**When it saves:** after you confirm the context, when you lock a title, after each abstract draft, and when you finalize.

**Resuming:** when you start the skill and saved sessions exist, the first question offers to resume one of your 3 most recent sessions (or start a new one). The agent picks up from where you left off and skips everything the file already answers.

**What's stored:** facts and drafts only (your event details, settings, the current title and abstract, and titles you rejected, so they aren't proposed again). The chat itself isn't saved.

**No file access?** In environments that can't write files, such as some web chats, the agent tells you once and gives you a copy-ready JSON block at each checkpoint instead. Paste it into a later conversation to resume.

## Good to know

- **Limits are strict.** Character and word counts appear next to every draft. When a code tool is available, the agent uses it to verify tight limits.
- **No invented facts.** The agent asks rather than guessing details about you, your event or your content.
- **Your language.** It writes in the language you use, unless you ask for another.
- **Style, not sentences.** If you share a past session as inspiration, the agent copies its style (sentence length, voice, humor, structure) but never its wording.
