# Pinned Communications

The unified communications and messaging system for Pinned Flow: every message
sent to a sender, a receiver, a runner, a host, an admin-driven job change, or
someone who has not signed up yet — what fires it, which channel carries it,
what it says, and why it says it that way.

A static site. No build step on Netlify; pages are generated locally and
committed.

**63 touchpoints** — 10 live today, 12 partial, 28 not built, 10 channel
changes, 2 defects. Every lane page opens with its **SMS journey**: the moments in order,
which channel carries each one, and how many of them cost an SMS.

## Where it came from

| Source | What it contributed |
| --- | --- |
| `PINNED COMMUNICATION MAP.pdf` (9 Oct 2026) | The touchpoint inventory for runners, virtual hosts, admin, senders and receivers. Every touchpoint traceable to it carries a `Map · …` source line. |
| `pinned-core` `db/seeds.rb` | The 33 live `NotificationTemplate` bodies, quoted verbatim as “Live today” beside each rewrite. |
| `pinned-core` `app/services/routing/batch_offer/build.rb`, `app/workers/notifications/dispatch_worker.rb`, `app/services/fcm_sender.rb` | The runner offer push, and the three code-level causes of the duplicate-notification defect. |
| `PINNED BRAND GUIDE2.pdf` | Colour, type and the rule that DM Mono is reserved for codes and tracking references. The brand guide has no verbal identity section — the Voice page is the gap it leaves. |
| Runner lock-screen capture, 9 Oct 2026 | Four identical offer notifications in 24 minutes. The evidence the whole thing is built around. |

### Round two — the team review, 13 October 2026

| Source | What it changed |
| --- | --- |
| `Senders Communication Touchpoints.docx` | Copy rewrites and a keep/remove recommendation on every sender touchpoint. Four messages move to in-app only. |
| `PINNED RUNNERS COMMS.docx` | Six runner messages rewritten warmer, in the team's own voice. Used as written. |
| `PINNED HOST TOUCHPOINTS REVIEW .docx` | Channel decisions, plus three policy questions that block copy. |
| Runner comms screenshot | Keep / move markings per channel, and four messages that do not exist: suspension, reinstatement, account deletion, and the sign-in code that should become a PIN. |

Their decisions live in a `REVIEW` merge layer at the end of `_build/data.py`
rather than edited into the round-one block, so the provenance of every change
stays readable. `NEW_TOUCHPOINTS` adds what the review asked for, and `ORDER`
sets the display sequence.

Two things the review asked for that are not channel decisions:

- **The warmth layer** (`principles.html#warmth`) — round one answered *what
  happened, what do I do* and never *why should I care*. Six warmth moves, and a
  per-lane budget, because warmth spent everywhere is warmth nobody feels.
- **The SMS journey** (`JOURNEYS` in `data.py`) — on every lane page. Steps
  numbered `+` only happen when something goes wrong, so the budget quoted is the
  budget for a journey that works.

### Round three — the receiver lane, 27 October 2026

Two inputs, and they disagreed.

| Source | What it contributed |
| --- | --- |
| `PINNED RECEIVERS COMMS(1).docx` | The lane missing from round two: branch triggers, the waiting ladder, and a rung 4 that still offers a doorstep delivery on the last day. |
| **publicchoicepage.netlify.app** | The page every receiver SMS links to — and from today the reference for tone. |

The page wins on voice, because it is the surface a receiver is holding when the
SMS arrives: if the two do not sound like the same company, the link looks like
a phishing link. The pack wins on triggers, because operations knows what fires
when. Six specific disagreements are laid out on the Build order page under
**The pack against the page**.

The substantive one: the pack sells the paid doorstep delivery and never
mentions that collecting is free, while the live page offers free collection
four times over and adds *no charge, no pressure*. Free is named first now, in
every variant.

The page also carries three touchpoints neither the Communication Map nor the
pack had — *your runner can't find you*, the priced relocation, and the runner
rating — and it supplies the real sample values, so character counts here are
counts of the actual thing.

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
index.html          the map: evidence, the review, the six lanes, every touchpoint
principles.html     eight principles, the warmth layer, the clarity contract, the hook, the glossary
channels.html       channel doctrine, the eight laws, the escalation ladder, tokens
senders.html        12 touchpoints ·  4 SMS on a journey that works
receivers.html      17 ·  4
runners.html        15 ·  4
hosts.html           9 ·  1
admin.html           5 ·  4
prospects.html       5 ·  3
library.html        the full table, filterable, plus every rewrite side by side
gaps.html           what the review changed, open questions, defects, four-week build order
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
  review="what the team decided about channels, 13 Oct",
  warmth="the warmth move this message uses, if any",
  notes=[("warn", "defects and evidence"), ("hook", "hook commentary")])
```

Statuses: `live`, `partial`, `gap`, `defect`, `change` (the message stays, the
channel mix does not) and `retire` (it goes away — a retired touchpoint carries
no copy, which the lint allows only for that status).

Character counts are measured with the longest realistic token values
(`SAMPLES` in `data.py`) filled in, not with the tokens left empty. An SMS that
fits “Jay” and breaks on “Wanjiru” has not been written.

Bump `BUILD` in `data.py` when assets change; it is the `?v=` cache buster.

## Status

Draft. Nothing here has been applied to `pinned-core`. Most rewrites are
`NotificationTemplate#body` edits against existing keys — no migration — and the
defects and channel changes are the code work listed on the Build order page.

Decisions that are not ours to make and that block copy which is otherwise
written are all on the Build order page under Open questions. The one at the top
is free storage: the receiver pack says six hours in one place and twelve in
another, and this site carries 24 countable hours with the clock paused
overnight. Nothing was changed on the strength of a draft, because the ladder,
the charging trigger and the sender-side return all hang off that number.
