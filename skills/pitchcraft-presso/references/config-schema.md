# session.json schema

All paths are relative to the folder holding `session.json`.

```jsonc
{
  "theme":   { "a1": "#2dd4bf", "a2": "#8b5cf6", "a3": "#34d399",       // accents (hex)
               "bg": "#0d1119", "bg2": "#0a1e25", "bg3": "#171127",     // page + gradient corners
               "card": "#10131b", "border": "#232838", "text": "#eef1f7", "muted": "#a3abbd",
               "on_accent": "#05060a",                                   // text on the gradient (step badges)
               "mode": "dark",                                           // "dark" | "light"; light uses logos' "dark" file
               "font_head": "Space Grotesk", "font_body": "Inter" },    // all optional; generate with `kit.py theme`
  "session": { "title": "...",                // required: page title
               "headline": "...",             // optional longer title (supports [[gradient]])
               "event": "Conf name",          // eyebrow on the cover
               "pillars": ["Own it", "Run it", "Trust it"],   // 2-4 key ideas, used by the 'pillars' slide
               "lang": "en",
               "abstract": "...", "takeaway": "...", "tone": "...",   // optional, not rendered: context imported
               "audience": "...", "brainstorm_id": "..." },           // from a brainstorm session, for drafting slides
  "brand":   { "logos": [ { "name": "Acme", "light": "img/acme-white.svg",   // header logo on a dark theme
                                            "dark": "img/acme.svg",         // header logo on a light theme
                                            "src": "img/acme.svg",          // fallback for either
                                            "height": 38 } ] },
  "deck":    { "slides": [ /* see slide-types.md */ ] }
}
```

Text fields accept `**bold**`, `*italic*` and `[[gradient words]]`.
