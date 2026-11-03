#!/usr/bin/env python3
"""Check meeting recaps against brain/RESOLVER.md and brain/SANITIZER.md.

Usage: python3 extra/process-call/check_recap.py <recap.md> [...]
Prints PASS / WARN / FAIL (SKIP when a check doesn't apply) per check for each
file, then a summary. Exits 1 if any check FAILs. Standard library only.

FAIL checks
 1 path      A file under brain/ must be brain/knowledge/meetings/YYYY-MM-DD-<slug>.md
             (slug: lowercase letters, digits, hyphens). Skipped for files outside brain/.
 2 front     Front matter has type: meeting, plus non-empty date, account, attendees, source.
 3 sections  "## Summary", "## Action items", "## Open questions", "## Flags for a person".
 4 actions   Every action-item table row (not the header or separator) has exactly one
             owner (no "and", "/", "&", "or", ",") and a Due cell in YYYY-MM-DD form.
 5 links     Every relative markdown link points to a path that exists, resolved from the
             recap's own folder (URLs, mailto: and #anchors are ignored).
 6 redflags  No SANITIZER red-flag phrase anywhere (case-insensitive, whole words,
             plural allowed: "agency fees" and "DMs" count). "left the call" only as a
             pasted transcript marker in square brackets, e.g. "[Dana Reyes left the call]",
             so the approved held-back Flags line passes.
WARN checks
 7 numbers   Possible retyped performance number: a "$" amount, or GMV / ad spend /
             affiliates / retention within 5 words of a number (ISO dates and link targets
             ignored). Client-agreed budgets and targets are allowed, so a person checks.
 8 bullets   The Summary has 3 to 6 top-level bullets.
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote

SECTIONS = ["Summary", "Action items", "Open questions", "Flags for a person"]
RED_FLAGS = ["between us", "don't mention", "dm", "dmed", "flaky", "difficult",
             "checked out", "agency fee", "our fee", "margin"]
RED_RE = re.compile(r"\b(" + "|".join(map(re.escape, RED_FLAGS)) + r")s?\b"
                    r"|\[[^\]\n]*\bleft the call\]", re.I)  # pasted marker "[Dana Reyes left the call]"
NAME_RE = re.compile(r"\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*\.md")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
MULTI_OWNER_RE = re.compile(r"\b(?:and|or)\b|[/&,]", re.I)
NUM_RE = re.compile(r"[$~]?\d[\d,.]*[kKmM%]?")
METRIC_RE = re.compile(r"gmv|adspend|affiliates?|retention", re.I)


def split_front(text):
    """Return (front-matter dict or None, index of the first body line)."""
    m = re.match(r"---\n(.*?)\n---[ \t]*(?:\n|$)", text, re.S)
    if not m:
        return None, 0
    pairs = [l.partition(":") for l in m.group(1).splitlines()]
    return {k.strip(): v.strip().strip("\"'") for k, sep, v in pairs if sep}, m.group(0).count("\n")


def section(lines, name):
    """Lines under '## name' up to the next # or ## heading; None if absent."""
    out = None
    for line in lines:
        if out is not None:
            if re.match(r"#{1,2} ", line):
                break
            out.append(line)
        elif line.rstrip() == "## " + name:
            out = []
    return out


def numbered(lines, start=0):
    """(line number, text without link targets) for lines[start:]."""
    return [(n, re.sub(r"\]\([^)]*\)", "]", l.replace("\u2019", "'")))
            for n, l in enumerate(lines[start:], start + 1)]


def result(num, name, problems, level="FAIL", ok=""):
    return (num, name, level if problems else "PASS", "; ".join(problems) or ok)


def check(path):
    p = Path(path)
    if not p.is_file():
        return [(0, "file", "FAIL", "file not found")]
    text = p.read_text(encoding="utf-8")
    lines = text.splitlines()
    fm, body = split_front(text)

    parts = p.resolve().parts
    if "brain" not in parts:
        res = [(1, "path", "SKIP", "outside brain/")]
    else:
        rel = parts[len(parts) - 1 - parts[::-1].index("brain"):]
        ok = rel[1:3] == ("knowledge", "meetings") and len(rel) == 4 and NAME_RE.fullmatch(rel[3])
        res = [(1, "path", "PASS" if ok else "FAIL", "/".join(rel))]

    bad = ["no front matter"] if fm is None else ["missing " + k for k in (
        "date", "account", "attendees", "source") if not fm.get(k, "").strip("[] ")]
    if fm is not None and fm.get("type") != "meeting":
        bad.append("type is %r, not 'meeting'" % fm.get("type"))
    res.append(result(2, "front", bad))

    res.append(result(3, "sections", ["missing ## " + s for s in SECTIONS if section(lines, s) is None]))

    actions = section(lines, "Action items")
    if actions is None:
        res.append((4, "actions", "SKIP", "no Action items section (see 3)"))
    else:
        rows = [l.strip() for l in actions if l.strip().startswith("|")]
        cells = lambda r: [c.strip() for c in r.strip("|").split("|")]
        head = [c.lower() for c in cells(rows[0])] if rows else []
        oi = head.index("owner") if "owner" in head else 0
        di = head.index("due") if "due" in head else len(head) - 1
        data = [cells(r) for r in rows[1:] if not re.fullmatch(r"[|\s:-]+", r)]
        bad = []
        for n, c in enumerate(data, 1):
            owner, due = (c[oi] if oi < len(c) else ""), (c[di] if 0 <= di < len(c) else "")
            if not owner or MULTI_OWNER_RE.search(owner):
                bad.append("row %d owner %r" % (n, owner))
            if not DATE_RE.fullmatch(due):
                bad.append("row %d due %r" % (n, due))
        res.append(result(4, "actions", bad, ok="%d row(s)" % len(data)))

    res.append(result(5, "links", ["L%d %s" % (n, t) for n, l in enumerate(lines, 1) for t in LINK_RE.findall(l)
                                   if not re.match(r"[a-z][a-z0-9+.-]*:|#|/", t, re.I)
                                   and not (p.parent / unquote(t.split("#")[0])).exists()]))

    res.append(result(6, "redflags", ["L%d %r" % (n, m.group(0)) for n, l in numbered(lines)
                                      for m in RED_RE.finditer(l)]))

    hits = []
    for n, line in numbered(lines, body):
        toks = [t.strip("()[]*,.;:!?\"'`") for t in re.sub(r"(?i)\bad\s+spend\b", "adspend", line).split()]
        mets = [i for i, t in enumerate(toks) if METRIC_RE.fullmatch(t)]
        nums = [i for i, t in enumerate(toks) if NUM_RE.fullmatch(t) and not DATE_RE.fullmatch(t)]
        if re.search(r"\$\s?\d", line) or any(abs(m - k) <= 5 for m in mets for k in nums):
            hits.append("L%d (check against the sheet)" % n)
    res.append(result(7, "numbers", hits, "WARN"))

    count = sum(1 for l in section(lines, "Summary") or [] if re.match(r"[-*+] ", l))
    res.append(result(8, "bullets", [] if 3 <= count <= 6 else ["%d bullet(s)" % count], "WARN",
                      "%d bullet(s)" % count))
    return res


def main(argv):
    if not argv:
        print(__doc__.strip())
        return 2
    totals = []
    for path in argv:
        print("\n" + path)
        st = []
        for num, name, status, detail in check(path):
            print("  %-4s  %d %-9s %s" % (status, num, name, detail))
            st.append(status)
        worst = "FAIL" if "FAIL" in st else "WARN" if "WARN" in st else "PASS"
        totals.append("  %-4s  %s  (%d pass, %d warn, %d fail)" % (
            worst, path, st.count("PASS"), st.count("WARN"), st.count("FAIL")))
    failed = sum(t.lstrip().startswith("FAIL") for t in totals)
    print("\nSummary\n" + "\n".join(totals) + "\n%d of %d file(s) failed" % (failed, len(totals)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
