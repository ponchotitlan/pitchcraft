"""Shared helpers for pitchcraft-presso: config loading, theme and paths."""
import html, json, os, pathlib, re, shutil, sys

SKILL_DIR = pathlib.Path(__file__).resolve().parent.parent
ASSETS = SKILL_DIR / 'assets'

DEFAULT_THEME = {
    'bg': '#0d1119', 'bg2': '#0a1e25', 'bg3': '#171127',          # page background and its two gradient corners
    'card': '#10131b', 'border': '#232838',
    'text': '#eef1f7', 'muted': '#a3abbd',
    'a1': '#2dd4bf', 'a2': '#8b5cf6', 'a3': '#34d399',            # teal, violet, green: the three accents
    'on_accent': '#05060a',                                        # text drawn on the accent gradient (step badges)
    'mode': 'dark',                                                # 'dark' or 'light': picks the logo variant
    'font_head': 'Space Grotesk', 'font_body': 'Inter',
}


class Die(Exception):
    pass


def load_config(path):
    p = pathlib.Path(path).resolve()
    if not p.exists():
        raise Die(f'Config not found: {p}')
    try:
        cfg = json.loads(p.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        raise Die(f'{p.name} is not valid JSON: {e}')
    cfg['_base'] = p.parent
    cfg['theme'] = {**DEFAULT_THEME, **cfg.get('theme', {})}
    cfg.setdefault('session', {})
    cfg.setdefault('brand', {})
    return cfg


def resolve(cfg, rel_path):
    """A path written in the config, resolved against the config file's folder."""
    return (cfg['_base'] / rel_path).resolve()


def need_file(cfg, rel_path, what):
    p = resolve(cfg, rel_path)
    if not p.exists():
        raise Die(f'{what}: file not found: {rel_path} (looked in {p})')
    return p


def relpath(target, from_dir):
    return pathlib.Path(os.path.relpath(pathlib.Path(target), pathlib.Path(from_dir))).as_posix()


def esc(s):
    return html.escape(str(s), quote=True)


def rich(s):
    """Escape, then allow **bold**, *italic* and [[gradient words]] in config text."""
    s = esc(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<![\w*])\*(?=\S)(.+?)(?<=\S)\*(?![\w*])', r'<em>\1</em>', s)
    s = re.sub(r'\[\[(.+?)\]\]', r'<span class="grad">\1</span>', s)
    return s


def rgb(hexstr):
    h = hexstr.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def accents(theme):
    return [theme['a1'], theme['a2'], theme['a3']]


def pillar_colors(theme, n):
    a = accents(theme)
    return [a[i % 3] for i in range(n)]


def logo_variant(logo, bg='dark'):
    """Pick the right logo file for a dark or light background. 'light' = for dark backgrounds."""
    if bg == 'dark':
        return logo.get('light') or logo.get('src')
    return logo.get('dark') or logo.get('src')
