# pitchcraft-brainstorm

Turn a rough idea into a finished session title and abstract for a conference, meetup, internal event or academic venue. Your agent works with you in short rounds of multiple-choice questions, so it feels like tapping through a quick questionnaire, not filling in a long form.

It works for talks, workshops, panels, keynotes and lightning talks. You can start from scratch, or from an existing talk, slide deck, paper, blog post or rough draft.

> Not installed yet? See [Installation](../../README.md#-installation) in the main README.

## Questions to try

Copy any of these into your agent to use a feature of the skill.

| I want to... | Ask something like |
| --- | --- |
| Write a title and abstract from scratch | "Help me write a title and abstract for a 30-minute talk on platform engineering at DevOpsCon." |
| Start from existing material | "Turn this blog post into a workshop abstract for EmbeddedConf." (paste the text, attach a file or give a URL) |
| Improve a draft I already have | "My title is boring. Here's my current abstract, can you rework both?" |
| Respect submission limits | "Title up to 80 characters, abstract up to 150 words. Show me the counts." |
| Write in a specific voice | "Keep it practical and plain-spoken. No buzzwords, no emojis, no questions in the title." |
| Copy the style of something I like | "Use the style of this abstract as a reference, but don't copy its wording." (text, file or URL) |
| Explore title options | "Give me 4 title candidates from different angles, then mix the first and third." |
| Change a draft in a specific way | "Make the opening stronger and the takeaways more concrete." |
| Write in another language | "Write the whole thing in Spanish." |
| Save my progress | "Save this session as a file." (download or on screen, your choice) |
| Continue a previous session | "Resume this session." (paste or attach the session file, or give a URL) |
| Convert something into a session file | "Convert this abstract and these notes into a session file." |
| Convert samples into a writing style | "Turn these three past abstracts into a writing style file." |
| Reuse my writing style later | "Save this writing style so I can use it next time." |
| Get the result in a shareable format | "Export the final title and abstract as Word." |
| Get a shorter or different-tone version | "Give me a shorter version, and one in a more playful tone." |

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
| **B. Voice and limits** | Tone, title and abstract length limits, an optional writing style to follow (text, file or URL), style guardrails (no buzzwords, no emojis, ...) |
| **C. The facts** | One short message asking for what only you know: event name and theme, your idea in a sentence or two, and any source material and your writing style reference, as text, a file or a URL |

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

From there you can stop, save the session file, ask for a shorter version, ask for a version in another tone, or export the text as Markdown, plain text or Word.

## Answering questions

- **Pick options.** If your agent has a question tool (Claude Code, Codex and others), you'll get clickable options. Otherwise you'll see a numbered list and can reply with something like `1a, 2c`.
- **Or just type.** Free text always counts as a full answer: "make it funnier and drop the bullet points" works anywhere.
- **Recommended options** are listed first and marked **(Recommended)**.
- Every round starts with a status line so you can see your progress:
  `Round 3 · Title (locked): "..." · Abstract draft v2 · 112/150 words`

## Saving and resuming

Nothing is stored on your machine or in the agent's memory, so the skill behaves the same in every LLM client. The conversation is the only state. When you want to keep something, the agent hands it to you as a Markdown document, and you bring it back later.

**Saving:** the first time you save, the agent asks once how you want it: **Download a file** (when the environment can hand one over) or **Show it on screen** in a copy-ready block. You can also ask for another format such as plain text or Word. It remembers your choice for the rest of the session.

**When it offers:** after you confirm the context, when you lock a title, occasionally while refining the abstract, and at the end. It's always an optional extra, never a blocker, and you can ask for the file at any moment ("save this").

**Resuming:** start a new conversation, pick **Resume a saved session file** as the starting point, and paste the file, attach it or give a URL. The agent skips everything the file already answers and continues from where you stopped.

**Templates and examples:** blank copies of both file formats are in [`templates/`](templates/) and filled-in fictional samples in [`examples/`](examples/).

**What's in the file:** facts and drafts only (event details, settings, the current title and abstract, and titles you rejected so they aren't proposed again). The chat itself isn't included.

## Converting existing material

Already have a finished title and abstract, notes from an earlier brainstorm, or a pile of your past abstracts? Ask the agent to "convert this into a session file" or "turn these into a writing style", or choose **Convert it into a file** as the starting point. Share the material as text, a file or a URL, and you get a Markdown file back with no question rounds.

- **Session file:** your title and abstract are copied word for word, counts are calculated, and anything the material doesn't say is left empty rather than guessed. You can resume a brainstorm from it right away.
- **Writing style file:** the agent describes the traits it sees across your samples (voice, sentence length, humor, title patterns) in its own words, never quoting you.
- The agent tells you in a few lines what it filled in and what it left empty, then hands over the file as a download or on screen, your choice.

## Starting from something

If you start from an existing talk, slides, a paper, a blog post or a rough draft, share it as **pasted text, an attached file or a URL**, whichever is easiest. If the agent can't open it (no browsing tool, access denied), it tells you in one line and asks you to paste the text instead.

## Writing styles

You can reuse how you like to write across sessions without any stored memory.

- **Using a style:** in the voice-and-limits round, optionally share a writing style as text, a file or a URL. That can be a past abstract or blog post you like, or a style file saved earlier. The agent copies its style, never its wording. Anything you say in the current session overrides it.
- **Saving:** after the agent analyzes a style reference, or when you finalize a session, it offers **Save this writing style**. It shows you the proposed profile, asks for a name, and hands it over as a Markdown file or on screen.
- **Updating:** if you tweaked tone or guardrails along the way, you can get an updated style file at the end.
- **What's in it:** traits in plain words (voice, sentence length, humor, title patterns, words to prefer or avoid). Never your actual sentences or titles.

## Good to know

- **Limits are strict.** Character and word counts appear next to every draft. When a code tool is available, the agent uses it to verify tight limits.
- **No invented facts.** The agent asks rather than guessing details about you, your event or your content.
- **Your language.** It writes in the language you use, unless you ask for another.
- **Style, not sentences.** If you share a style reference, the agent copies its style (sentence length, voice, humor, structure) but never its wording.
