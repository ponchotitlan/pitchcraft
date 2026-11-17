---
name: pitchcraft-brainstorm
description: Brainstorm and refine the title and abstract for a conference or event session (talk, workshop, panel, keynote) through short iterative rounds of multiple-choice questions. Use when the user wants to write, improve, or rework a session title, abstract, or CFP submission, from scratch or based on an existing talk, draft, paper, or blog post.
---

# Pitchcraft Brainstorm

Guide the user from rough idea to a finished session title and abstract. Work in rounds. Every round is a set of choice questions with an open-input escape hatch. The experience should feel like tapping through a short questionnaire, never like filling in a long form.

This skill is platform-agnostic. It describes behavior, not specific tools. Use whatever your environment offers, following the interaction layer below.

## Interaction layer

Every "question round" in this skill means: 1-4 short questions, each with 2-4 options, plus an open-input escape hatch.

**Step 1: look for a structured question tool before writing anything.** This is any tool that shows the user selectable options, for example `AskUserQuestion`, `request_user_input`, or similarly named ask/choice/form tools. If tools are loaded lazily or listed by name only (deferred), load the schema first (e.g. via a tool search) and then call it. Do not conclude the tool is missing until you have checked.

**Step 2a: if a structured question tool exists, use it for every round, including the very first reply.**
- Use multi-select where several answers make sense.
- Rely on the tool's built-in "Other"/free-text input; if it has none, add a "Something else (type it)" option.
- Mention in one short line that the user can pick options or use Other to say anything else.

**Step 2b: if no such tool exists**, present each round as a compact numbered list with lettered options and tell the user how to reply:

```
1. Session type?  a) Talk  b) Workshop  c) Panel  d) Keynote
2. Audience level?  a) Beginners  b) Practitioners  c) Experts  d) Mixed

Reply like "1a, 2c" or just describe it in your own words.
```

**Never open with a block of open-ended questions in prose** (e.g. "1. What's the event? 2. What's the audience? 3. ..."). That is the anti-pattern this skill exists to avoid. Turn every question that can be a choice into options. Free-text is requested only for facts that can't be options (see Phase 0, Round C), and then in a single short message.

Whichever method is used:
- **Free text is always welcome** and counts as a full answer for the round. Apply it and continue.
- **Recommended option first**, marked "(Recommended)", when you have a clear view.
- **Never re-ask what the user already told you.** Read their message and any attached or pasted material first; skip any question already answered, and skip whole rounds if everything is covered.
- **Keep the draft visible while asking.** Text written right before a question dialog may not be on screen once the dialog opens, so never rely on it alone. Do both:
  1. Show the current draft as a normal message first. If the environment has a dedicated tool for sending messages to the user, use it for this.
  2. Repeat the current draft inside the first question's text (title and abstract, with counts), so it stays visible in the dialog itself. If options support a preview field, put full candidate drafts there.
- **Open every round with a status line** above the draft: `Round 3 · Title (locked): "..." · Abstract draft v2 · 112/150 words`. This shows progress at a glance.
- **Make each question stand alone.** It must make sense without the surrounding text and name what it refers to.
- **Keep rounds short.** One draft set, one set of questions, no long preambles. If the platform caps questions per call, split across calls.

## General rules

- **Respect constraints strictly.** Count characters/words for any limit and show the count beside each draft, e.g. `(68/80 chars)`. If a code or calculation tool is available, use it to verify tight limits; otherwise count carefully by hand and say the count is approximate if unsure.
- **Don't invent facts** about the speaker, the event, or the content. Ask instead.
- **Match the user's language** unless they ask for another. Confirm it in the context summary.
- **Never copy wording** from example sessions; learn the style, not the sentences.

## Phase 0: Gather context

Your first reply starts here with Round A. At most one short line of intro ("Let's build your session title and abstract. A few quick taps to set the scene."), then the questions.

**Round A: the basics** (one call, 4 questions)
1. *Event type:* Industry/tech conference, Community meetup, Internal/company event, Academic/scientific.
2. *Session type:* Talk, Workshop, Panel, Keynote (Other covers lightning talk and anything else).
3. *Starting point:* From scratch, Based on an existing talk or slides, Based on a paper or blog post, Based on a rough draft I have.
4. *Audience level:* Beginners, Practitioners, Experts, Mixed room.

**Round B: voice and limits** (one call, 4 questions)
1. *Tone:* Practical and plain-spoken, Playful and witty, Bold and provocative, Credible and academic.
2. *Limits:* No limits, Short (title up to 80 chars, abstract up to 150 words), Medium (title up to 100 chars, abstract up to 300 words), Exact limits (type them in Other).
3. *Past session for tone inspiration:* No example, I'll paste one, I'll attach a file or link.
4. *Style guardrails* (multi-select): No buzzwords, No emojis, No questions in the title, None.

**Round C: the facts only the user knows** (one short plain message, only for what's still missing)
Ask once, in one or two lines, for: the event name and theme, the idea of the session in a sentence or two, and, if they chose a based-on-existing starting point or an example, the pasted text, file, or link. Mention that a key takeaway and must-mention links or names are welcome but optional. If the user's opening message already contained these facts, skip this round.

**Confirm** (one question round)
Give a short summary of everything gathered ("Here's what I have: ..."), including language, then ask: **Looks right, start on the title** / **Adjust something** (free text for details).

If an example session was provided, analyze its traits (sentence length, voice, use of questions, humor, structure) and mirror the style in the drafts, not the wording.

## Phase 1: Title

1. **Draft 4 title candidates**, each with a distinct angle (benefit-led, curiosity/question, bold claim, plain descriptive; optionally with a subtitle). Respect the title limit, show char counts, and add a one-line note on each angle.
2. **Ask a question round** (write each candidate's full text in its option label, so the choices are readable inside the dialog):
   - *Direction:* which candidate is closest? Options: each candidate, **Mix elements of several**, **None, try new angles**.
   - *What to change* (multi-select): Shorter, More specific, More curious, More playful, More serious/credible, Less jargon, More technical, Add a subtitle, Change keywords.
   - *Status:* **Lock this title** (only valid when one candidate is selected) / **Keep iterating**.
3. **Iterate:** apply the feedback and produce a fresh set (3-4 options, or 1-2 when converging). Say briefly what changed since the last round, then ask the same structure again.
4. When the user chooses **Lock this title**, restate it with its char count and confirm before moving on.

## Phase 2: Abstract

Build the abstract around the locked title.

1. **Settle format first** (one question round):
   - *Length:* use the user's limit if given; otherwise offer Short (~50-80 words), Medium (~120-150), Long (~200-250).
   - *Structure* (multi-select): Hook / opening problem, What the session covers, What attendees will learn (bullets), Who it's for, About the speaker, Call to action.
   - *Formatting:* Plain text, Markdown (bold, bullets), Markdown with links, Match the event's form field. Free text covers specifics such as "include these 2 links" or "no bullets".
2. **Draft the abstract** under the title, with the word/char count against the limit. Include any supplied links, formatted as requested.
3. **Ask a question round** (the first question's text must contain the full current title and abstract with counts, per the interaction layer, so the user can read the draft while answering):
   - *What to adjust* (multi-select): Stronger opening, Shorter, Longer / more detail, More concrete takeaways, Change tone, Reorder sections, Add or fix links, Change formatting, Simplify language.
   - *Section check:* which part needs the most work? Opening, Body, Takeaways, Closing, or **All fine**.
   - *Status:* **Looks good, finalize** / **Keep iterating**.
4. **Iterate** with the full revised draft each round (not diffs), shown both as a message and inside the question, with a one-line note on what changed. If the abstract drifts so far that the title no longer fits, flag it and offer to revisit the title.
5. Continue until the user chooses **Looks good, finalize**.

## Phase 3: Final delivery

Present the complete result in one block:

```
# <Title>   (N chars)

<Abstract in the agreed format>   (N words / N chars)
```

Then:
- State constraint compliance in one line (e.g. "Title 68/80 chars, abstract 142/150 words").
- Ask a final question round: **Done**, **Shorter version**, **Version in another tone**, **Save to a file**, plus free text.
- If asked to save: write it to a file in the requested format if the environment supports file output; otherwise give the content in a copy-ready block.

## Drafting guidance

- **Titles:** specific beats clever; avoid stacked buzzwords; front-load the keyword; let a subtitle carry clarity if the main title carries the hook.
- **Abstracts:** lead with the audience's problem or a concrete moment, not "In this talk, I will...". Make takeaways tangible and verifiable ("you'll leave with a checklist for X"). Cut filler. The first two sentences must carry the value, because reviewers and attendees skim.
