"""Write a docker-compose.yml (+ nginx.conf) in the talk folder that mounts the built deck as a web server."""
import pathlib, shutil, time
from common import *
import deck as deck_mod

BASE_IMAGE = 'nginxinc/nginx-unprivileged:1.27-alpine'

NGINX_CONF = """server {
    listen 8080;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    gzip on;
    gzip_types text/css application/javascript image/svg+xml;

    add_header X-Content-Type-Options nosniff always;
    add_header Referrer-Policy strict-origin-when-cross-origin always;

    location = /healthz { access_log off; default_type text/plain; return 200 "ok\\n"; }

    location /fonts/ { expires 30d; add_header Cache-Control "public, immutable"; }
    location / {
        # index.html is rebuilt with every talk update: never serve a stale copy
        add_header Cache-Control "no-cache";
        try_files $uri $uri/ =404;
    }
}
"""

COMPOSE = """# Serves the built deck with nginx. The deck is mounted, not copied into an image:
# Edit the files in that folder (or rebuild them) and just reload the browser.
services:
  {name}:
    image: {base}
    container_name: {name}
    ports:
      - "${{PORT:-8080}}:8080"
    volumes:
      - ./{deck}:/usr/share/nginx/html:ro
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://127.0.0.1:8080/healthz"]
      interval: 30s
      timeout: 3s
"""


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', str(s).lower()).strip('-')[:40] or 'talk'


def find_deck(base, out_dir):
    """The deck folder that already exists (has index.html), most specific first. -> Path or None"""
    for d in (pathlib.Path(out_dir) / 'deck', base / 'build' / 'deck', base / 'deck', base):
        if (d / 'index.html').is_file():
            return d.resolve()
    return None


def package(cfg, out_dir, deck=None, rebuild=False, force=False):
    """Write docker-compose.yml + nginx.conf next to session.json, mounting the deck that is already there.
    The deck is only generated from session.json when none exists yet, or when rebuild=True (the old one
    is moved aside first, never overwritten). Returns (project_dir, written, skipped, deck_dir, note)."""
    base = cfg['_base']
    if deck:
        d = pathlib.Path(deck)
        d = (d if d.is_absolute() else pathlib.Path.cwd() / d).resolve()
        if not (d / 'index.html').is_file():
            raise Die(f'No index.html in {d}.')
        existing = d
    else:
        existing = find_deck(base, out_dir)
    note = ''
    if existing and not rebuild:
        deck_dir, note = existing, f'mounting your existing deck: {existing} (not rebuilt from session.json)'
    else:
        deck_dir = pathlib.Path(out_dir).resolve() / 'deck'
        if existing and rebuild:
            if existing == base:
                raise Die('--rebuild would replace the deck in the talk folder itself; point --out at another folder.')
            backup = existing.with_name(f'{existing.name}.bak-{time.strftime("%Y%m%d-%H%M%S")}')
            shutil.move(str(existing), str(backup))
            note = f'rebuilt from session.json; previous deck kept in {backup}'
        else:
            note = 'no deck found, built it from session.json'
        deck_mod.build(cfg, deck_dir)
    try:
        deck_rel = deck_dir.relative_to(base).as_posix() or '.'
    except ValueError:
        raise Die(f'The deck folder {deck_dir} must be inside the talk folder {base} so compose can mount it.')
    if deck_dir == base:
        note += '; the whole talk folder is served, including session.json (move the deck into build/deck to avoid that)'
    files = {'nginx.conf': NGINX_CONF,
             'docker-compose.yml': COMPOSE.format(name=slug(cfg['session'].get('title')), base=BASE_IMAGE, deck=deck_rel)}
    written, skipped = [], []
    for fn, text in files.items():
        p = base / fn
        if p.exists() and p.read_text(encoding='utf-8') != text and not force:
            skipped.append(fn)  # never overwrite the user's own edits silently
            continue
        p.write_text(text, encoding='utf-8')
        written.append(fn)
    return base, written, skipped, deck_dir, note
