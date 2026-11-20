"""Start a session.json from content the user already has: a Markdown outline and/or a pitchcraft-brainstorm session.

Outline format (full spec: references/outline-format.md):

    ---
    title: Short session title
    headline: Longer cover title with [[gradient words]]
    event: Example Conf 2026
    pillars: Own it, Run it, Trust it
    lang: en
    logo: images/logo-white.svg     (optional; logo_dark: for light themes, logo_name: alt text)
    theme:
      from_image: brand.png
      mode: light
      a1: "#e11d48"
    ---
    # Cover title            (one '#' heading = cover slide; text below = subtitle)
    ## Slide title           (each '##' = one slide; type guessed, or forced: '## [cards] Title')
    Lead paragraph.
    > Punch line.
    - bullet items
"""
import json, os, pathlib, re
from common import Die

TYPES = ('cover', 'statement', 'cards', 'steps', 'pillars', 'compare', 'media', 'video', 'links', 'html')
YT = re.compile(r'(?:youtu\.be/|youtube(?:-nocookie)?\.com/(?:watch\?v=|embed/|shorts/))([\w-]{6,})')
URL = re.compile(r'https?://\S+')


def _scalar(v):
    v = v.strip()
    if v[:1] not in '"\'':  # drop a trailing "  # comment" (hex colours must be quoted, as in YAML)
        v = re.sub(r'\s+#.*$', '', v)
    if len(v) >= 2 and v[0] == v[-1] and v[0] in '"\'':
        return v[1:-1]
    if v.startswith('[') and v.endswith(']'):
        v = v[1:-1]
        return [_scalar(x) for x in v.split(',') if x.strip()]
    return v


def front_matter(text):
    """A small YAML subset: `key: value`, `key: a, b` lists for pillars, and one level of indented children."""
    m = re.match(r'---\s*\n(.*?)\n---\s*\n', text, re.S)
    if not m:
        return {}, text
    meta, parent = {}, None
    for raw in m.group(1).splitlines():
        if not raw.strip() or raw.lstrip().startswith('#'):
            continue
        k, _, v = raw.strip().partition(':')
        if not _:
            raise Die(f'Outline front matter: cannot read line "{raw.strip()}" (expected "key: value").')
        k = k.strip()
        if raw[:1] in ' \t' and parent is not None:
            meta[parent][k] = _scalar(v)
        elif v.strip():
            meta[k], parent = _scalar(v), None
        else:
            meta[k], parent = {}, k
    if isinstance(meta.get('pillars'), str):
        meta['pillars'] = [p.strip() for p in meta['pillars'].split(',') if p.strip()]
    return meta, text[m.end():]


def _split_item(t):
    """'🔧 **Title** - text' / 'Title: text' -> (emoji, title, text)."""
    emoji = ''
    m = re.match(r'([^\w\s*\[(`"\'<>-]+)\s+(.*)', t)
    if m:
        emoji, t = m.group(1), m.group(2)
    m = re.match(r'\*\*(.+?)\*\*\s*(?:[-:–—]\s*)?(.*)', t) or re.match(r'(.+?)\s+[–—-]\s+(.*)', t) or re.match(r'([^:]{1,60}):\s+(.*)', t)
    return (emoji, m.group(1).strip(), m.group(2).strip()) if m else (emoji, t.strip(), '')


def _slide(kind, title, body, rel):
    lead, punch, bullets, subs, image, alt, yt, url, cur = [], [], [], [], None, '', None, None, None
    for line in body:
        s = line.strip()
        if not s:
            continue
        if s.startswith('### '):
            cur = {'label': s[4:].strip(), 'items': []}
            subs.append(cur)
        elif re.match(r'[-*+]\s+|\d+[.)]\s+', s):
            item = re.sub(r'^([-*+]|\d+[.)])\s+', '', s)
            (cur['items'] if cur is not None else bullets).append(item)
        elif s.startswith('>'):
            punch.append(s.lstrip('> ').strip())
        elif re.match(r'!\[', s):
            m = re.match(r'!\[(.*?)\]\((.+?)\)', s)
            if m:
                alt, image = m.group(1), rel(m.group(2))
        elif YT.search(s) and not lead:
            yt, url = YT.search(s).group(1), URL.search(s).group(0)
        else:
            lead.append(s)
    if not kind:  # guess the type from what the slide contains
        kind = ('video' if yt else 'media' if image else 'compare' if len(subs) == 2
                else 'links' if bullets and all(URL.search(b) for b in bullets)
                else 'steps' if bullets else 'statement')
    s = {'type': kind}
    if title:
        s['title'] = title
    if lead and kind != 'cover':
        s['lead'] = ' '.join(lead)
    if punch:
        s['punch'] = ' '.join(punch)
    if kind == 'cover':
        if lead:
            s['sub'] = ' '.join(lead)
    elif kind == 'steps':
        s['items'] = [b if not _split_item(b)[2] else {'title': _split_item(b)[1], 'text': _split_item(b)[2]} for b in bullets]
    elif kind == 'cards':
        s['cards'] = [dict(zip(('emoji', 'title', 'text'), _split_item(b))) for b in bullets]
        s['cards'] = [{k: v for k, v in c.items() if v} for c in s['cards']]
    elif kind == 'pillars' and bullets:
        s['items'] = bullets
    elif kind == 'compare':
        if len(subs) != 2:
            raise Die(f'Outline slide "{title}": a compare slide needs exactly two "### Label" lists.')
        s['left'], s['right'] = subs
    elif kind == 'media':
        if image:
            s['image'], s['alt'] = image, alt
    elif kind == 'video':
        if not yt:
            raise Die(f'Outline slide "{title}": a video slide needs a YouTube URL line.')
        s['youtube'], s['url'] = yt, url
    elif kind == 'links':
        items = []
        for b in bullets:
            m = URL.search(b)
            emoji, t, _ = _split_item(URL.sub('', b).strip(' -:–—'))
            it = {'title': t or (m.group(0) if m else b), 'url': m.group(0) if m else ''}
            if emoji:
                it['emoji'] = emoji
            items.append(it)
        s['items'] = items
    elif kind == 'html':
        s['html'] = '\n'.join(body).strip()
        s.pop('lead', None)
    elif bullets:  # statement with bullets: keep them in the lead rather than dropping them
        s['lead'] = (s.get('lead', '') + ' ' + ' · '.join(bullets)).strip()
    return s


def from_outline(path, dest):
    """Parse a Markdown outline. Image paths are rewritten relative to `dest` (where session.json goes)."""
    path = pathlib.Path(path).resolve()
    if not path.exists():
        raise Die(f'Outline not found: {path}')
    meta, body = front_matter(path.read_text(encoding='utf-8'))

    def rel(p):
        if re.match(r'https?://', p) or os.path.isabs(p):
            return p
        return pathlib.Path(os.path.relpath(path.parent / p, dest)).as_posix()

    slides, cur = [], None
    for line in body.splitlines():
        m = re.match(r'(#{1,2})\s+(?:\[(\w+)\]\s*)?(.*)', line)
        if m:
            kind = m.group(2)
            if kind and kind not in TYPES:
                raise Die(f'Outline: unknown slide type [{kind}] in "{line.strip()}". Known: {", ".join(TYPES)}.')
            cur = [kind or ('cover' if m.group(1) == '#' else None), m.group(3).strip(), []]
            slides.append(cur)
        elif cur is not None:
            cur[2].append(line)
    if not slides:
        raise Die(f'{path.name}: no slides found. Start each slide with "## Title" (and the cover with "# Title").')
    theme = meta.pop('theme', {}) or {}
    if not isinstance(theme, dict):
        raise Die('Outline front matter: "theme" must be an indented block (from_image, mode, a1, ...).')
    if theme.get('from_image'):
        theme['from_image'] = str((path.parent / theme['from_image']).resolve())
    session = {k: meta[k] for k in ('title', 'headline', 'event', 'pillars', 'lang', 'abstract') if k in meta}
    out = {'session': session}
    if meta.get('logo') or meta.get('logo_dark'):
        lg = {'name': meta.get('logo_name') or session.get('title', 'Logo')}
        if meta.get('logo'):
            lg['light'] = rel(meta['logo'])
        if meta.get('logo_dark'):
            lg['dark'] = rel(meta['logo_dark'])
        out['brand'] = {'logos': [lg]}
    return {**out, 'deck': {'slides': [_slide(k, t, b, rel) for k, t, b in slides]}}, theme


def brainstorm_store():
    return pathlib.Path(os.environ.get('PITCHCRAFT_DIR') or pathlib.Path.home() / '.pitchcraft' / 'sessions').expanduser()


def from_brainstorm(ref):
    """Load a pitchcraft-brainstorm session (a path, or an id in its store) -> session fields + a minimal deck."""
    p = pathlib.Path(ref).expanduser()
    if not p.exists():
        p = brainstorm_store() / (ref if ref.endswith('.json') else ref + '.json')
    if not p.exists():
        found = sorted(brainstorm_store().glob('*.json'), key=lambda f: f.stat().st_mtime, reverse=True)[:5]
        hint = ('Recent sessions: ' + ', '.join(f.stem for f in found)) if found else f'No sessions in {brainstorm_store()}.'
        raise Die(f'Brainstorm session not found: {ref}. {hint}')
    try:
        b = json.loads(p.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        raise Die(f'{p.name} is not valid JSON: {e}')
    ctx, fin = b.get('context', {}), b.get('final', {})
    title = fin.get('title') or b.get('title', {}).get('current', '')
    abstract = fin.get('abstract') or b.get('abstract', {}).get('current', '')
    session = {k: v for k, v in {
        'title': title, 'event': ctx.get('event_name', ''), 'lang': ctx.get('language', ''),
        'abstract': abstract, 'takeaway': ctx.get('key_takeaway', ''), 'tone': ctx.get('tone', ''),
        'audience': ctx.get('audience_level', ''), 'brainstorm_id': b.get('id', p.stem)}.items() if v}
    if session.get('lang') and len(session['lang']) > 5:  # "English" -> leave for the assistant; keep codes like "en"
        session['language'] = session.pop('lang')
    slides = [{'type': 'cover', 'title': title}]
    if ctx.get('key_takeaway'):
        slides.append({'type': 'statement', 'eyebrow': 'The takeaway', 'title': ctx['key_takeaway']})
    return {'session': session, 'deck': {'slides': slides}}, b.get('stage', '')


def merge(base, extra):
    """Fill fields of `base` from `extra` without overriding what base already has; slides come from base if it has any."""
    out = {'session': {**extra.get('session', {}), **base.get('session', {})}}
    if base.get('brand') or extra.get('brand'):
        out['brand'] = base.get('brand') or extra.get('brand')
    out['deck'] = base.get('deck') if base.get('deck', {}).get('slides') else extra.get('deck', {'slides': []})
    return out
