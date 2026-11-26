<div align="center">
<pre>
 .--------------------------------------------------.
 |                                                  |
 |           P  I  T  C  H  C  R  A  F  T           |
 |  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  |
 |      idea  .  title  .  abstract  .  slides      |
 |                                                  |
 '-------------------------.------------------------'
                           |                         
       \o/     "...and that's why you should         
     .--|--.     never do a live demo."              
     | ~~~ |                                         
     |_____|                                         
 ____|_____|_________________________________________
    o   o   o   o   o   o   o   o   o   o   o   o    
   \|/ /|\ \|/ /|\ \|/ /|\ \|/ /|\ \|/ /|\ \|/ /|\   
          *clap*         *clap*          *clap*      
</pre>
</div>

🎤✨ A collection of agent skills and prompts that help you write a strong submission for any upcoming event or conference, and then present it: titles, abstracts, CFP answers, slide decks and more.

🧩 Each skill is a self-contained folder with a `SKILL.md` file that follows the open [Agent Skills](https://agentskills.io) format. They describe behavior, not platform-specific tools, so the same skill works in Claude, Codex, Copilot, Cursor, Gemini and other agents that support skills. Agents without skill support can use the file as a plain prompt.

## 🧰 Available skills

| Skill | What it does | Docs |
| --- | --- | --- |
| 🧠 [`pitchcraft-brainstorm`](skills/pitchcraft-brainstorm/SKILL.md) | Takes you from a rough idea to a finished session title and abstract for a talk, workshop, panel or keynote. It asks short rounds of multiple-choice questions (event, audience, tone, length limits), offers 4 title candidates to pick from, then drafts and refines the abstract with the full draft always in view. Character and word limits are enforced throughout. It can start from scratch or from an existing talk, draft, paper or blog post. Nothing is stored locally: when you want to keep a session or a writing style, you get it as a Markdown file (download or on screen) and bring it back later by pasting it, attaching it or giving a URL. It can also convert an existing abstract or writing samples into those files, and export the result as Markdown, text or Word. | 📖 [Usage guide](skills/pitchcraft-brainstorm/README.md) |
| 🏛️ [`pitchcraft-council`](skills/pitchcraft-council/SKILL.md) | Stress-tests your session title and abstract before you submit it. A council of five agents (CFP Analyser, Conference Researcher, Programme Committee Member, Audience Member and Synthesiser) reads it from each seat, running in parallel where they don't depend on each other. You get committee and attendee scores, the top rejection risks, two title rewrites, a full abstract rewrite and five ranked edits. It uses only the event and CFP URLs you paste. Works best in agents that can spawn subagents; otherwise it plays the roles one by one. | 📖 [Usage guide](skills/pitchcraft-council/README.md) |
| 🎞️ [`pitchcraft-presso`](skills/pitchcraft-presso/SKILL.md) | Turns your talk into an interactive HTML slide deck (keyboard navigation, slide index, step-by-step reveals, QR closing slide). Start from a Markdown outline, a `pitchcraft-brainstorm` session or a guided Q&A. Use the default dark teal-and-violet style, give your own colours, or match the palette of a reference image (logo, brand sheet, event site). Needs Python 3.8+ and nothing else. | 📖 [Usage guide](skills/pitchcraft-presso/README.md) |

## 🔗 Use it straight from the repo URL

No install needed for agents that can read a URL. Give the agent the repo link and ask for what you want, for example: "Read https://github.com/ponchotitlan/pitchcraft and help me write an abstract for my talk."

The agent starts at [`AGENTS.md`](AGENTS.md), which routes the request to the right skill's `SKILL.md` and explains the conventions. `pitchcraft-brainstorm` is instructions only, so this works even when the agent can't run code or write files. `pitchcraft-council` is instructions only too, and runs fastest in an agent that can spawn subagents. `pitchcraft-presso` runs scripts, so it needs an agent that can execute Python (see Requirements below).

## 📦 Installation

Every skill is a folder under [`skills/`](skills/) containing a `SKILL.md`. Installing a skill means putting that **whole folder** where your agent looks for skills, not just `SKILL.md`: `pitchcraft-brainstorm` also has `templates/` and `examples/`, `pitchcraft-council` has its `agents/` folder with the five council members, and `pitchcraft-presso` has its `scripts/`, `assets/` and other subfolders. The release ZIPs include these automatically.

> ⚙️ **Requirements per skill.** `pitchcraft-brainstorm` is instructions only and works anywhere: it keeps no state, needs no storage and no memory feature, and hands you files rather than writing them to your machine. `pitchcraft-council` is instructions only as well, and runs its agents in parallel when your agent can spawn subagents (Claude Code and most coding agents can); without that it plays the five roles one after another, just more slowly. `pitchcraft-presso` runs Python scripts, so the agent must be able to run code: Claude Code, Codex, Copilot, Cursor and Gemini CLI can on your machine; in Claude.ai and Claude Desktop chat, turn on code execution.

Start by cloning the repo:

```bash
git clone https://github.com/ponchotitlan/pitchcraft.git
cd pitchcraft
```

The examples below install every skill (`skills/*`). To install just one, replace `skills/*` with its folder, e.g. `skills/pitchcraft-presso`.

### ⚡ Any agent (skills CLI)

The [`skills`](https://github.com/vercel-labs/skills) CLI installs skills from a GitHub repo into most popular agents and asks which ones to target:

```bash
npx skills add ponchotitlan/pitchcraft
```

It lists the skills in the repo so you can pick one or all.

### 🤖 Claude Code

```bash
# Available in all your projects
mkdir -p ~/.claude/skills
cp -r skills/* ~/.claude/skills/

# Or only in the current project
mkdir -p .claude/skills
cp -r skills/* .claude/skills/
```

Start a new Claude Code session (skills are loaded at start-up). Claude picks a skill up automatically when your request matches it, or you can call one directly with `/pitchcraft-brainstorm`, `/pitchcraft-presso` or `/pitchcraft-council`. In Claude Desktop, this applies to the **Code** tab only; the chat tab needs the upload below.

### 💬 Claude.ai and Claude Desktop (chat)

These apps don't read skill folders on your computer, so copying to `~/.claude/skills/` has no effect here. Upload each skill as a ZIP instead:

1. Get the ZIP: download `pitchcraft-brainstorm.zip`, `pitchcraft-council.zip` or `pitchcraft-presso.zip` from the [latest release](https://github.com/ponchotitlan/pitchcraft/releases/latest), or build it from your clone:
   ```bash
   cd skills
   zip -r pitchcraft-presso.zip pitchcraft-presso -x '*.DS_Store'
   ```
   The ZIP must contain the skill folder itself (with `SKILL.md` inside it), not the loose files.
2. Open **Settings → Capabilities**. For `pitchcraft-presso`, make sure code execution is on.
3. Under **Skills**, upload the ZIP and make sure it is toggled on.
4. Start a **new** chat, for example: "Help me write a CFP abstract for my KubeCon talk", or "Turn this outline into a slide deck".

In the chat apps the skill runs in Claude's online sandbox, not on your computer. Attach the files it needs (an outline, a reference image, logos, a saved brainstorm session file), and download what it produces from the chat: the finished deck, or a session or writing style file.

🏢 On Team and Enterprise plans, an admin can share the skill with the whole organization.

### 🧑‍💻 OpenAI Codex CLI

```bash
mkdir -p ~/.codex/skills
cp -r skills/* ~/.codex/skills/
```

Restart Codex to load it. Invoke it explicitly with `$pitchcraft-brainstorm`, or just describe what you need.

### 🐙 GitHub Copilot (VS Code, Copilot CLI, coding agent)

```bash
# Project-level, shared with your repo
mkdir -p .github/skills
cp -r skills/* .github/skills/

# Or personal, for all projects
mkdir -p ~/.copilot/skills
cp -r skills/* ~/.copilot/skills/
```

### 🖱️ Cursor

```bash
mkdir -p .cursor/skills
cp -r skills/* .cursor/skills/
```

### ♊ Gemini CLI

```bash
mkdir -p ~/.gemini/skills
cp -r skills/* ~/.gemini/skills/
```

Run `/skills list` inside Gemini CLI to confirm it loaded.

### 🌐 ChatGPT, Gemini web, or any other assistant

If your assistant doesn't support skills, use the skill as a prompt. This works fully for `pitchcraft-brainstorm`; it needs only the contents of `SKILL.md`, since the skeletons of its file formats are included in it, and `templates/` and `examples/` are optional extras. `pitchcraft-council` also works this way: paste `SKILL.md` followed by the five files in `agents/`, and the assistant plays the council one role at a time. For `pitchcraft-presso` the assistant can write the `session.json` or the outline, but you run `python3 skills/pitchcraft-presso/scripts/kit.py deck session.json` yourself to build the deck.

- 📋 **One-off:** paste the contents of `SKILL.md` (without the `---` front matter) at the start of a chat, followed by your request.
- 🔁 **Reusable:** paste it into the instructions of a Custom GPT, a Gemini Gem, a Claude Project, or your tool's custom-instructions field.

> 💡 Skill locations and commands change as platforms evolve. If a path above doesn't work, check your agent's documentation for where it loads skills from.

---

<div align="center"><br />
    Made with ☕️ by Poncho Sandoval - <code>Developer Advocate 🥑 @ DevNet - Cisco Systems 🇵🇹</code><br /><br />
</div>
