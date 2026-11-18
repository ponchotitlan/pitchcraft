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

## Installation

Every skill is a folder under [`skills/`](skills/) containing a `SKILL.md`. Installing a skill means copying that folder to where your agent looks for skills. Start by cloning the repo:

```bash
git clone https://github.com/ponchotitlan/pitchcraft.git
cd pitchcraft
```

The examples below install `pitchcraft-brainstorm`. Swap in another skill name, or copy the whole `skills/*` set, to install more.

### Any agent (skills CLI)

The [`skills`](https://github.com/vercel-labs/skills) CLI installs skills from a GitHub repo into most popular agents and asks which ones to target:

```bash
npx skills add ponchotitlan/pitchcraft
```

### Claude Code

```bash
# Available in all your projects
mkdir -p ~/.claude/skills
cp -r skills/pitchcraft-brainstorm ~/.claude/skills/

# Or only in the current project
mkdir -p .claude/skills
cp -r skills/pitchcraft-brainstorm .claude/skills/
```

Claude picks the skill up automatically when you ask for help with a session abstract. You can also call it directly with `/pitchcraft-brainstorm`.

### Claude.ai and Claude Desktop

1. Zip the skill folder: `cd skills && zip -r pitchcraft-brainstorm.zip pitchcraft-brainstorm`
2. Open **Settings → Capabilities → Skills** and upload the zip.
3. Make sure the skill is toggled on, then start a chat, for example: "Help me write a CFP abstract for my KubeCon talk."

On Team and Enterprise plans, an admin can share the skill with the whole organization.

### OpenAI Codex CLI

```bash
mkdir -p ~/.codex/skills
cp -r skills/pitchcraft-brainstorm ~/.codex/skills/
```

Restart Codex to load it. Invoke it explicitly with `$pitchcraft-brainstorm`, or just describe what you need.

### GitHub Copilot (VS Code, Copilot CLI, coding agent)

```bash
# Project-level, shared with your repo
mkdir -p .github/skills
cp -r skills/pitchcraft-brainstorm .github/skills/

# Or personal, for all projects
mkdir -p ~/.copilot/skills
cp -r skills/pitchcraft-brainstorm ~/.copilot/skills/
```

### Cursor

```bash
mkdir -p .cursor/skills
cp -r skills/pitchcraft-brainstorm .cursor/skills/
```

### Gemini CLI

```bash
mkdir -p ~/.gemini/skills
cp -r skills/pitchcraft-brainstorm ~/.gemini/skills/
```

Run `/skills list` inside Gemini CLI to confirm it loaded.

### ChatGPT, Gemini web, or any other assistant

If your assistant doesn't support skills, use the skill as a prompt:

- **One-off:** paste the contents of `SKILL.md` (without the `---` front matter) at the start of a chat, followed by your request.
- **Reusable:** paste it into the instructions of a Custom GPT, a Gemini Gem, a Claude Project, or your tool's custom-instructions field.

> Skill locations and commands change as platforms evolve. If a path above doesn't work, check your agent's documentation for where it loads skills from.

## Contributing

New skills and improvements are welcome. Add each skill as `skills/<skill-name>/SKILL.md` with `name` and `description` front matter, keep it platform-agnostic, add a `README.md` usage guide next to it, and add a row to the table above.

## License

[Apache 2.0](LICENSE)
