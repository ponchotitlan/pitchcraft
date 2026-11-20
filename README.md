<div align="center">
<pre>
                      .   *        .       *                
           /\       *    \|/   .        .                   
          /  \       .  --*--      *                        
         / *  \          /|\   .                            
        /  .   \   *      |                                 
   ____/________\____     |      .~~~~~~~~~~~~~~~~~~~~~~~~~.
       ( o    o )         |      |  ~ Expecto Acceptum! ~  |
        \  ~~  /  \_______|      |                         |
     ___/\\\\//\\___      |      |  "Kubernetes Is Lying   |
    /   \\\\\\///   \     |      |   to You"               |
   /     \\\\///     \    |      |                         |
  /   /   \\\//   \   \   |      |  CFP status: ACCEPTED   |
 /___/     \\/     \___\  |      '~~~~~~~~~~~~~~~~~~~~~~~~~'
     |              |     |                                 
     |______________|     |                                 
       ^^        ^^      _|_                                
                                                            
          P  I  T  C  H  C  R  A  F  T                      
       ( witchcraft, but for CFP submissions )              
</pre>
</div>

A collection of agent skills and prompts that help you write a strong submission for any upcoming event or conference: titles, abstracts, CFP answers and more.

Each skill is a self-contained `SKILL.md` file that follows the open [Agent Skills](https://agentskills.io) format. They describe behavior, not platform-specific tools, so the same skill works in Claude, Codex, Copilot, Cursor, Gemini and other agents that support skills. Agents without skill support can use the file as a plain prompt.

## Available skills

| Skill | What it does | Docs |
| --- | --- | --- |
| [`pitchcraft-brainstorm`](skills/pitchcraft-brainstorm/SKILL.md) | Takes you from a rough idea to a finished session title and abstract for a talk, workshop, panel or keynote. It asks short rounds of multiple-choice questions (event, audience, tone, length limits), offers 4 title candidates to pick from, then drafts and refines the abstract with the full draft always in view. Character and word limits are enforced throughout. It can start from scratch or from an existing talk, draft, paper or blog post. Sessions are saved as JSON files (`~/.pitchcraft/sessions/` by default), so you can resume later in any agent, and the result can be exported as Markdown, text or Word. | [Usage guide](skills/pitchcraft-brainstorm/README.md) |
| [`pitchcraft-presso`](skills/pitchcraft-presso/SKILL.md) | Turns your talk into an interactive HTML slide deck (keyboard navigation, slide index, step-by-step reveals, QR closing slide). Start from a Markdown outline, a `pitchcraft-brainstorm` session or a guided Q&A. Use the default dark teal-and-violet style, give your own colours, or match the palette of a reference image (logo, brand sheet, event site). Needs Python 3.8+ and nothing else. | [Usage guide](skills/pitchcraft-presso/README.md) |

## Installation

Every skill is a folder under [`skills/`](skills/) containing a `SKILL.md`. Installing a skill means putting that **whole folder** (not just `SKILL.md`: `pitchcraft-presso` also needs its `scripts/`, `assets/` and other subfolders) where your agent looks for skills.

> **Requirements per skill.** `pitchcraft-brainstorm` is instructions only and works anywhere. `pitchcraft-presso` runs Python scripts, so the agent must be able to run code: Claude Code, Codex, Copilot, Cursor and Gemini CLI can on your machine; in Claude.ai and Claude Desktop chat, turn on code execution.

Start by cloning the repo:

```bash
git clone https://github.com/ponchotitlan/pitchcraft.git
cd pitchcraft
```

The examples below install every skill (`skills/*`). To install just one, replace `skills/*` with its folder, e.g. `skills/pitchcraft-presso`.

### Any agent (skills CLI)

The [`skills`](https://github.com/vercel-labs/skills) CLI installs skills from a GitHub repo into most popular agents and asks which ones to target:

```bash
npx skills add ponchotitlan/pitchcraft
```

It lists the skills in the repo so you can pick one or all.

### Claude Code

```bash
# Available in all your projects
mkdir -p ~/.claude/skills
cp -r skills/* ~/.claude/skills/

# Or only in the current project
mkdir -p .claude/skills
cp -r skills/* .claude/skills/
```

Start a new Claude Code session (skills are loaded at start-up). Claude picks a skill up automatically when your request matches it, or you can call one directly with `/pitchcraft-brainstorm` or `/pitchcraft-presso`. In Claude Desktop, this applies to the **Code** tab only; the chat tab needs the upload below.

### Claude.ai and Claude Desktop (chat)

These apps don't read skill folders on your computer, so copying to `~/.claude/skills/` has no effect here. Upload each skill as a ZIP instead:

1. Get the ZIP: download `pitchcraft-brainstorm.zip` or `pitchcraft-presso.zip` from the [latest release](https://github.com/ponchotitlan/pitchcraft/releases/latest), or build it from your clone:
   ```bash
   cd skills
   zip -r pitchcraft-presso.zip pitchcraft-presso -x '*.DS_Store'
   ```
   The ZIP must contain the skill folder itself (with `SKILL.md` inside it), not the loose files.
2. Open **Settings → Capabilities**. For `pitchcraft-presso`, make sure code execution is on.
3. Under **Skills**, upload the ZIP and make sure it is toggled on.
4. Start a **new** chat, for example: "Help me write a CFP abstract for my KubeCon talk", or "Turn this outline into a slide deck".

In the chat apps the skill runs in Claude's online sandbox, not on your computer. Attach the files it needs (an outline, a reference image, logos, a brainstorm session JSON from `~/.pitchcraft/sessions/`), and download the finished deck from the chat.

On Team and Enterprise plans, an admin can share the skill with the whole organization.

### OpenAI Codex CLI

```bash
mkdir -p ~/.codex/skills
cp -r skills/* ~/.codex/skills/
```

Restart Codex to load it. Invoke it explicitly with `$pitchcraft-brainstorm`, or just describe what you need.

### GitHub Copilot (VS Code, Copilot CLI, coding agent)

```bash
# Project-level, shared with your repo
mkdir -p .github/skills
cp -r skills/* .github/skills/

# Or personal, for all projects
mkdir -p ~/.copilot/skills
cp -r skills/* ~/.copilot/skills/
```

### Cursor

```bash
mkdir -p .cursor/skills
cp -r skills/* .cursor/skills/
```

### Gemini CLI

```bash
mkdir -p ~/.gemini/skills
cp -r skills/* ~/.gemini/skills/
```

Run `/skills list` inside Gemini CLI to confirm it loaded.

### ChatGPT, Gemini web, or any other assistant

If your assistant doesn't support skills, use the skill as a prompt. This works fully for `pitchcraft-brainstorm`. For `pitchcraft-presso` the assistant can write the `session.json` or the outline, but you run `python3 skills/pitchcraft-presso/scripts/kit.py deck session.json` yourself to build the deck.

- **One-off:** paste the contents of `SKILL.md` (without the `---` front matter) at the start of a chat, followed by your request.
- **Reusable:** paste it into the instructions of a Custom GPT, a Gemini Gem, a Claude Project, or your tool's custom-instructions field.

> Skill locations and commands change as platforms evolve. If a path above doesn't work, check your agent's documentation for where it loads skills from.

## Contributing

New skills and improvements are welcome. Add each skill as `skills/<skill-name>/SKILL.md` with `name` and `description` front matter, keep it platform-agnostic, add a `README.md` usage guide next to it, and add a row to the table above. Pushing a tag like `v1.2.0` publishes a release with one ZIP per skill (see `.github/workflows/release.yml`).

## License

[Apache 2.0](LICENSE)
