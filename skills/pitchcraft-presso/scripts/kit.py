#!/usr/bin/env python3
"""pitchcraft-presso: one session.json in, an interactive slide deck out.

  python3 kit.py init  [dir] [--from-outline talk.md] [--from-brainstorm ID|PATH] [theme options]
                                             write a starter session.json: from the example template, or from
                                             content you already have; theme options set the style up front
  python3 kit.py check session.json          validate the config and that every referenced file exists
  python3 kit.py deck  session.json [--out DIR]
  python3 kit.py theme [session.json] [--from-image IMG] [--mode dark|light] [--a1 HEX ...] [--write]
                                             build a theme from manual colours and/or a reference image;
                                             prints it, and saves it into session.json only with --write
"""
import argparse, pathlib, shutil, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import *
import deck as deck_mod
import theme as theme_mod
import outline as outline_mod


def check(cfg):
    problems = []
    th = cfg['theme']
    for k in theme_mod.COLOR_KEYS + ('on_accent',):
        if not re.fullmatch(r'#[0-9a-fA-F]{3}([0-9a-fA-F]{3})?', str(th[k])):
            problems.append(f'theme.{k} is not a hex colour: {th[k]}')
    if th.get('mode') not in ('dark', 'light'):
        problems.append(f'theme.mode must be "dark" or "light", not {th.get("mode")!r}')
    paths = []
    for lg in cfg['brand'].get('logos', []):
        paths += [lg.get('light'), lg.get('dark'), lg.get('src')]
    for i, s in enumerate(cfg.get('deck', {}).get('slides', [])):
        if s.get('type') not in deck_mod.RENDER:
            problems.append(f'deck.slides[{i}]: unknown type "{s.get("type")}"')
        paths += [s.get('image'), (s.get('qr') or {}).get('img')] + [it.get('img') for it in s.get('items', []) if isinstance(it, dict)]
    for p in filter(None, paths):
        if not resolve(cfg, p).exists():
            problems.append(f'missing file: {p}')
    if not cfg['session'].get('title'):
        problems.append('session.title is empty')
    return problems


def style_spec(a, extra=None):
    """Theme inputs from the command line, over those from an outline's front matter. -> (given, image, mode)"""
    extra = dict(extra or {})
    given = {}
    for k in theme_mod.COLOR_KEYS + ('on_accent',):
        v = getattr(a, k) or extra.get(k)
        if v:
            v = str(v)
            if not re.fullmatch(r'#?[0-9a-fA-F]{3}([0-9a-fA-F]{3})?', v):
                raise Die(f'theme {k} is not a hex colour: {v}')
            given[k] = v if v.startswith('#') else '#' + v
    for k in ('font_head', 'font_body'):
        if getattr(a, k) or extra.get(k):
            given[k] = getattr(a, k) or extra.get(k)
    mode = a.mode or extra.get('mode')
    if mode and mode not in ('dark', 'light'):
        raise Die(f'theme mode must be "dark" or "light", not {mode!r}')
    return given, a.from_image or extra.get('from_image'), mode


def make_theme(given, image, mode, base=None):
    pal = None
    if image:
        img = pathlib.Path(image)
        if not img.is_absolute() and base and not img.exists():
            img = pathlib.Path(base) / img
        pal = theme_mod.palette(img)
    th = theme_mod.derive(given, mode, pal)
    print(theme_mod.swatches(th, pal))
    for w in theme_mod.contrast_report(th):
        print('Warning:', w)
    return th


def cmd_init(a):
    dest = pathlib.Path(a.config or '.').resolve()
    target = dest / 'session.json'
    if target.exists():
        raise Die(f'{target} already exists; not overwriting.')
    cfg, notes = None, []
    otheme = {}
    if a.from_outline:
        cfg, otheme = outline_mod.from_outline(a.from_outline, dest)
        notes.append(f'content: {len(cfg["deck"]["slides"])} slides from {a.from_outline}')
    if a.from_brainstorm:
        b, stage = outline_mod.from_brainstorm(a.from_brainstorm)
        cfg = outline_mod.merge(cfg, b) if cfg else b
        notes.append(f'session details from brainstorm "{b["session"].get("brainstorm_id")}" (stage: {stage or "unknown"})'
                     + ('' if stage == 'final' else '; it is not finalized, so title/abstract may still change'))
    given, image, mode = style_spec(a, otheme)
    styled = bool(given or image or mode)
    dest.mkdir(parents=True, exist_ok=True)
    if cfg is None:  # no content given: the example template, as before
        cfg = json.loads((SKILL_DIR / 'examples' / 'session.example.json').read_text(encoding='utf-8'))
        shutil.copytree(SKILL_DIR / 'examples' / 'images', dest / 'images', dirs_exist_ok=True)
        notes.append('content: example template with placeholder images in ' + str(dest / 'images'))
    else:
        cfg = {'session': cfg['session'], 'brand': cfg.get('brand') or {'logos': []}, 'deck': cfg['deck']}
    if styled:
        cfg = {'theme': make_theme(given, image, mode, pathlib.Path.cwd()), **{k: v for k, v in cfg.items() if k != 'theme'}}
        notes.append('style: custom theme' + (f' from {image}' if image else ''))
    else:
        notes.append('style: default dark teal-and-violet (change later with "kit.py theme")')
    target.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'Wrote {target}\n  - ' + '\n  - '.join(notes))
    problems = check(load_config(target))
    if problems:
        print('Still to do before building:\n  - ' + '\n  - '.join(problems))
    print(f'Next: review and edit it, then run: python3 kit.py deck {target}')


def cmd_theme(a):
    given, image, mode = style_spec(a)
    if not given and not image:
        raise Die('Give a reference image (--from-image) and/or colours (--a1, --a2, --bg, ...).')
    th = make_theme(given, image, mode, pathlib.Path(a.config).resolve().parent if a.config else None)
    print(json.dumps({'theme': th}, indent=2))
    if a.write:
        if not a.config:
            raise Die('--write needs the path to session.json.')
        p = pathlib.Path(a.config).resolve()
        data = json.loads(p.read_text(encoding='utf-8'))
        old = data.get('theme', {})
        for k in ('font_head', 'font_body'):  # keep fonts the user already chose
            if k in old and k not in th:
                th[k] = old[k]
        data['theme'] = th
        p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        print(f'Saved theme to {p} (previous theme: {json.dumps(old) if old else "none"})')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('cmd', choices=['init', 'check', 'deck', 'theme'])
    ap.add_argument('config', nargs='?')
    ap.add_argument('--out', help='output folder (default: ./build next to the config)')
    c = ap.add_argument_group('init: start from content you have')
    c.add_argument('--from-outline', metavar='MD', help='Markdown outline: "## Title" per slide, front matter for session and theme (references/outline-format.md)')
    c.add_argument('--from-brainstorm', metavar='ID|PATH', help='a pitchcraft-brainstorm session (id in ~/.pitchcraft/sessions or $PITCHCRAFT_DIR, or a path)')
    t = ap.add_argument_group('theme options (theme, and init)')
    t.add_argument('--from-image', metavar='IMG', help='reference image (logo, brand sheet, screenshot) to take the palette from')
    t.add_argument('--mode', choices=['dark', 'light'], help='page style (default: from --bg, else the image, else dark)')
    for k in theme_mod.COLOR_KEYS + ('on_accent',):
        t.add_argument(f'--{k.replace("_", "-")}', dest=k, metavar='HEX', help=f'set {k} yourself (wins over the image)')
    t.add_argument('--font-head', dest='font_head'); t.add_argument('--font-body', dest='font_body')
    t.add_argument('--write', action='store_true', help='save the theme into session.json (replaces its "theme" block)')
    a = ap.parse_args()
    try:
        if a.cmd == 'theme':
            return cmd_theme(a)
        if a.cmd == 'init':
            return cmd_init(a)
        if not a.config:
            raise Die('Give the path to session.json.')
        cfg = load_config(a.config)
        out = pathlib.Path(a.out).resolve() if a.out else cfg['_base'] / 'build'
        if a.cmd == 'check':
            problems = check(cfg)
            if not problems:
                for w in theme_mod.contrast_report(cfg['theme']):
                    print('Warning:', w)
            print('\n'.join(['Problems:'] + ['  - ' + p for p in problems]) if problems else 'OK: config is valid and every referenced file exists.')
            sys.exit(1 if problems else 0)
        problems = check(cfg)
        if problems:
            raise Die('Fix these first:\n  - ' + '\n  - '.join(problems))
        p, n = deck_mod.build(cfg, out / 'deck')
        print(f'deck: {n} slides -> {p}')
    except Die as e:
        print('Error:', e, file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
