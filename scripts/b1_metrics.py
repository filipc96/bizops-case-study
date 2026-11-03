#!/usr/bin/env python3
"""B1: recompute the recap number per pod from the raw call log.

The number: share of client calls with a recap posted within N minutes of call_end
(N = 60 by default; a recap counts if minutes_to_post <= N). Denominator = calls held.

Usage:
    python3 scripts/b1_metrics.py              # 60-minute threshold
    python3 scripts/b1_metrics.py 15           # any other threshold, in minutes
    python3 scripts/b1_metrics.py --from 2026-09-21 --to 2026-09-24   # one week (dates inclusive)
    python3 scripts/b1_metrics.py --from 2026-09-24 --to 2026-09-24   # one day
    python3 scripts/b1_metrics.py --calls calls.csv --adoption adoption.csv

--from / --to filter on the `date` column. The adoption.csv check only runs when the
filter keeps every call, because the dashboard covers the whole log.

Standard library only.
"""
import argparse
import csv
import statistics
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POD_ORDER = ["North", "East", "South", "West"]
TS_FMT = "%Y-%m-%d %H:%M"
DASHBOARD_MINUTES = 60          # adoption.csv is defined at "within 1hr"
EAST_SPLIT = "2026-09-15"       # "before" = date < split, "after" = date >= split


def load_calls(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["recorded"] = r["recorded"].strip().lower() == "yes"
        r["posted_by"] = r["posted_by"].strip()
        if r["recap_posted_at"].strip():
            end = datetime.strptime(r["call_end"], TS_FMT)
            posted = datetime.strptime(r["recap_posted_at"], TS_FMT)
            r["minutes"] = (posted - end).total_seconds() / 60
        else:
            r["minutes"] = None
    return rows


def summarise(rows, minutes):
    held = len(rows)
    posted = [r for r in rows if r["minutes"] is not None]
    within = sum(r["minutes"] <= minutes for r in posted)
    return {
        "held": held,
        "recorded": sum(r["recorded"] for r in rows),
        "posted": len(posted),
        "within": within,
        "share": within / held if held else None,
    }


def pct(x):
    return "n/a" if x is None else f"{x:.0%}"


def fmt_median(values):
    if not values:
        return "-"
    return f"{statistics.median(values):.0f} min (n={len(values)})"


def by_pod(rows):
    pods = {p: [] for p in POD_ORDER}
    for r in rows:
        pods.setdefault(r["pod"], []).append(r)
    return pods


def print_pod_table(pods, minutes):
    print(f"\n1. Per pod, recap within {minutes} min of call_end (<= {minutes})")
    hdr = f"{'pod':<7}{'held':>6}{'recorded':>10}{'posted':>8}{'within':>8}{'share':>8}"
    print(hdr)
    print("-" * len(hdr))
    ranked = sorted(pods.items(), key=lambda kv: summarise(kv[1], minutes)["share"] or 0, reverse=True)
    for pod, rows in ranked:
        s = summarise(rows, minutes)
        print(f"{pod:<7}{s['held']:>6}{s['recorded']:>10}{s['posted']:>8}{s['within']:>8}{pct(s['share']):>8}")
    t = summarise([r for rows in pods.values() for r in rows], minutes)
    print(f"{'All':<7}{t['held']:>6}{t['recorded']:>10}{t['posted']:>8}{t['within']:>8}{pct(t['share']):>8}")


def print_medians(pods):
    print("\n2. Median minutes from call_end to recap, by who posted it")
    print(f"{'pod':<7}{'agent':>20}{'AM':>20}")
    for pod, rows in pods.items():
        agent = [r["minutes"] for r in rows if r["minutes"] is not None and r["posted_by"] == "agent"]
        am = [r["minutes"] for r in rows if r["minutes"] is not None and r["posted_by"] == "AM"]
        print(f"{pod:<7}{fmt_median(agent):>20}{fmt_median(am):>20}")


def print_east_split(pods, minutes):
    east = pods.get("East", [])
    print(f"\n3. East before / after {EAST_SPLIT} (threshold {minutes} min)")
    print(f"{'period':<22}{'held':>6}{'within':>8}{'share':>8}{'by agent':>10}{'by AM':>7}")
    for label, part in (
        (f"before (< {EAST_SPLIT})", [r for r in east if r["date"] < EAST_SPLIT]),
        (f"after  (>= {EAST_SPLIT})", [r for r in east if r["date"] >= EAST_SPLIT]),
    ):
        s = summarise(part, minutes)
        agent = sum(r["posted_by"] == "agent" for r in part)
        am = sum(r["posted_by"] == "AM" for r in part)
        print(f"{label:<22}{s['held']:>6}{s['within']:>8}{pct(s['share']):>8}{agent:>10}{am:>7}")


def print_dashboard_check(pods, adoption_path):
    print(f"\n4. calls.csv vs adoption.csv (dashboard is defined at {DASHBOARD_MINUTES} min)")
    with open(adoption_path, newline="") as f:
        dash = {r["pod"]: r for r in csv.DictReader(f)}
    fields = (
        ("held", "client_calls_held"),
        ("recorded", "calls_recorded"),
        ("within", "recaps_posted_within_1hr"),
    )
    any_mismatch = False
    for pod, rows in pods.items():
        s = summarise(rows, DASHBOARD_MINUTES)
        d = dash.get(pod)
        if d is None:
            print(f"  {pod}: missing from adoption.csv")
            any_mismatch = True
            continue
        issues = []
        for key, col in fields:
            if int(d[col]) != s[key]:
                issues.append(f"{col}: dashboard {d[col]} vs log {s[key]}")
        dash_share = float(d["share_of_calls_with_recap_within_1hr"].rstrip("%")) / 100
        if round(dash_share, 2) != round(s["share"], 2):
            hint = ""
            if s["recorded"] and round(dash_share, 2) == round(s["within"] / s["recorded"], 2):
                hint = " (dashboard divides by calls recorded, not calls held)"
            issues.append(f"share: dashboard {pct(dash_share)} vs log {pct(s['share'])}{hint}")
        own = int(d["recaps_posted_within_1hr"]) / int(d["client_calls_held"])
        if round(own, 2) != round(dash_share, 2):
            issues.append(f"dashboard is internally inconsistent: its own {d['recaps_posted_within_1hr']}"
                          f"/{d['client_calls_held']} = {pct(own)}, not {pct(dash_share)}")
        any_mismatch |= bool(issues)
        print(f"  {pod}: " + ("matches" if not issues else "; ".join(issues)))
    for pod in dash:
        if pod not in pods:
            print(f"  {pod}: in adoption.csv but not in calls.csv")
            any_mismatch = True
    if not any_mismatch:
        print("  No mismatches.")


def print_data_checks(rows):
    print("\n5. Data checks on calls.csv")
    dupes = sorted(i for i, n in Counter(r["call_id"] for r in rows).items() if n > 1)
    checks = [
        ("duplicate call_ids", dupes),
        ("date column != call_end date", [r["call_id"] for r in rows if not r["call_end"].startswith(r["date"])]),
        ("recap posted before call_end", [r["call_id"] for r in rows if r["minutes"] is not None and r["minutes"] < 0]),
        ("recap posted but call not recorded", [r["call_id"] for r in rows if r["minutes"] is not None and not r["recorded"]]),
        ("posted_by set but no recap time", [r["call_id"] for r in rows if r["posted_by"] and r["minutes"] is None]),
        ("recorded but no recap posted", [f"{r['call_id']} ({r['pod']}, {r['account']})" for r in rows
                                          if r["recorded"] and r["minutes"] is None]),
    ]
    for label, hits in checks:
        print(f"  {label}: {', '.join(hits) if hits else 'none'}")


def iso_date(value):
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected YYYY-MM-DD, got {value!r}")
    return value


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("minutes", nargs="?", type=float, default=60,
                    help="threshold in minutes after call_end (default 60, inclusive)")
    ap.add_argument("--from", dest="date_from", type=iso_date, metavar="YYYY-MM-DD",
                    help="first call date to include (inclusive)")
    ap.add_argument("--to", dest="date_to", type=iso_date, metavar="YYYY-MM-DD",
                    help="last call date to include (inclusive)")
    ap.add_argument("--calls", default=ROOT / "calls.csv", type=Path)
    ap.add_argument("--adoption", default=ROOT / "adoption.csv", type=Path)
    args = ap.parse_args()
    if args.date_from and args.date_to and args.date_from > args.date_to:
        ap.error(f"--from {args.date_from} is after --to {args.date_to}")
    minutes = int(args.minutes) if args.minutes.is_integer() else args.minutes

    all_rows = load_calls(args.calls)
    rows = [r for r in all_rows
            if (not args.date_from or r["date"] >= args.date_from)
            and (not args.date_to or r["date"] <= args.date_to)]
    window = f"{args.date_from or 'start'} to {args.date_to or 'end'}"
    if not rows:
        print(f"No calls in calls.csv from {window}.")
        return
    pods = by_pod(rows)
    print(f"{len(rows)} calls, {min(r['date'] for r in rows)} to {max(r['date'] for r in rows)}"
          + (f" (filter: {window})" if len(rows) < len(all_rows) else ""))
    print_pod_table(pods, minutes)
    print_medians(pods)
    print_east_split(pods, minutes)
    if len(rows) == len(all_rows):
        print_dashboard_check(pods, args.adoption)
    else:
        print("\n4. calls.csv vs adoption.csv: skipped, because the dashboard covers the whole log, not this filter")
    print_data_checks(rows)


if __name__ == "__main__":
    main()
