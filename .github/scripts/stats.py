#!/usr/bin/env python3
"""Render assets/stats.svg (profile stats + top languages) in the profile's style.

Runs in GitHub Actions with GITHUB_TOKEN; only public data is used. Standard library only.
    GITHUB_TOKEN=... python3 .github/scripts/stats.py <login> <output.svg>
"""
import html
import json
import os
import sys
import urllib.request

LOGIN = sys.argv[1]
OUT = sys.argv[2]

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection { contributionCalendar { totalContributions } }
    followers { totalCount }
    pullRequests { totalCount }
    issues { totalCount }
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false, first: 100) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name color } } }
      }
    }
  }
}
"""


def query():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": "bearer " + os.environ["GITHUB_TOKEN"], "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    if "errors" in data:
        sys.exit(json.dumps(data["errors"], indent=2))
    return data["data"]["user"]


def main():
    u = query()
    repos = u["repositories"]["nodes"]
    stars = sum(r["stargazerCount"] for r in repos)
    langs = {}
    colors = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]
            langs[n] = langs.get(n, 0) + e["size"]
            colors[n] = e["node"]["color"] or "#b48cff"
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:6]
    total = sum(v for _, v in top) or 1

    stats = [
        ("Contributions (last year)", u["contributionsCollection"]["contributionCalendar"]["totalContributions"], "#f05cf0"),
        ("Public repositories", u["repositories"]["totalCount"], "#b48cff"),
        ("Stars earned", stars, "#5ee6f7"),
        ("Pull requests", u["pullRequests"]["totalCount"], "#f05cf0"),
        ("Issues opened", u["issues"]["totalCount"], "#b48cff"),
    ]

    font = "'Segoe UI','Ubuntu','Helvetica Neue',Arial,sans-serif"
    w, h = 1200, 260
    rows = []
    for i, (label, value, color) in enumerate(stats):
        y = 70 + i * 38
        rows.append(
            f'<g class="in" style="animation-delay:{0.15 * i:.2f}s">'
            f'<rect x="0" y="0" width="5" height="18" fill="{color}" transform="translate(44 {y - 14}) skewX(-14)"/>'
            f'<text x="60" y="{y}" font-family="{font}" font-size="18" fill="#e6e3ff" fill-opacity="0.85">{html.escape(label)}</text>'
            f'<text x="540" y="{y}" text-anchor="end" font-family="{font}" font-size="20" font-weight="800" font-style="italic" fill="{color}">{value}</text>'
            f"</g>")

    bar = []
    legend = []
    x = 640.0
    bar_w = 520.0
    for i, (name, size) in enumerate(top):
        seg = bar_w * size / total
        bar.append(f'<rect x="{x:.1f}" y="70" width="{seg:.1f}" height="14" fill="{colors[name]}"/>')
        x += seg
        lx = 640 + (i % 2) * 270
        ly = 124 + (i // 2) * 36
        pct = 100.0 * size / total
        legend.append(
            f'<g class="in" style="animation-delay:{0.3 + 0.12 * i:.2f}s">'
            f'<circle cx="{lx + 7}" cy="{ly - 6}" r="7" fill="{colors[name]}"/>'
            f'<text x="{lx + 22}" y="{ly}" font-family="{font}" font-size="17" fill="#e6e3ff">{html.escape(name)}</text>'
            f'<text x="{lx + 250}" y="{ly}" text-anchor="end" font-family="{font}" font-size="17" fill="#9d97c9">{pct:.1f}%</text>'
            f"</g>")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#f05cf0"/><stop offset="0.5" stop-color="#b48cff"/><stop offset="1" stop-color="#5ee6f7"/>
    </linearGradient>
    <pattern id="dots" width="6" height="6" patternUnits="userSpaceOnUse"><circle cx="3" cy="3" r="0.9" fill="#8f8cff" fill-opacity="0.12"/></pattern>
    <clipPath id="barclip"><rect x="640" y="70" width="{bar_w}" height="14" rx="7"/></clipPath>
    <style>
      .in {{ animation: in .8s cubic-bezier(.2,.8,.2,1) both; }}
      .grow {{ animation: grow 1.6s cubic-bezier(.2,.8,.2,1) both; transform-origin: 640px 0; }}
      @keyframes in {{ from {{ opacity: 0; transform: translateX(-8px) }} to {{ opacity: 1; transform: none }} }}
      @keyframes grow {{ from {{ transform: scaleX(0) }} to {{ transform: scaleX(1) }} }}
      @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important }} }}
    </style>
  </defs>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="#0d0b1e" stroke="url(#edge)" stroke-width="2"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="url(#dots)"/>
  <line x1="600" y1="30" x2="580" y2="{h - 30}" stroke="#2c2756" stroke-width="2"/>
  <text x="40" y="36" font-family="{font}" font-size="15" font-weight="700" fill="#9d97c9" letter-spacing="2">GITHUB</text>
  <text x="640" y="50" font-family="{font}" font-size="15" font-weight="700" fill="#9d97c9" letter-spacing="2">TOP LANGUAGES</text>
  {''.join(rows)}
  <rect x="640" y="70" width="{bar_w}" height="14" rx="7" fill="#151231"/>
  <g clip-path="url(#barclip)"><g class="grow">{''.join(bar)}</g></g>
  {''.join(legend)}
</svg>
"""
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"wrote {OUT}: {stats}, top languages {top}")


if __name__ == "__main__":
    main()
