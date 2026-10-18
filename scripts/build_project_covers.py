"""Build the six linked project covers for the GitHub profile README."""

from pathlib import Path
import re


OUT = Path(__file__).resolve().parents[1] / 'assets' / 'project-covers'
OUT.mkdir(parents=True, exist_ok=True)

FONT = 'Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Noto Sans CJK SC, PingFang SC, sans-serif'


def _body_color(hex_color, element, attribute, filename):
    """Move the original pale UI drawings into a readable electric-blue palette."""
    red, green, blue = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    lightness = (red + green + blue) / (3 * 255)
    warm = red > blue + 12 and red > green + 6
    violet = red > green + 6 and blue > green + 5

    if element == 'text':
        if filename == 'personal-site.svg':
            return '#07529A' if lightness < 0.72 else '#2676B6'
        return '#F4FDFF' if lightness < 0.72 else '#D4F6FF'
    if attribute == 'stroke':
        if filename == 'motoviz.svg' and lightness < 0.55:
            return '#075698'
        if warm:
            return '#FFE8BC'
        if violet:
            return '#C9C0FF'
        return '#B7F4FF' if lightness < 0.75 else '#8EE9FF'
    if warm:
        return '#FFE9B7' if lightness > 0.83 else '#F8CE92'
    if violet:
        return '#AFAEFF' if lightness > 0.83 else '#7D8DE0'
    if lightness >= 0.96:
        return '#A7E5FF'
    if lightness >= 0.90:
        return '#6EC9F5'
    if lightness >= 0.82:
        return '#3E9DDD'
    if lightness >= 0.72:
        return '#267CC5'
    return '#125B9F'


def _neon_body(body, filename):
    def recolor(match):
        tag = match.group(0)
        element = re.match(r'<(rect|circle|path|text)', tag).group(1)

        def replace_attribute(attribute_match):
            attribute, hex_color = attribute_match.groups()
            return f'{attribute}="{_body_color(hex_color, element, attribute, filename)}"'

        tag = re.sub(r'(fill|stroke)="(#[0-9A-Fa-f]{6})"', replace_attribute, tag)
        if element != 'rect':
            return tag

        width_match = re.search(r'\bwidth="([0-9.]+)"', tag)
        height_match = re.search(r'\bheight="([0-9.]+)"', tag)
        if not (width_match and height_match):
            return tag
        width, height = float(width_match.group(1)), float(height_match.group(1))
        if height <= 6 and width >= 30:
            return re.sub(r'fill="[^"]+"', 'fill="#B5F0FF"', tag, count=1)
        if width >= 100 and height >= 20:
            if filename == 'personal-site.svg':
                gradient = 'site-glass'
            elif filename in ('scene-director.svg', 'light-fresh-film.svg'):
                gradient = 'scene-glass'
            elif filename == 'motoviz.svg' and width >= 300:
                gradient = 'scene-glass'
            else:
                gradient = 'ui-glass'
            return re.sub(r'fill="[^"]+"', f'fill="url(#{gradient})"', tag, count=1)
        if width <= 65 and 12 <= height <= 26:
            return re.sub(r'fill="[^"]+"', 'fill="#318DCE"', tag, count=1)
        return tag

    return re.sub(r'<(?:rect|circle|path|text)\b[^>]*>', recolor, body)


def cover(filename, title, subtitle, index, tag, accent, body, footer):
    accent = '#A9F7FF'
    body = _neon_body(body, filename)
    if filename == 'motoviz.svg':
        start = body.index('<rect x="50" y="172"')
        end = body.index('<rect x="416" y="170"', start)
        bike = Path(__file__).with_name('motoviz_neon_body.svgfrag').read_text(encoding='utf-8')
        body = body[:start] + bike + '\n  ' + body[end:]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="360" viewBox="0 0 640 360" role="img" aria-labelledby="title desc">
  <title id="title">{title} · MN0709 project cover</title>
  <desc id="desc">{subtitle}. Original vector illustration of {footer}.</desc>
  <defs>
    <linearGradient id="background" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#053D86"/>
      <stop offset="0.48" stop-color="#075AA9"/>
      <stop offset="1" stop-color="#078ACD"/>
    </linearGradient>
    <linearGradient id="surface" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0966B2"/>
      <stop offset="0.5" stop-color="#3195D3"/>
      <stop offset="1" stop-color="#1079C5"/>
    </linearGradient>
    <linearGradient id="pill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#1164B9"/>
      <stop offset="1" stop-color="#2F9DFA"/>
    </linearGradient>
    <linearGradient id="ui-glass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#1C71BE"/>
      <stop offset="0.52" stop-color="#3B9BD8"/>
      <stop offset="1" stop-color="#55B9E6"/>
    </linearGradient>
    <linearGradient id="scene-glass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#70BAE9"/>
      <stop offset="0.48" stop-color="#8FD7F2"/>
      <stop offset="1" stop-color="#3D99D7"/>
    </linearGradient>
    <linearGradient id="site-glass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#C9F2FF"/>
      <stop offset="0.56" stop-color="#A4DAF6"/>
      <stop offset="1" stop-color="#66B8E9"/>
    </linearGradient>
    <linearGradient id="caustic" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#6DCAFF" stop-opacity="0"/>
      <stop offset="0.25" stop-color="#CEFFFF" stop-opacity="0.65"/>
      <stop offset="0.5" stop-color="#7EE2FF" stop-opacity="0.05"/>
      <stop offset="0.78" stop-color="#D8A8FF" stop-opacity="0.52"/>
      <stop offset="1" stop-color="#69E7FF" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="aura" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#8BF7FF" stop-opacity="0.78"/>
      <stop offset="0.45" stop-color="#44CBFF" stop-opacity="0.34"/>
      <stop offset="1" stop-color="#44CBFF" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="rainbow" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#FFE9BE" stop-opacity="0.45"/>
      <stop offset="0.32" stop-color="#C99CFF" stop-opacity="0.22"/>
      <stop offset="0.67" stop-color="#6CFCED" stop-opacity="0.12"/>
      <stop offset="1" stop-color="#6CFCED" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="flare" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.9"/>
      <stop offset="0.18" stop-color="#C2FFFF" stop-opacity="0.5"/>
      <stop offset="1" stop-color="#67D9FF" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadow" x="-20%" y="-30%" width="140%" height="170%">
      <feDropShadow dx="0" dy="5" stdDeviation="11" flood-color="#A5F9FF" flood-opacity="0.5"/>
    </filter>
    <filter id="soft-glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="9"/>
    </filter>
    <clipPath id="window-clip"><rect x="31" y="155" width="578" height="166" rx="18"/></clipPath>
    <clipPath id="card-clip"><rect x="1" y="1" width="638" height="358" rx="25"/></clipPath>
  </defs>
  <rect x="2" y="2" width="636" height="356" rx="26" fill="#24DCFF" opacity="0.55" filter="url(#soft-glow)"/>
  <rect x="0.5" y="0.5" width="639" height="359" rx="26" fill="url(#background)" stroke="#BDFBFF" stroke-width="1.5"/>
  <g clip-path="url(#card-clip)">
    <ellipse cx="115" cy="116" rx="185" ry="141" fill="url(#aura)" opacity="0.35"/>
    <ellipse cx="496" cy="285" rx="186" ry="168" fill="url(#aura)" opacity="0.56"/>
    <ellipse cx="328" cy="16" rx="172" ry="93" fill="url(#rainbow)" opacity="0.8"/>
    <ellipse cx="540" cy="65" rx="125" ry="93" fill="url(#rainbow)" opacity="0.85"/>
    <ellipse cx="50" cy="258" rx="158" ry="136" fill="url(#rainbow)" opacity="0.38"/>
    <ellipse cx="390" cy="196" rx="134" ry="115" fill="url(#rainbow)" opacity="0.34"/>
    <path d="M-20 136C155 40 220 171 372 68S568 99 666-15" fill="none" stroke="url(#caustic)" stroke-width="40" opacity="0.73" filter="url(#soft-glow)"/>
    <path d="M-35 354C140 267 308 366 430 256S592 284 669 207" fill="none" stroke="url(#caustic)" stroke-width="34" opacity="0.72" filter="url(#soft-glow)"/>
    <path d="M-10 47C126 5 176 94 312 52S498 86 652 17" fill="none" stroke="url(#caustic)" stroke-width="18" opacity="0.5" filter="url(#soft-glow)"/>
    <path d="M33 347C131 289 194 343 274 302S384 308 444 274" fill="none" stroke="#C5FEFF" stroke-width="6" opacity="0.18" filter="url(#soft-glow)"/>
    <path d="M-8 181C147 63 276 218 407 102S566 108 647 16" fill="none" stroke="#A6FCFF" stroke-width="2" opacity="0.15"/>
    <path d="M-13 356C132 270 262 340 427 242S553 280 650 191" fill="none" stroke="#C8FCFF" stroke-width="2" opacity="0.22"/>
    <ellipse cx="526" cy="2" rx="90" ry="31" fill="url(#flare)" opacity="0.48"/>
    <ellipse cx="84" cy="357" rx="84" ry="30" fill="url(#flare)" opacity="0.38"/>
  </g>
  <path d="M1 50.5h638" stroke="#A9EDFF" stroke-opacity="0.48"/>
  <circle cx="29" cy="25" r="5" fill="#FC7D9B"/>
  <circle cx="47" cy="25" r="5" fill="#FFE26D"/>
  <circle cx="65" cy="25" r="5" fill="#71FFB0"/>
  <text x="90" y="29" fill="#E8FAFF" font-family="{FONT}" font-weight="700" font-size="11" letter-spacing="2">MN0709 / SELECTED WORK</text>
  <text x="584" y="29" fill="#F4FCFF" font-family="{FONT}" font-weight="700" font-size="12" text-anchor="end">{index} / 06</text>
  <rect x="31" y="72" width="4" height="63" rx="2" fill="{accent}" filter="url(#shadow)"/>
  <text x="47" y="104" fill="#FFFFFF" font-family="{FONT}" font-size="29" font-weight="750" letter-spacing="-0.7">{title}</text>
  <text x="48" y="130" fill="#E9F8FF" font-family="{FONT}" font-size="15" font-weight="600">{subtitle}</text>
  <rect x="482" y="78" width="125" height="25" rx="12.5" fill="url(#pill)" stroke="#D5F9FF" filter="url(#shadow)"/>
  <text x="544.5" y="95" text-anchor="middle" fill="#FFFFFF" font-family="{FONT}" font-size="10" font-weight="700" letter-spacing="1.2">{tag}</text>
  <rect x="31" y="155" width="578" height="166" rx="18" fill="url(#surface)" stroke="#B8F8FF" stroke-width="1.7" filter="url(#shadow)"/>
  <g clip-path="url(#window-clip)">{body}</g>
  <g clip-path="url(#window-clip)" opacity="0.2">
    <ellipse cx="518" cy="169" rx="178" ry="60" fill="url(#flare)"/>
    <path d="M25 328C155 249 226 340 347 256S539 270 630 184" fill="none" stroke="url(#caustic)" stroke-width="17" filter="url(#soft-glow)"/>
  </g>
  <rect x="32" y="156" width="576" height="164" rx="17" fill="none" stroke="#FFFFFF" stroke-opacity="0.52"/>
  <path d="M46 160h141M452 316h142" stroke="#DBFDFF" stroke-width="2" stroke-linecap="round" opacity="0.9"/>
  <circle cx="300" cy="156" r="3" fill="#FFFFFF"/>
  <ellipse cx="365" cy="155" rx="36" ry="10" fill="url(#flare)"/>
  <ellipse cx="36" cy="314" rx="28" ry="11" fill="url(#flare)" opacity="0.75"/>
  <ellipse cx="606" cy="309" rx="32" ry="11" fill="url(#flare)" opacity="0.75"/>
  <circle cx="40" cy="340" r="3" fill="{accent}"/>
  <text x="50" y="344" fill="#E4F9FF" font-family="{FONT}" font-size="10" font-weight="700" letter-spacing="1.8">{footer.upper()}</text>
  <path d="M580 341h23m-7-7 7 7-7 7" fill="none" stroke="#EEFFFF" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''
    (OUT / filename).write_text(svg + '\n', encoding='utf-8')


cover(
    'meeting-review.svg', '会脉 · meeting-review', '让会议记录回到可追溯的事实',
    '01', 'MEETING AI', '#7798AB',
    '''
  <rect x="31" y="155" width="578" height="33" fill="#F1F6F9"/>
  <circle cx="52" cy="171.5" r="4" fill="#91B9C1"/>
  <text x="66" y="175" fill="#577084" font-family="''' + FONT + '''" font-size="11" font-weight="700" letter-spacing="1">REVIEW SESSION</text>
  <path d="M413 172h88" stroke="#A8C4D0" stroke-width="2" stroke-linecap="round"/>
  <circle cx="517" cy="172" r="3" fill="#8FAEC0"/>
  <path d="M522 172h59" stroke="#A8C4D0" stroke-width="2" stroke-linecap="round"/>
  <path d="M327 190v131" stroke="#E1EAF0"/>
  <text x="53" y="208" fill="#91A4B3" font-family="''' + FONT + '''" font-size="9" font-weight="700" letter-spacing="1.7">TRANSCRIPT</text>
  <text x="350" y="208" fill="#91A4B3" font-family="''' + FONT + '''" font-size="9" font-weight="700" letter-spacing="1.7">DECISIONS &amp; ACTIONS</text>
  <rect x="51" y="222" width="53" height="21" rx="7" fill="#E7F0F3"/>
  <text x="77.5" y="236" fill="#5E8490" text-anchor="middle" font-family="''' + FONT + '''" font-size="10" font-weight="700">08:32</text>
  <rect x="114" y="224" width="150" height="6" rx="3" fill="#8EADBC"/>
  <rect x="114" y="237" width="186" height="5" rx="2.5" fill="#DFE9EF"/>
  <rect x="51" y="256" width="53" height="21" rx="7" fill="#EDECF7"/>
  <text x="77.5" y="270" fill="#8983AE" text-anchor="middle" font-family="''' + FONT + '''" font-size="10" font-weight="700">12:47</text>
  <rect x="114" y="258" width="126" height="6" rx="3" fill="#AAA9C7"/>
  <rect x="114" y="271" width="167" height="5" rx="2.5" fill="#DFE9EF"/>
  <rect x="51" y="289" width="249" height="20" rx="9" fill="#F3F7F9"/>
  <path d="M64 299h2v-5h2v11h2v-8h2v4h2v-12h2v18h2v-11h2v7h2v-5h2v3h2v-8h2v12h2v-5h2v-5h2v7h2v-4h2" fill="none" stroke="#8EAEBB" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M109 299h173" stroke="#D2E0E8" stroke-width="2" stroke-linecap="round"/>
  <circle cx="206" cy="299" r="4" fill="#7798AB"/>
  <rect x="350" y="220" width="232" height="43" rx="10" fill="#F5F8FB" stroke="#E2EAF0"/>
  <circle cx="369" cy="241" r="10" fill="#E1EDF0"/>
  <path d="m365 241 3 3 5-6" fill="none" stroke="#729B9E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="386" y="239" fill="#50687A" font-family="''' + FONT + '''" font-size="11" font-weight="700">决策有出处</text>
  <text x="386" y="253" fill="#91A4B3" font-family="''' + FONT + '''" font-size="9">链接到原句与时间戳</text>
  <rect x="350" y="272" width="232" height="32" rx="10" fill="#F5F8FB" stroke="#E2EAF0"/>
  <rect x="362" y="282" width="12" height="12" rx="3" fill="#EEEAF6" stroke="#A49CC4"/>
  <text x="387" y="292" fill="#50687A" font-family="''' + FONT + '''" font-size="11" font-weight="700">行动项清晰可回看</text>
    ''', 'traceable meeting review')


cover(
    'desk-research.svg', 'DeskResearch', '从资料来源走向带引用的结论',
    '02', 'RESEARCH AGENT', '#9D98BD',
    '''
  <rect x="51" y="174" width="250" height="34" rx="11" fill="#FFFFFF" stroke="#DDE5EE"/>
  <circle cx="71" cy="190" r="7" fill="none" stroke="#9F9BBD" stroke-width="2"/>
  <path d="m76 195 6 6" stroke="#9F9BBD" stroke-width="2" stroke-linecap="round"/>
  <text x="92" y="195" fill="#90A0B1" font-family="''' + FONT + '''" font-size="11">Research question...</text>
  <path d="M190 211v16m0 0h102" fill="none" stroke="#B5ADCE" stroke-width="1.7" stroke-dasharray="3 4"/>
  <path d="M190 227h-96" fill="none" stroke="#B5ADCE" stroke-width="1.7" stroke-dasharray="3 4"/>
  <rect x="51" y="227" width="140" height="65" rx="11" fill="#F6F7FB" stroke="#E1E5EF"/>
  <rect x="62" y="238" width="26" height="18" rx="5" fill="#E6E4F3"/>
  <text x="75" y="251" fill="#847EAD" text-anchor="middle" font-family="''' + FONT + '''" font-size="9" font-weight="700">S1</text>
  <rect x="96" y="241" width="76" height="5" rx="2.5" fill="#A9AAC6"/>
  <rect x="96" y="251" width="63" height="4" rx="2" fill="#D3DCE7"/>
  <rect x="62" y="267" width="107" height="4" rx="2" fill="#D8E0E9"/>
  <rect x="205" y="227" width="140" height="65" rx="11" fill="#F6F8FA" stroke="#E1E5EF"/>
  <rect x="216" y="238" width="26" height="18" rx="5" fill="#E2EEF0"/>
  <text x="229" y="251" fill="#668F9B" text-anchor="middle" font-family="''' + FONT + '''" font-size="9" font-weight="700">S2</text>
  <rect x="250" y="241" width="76" height="5" rx="2.5" fill="#9AAFC0"/>
  <rect x="250" y="251" width="63" height="4" rx="2" fill="#D3DCE7"/>
  <rect x="216" y="267" width="107" height="4" rx="2" fill="#D8E0E9"/>
  <path d="M359 258h22" stroke="#B7B3D2" stroke-width="2" stroke-linecap="round"/>
  <path d="m374 252 7 6-7 6" fill="none" stroke="#B7B3D2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="399" y="176" width="180" height="117" rx="13" fill="#FCFCFE" stroke="#DDE3EE"/>
  <rect x="399" y="176" width="180" height="27" rx="13" fill="#EFEFF8"/>
  <path d="M399 192v11h180v-11" fill="#EFEFF8"/>
  <circle cx="414" cy="190" r="4" fill="#ADA8C8"/>
  <text x="426" y="194" fill="#77749A" font-family="''' + FONT + '''" font-size="10" font-weight="700">EVIDENCE BRIEF</text>
  <rect x="414" y="218" width="88" height="6" rx="3" fill="#8C93B4"/>
  <rect x="414" y="233" width="145" height="5" rx="2.5" fill="#DAE2EB"/>
  <rect x="414" y="245" width="124" height="5" rx="2.5" fill="#DAE2EB"/>
  <rect x="414" y="263" width="42" height="18" rx="7" fill="#EBE9F6"/>
  <text x="435" y="276" fill="#8580A6" text-anchor="middle" font-family="''' + FONT + '''" font-size="9" font-weight="700">[S1]</text>
  <rect x="462" y="263" width="42" height="18" rx="7" fill="#E6F0F2"/>
  <text x="483" y="276" fill="#658B98" text-anchor="middle" font-family="''' + FONT + '''" font-size="9" font-weight="700">[S2]</text>
  <rect x="520" y="263" width="44" height="18" rx="7" fill="#F3F6FA" stroke="#DBE4EB"/>
  <text x="542" y="276" fill="#71899A" text-anchor="middle" font-family="''' + FONT + '''" font-size="9" font-weight="700">EXPORT</text>
    ''', 'sourced research workflow')


cover(
    'motoviz.svg', 'MotoViz', '3D 改装展示 × RAG 配件检索',
    '03', 'TEAM MVP', '#7198A4',
    '''
  <rect x="50" y="172" width="350" height="132" rx="12" fill="#F6FAFB" stroke="#E0E9EF"/>
  <path d="M51 281h348" stroke="#DAE6EC" stroke-width="1.5"/>
  <path d="M81 177v105m55-105v105m55-105v105m55-105v105m55-105v105m55-105v105" stroke="#EAF0F4"/>
  <path d="M62 243h320m-320-32h320" stroke="#EEF3F6"/>
  <circle cx="123" cy="263" r="27" fill="#FFFFFF" stroke="#4E7284" stroke-width="5"/>
  <circle cx="123" cy="263" r="12" fill="#E8F1F3" stroke="#91ADB7" stroke-width="2"/>
  <circle cx="318" cy="263" r="27" fill="#FFFFFF" stroke="#4E7284" stroke-width="5"/>
  <circle cx="318" cy="263" r="12" fill="#E8F1F3" stroke="#91ADB7" stroke-width="2"/>
  <path d="M123 263 163 210h85l42 53h28M163 210l-18 53h145l-42-53M184 210l24 30h48" fill="none" stroke="#426B7B" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="m168 207 30-25h55l35 32-25 19-69-1z" fill="#A4BFCA" stroke="#527789" stroke-width="2"/>
  <path d="m207 180 6-11h42l10 15" fill="none" stroke="#54798A" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M282 202h38l18-19h20m-39 19 13 32" fill="none" stroke="#54798A" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M325 179h31l11 5" fill="none" stroke="#54798A" stroke-width="4" stroke-linecap="round"/>
  <path d="M153 204h-19l-7-11h-18" fill="none" stroke="#54798A" stroke-width="4" stroke-linecap="round"/>
  <circle cx="234" cy="245" r="17" fill="#EDF4F5" stroke="#7C9CA8" stroke-width="2"/>
  <path d="M224 245h20m-10-10v20" stroke="#7C9CA8" stroke-width="2"/>
  <circle cx="271" cy="203" r="5" fill="#A99FC4"/>
  <path d="M271 198v-25h140" fill="none" stroke="#A99FC4" stroke-width="1.7" stroke-dasharray="4 4"/>
  <rect x="416" y="170" width="165" height="134" rx="12" fill="#FFFFFF" stroke="#DCE7EE"/>
  <text x="431" y="191" fill="#607A8D" font-family="''' + FONT + '''" font-size="10" font-weight="700" letter-spacing="1">PARTS SEARCH</text>
  <rect x="430" y="201" width="137" height="24" rx="8" fill="#F3F7FA" stroke="#E0EAF0"/>
  <circle cx="444" cy="213" r="4.5" fill="none" stroke="#96AFC0" stroke-width="1.5"/>
  <path d="m447 216 4 4" stroke="#96AFC0" stroke-width="1.5"/>
  <path d="M458 213h78" stroke="#CEDBE4" stroke-width="3" stroke-linecap="round"/>
  <rect x="430" y="236" width="137" height="32" rx="8" fill="#F5F8FB"/>
  <circle cx="444" cy="252" r="7" fill="#E3EFF0"/>
  <path d="m441 252 2 2 4-5" fill="none" stroke="#6D9A9F" stroke-width="1.5" stroke-linecap="round"/>
  <rect x="457" y="246" width="67" height="4" rx="2" fill="#819DAA"/>
  <rect x="457" y="255" width="92" height="3" rx="1.5" fill="#D8E2E9"/>
  <text x="432" y="290" fill="#8F9DAB" font-family="''' + FONT + '''" font-size="9">3D VIEW  ·  EVIDENCE LINKS</text>
    ''', 'motorcycle visualization and parts retrieval')


cover(
    'scene-director.svg', '15s Scene Director', '把 15 秒拆成有节奏的镜头',
    '04', 'PROMPT SKILL', '#A89CC0',
    '''
  <path d="M31 292h578" stroke="#E6EBF1"/>
  <rect x="51" y="177" width="151" height="100" rx="11" fill="#EFF4F8" stroke="#D8E3EB"/>
  <rect x="218" y="177" width="151" height="100" rx="11" fill="#EFF4F8" stroke="#D8E3EB"/>
  <rect x="385" y="177" width="151" height="100" rx="11" fill="#EFF4F8" stroke="#D8E3EB"/>
  <path d="M52 248q36-27 75-7t74-5v40H52z" fill="#CDDEE5"/>
  <circle cx="110" cy="213" r="22" fill="#DCD6ED"/>
  <circle cx="110" cy="213" r="11" fill="#F9FAFC"/>
  <path d="M76 244 98 221l16 15 18-13 33 29" fill="none" stroke="#90AABA" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M219 247q29-12 73-16 44 8 76 23v22H219z" fill="#CDD8E7"/>
  <path d="m247 240 29-41 31 37" fill="#E2E8F0" stroke="#A2AEC6" stroke-width="2"/>
  <path d="M292 232q9-21 19-21t20 21" fill="none" stroke="#8F9FAF" stroke-width="2"/>
  <circle cx="309" cy="223" r="4" fill="#9D95BC"/>
  <path d="M386 242q34 4 62-13 39-23 87 3v44H386z" fill="#CBDDE5"/>
  <path d="M415 235q13-23 22-23 11 0 22 23M461 227q16-30 31-30 13 0 29 34" fill="none" stroke="#94ABBC" stroke-width="2.5"/>
  <path d="M459 194h2m-11 7 2 1m20 0 2-1m-14-19v3" stroke="#B2A5CC" stroke-width="2" stroke-linecap="round"/>
  <circle cx="461" cy="194" r="5" fill="#DCD4EB"/>
  <rect x="60" y="254" width="56" height="16" rx="7" fill="#FFFFFF" fill-opacity="0.88"/>
  <text x="88" y="266" fill="#6C8097" text-anchor="middle" font-family="''' + FONT + '''" font-size="9" font-weight="700">00–05s</text>
  <rect x="227" y="254" width="56" height="16" rx="7" fill="#FFFFFF" fill-opacity="0.88"/>
  <text x="255" y="266" fill="#6C8097" text-anchor="middle" font-family="''' + FONT + '''" font-size="9" font-weight="700">05–10s</text>
  <rect x="394" y="254" width="56" height="16" rx="7" fill="#FFFFFF" fill-opacity="0.88"/>
  <text x="422" y="266" fill="#6C8097" text-anchor="middle" font-family="''' + FONT + '''" font-size="9" font-weight="700">10–15s</text>
  <path d="M102 299h387" stroke="#D0D9E5" stroke-width="4" stroke-linecap="round"/>
  <circle cx="102" cy="299" r="6" fill="#B5ADC9"/>
  <circle cx="294" cy="299" r="6" fill="#A4B7C8"/>
  <circle cx="489" cy="299" r="6" fill="#8DADBB"/>
  <path d="M548 228h39m-8-8 8 8-8 8" fill="none" stroke="#AA9EC2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    ''', 'three-beat 15-second storyboard')


cover(
    'light-fresh-film.svg', 'Light Fresh Short Film', '为 5–30 秒短片设计轻盈叙事',
    '05', 'PROMPT SKILL', '#8EADB3',
    '''
  <rect x="49" y="172" width="543" height="114" rx="12" fill="#EAF1F4" stroke="#D6E3EA"/>
  <rect x="61" y="183" width="161" height="91" rx="8" fill="#F8F9F5"/>
  <rect x="239" y="183" width="161" height="91" rx="8" fill="#F9F8F5"/>
  <rect x="417" y="183" width="161" height="91" rx="8" fill="#F8F9F5"/>
  <circle cx="183" cy="209" r="16" fill="#E7E3D4"/>
  <path d="M62 250q49-26 99 2t61-3v25H62z" fill="#C9DCE2"/>
  <path d="M92 253q15-29 32-33 21 8 37 33" fill="#DBE7E5"/>
  <path d="M76 269q24-42 48-14" fill="none" stroke="#8DAC9E" stroke-width="3" stroke-linecap="round"/>
  <path d="M247 256q41-20 79 1t66-13v30H247z" fill="#D4DDE7"/>
  <path d="M282 274q10-41 26-54 21 8 30 54" fill="#C2D4D9"/>
  <circle cx="309" cy="214" r="8" fill="#9DAFC1"/>
  <path d="M312 221q-1 27 16 47" fill="none" stroke="#849CB0" stroke-width="3" stroke-linecap="round"/>
  <path d="M418 250q31-24 75-7 43 15 85 0v31H418z" fill="#CCDDE2"/>
  <path d="M467 262q10-48 36-48 30 0 38 48" fill="#E3E8E3"/>
  <path d="M473 258q10-39 29-40 20 1 29 40" fill="none" stroke="#A8C1BD" stroke-width="2"/>
  <path d="M428 224q11-14 22 0m81-18q8-10 16 0" fill="none" stroke="#B9C7CC" stroke-width="2" stroke-linecap="round"/>
  <path d="M61 297h518" stroke="#DCE6ED" stroke-width="3" stroke-linecap="round"/>
  <path d="M61 297h141" stroke="#9FBEBE" stroke-width="3" stroke-linecap="round"/>
  <circle cx="202" cy="297" r="5" fill="#8EADB3"/>
  <text x="58" y="313" fill="#91A1AF" font-family="''' + FONT + '''" font-size="9" font-weight="700" letter-spacing="1">OPENING</text>
  <text x="285" y="313" fill="#91A1AF" font-family="''' + FONT + '''" font-size="9" font-weight="700" letter-spacing="1">MOMENT</text>
  <text x="526" y="313" fill="#91A1AF" font-family="''' + FONT + '''" font-size="9" font-weight="700" letter-spacing="1">AFTERGLOW</text>
    ''', 'gentle short-film storyboard')


cover(
    'personal-site.svg', 'MN0709 · Personal Site', '产品、项目与写作的个人入口',
    '06', 'PORTFOLIO', '#8F9FC1',
    '''
  <rect x="48" y="172" width="544" height="133" rx="12" fill="#FFFFFF" stroke="#DBE5ED"/>
  <rect x="48" y="172" width="544" height="25" rx="12" fill="#F0F4F8"/>
  <path d="M48 186v11h544v-11" fill="#F0F4F8"/>
  <circle cx="64" cy="184.5" r="3" fill="#C3CFDB"/>
  <circle cx="76" cy="184.5" r="3" fill="#C3CFDB"/>
  <circle cx="88" cy="184.5" r="3" fill="#C3CFDB"/>
  <rect x="129" y="178" width="255" height="13" rx="6" fill="#FFFFFF"/>
  <text x="137" y="188" fill="#A1B1BF" font-family="''' + FONT + '''" font-size="8">mn0709.github.io</text>
  <path d="M393 197v108" stroke="#E4EBF1"/>
  <text x="70" y="225" fill="#334C61" font-family="''' + FONT + '''" font-size="24" font-weight="750">MN0709</text>
  <text x="71" y="244" fill="#8FA0B2" font-family="''' + FONT + '''" font-size="10" font-weight="700" letter-spacing="1.6">AI PRODUCT BUILDER</text>
  <rect x="70" y="257" width="185" height="4" rx="2" fill="#CBD8E3"/>
  <rect x="70" y="268" width="148" height="4" rx="2" fill="#DDE6EE"/>
  <rect x="70" y="284" width="58" height="14" rx="7" fill="#E9EDF6"/>
  <text x="99" y="294" text-anchor="middle" fill="#858EAF" font-family="''' + FONT + '''" font-size="8" font-weight="700">PROJECTS</text>
  <rect x="136" y="284" width="53" height="14" rx="7" fill="#E8F1F3"/>
  <text x="162.5" y="294" text-anchor="middle" fill="#7899A3" font-family="''' + FONT + '''" font-size="8" font-weight="700">WRITING</text>
  <rect x="414" y="211" width="72" height="68" rx="9" fill="#EEF3F8" stroke="#DFE6EF"/>
  <rect x="426" y="223" width="48" height="6" rx="3" fill="#9EADC0"/>
  <rect x="426" y="237" width="38" height="4" rx="2" fill="#CCD8E3"/>
  <rect x="426" y="245" width="43" height="4" rx="2" fill="#CCD8E3"/>
  <path d="M426 266h42" stroke="#ADB9CF" stroke-width="2" stroke-linecap="round"/>
  <rect x="498" y="222" width="72" height="68" rx="9" fill="#EEF5F6" stroke="#DFE9EB"/>
  <circle cx="521" cy="241" r="11" fill="#C6DBE1"/>
  <path d="m512 255 12-14 11 11 9-7 13 16" fill="none" stroke="#82A7AE" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M433 283h57m4 0h18" stroke="#C9D5E1" stroke-width="2" stroke-linecap="round"/>
    ''', 'personal website preview')


heading = '''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="68" viewBox="0 0 1000 68" role="img" aria-labelledby="title desc">
  <title id="title">精选项目</title>
  <desc id="desc">我关注真实任务中的 AI 产品：先弄清问题，再做可验证的工作流，最后用证据决定下一步。</desc>
  <defs>
    <linearGradient id="blue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#064486"/>
      <stop offset="0.58" stop-color="#0879BD"/>
      <stop offset="1" stop-color="#23A6E9"/>
    </linearGradient>
    <radialGradient id="glow"><stop stop-color="#B4FFFF" stop-opacity="0.64"/><stop offset="1" stop-color="#B4FFFF" stop-opacity="0"/></radialGradient>
    <filter id="blur"><feGaussianBlur stdDeviation="10"/></filter>
  </defs>
  <rect x="1" y="1" width="998" height="66" rx="16" fill="url(#blue)" stroke="#A8F6FF" stroke-width="1.5"/>
  <ellipse cx="395" cy="4" rx="200" ry="77" fill="url(#glow)" opacity="0.43"/>
  <ellipse cx="903" cy="68" rx="180" ry="86" fill="url(#glow)" opacity="0.5"/>
  <path d="M450 15C602 69 788-19 1044 39" stroke="#A8FDFF" stroke-width="26" fill="none" opacity="0.34" filter="url(#blur)"/>
  <text x="25" y="42" fill="#FFFFFF" font-family="Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Noto Sans CJK SC, PingFang SC, sans-serif" font-size="18" font-weight="750">我关注真实任务中的 AI 产品：先弄清问题，再做可验证的工作流，最后用证据决定下一步。</text>
</svg>'''
(OUT / 'selected-work-heading.svg').write_text(heading + '\n', encoding='utf-8')


print('\n'.join(str(p) for p in sorted(OUT.glob('*.svg'))))
