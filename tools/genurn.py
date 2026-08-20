"""Grow the bloom that sits in the jar.

Placed by a seeded sampler rather than by hand: a couple of hundred leaves and
blossoms need to look scattered, and a person placing them one at a time ends
up with a rhythm. The seed is fixed, so the drawing is the same every time.

The mass is not an ellipse. Its radius wobbles with the angle, and the same
wobble draws the underwash and bounds the scatter, so the wash and what grows
in it share one silhouette.
"""
import math, random

R = random.Random(20260919)
CX, CY, RX, RY = 148, 166, 94, 92


def edge(t):
    """how far out the mass reaches at this angle: lumpy, never a clean curve"""
    return 1 + .17 * math.sin(3 * t + 1.1) + .11 * math.sin(5 * t + 2.3) + .06 * math.sin(8 * t - .4)


def at(t, r):
    e = edge(t)
    return CX + math.cos(t) * RX * r * e, CY + math.sin(t) * RY * r * e


def jit(a):
    return R.uniform(-a, a)


# the foot of the plant: everything grows from the mouth of the jar
MOUTH_Y = 250
out = []

# ── the mass itself, as one closed shape for the wash to fill ────────────
pts = []
for i in range(48):
    t = -math.pi * 2 * i / 48
    x, y = at(t, 1.0)
    pts.append((x, min(y, 272)))
d = f'M {pts[0][0]:.0f} {pts[0][1]:.0f}'
for i in range(1, len(pts), 2):
    cx_, cy_ = pts[i]
    ex, ey = pts[(i + 1) % len(pts)]
    d += f' Q {cx_:.0f} {cy_:.0f} {ex:.0f} {ey:.0f}'
d += ' Z'
out.append(('mass', [f'<path d="{d}"/>']))

# ── stems: mostly buried, a few reaching past the leaves ────────────────
stems = []
for i in range(16):
    t = math.radians(R.uniform(-188, 8))
    r = R.uniform(.30, .60)
    ex, ey = at(t, r)
    sx, sy = 150 + jit(13), MOUTH_Y + jit(5)
    mx = (sx + ex) / 2 + math.cos(t) * 24 + jit(9)
    my = (sy + ey) / 2 + jit(13)
    stems.append(f'<path d="M {sx:.0f} {sy:.0f} Q {mx:.0f} {my:.0f} {ex:.0f} {ey:.0f}"/>')
out.append(('stems', stems))

# ── leaves: two passes, a darker one under a lighter one, so the mass has
#    depth rather than being one flat green ────────────────────────────────
def leaf_pass(n, lo, hi, smin, smax):
    got = []
    for _ in range(n):
        t = math.radians(R.uniform(-200, 20))
        r = math.sqrt(R.uniform(lo, hi))
        x, y = at(t, r)
        x += jit(4); y += jit(4)
        if y > 272:
            continue
        ang = math.degrees(t) + jit(44)
        rx = R.uniform(smin, smax)
        ry = rx * R.uniform(.30, .48)
        got.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx:.1f}" ry="{ry:.1f}" '
                   f'transform="rotate({ang:.0f} {x:.0f} {y:.0f})"/>')
    return got

out.append(('leavesdark', leaf_pass(140, .02, .86, 4.2, 9.0)))
out.append(('leaveslight', leaf_pass(125, .16, 1.04, 3.4, 7.6)))

# a skirt of leaves gathered where the plant leaves the mouth of the jar, so
# there is no bare stalk between the two
skirt = []
for _ in range(64):
    a = math.radians(R.uniform(-172, -8))
    rr = R.uniform(.18, .95)
    x = 150 + math.cos(a) * 74 * rr + jit(6)
    y = 236 - math.sin(a) * 44 * rr + jit(7)
    if y > 268 or y < 176:
        continue
    ang = R.uniform(-70, 70)
    rx = R.uniform(4.0, 8.0)
    skirt.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx:.1f}" ry="{rx * R.uniform(.30, .46):.1f}" '
                 f'transform="rotate({ang:.0f} {x:.0f} {y:.0f})"/>')
out.append(('skirt', skirt))

# ── the drape: what falls over the front of the jar, painted after it ────
drape_l, drape_b = [], []
for _ in range(52):
    a = math.radians(R.uniform(-168, -12))
    rr = R.uniform(.62, 1.06)
    x = 150 + math.cos(a) * 80 * rr + jit(7)
    y = 248 + (1 - math.sin(a)) * 30 * rr + jit(8)
    if y < 236 or y > 302:
        continue
    ang = R.uniform(-80, 80)
    rx = R.uniform(3.8, 7.6)
    drape_l.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx:.1f}" ry="{rx * R.uniform(.30, .46):.1f}" '
                   f'transform="rotate({ang:.0f} {x:.0f} {y:.0f})"/>')
    if R.random() < .5:
        drape_b.append(f'<circle cx="{x + jit(5):.0f}" cy="{y + jit(6):.0f}" r="{R.uniform(2.2, 4.4):.1f}"/>')
out.append(('drapeleaf', drape_l))
out.append(('drapebud', drape_b))

# ── blossom: through the whole mass, gathering toward the outside ────────
buds, hearts = [], []
for _ in range(180):
    t = math.radians(R.uniform(-204, 24))
    r = R.uniform(.20, 1.04) ** .55
    x, y = at(t, r)
    x += jit(3.5); y += jit(3.5)
    if y > 274:
        continue
    rad = R.uniform(1.9, 4.6)
    buds.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rad:.1f}"/>')
    if rad > 3.4 and R.random() < .55:
        hearts.append(f'<circle cx="{x + jit(1.1):.0f}" cy="{y + jit(1.1):.0f}" r="{rad * .45:.1f}"/>')
out.append(('buds', buds))
out.append(('hearts', hearts))

for name, items in out:
    print(f'<!-- {name}: {len(items)} -->')
    line = '        '
    for it in items:
        if len(line) + len(it) > 112:
            print(line); line = '        '
        line += it
    if line.strip():
        print(line)
    print()
