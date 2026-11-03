#!/usr/bin/env python3
"""Pod recap dashboard: writes extra/pod-dashboard/dashboard.html from calls.csv.

Usage:
    python3 extra/pod-dashboard/dashboard.py                    # 60-minute threshold, whole log
    python3 extra/pod-dashboard/dashboard.py 15                 # any other threshold, in minutes
    python3 extra/pod-dashboard/dashboard.py --from 2026-09-21 --to 2026-09-24

Each run rebuilds dashboard.html for the dates given (no dates = the whole log) with the
same layout, and prints everything the page shows as text: first the per-pod table in
b1_metrics.py's format (so the two can be diffed), then recorded calls with no recap, the
gap to the 80% target, capture x speed, agent vs AM medians, weekly share and the
adoption.csv comparison. Never edit the HTML by hand: this script is the only thing that writes it.

Every count and share comes from scripts/b1_metrics.py (load_calls, summarise, by_pod),
so this page and B1 can't disagree. The page is one self-contained HTML file: inline
CSS, SVG and a few lines of JS for tooltips; no external libraries or fonts.
Standard library only.
"""
import argparse
import csv
import html
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.dont_write_bytecode = True          # keep scripts/ free of __pycache__
sys.path.insert(0, str(ROOT / "scripts"))
from b1_metrics import (DASHBOARD_MINUTES, by_pod, fmt_median, iso_date,  # noqa: E402
                        load_calls, pct, summarise)

TARGET = 0.80                           # INSTRUCTIONS.md:40, brain/NOW.md:10
OUT = HERE / "dashboard.html"
esc = html.escape


def tip(value, label):
    """Attributes for the hover/focus tooltip (value first, label second)."""
    return f'tabindex="0" data-v="{esc(value)}" data-l="{esc(label)}"'


def width(x):
    return f"{0 if x is None else min(x, 1) * 100:.1f}%"


def tick_row(ticks):
    """Axis labels placed at their exact position along the track: [(fraction, label), ...]."""
    return '<span class="tk">' + "".join(f'<span style="left:{f:.4%}">{t}</span>' for f, t in ticks) + "</span>"


def icon(kind):
    fill, ink = {"warn": ("var(--warn)", "#0b0b0b"), "serious": ("var(--serious)", "#ffffff")}[kind]
    return (f'<svg class="icon" viewBox="0 0 16 16" aria-hidden="true"><path d="M8 1.5 15 14.5H1z" fill="{fill}"/>'
            f'<path d="M8 6v4.2M8 12v.6" stroke="{ink}" stroke-width="1.6" stroke-linecap="round"/></svg>')


def week_label(a, b):
    if a == b:
        return f"{a.day} {a:%b}"
    return f"{a.day}–{b.day} {b:%b}" if a.month == b.month else f"{a.day} {a:%b}–{b.day} {b:%b}"


def weeks(rows):
    """Monday-start weeks, clipped to the first and last call date in rows."""
    first, last = (date.fromisoformat(f(r["date"] for r in rows)) for f in (min, max))
    monday = first - timedelta(days=first.weekday())
    out = []
    while monday <= last:
        a, b = max(monday, first), min(monday + timedelta(days=6), last)
        out.append((week_label(a, b), [r for r in rows if a.isoformat() <= r["date"] <= b.isoformat()]))
        monday += timedelta(days=7)
    return out


def adoption_status(pod, adoption, full_log):
    """('range' | 'missing' | 'match' | 'differ', adoption.csv share, calls.csv share at 60 min)."""
    if not full_log:
        return "range", None, None
    d, log60 = adoption.get(pod), summarise(PODS[pod], DASHBOARD_MINUTES)["share"]
    if d is None:
        return "missing", None, log60
    dash = float(d["share_of_calls_with_recap_within_1hr"].rstrip("%")) / 100
    return ("match" if log60 is not None and round(dash, 2) == round(log60, 2) else "differ"), dash, log60


def ratios(s):
    """(capture, speed): recorded / held and within / recorded, from summarise's counts."""
    return (s["recorded"] / s["held"] if s["held"] else None,
            s["within"] / s["recorded"] if s["recorded"] else None)


def gap(s):
    """On-time recaps still needed to reach the target share of calls held."""
    return max(0, -(-round(TARGET * 100) * s["held"] // 100) - s["within"])


def medians(pod):
    """{who: (median minutes or None, label)} over every posted recap, label as B1 prints it."""
    out = {}
    for who in ("agent", "AM"):
        vals = [r["minutes"] for r in PODS[pod] if r["minutes"] is not None and r["posted_by"] == who]
        out[who] = (statistics.median(vals), fmt_median(vals)) if vals else (None, "none posted")
    return out


def weekly(order, all_rows, minutes, sel):
    """Weeks across the whole log, which of them overlap the chosen dates, and each pod's series."""
    wk = weeks(all_rows)
    on = [bool(sel) and any(sel[0] <= r["date"] <= sel[1] for r in part) for _, part in wk]
    series = {pod: [(lab, summarise([r for r in part if r["pod"] == pod], minutes)) for lab, part in wk]
              for pod in order}
    return wk, on, series


def section_share(order, stats, total, adoption, minutes, full_log):
    rows = []
    for pod in order + ["All pods"]:
        s = total if pod == "All pods" else stats[pod]
        n = f"{s['within']} of {s['held']} calls held"
        adopt = ""
        if pod != "All pods":
            kind, dash, log60 = adoption_status(pod, adoption, full_log)
            at = "" if minutes == DASHBOARD_MINUTES else f" at {DASHBOARD_MINUTES} min"
            if kind == "range":
                adopt = '<span class="adopt">adoption.csv: whole log only, not compared for these dates</span>'
            elif kind == "missing":
                adopt = f'<span class="adopt">{icon("warn")} Not in adoption.csv</span>'
            elif kind == "match":
                adopt = f'<span class="adopt">adoption.csv: {pct(dash)}, matches{at}</span>'
            else:
                adopt = (f'<span class="adopt flag">{icon("warn")} <b>Differs:</b> adoption.csv says {pct(dash)};'
                         f' calls.csv gives {pct(log60)}{at}</span>')
        rows.append(f"""
<div class="brow{' total' if pod == 'All pods' else ''}" {tip(pct(s['share']), f'{pod}: {n}')}>
  <span class="name">{esc(pod)}</span>
  <span class="track"><span class="fill" style="width:{width(s['share'])}"></span><span class="target" style="left:{TARGET:.0%}"></span></span>
  <span class="val">{pct(s['share'])}</span>
  <span class="meta">{s['held']} held · {s['recorded']} recorded · {s['posted']} posted · {s['within']} within {minutes} min</span>
  {adopt}
</div>""")
    note = f"adoption.csv is defined at {DASHBOARD_MINUTES} min." if minutes != DASHBOARD_MINUTES else ""
    return f"""
<section class="card"><h2>1. Recap within {minutes} min, by pod</h2>
<p class="sub">Share of calls held with a recap posted within {minutes} min of call end. Line: {TARGET:.0%} target. {note}</p>
<div class="bars">
<div class="axis-top"><span></span><span class="lab"><span style="left:{TARGET:.0%}">{TARGET:.0%} target</span></span><span></span></div>
{''.join(rows)}
<div class="axis"><span></span>{tick_row([(v / 100, f"{v}%") for v in (0, 25, 50, 75, 100)])}<span></span></div>
</div></section>"""


def section_split(order, stats, minutes):
    def cell(x, num, den, what, unit):
        frac = f"{num}/{den}" if den else f"0 {unit}"
        return f'<td {tip(pct(x), f"{pod} {what}: {frac}")}><span class="num">{pct(x)}</span> <small>{frac}</small><span class="meter"><span style="width:{width(x)}"></span></span></td>'
    body = ""
    for pod in order:
        s = stats[pod]
        capture, speed = ratios(s)
        body += (f"<tr><th>{esc(pod)}</th>{cell(capture, s['recorded'], s['held'], 'capture', 'held')}"
                 f"{cell(speed, s['within'], s['recorded'], 'speed', 'recorded')}<td class=\"share\">{pct(s['share'])}</td></tr>")
    return f"""
<section class="card"><h2>2. Capture × speed</h2>
<p class="sub">Capture = recorded ÷ held. Speed = within {minutes} min ÷ recorded. Their product is the share in section 1.</p>
<table class="split"><thead><tr><th>Pod</th><th>Capture</th><th>× Speed</th><th>= Share</th></tr></thead>
<tbody>{body}</tbody></table></section>"""


def section_medians(order, minutes):
    meds = {(pod, who): v for pod in order for who, v in medians(pod).items()}
    top = max([m for m, _ in meds.values() if m is not None] + [minutes])
    top = -(-top // 30) * 30 or 30
    steps = list(range(0, int(top) + 1, 30))
    ticks = tick_row([(t / top, f"{t} min" if t == steps[-1] else str(t)) for t in steps])
    grid = f"background-size:{30 / top:.4%} 100%"
    groups = ""
    for pod in order:
        bars = ""
        for who, cls in (("agent", "s1"), ("AM", "s2")):
            m, label = meds[pod, who]
            bars += f"""
  <div class="mrow" {tip(label, f'{pod}, median minutes to post, {who}')}>
    <span class="track" style="{grid}"><span class="fill {cls}" style="width:{width(None if m is None else m / top)}"></span><span class="target" style="left:{minutes / top:.1%}"></span></span>
    <span class="mval{' none' if m is None else ''}">{esc(label)}</span>
  </div>"""
        groups += f'<div class="mgroup"><div class="mname">{esc(pod)}</div>{bars}</div>'
    return f"""
<section class="card"><h2>3. Median minutes to post, agent vs AM</h2>
<p class="sub">From call end to recap, over every posted recap. Line: the {minutes}-min threshold.</p>
<div class="legend"><span class="key s1"></span>Agent <span class="key s2"></span>AM</div>
<div class="axis-top m"><span class="lab"><span style="left:{minutes / top:.1%}">{minutes} min</span></span><span></span></div>
{groups}
<div class="axis m">{ticks}<span></span></div>
</section>"""


def spark(pod, series, selected):
    x0, x1, yt, yb = 40, 270, 14, 118
    xs = [x0 + i * (x1 - x0) / max(len(series) - 1, 1) for i in range(len(series))] if len(series) > 1 else [(x0 + x1) / 2]
    y = lambda v: yb - v * (yb - yt)
    half = (x1 - x0) / max(len(series) - 1, 1) / 2
    out = [f'<rect x="{x - half:.1f}" y="{yt - 6}" width="{2 * half:.1f}" height="{yb - yt + 12}" class="sel"/>'
           for x, on in zip(xs, selected) if on]
    out += [f'<line x1="{x0}" x2="{x1}" y1="{y(v):.1f}" y2="{y(v):.1f}" class="{"base" if v == 0 else "grid"}"/>'
           f'<text x="{x0 - 6}" y="{y(v) + 3.5:.1f}" class="yl" text-anchor="end">{v:.0%}</text>' for v in (0, 0.5, 1)]
    out.append(f'<line x1="{x0}" x2="{x1}" y1="{y(TARGET):.1f}" y2="{y(TARGET):.1f}" class="tline"/>'
               f'<text x="{x0 - 6}" y="{y(TARGET) + 3.5:.1f}" class="yl t" text-anchor="end">{TARGET:.0%}</text>')
    pts = [(x, y(s["share"]), lab, s) for x, (lab, s) in zip(xs, series) if s["share"] is not None]
    path, prev = "", None
    for x, (lab, s) in zip(xs, series):
        if s["share"] is None:
            prev = None
            continue
        path += f"{'L' if prev else 'M'}{x:.1f},{y(s['share']):.1f}"
        prev = x
    out.append(f'<path d="{path}" class="line"/>')
    for x, (lab, _) in zip(xs, series):
        out.append(f'<text x="{x:.1f}" y="138" class="xl" text-anchor="middle">{esc(lab)}</text>')
    for x, yy, lab, s in pts:
        out.append(f'<g class="pt" {tip(pct(s["share"]), f"{pod}, {lab}: {s["within"]} of {s["held"]} calls held")}>'
                   f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="12" class="hit"/><circle cx="{x:.1f}" cy="{yy:.1f}" r="4" class="dot"/></g>')
    if pts:
        x, yy, _, s = pts[-1]
        out.append(f'<text x="{x + 9:.1f}" y="{yy + 4:.1f}" class="end">{pct(s["share"])}</text>')
    summary = ", ".join(f"{lab} {pct(s['share'])}" for lab, s in series)
    return (f'<figure class="spark"><figcaption>{esc(pod)}</figcaption><svg viewBox="0 0 320 146" role="img" '
            f'aria-label="{esc(pod)} weekly share: {esc(summary)}">{"".join(out)}</svg></figure>')


def section_weekly(order, all_rows, minutes, sel):
    """Always the whole log, so the layout never changes; weeks overlapping the chosen dates are shaded."""
    wk, on, by = weekly(order, all_rows, minutes, sel)
    charts, trs = "", ""
    for pod in order:
        series = by[pod]
        charts += spark(pod, series, on)
        trs += f"<tr><th>{esc(pod)}</th>" + "".join(
            f"<td>{pct(s['share'])} <small>{s['within']}/{s['held']}</small></td>" for _, s in series) + "</tr>"
    head = "".join(f'<th{" class=sel" if o else ""}>{esc(lab)}</th>' for (lab, _), o in zip(wk, on))
    first, last = min(r["date"] for r in all_rows), max(r["date"] for r in all_rows)
    shade = f" Shaded: weeks that include {sel[0]} to {sel[1]} (each point is the full week)." if sel else ""
    return f"""
<section class="card"><h2>4. Weekly share, by pod</h2>
<p class="sub">Recap within {minutes} min ÷ calls held, per Monday-start week, across the whole log ({first} to {last}). Line: {TARGET:.0%} target.{shade}</p>
<div class="sparks">{charts}</div>
<details><summary>Table</summary><div class="scroll"><table class="wk"><thead><tr><th>Pod</th>{head}</tr></thead><tbody>{trs}</tbody></table></div></details>
</section>"""


def section_alerts(rows):
    hits = sorted((r for r in rows if r["recorded"] and r["minutes"] is None), key=lambda r: (r["date"], r["call_id"]))
    if not hits:
        body = '<p class="sub">None: every recorded call has a recap.</p>'
    else:
        trs = "".join(f"<tr><td>{esc(r['call_id'])}</td><td>{esc(r['pod'])}</td><td>{esc(r['account'])}</td><td>{esc(r['date'])}</td></tr>"
                      for r in hits)
        body = (f'<p class="alert">{icon("serious")} <b>{len(hits)} recorded call{"s" if len(hits) != 1 else ""} with no recap</b></p>'
                f'<table class="alerts"><thead><tr><th>Call</th><th>Pod</th><th>Account</th><th>Date</th></tr></thead><tbody>{trs}</tbody></table>')
    return f'<section class="card"><h2>5. Alerts: recorded calls with no recap</h2>{body}</section>'


CSS = """
:root{color-scheme:light;--page:#f9f9f7;--surface:#fcfcfb;--ink:#0b0b0b;--ink-2:#52514e;--muted:#898781;
--grid:#e1e0d9;--axis:#c3c2b7;--border:rgba(11,11,11,.10);--s1:#2a78d6;--s2:#eb6834;--track:#cde2fb;
--warn:#fab219;--serious:#ec835a;--flag-bg:#fff6e0}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){color-scheme:dark;--page:#0d0d0d;--surface:#1a1a19;
--ink:#f0efec;--ink-2:#c3c2b7;--grid:#2c2c2a;--axis:#383835;--border:rgba(255,255,255,.10);--s1:#3987e5;--s2:#d95926;
--track:#0d366b;--flag-bg:#2e2512}}
:root[data-theme="dark"]{color-scheme:dark;--page:#0d0d0d;--surface:#1a1a19;--ink:#f0efec;--ink-2:#c3c2b7;--grid:#2c2c2a;
--axis:#383835;--border:rgba(255,255,255,.10);--s1:#3987e5;--s2:#d95926;--track:#0d366b;--flag-bg:#2e2512}
*{box-sizing:border-box}
body{margin:0;background:var(--page);color:var(--ink);font:15px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:780px;margin:0 auto;padding:24px 16px 48px}
h1{font-size:22px;margin:0 0 4px}h2{font-size:16px;margin:0 0 4px}
.lede{color:var(--ink-2);margin:0 0 20px;font-size:14px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:16px;margin:0 0 16px}
.sub{color:var(--ink-2);font-size:13px;margin:0 0 14px}
.track{position:relative;height:16px;border-left:1px solid var(--axis);border-right:1px solid var(--grid);
background-image:linear-gradient(to right,var(--grid) 1px,transparent 1px);background-size:25% 100%}
.fill{position:absolute;left:0;top:0;bottom:0;border-radius:0 4px 4px 0;background:var(--s1)}
.fill.s2{background:var(--s2)}
.target{position:absolute;top:-5px;bottom:-5px;width:2px;margin-left:-1px;background:var(--ink-2)}
.brow,.axis,.axis-top{display:grid;grid-template-columns:4.6rem 1fr 3rem;column-gap:10px;align-items:center}
.brow{row-gap:3px;padding:8px 0;border-radius:6px}
.brow.total{border-top:1px solid var(--grid);margin-top:4px;padding-top:12px}
.name{font-weight:600}.val{font-weight:600;text-align:right;font-variant-numeric:tabular-nums}
.meta,.adopt{grid-column:2/4;font-size:13px;color:var(--ink-2)}
.adopt.flag{color:var(--ink);background:var(--flag-bg);border-radius:6px;padding:2px 6px;justify-self:start}
.icon{width:14px;height:14px;vertical-align:-2px}
.lab{position:relative;height:18px;font-size:12px;color:var(--ink-2)}
.lab span{position:absolute;transform:translateX(-50%);white-space:nowrap}
.tk{position:relative;height:16px;font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums}
.tk span{position:absolute;transform:translateX(-50%);white-space:nowrap}
.axis{margin-top:6px}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{text-align:left;padding:8px 6px;border-bottom:1px solid var(--grid);vertical-align:top}
thead th{font-size:12px;color:var(--ink-2);font-weight:600}
td{font-variant-numeric:tabular-nums}td small{color:var(--ink-2)}
.num{font-weight:600}.split td.share{font-weight:600}
.meter{display:block;height:6px;border-radius:3px;background:var(--track);margin-top:6px;overflow:hidden}
.meter span{display:block;height:100%;background:var(--s1);border-radius:3px}
.legend{display:flex;gap:14px;align-items:center;font-size:13px;color:var(--ink-2);margin:0 0 8px}
.key{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:-8px}
.key.s1{background:var(--s1)}.key.s2{background:var(--s2)}
.axis-top.m,.axis.m{grid-template-columns:1fr 8rem}
.mgroup{padding:6px 0}.mname{font-weight:600;font-size:14px;margin-bottom:4px}
.mrow{display:grid;grid-template-columns:1fr 8rem;column-gap:10px;align-items:center;margin-bottom:2px;border-radius:4px}
.mrow .track{height:12px}.mrow .target{top:-3px;bottom:-3px}
.mval{font-size:13px;font-variant-numeric:tabular-nums}.mval.none{color:var(--muted)}
.sparks{display:grid;grid-template-columns:1fr;gap:8px}
@media (min-width:640px){.sparks{grid-template-columns:1fr 1fr}}
.spark{margin:0}.spark figcaption{font-weight:600;font-size:14px}
.spark svg{display:block;width:100%;max-width:420px;height:auto;overflow:visible}
.spark .sel{fill:var(--s1);opacity:.08}.wk th.sel{color:var(--ink)}
.spark .grid{stroke:var(--grid);stroke-width:1}.spark .base{stroke:var(--axis);stroke-width:1}
.spark .tline{stroke:var(--ink-2);stroke-width:1}
.spark .line{fill:none;stroke:var(--s1);stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.spark .dot{fill:var(--s1);stroke:var(--surface);stroke-width:2}.spark .hit{fill:transparent}
.spark text{font-size:11px;fill:var(--muted)}.spark .yl.t{fill:var(--ink-2);font-weight:600}
.spark .xl{fill:var(--ink-2)}.spark .end{fill:var(--ink);font-weight:600;font-size:12px}
details{margin-top:10px;font-size:14px}summary{cursor:pointer;color:var(--ink-2)}
.scroll{overflow-x:auto}.wk td{white-space:nowrap}
.alert{margin:0 0 8px}
[data-v]{outline:none;cursor:default}
.brow:hover,.brow:focus-visible,.mrow:hover,.mrow:focus-visible,td[data-v]:hover,td[data-v]:focus-visible{background:var(--page)}
.pt:hover .dot,.pt:focus .dot{r:5.5;stroke:var(--ink)}
#tip{position:fixed;z-index:9;pointer-events:none;background:var(--surface);color:var(--ink);border:1px solid var(--border);
border-radius:8px;padding:6px 10px;font-size:13px;box-shadow:0 4px 16px rgba(0,0,0,.18);max-width:260px}
#tip strong{display:block;font-size:15px}#tip span{color:var(--ink-2)}
.foot{color:var(--muted);font-size:12px}
"""

JS = """
const tip=document.getElementById('tip');
function show(e){const t=e.currentTarget,v=document.createElement('strong'),l=document.createElement('span');
v.textContent=t.dataset.v;l.textContent=t.dataset.l;tip.replaceChildren(v,l);tip.hidden=false;
let x,y;if(e.type==='focus'){const r=t.getBoundingClientRect();x=r.left+r.width/2;y=r.top}else{x=e.clientX;y=e.clientY}
const w=tip.offsetWidth,h=tip.offsetHeight;tip.style.left=Math.min(Math.max(8,x-w/2),innerWidth-w-8)+'px';
tip.style.top=(y-h-12<8?y+20:y-h-12)+'px'}
function hide(){tip.hidden=true}
document.querySelectorAll('[data-v]').forEach(el=>{el.addEventListener('pointermove',show);el.addEventListener('focus',show);
el.addEventListener('pointerleave',hide);el.addEventListener('blur',hide)});
"""


def print_summary(order, stats, rows, all_rows, adoption, minutes, full_log, filt):
    """Everything the page shows, as text: the per-pod table first, in b1_metrics.py's layout so it can be diffed."""
    first, last = min(r["date"] for r in rows), max(r["date"] for r in rows)
    total = summarise(rows, minutes)
    print(f"{len(rows)} calls, {first} to {last}{filt}")
    hdr = f"{'pod':<7}{'held':>6}{'recorded':>10}{'posted':>8}{'within':>8}{'share':>8}"
    print(hdr + "\n" + "-" * len(hdr))
    for pod, s in [(p, stats[p]) for p in order] + [("All", total)]:
        print(f"{pod:<7}{s['held']:>6}{s['recorded']:>10}{s['posted']:>8}{s['within']:>8}{pct(s['share']):>8}")
    hits = sorted((r for r in rows if r["recorded"] and r["minutes"] is None), key=lambda r: (r["date"], r["call_id"]))
    print("Recorded calls with no recap: " + (", ".join(
        f"{r['call_id']} ({r['pod']}, {r['account']}, {r['date']})" for r in hits) or "none"))

    print(f"\nOn-time recaps still needed to reach {TARGET:.0%}: "
          + ", ".join(f"{p} {gap(s)}" for p, s in [(p, stats[p]) for p in order] + [("All", total)]))
    print(f"\nCapture (recorded / held) x speed (within {minutes} min / recorded):")
    for pod in order:
        s, (capture, speed) = stats[pod], ratios(stats[pod])
        cap = f"{s['recorded']}/{s['held']} = {pct(capture)}" if s["held"] else "n/a (0 held)"
        spd = f"{s['within']}/{s['recorded']} = {pct(speed)}" if s["recorded"] else "n/a (0 recorded)"
        print(f"  {pod:<7}capture {cap:<16} speed {spd}")
    print("\nMedian minutes from call end to recap (agent | AM):")
    for pod in order:
        m = medians(pod)
        print(f"  {pod:<7}{m['agent'][1]:<16}| {m['AM'][1]}")
    sel = None if full_log else (first, last)
    wk, on, by = weekly(order, all_rows, minutes, sel)
    print("\nWeekly share, whole log" + (" (* = week includes the chosen dates)" if sel else "") + ":")
    for pod in order:
        print(f"  {pod:<7}" + " · ".join(f"{lab}{'*' if o else ''} {pct(s['share'])} ({s['within']}/{s['held']})"
                                         for (lab, s), o in zip(by[pod], on)))
    if not full_log:
        print("\nadoption.csv: whole log only, not compared for these dates")
    else:
        parts = []
        for pod in order:
            kind, dash, log60 = adoption_status(pod, adoption, full_log)
            parts.append(f"{pod} missing" if kind == "missing" else f"{pod} matches ({pct(dash)})" if kind == "match"
                         else f"{pod} DIFFERS: adoption.csv {pct(dash)}, calls.csv {pct(log60)}")
        print(f"\nadoption.csv vs calls.csv at {DASHBOARD_MINUTES} min: " + "; ".join(parts))


def main():
    global PODS
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("minutes", nargs="?", type=float, default=60, help="threshold in minutes after call_end (default 60)")
    ap.add_argument("--from", dest="date_from", type=iso_date, metavar="YYYY-MM-DD")
    ap.add_argument("--to", dest="date_to", type=iso_date, metavar="YYYY-MM-DD")
    args = ap.parse_args()
    if args.date_from and args.date_to and args.date_from > args.date_to:
        ap.error(f"--from {args.date_from} is after --to {args.date_to}")
    minutes = int(args.minutes) if args.minutes.is_integer() else args.minutes

    all_rows = load_calls(ROOT / "calls.csv")
    rows = [r for r in all_rows if (not args.date_from or r["date"] >= args.date_from)
            and (not args.date_to or r["date"] <= args.date_to)]
    if not rows:
        sys.exit("No calls in calls.csv for that date filter.")
    PODS = by_pod(rows)
    stats = {pod: summarise(part, minutes) for pod, part in PODS.items()}
    order = sorted(PODS, key=lambda p: stats[p]["share"] or 0, reverse=True)    # B1's ranking
    full_log = len(rows) == len(all_rows)
    with open(ROOT / "adoption.csv", newline="") as f:
        adoption = {r["pod"]: r for r in csv.DictReader(f)}
    first, last = min(r["date"] for r in rows), max(r["date"] for r in rows)
    filt = f" (filter: {args.date_from or 'start'} to {args.date_to or 'end'})" if not full_log else ""

    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pod recap dashboard</title><style>{CSS}</style></head>
<body><main>
<h1>Recaps by pod</h1>
<p class="lede">{len(rows)} calls held, {first} to {last}{esc(filt)}. A recap counts if posted within {minutes} min of call end.
Target: {TARGET:.0%} in every pod by 31 Oct. Built from <code>calls.csv</code> with <code>scripts/b1_metrics.py</code>.</p>
{section_share(order, stats, summarise(rows, minutes), adoption, minutes, full_log)}
{section_split(order, stats, minutes)}
{section_medians(order, minutes)}
{section_weekly(order, all_rows, minutes, None if full_log else (first, last))}
{section_alerts(rows)}
<p class="foot">Regenerate: <code>python3 extra/pod-dashboard/dashboard.py [minutes] [--from YYYY-MM-DD --to YYYY-MM-DD]</code></p>
</main><div id="tip" role="status" hidden></div><script>{JS}</script></body></html>
"""
    OUT.write_text(page, encoding="utf-8")
    print(OUT)
    print_summary(order, stats, rows, all_rows, adoption, minutes, full_log, filt)

if __name__ == "__main__":
    main()
