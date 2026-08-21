"""Assemble the jar-and-bloom symbol from the generated foliage.

Every pigment and every opacity is a custom property with the quiet
corner-mark value as its fallback, so one symbol serves both jobs: the page's
corner marks take the defaults, and the cover's hero overrides them with
stronger paint. Custom properties inherit into the shadow tree a <use>
instantiates, so nothing has to be drawn twice.
"""
import re, subprocess, sys

frag = subprocess.run([sys.executable, 'genurn.py'], capture_output=True, text=True, check=True).stdout


def section(name):
    m = re.search(r'<!-- %s: \d+ -->\n(.*?)\n\n' % name, frag, re.S)
    return m.group(1).rstrip()


MASS, BSTEM, BLEAF, BBUD, FSTEM, FLEAF, FBUD, DSTEM, DLEAF, DBUD = (section(n) for n in
    ('mass', 'backstem', 'backleaf', 'backbud',
     'frontstem', 'frontleaf', 'frontbud',
     'drapestem', 'drapeleaf', 'drapebud'))

# a wide-bellied garden jar: broad mouth, shoulder just under the rim, tapering
# to a modest foot — the jars the reference photograph is full of
JAR = ('M 102 252 C 98 268, 82 288, 80 312 C 78 342, 90 372, 108 388 L 192 388 '
       'C 210 372, 222 342, 220 312 C 218 288, 202 268, 198 252 Z')
LIP = ('M 97 250 C 120 259, 180 259, 203 250 C 203 241, 184 237, 150 237 '
       'C 116 237, 97 241, 97 250 Z')


def f(prop, token, fallback):
    return f'{prop}:var(--u-{token},{fallback})'


SYMBOL = f'''    <path id="urnJar" d="{JAR}"/>
    <path id="urnLip" d="{LIP}"/>
    <g id="urnGeo"><use href="#urnJar"/><use href="#urnLip"/></g>
    <!-- a clipPath's children must be shapes: a use of a group clips to nothing -->
    <clipPath id="urnGeoClip"><use href="#urnJar"/><use href="#urnLip"/></clipPath>

    <!-- ══ the bloom, drawn once ══ Two vessels carry it — the jar in the
         page's corners and the mended vessel on the cover — so it lives out
         here as four groups they both point at, placed by transforms. The
         filters go on the <use>, not in here, or they would run twice. -->
    <g id="bloomMass" style="{f('fill', 'mass', '#7C8757')};{f('opacity', 'mass-o', '.1')}">
{MASS}
    </g>
    <!-- the far half of the plant: thinner stems, smaller leaves, deeper green -->
    <g id="bloomUnder">
      <g fill="none" stroke-width="1.5" stroke-linecap="round"
         style="{f('stroke', 'stem', '#5C6940')};{f('opacity', 'stem-o', '.4')}">
{BSTEM}
      </g>
      <g style="{f('fill', 'leafd', '#4F5C36')};{f('opacity', 'leafd-o', '.42')}">
{BLEAF}
      </g>
      <g style="{f('fill', 'budd', '#C4661B')};{f('opacity', 'budd-o', '.44')}">
{BBUD}
      </g>
    </g>
    <!-- and the near half over it -->
    <g id="bloomOver">
      <g fill="none" stroke-width="2" stroke-linecap="round"
         style="{f('stroke', 'stem2', '#6B784B')};{f('opacity', 'stem2-o', '.44')}">
{FSTEM}
      </g>
      <g style="{f('fill', 'leafl', '#77855A')};{f('opacity', 'leafl-o', '.46')}">
{FLEAF}
      </g>
      <g style="{f('fill', 'bud', '#DC7C2A')};{f('opacity', 'bud-o', '.6')}">
{FBUD}
      </g>
    </g>
    <g id="bloomDrape">
      <g fill="none" stroke-width="1.8" stroke-linecap="round"
         style="{f('stroke', 'stem', '#5F6C42')};{f('opacity', 'spill-o', '.4')}">
{DSTEM}
      </g>
      <g style="{f('fill', 'leafd', '#5F6C42')};{f('opacity', 'spill-o', '.42')}">
{DLEAF}
      </g>
      <g style="{f('fill', 'bud', '#D97A2B')};{f('opacity', 'spill-bud-o', '.54')}">
{DBUD}
      </g>
    </g>

    <!-- ══ the jar, for the page's corners ══ -->
    <symbol id="urnMark" viewBox="0 0 300 400">
      <use href="#bloomMass"  filter="url(#wcWet)"/>
      <use href="#bloomUnder" filter="url(#wcC)"/>
      <use href="#bloomOver"  filter="url(#wcB)"/>
      <!-- two thin washes that do not quite agree, so the paper is never
           fully covered and the terracotta keeps moving -->
      <use href="#urnGeo" filter="url(#wcA)"
           style="{f('fill', 'clay1', '#D9A472')};{f('opacity', 'clay1-o', '.46')}"/>
      <use href="#urnGeo" filter="url(#wcB)" transform="translate(3.5,-2.5)"
           style="{f('fill', 'clay2', '#C0854E')};{f('opacity', 'clay2-o', '.3')}"/>
      <g clip-path="url(#urnGeoClip)">
        <ellipse cx="206" cy="322" rx="40" ry="86" filter="url(#wcB)"
                 style="{f('fill', 'shade', '#96602F')};{f('opacity', 'shade-o', '.26')}"/>
        <ellipse cx="150" cy="384" rx="62" ry="20" filter="url(#wcC)"
                 style="{f('fill', 'foot', '#845228')};{f('opacity', 'foot-o', '.2')}"/>
        <ellipse cx="118" cy="300" rx="24" ry="42" filter="url(#wcB)"
                 style="{f('fill', 'lite', '#F2DCC2')};{f('opacity', 'lite-o', '.32')}"/>
        <path d="M 96 300 C 122 290, 156 306, 184 296 C 192 322, 176 350, 146 354 C 114 358, 92 332, 96 300 Z"
              filter="url(#wcB)"
              style="{f('fill', 'back', '#EED7BC')};{f('opacity', 'back-o', '.24')}"/>
        <use href="#urnGeo" fill="none" stroke-width="7" filter="url(#wcPool)"
             style="{f('stroke', 'pool', '#8E5A2C')};{f('opacity', 'pool-o', '.42')}"/>
        <rect x="70" y="230" width="160" height="170" filter="url(#wcGrain)"
              style="{f('opacity', 'grain-o', '.15')}"/>
        <g fill="none" stroke-width="2.2" filter="url(#wcC)"
           style="{f('stroke', 'ring', '#8E5A2C')};{f('opacity', 'ring-o', '.2')}">
          <path d="M 84 300 C 118 312, 182 312, 216 299"/>
          <path d="M 88 340 C 120 352, 180 352, 212 339"/>
        </g>
      </g>
      <use href="#urnGeo" fill="none" stroke-width="1.5" filter="url(#wcB)"
           style="{f('stroke', 'line', '#7E4F26')};{f('opacity', 'line-o', '.42')}"/>
      <use href="#bloomDrape" filter="url(#wcC)"/>
    </symbol>

    <!-- ══ the mended vessel with the bloom in it, for the cover ══
         The same flowers, lifted to a taller and narrower mouth, and the
         drape squeezed in to hang from a rim a third of the jar's width. -->
    <symbol id="vesselBloom" viewBox="0 0 300 400">
      <g transform="translate(0,-62)">
        <use href="#bloomMass"  filter="url(#wcWet)"/>
        <use href="#bloomUnder" filter="url(#wcC)"/>
        <use href="#bloomOver"  filter="url(#wcB)"/>
      </g>
      <g transform="translate(33,146) scale(.78)">
        <use href="#vesselBody" filter="url(#wcA)"
             style="{f('fill', 'vclay1', '#EADFCA')};{f('opacity', 'vclay1-o', '.46')}"/>
        <use href="#vesselBody" filter="url(#wcB)" transform="translate(2.5,-2)"
             style="{f('fill', 'vclay2', '#DCC9AC')};{f('opacity', 'vclay2-o', '.26')}"/>
        <g clip-path="url(#vesselGeoClip)">
          <ellipse cx="198" cy="230" rx="36" ry="94" filter="url(#wcB)"
                   style="{f('fill', 'vshade', '#C3AE8F')};{f('opacity', 'vshade-o', '.2')}"/>
          <ellipse cx="120" cy="186" rx="21" ry="42" filter="url(#wcB)"
                   style="{f('fill', 'vlite', '#FCF8F1')};{f('opacity', 'vlite-o', '.36')}"/>
          <path d="M 100 196 C 124 186, 158 202, 186 192 C 194 218, 178 248, 148 252 C 116 256, 96 228, 100 196 Z"
                filter="url(#wcB)"
                style="{f('fill', 'vback', '#FBF6EC')};{f('opacity', 'vback-o', '.28')}"/>
          <use href="#vesselBody" fill="none" stroke-width="6" filter="url(#wcPool)"
               style="{f('stroke', 'vpool', '#B3A183')};{f('opacity', 'vpool-o', '.4')}"/>
          <rect x="70" y="45" width="170" height="290" filter="url(#wcGrain)"
                style="{f('opacity', 'vgrain-o', '.13')}"/>
          <g fill="none" stroke-width="2" filter="url(#wcC)"
             style="{f('stroke', 'vring', '#AEA187')};{f('opacity', 'vring-o', '.24')}">
            <path d="M 94 156 C 128 166, 174 166, 208 155"/>
            <path d="M 88 196 C 126 208, 176 208, 214 195"/>
            <path d="M 95 246 C 130 258, 172 258, 207 245"/>
          </g>
          <!-- the gold, wet into wet: the bloom it made, then the line that dried in it -->
          <use href="#vesselJoins" filter="url(#wcWet)" stroke-width="8"
               style="{f('stroke', 'vglow', '#DCC07A')};{f('opacity', 'vglow-o', '.4')}"/>
          <use href="#vesselJoins" filter="url(#wcC)" stroke-width="2.2"
               style="{f('stroke', 'vgold', '#BE9838')};{f('opacity', 'vgold-o', '.7')}"/>
        </g>
        <path d="M 130 63 C 143 69, 159 69, 172 63" fill="none" stroke-width="1.4" filter="url(#wcC)"
              style="{f('stroke', 'vline', '#8E846E')};{f('opacity', 'vline-o', '.42')}"/>
        <use href="#vesselBody" fill="none" stroke-width="1.4" filter="url(#wcB)"
             style="{f('stroke', 'vline', '#8E846E')};{f('opacity', 'vline-o', '.42')}"/>
      </g>
      <g transform="translate(150,206) scale(.74,1.02) translate(-150,-248)">
        <use href="#bloomDrape" filter="url(#wcC)"/>
      </g>
    </symbol>
'''
sys.stdout.write(SYMBOL)
