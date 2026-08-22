"""Turn the cover painting's orange blossom white, and leave everything else.

Only the blossom moves. The mask is three conditions at once: a warm hue, real
saturation, and the vertical band the flowers occupy — because the gold in the
vessel's joins and the clay of TAP TO OPEN are the same hue as the flowers and
must not be touched. Every edge of the mask is feathered, or the recolour
leaves a visible cut.

White blossom on cream paper cannot simply be desaturated: it would sink into
the background, since the paper is already RGB(253,245,234). So the petals are
remapped onto a white range with their shading kept — the darks lift to a warm
grey and the lights go to near-white — and a trace of warmth is left in the
shadows so the mass still reads as painted rather than erased.
"""
from PIL import Image, ImageFilter
import numpy as np, sys

src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGB')
hsv = np.asarray(im.convert('HSV')).astype(np.float32)
H, S, V = hsv[..., 0].copy(), hsv[..., 1].copy(), hsv[..., 2].copy()
h, w = H.shape

def smooth(x, a, b):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)

yy = np.arange(h, dtype=np.float32)[:, None] * np.ones((1, w), np.float32)
# the flowers' band, soft at both ends so nothing cuts
band = smooth(yy, 575, 615) * (1 - smooth(yy, 1245, 1300))
# the blossom's hue and not the foliage's. The two are cleanly apart in this
# painting: the flowers sit at hue 22-33 degrees and are light, the olive
# leaves at 50-61 degrees and are dark. A wide window takes the leaves with it.
hue = smooth(H, 4, 11) * (1 - smooth(H, 27, 35))
# enough colour to be blossom rather than paper
sat = smooth(S, 34, 62)
# and not the deep shadow under the foliage, which is dark whatever its hue
lit = 0.25 + 0.75 * smooth(V, 95, 145)
a = band * hue * sat * lit
a = np.asarray(Image.fromarray((a * 255).astype(np.uint8)).filter(
    ImageFilter.GaussianBlur(1.2))).astype(np.float32) / 255.0

# petals: keep the modelling, move the range to white
lo, hi = 80.0, 250.0
t = np.clip((V - lo) / (hi - lo), 0, 1)
Vw = 197 + t * 58                      # 197 in the deepest shadow, 255 at the top
Sw = (1 - t) * 20                      # warmth only where it is dark
Hw = np.full_like(H, 26.0)             # a warm grey, not a colour

H2 = H * (1 - a) + Hw * a
S2 = S * (1 - a) + Sw * a
V2 = V * (1 - a) + Vw * a

out = Image.fromarray(np.stack([H2, S2, V2], -1).clip(0, 255).astype(np.uint8),
                      'HSV').convert('RGB')
out.save(dst)
print('wrote', dst, out.size, 'mask touched %.1f%% of pixels' % (100 * (a > .02).mean()))
