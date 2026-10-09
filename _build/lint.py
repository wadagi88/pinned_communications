# -*- coding: utf-8 -*-
"""Checks the generated site: links, anchors, tokens, SMS length."""
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D  # noqa: E402

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
TOKEN_RE = re.compile(r"\{\{(\w+)\}\}")
MARKER_RE = re.compile(r"\n\[([^\]]+)\]\s*$")
fails, warns = [], []


def fill(body):
    return TOKEN_RE.sub(lambda m: D.SAMPLES.get(m.group(1), m.group(1)), body)


def segments(n):
    return 1 if n <= 160 else math.ceil(n / 153)


pages = {f for f in os.listdir(ROOT) if f.endswith(".html")}
anchors = {}
for f in pages:
    html = open(os.path.join(ROOT, f)).read()
    anchors[f] = set(re.findall(r'id="([^"]+)"', html))

# every nav target exists
for href, _ in D.NAV:
    if href not in pages:
        fails.append("nav points at a missing page: %s" % href)

# every internal link resolves, anchors included
for f in sorted(pages):
    html = open(os.path.join(ROOT, f)).read()
    for href in re.findall(r'href="([^"#:]*\.html)(#[^"]*)?"', html):
        target, frag = href[0], href[1]
        if target not in pages:
            fails.append("%s links to missing page %s" % (f, target))
        elif frag and frag[1:] not in anchors[target]:
            fails.append("%s links to missing anchor %s%s" % (f, target, frag))
    if "assets/comms.css" not in html:
        fails.append("%s does not load the stylesheet" % f)

# touchpoint integrity
ids = set()
for t in D.TOUCHPOINTS:
    if t["id"] in ids:
        fails.append("duplicate touchpoint id %s" % t["id"])
    ids.add(t["id"])
    if t["lane"] not in D.LANE_BY_KEY:
        fails.append("%s has unknown lane %s" % (t["id"], t["lane"]))
    if t["status"] not in ("live", "partial", "gap", "defect"):
        fails.append("%s has unknown status %s" % (t["id"], t["status"]))
    msg_channels = {c for c, _ in t["msgs"]}
    if not msg_channels:
        fails.append("%s has no copy" % t["id"])
    for c in msg_channels:
        if c not in t["channels"]:
            fails.append("%s writes %s copy but does not list the channel" % (t["id"], c))
    for c in t["channels"]:
        if c not in msg_channels:
            warns.append("%s lists %s but has no %s copy" % (t["id"], c, c))
    for c, p in t["msgs"]:
        text = p if isinstance(p, str) else " ".join(p)
        for tok in TOKEN_RE.findall(text):
            if tok not in D.SAMPLES:
                fails.append("%s uses unmeasured token {{%s}}" % (t["id"], tok))
        if c in ("sms", "whatsapp"):
            body = MARKER_RE.sub("", p)
            n = len(fill(body))
            if segments(n) > 2:
                fails.append("%s SMS is %d chars (%d segments)" % (t["id"], n, segments(n)))
        if c == "push":
            if len(fill(p[0])) > 45:
                warns.append("%s push title is %d chars" % (t["id"], len(fill(p[0]))))
            if len(fill(p[1])) > 110:
                warns.append("%s push body is %d chars" % (t["id"], len(fill(p[1]))))

for w in warns:
    print("  warn  %s" % w)
for f in fails:
    print("  FAIL  %s" % f)
print("lint: %d pages, %d touchpoints, %d warnings, %d failures"
      % (len(pages), len(D.TOUCHPOINTS), len(warns), len(fails)))
sys.exit(1 if fails else 0)
