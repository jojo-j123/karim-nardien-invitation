# tools

The urn's foliage is generated, not hand-placed. A couple of hundred leaves and
blossoms need to look scattered, and a hand placing them one at a time falls
into a rhythm you can see.

    python3 buildurn.py > urn.symbol

`genurn.py` samples the leaves, buds and stems against a lumpy boundary — the
same boundary that draws the underwash, so the wash and what grows in it share
one silhouette. The seed is fixed, so the drawing comes out the same every run.
`buildurn.py` wraps that scatter in the jar and the watercolour layers and
prints the finished `<symbol id="urnMark">`.

Every pigment and every opacity in the symbol is a CSS custom property whose
fallback is the quiet corner-mark value, so one drawing does both jobs: the
page's corner marks take the defaults, and `.vase-wrap` on the cover overrides
them with stronger paint. Custom properties inherit into the shadow tree a
`<use>` instantiates, so nothing is drawn twice.

To change the planting, edit `genurn.py`, run the command above, and paste the
result over the existing `urnJar` … `</symbol>` block in
`karim-nardine-invitation.html`.
