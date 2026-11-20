"""Theme builder: a full deck theme from manual colours and/or a reference image's palette.

Standard library only. PNG is decoded natively; other formats (JPEG, WebP, GIF...) go through
Pillow if it is installed, else macOS `sips`, else you are asked to convert the image to PNG.
"""
import colorsys, pathlib, shutil, struct, subprocess, tempfile, zlib
from common import Die, rgb

COLOR_KEYS = ('bg', 'bg2', 'bg3', 'card', 'border', 'text', 'muted', 'a1', 'a2', 'a3')


# ---------- colour maths ----------

def to_hex(c):
    return '#%02x%02x%02x' % tuple(max(0, min(255, round(v))) for v in c)


def hls(c):
    return colorsys.rgb_to_hls(*(v / 255 for v in c))


def from_hls(h, l, s):
    return tuple(v * 255 for v in colorsys.hls_to_rgb(h % 1, max(0, min(1, l)), max(0, min(1, s))))


def luminance(c):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def hue_dist(a, b):
    d = abs(a - b) % 1
    return min(d, 1 - d)


def readable(c, bg, target):
    """Nudge c's lightness (keeping hue) until it reaches `target` contrast against bg."""
    h, l, s = hls(c)
    dark_bg = luminance(bg) < 0.2
    step = 0.02 if dark_bg else -0.02
    out = c
    for _ in range(50):
        if contrast(out, bg) >= target:
            return out
        l += step
        out = from_hls(h, l, s)
    return out


# ---------- image decoding ----------

def _png_pixels(data):
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        return None
    pos, idat, plte, trns = 8, b'', None, None
    w = h = depth = ctype = interlace = None
    while pos < len(data):
        n, typ = struct.unpack('>I4s', data[pos:pos + 8])
        chunk = data[pos + 8:pos + 8 + n]
        pos += 12 + n
        if typ == b'IHDR':
            w, h, depth, ctype, _, _, interlace = struct.unpack('>IIBBBBB', chunk)
        elif typ == b'PLTE':
            plte = [tuple(chunk[i:i + 3]) for i in range(0, len(chunk), 3)]
        elif typ == b'tRNS':
            trns = chunk
        elif typ == b'IDAT':
            idat += chunk
        elif typ == b'IEND':
            break
    if depth != 8 or interlace:
        raise Die('This PNG uses a bit depth or interlacing the built-in reader does not support. '
                  'Re-save it as a standard 8-bit PNG, or install Pillow (pip install pillow).')
    bpp = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ctype]
    raw = zlib.decompress(idat)
    stride = w * bpp
    prev = bytearray(stride)
    rows, i = [], 0
    for _ in range(h):
        f = raw[i]
        line = bytearray(raw[i + 1:i + 1 + stride])
        i += 1 + stride
        for x in range(stride):
            a = line[x - bpp] if x >= bpp else 0
            b = prev[x]
            c = prev[x - bpp] if x >= bpp else 0
            if f == 1:
                line[x] = (line[x] + a) & 255
            elif f == 2:
                line[x] = (line[x] + b) & 255
            elif f == 3:
                line[x] = (line[x] + (a + b) // 2) & 255
            elif f == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        rows.append(bytes(line))
        prev = line
    px = []
    for line in rows:
        for x in range(0, stride, bpp):
            v = line[x:x + bpp]
            if ctype == 0:
                px.append((v[0], v[0], v[0], 255))
            elif ctype == 2:
                px.append((v[0], v[1], v[2], 255))
            elif ctype == 3:
                alpha = trns[v[0]] if trns and v[0] < len(trns) else 255
                px.append(plte[v[0]] + (alpha,))
            elif ctype == 4:
                px.append((v[0], v[0], v[0], v[1]))
            else:
                px.append(tuple(v))
    return px


def read_pixels(path, max_px=200_000):
    path = pathlib.Path(path)
    if not path.exists():
        raise Die(f'Reference image not found: {path}')
    try:
        from PIL import Image  # optional
        im = Image.open(path).convert('RGBA')
        im.thumbnail((400, 400))
        return list(im.getdata())
    except ImportError:
        pass
    px = _png_pixels(path.read_bytes())
    if px is None:
        sips = shutil.which('sips')
        if not sips:
            raise Die(f'{path.name} is not a PNG and neither Pillow nor macOS sips is available. '
                      'Convert it to PNG, or install Pillow (pip install pillow).')
        with tempfile.TemporaryDirectory() as td:
            out = pathlib.Path(td) / 'ref.png'
            r = subprocess.run([sips, '-s', 'format', 'png', '-Z', '400', str(path), '--out', str(out)], capture_output=True)
            if r.returncode or not out.exists():
                raise Die(f'Could not convert {path.name} to PNG with sips: {r.stderr.decode(errors="replace").strip()}')
            px = _png_pixels(out.read_bytes())
    step = max(1, len(px) // max_px)
    return px[::step]


# ---------- palette extraction ----------

def palette(path, n=8):
    """The image's main colours, most common first: [(rgb, share)]."""
    buckets = {}
    total = 0
    for r, g, b, a in read_pixels(path):
        if a < 128:
            continue
        k = (r >> 4, g >> 4, b >> 4)
        e = buckets.setdefault(k, [0, 0, 0, 0])
        e[0] += 1; e[1] += r; e[2] += g; e[3] += b
        total += 1
    if not total:
        raise Die('The reference image has no opaque pixels.')
    cols = sorted(((e[0], (e[1] / e[0], e[2] / e[0], e[3] / e[0])) for e in buckets.values()), reverse=True)
    picked = []
    for cnt, c in cols:
        for p in picked:
            if sum((x - y) ** 2 for x, y in zip(c, p[0])) < 48 ** 2:
                p[1] += cnt
                break
        else:
            picked.append([c, cnt])
    picked.sort(key=lambda p: -p[1])
    return [(tuple(c), cnt / total) for c, cnt in picked[:n]]


def pick_accents(pal):
    """Up to three vivid, mutually distinct hues, by (share x saturation)."""
    cands = []
    for c, share in pal:
        h, l, s = hls(c)
        if s >= 0.25 and 0.2 <= l <= 0.85:
            cands.append((share ** 0.5 * s, c, h))
    cands.sort(key=lambda t: -t[0])
    out = []
    for _, c, h in cands:
        if all(hue_dist(h, hls(o)[0]) > 0.04 for o in out):
            out.append(c)
        if len(out) == 3:
            break
    return out


# ---------- theme derivation ----------

def derive(given=None, mode=None, pal=None):
    """Fill every missing token. `given` = user/manual values (hex strings), which always win."""
    given = {k: v for k, v in (given or {}).items() if v}
    acc = [rgb(given[k]) if k in given else None for k in ('a1', 'a2', 'a3')]
    found = pick_accents(pal) if pal else []
    for i in range(3):
        if acc[i] is None and found:
            c = found.pop(0)
            while found and any(x is not None and hue_dist(hls(c)[0], hls(x)[0]) < 0.04 for x in acc):
                c = found.pop(0)
            acc[i] = c
    if acc[0] is None:
        acc[0] = rgb('#2dd4bf')
    if not mode:
        if 'bg' in given:
            mode = 'light' if luminance(rgb(given['bg'])) > 0.4 else 'dark'
        elif pal:
            mode = 'light' if luminance(pal[0][0]) > 0.5 else 'dark'
        else:
            mode = 'dark'
    h1, l1, s1 = hls(acc[0])
    for i in (1, 2):  # fill gaps with a hue rotated away from the accents we have
        if acc[i] is None:
            have = [hls(c)[0] for c in acc if c is not None]
            def score(rot):
                h = (h1 + rot) % 1
                muddy = 0.1 if mode == 'light' and 0.1 < h < 0.24 else 0  # yellows go olive when darkened
                return min(0.15, min(hue_dist(h, x) for x in have)) - muddy
            rot = max((0.2, -0.2, 0.12, -0.12, -0.35, 0.35, 0.5), key=score)
            acc[i] = from_hls(h1 + rot, l1, max(s1, 0.5))
    # neutrals take the image's dominant hue when it is a background-like colour, else a1's
    base = pal[0][0] if pal and hls(pal[0][0])[2] < 0.9 else acc[0]
    ha, hb = hls(base)[0], hls(acc[1])[0]
    sat = min(0.30, hls(base)[2]) if base is not acc[0] else 0.30
    if mode == 'dark':
        t = dict(bg=from_hls(ha, 0.075, sat), bg2=from_hls(ha, 0.09, 0.55), bg3=from_hls(hb, 0.09, 0.45),
                 card=from_hls(ha, 0.09, 0.22), border=from_hls(ha, 0.18, 0.20),
                 text=from_hls(ha, 0.95, 0.25), muted=from_hls(ha, 0.70, 0.12))
    else:
        t = dict(bg=from_hls(ha, 0.975, sat), bg2=from_hls(ha, 0.94, 0.55), bg3=from_hls(hb, 0.94, 0.45),
                 card=from_hls(ha, 0.995, 0.30), border=from_hls(ha, 0.85, 0.18),
                 text=from_hls(ha, 0.10, 0.30), muted=from_hls(ha, 0.36, 0.12))
    if pal:  # an image whose main colour already suits the mode is the page background as-is
        c = pal[0][0]; l = hls(c)[1]
        if (mode == 'dark' and l < 0.16) or (mode == 'light' and l > 0.9):
            t['bg'] = c
    for k in list(t):
        if k in given:
            t[k] = rgb(given[k])
    bg = t['bg']
    # accents carry eyebrows, links and borders: keep them readable on the page
    for i, k in enumerate(('a1', 'a2', 'a3')):
        if k not in given:
            acc[i] = readable(acc[i], bg, 4.5 if i == 0 else 3.0)
    t.update(a1=acc[0], a2=acc[1], a3=acc[2])
    out = {k: to_hex(t[k]) for k in COLOR_KEYS}
    out['mode'] = mode
    out['on_accent'] = given.get('on_accent') or ('#05060a' if (luminance(acc[0]) + luminance(acc[1])) / 2 > 0.18 else '#ffffff')
    for k in ('font_head', 'font_body'):
        if k in given:
            out[k] = given[k]
    return out


def contrast_report(theme):
    """Warnings for pairs that will be hard to read."""
    bg = rgb(theme['bg']); card = rgb(theme['card'])
    checks = [('text', bg, 4.5, 'page'), ('text', card, 4.5, 'card'), ('muted', bg, 3.0, 'page'),
              ('muted', card, 3.0, 'card'), ('a1', bg, 3.0, 'page')]
    out = []
    for k, against, need, where in checks:
        r = contrast(rgb(theme[k]), against)
        if r < need:
            out.append(f'theme.{k} on the {where} background: contrast {r:.1f}:1, aim for at least {need}:1')
    return out


def swatches(theme, pal=None):
    def sw(h):
        r, g, b = rgb(h)
        return f'\x1b[48;2;{r};{g};{b}m    \x1b[0m'
    lines = []
    if pal:
        lines.append('Reference palette: ' + ' '.join(f'{sw(to_hex(c))} {to_hex(c)} {s:.0%}' for c, s in pal))
    lines.append(f'Theme ({theme["mode"]}):')
    lines += [f'  {sw(theme[k])} {k:<7} {theme[k]}' for k in COLOR_KEYS]
    return '\n'.join(lines)
