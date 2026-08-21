"""Grow the bloom the vessels carry.

The first version of this scattered ellipses and circles inside a blob, and it
read as confetti, because that is what it was. A plant is not a scatter. It has
a skeleton: stems leave the mouth, divide once or twice, carry their leaves in
opposite pairs along their length, and put their flowers at the ends. Leaves
are not ellipses — they have a rounded base and a point — and small blossom is
not a dot, it is a five-lobed rosette in a cluster of its own kind.

So this builds the skeleton first and hangs everything off it. Two passes: a
darker, smaller one behind, and a lighter, larger one in front, so the mass has
a near and a far. The seed is fixed, so the drawing is the same every run.
"""
import math, random

R = random.Random(20260919)
MOUTH = (150, 250)          # where every stem leaves the vessel
CX, CY, RX, RY = 148, 166, 94, 92   # the air the plant is allowed to fill


def jit(a):
    return R.uniform(-a, a)


def qpoint(p0, p1, p2, t):
    u = 1 - t
    return (u*u*p0[0] + 2*u*t*p1[0] + t*t*p2[0],
            u*u*p0[1] + 2*u*t*p1[1] + t*t*p2[1])


def qtangent(p0, p1, p2, t):
    u = 1 - t
    dx = 2*u*(p1[0]-p0[0]) + 2*t*(p2[0]-p1[0])
    dy = 2*u*(p1[1]-p0[1]) + 2*t*(p2[1]-p1[1])
    return math.degrees(math.atan2(dy, dx))


def leaf(x, y, ang, L, W):
    """a leaf: rounded at the base, pointed at the tip, drawn along its stem.
    Unit shape runs from (0,0) at the base to (0,-1) at the tip."""
    return (f'<path d="M0 0C{W:.1f} {-L*.22:.1f} {W*.62:.1f} {-L*.8:.1f} 0 {-L:.0f}'
            f'C{-W*.62:.1f} {-L*.8:.1f} {-W:.1f} {-L*.22:.1f} 0 0Z" '
            f'transform="translate({x:.0f} {y:.0f}) rotate({ang:.0f})"/>')


def floret(x, y, r, turn=0.0):
    """five round lobes around a small eye — what a spray of little flowers is.
    Each petal is a cubic that bulges out and comes back, so the lobe is plump
    rather than pointed; a pointed five-lobe is an asterisk, not a flower."""
    inner, out = r * .52, r * 1.16
    d = ''
    for k in range(5):
        a0 = math.radians(k * 72 - 90 + turn)
        a1 = math.radians((k + 1) * 72 - 90 + turn)
        m = (a0 + a1) / 2
        p0 = (x + inner*math.cos(a0), y + inner*math.sin(a0))
        p1 = (x + inner*math.cos(a1), y + inner*math.sin(a1))
        c0 = (x + out*math.cos(m - .40), y + out*math.sin(m - .40))
        c1 = (x + out*math.cos(m + .40), y + out*math.sin(m + .40))
        if not d:
            d = f'M{p0[0]:.1f} {p0[1]:.1f}'
        d += f'C{c0[0]:.1f} {c0[1]:.1f} {c1[0]:.1f} {c1[1]:.1f} {p1[0]:.1f} {p1[1]:.1f}'
    return f'<path d="{d}Z"/>'


def cluster(x, y, n, spread, rmin, rmax, into):
    """blossom does not arrive one at a time; it arrives in a head"""
    for _ in range(n):
        a, rr = R.uniform(0, 6.283), R.uniform(0, 1) ** .6 * spread
        into.append(floret(x + math.cos(a)*rr, y + math.sin(a)*rr * .82,
                           R.uniform(rmin, rmax), R.uniform(0, 72)))


def limb(p0, p1, p2, stems, leaves, buds, *, leaf_len, depth, tip_head, head=(5, 10)):
    """draw one stem, hang its leaves along it in opposite pairs, and put a
       head of blossom at its end"""
    stems.append(f'<path d="M{p0[0]:.0f} {p0[1]:.0f}Q{p1[0]:.0f} {p1[1]:.0f} {p2[0]:.0f} {p2[1]:.0f}"/>')
    stations = R.randint(4, 6)
    for i in range(stations):
        t = .12 + (.86 - .12) * i / max(1, stations - 1)
        x, y = qpoint(p0, p1, p2, t)
        ang = qtangent(p0, p1, p2, t)
        taper = 1 - .45 * t                       # leaves shrink toward the tip
        for side in (-1, 1):                       # opposite pairs, as they grow
            L = leaf_len * taper * R.uniform(.8, 1.2)
            leaves.append(leaf(x + jit(1.5), y + jit(1.5),
                               ang + 90 + side * R.uniform(38, 62) + jit(8),
                               L, L * R.uniform(.30, .40)))
    if tip_head:
        cluster(p2[0], p2[1], R.randint(*head), 9 + depth * 3, 2.4, 4.4, buds)
    return p2


def grow(n_trunks, arc, reach, leaf_len, depth, stems, leaves, buds,
         origin=MOUTH, rise=1.0, head=(5, 10), flowering=1.0):
    for i in range(n_trunks):
        a = math.radians(arc[0] + (arc[1] - arc[0]) * (i + R.uniform(.15, .85)) / n_trunks)
        length = reach * R.uniform(.72, 1.0)
        tip = (origin[0] + math.cos(a) * length * .82,
               origin[1] + math.sin(a) * length * rise)
        # bow the stem so it leaves the mouth upright and opens out
        mid = ((origin[0] + tip[0]) / 2 + math.cos(a) * length * .18 + jit(6),
               (origin[1] + tip[1]) / 2 - length * .16 * rise + jit(6))
        limb(origin, mid, tip, stems, leaves, buds, head=head,
             leaf_len=leaf_len, depth=depth, tip_head=R.random() < flowering)
        for _ in range(R.randint(1, 3)):           # where it divides
            t = R.uniform(.42, .82)
            bx, by = qpoint(origin, mid, tip, t)
            ba = a + math.radians(R.uniform(-42, 42))
            blen = length * R.uniform(.3, .52)
            btip = (bx + math.cos(ba) * blen, by + math.sin(ba) * blen * rise)
            bmid = ((bx + btip[0]) / 2 + jit(5), (by + btip[1]) / 2 - blen * .2 * rise + jit(5))
            limb((bx, by), bmid, btip, stems, leaves, buds, head=head,
                 leaf_len=leaf_len * .82, depth=depth, tip_head=R.random() < flowering)


out = []

# ── the wash the whole plant sits in, lumpy so it is never a clean curve ──
def edge(t):
    return 1 + .17*math.sin(3*t + 1.1) + .11*math.sin(5*t + 2.3) + .06*math.sin(8*t - .4)

pts = []
for i in range(48):
    t = -math.pi * 2 * i / 48
    e = edge(t)
    pts.append((CX + math.cos(t)*RX*e, min(CY + math.sin(t)*RY*e, 272)))
d = f'M {pts[0][0]:.0f} {pts[0][1]:.0f}'
for i in range(1, len(pts), 2):
    d += f' Q {pts[i][0]:.0f} {pts[i][1]:.0f} {pts[(i+1) % len(pts)][0]:.0f} {pts[(i+1) % len(pts)][1]:.0f}'
out.append(('mass', []))

# ── the far half of the plant, then the near half over it ────────────────
for name, n, arc, reach, ln, depth in (('back',  8, (-166, -14), 128, 15, 0),
                                       ('front', 7, (-152, -28), 108, 18, 1)):
    stems, leaves, buds = [], [], []
    grow(n, arc, reach, ln, depth, stems, leaves, buds)
    out.append((name + 'stem', stems))
    out.append((name + 'leaf', leaves))
    out.append((name + 'bud', buds))

# ── and what hangs over the front of the vessel ──────────────────────────
stems, leaves, buds = [], [], []
grow(3, (34, 146), 66, 12, 1, stems, leaves, buds, origin=(150, 242), rise=1.0,
     head=(2, 5), flowering=.45)
out.append(('drapestem', stems))
out.append(('drapeleaf', leaves))
out.append(('drapebud', buds))

for name, items in out:
    print(f'<!-- {name}: {len(items)} -->')
    line = '        '
    for it in items:
        if len(line) + len(it) > 116:
            print(line); line = '        '
        line += it
    if line.strip():
        print(line)
    print()
