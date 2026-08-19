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

To change the planting, edit `genurn.py`, run the command above, and paste the
result over the existing `urnJar` … `</symbol>` block in
`karim-nardine-invitation.html`.
