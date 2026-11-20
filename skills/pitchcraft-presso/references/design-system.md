# Design system

CSS variables the deck defines (from `theme`): `--bg --bg2 --bg3 --card --border --text --muted --a1 --a2 --a3 --a1-rgb --a2-rgb --bg-rgb --text-rgb --on-accent --grad --font-head --font-body`, and `data-mode="dark|light"` on `<html>`. Use these instead of literal colours in custom CSS or `html` slides, so the markup works with any theme.

| Token | Default | Use |
|---|---|---|
| bg / bg2 / bg3 | #0d1119 / #0a1e25 / #171127 | page and its diagonal gradient (teal-tinted top-left, violet-tinted bottom-right) |
| card / border | #10131b / #232838 | cards, pills, tiles |
| text / muted | #eef1f7 / #a3abbd | body / secondary |
| a1 teal / a2 violet / a3 green | #2dd4bf / #8b5cf6 / #34d399 | accents; gradient = a1 to a2 |
| on_accent | #05060a | text on the gradient (step numbers) |
| mode | dark | `light` switches the header to the logos' `dark` files |

Custom themes: `kit.py theme` (manual colours and/or `--from-image`), see SKILL.md.

Type scale (deck): h1 clamp(40px, 5.8vw, 100px); h2 clamp(32px, 4.2vw, 68px); body clamp(18px, 1.6vw, 26px). Radii: cards 16-18px, pills 999px, QR tiles 22-26px. Headlines weight 700 with -0.02em tracking; captions uppercase with 0.12-0.14em tracking in Space Grotesk.

Accessibility: `kit.py theme` and `kit.py check` warn when text, muted or a1 fall below readable contrast (4.5:1 text, 3:1 muted/accent); every logo and QR has alt text; reveal animations never leave content hidden (a 2.5 s safety net shows everything).
