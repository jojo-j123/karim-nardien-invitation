"""Build the link-preview card.

The og:image was invitation-plate.png — the painted border of the invitation
with nothing on it, because the plate's words are HTML laid over the artwork
rather than baked into it. Shared on WhatsApp that reads as an empty card.

This composes a proper landscape card at the 1.91:1 the scrapers want, out of
the cover painting and nothing else: its own title lettering on the left, its
vessel on the right, on its own paper. No type is set here — the words are
lifted from the painting as pixels — so nothing depends on a font loading.
"""
from PIL import Image, ImageFilter
import numpy as np

W, H = 1200, 630
cover = Image.open('cover.png').convert('RGB')

# the bands, measured off the painting: the two title lines, the little rule,
# and the bouquet with its vessel. TAP TO OPEN is left out — it is an
# instruction for the page, not something to say in a preview.
TITLE = (140, 148, 600, 368)      # both lines and the rule beneath them
VESSEL = (0, 480, 730, 1492)

# ── the ground: the painting's own paper, its tone taken down its height ──
edge = np.asarray(cover).astype(np.float32)
stops = []
for i in range(9):
    y = int(i / 8 * (cover.height - 1))
    band = np.concatenate([edge[y:y+6, :12].reshape(-1, 3),
                           edge[y:y+6, -12:].reshape(-1, 3)]).mean(0)
    stops.append(band)
grad = np.zeros((H, W, 3), np.float32)
for y in range(H):
    t = y / (H - 1) * 8
    i = min(int(t), 7)
    f = t - i
    grad[y] = stops[i] * (1 - f) + stops[i + 1] * f
card = Image.fromarray(grad.round().astype(np.uint8))

# and the paper's own grain over it, so the ground is not a flat sweep
patch = cover.crop((0, 0, 730, 150)).resize((W, H), Image.LANCZOS).filter(
    ImageFilter.GaussianBlur(6))
card = Image.blend(card, patch, .35)


def place(box, height, cx, bottom):
    """Drop one piece of the painting on the card with its paper divided out.

    A piece pasted straight leaves a rectangle, because the card's ground and
    the painting's paper are a shade apart. Multiplying leaves one too. What a
    watercolour actually does to the sheet under it is scale it — so divide the
    piece by its own paper to get that scaling, then apply it to the ground.
    Where the piece is bare paper the ratio is 1 and nothing happens at all;
    where it is wash, the ground darkens by exactly as much as the paper did.
    The paper is measured per row, because the sheet is not one flat tone.
    """
    piece = cover.crop(box)
    w = round(piece.width * height / piece.height)
    piece = piece.resize((w, height), Image.LANCZOS)
    arr = np.asarray(piece, np.float32)

    # The paper is measured off the blank strips down either side, but a row
    # where the blossom reaches the edge poisons its own sample, and because
    # the blossom is whiter than the paper that shows up as a bright streak
    # clean across the card. So the profile is only a starting point: a median
    # rejects the poisoned rows, and a quadratic through what is left gives the
    # sheet's actual gradient, which no single row can then pull off course.
    e = max(3, w // 60)
    prof = np.concatenate([arr[:, :e], arr[:, -e:]], 1).mean(1)
    k = max(3, (height // 12) | 1)
    pad = np.pad(prof, ((k // 2, k // 2), (0, 0)), mode='edge')
    med = np.stack([np.median(pad[i:i + k], 0) for i in range(height)])
    yy = np.arange(height, dtype=np.float32)
    rowpaper = np.stack([np.polyval(np.polyfit(yy, med[:, c], 2), yy)
                         for c in range(3)], 1)[:, None, :]
    ratio = np.clip(arr / np.maximum(rowpaper, 1.0), 0, 1.10)

    x, y = round(cx - w / 2), round(bottom - height)
    under = np.asarray(card.crop((x, y, x + w, y + height)), np.float32)
    card.paste(Image.fromarray((under * ratio).clip(0, 255).astype(np.uint8)), (x, y))


place(VESSEL, 556, 872, 612)
place(TITLE, 176, 390, 348)

card.save('og-card.png')
card.save('og-card.jpg', quality=90, optimize=True, progressive=True)
print('og-card %dx%d  png %d KB  jpg %d KB' % (
    W, H, len(open('og-card.png','rb').read()) // 1024,
    len(open('og-card.jpg','rb').read()) // 1024))
