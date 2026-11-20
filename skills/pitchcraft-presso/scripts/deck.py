"""Build the slide deck (one self-contained index.html) from the 'deck' section of the session config."""
import pathlib, shutil
from common import *

LAYOUT_NOTES = """slide types: cover, statement, cards, steps, pillars, compare, media, video, links, html"""


def _title(s, default):
    return s.get('index_title') or re.sub(r'<[^>]+>|\[\[|\]\]|\*\*', '', s.get('title') or default)


def _attrs(s, i, mode):
    t = esc(_title(s, f'Slide {i + 1}'))
    mn = f' data-min="{esc(s["min"])}"' if s.get('min') else ''
    sid = f' id="{esc(s["id"])}"' if s.get('id') else ''
    return f'{sid}{mn} data-title="{t}" data-mode="{esc(s.get("mode", mode))}"'


def _img(cfg, out_dir, rel, what):
    return relpath(need_file(cfg, rel, what), out_dir)


def r_cover(cfg, s, i, out_dir):
    se = cfg['session']
    title = s.get('title') or se.get('headline') or se.get('title', 'Session title')
    sub = s.get('sub') or (se.get('title') if title != se.get('title') else '')
    event = s.get('event') or se.get('event', '')
    qr = ''
    if s.get('qr'):
        q = s['qr']
        href = esc(q.get('href', ''))
        qr = (f'<aside class="takehome"><a class="glare" href="{href}" target="_blank" rel="noopener"><span class="tile">'
              f'<img src="{_img(cfg, out_dir, q["img"], "cover QR")}" alt="{esc(q.get("alt", "QR code"))}"></span></a>'
              f'<p>{esc(q.get("caption", ""))}</p></aside>')
    return (f'<section class="block cover" {_attrs(s, i, "Cover")}>\n<div class="cover-grid"><div class="cover-text">'
            + (f'<p class="cover-event">{esc(event)}</p>' if event else '')
            + f'<h1>{rich(title)}</h1>' + (f'<p class="sub">{esc(sub)}</p>' if sub else '') + f'</div>{qr}</div></section>')


def r_statement(cfg, s, i, out_dir):
    return (f'<section class="block" {_attrs(s, i, "Talk")}>'
            + (f'<p class="eyebrow">{esc(s["eyebrow"])}</p>' if s.get('eyebrow') else '')
            + f'<h2>{rich(s.get("title", ""))}</h2>'
            + (f'<p class="lead">{rich(s["lead"])}</p>' if s.get('lead') else '')
            + (f'<p class="punch">{rich(s["punch"])}</p>' if s.get('punch') else '') + '</section>')


def r_cards(cfg, s, i, out_dir):
    cards = s.get('cards', [])
    cols = s.get('columns', min(3, max(1, len(cards))))
    items = ''.join(f'<div class="card" data-step="{k + 1}">'
                    + (f'<span class="e" aria-hidden="true">{esc(c["emoji"])}</span>' if c.get('emoji') else '')
                    + f'<h3>{rich(c.get("title", ""))}</h3>' + (f'<p>{rich(c["text"])}</p>' if c.get('text') else '') + '</div>'
                    for k, c in enumerate(cards))
    return (f'<section class="block compact" {_attrs(s, i, "Talk")}><h2>{rich(s.get("title", ""))}</h2>'
            + (f'<p class="lead">{rich(s["lead"])}</p>' if s.get('lead') else '')
            + f'<div class="cards" style="--cols:{cols}">{items}</div>'
            + (f'<p class="punch">{rich(s["punch"])}</p>' if s.get('punch') else '') + '</section>')


def r_steps(cfg, s, i, out_dir):
    items = ''.join(f'<li data-step="{k + 1}"><b>{rich(it if isinstance(it, str) else it.get("title", ""))}</b>'
                    + ('' if isinstance(it, str) or not it.get('text') else f'<span>{rich(it["text"])}</span>') + '</li>'
                    for k, it in enumerate(s.get('items', [])))
    return (f'<section class="block compact" {_attrs(s, i, "Talk")}><h2>{rich(s.get("title", ""))}</h2>'
            + (f'<p class="lead">{rich(s["lead"])}</p>' if s.get('lead') else '') + f'<ol class="steps">{items}</ol></section>')


def r_pillars(cfg, s, i, out_dir):
    names = s.get('items') or cfg['session'].get('pillars') or []
    cols = pillar_colors(cfg['theme'], len(names))
    items = ''.join(f'<div class="pillar" style="--pc:{c}" data-step="{k + 1}"><i></i>{esc(n)}</div>' for k, (n, c) in enumerate(zip(names, cols)))
    return (f'<section class="block" {_attrs(s, i, "Talk")}><h2>{rich(s.get("title", ""))}</h2>'
            + (f'<p class="lead">{rich(s["lead"])}</p>' if s.get('lead') else '') + f'<div class="pillars">{items}</div></section>')


def r_compare(cfg, s, i, out_dir):
    def col(c, cls):
        return (f'<div class="col {cls}" data-step="{1 if cls == "bad" else 2}"><h3>{rich(c.get("label", ""))}</h3><ul>'
                + ''.join(f'<li>{rich(x)}</li>' for x in c.get('items', [])) + '</ul></div>')
    return (f'<section class="block compact" {_attrs(s, i, "Talk")}><h2>{rich(s.get("title", ""))}</h2>'
            f'<div class="cols">{col(s.get("left", {}), "bad")}{col(s.get("right", {}), "good")}</div>'
            + (f'<p class="punch">{rich(s["punch"])}</p>' if s.get('punch') else '') + '</section>')


def r_media(cfg, s, i, out_dir):
    img = ''
    if s.get('image'):
        img = f'<figure><img src="{_img(cfg, out_dir, s["image"], "media slide image")}" alt="{esc(s.get("alt", ""))}"></figure>'
    text = (f'<div><h2>{rich(s.get("title", ""))}</h2>' + (f'<div class="cue">{rich(s["cue"])}</div>' if s.get('cue') else '')
            + (f'<p class="lead">{rich(s["lead"])}</p>' if s.get('lead') else '') + '</div>')
    return f'<section class="block" {_attrs(s, i, s.get("mode", "Talk"))}><div class="media-grid">{text}{img}</div></section>'


def r_video(cfg, s, i, out_dir):
    vid = s.get('youtube', '')
    if not vid:
        raise Die(f'Slide {i + 1} (video) needs a "youtube" video id.')
    link = esc(s.get('url') or f'https://youtu.be/{vid}')
    return (f'<section class="block video" {_attrs(s, i, "Demo")}>'
            f'<div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/{esc(vid)}" title="{esc(s.get("title", "Video"))}" loading="lazy" '
            'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; fullscreen" '
            'referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>'
            f'<p class="video-link"><a href="{link}" target="_blank" rel="noopener">Not playing? Watch on YouTube</a></p></section>')


def r_links(cfg, s, i, out_dir):
    items = []
    for k, it in enumerate(s.get('items', [])):
        href = esc(it.get('url', ''))
        shown = esc(re.sub(r'^https?://(www\.)?', '', it.get('url', '')).rstrip('/'))
        qr = ''
        if it.get('img'):
            qr = (f'<a class="glare" href="{href}" target="_blank" rel="noopener" tabindex="-1" aria-hidden="true"><span class="tile">'
                  f'<img src="{_img(cfg, out_dir, it["img"], "QR image")}" alt="QR code for {esc(it.get("title", ""))}"></span></a>')
        items.append(f'<div class="qr" data-step="{k + 1}">{qr}'
                     + (f'<span class="sub2">{esc(it["sub"])}</span>' if it.get('sub') else '')
                     + f'<a class="ttl" href="{href}" target="_blank" rel="noopener">{esc(it.get("emoji", ""))} {esc(it.get("title", ""))}</a><span class="u">{shown}</span></div>')
    return (f'<section class="block qa" {_attrs(s, i, "Q&A")}><h2>{rich(s.get("title", "Questions"))}</h2>'
            + (f'<p class="lead">{rich(s["lead"])}</p>' if s.get('lead') else '') + f'<div class="qrs">{"".join(items)}</div></section>')


def r_html(cfg, s, i, out_dir):
    """Escape hatch: your own markup inside a standard section. Use the engine's classes and tokens."""
    return f'<section class="block {esc(s.get("class", ""))}" {_attrs(s, i, "Talk")}>{s.get("html", "")}</section>'


RENDER = {'cover': r_cover, 'statement': r_statement, 'cards': r_cards, 'steps': r_steps, 'pillars': r_pillars,
          'compare': r_compare, 'media': r_media, 'video': r_video, 'links': r_links, 'html': r_html}


def build(cfg, out_dir):
    out_dir = pathlib.Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    slides = cfg.get('deck', {}).get('slides', [])
    if not slides:
        raise Die('The config has no deck.slides. Run "kit.py init" for a starting point.')
    parts = []
    for i, s in enumerate(slides):
        t = s.get('type')
        if t not in RENDER:
            raise Die(f'Slide {i + 1}: unknown type "{t}". Known types: {", ".join(RENDER)}.')
        parts.append(RENDER[t](cfg, s, i, out_dir))

    th = cfg['theme']
    # fonts: copy the bundled ones next to the deck, so the folder is self-contained
    fdir = out_dir / 'fonts'
    fdir.mkdir(exist_ok=True)
    faces = []
    for f in (ASSETS / 'fonts').glob('*.woff2'):
        shutil.copy(f, fdir / f.name)
    for fam, files in (('Space Grotesk', [('400', 'SpaceGrotesk-400'), ('500', 'SpaceGrotesk-500'), ('700', 'SpaceGrotesk-500')]),
                       ('Inter', [('400', 'Inter-400'), ('500', 'Inter-500'), ('600', 'Inter-600'), ('700', 'Inter-700')])):
        for w, fn in files:
            faces.append(f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:normal;font-display:swap;src:url("fonts/{fn}.woff2") format("woff2")}}')
    for fn in ('OFL.txt', 'SpaceGrotesk-OFL.txt'):
        if (ASSETS / 'fonts' / fn).exists():
            shutil.copy(ASSETS / 'fonts' / fn, fdir / fn)

    r1, r2, rb, rt = (','.join(map(str, rgb(th[k]))) for k in ('a1', 'a2', 'bg', 'text'))
    root = (f'--bg:{th["bg"]};--bg2:{th["bg2"]};--bg3:{th["bg3"]};--card:{th["card"]};--border:{th["border"]};--text:{th["text"]};--muted:{th["muted"]};'
            f'--a1:{th["a1"]};--a2:{th["a2"]};--a3:{th["a3"]};--a1-rgb:{r1};--a2-rgb:{r2};--bg-rgb:{rb};--text-rgb:{rt};--on-accent:{th["on_accent"]};'
            f'--grad:linear-gradient(90deg,{th["a1"]},{th["a2"]});--font-head:"{th["font_head"]}";--font-body:"{th["font_body"]}"')

    logos = []
    for lg in cfg['brand'].get('logos', []):
        src = logo_variant(lg, th.get('mode', 'dark'))
        if src:
            logos.append(f'<img src="{_img(cfg, out_dir, src, "brand logo " + lg.get("name", ""))}" alt="{esc(lg.get("name", ""))}" '
                         f'style="height:{int(lg.get("height", 34))}px" onerror="this.style.display=\'none\'">')

    shell = (ASSETS / 'deck' / 'shell.html').read_text(encoding='utf-8')
    title = cfg['session'].get('title', 'Session')
    page = (shell.replace('__MODE__', 'light' if th.get('mode') == 'light' else 'dark').replace('__LANG__', cfg['session'].get('lang', 'en')).replace('__BG__', th['bg']).replace('__TITLE__', esc(title))
            .replace('__FONTFACES__', '\n'.join(faces)).replace('__ROOT__', root)
            .replace('__CSS__', (ASSETS / 'deck' / 'deck.css').read_text(encoding='utf-8'))
            .replace('__BRANDBAR__', ''.join(logos)).replace('__SLIDES__', '\n\n'.join(parts))
            .replace('__JS__', (ASSETS / 'deck' / 'deck.js').read_text(encoding='utf-8')))
    (out_dir / 'index.html').write_text(page, encoding='utf-8')
    return out_dir / 'index.html', len(parts)
