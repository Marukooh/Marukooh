#!/usr/bin/env python3
"""Generate the animated SVG assets for the profile README (palette from the avatar). Usage: assets.py assets/"""
import html
import os
import sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

FONT = "'Segoe UI','Ubuntu','Helvetica Neue',Arial,sans-serif"
MONO = "'JetBrains Mono','Fira Code','Cascadia Code','DejaVu Sans Mono',Consolas,monospace"
PINK, VIOLET, CYAN, TEXT, MUTED, BG, PANEL = "#f05cf0", "#b48cff", "#5ee6f7", "#e6e3ff", "#9d97c9", "#0d0b1e", "#151231"
REDUCED = "@media (prefers-reduced-motion: reduce) { * { animation: none !important } }"


def esc(s):
    return html.escape(s, quote=True)


def write(name, svg):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(svg)


# ---------------------------------------------------------------- divider
write("divider.svg", f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 24" width="1200" height="24">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{PINK}" stop-opacity="0"/>
      <stop offset="0.2" stop-color="{PINK}"/>
      <stop offset="0.8" stop-color="{CYAN}"/>
      <stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="p" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#fff"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <filter id="b"><feGaussianBlur stdDeviation="2"/></filter>
  </defs>
  <rect x="0" y="11" width="1200" height="2" fill="url(#g)"/>
  <rect x="0" y="8" width="160" height="8" fill="url(#p)" filter="url(#b)">
    <animate attributeName="x" from="-200" to="1240" dur="4s" repeatCount="indefinite"/>
  </rect>
  <g fill="{TEXT}" opacity="0.8">
    <polygon points="590,12 600,4 610,12 600,20"><animateTransform attributeName="transform" type="rotate" from="0 600 12" to="360 600 12" dur="10s" repeatCount="indefinite"/></polygon>
  </g>
</svg>
""")


# ---------------------------------------------------------------- section titles
def title(name, label, icon_color):
    w = 1200
    write(name, f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 56" width="{w}" height="56">
  <defs>
    <linearGradient id="t" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{PINK}"/>
      <stop offset="1" stop-color="{CYAN}"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="-0.2 0;0.2 0;-0.2 0" dur="6s" repeatCount="indefinite"/>
    </linearGradient>
    <style>
      .bar {{ animation: grow 1.4s cubic-bezier(.2,.8,.2,1) both; transform-origin: 0 0; }}
      @keyframes grow {{ from {{ transform: scaleX(0) }} to {{ transform: scaleX(1) }} }}
      {REDUCED}
    </style>
  </defs>
  <g transform="skewX(-14) translate(14 0)">
    <rect x="4" y="12" width="10" height="30" fill="{icon_color}"/>
    <rect x="20" y="12" width="5" height="30" fill="{icon_color}" opacity="0.5"/>
  </g>
  <text x="44" y="38" font-family="{FONT}" font-weight="800" font-style="italic" font-size="26" fill="url(#t)" letter-spacing="1">{esc(label)}</text>
  <rect class="bar" x="44" y="48" width="{w - 60}" height="2" fill="url(#t)" opacity="0.5"/>
</svg>
""")


title("title-about.svg", "ABOUT ME", PINK)
title("title-projects.svg", "WHAT I'M BUILDING", VIOLET)
title("title-linux.svg", "LINUX DESKTOP FIXES", CYAN)
title("title-stack.svg", "TECH STACK", PINK)
title("title-playing.svg", "CURRENTLY PLAYING", VIOLET)
title("title-stats.svg", "STATS", CYAN)


# ---------------------------------------------------------------- terminal "about" card with typing lines
lines = [
    ("$ ", "whoami", PINK),
    ("> ", "Maruko · software developer @AlmavivA · Rome, Italy", TEXT),
    ("$ ", "cat ~/.config/interests", PINK),
    ("> ", "C++/Qt · TypeScript · Python · reverse-engineering game bugs", TEXT),
    ("$ ", "uname -a", PINK),
    ("> ", "CachyOS + KDE Plasma 6 (Wayland) · violet glass everywhere", TEXT),
    ("$ ", "echo $MOTTO", PINK),
    ("> ", "if it breaks on Linux, I patch it - then I ship the patch", CYAN),
]
W, H = 1200, 70 + len(lines) * 30
char_w = 10.8
rows = []
t = 0.4
for i, (prompt, txt, color) in enumerate(lines):
    y = 64 + i * 30
    full = len(prompt + txt)
    width = full * char_w + 4
    dur = max(0.5, len(txt) * 0.035)
    rows.append(f"""
  <clipPath id="c{i}"><rect x="28" y="{y - 20}" height="28" width="0">
    <animate attributeName="width" from="0" to="{width:.0f}" begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze" calcMode="discrete" keyTimes="{';'.join(f'{k / full:.3f}' for k in range(full + 1))}" values="{';'.join(f'{k * char_w:.1f}' for k in range(full + 1))}"/>
  </rect></clipPath>
  <text clip-path="url(#c{i})" x="30" y="{y}" font-family="{MONO}" font-size="16" xml:space="preserve"><tspan fill="{VIOLET if prompt.startswith('>') else CYAN}">{esc(prompt)}</tspan><tspan fill="{color}">{esc(txt)}</tspan></text>""")
    t += dur + (0.35 if prompt.startswith("$") else 0.6)
cursor_y = 64 + (len(lines) - 1) * 30
write("about.svg", f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <linearGradient id="border" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{PINK}"/>
      <stop offset="0.5" stop-color="{VIOLET}"/>
      <stop offset="1" stop-color="{CYAN}"/>
    </linearGradient>
    <pattern id="dots" width="6" height="6" patternUnits="userSpaceOnUse"><circle cx="3" cy="3" r="0.9" fill="#8f8cff" fill-opacity="0.12"/></pattern>
    <style>
      .cur {{ animation: blink 1s steps(1) infinite; }}
      @keyframes blink {{ 50% {{ opacity: 0 }} }}
      {REDUCED}
    </style>
  </defs>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="{BG}" stroke="url(#border)" stroke-width="2"/>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="url(#dots)"/>
  <circle cx="26" cy="22" r="6" fill="#ff5f87"/><circle cx="46" cy="22" r="6" fill="#f7c95c"/><circle cx="66" cy="22" r="6" fill="{CYAN}"/>
  <text x="{W / 2}" y="27" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{MUTED}">maruko@cachyos: ~</text>
  {''.join(rows)}
  <rect class="cur" x="{30 + (len(lines[-1][0]) + len(lines[-1][1])) * char_w + 4:.0f}" y="{cursor_y - 15}" width="9" height="18" fill="{PINK}" opacity="0">
    <set attributeName="opacity" to="1" begin="{t:.2f}s"/>
  </rect>
</svg>
""")


# ---------------------------------------------------------------- project cards
def wrap(text, width):
    words, out, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        out.append(cur)
    return out


LANG_COLORS = {"C++": "#f34b7d", "Python": "#3572A5", "TypeScript": "#3178c6", "Vala": "#a56de2", "C": "#555555"}


def card(name, title_text, desc, lang, tag, accent, delay):
    w, h = 590, 186
    lines_ = wrap(desc, 54)[:3]
    desc_svg = "".join(
        f'<text x="26" y="{84 + i * 23}" font-family="{FONT}" font-size="17" fill="{TEXT}" fill-opacity="0.85">{esc(l)}</text>'
        for i, l in enumerate(lines_))
    lc = LANG_COLORS.get(lang, VIOLET)
    write(name, f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{PANEL}"/>
      <stop offset="1" stop-color="{BG}"/>
    </linearGradient>
    <linearGradient id="edge" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{w}" y2="{h}">
      <stop offset="0" stop-color="{PINK}"/>
      <stop offset="0.5" stop-color="{VIOLET}"/>
      <stop offset="1" stop-color="{CYAN}"/>
    </linearGradient>
    <pattern id="dots" width="6" height="6" patternUnits="userSpaceOnUse"><circle cx="3" cy="3" r="0.9" fill="#8f8cff" fill-opacity="0.18"/></pattern>
    <clipPath id="clip"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14"/></clipPath>
    <filter id="blur"><feGaussianBlur stdDeviation="2.5"/></filter>
    <style>
      .run {{ stroke-dasharray: 160 {2 * (w + h)}; animation: run 5s linear infinite; animation-delay: {delay}s; }}
      .in {{ animation: in .9s cubic-bezier(.2,.8,.2,1) both; animation-delay: {delay * 0.15:.2f}s; }}
      @keyframes run {{ from {{ stroke-dashoffset: 0 }} to {{ stroke-dashoffset: -{2 * (w + h)} }} }}
      @keyframes in {{ from {{ opacity: 0; transform: translateX(-10px) }} to {{ opacity: 1; transform: translateX(0) }} }}
      {REDUCED}
    </style>
  </defs>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="url(#bg)" stroke="#2c2756" stroke-width="2"/>
  <g clip-path="url(#clip)">
    <polygon points="{w - 170},0 {w},0 {w},{h} {w - 330},{h}" fill="url(#dots)"/>
    <line x1="{w - 330}" y1="{h}" x2="{w - 170}" y2="0" stroke="{PINK}" stroke-opacity="0.5" stroke-width="2"/>
    <line x1="{w - 300}" y1="{h}" x2="{w - 140}" y2="0" stroke="{CYAN}" stroke-opacity="0.5" stroke-width="3"/>
  </g>
  <rect class="run" x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="none" stroke="url(#edge)" stroke-width="3" filter="url(#blur)"/>
  <rect class="run" x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="none" stroke="url(#edge)" stroke-width="2"/>
  <g class="in">
    <rect x="26" y="26" width="5" height="26" fill="{accent}" transform="skewX(-14)"/>
    <text x="44" y="47" font-family="{FONT}" font-weight="800" font-style="italic" font-size="27" fill="#ffffff">{esc(title_text)}</text>
    {desc_svg}
    <circle cx="32" cy="{h - 24}" r="6" fill="{lc}"/>
    <text x="44" y="{h - 19}" font-family="{FONT}" font-size="16" fill="{MUTED}">{esc(lang)}</text>
    <text x="{w - 26}" y="{h - 19}" text-anchor="end" font-family="{FONT}" font-size="14" font-weight="700" fill="{accent}" letter-spacing="1">{esc(tag.upper())}</text>
  </g>
</svg>
""")


card("card-vkd3d-autopsy.svg", "vkd3d-autopsy",
     "Find out why a D3D12 game hangs the GPU under Proton: breadcrumbs, device faults, NVIDIA diagnostics and VA dumps in one run.",
     "Python", "gpu debugging", CYAN, 0)
card("card-vesktop-patches.svg", "vesktop-patches",
     "Fixes for Vesktop on Linux: sharp Go Live streams, no own-audio bursts while streaming, no venmic crash. Re-applied after updates.",
     "Python", "linux · discord", PINK, 1.2)
card("card-loganalyzer.svg", "LogAnalyzer",
     "Fast native log viewer for huge files: multi-core search, severity and timestamp filters, follow mode, portable builds.",
     "C++", "c++ · qt/qml", VIOLET, 2.4)
card("card-camp-funds.svg", "Camp-Funds-Withdraw",
     "Crimson Desert mod: adds Withdraw Camp Funds to Carl's menu and turns Greymane Camp Funds back into silver.",
     "C++", "game mod", PINK, 0.6)
card("card-wfhelper.svg", "WFHelper",
     "Desktop Warframe companion: inventory, relic reward scanner, warframe.market prices, mastery, foundry and world state.",
     "TypeScript", "svelte · desktop", CYAN, 1.8)
card("card-archons-eye.svg", "Archon's Eye",
     "Elite Dangerous scanner that finds high-value trader and miner traffic systems.",
     "Python", "elite dangerous", VIOLET, 3.0)


# ---------------------------------------------------------------- now playing ticker
games = ["Warframe", "Elite Dangerous", "Crimson Desert", "ACE COMBAT 8", "AION 2", "World of Warcraft"]
sep = "   ◆   "
strip = sep.join(games) + sep
tw = len(strip) * 11.2
write("playing.svg", f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 64" width="1200" height="64">
  <defs>
    <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{BG}"/>
      <stop offset="0.08" stop-color="{BG}" stop-opacity="0"/>
      <stop offset="0.92" stop-color="{BG}" stop-opacity="0"/>
      <stop offset="1" stop-color="{BG}"/>
    </linearGradient>
    <linearGradient id="t" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{PINK}"/>
      <stop offset="0.5" stop-color="{TEXT}"/>
      <stop offset="1" stop-color="{CYAN}"/>
    </linearGradient>
    <clipPath id="c"><rect x="1" y="1" width="1198" height="62" rx="12"/></clipPath>
    <style>
      .roll {{ animation: roll {len(games) * 4}s linear infinite; }}
      @keyframes roll {{ from {{ transform: translateX(0) }} to {{ transform: translateX(-{tw:.0f}px) }} }}
      {REDUCED}
    </style>
  </defs>
  <rect x="1" y="1" width="1198" height="62" rx="12" fill="{BG}" stroke="#2c2756" stroke-width="2"/>
  <g clip-path="url(#c)">
    <g class="roll">
      <text x="20" y="40" font-family="{FONT}" font-weight="800" font-style="italic" font-size="20" fill="url(#t)" xml:space="preserve" letter-spacing="1">{esc((strip * 3).upper())}</text>
    </g>
    <rect width="1200" height="64" fill="url(#fade)"/>
  </g>
</svg>
""")

print("written to", OUT)
