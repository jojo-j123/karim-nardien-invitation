# tools

The urn's foliage is generated, not hand-placed. A couple of hundred leaves and
blossoms need to look scattered, and a hand placing them one at a time falls
into a rhythm you can see.

    python3 buildurn.py > urn.symbol

`genurn.py` grows a skeleton and hangs the plant off it: stems leave the mouth,
divide once or twice, carry their leaves in opposite pairs along their length,
and put a head of blossom at the tips. Leaves are leaf-shaped — rounded base,
pointed tip, laid along the stem they grow from — and the blossom is a
five-lobed rosette in a cluster, not a dot. Two passes, a darker smaller one
behind and a lighter larger one in front, give the mass a near and a far. The
seed is fixed, so the drawing comes out the same every run.
`buildurn.py` wraps that scatter in the watercolour layers and prints two
symbols: `#urnMark`, the terracotta jar the page's corners carry, and
`#vesselBloom`, the mended vessel in flower on the cover. The bloom itself is
emitted once, as four groups both symbols point at with `<use>` — the cover
lifts it to a taller mouth and squeezes the drape in with transforms, so the
second vessel costs a wrapper rather than another four hundred shapes.

Every pigment and every opacity in the symbol is a CSS custom property whose
fallback is the quiet corner-mark value, so one drawing does both jobs: the
page's corner marks take the defaults, and `.vase-wrap` on the cover overrides
them with stronger paint. Custom properties inherit into the shadow tree a
`<use>` instantiates, so nothing is drawn twice.

To change the planting, edit `genurn.py`, run the command above, and paste the
result over the existing `urnJar` … `</symbol>` block in
`karim-nardine-invitation.html`.

## Cache stamps

`vercel.json` serves images and audio as `immutable`, which is only honest if a
changed file means a changed URL. `tools/stamp.py` makes that true: it hashes
each served asset and rewrites its reference to `name.ext?v=<hash>`.

**Run it after touching any image or the audio, before committing** — otherwise
a guest who has already opened the invitation keeps the old file for a year and
reloading will not shift it.

    python3 tools/stamp.py

It leaves the Supabase-hosted copies of the track alone; those are not served by
this deployment and are not ours to stamp.

## The link-preview card

`og-card.jpg` is what WhatsApp and the rest show when the invitation is
shared. It is **not** `invitation-plate.png`: that file is only the painted
border, because the plate's words are HTML laid over the artwork, so sharing it
showed an empty card.

`tools/ogcard.py` composes the card at 1200x630 from `cover.png` alone — the
title lettering and the vessel, lifted as pixels, so nothing depends on a font
loading. Rerun it after changing the cover, then rerun `stamp.py`:

    python3 tools/ogcard.py && python3 tools/stamp.py
