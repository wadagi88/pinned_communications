# -*- coding: utf-8 -*-
"""Generate the Pinned Communications surface. Run: _build/build.sh"""
import html
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D  # noqa: E402

OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
V = D.BUILD

TOKEN_RE = re.compile(r"\{\{(\w+)\}\}")
MARKER_RE = re.compile(r"\n\[([^\]]+)\]\s*$")
BUTTON_RE = re.compile(r"\[\s([^\]]+?)\s\]")


def e(s):
    return html.escape(str(s), quote=False)


def split_marker(body):
    """Trailing '[−7 days]' line is a label for the rung, not part of the copy."""
    m = MARKER_RE.search(body)
    if not m:
        return body, None
    return body[: m.start()], m.group(1)


def fill(body):
    return TOKEN_RE.sub(lambda m: D.SAMPLES.get(m.group(1), m.group(1)), body)


def segments(n):
    if n <= 160:
        return 1
    return math.ceil(n / 153)


def tok_html(body):
    """Escape, then put tokens in mono so a reader sees what is variable."""
    out = e(body)
    out = TOKEN_RE.sub(lambda m: '<span class="tok">{{%s}}</span>' % m.group(1), out)
    return out


def buttons_html(body):
    return BUTTON_RE.sub(lambda m: '<span class="chip">%s</span>' % e(m.group(1)), tok_html(body))


def chips(channels):
    return "".join(
        '<span class="chip %s">%s</span>' % (D.CHANNEL_CLASS[c], D.CHANNEL_LABEL[c])
        for c in channels
    )


STATUS_WORD = D.STATUS_WORD


def badge(status):
    return '<span class="badge %s">%s</span>' % (status, STATUS_WORD[status])


# ── message rendering ────────────────────────────────────────────────────────

def render_sms(body, label="SMS"):
    body, marker = split_marker(body)
    n = len(fill(body))
    seg = segments(n)
    over = " over" if seg > 2 else ""
    cap = label + (" · " + marker if marker else "")
    return (
        '<div class="msg"><div class="msg-cap"><span class="lbl">%s</span>'
        '<span class="count%s">%d chars · %d segment%s</span></div>'
        '<div class="sms-bubble">%s</div></div>'
        % (e(cap), over, n, seg, "" if seg == 1 else "s", tok_html(body))
    )


def render_push(payload):
    title, body = payload
    tn, bn = len(fill(title)), len(fill(body))
    warn = " over" if (tn > 45 or bn > 110) else ""
    return (
        '<div class="msg"><div class="msg-cap"><span class="lbl">Push · lock screen</span>'
        '<span class="count%s">title %d · body %d</span></div>'
        '<div class="lock"><span class="ico"><i></i><i></i><i></i><i></i></span><span>'
        '<span class="l-app">Pinned Runner</span>'
        '<span class="l-title">%s</span><span class="l-body">%s</span></span></div></div>'
        % (warn, tn, bn, tok_html(title), tok_html(body))
    )


def render_in_app(payload):
    title, body = payload
    return (
        '<div class="msg"><div class="msg-cap"><span class="lbl">In-app</span></div>'
        '<div class="toast"><b>%s</b><p>%s</p></div></div>'
        % (tok_html(title), buttons_html(body).replace("\n", "<br>"))
    )


def render_email(payload):
    subject, body = payload
    return (
        '<div class="msg"><div class="msg-cap"><span class="lbl">Email</span></div>'
        '<div class="email"><div class="email-head"><span>Pinned · notifications@pinned.app</span>'
        '<b>%s</b></div><div class="email-body">%s</div></div></div>'
        % (tok_html(subject), tok_html(body))
    )


def render_whatsapp(body):
    return render_sms(body, label="WhatsApp")


def render_msg(channel, payload):
    if channel == "sms":
        return render_sms(payload)
    if channel == "whatsapp":
        return render_whatsapp(payload)
    if channel == "push":
        return render_push(payload)
    if channel == "in_app":
        return render_in_app(payload)
    if channel == "email":
        return render_email(payload)
    raise ValueError(channel)


def render_old(old):
    if not old:
        return ""
    n = len(fill(old.split("\n— ")[0]))
    return (
        '<div class="msg"><div class="msg-cap"><span class="lbl">Live today</span>'
        '<span class="count">%d chars · %d segment%s</span></div>'
        '<div class="old">%s</div></div>'
        % (n, segments(n), "" if segments(n) == 1 else "s", tok_html(old))
    )


def render_tp(t):
    left = "".join(render_msg(c, p) for c, p in t["msgs"])
    right = []
    if t["old"]:
        right.append(render_old(t["old"]))
    if t["rules"]:
        right.append('<div class="msg"><span class="lbl">Rules</span><ul>%s</ul></div>'
                     % "".join("<li>%s</li>" % r for r in t["rules"]))
    notes = ""
    if t.get("review"):
        notes += ('<div class="tp-note team"><span class="nlbl">Team review · 13 Oct</span>%s</div>'
                  % t["review"])
    if t.get("warmth"):
        notes += ('<div class="tp-note warm"><span class="nlbl">Warmth</span>%s</div>'
                  % e(t["warmth"]))
    notes += "".join('<div class="tp-note %s">%s</div>' % (kind, text) for kind, text in t["notes"])
    meta = []
    if t["key"]:
        meta.append('<span class="chip">%s</span>' % e(t["key"]))
    if t["hook"]:
        meta.append('<span class="chip">Hook · %s</span>' % e(t["hook"]))
    return """
<article class="tp" id="%(id)s">
  <div class="tp-head">
    <span class="tp-id">%(id)s</span>
    <span class="tp-title"><h3>%(name)s</h3><p>%(intent)s</p></span>
    <span class="tp-meta">%(badge)s<span class="chips">%(chips)s</span></span>
  </div>
  <div class="tp-body">
    <div class="kv">
      <div><b>Trigger</b><span>%(trigger)s</span></div>
      <div><b>Timing</b><span>%(timing)s</span></div>
      <div><b>Source</b><span>%(source)s</span></div>
    </div>
    <div class="chips" style="margin-top:14px">%(meta)s</div>
    %(notes)s
    <div class="tp-cols" style="margin-top:18px">
      <div>%(left)s</div>
      <div>%(right)s</div>
    </div>
  </div>
</article>""" % dict(
        id=e(t["id"]), name=e(t["name"]), intent=e(t["intent"]), badge=badge(t["status"]),
        chips=chips(t["channels"]), trigger=e(t["trigger"]), timing=e(t["timing"]),
        source=e(t["source"] or "—"), meta="".join(meta), notes=notes,
        left=left, right="".join(right))


# ── page shell ───────────────────────────────────────────────────────────────

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,700;0,9..40,800;1,9..40,400&family=DM+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="assets/comms.css?v=%(v)d">
<link rel="icon" href="data:image/svg+xml,%%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%%3E%%3Crect width='32' height='32' fill='%%23C8005A'/%%3E%%3Cg fill='%%23fff'%%3E%%3Cpath d='M6 8h20l-3 5H9z'/%%3E%%3Cpath d='M8 15h16l-2.5 4.5h-11z'/%%3E%%3Cpath d='M10 21h12l-2 3.5h-8z'/%%3E%%3C/g%%3E%%3C/svg%%3E">
<script>
  // Theme choice is a per-device convenience; failure must never blank the page.
  try { var t = localStorage.getItem("pinned-comms-theme"); if (t) document.documentElement.dataset.theme = t; } catch (err) {}
</script>
</head>
<body>
"""

FOOT = """
<footer>
  <div class="wrap">
    <p><b>Pinned Communications</b> · drafted from the Communication Map and the live templates in pinned-core · %(updated)s</p>
    <p>Internal working document. Build %(v)d.</p>
  </div>
</footer>
<script>
  document.querySelectorAll("[data-themer]").forEach(function (b) {
    b.addEventListener("click", function () {
      var root = document.documentElement;
      var now = root.dataset.theme === "dark" ? "light" : "dark";
      root.dataset.theme = now;
      try { localStorage.setItem("pinned-comms-theme", now); } catch (err) {}
    });
  });
</script>
</body>
</html>
"""


def navbar(current):
    links = []
    for href, label in D.NAV:
        cls = ' class="on"' if href == current else ""
        links.append('<a href="%s"%s>%s</a>' % (href, cls, e(label)))
    return """
<nav class="navbar"><div class="wrap">
  <a class="home" href="index.html">Pinned Comms</a>
  %s
  <span class="spacer"></span>
  <button class="themer" type="button" data-themer>Theme</button>
</div></nav>""" % "\n  ".join(links)


def page(filename, title, desc, body):
    out = HEAD % dict(title=e(title), desc=e(desc), v=V)
    out += body
    out += FOOT % dict(updated=D.UPDATED, v=V)
    with open(os.path.join(OUT, filename), "w") as fh:
        fh.write(out)
    return filename


def phead(crumb, eyebrow, h1, lede):
    return """
<header class="phead"><div class="wrap">
  <p class="crumb"><a href="index.html">Pinned Communications</a> · %s</p>
  <p class="eyebrow" style="margin-top:10px">%s</p>
  <h1>%s</h1>
  <p class="lede">%s</p>
</div></header>""" % (e(crumb), e(eyebrow), e(h1), lede)


def section(num, title, sub, body, anchor=None):
    a = ' id="%s"' % anchor if anchor else ""
    sub_html = '<p class="sec-sub">%s</p>' % sub if sub else ""
    return """
<section%s><div class="wrap">
  <div class="sec-head"><span class="sec-num">%s</span><h2>%s</h2></div>
  %s
  <div class="rule"></div>
  %s
</div></section>""" % (a, e(num), e(title), sub_html, body)


CH_SHORT = {"sms": "SMS", "push": "Push", "in_app": "In-app", "email": "Email",
            "whatsapp": "WhatsApp", "retire": "None"}


def render_journey(lane_key):
    j = D.JOURNEYS.get(lane_key)
    if not j:
        return ""
    rows = []
    for st in j["steps"]:
        cls = "jstep"
        if st["ch"] == "sms":
            cls += " is-sms"
        if st["ch"] == "retire" or st.get("flag") == "retire":
            cls += " is-retire"
        chip_cls = D.CHANNEL_CLASS.get(st["ch"], "")
        flag = ""
        if st.get("flag") == "open":
            flag = '<span class="flag">open question</span>'
        elif st.get("flag") == "retire":
            flag = '<span class="flag">retired</span>'
        rows.append(
            '<div class="%s"><span class="jn">%s</span>'
            '<span class="jwhen">%s</span>'
            '<span class="jch"><span class="chip %s">%s</span></span>'
            '<span class="jwhat">%s%s</span>'
            '<span class="jwhy">%s</span></div>'
            % (cls, e(st["n"]), e(st["when"]), chip_cls, e(CH_SHORT.get(st["ch"], st["ch"])),
               tok_html(st["what"]), flag, e(st["why"])))
    return """
<div class="jrny">
  <div class="jrny-head"><h3>%s</h3><p>%s</p></div>
  %s
</div>""" % (e(j["headline"]), e(j["sub"]), "\n  ".join(rows))


# ── pages ────────────────────────────────────────────────────────────────────

def by_lane(key):
    return [t for t in D.TOUCHPOINTS if t["lane"] == key]


def counts():
    c = {k: 0 for k in STATUS_WORD}
    for t in D.TOUCHPOINTS:
        c[t["status"]] += 1
    return c


def sms_steps(lane_key, path_only=False):
    j = D.JOURNEYS.get(lane_key)
    if not j:
        return []
    return [st for st in j["steps"]
            if st["ch"] == "sms" and not (path_only and st["off"])]


def matrix_rows(tps, link_page=None):
    rows = []
    for t in tps:
        href = "%s#%s" % (link_page or D.LANE_BY_KEY[t["lane"]]["page"], t["id"])
        rows.append(
            "<tr data-lane=\"%s\" data-status=\"%s\"><td class=\"id\"><a href=\"%s\">%s</a></td>"
            "<td><b>%s</b><span class=\"muted\">%s</span></td>"
            "<td>%s</td><td><span class=\"chips\">%s</span></td><td>%s</td>"
            "<td class=\"id\">%s</td></tr>"
            % (t["lane"], t["status"], href, e(t["id"]), e(t["name"]), e(t["trigger"]),
               e(t["timing"]), chips(t["channels"]), badge(t["status"]),
               e(t["key"] or "—")))
    return "\n".join(rows)


def build_index():
    c = counts()
    lanes = []
    for l in LANES_ORDERED:
        tps = by_lane(l["key"])
        items = "".join(
            '<li><b>%s</b> %s <em>%s</em></li>' % (e(t["id"]), e(t["name"]), e(" · ".join(D.CHANNEL_LABEL[x] for x in t["channels"])))
            for t in tps)
        lanes.append("""
<div class="lane %s">
  <div class="lane-head"><h3>%s</h3><a href="%s#journey">%d touchpoints · %d SMS →</a></div>
  <p style="padding:0 20px;color:var(--text-2);font-size:.93rem">%s</p>
  <ol>%s</ol>
</div>""" % (l["colour"], e(l["title"]), l["page"], len(tps),
             len(sms_steps(l["key"], True)), e(l["who"]), items))

    body = """
<header class="mast">
  <div class="mast-wedges"><i></i><i></i><i></i><i></i></div>
  <div class="wrap">
    <span class="logomark"><span></span><span></span><span></span><span></span></span>
    <p class="eyebrow">Communications &amp; messaging system</p>
    <h1>One voice, <em>every</em> parcel.</h1>
    <p class="lede">Every message Pinned sends to a sender, a receiver, a runner, a host or someone
      who has not signed up yet — what fires it, which channel carries it, what it says, and why.
      Drafted from the Communication Map and audited against the templates running in pinned-core today.</p>
    <div class="mast-facts">
      <div><b>%(total)d</b><small>touchpoints</small></div>
      <div><b>%(live)d</b><small>live today</small></div>
      <div><b>%(partial)d</b><small>partial</small></div>
      <div><b>%(gap)d</b><small>not built</small></div>
      <div><b>%(change)d</b><small>channel changes</small></div>
      <div><b>%(defect)d</b><small>defects</small></div>
    </div>
  </div>
</header>
%(nav)s
""" % dict(total=len(D.TOUCHPOINTS), nav=navbar("index.html"), **c)

    body += section("00", "Why this exists", None, """
<div class="grid g3">
  <div class="card accent-org">
    <span class="lbl">Evidence</span>
    <h3 style="margin-top:8px">%s</h3>
    <p>%s</p>
    <p><b style="color:var(--text)">%s</b></p>
  </div>
  <div class="card accent-mag">
    <span class="lbl">The philosophy</span>
    <h3 style="margin-top:8px">Great products are not an accident</h3>
    <p>A delivery business is judged on the messages far more often than on the deliveries. Most
      customers touch Pinned four times a year and read our SMS six times a week. The messages
      <i>are</i> the product for everyone who is not holding a parcel.</p>
    <p>Clarity and intuitiveness are not a tone of voice. They are a set of decisions taken once,
      written down, and then enforced in code: one event one message, one action per message,
      four rungs then silence, the code on its own line.</p>
    <p><a href="principles.html">The nine principles →</a></p>
  </div>
  <div class="card accent-flow">
    <span class="lbl">Round three · 27 October</span>
    <h3 style="margin-top:8px">The receiver page sets the voice</h3>
    <p>Every receiver SMS ends in a link to <b>publicchoicepage.netlify.app</b>, and the two are read
      forty seconds apart. That page is now the reference for tone, and the receiver lane has been
      rewritten against it rather than against this site.</p>
    <p>It overturned the review pack on one substantive point: the pack sells the paid doorstep
      delivery and never mentions that collecting is free, while the page offers free collection four
      times over and adds <i>no charge, no pressure</i>. Free is named first now, in every variant.</p>
    <p><a href="gaps.html#packvspage">The pack against the page →</a> ·
       <a href="principles.html#tone">The reference →</a></p>
  </div>
</div>""" % (e(D.EVIDENCE["title"]), D.EVIDENCE["body"], e(D.EVIDENCE["close"])))

    body += section("01", "How to read this", None, """
<div class="grid g4">
  <div class="card"><span class="lbl">Live</span><p class="tight">A template exists in
    <code>NotificationTemplate</code> and fires. The copy here is a rewrite of what is already sending.</p></div>
  <div class="card"><span class="lbl">Partial</span><p class="tight">Something fires, but it is
    missing a channel the map asks for, a rung in its ladder, or the point of the message.</p></div>
  <div class="card"><span class="lbl">Not built</span><p class="tight">The map asks for it, or the
    hook needs it, and nothing sends it today.</p></div>
  <div class="card"><span class="lbl">Defect</span><p class="tight">It fires, and what it does is
    wrong — a duplicate, a wrong token, or a notification that damages trust each time it lands.</p></div>
</div>
<p class="sec-sub" style="margin-top:20px">Character counts are measured with the longest realistic
  values filled in, not with the tokens left empty. An SMS that fits “Jay” and breaks on
  “Wanjiru” has not been written.</p>""")

    body += section("02", "The six lanes", None,
                    '<div class="grid g2">%s</div>' % "".join(lanes))

    body += section("03", "Every touchpoint", None, """
<div class="scroller"><table>
<thead><tr><th>ID</th><th>Touchpoint</th><th>Timing</th><th>Channels</th><th>Status</th><th>Template key</th></tr></thead>
<tbody>%s</tbody></table></div>""" % matrix_rows(D.TOUCHPOINTS))

    body += '<div class="wrap"><div class="endrule"></div></div>'
    return page("index.html", "Pinned Communications", SITE_DESC, body)


def build_principles():
    body = phead("Voice", "How Pinned speaks",
                 "Nine principles, a warmth layer, and a contract every message signs",
                 "Clarity is not a style. It is the same four questions answered in the same order, "
                 "every time, in every channel. Warmth is not a style either — it is the four or five "
                 "moments in a journey where somebody has something at stake, and we show that we know it.")
    body += navbar("principles.html")

    cards = []
    for p in D.PRINCIPLES:
        cards.append("""
<div class="card">
  <span class="sec-num">%s</span>
  <h3 style="margin-top:6px">%s</h3>
  <p>%s</p>
  <div class="dd" style="margin-top:14px">
    <div class="y"><span class="lbl">Write this</span><span class="ex">%s</span></div>
    <div class="n"><span class="lbl">Not this</span><span class="ex">%s</span></div>
  </div>
</div>""" % (e(p["n"]), e(p["t"]), e(p["p"]), e(p["yes"]).replace("\n", "<br>"), e(p["no"])))
    body += section("01", "The principles", None, '<div class="grid">%s</div>' % "".join(cards))

    wcards = []
    for w in D.WARMTH_MOVES:
        wcards.append("""
<div class="card accent-mag">
  <span class="sec-num">%s</span>
  <h3 style="margin-top:6px">%s</h3>
  <p>%s</p>
  <div class="dd" style="margin-top:14px">
    <div class="y"><span class="lbl">Write this</span><span class="ex">%s</span></div>
    <div class="n"><span class="lbl">Not this</span><span class="ex">%s</span></div>
  </div>
</div>""" % (e(w["n"]), e(w["t"]), e(w["p"]), e(w["yes"]), e(w["no"])))
    budget = "".join('<div class="card"><span class="lbl">%s</span><p class="tight">%s</p></div>'
                     % (e(a), e(b)) for a, b in D.WARMTH_BUDGET)
    tr = D.TONE_REFERENCE
    tr_rules = "".join('<div class="card"><span class="lbl">%s</span><p class="tight">%s</p></div>'
                       % (e(a), b) for a, b in tr["rules"])
    body += section("02", "The reference", None,
                    '<div class="card accent-lock"><span class="lbl">%s</span>'
                    '<h3 style="margin-top:8px">%s</h3><p>%s</p></div>'
                    '<div class="grid g2" style="margin-top:16px">%s</div>'
                    % (e(tr["url"]), e(tr["title"]), e(tr["body"]), tr_rules),
                    anchor="tone")

    pos = D.POSITIONING
    pos_rules = "".join('<div class="card"><span class="lbl">%s</span><p class="tight">%s</p></div>'
                        % (e(a), e(b)) for a, b in pos["where"])
    body += section("03", "The warmth layer",
                    D.WARMTH_INTRO,
                    '<div class="grid g2">%s</div>'
                    '<h3 style="margin:38px 0 0">Where the warmth is allowed to go</h3>'
                    '<p class="sec-sub" style="margin-top:10px">Warmth spent everywhere is warmth nobody '
                    'feels. Each lane gets a short list of moments, and the messages in between stay plain.</p>'
                    '<div class="grid g4" style="margin-top:16px">%s</div>'
                    '<h3 style="margin:38px 0 0">The positioning line</h3>'
                    '<div class="card accent-mag" style="margin-top:16px">'
                    '<p style="font-size:1.5rem;font-weight:800;letter-spacing:-.02em;color:var(--text);margin:0">%s</p>'
                    '<p>%s</p></div>'
                    '<div class="grid g4" style="margin-top:16px">%s</div>'
                    % ("".join(wcards), budget, e(pos["line"]), e(pos["body"]), pos_rules),
                    anchor="warmth")

    rows = "".join(
        '<div class="card"><span class="lbl">%d. %s</span><p class="tight">%s</p></div>' % (i + 1, e(q), e(a))
        for i, (q, a) in enumerate(D.CONTRACT))
    body += section("04", "The clarity contract",
                    "Every Pinned message answers these four questions, in this order. A message that "
                    "cannot answer the third should not be sent.",
                    '<div class="grid g4">%s</div>' % rows)

    hooks = "".join(
        '<div><span class="n">%s</span><h4>%s</h4><p>%s</p></div>' % (e(h["n"]), e(h["t"]), e(h["p"]))
        for h in D.HOOK_FRAME)
    lane_hooks = []
    for l in LANES_ORDERED:
        h = l["hook"]
        lane_hooks.append("""
<div class="card %s">
  <h3>%s</h3>
  <div class="kv">
    <div><b>Trigger</b><span>%s</span></div>
    <div><b>Action</b><span>%s</span></div>
    <div><b>Reward</b><span>%s</span></div>
    <div><b>Investment</b><span>%s</span></div>
  </div>
</div>""" % (l["colour"], e(l["title"]), e(h["trigger"]), e(h["action"]), e(h["reward"]), e(h["investment"])))
    body += section("05", "The hook, applied",
                    "Trigger, action, variable reward, investment. Pinned already has genuine variable "
                    "rewards — the runner's payout, the host's weekly figure, the proof photo. None of "
                    "them are currently where the person looks.",
                    '<div class="hook">%s</div><div class="grid g2" style="margin-top:22px">%s</div>'
                    % (hooks, "".join(lane_hooks)))

    gl = "".join('<tr><td><b>%s</b></td><td>%s</td></tr>' % (e(a), e(b)) for a, b in D.GLOSSARY)
    body += section("06", "Words we do not use",
                    "Internal vocabulary leaks into customer copy whenever nobody writes it down.",
                    '<div class="scroller"><table><thead><tr><th>Inside Pinned</th>'
                    '<th>What the customer reads</th></tr></thead><tbody>%s</tbody></table></div>' % gl)
    body += '<div class="wrap"><div class="endrule"></div></div>'
    return page("principles.html", "Voice · Pinned Communications",
                "The eight principles, the clarity contract and the hook framework.", body)


def build_channels():
    body = phead("Channels & rules", "What each channel is for",
                 "Six channels, eight laws",
                 "A channel is a job, not a copy of the message. “(sms, email, in-app)” in the map "
                 "means three different jobs — not the same sentence three times.")
    body += navbar("channels.html")

    cards = []
    for c in D.CHANNELS:
        cards.append("""
<div class="card">
  <span class="chips"><span class="chip %s">%s</span></span>
  <h3 style="margin-top:10px">%s</h3>
  <div class="kv">
    <div><b>Use for</b><span>%s</span></div>
    <div><b>Never for</b><span>%s</span></div>
  </div>
  <span class="lbl" style="margin-top:16px">Rules</span>
  <ul>%s</ul>
</div>""" % (D.CHANNEL_CLASS[c["k"]], D.CHANNEL_LABEL[c["k"]], e(c["role"]), e(c["use"]), e(c["avoid"]),
             "".join("<li>%s</li>" % e(r) for r in c["rules"])))
    body += section("01", "Channel doctrine", None, '<div class="grid g2">%s</div>' % "".join(cards))

    laws = "".join(
        '<div class="card accent-mag"><span class="sec-num">%02d</span><h3 style="margin-top:6px">%s</h3><p>%s</p></div>'
        % (i + 1, e(l["t"]), l["p"]) for i, l in enumerate(D.LAWS))
    body += section("02", "The eight laws",
                    "These are the decisions that stop the estate drifting back into noise. Each one is "
                    "enforceable in <code>Notifications::DispatchWorker</code> rather than trusted to "
                    "whoever writes the next template.",
                    '<div class="grid g2">%s</div>' % laws)

    body += section("03", "The escalation ladder",
                    "Every reminder sequence uses the same four rungs. Tone escalates by specificity, "
                    "never by volume, and nothing follows the fourth.",
                    """
<div class="grid g4">
  <div class="card accent-flow"><span class="lbl">Rung 1 · neutral</span>
    <p class="tight">State the fact and the opening hours. Mention no charge, because none applies.</p>
    <span class="ex" style="display:block;font-family:var(--mono);font-size:.84rem;background:var(--sunk);padding:9px 11px;border-radius:3px;margin-top:10px">Your parcel is still at Shell Kileleshwa, open until 21:00.</span></div>
  <div class="card accent-lock"><span class="lbl">Rung 2 · specific</span>
    <p class="tight">Name the deadline, the rate that follows it, and the alternative.</p>
    <span class="ex" style="display:block;font-family:var(--mono);font-size:.84rem;background:var(--sunk);padding:9px 11px;border-radius:3px;margin-top:10px">Free storage ends Fri 18:00. After that: Ksh 50/hr.</span></div>
  <div class="card accent-org"><span class="lbl">Rung 3 · consequence</span>
    <p class="tight">The charge has started. Say how to stop it in the same line.</p>
    <span class="ex" style="display:block;font-family:var(--mono);font-size:.84rem;background:var(--sunk);padding:9px 11px;border-radius:3px;margin-top:10px">Ksh 50/hr, Ksh 1,250 so far. It stops the moment you collect.</span></div>
  <div class="card accent-ink"><span class="lbl">Rung 4 · final</span>
    <p class="tight">A fact already in motion, a total, and a human to talk to. Then silence.</p>
    <span class="ex" style="display:block;font-family:var(--mono);font-size:.84rem;background:var(--sunk);padding:9px 11px;border-radius:3px;margin-top:10px">Last day: it goes back to the sender today.</span></div>
</div>""")

    sc = D.STORAGE_CLOCK
    sc_rules = "".join('<div class="card"><span class="lbl">%s</span><p class="tight">%s</p></div>'
                       % (e(a), b) for a, b in sc["rules"])
    body += section("04", "The storage clock",
                    "The one fact that most copy on this site depends on, and the easiest to get wrong.",
                    '<div class="card accent-org"><h3>%s</h3><p>%s</p></div>'
                    '<div class="grid g2" style="margin-top:16px">%s</div>'
                    % (e(sc["headline"]), sc["body"], sc_rules),
                    anchor="storage")

    toks = "".join('<tr><td class="id">{{%s}}</td><td>%s</td></tr>' % (e(k), e(v))
                   for k, v in sorted(D.SAMPLES.items()))
    body += section("05", "Tokens",
                    "The value in the right column is what the character counts on this site are measured "
                    "with — the longest realistic value, not a short one.",
                    '<div class="scroller"><table><thead><tr><th>Token</th><th>Measured as</th></tr>'
                    '</thead><tbody>%s</tbody></table></div>' % toks)
    body += '<div class="wrap"><div class="endrule"></div></div>'
    return page("channels.html", "Channels & rules · Pinned Communications",
                "Channel doctrine, the eight laws, the escalation ladder and the token set.", body)


def build_lane(lane):
    tps = by_lane(lane["key"])
    h = lane["hook"]
    body = phead(lane["title"],
                 "%d touchpoints · %d SMS on a journey that works" % (len(tps), len(sms_steps(lane["key"], True))),
                 lane["title"], e(lane["who"]))
    body += navbar(lane["page"])
    body += section("01", "What they are here for", None, """
<div class="grid g2">
  <div class="card %s"><span class="lbl">The job they hire Pinned for</span>
    <h3 style="margin-top:8px">%s</h3>
    <p>Every message on this page is judged against that sentence. If it does not help with
      it, or protect it, it should not be sent.</p></div>
  <div class="card"><span class="lbl">The hook</span>
    <div class="kv">
      <div><b>Trigger</b><span>%s</span></div>
      <div><b>Action</b><span>%s</span></div>
      <div><b>Reward</b><span>%s</span></div>
      <div><b>Investment</b><span>%s</span></div>
    </div></div>
</div>""" % (lane["colour"], e(lane["job"]), e(h["trigger"]), e(h["action"]),
             e(h["reward"]), e(h["investment"])))

    stages = []
    seen = []
    for t in tps:
        if t["stage"] not in seen:
            seen.append(t["stage"])
    for stage in seen:
        items = "".join(render_tp(t) for t in tps if t["stage"] == stage)
        stages.append('<h3 style="margin-top:38px">%s</h3>%s' % (e(stage), items))
    n_path, n_all = len(sms_steps(lane["key"], True)), len(sms_steps(lane["key"]))
    body += section("02", "The SMS journey",
                    "Every moment in order, and the channel that carries it. Highlighted rows cost an SMS: "
                    "<b>%d on a journey that works</b>, %d more only when something goes wrong. A row "
                    "numbered <b>+</b> is one of those; everything unhighlighted is a deliberate decision "
                    "not to spend an SMS." % (n_path, n_all - n_path),
                    render_journey(lane["key"]), anchor="journey")
    body += section("03", "Touchpoints", None, "".join(stages))
    body += '<div class="wrap"><div class="endrule"></div></div>'
    return page(lane["page"], "%s · Pinned Communications" % lane["title"],
                "Every Pinned message to %s." % lane["title"].lower(), body)


def build_library():
    body = phead("Copy library", "%d touchpoints, every channel" % len(D.TOUCHPOINTS),
                 "The library",
                 "One table of everything Pinned sends. Filter by lane or status; each ID links to "
                 "the full copy, the live version and the rules behind it.")
    body += navbar("library.html")
    lane_btns = "".join('<button class="themer" data-f="lane" data-v="%s">%s</button>' % (l["key"], e(l["title"]))
                        for l in LANES_ORDERED)
    status_btns = "".join('<button class="themer" data-f="status" data-v="%s">%s</button>' % (k, v)
                          for k, v in STATUS_WORD.items())
    body += section("01", "Everything, in one table", None, """
<div class="chips" style="gap:8px;margin-bottom:6px">
  <button class="themer" data-f="all" data-v="all">All %d</button>%s
</div>
<div class="chips" style="gap:8px">%s</div>
<div class="scroller"><table id="lib">
<thead><tr><th>ID</th><th>Touchpoint</th><th>Timing</th><th>Channels</th><th>Status</th><th>Template key</th></tr></thead>
<tbody>%s</tbody></table></div>
<script>
  var rows = Array.prototype.slice.call(document.querySelectorAll("#lib tbody tr"));
  document.querySelectorAll("[data-f]").forEach(function (b) {
    b.addEventListener("click", function () {
      var f = b.dataset.f, v = b.dataset.v;
      rows.forEach(function (r) {
        r.style.display = (f === "all" || r.dataset[f] === v) ? "" : "none";
      });
    });
  });
</script>""" % (len(D.TOUCHPOINTS), lane_btns, status_btns, matrix_rows(D.TOUCHPOINTS)))

    rewrites = [t for t in D.TOUCHPOINTS if t["old"]]
    cards = []
    for t in rewrites:
        new_sms = [p for c, p in t["msgs"] if c in ("sms", "whatsapp")]
        after = "".join(render_sms(p) for p in new_sms) if new_sms else \
            "".join(render_msg(c, p) for c, p in t["msgs"])
        cards.append("""
<div class="card">
  <div class="tp-head" style="background:transparent;border:0;padding:0 0 12px">
    <span class="tp-id">%s</span>
    <span class="tp-title"><h3>%s</h3><p>%s</p></span>
    <span class="tp-meta">%s</span>
  </div>
  <div class="tp-cols">
    <div>%s</div>
    <div>%s</div>
  </div>
  <p style="margin-top:10px"><a href="%s#%s">Rules and channels →</a></p>
</div>""" % (e(t["id"]), e(t["name"]), e(t["intent"]), badge(t["status"]),
             render_old(t["old"]), after, D.LANE_BY_KEY[t["lane"]]["page"], e(t["id"])))
    body += section("02", "Rewrites, side by side",
                    "%d of the live templates change. None of them need a migration — every one is a "
                    "<code>body</code> edit against an existing <code>NotificationTemplate</code> key."
                    % len(rewrites),
                    '<div class="grid">%s</div>' % "".join(cards))
    body += '<div class="wrap"><div class="endrule"></div></div>'
    return page("library.html", "Copy library · Pinned Communications",
                "Every Pinned message, with the live version beside the rewrite.", body)


def build_gaps():
    c = counts()
    body = phead("Build order", "From map to shipped", "What to build, in what order",
                 "Four weeks, smallest blast radius first: stop the damage, rewrite what already "
                 "fires, close the map's gaps, then make the system enforce its own rules.")
    body += navbar("gaps.html")
    body += """
<div class="wrap"><div class="stats">
  <div><b>%(total)d</b><small>touchpoints</small></div>
  <div><b>%(live)d</b><small>live today</small></div>
  <div><b>%(partial)d</b><small>partial</small></div>
  <div><b>%(gap)d</b><small>not built</small></div>
  <div><b>%(change)d</b><small>channel changes</small></div>
  <div class="hot"><b>%(defect)d</b><small>defects</small></div>
</div></div>""" % dict(total=len(D.TOUCHPOINTS), **c)

    pvp = "".join(
        '<div class="card"><h3>%s</h3><p>%s</p><p style="color:var(--text)">%s</p></div>'
        % (e(x["t"]), x["p"], x["v"]) for x in D.PACK_VS_PAGE)
    body += section("01", "The pack against the page",
                    "The receiver pack and the live receiver page disagreed in six places. The page wins "
                    "on voice, because it is the surface the receiver is holding when the SMS arrives; "
                    "the pack wins on triggers, because operations knows what fires when.",
                    '<div class="grid g2">%s</div>' % pvp,
                    anchor="packvspage")

    changes = [t for t in D.TOUCHPOINTS if t["status"] in ("change", "retire")]
    srcs = "".join('<div><b>%s</b><p>%s</p></div>' % (e(a), e(b)) for a, b in D.REVIEW_SOURCES)
    body += section("02", "What the reviews changed",
                    "Three documents and an annotated screenshot came back from the team on 13 October. "
                    "Every channel decision below is theirs; the copy follows their wording wherever they "
                    "wrote it.",
                    '<div class="srcs">%s</div>'
                    '<div class="scroller" style="margin-top:22px"><table><thead><tr><th>ID</th>'
                    '<th>Touchpoint</th><th>Timing</th><th>Channels now</th><th>Status</th>'
                    '<th>Template key</th></tr></thead><tbody>%s</tbody></table></div>'
                    % (srcs, matrix_rows(changes)))

    qs = "".join('<div><span class="who">%s</span><h4>%s</h4><p>%s</p></div>'
                 % (e(q["who"]), e(q["q"]), e(q["why"])) for q in D.OPEN_QUESTIONS)
    body += section("03", "Open questions",
                    "Decisions that are not ours to make. Each one blocks copy that is otherwise "
                    "written and ready.",
                    '<div class="qs">%s</div>' % qs)

    weeks = []
    for w in D.BUILD_ORDER:
        items = "".join(
            ('<li>%s</li>' % i[1]) if i[0] == "\u2014" else ('<li><b>%s</b> — %s</li>' % (e(i[0]), i[1]))
            for i in w["items"])
        weeks.append('<div class="card accent-mag"><span class="lbl">%s</span>'
                     '<h3 style="margin-top:8px">%s</h3><ul>%s</ul></div>'
                     % (e(w["w"]), e(w["t"]), items))
    body += section("04", "Four weeks", None, '<div class="grid g2">%s</div>' % "".join(weeks))

    defects = [t for t in D.TOUCHPOINTS if t["status"] == "defect"]
    body += section("05", "The defects",
                    "Not copy preferences. Each one is doing measurable damage every day it ships.",
                    "".join(render_tp(t) for t in defects))

    gaps = [t for t in D.TOUCHPOINTS if t["status"] == "gap"]
    body += section("06", "Not built",
                    "%d touchpoints the map asks for, or the hook needs, that nothing sends today."
                    % len(gaps),
                    '<div class="scroller"><table><thead><tr><th>ID</th><th>Touchpoint</th>'
                    '<th>Timing</th><th>Channels</th><th>Status</th><th>Template key</th></tr></thead>'
                    '<tbody>%s</tbody></table></div>' % matrix_rows(gaps))

    notes = "".join('<div class="kv"><div><b style="min-width:230px">%s</b><span>%s</span></div></div>'
                    % (a, b) for a, b in D.CODE_NOTES)
    body += section("07", "Where this lands in the code",
                    "Nothing here needs a new messaging stack. The seams already exist.",
                    '<div class="card">%s</div>' % notes)
    body += '<div class="wrap"><div class="endrule"></div></div>'
    return page("gaps.html", "Build order · Pinned Communications",
                "The defects, the gaps and a four-week build order.", body)


LANES_ORDERED = D.LANES
SITE_DESC = ("Every message Pinned sends — senders, receivers, runners, hosts, admin and prospects — "
             "with the copy, the rules and the build order.")


def main():
    built = [build_index(), build_principles(), build_channels()]
    for lane in LANES_ORDERED:
        built.append(build_lane(lane))
    built.append(build_library())
    built.append(build_gaps())
    print("built %d pages: %s" % (len(built), ", ".join(built)))


if __name__ == "__main__":
    main()
