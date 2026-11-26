# pitchcraft-council

Stress-test your session abstract before you submit it. A council of five agents reads it from the seats that decide its fate at an event: the Call for Papers, the conference culture, the programme committee and the audience. A coach then turns their feedback into scores, rewrites and a ranked list of edits.

It works on a **session title and abstract** for a specific event. The goal is a clearer pitch for the right people, not gaming the selection.

> Not installed yet? See [Installation](../../README.md#-installation) in the main README. Install the whole `pitchcraft-council` folder, including `agents/`.

## The council

| Agent | Role | Produces |
| --- | --- | --- |
| 🔍 CFP Analyser | Reads the Call for Papers | Themes, formats, audience, hard rules, hidden signals, CFP questions |
| 📚 Conference Researcher | Studies the event and its past programme | Ethos, accepted-talk patterns, rejection signals, trends |
| 🎯 Programme Committee Member | Reviews like a volunteer reviewer | Scores, top 3 rejection risks, top 3 edits |
| 🙋 Audience Member | Picks sessions like an attendee | Scores, best thing, biggest hesitation, title idea |
| 🧠 Synthesiser | Senior conference coach | Both scores and verdicts, 2 titles, abstract rewrite, 3 ranked edits |

## How it runs

```
brief ─┬─► cfp-analyser ───────────────┐
       └─► conference-researcher ──┬───┴─► programme-committee ─┐
                                   └─► audience-member ─────────┴─► synthesiser
```

- **Parallel waves.** Analyser and Researcher run at the same time. The Audience starts as soon as the Researcher is done, the Committee when both are done, and the Synthesiser last.
- **Needs subagents for parallel mode.** In an agent that can spawn subagents, the waves run concurrently. Without them, the same agent plays the five roles one after another and gives the same kind of report, just slower.
- **Live progress.** You see what is happening at every step: a task list when your agent has one, plus a one-line status when agents start and finish (`▶️ Wave 1 · Analyser and Researcher reading in parallel`, `✅ Researcher done · Audience started`). In sequential mode it announces each role as it plays it.
- **Independent opinions.** The Committee and Audience never see each other's output. Only the Synthesiser sees both and flags where they disagreed.
- **It asks for what it needs.** Before any agent starts, it collects the title, abstract, event name, **CFP URL** and **event URL**, in one questionnaire form when your agent can show one, otherwise in one message. It won't run without sources unless you say there are none.
- **Your sources only.** The agents read the event URL and CFP URL you give them, plus anything else you paste, and nothing more. If a page can't be fetched, paste its text. With no source at all, that agent says what it couldn't verify and the report flags it.
- **Scores.** Each criterion is 1 to 5 with a reason. Committee and Attendee scores are each out of 100 and shown with their verdicts (accept/borderline/reject and would attend yes/maybe/no). There is no combined overall score, so a disagreement between the two seats is never averaged away.
- **Nothing is stored.** You get a Markdown report on screen or as a download.

## What you need

- Title and abstract (verbatim), or a [`pitchcraft-brainstorm`](../pitchcraft-brainstorm/README.md) session file.
- The event name, the **CFP URL** and the **event URL** (or pasted text from those pages). The review is only as good as these sources, so the skill asks for them if you leave them out.

## Questions to try

| I want to... | Ask something like |
| --- | --- |
| Review an abstract before submitting | "Run the council on this abstract for DevOpsCon. Event: https://... CFP: https://..." (paste title and abstract) |
| Start from a saved session | "Run the council on this session file." (paste or attach it) |
| Check against hard rules | "Does my abstract break any CFP rule?" |
| Get a rewrite | "Give me the council's rewrite, keeping it under 150 words." |
| Try another session for the same event | "Now run the council on this other abstract for the same event." (reuses the CFP and event research) |
| Re-check after edits | "Re-score this revised version." |
| Keep the result | "Give me the report as a Markdown file." |

In Claude Code you can call it with `/pitchcraft-council`, and in Codex with `$pitchcraft-council`.

## Files

| Path | What it is |
| --- | --- |
| [`SKILL.md`](SKILL.md) | The orchestrator: flow, parallel rules, fallbacks |
| [`agents/`](agents/) | One Markdown file per council member (name and description in the front matter, instructions in the body) |
| [`templates/`](templates/) | The brief and the report formats |
| [`examples/`](examples/council-report-sample.md) | A fictional filled-in report |

The agent files are plain Markdown with a minimal front matter, so they can be copied into the agents folder of platforms that support native subagents. The orchestrator also passes their content as a prompt to any generic subagent tool, so copying them is optional.
