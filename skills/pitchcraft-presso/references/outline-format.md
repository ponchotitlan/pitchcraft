# Outline format (`kit.py init --from-outline talk.md`)

A plain Markdown file that becomes `session.json`. Full example: `examples/outline.example.md`. Image paths are relative to the outline file and are rewritten for `session.json`.

## Front matter (optional)

```yaml
---
title: Short session title          # session.title (page title)
headline: Longer cover title with [[gradient words]]
event: Example Conf 2026
pillars: Own it, Run it, Trust it   # comma list, or [a, b, c]
lang: en
logo: images/logo-white.svg         # header logo for dark themes
logo_dark: images/logo.svg          # header logo for light themes
logo_name: Acme                     # alt text
theme:                              # same keys as `kit.py theme` flags
  from_image: brand.png             # palette from a reference image
  mode: light                       # dark | light
  a1: "#e11d48"                     # any of a1 a2 a3 bg bg2 bg3 card border text muted on_accent font_head font_body
---
```

## Slides

- `# Title` is the cover; the text under it is the subtitle.
- Each `## Title` starts a slide. Force a type with `## [cards] Title` (any type in `slide-types.md`); otherwise it is guessed:

| Slide body contains | Type guessed |
|---|---|
| a YouTube URL | `video` |
| an image `![alt](path)` | `media` |
| exactly two `### Label` lists | `compare` (second = highlighted) |
| bullets that all hold a URL | `links` |
| other bullets or a numbered list | `steps` |
| only text | `statement` |

- Plain text lines become the `lead`; `> text` becomes the `punch`.
- Bullet items read as `emoji **Title** - text`, `Title - text` or `Title: text` (all parts optional). Under `[cards]` they become cards; under `[pillars]` they override `session.pillars`; under `links` the URL is pulled out of the line.
- `## [html] Title` keeps the body as raw markup.
- `**bold**`, `*italic*` and `[[gradient words]]` work everywhere.
