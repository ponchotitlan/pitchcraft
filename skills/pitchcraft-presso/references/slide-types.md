# Slide types

Common fields on every slide: `title`, `index_title` (label in the G index), `id`, `min` ("5-6.5", timing note), `mode` (label).
Text supports `**bold**`, `*italic*` and `[[gradient words]]`.

| type | fields | notes |
|---|---|---|
| `cover` | `title`, `sub`, `event`, `qr: {img, href, caption, alt}` | Opening slide. `title` falls back to `session.headline`. The QR gets the animated glare border. |
| `statement` | `eyebrow`, `title`, `lead`, `punch` | One idea, big. The default workhorse. |
| `cards` | `title`, `lead`, `columns` (1-4), `cards: [{emoji,title,text}]`, `punch` | Items reveal one after another. 3 to 6 cards. |
| `steps` | `title`, `lead`, `items: ["text" or {title,text}]` | Numbered list with gradient badges. |
| `pillars` | `title`, `lead`, `items` (default `session.pillars`) | Coloured pills, one per key idea. |
| `compare` | `title`, `left: {label,items}`, `right: {label,items}`, `punch` | Right column is the highlighted choice. |
| `media` | `title`, `cue`, `lead`, `image`, `alt`, `mode` | Text left, image/GIF right. Good for demo setups and memes. |
| `video` | `youtube` (id), `title`, `url` | YouTube embed, centred, with a "Watch on YouTube" fallback. Needs internet and a page served over http(s) or opened from disk with a Referer-capable browser; if the player shows error 153, serve the folder over http. |
| `links` | `title`, `lead`, `items: [{emoji,title,url,sub,img}]` | Closing slide: QR (optional) + clickable title + URL. |
| `html` | `html`, `class` | Raw markup inside a standard `<section class="block">`. Use `data-step="n"` on children to reveal them in order. |

Keys at runtime: arrows/space/PageUp/PageDown move, `G` opens the slide index, `F` toggles full screen, Home/End jump. Append `?shot=N` to the URL to show slide N alone, fully revealed (for screenshots and PDF export).
