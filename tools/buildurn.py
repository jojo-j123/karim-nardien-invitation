"""Assemble the jar-and-bloom symbol from the generated foliage."""
import re, subprocess, sys

frag = subprocess.run([sys.executable, 'genurn.py'], capture_output=True, text=True, check=True).stdout

def section(name):
    m = re.search(r'<!-- %s: \d+ -->\n(.*?)\n\n' % name, frag, re.S)
    return m.group(1).rstrip()

MASS, STEMS, LDARK, LLIGHT, SKIRT, BUDS, HEARTS = (section(n) for n in
    ('mass', 'stems', 'leavesdark', 'leaveslight', 'skirt', 'buds', 'hearts'))

# a wide-bellied garden jar: broad mouth, shoulder just under the rim, tapering
# to a modest foot — the jars the reference photograph is full of
JAR = ('M 102 252 C 98 268, 82 288, 80 312 C 78 342, 90 372, 108 388 L 192 388 '
       'C 210 372, 222 342, 220 312 C 218 288, 202 268, 198 252 Z')
LIP = ('M 97 250 C 120 259, 180 259, 203 250 C 203 241, 184 237, 150 237 '
       'C 116 237, 97 241, 97 250 Z')

SYMBOL = f'''    <path id="urnJar" d="{JAR}"/>
    <path id="urnLip" d="{LIP}"/>
    <g id="urnGeo"><use href="#urnJar"/><use href="#urnLip"/></g>
    <!-- a clipPath's children must be shapes: a use of a group clips to nothing -->
    <clipPath id="urnGeoClip"><use href="#urnJar"/><use href="#urnLip"/></clipPath>
    <symbol id="urnMark" viewBox="0 0 300 400">
      <!-- ── the bloom, painted before the jar so its stems run behind the rim ── -->
      <!-- the mass, laid in wet as one shape before anything is drawn in it -->
      <g fill="#7C8757" opacity=".1" filter="url(#wcWet)">
{MASS}
      </g>
      <!-- what lies under: the stems (mostly buried), the darker leaves, and the
           skirt of foliage where the plant leaves the mouth of the jar -->
      <g filter="url(#wcC)">
        <g fill="none" stroke="#5C6940" stroke-width="1.7" stroke-linecap="round" opacity=".26">
{STEMS}
        </g>
        <g fill="#4F5C36" opacity=".34">
{LDARK}
        </g>
        <g fill="#5C6940" opacity=".34">
{SKIRT}
        </g>
      </g>
      <!-- and what lies over: the lit leaves and the blossom -->
      <g filter="url(#wcB)">
        <g fill="#77855A" opacity=".38">
{LLIGHT}
        </g>
        <g fill="#DC7C2A" opacity=".52">
{BUDS}
        </g>
        <g fill="#AE4C0C" opacity=".4">
{HEARTS}
        </g>
      </g>

      <!-- ── the jar: two thin washes that do not quite agree, so the paper is
             never fully covered and the terracotta keeps moving ── -->
      <use href="#urnGeo" fill="#D9A472" opacity=".46" filter="url(#wcA)"/>
      <use href="#urnGeo" fill="#C0854E" opacity=".3"  filter="url(#wcB)" transform="translate(3.5,-2.5)"/>
      <g clip-path="url(#urnGeoClip)">
        <!-- the shaded side, and the light the left of it keeps -->
        <ellipse cx="206" cy="322" rx="40" ry="86" fill="#96602F" opacity=".26" filter="url(#wcB)"/>
        <ellipse cx="150" cy="384" rx="62" ry="20" fill="#845228" opacity=".2"  filter="url(#wcC)"/>
        <ellipse cx="118" cy="300" rx="24" ry="42" fill="#F2DCC2" opacity=".32" filter="url(#wcB)"/>
        <path d="M 96 300 C 122 290, 156 306, 184 296 C 192 322, 176 350, 146 354 C 114 358, 92 332, 96 300 Z"
              fill="#EED7BC" opacity=".24" filter="url(#wcB)"/>
        <!-- pigment pooling where the wash met its own edge -->
        <use href="#urnGeo" fill="none" stroke="#8E5A2C" stroke-width="7" opacity=".42" filter="url(#wcPool)"/>
        <rect x="70" y="230" width="160" height="170" filter="url(#wcGrain)" opacity=".15"/>
        <!-- the throwing rings, brushed on damp -->
        <g fill="none" stroke="#8E5A2C" stroke-width="2.2" opacity=".2" filter="url(#wcC)">
          <path d="M 84 300 C 118 312, 182 312, 216 299"/>
          <path d="M 88 340 C 120 352, 180 352, 212 339"/>
        </g>
      </g>
      <!-- the drawn line, thin and loose, sitting a little off its own wash -->
      <use href="#urnGeo" fill="none" stroke="#7E4F26" stroke-width="1.5" opacity=".42" filter="url(#wcB)"/>

      <!-- ── what spills over the front of the rim ── -->
      <g filter="url(#wcC)">
        <g fill="none" stroke="#5F6C42" stroke-width="2" stroke-linecap="round" opacity=".38">
          <path d="M 132 244 Q 108 258, 96 280"/><path d="M 172 244 Q 198 256, 210 276"/>
          <path d="M 150 242 Q 146 262, 134 274"/>
        </g>
        <g fill="#5F6C42" opacity=".36">
          <ellipse cx="104" cy="270" rx="7.4" ry="3" transform="rotate(56 104 270)"/>
          <ellipse cx="204" cy="266" rx="7" ry="2.8" transform="rotate(-52 204 266)"/>
          <ellipse cx="139" cy="266" rx="6" ry="2.6" transform="rotate(70 139 266)"/>
        </g>
        <g fill="#D97A2B" opacity=".46">
          <circle cx="95" cy="282" r="5"/><circle cx="211" cy="278" r="4.6"/>
          <circle cx="133" cy="276" r="3.6"/><circle cx="116" cy="256" r="3"/>
        </g>
      </g>
    </symbol>
'''
sys.stdout.write(SYMBOL)
