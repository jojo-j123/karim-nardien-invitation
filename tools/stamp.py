"""Stamp every served asset with a hash of its own contents.

vercel.json serves .webp/.png/.mp3 with `immutable`, which tells a browser not
merely that it may cache the file but that it need never ask about it again —
not even a conditional request. That is the right header only when a changed
file means a changed URL. It was not: the cover was being repainted under the
same name, so a guest who had opened the invitation once kept the old painting
for a year and no amount of reloading would shift it.

So every asset URL carries ?v=<hash of the file>. Change the file, the hash
changes, the URL changes, and the browser has no choice but to fetch it —
while `immutable` becomes true rather than a promise the file kept breaking.

Run this after touching any image or the audio, before committing.
"""
import hashlib, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ['karim-nardine-invitation.html']
ASSETS = ['cover.webp', 'invitation-plate.webp', 'og-card.jpg', 'music.mp3',
          'botanicals/bot-stems-left.webp', 'botanicals/bot-blush-left.webp',
          'botanicals/bot-stems-right.webp', 'botanicals/bot-leaves-right.webp']

# the track is also hosted on Supabase, and those URLs are not ours to stamp:
# only the copy served from this deployment goes through vercel.json's rule
SKIP_PREFIX = '/storage/v1/object/public/'

stamps = {}
for a in ASSETS:
    f = ROOT / a
    if not f.exists():
        sys.exit(f'missing asset: {a}')
    stamps[a] = hashlib.sha256(f.read_bytes()).hexdigest()[:10]

changed = False
for page in PAGES:
    p = ROOT / page
    s = before = p.read_text()
    for a, h in stamps.items():
        # the reference with whatever stamp it already carries, or none —
        # skipping any that is part of a URL served by somebody else
        def sub(m):
            # look back only as far as the quote that opens this reference, so
            # a Supabase URL on the line above cannot be mistaken for this one
            txt = m.string
            start = max(txt.rfind(c, 0, m.start()) for c in '"\'()')
            if SKIP_PREFIX in txt[start:m.start()]:
                return m.group(0).split('?')[0]
            return a + '?v=' + h
        s = re.sub(re.escape(a) + r'(\?v=[0-9a-f]+)?', sub, s)
    if s != before:
        p.write_text(s); changed = True
    for a, h in stamps.items():
        n = s.count(a + '?v=' + h)
        print(f'  {a:<38} v={h}  {n} reference{"" if n == 1 else "s"} in {page}')
print('\n' + ('rewritten' if changed else 'already up to date'))
