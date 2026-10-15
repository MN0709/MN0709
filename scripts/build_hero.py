from __future__ import annotations

import base64
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageChops


REPO = Path(__file__).resolve().parents[1]
ASSETS = REPO / 'assets'
OUTPUT = ASSETS / 'portfolio-launch.svg'


def embed_pose(name: str) -> str:
    path = ASSETS / f'ip-{name}.png'
    with Image.open(path) as source:
        rgba = source.convert('RGBA')
        alpha = rgba.getchannel('A')
        threshold = alpha.point(lambda value: 255 if value > 16 else 0)
        bounds = threshold.getbbox()
        if bounds is None:
            raise ValueError(f'No visible subject: {path}')
        left, top, right, bottom = bounds
        bottom = top + int((bottom - top) * 0.68)
        pad_x = int((right - left) * 0.035)
        pad_y = int((bottom - top) * 0.025)
        crop = rgba.crop((max(0, left - pad_x), max(0, top - pad_y), min(rgba.width, right + pad_x), min(rgba.height, bottom + pad_y)))
        fade = Image.new('L', (1, crop.height), 255)
        fade_start = int(crop.height * 0.83)
        for y in range(fade_start, crop.height):
            fade.putpixel((0, y), int(255 * (crop.height - 1 - y) / (crop.height - fade_start)))
        crop.putalpha(ImageChops.multiply(crop.getchannel('A'), fade.resize(crop.size)))
        crop.thumbnail((420, 700), Image.Resampling.LANCZOS)
        buffer = BytesIO()
        crop.save(buffer, format='PNG', optimize=True)
        return 'data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode('ascii')


poses = {name: embed_pose(name) for name in ('greet', 'present', 'think')}

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="540" viewBox="0 0 1000 540" role="img" aria-labelledby="title desc">
<title id="title">马宁的 AI 产品工作台</title>
<desc id="desc">浅色终端依次展示问题、工作流与验证；右侧的个人形象依次挥手、介绍作品、思考。点击图片访问个人网站。</desc>
<defs>
  <linearGradient id="canvas" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#f7f8fb"/><stop offset="1" stop-color="#edf2f6"/></linearGradient>
  <linearGradient id="right" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#eef1f7"/><stop offset="1" stop-color="#e7eaf2"/></linearGradient>
  <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#35445b" flood-opacity=".12"/></filter>
  <clipPath id="windowClip"><rect x="1" y="1" width="998" height="538" rx="20"/></clipPath>
</defs>
<style>
  .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "PingFang SC", "Microsoft YaHei", monospace; }}
  .sans {{ font-family: Inter, -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif; }}
  .line {{ opacity:0; animation: reveal 10s ease-in-out infinite; }}
  .l1 {{ animation-delay:.2s }} .l2 {{ animation-delay:.6s }} .l3 {{ animation-delay:1s }} .l4 {{ animation-delay:1.4s }} .l5 {{ animation-delay:1.8s }} .l6 {{ animation-delay:2.2s }}
  .ready {{ opacity:0; animation: ready 10s ease-in-out infinite; }}
  .pose {{ transform-origin:790px 472px; }}
  .pose-present,.pose-think,.caption-present,.caption-think {{ opacity:0; }}
  .pose-greet {{ animation: greet 10s ease-in-out infinite; }}
  .pose-present {{ animation: present 10s ease-in-out infinite; }}
  .pose-think {{ animation: think 10s ease-in-out infinite; }}
  .caption-greet {{ animation: greet 10s ease-in-out infinite; }}
  .caption-present {{ animation: present 10s ease-in-out infinite; }}
  .caption-think {{ animation: think 10s ease-in-out infinite; }}
  .arrow {{ animation: nudge 1.4s ease-in-out infinite; }}
  @keyframes reveal {{ 0%,5% {{opacity:0;transform:translateY(5px)}} 10%,79% {{opacity:1;transform:translateY(0)}} 91%,100% {{opacity:0;transform:translateY(-2px)}} }}
  @keyframes ready {{ 0%,36% {{opacity:0;transform:translateY(5px)}} 42%,83% {{opacity:1;transform:translateY(0)}} 91%,100% {{opacity:0}} }}
  @keyframes greet {{ 0%,29% {{opacity:1;transform:translateY(0)}} 33%,96% {{opacity:0;transform:translateY(7px)}} 100% {{opacity:1;transform:translateY(0)}} }}
  @keyframes present {{ 0%,31% {{opacity:0;transform:translateY(7px)}} 35%,62% {{opacity:1;transform:translateY(0)}} 66%,100% {{opacity:0;transform:translateY(7px)}} }}
  @keyframes think {{ 0%,64% {{opacity:0;transform:translateY(7px)}} 68%,94% {{opacity:1;transform:translateY(0)}} 98%,100% {{opacity:0;transform:translateY(7px)}} }}
  @keyframes nudge {{ 0%,100% {{transform:translateX(0)}} 50% {{transform:translateX(6px)}} }}
  @media (prefers-reduced-motion: reduce) {{
    .line,.ready,.pose,.caption-greet,.caption-present,.caption-think,.arrow {{animation:none;transform:none}}
    .line,.ready,.pose-greet,.caption-greet {{opacity:1}}
    .pose-present,.pose-think,.caption-present,.caption-think {{opacity:0}}
  }}
</style>

<rect x="1" y="1" width="998" height="538" rx="20" fill="url(#canvas)" stroke="#d9e0e8" stroke-width="2" filter="url(#shadow)"/>
<g clip-path="url(#windowClip)">
  <rect x="1" y="1" width="998" height="52" fill="#f3f5f8"/>
  <line x1="1" y1="53" x2="999" y2="53" stroke="#dce3eb"/>
  <circle cx="25" cy="27" r="7" fill="#ef7273"/><circle cx="49" cy="27" r="7" fill="#f2c866"/><circle cx="73" cy="27" r="7" fill="#75c99e"/>
  <text class="mono" x="500" y="32" text-anchor="middle" fill="#7a8999" font-size="13">ning@studio — portfolio — 100×30</text>
  <rect x="621" y="54" width="378" height="485" fill="url(#right)"/>
  <line x1="621" y1="54" x2="621" y2="539" stroke="#dce3eb"/>
  <circle cx="820" cy="265" r="166" fill="#ffffff" opacity=".47"/>
  <circle cx="820" cy="265" r="130" fill="none" stroke="#cbd5e3" stroke-width="1.5" stroke-dasharray="4 8"/>
  <text class="mono" x="661" y="92" fill="#7a89a0" font-size="13" letter-spacing="1">PRODUCT · AGENT · CREATION</text>

  <text class="mono line l1" x="52" y="104" fill="#344359" font-size="20" font-weight="700">ning@studio ~ % whoami</text>
  <text class="sans line l2" x="52" y="145" fill="#233246" font-size="29" font-weight="700">马宁 · AI 产品经理</text>
  <line x1="52" y1="166" x2="570" y2="166" stroke="#e2e7ed"/>
  <text class="mono line l3" x="52" y="205" fill="#526376" font-size="19"><tspan fill="#5aa783">[ OK ]</tspan> 理解真实问题</text>
  <text class="mono line l4" x="52" y="244" fill="#526376" font-size="19"><tspan fill="#5aa783">[ OK ]</tspan> 搭建 Agent 工作流</text>
  <text class="mono line l5" x="52" y="283" fill="#526376" font-size="19"><tspan fill="#5aa783">[ OK ]</tspan> 用证据验证结果</text>
  <text class="mono line l6" x="52" y="350" fill="#4675aa" font-size="19" font-weight="700">ning@studio ~ % <tspan fill="#526376" font-weight="400">open ./portfolio</tspan></text>
  <text class="mono ready" x="52" y="397" fill="#4675aa" font-size="20" font-weight="700">READY TO BUILD _</text>
  <rect x="52" y="448" width="515" height="1" fill="#dce3eb"/>
  <text class="sans" x="52" y="485" fill="#53657a" font-size="15">点击探索我的个人网站</text>
  <text class="sans arrow" x="251" y="485" fill="#4675aa" font-size="22">→</text>

  <image class="pose pose-greet" x="640" y="100" width="360" height="408" preserveAspectRatio="xMidYMax meet" href="{poses['greet']}"/>
  <image class="pose pose-present" x="640" y="100" width="360" height="408" preserveAspectRatio="xMidYMax meet" href="{poses['present']}"/>
  <image class="pose pose-think" x="640" y="100" width="360" height="408" preserveAspectRatio="xMidYMax meet" href="{poses['think']}"/>
  <g class="caption-greet"><rect x="652" y="437" width="149" height="38" rx="19" fill="#ffffff" stroke="#dbe2eb"/><text class="sans" x="726.5" y="461" text-anchor="middle" fill="#526376" font-size="14" font-weight="700">你好，很高兴认识你</text></g>
  <g class="caption-present"><rect x="652" y="437" width="149" height="38" rx="19" fill="#ffffff" stroke="#dbe2eb"/><text class="sans" x="726.5" y="461" text-anchor="middle" fill="#526376" font-size="14" font-weight="700">一起看看我的作品</text></g>
  <g class="caption-think"><rect x="652" y="437" width="149" height="38" rx="19" fill="#ffffff" stroke="#dbe2eb"/><text class="sans" x="726.5" y="461" text-anchor="middle" fill="#526376" font-size="14" font-weight="700">从问题开始思考</text></g>
</g>
</svg>'''

OUTPUT.write_text(svg, encoding='utf-8')
print(f'{OUTPUT} ({OUTPUT.stat().st_size:,} bytes)')
