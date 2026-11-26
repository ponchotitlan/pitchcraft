---
name: pitchcraft-presso
description: Build an interactive HTML slide deck for a conference talk, workshop or keynote from one JSON file, in a dark teal-and-violet style by default or a custom theme from colours the user gives or a palette taken from a reference image (scroll-snap slides, keyboard navigation, slide index, step-by-step reveals, QR/links closing slide). Content can come from a Markdown outline, a pitchcraft-brainstorm session or a guided Q&A. Use when the user wants to create, restyle or extend a talk deck.
---

# pitchcraft-presso

One `session.json` is the source of truth; `kit.py deck` turns it into a single self-contained `deck/index.html` that opens from disk.

Needs only Python 3.8+ (standard library); `package` output needs docker compose to run. No network access: fonts (Space Grotesk, Inter, SIL OFL) are bundled and copied next to the deck. Run from anywhere: `python3 <skill-dir>/scripts/kit.py ...`.

## Workflow

1. **Kickoff: take what the user already gave, ask only for the rest** (see "Starting points" below). Never re-ask something their message, an attached file or a brainstorm session already answers.
2. **Create session.json** with one `init`, passing everything known up front:
   `python3 scripts/kit.py init <project-dir> [--from-outline talk.md] [--from-brainstorm <id|path>] [--from-image ref.png] [--a1 '#hex' ...] [--mode light|dark]`
   With no content source it copies the example template plus placeholder images. Edit the result; do not start from a blank file. Schema: `references/config-schema.md`. Slide fields: `references/slide-types.md`. Outline format: `references/outline-format.md`.
3. **Fill the gaps**: `init` prints what is still missing. Draft slides the user asked you to write (e.g. from the brainstorm abstract kept in `session.abstract`), and mark them as proposals.
4. **Validate**: `python3 scripts/kit.py check <project-dir>/session.json`. It lists unknown slide types, bad colours and every missing file. Fix all of them first.
   - **Restyle later** with `python3 scripts/kit.py theme <project-dir>/session.json --from-image ref.png` and/or `--a1 '#hex' --a2 ... --bg ... --mode light|dark`. It prints swatches, the theme JSON and contrast warnings; show them to the user, then re-run with `--write` to save. See "Custom themes" below.
5. **Build**: `python3 scripts/kit.py deck <project-dir>/session.json` (output in `<project-dir>/build/deck/`, or pass `--out`).
6. **Look at the result before reporting.** Open `deck/index.html?shot=N` in a browser or headless browser (it shows slide N alone, fully revealed) and check the cover, one dense slide and the closing slide. Do not just say it built.
7. **Web server (only if asked)**: `python3 scripts/kit.py package <project-dir>/session.json [--deck DIR] [--rebuild] [--force]`. It writes `docker-compose.yml` and `nginx.conf` **into the project dir** and **mounts the deck that already exists** (`build/deck/`, `deck/`, or any folder with `index.html` via `--deck`), read-only, into an nginx container: `cd <project-dir> && docker compose up -d`, then `http://localhost:8080` (`PORT=9000` changes the port). **Never regenerate a deck that exists**: the user may have hand-edited it. `package` only builds from session.json when no deck is found; `--rebuild` is the explicit opt-in, and then it moves the old deck to `<deck>.bak-<time>` first. Do not pass `--rebuild` unless the user asks for it, and do not run `deck` before `package`. It also keeps `docker-compose.yml`/`nginx.conf` the user edited unless `--force`. Do not run compose for the user unless asked.
8. **Deliver** with a short list of what was made, what you assumed (copy you wrote, defaults), and what the user must replace (placeholder images, QR codes, links).

## Starting points

The user can hand over **content** and **style** at the start, in any mix. Detect what they gave before asking anything:

| They gave | Content | Style |
|---|---|---|
| A Markdown outline / notes file | `--from-outline file.md` (convert loose notes to the outline format first, keeping their wording) | its front-matter `theme:` block, if any |
| A pitchcraft-brainstorm session (or "use my brainstorm") | `--from-brainstorm <id>`; sessions live in `$PITCHCRAFT_DIR` or `~/.pitchcraft/sessions/` | — |
| Pasted slides, a script or an existing talk | write an outline from it, then `--from-outline` | — |
| A reference image (logo, brand sheet, screenshot) | — | `--from-image path` |
| Colours, or words like "light, Cisco blue, minimal" | — | translate to `--a1 --a2 --bg --mode`; say which hex values you chose |
| Nothing | the example template | the default |

Command-line style flags win over the outline's `theme:` block; an outline wins over a brainstorm session for slides and any field both have.

**Kickoff round** (only for what is still unknown). Use a structured question tool if the environment has one (load it first if it is deferred); otherwise a compact numbered list the user answers like "1b, 2a". Recommended option first. Free text always counts as an answer.

1. *Content, where from?* — From my brainstorm session (list up to 3 recent ones by title, if the store has any) / From an outline or notes I'll give you / Build it with me slide by slide / Start from the example template.
2. *Style?* — Default dark teal-and-violet / Match a reference image (I'll attach it) / My own colours (type them) / Describe a mood (e.g. "light and calm").
3. *Length?* — 10 min (about 8 slides) / 20 min (about 15) / 30-45 min (about 25) / Other.

Then ask once, in one short message, only for facts that cannot be options: event name, the image or file paths, logos and QR links. Build it with me: go one section at a time (opening, 2-4 key ideas, demo, close), showing the slide list after each round.
## The visual style

- Dark page `#0d1119` with a teal glow top-left and a violet glow bottom-right; cards `#10131b` with a `#232838` hairline border.
- Accents: teal `#2dd4bf`, violet `#8b5cf6`, green `#34d399`; the brand gradient runs teal to violet. Pillars take the accents in order.
- Type: Space Grotesk for headlines and captions, Inter for body text. Headlines tight (`letter-spacing:-.02em`), captions uppercase with wide tracking.
- Minimal beats busy: one idea per slide, about one slide per minute of talk time.

Change colours and fonts only through `theme` in the config. Tokens: `references/design-system.md`.

## Custom themes

`kit.py theme` builds a complete theme (page, gradient corners, cards, border, text, muted, three accents, text-on-accent, mode) from whatever you give it:

- **Manual inputs**: any subset of `--a1 --a2 --a3 --bg --bg2 --bg3 --card --border --text --muted --on-accent --font-head --font-body`, plus `--mode dark|light`. Values given are kept exactly; the rest are derived (missing accents get distinct hues; neutrals are tinted from the base hue).
- **Reference image**: `--from-image IMG` extracts the main colours. The most vivid distinct hues become the accents; the dominant colour sets the mode and, if it already suits it, is the page background. Manual values win over the image, so `--from-image logo.png --a1 '#e11d48'` pins one colour.
- Mode is auto: from `--bg` if given, else the image's dominant colour, else dark. In `light` mode the deck header uses each logo's `dark` file.
- Derived accents are nudged until readable on the page; colours the user gave are never changed, but `theme` and `check` warn when contrast is low. Pass the warning on, do not silently override their choice.
- Without `--write` nothing is saved. `--write` replaces the `theme` block of session.json (keeping existing fonts) and prints the previous one so it can be restored.
- PNG is read natively. JPEG/WebP/GIF need Pillow or macOS `sips`; if neither exists, look at the image yourself and pass the colours you see as `--a1/--a2/--a3/--bg`.
- Fonts other than Space Grotesk and Inter are not bundled: they render only if installed on the presenting machine. Say so if the user sets one.

## Slide types (deck.slides[].type)

`cover`, `statement`, `cards`, `steps`, `pillars`, `compare`, `media`, `video`, `links`, and `html` (escape hatch for custom markup using the engine's classes and `data-step` reveals). Text fields accept `**bold**`, `*italic*` and `[[gradient words]]`.

## Rules that prevent the usual mistakes

- **Paths resolve relative to `session.json`.** A wrong path fails `check` with the file name.
- **Logos:** the deck header uses the `light` file (for dark backgrounds), falling back to `src`.
- **YouTube embeds** need internet. If the player shows error 153, serve the folder over http (`python3 -m http.server`) instead of opening it from disk, and keep the "Watch on YouTube" fallback link.
- **Do not invent facts.** Copy you draft is a proposal; say so. Never fabricate URLs, names or numbers.
- **Never overwrite the user's files silently.** `init` refuses to overwrite an existing `session.json`; build output goes to `build/`.
- Slides are `min-height:100vh`, not scrollable inside: split dense content instead of shrinking it.

## Extending

Add a slide type: write `r_<name>(cfg, s, i, out_dir)` in `scripts/deck.py`, register it in `RENDER`, add its CSS to `assets/deck/deck.css`. Re-run `check` and `deck`, and look at the render.
