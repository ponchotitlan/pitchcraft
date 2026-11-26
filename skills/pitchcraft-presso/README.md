# pitchcraft-presso

One `session.json` in; an interactive slide deck out, in a dark teal-and-violet style or your own theme.

```bash
python3 scripts/kit.py init  my-talk                 # starter session.json + placeholder images
python3 scripts/kit.py check my-talk/session.json
python3 scripts/kit.py deck  my-talk/session.json    # -> my-talk/build/deck/index.html

# write docker-compose.yml into the talk folder, then launch from there
python3 scripts/kit.py package my-talk/session.json
cd my-talk && docker compose up -d                    # -> http://localhost:8080

# start from content and style you already have, in one go
python3 scripts/kit.py init my-talk --from-outline talk.md --from-image brand.png
python3 scripts/kit.py init my-talk --from-brainstorm 2026-11-18-ai-agents-keynote --a1 '#e11d48' --mode light

# custom theme: preview, then save with --write
python3 scripts/kit.py theme my-talk/session.json --from-image brand.png
python3 scripts/kit.py theme my-talk/session.json --a1 '#e11d48' --a2 '#2563eb' --mode light --write
```

`package` writes the server files **into the talk folder** and mounts your existing deck (see "Serving the deck from a web server"). After that the folder runs on its own, without the skill.

Requirements: Python 3.8+; Docker Compose only if you want the web server. Nothing else (Pillow, if installed, lets `--from-image` read JPEG/WebP; on macOS `sips` does it without Pillow).

## Telling it what you want

You can give the skill your **content** and your **style** at the start, in any mix. Whatever you leave out, the assistant asks about in one short round of multiple-choice questions (where the content comes from, which style, how long the talk is). Everything you give up front skips its question.

### With an AI assistant

Say what you have in your first message. Some examples:

| You say | What happens |
|---|---|
| "Make a deck from `talk.md`" | Your outline becomes the slides (format below). |
| "Use my brainstorm session for the KubeCon talk" | Title, event, language and key takeaway come from your pitchcraft-brainstorm session; the assistant drafts the remaining slides from its abstract and marks them as proposals. |
| *pastes a script, notes or old slides* | The assistant turns them into an outline, keeping your wording, then builds from it. |
| "Match the colours in `brand.png`" | The palette is taken from the image. |
| "Light theme, accent `#e11d48`" | Your colours are used exactly; the rest is derived to match. |
| "Something calm and light, Cisco blue" | The assistant picks hex values for the mood and tells you which it chose. |
| "Build it with me" | A guided round per section: opening, 2-4 key ideas, demo, close. |
| "Serve my deck in `my-talk/` as a web server" | The assistant writes `docker-compose.yml` and `nginx.conf` in `my-talk/` that mount your existing deck. Nothing is regenerated. |
| *nothing* | The example template and the default dark teal-and-violet style. |

Combine them freely: *"Deck from `talk.md`, colours from `logo.png`, 20 minutes."*

### From the command line

`init` takes the same inputs as flags:

| Input | Flag |
|---|---|
| Markdown outline | `--from-outline talk.md` |
| Brainstorm session | `--from-brainstorm <id or path>` (looked up in `$PITCHCRAFT_DIR`, else `~/.pitchcraft/sessions/`; an unknown id lists your recent sessions) |
| Reference image | `--from-image brand.png` |
| Colours | `--a1 --a2 --a3` (accents), `--bg --bg2 --bg3 --card --border --text --muted --on-accent` |
| Light or dark | `--mode light` / `--mode dark` (default: from `--bg`, else the image, else dark) |
| Fonts | `--font-head`, `--font-body` (only Space Grotesk and Inter are bundled; others must be installed on the presenting machine) |

`init` prints what it took from where, a colour preview, any contrast warnings, and what is still missing (logos, images, links). It never overwrites an existing `session.json`.

**When inputs overlap:** colours on the command line beat the outline's `theme:` block, and the image fills whatever you did not set. For slides and session details, the outline beats the brainstorm session; the brainstorm fills only what the outline leaves out.

### Writing an outline

```markdown
---
title: Own It, Run It, Trust It
event: Example Conf 2026
pillars: Own it, Run it, Trust it
logo: images/logo-white.svg        # logo_dark: for light themes
theme:
  from_image: brand.png            # or mode / a1 / a2 / bg ...
---

# Running AI agents your team can [[actually trust]]
Own It, Run It, Trust It

## Agents are already in production
They act on real systems, with real credentials.
> The question is **who is accountable**.

## [cards] What every agent needs
- 🪪 **An identity** - Who is acting, and on whose behalf?
- 🔧 **The right tools** - Access that matches the job.
```

- `# Title` is the cover; each `## Title` is a slide. Text becomes the lead and `> text` the punch line.
- The slide type is guessed from what the slide holds (a YouTube link, an image, two `### Label` lists, links, bullets) or set with `## [type] Title`.
- Paths are relative to the outline file.

Full rules: [references/outline-format.md](references/outline-format.md). Complete example: [examples/outline.example.md](examples/outline.example.md).

### Changing the style later

```bash
python3 scripts/kit.py theme my-talk/session.json --from-image new-brand.png           # preview only
python3 scripts/kit.py theme my-talk/session.json --from-image new-brand.png --write   # save it
```

Without `--write` nothing changes. With it, the `theme` block is replaced, your fonts are kept, and the previous theme is printed so you can put it back. Then run `deck` again.

## Serving the deck from a web server

One command writes a Docker Compose file into **the talk's own folder**, next to `session.json`, that mounts the deck you already have:

```bash
python3 scripts/kit.py package my-talk/session.json [--deck DIR] [--rebuild] [--force]
```

```
my-talk/
  session.json
  build/deck/          your deck (mounted as it is, never regenerated)
  docker-compose.yml   nginx service that mounts the deck read-only, on port 8080
  nginx.conf           /healthz, no-cache for index.html, long cache for fonts
```

### Asking an AI assistant to do it

You don't need to know the commands. Say it in plain words, from the talk folder or naming it:

> *"Set up a web server for the deck in `my-talk/` so I can present it from `localhost:8080`."*

> *"I already edited `my-talk/build/deck/` by hand. Create a docker compose in `my-talk/` that serves those files. Don't rebuild anything."*

> *"Serve the presentation in this folder with docker compose, on port 9000."*

What the assistant does: runs `package` on your `session.json`, which mounts the deck that already exists and writes the two server files. It then tells you which deck it found and gives you `docker compose up -d`. It only starts the container if you ask it to. Words like *"rebuild"* or *"regenerate the deck from session.json"* are what make it use `--rebuild`; without them your deck stays as it is, and with them the old one is kept as a `.bak` folder.

If your deck lives somewhere unusual, say where: *"the deck is in `slides/dist/`"*.

Then work from the talk folder; the skill's folder is no longer needed:

```bash
cd my-talk
docker compose up -d          # open http://localhost:8080
PORT=9000 docker compose up -d   # another host port
docker compose down           # stop it
```

- **Your deck is never overwritten.** `package` mounts the deck that exists: `build/deck/`, `deck/`, or the folder you give with `--deck DIR` (anything with an `index.html`, including a deck you edited by hand). It builds from `session.json` only if it finds no deck at all.
- `--rebuild` regenerates the deck from `session.json` on purpose. The existing deck is first moved to `<deck>.bak-<date-time>`, never deleted.
- The deck is **mounted**, not baked into an image, so nothing is built. Edit the files and reload the browser; no restart needed.
- If you edited `docker-compose.yml` or `nginx.conf`, `package` keeps your version and says so. `--force` replaces them.
- `--out DIR` changes where a newly built deck goes; the deck must be inside the talk folder.
- To share it, copy the talk folder (or just `docker-compose.yml`, `nginx.conf` and the deck folder) to any host with Docker Compose. Put a reverse proxy in front for HTTPS.
- Serving over http also fixes the YouTube error 153 that appears when a video slide is opened from disk.

## Installing

See [Installation](../../README.md#-installation) in the main README. It has steps for Claude Code, Claude.ai / Claude Desktop, Codex, Copilot, Cursor, Gemini CLI and plain chat assistants.

Two things specific to this skill:

- **Install the whole folder**, not just `SKILL.md`. The deck is built by the Python scripts in `scripts/` using the files in `assets/`.
- **The agent must be able to run Python 3.8+.** Agents running on your computer (Claude Code, Codex, Copilot, Cursor, Gemini CLI) use your local Python. In Claude.ai and Claude Desktop chat, turn on code execution and attach your files (outline, images, brainstorm session JSON) to the chat; the deck is created in the online sandbox for you to download.

Nothing in the scripts needs network access or a specific AI platform.

## Layout

```
SKILL.md                  what the assistant reads
scripts/kit.py            CLI: init, check, deck, theme, package
scripts/package.py        writes docker-compose.yml + nginx.conf into the talk folder
scripts/theme.py          palette extraction and theme derivation
scripts/outline.py        Markdown outline and brainstorm-session import
scripts/deck.py           slide renderers and page assembly
scripts/common.py         config loading and helpers
assets/deck/              engine: shell.html, deck.css, deck.js (navigation, index, reveals, ?shot=N)
assets/fonts/             Space Grotesk + Inter (SIL OFL)
examples/                 session.example.json, outline.example.md + placeholder images
references/               schema, slide types, outline format, design system
```
