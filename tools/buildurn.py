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


MASS, STEMS, LDARK, LLIGHT, SKIRT, DLEAF, DBUD, BUDS, HEARTS = (section(n) for n in
    ('mass', 'stems', 'leavesdark', 'leaveslight', 'skirt',
     'drapeleaf', 'drapebud', 'buds', 'hearts'))

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
    <symbol id="urnMark" viewBox="0 0 300 400">
      <!-- ── the bloom, painted before the jar so its stems run behind the rim ── -->
      <!-- the mass, laid in wet as one shape before anything is drawn in it -->
      <g style="{f('fill', 'mass', '#7C8757')};{f('opacity', 'mass-o', '.1')}" filter="url(#wcWet)">
{MASS}
      </g>
      <!-- what lies under: the stems (mostly buried), the darker leaves, and the
           skirt of foliage where the plant leaves the mouth of the jar -->
      <g filter="url(#wcC)">
        <g fill="none" stroke-width="1.7" stroke-linecap="round"
           style="{f('stroke', 'stem', '#5C6940')};{f('opacity', 'stem-o', '.26')}">
{STEMS}
        </g>
        <g style="{f('fill', 'leafd', '#4F5C36')};{f('opacity', 'leafd-o', '.34')}">
{LDARK}
        </g>
        <g style="{f('fill', 'skirt', '#5C6940')};{f('opacity', 'skirt-o', '.34')}">
{SKIRT}
        </g>
      </g>
      <!-- and what lies over: the lit leaves and the blossom -->
      <g filter="url(#wcB)">
        <g style="{f('fill', 'leafl', '#77855A')};{f('opacity', 'leafl-o', '.38')}">
{LLIGHT}
        </g>
        <g style="{f('fill', 'bud', '#DC7C2A')};{f('opacity', 'bud-o', '.52')}">
{BUDS}
        </g>
        <g style="{f('fill', 'heart', '#AE4C0C')};{f('opacity', 'heart-o', '.4')}">
{HEARTS}
        </g>
      </g>

      <!-- ── the jar: two thin washes that do not quite agree, so the paper is
             never fully covered and the terracotta keeps moving ── -->
      <use href="#urnGeo" filter="url(#wcA)"
           style="{f('fill', 'clay1', '#D9A472')};{f('opacity', 'clay1-o', '.46')}"/>
      <use href="#urnGeo" filter="url(#wcB)" transform="translate(3.5,-2.5)"
           style="{f('fill', 'clay2', '#C0854E')};{f('opacity', 'clay2-o', '.3')}"/>
      <g clip-path="url(#urnGeoClip)">
        <!-- the shaded side, and the light the left of it keeps -->
        <ellipse cx="206" cy="322" rx="40" ry="86" filter="url(#wcB)"
                 style="{f('fill', 'shade', '#96602F')};{f('opacity', 'shade-o', '.26')}"/>
        <ellipse cx="150" cy="384" rx="62" ry="20" filter="url(#wcC)"
                 style="{f('fill', 'foot', '#845228')};{f('opacity', 'foot-o', '.2')}"/>
        <ellipse cx="118" cy="300" rx="24" ry="42" filter="url(#wcB)"
                 style="{f('fill', 'lite', '#F2DCC2')};{f('opacity', 'lite-o', '.32')}"/>
        <path d="M 96 300 C 122 290, 156 306, 184 296 C 192 322, 176 350, 146 354 C 114 358, 92 332, 96 300 Z"
              filter="url(#wcB)"
              style="{f('fill', 'back', '#EED7BC')};{f('opacity', 'back-o', '.24')}"/>
        <!-- pigment pooling where the wash met its own edge -->
        <use href="#urnGeo" fill="none" stroke-width="7" filter="url(#wcPool)"
             style="{f('stroke', 'pool', '#8E5A2C')};{f('opacity', 'pool-o', '.42')}"/>
        <rect x="70" y="230" width="160" height="170" filter="url(#wcGrain)"
              style="{f('opacity', 'grain-o', '.15')}"/>
        <!-- the throwing rings, brushed on damp -->
        <g fill="none" stroke-width="2.2" filter="url(#wcC)"
           style="{f('stroke', 'ring', '#8E5A2C')};{f('opacity', 'ring-o', '.2')}">
          <path d="M 84 300 C 118 312, 182 312, 216 299"/>
          <path d="M 88 340 C 120 352, 180 352, 212 339"/>
        </g>
      </g>
      <!-- the drawn line, thin and loose, sitting a little off its own wash -->
      <use href="#urnGeo" fill="none" stroke-width="1.5" filter="url(#wcB)"
           style="{f('stroke', 'line', '#7E4F26')};{f('opacity', 'line-o', '.42')}"/>

      <!-- ── the drape: what falls over the front of the jar ── -->
      <g filter="url(#wcC)">
        <g fill="none" stroke-width="2" stroke-linecap="round"
           style="{f('stroke', 'stem', '#5F6C42')};{f('opacity', 'spill-o', '.38')}">
          <path d="M 132 244 Q 108 258, 96 282"/><path d="M 172 244 Q 198 256, 210 278"/>
          <path d="M 150 242 Q 146 262, 134 276"/><path d="M 118 246 Q 100 268, 106 296"/>
          <path d="M 186 246 Q 208 266, 202 294"/>
        </g>
        <g style="{f('fill', 'leafd', '#5F6C42')};{f('opacity', 'spill-o', '.36')}">
{DLEAF}
        </g>
        <g style="{f('fill', 'bud', '#D97A2B')};{f('opacity', 'spill-bud-o', '.46')}">
{DBUD}
        </g>
      </g>
    </symbol>
'''
sys.stdout.write(SYMBOL)
