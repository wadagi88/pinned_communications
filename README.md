# Pinned Communications

The unified communications and messaging system for Pinned Flow: every message
sent to a sender, a receiver, a runner, a host, an admin-driven job change, or
someone who has not signed up yet — what fires it, which channel carries it,
what it says, and why it says it that way.

A static site. No build step on Netlify; pages are generated locally and
committed.

**49 touchpoints** — 13 live today, 16 partial, 17 not built, 3 defects.

## Where it came from

| Source | What it contributed |
| --- | --- |
| `PINNED COMMUNICATION MAP.pdf` (9 Oct 2026) | The touchpoint inventory for runners, virtual hosts, admin, senders and receivers. Every touchpoint traceable to it carries a `Map · …` source line. |
| `pinned-core` `db/seeds.rb` | The 33 live `NotificationTemplate` bodies, quoted verbatim as “Live today” beside each rewrite. |
| `pinned-core` `app/services/routing/batch_offer/build.rb`, `app/workers/notifications/dispatch_worker.rb`, `app/services/fcm_sender.rb` | The runner offer push, and the three code-level causes of the duplicate-notification defect. |
| `PINNED BRAND GUIDE2.pdf` | Colour, type and the rule that DM Mono is reserved for codes, OTPs and tracking references. The brand guide has no verbal identity section — the Voice page is the gap it leaves. |
| Runner lock-screen capture, 9 Oct 2026 | Four identical offer notifications in 24 minutes. The evidence the whole thing is built around. |

Two lanes are not in the PDF and were added:

- **Prospects** — the “any potential” audience: marketplace-group replies,
  enquiries, abandoned quotes, and the receiver→sender conversion, which is the
  largest warm audience Pinned has.
- **R7, the runner offer push** — the single highest-volume message in the
  business, live in code and absent from the map.

## Build

```sh
./_build/build.sh
```

Generates all 11 pages from `_build/data.py` and then lints: internal links,
anchors, unmeasured tokens, SMS segment counts and push title/body lengths. A
failure exits non-zero.

Preview locally on port 3110 (`comms` in `pinned-app2/.claude/launch.json`), or:

```sh
cd /Users/alldan/pinned-comms && python3 -m http.server 3110
```

## Deploy to Netlify

Drag-and-drop the folder, or connect the repo with:

- **Build command** — none
- **Publish directory** — `.`

`netlify.toml` sets the security headers and makes HTML and assets revalidate,
so a deploy is never masked by a phone's cache. Pages carry
`noindex, nofollow` — this is an internal working document.

## Structure

```
index.html          the map: evidence, the six lanes, every touchpoint
principles.html     eight principles, the clarity contract, the hook framework, the glossary
channels.html       channel doctrine, the eight laws, the escalation ladder, tokens
senders.html        10 touchpoints
receivers.html      11
runners.html        10
hosts.html           8
admin.html           5
prospects.html       5
library.html        the full table, filterable, plus every rewrite side by side
gaps.html           the three defects, what is missing, a four-week build order
assets/comms.css    one stylesheet; brand tokens shared with the Growth Desk
_build/data.py      all content — touchpoints, copy, principles, laws
_build/build.py     the generator
_build/lint.py      the checks
```

## Editing

Everything is in `_build/data.py`. A touchpoint is a dict:

```python
T(id="C2", lane="receiver", stage="Arrived", name="It is here — collect with this code",
  trigger="Parcel reaches the destination pod or station",
  timing="On arrival scan", channels=["sms", "in_app"],
  status="live", key="parcel_arrived", source="Map · Receiver 1", hook="Action",
  intent="One line on what this message is for.",
  old="the verbatim copy that is live today, or None",
  msgs=[("sms", "..."), ("in_app", ("title", "body"))],
  rules=["the decisions behind the copy"],
  notes=[("warn", "defects and evidence"), ("hook", "hook commentary")])
```

Character counts are measured with the longest realistic token values
(`SAMPLES` in `data.py`) filled in, not with the tokens left empty. An SMS that
fits “Jay” and breaks on “Wanjiru” has not been written.

Bump `BUILD` in `data.py` when assets change; it is the `?v=` cache buster.

## Status

Draft for review. Nothing here has been applied to `pinned-core`. The rewrites
are `NotificationTemplate#body` edits against existing keys — no migration —
and the three defects are code changes listed on the Build order page.
