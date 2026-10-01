"""Renders assets/stats-{dark,light}.svg from live GitHub data.

Runs daily in .github/workflows/stats.yml. Locally:

    GITHUB_TOKEN=... python scripts/stats.py
"""
import datetime as dt
import json
import os
import urllib.request

from kit import both, eyebrow, esc, measure, svg, tile

USER = os.environ.get("GH_USER", "ishan-one8")
W = 1200

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 8, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } }
      }
    }
    contributionsCollection {
      contributionCalendar { totalContributions weeks { contributionDays { contributionCount date weekday } } }
    }
  }
}"""


def fetch():
    token = os.environ["GITHUB_TOKEN"]
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        res = json.load(r)
    if "errors" in res:
        raise SystemExit(f"GitHub API error: {res['errors']}")
    u = res["data"]["user"]
    repos = u["repositories"]["nodes"]
    langs = {}
    for repo in repos:
        for e in repo["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    cal = u["contributionsCollection"]["contributionCalendar"]
    weeks = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in cal["weeks"]][-52:]
    calendar = [[(d["date"], d["weekday"], d["contributionCount"]) for d in w["contributionDays"]] for w in cal["weeks"]]
    return dict(
        repos=u["repositories"]["totalCount"],
        stars=sum(r["stargazerCount"] for r in repos),
        followers=u["followers"]["totalCount"],
        contributions=cal["totalContributions"],
        langs=sorted(langs.items(), key=lambda kv: -kv[1]),
        weeks=weeks,
        calendar=calendar,
        active_days=sum(1 for w in calendar for d in w if d[2]),
    )


def smooth(pts):
    """Catmull-Rom through the points, as cubic Béziers that never dip below the baseline."""
    lo, hi = min(p[1] for p in pts), max(p[1] for p in pts)
    clamp = lambda c: (c[0], min(max(c[1], lo), hi))
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(len(pts) - 1):
        p0, p1, p2 = pts[max(i - 1, 0)], pts[i], pts[i + 1]
        p3 = pts[min(i + 2, len(pts) - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        c1, c2 = clamp(c1), clamp(c2)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d


def fmt(n):
    return f"{n / 1000:.1f}k".replace(".0k", "k") if n >= 10000 else f"{n:,}"


def card(data):
    def f(t):
        g = 16
        kw = (W - 3 * g) / 4
        kh = 150
        y2 = kh + g
        bw = (W - g) / 2
        bh = 230
        H = y2 + bh
        parts = []
        second = (("STARS EARNED", data["stars"], "across all repos") if data["stars"] >= 10 else
                  ("ACTIVE DAYS", data["active_days"], "with commits this year"))
        kpis = [("PUBLIC REPOS", data["repos"], "projects shipped"),
                second,
                ("FOLLOWERS", data["followers"], "on GitHub"),
                ("CONTRIBUTIONS", data["contributions"], "in the last year")]
        for i, (label, val, sub) in enumerate(kpis):
            x = i * (kw + g)
            parts.append(tile(t, x, 0, kw, kh, glow=(x + kw, 0, [t["a1"], t["a2"], t["a3"], t["good"]][i])))
            parts.append(eyebrow(t, x + 26, 40, label))
            parts.append(f'<g class="rise" style="animation-delay:{i * .1:.1f}s">'
                         f'<text class="f-sans" x="{x + 24}" y="104" font-size="50" font-weight="600" letter-spacing="-2" fill="url(#headg)">{fmt(val)}</text></g>')
            parts.append(f'<text class="f-sans" x="{x + 26}" y="130" font-size="14" fill="{t["text3"]}">{sub}</text>')

        # languages
        parts.append(tile(t, 0, y2, bw, bh))
        parts.append(eyebrow(t, 26, y2 + 40, "TOP LANGUAGES"))
        top = data["langs"][:5]
        rest = sum(v for _, v in data["langs"][5:])
        if rest:
            top.append(("Other", rest))
        total = sum(v for _, v in top) or 1
        cols = [t["a1"], t["a2"], t["a3"], "#F472B6", "#F59E0B", t["text3"]]
        bx, bwid, by = 26, bw - 52, y2 + 62
        x = bx
        segs = []
        for i, (name, v) in enumerate(top):
            w = bwid * v / total
            segs.append(f'<rect class="grow" style="animation-delay:{i * .08:.2f}s" x="{x:.1f}" y="{by}" width="{max(w - 3, 1.5):.1f}" height="10" rx="3" fill="{cols[i]}"/>')
            x += w
        parts.append(f'<rect x="{bx}" y="{by}" width="{bwid:.1f}" height="10" rx="5" fill="{t["surface2"]}"/>' + "".join(segs))
        for i, (name, v) in enumerate(top):
            cx_ = bx + (i % 2) * (bwid / 2)
            cy_ = by + 52 + (i // 2) * 40
            pct = f"{v / total * 100:.1f}%"
            parts.append(f'<circle cx="{cx_ + 5}" cy="{cy_ - 5}" r="5" fill="{cols[i]}"/>'
                         f'<text class="f-sans" x="{cx_ + 20}" y="{cy_}" font-size="15" font-weight="500" fill="{t["text"]}">{esc(name)}</text>'
                         f'<text class="f-mono" x="{cx_ + bwid / 2 - 30}" y="{cy_}" text-anchor="end" font-size="13" fill="{t["text3"]}">{pct}</text>')
        if not top:
            parts.append(f'<text class="f-sans" x="26" y="{by + 50}" font-size="15" fill="{t["text3"]}">No public code yet.</text>')

        # activity
        ax0 = bw + g
        parts.append(tile(t, ax0, y2, bw, bh, glow=(ax0 + bw, y2 + bh, t["a2"])))
        parts.append(eyebrow(t, ax0 + 26, y2 + 40, "ACTIVITY  ·  LAST 52 WEEKS"))
        weeks = data["weeks"] or [0]
        peak = max(weeks) or 1
        px0, px1, py0, py1 = ax0 + 26, ax0 + bw - 26, y2 + 76, y2 + bh - 34
        n = max(len(weeks) - 1, 1)
        pts = [(px0 + (px1 - px0) * i / n, py1 - (py1 - py0) * v / peak) for i, v in enumerate(weeks)]
        line = smooth(pts)
        area = line + f" L{px1:.1f},{py1:.1f} L{px0:.1f},{py1:.1f} Z"
        pk = max(range(len(weeks)), key=lambda i: weeks[i])
        parts.append(f"""
  <linearGradient id="areag" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{t['a1']}" stop-opacity=".40"/><stop offset="1" stop-color="{t['a1']}" stop-opacity="0"/></linearGradient>
  <path d="M{px0} {py1 + .5}H{px1}" stroke="{t['hair']}" stroke-opacity="{t['hair_op'] * 2:.2f}"/>
  <path d="{area}" fill="url(#areag)"/>
  <path class="draw" d="{line}" stroke="url(#aur)" stroke-width="2.5" stroke-linecap="round" pathLength="100"/>
  <circle cx="{pts[pk][0]:.1f}" cy="{pts[pk][1]:.1f}" r="4.5" fill="{t['text']}"/>
  <circle class="ping" cx="{pts[pk][0]:.1f}" cy="{pts[pk][1]:.1f}" r="4.5" fill="{t['text']}"/>
  <text class="f-mono" x="{px1}" y="{y2 + 40}" text-anchor="end" font-size="11.5" fill="{t['text2']}">PEAK  {peak}/WEEK</text>
  <text class="f-mono" x="{px0}" y="{y2 + bh - 12}" font-size="10.5" letter-spacing="1.5" fill="{t['text3']}">12 MONTHS AGO</text>
  <text class="f-mono" x="{px1}" y="{y2 + bh - 12}" text-anchor="end" font-size="10.5" letter-spacing="1.5" fill="{t['text3']}">THIS WEEK</text>""")

        stamp = dt.datetime.now(dt.timezone.utc).strftime("%d %b %Y").upper()
        css = """
    .rise{animation:rise .9s cubic-bezier(.2,.7,.2,1) both;}
    @keyframes rise{from{opacity:0;transform:translateY(10px);}to{opacity:1;transform:none;}}
    .grow{transform-box:fill-box;transform-origin:left;animation:grow 1s cubic-bezier(.2,.7,.2,1) both;}
    @keyframes grow{from{transform:scaleX(0);}}
    .draw{stroke-dasharray:100;animation:draw 2.4s cubic-bezier(.4,0,.2,1) both;}
    @keyframes draw{from{stroke-dashoffset:100;}to{stroke-dashoffset:0;}}
    .ping{transform-box:fill-box;transform-origin:center;animation:ping 2.4s cubic-bezier(0,0,.2,1) infinite;}
    @keyframes ping{75%,100%{transform:scale(2.6);opacity:0;}}"""
        parts.append(eyebrow(t, W - 4, H + 26, f"SYNCED {stamp}  ·  UPDATES DAILY", "end"))
        langs = ", ".join(f"{n} {v / total * 100:.0f}%" for n, v in top)
        return svg(t, W, H + 34, "".join(parts), "GitHub numbers",
                   f"{data['repos']} public repositories, {second[1]} {second[0].lower()}, {data['followers']} followers and "
                   f"{data['contributions']} contributions in the last year. Top languages: {langs}.", css)
    return f


def streaks(days):
    """Current streak (today may still be empty), longest streak and best day."""
    counts = [c for _, _, c in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    cur, i = 0, len(counts) - 1
    if i >= 0 and counts[i] == 0:
        i -= 1
    while i >= 0 and counts[i]:
        cur, i = cur + 1, i - 1
    best = max(days, key=lambda d: d[2]) if days else ("", 0, 0)
    return cur, longest, best


def heatmap(data):
    def f(t):
        H = 340
        cal = data["calendar"][-53:]
        days = [d for w in cal for d in w]
        cur, longest, best = streaks(days)
        peak = max((c for _, _, c in days), default=0) or 1
        dark = t["bg"] == "#08080A"
        scale = (["#1E1B4B", "#3730A3", "#6366F1", "#A5B4FC"] if dark
                 else ["#C7D2FE", "#A5B4FC", "#6366F1", "#4338CA"])

        def level(c):
            if c == 0:
                return None
            return scale[min(3, int(c / peak * 4 - 1e-9))]

        x0, y0 = 32, 122
        step = (W - 64) / 53
        cell = step - 4.2
        cells, months, last_m, last_wi = [], [], None, -9
        for wi, week in enumerate(cal):
            for date, wd, c in week:
                x, y = x0 + wi * step, y0 + wd * step
                col = level(c)
                fill = (f'fill="{col}"' if col else
                        f'fill="{t["surface2"]}" stroke="{t["hair"]}" stroke-opacity="{t["hair_op"]}"')
                cells.append(f'<rect class="pop" style="animation-delay:{wi * .018 + wd * .02:.3f}s" x="{x:.1f}" y="{y:.1f}" '
                             f'width="{cell:.1f}" height="{cell:.1f}" rx="4" {fill}/>')
            m = week[0][0][5:7]
            if m != last_m and wi < 51:
                if wi - last_wi < 3 and months:
                    months.pop()  # a sliver of the previous month: label the new one instead
                months.append(f'<text class="f-mono" x="{x0 + wi * step:.1f}" y="{y0 - 14}" font-size="11" fill="{t["text3"]}">'
                              f'{dt.date(2000, int(m), 1).strftime("%b").upper()}</text>')
                last_m, last_wi = m, wi
        bd = dt.date.fromisoformat(best[0]).strftime("%d %b").upper() if best[0] else "—"
        kpis = [("CURRENT STREAK", f"{cur} day{'s' * (cur != 1)}"), ("LONGEST STREAK", f"{longest} day{'s' * (longest != 1)}"),
                ("BEST DAY", f"{best[2]} · {bd}")]
        ks, kx = [], W - 32
        for label, val in reversed(kpis):
            w = max(measure(val, 22, weight=600, spacing=-.6), measure(label, 11.5, "mono", 2))
            ks.append(eyebrow(t, kx, 44, label, "end") +
                      f'<text class="f-sans" x="{kx}" y="76" text-anchor="end" font-size="22" font-weight="600" letter-spacing="-.6" fill="{t["text"]}">{esc(val)}</text>')
            kx -= w + 40
        legend_x = W - 32 - 5 * 18 - 40
        legend = [f'<text class="f-mono" x="{legend_x - 10}" y="{H - 30}" text-anchor="end" font-size="11" fill="{t["text3"]}">LESS</text>']
        for i, col in enumerate([None] + scale):
            fill = f'fill="{col}"' if col else f'fill="{t["surface2"]}" stroke="{t["hair"]}" stroke-opacity="{t["hair_op"]}"'
            legend.append(f'<rect x="{legend_x + i * 18}" y="{H - 42}" width="14" height="14" rx="3.5" {fill}/>')
        legend.append(f'<text class="f-mono" x="{legend_x + 5 * 18 + 4}" y="{H - 30}" font-size="11" fill="{t["text3"]}">MORE</text>')
        total = sum(c for _, _, c in days)
        body = f"""
  {tile(t, 0, 0, W, H, glow=(W, 0, t['a1']))}
  {eyebrow(t, 32, 44, "CONTRIBUTIONS")}
  <text class="f-sans" x="32" y="80" font-size="30" font-weight="600" letter-spacing="-1" fill="url(#headg)">{total:,}<tspan class="f-serif" font-size="30" font-weight="400" letter-spacing="0" fill="{t['text2']}"> in the last year</tspan></text>
  {''.join(ks)}
  {''.join(months)}
  {''.join(cells)}
  {''.join(legend)}
  <text class="f-mono" x="32" y="{H - 30}" font-size="11" letter-spacing="1.5" fill="{t['text3']}">ONE SQUARE = ONE DAY  ·  UPDATES DAILY</text>"""
        css = """
    .pop{transform-box:fill-box;transform-origin:center;animation:pop .5s cubic-bezier(.2,.7,.2,1) both;}
    @keyframes pop{from{transform:scale(.2);opacity:0;}}"""
        return svg(t, W, H, body, "Contribution activity",
                   f"{total} contributions in the last year. Current streak {cur} days, longest streak {longest} days, "
                   f"best day {best[2]} contributions.", css)
    return f


if __name__ == "__main__":
    data = fetch()
    print(json.dumps({k: v for k, v in data.items() if k not in ("weeks", "calendar")}, indent=1))
    both("stats", card(data))
    both("activity", heatmap(data))
