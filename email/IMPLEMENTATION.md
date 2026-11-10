# Pinned email — implementation brief

One shell, seven blocks, one worked example. You do not accumulate templates;
you accumulate emails made from one shell. A collection code, a host statement,
a new-Pod notice and a cold pitch are the same file with different blocks in
the middle.

| file | what it is |
|---|---|
| `pinned-email-template.html` | the shell — doctype, head, logo, card, footer, dark mode |
| `pinned-email-blocks.html` | seven `<tr>` blocks that drop into the card |
| `psv-pitch.html` | a finished email built from blocks 1, 5, 7, 4 and 6 |
| `assets/pinned-email-logo-*.png` | the lockup at 2×, light and dark |

---

## 1. Where each piece goes

**The shell → `app/views/layouts/mailer.html.erb` in `pinned_systemadmin`.**
That file exists and currently carries no brand. Everything between the
headline block and the footer becomes `yield`.

**The blocks → the Messaging Centre composer.** They are what a person inserts
into the body when writing a campaign. They already use `{{…}}`, the same merge
syntax the composer documents.

**The example → one record in `AdminApi.messaging.templates`**, with
`channel: "email"` and `kind: "promotional"`.

**The logos → a public HTTPS path on `pinnedflow.app`.** This is the only part
that touches the main site. Email clients cannot read anything else — not a
`file://` path, not an asset-pipeline digest URL that changes on deploy, and
not SVG, which Gmail and Outlook strip. Serve them at a stable path that
survives redeploys, then set `{{asset_base}}` to that folder.

---

## 2. Merge tokens — already built

Branch `messaging/merge-tokens` on `pinned_systemadmin` (pushed) adds
`AdminApi::Fixture::Messaging.merge_tokens(channel:, kind:)` and points both
the template editor and the notification editor at it. Before that change each
composer inlined its own hash, so a token could exist in one and be missing
from the other — which was already true of `pod`, `runner`, `dest`, `amount`
and `link`.

The HTTP seam carries the matching stub:
`GET /admin/v1/messaging/merge_tokens?channel=&kind=`

**What the backend has to resolve, and when:**

| group | tokens | resolved |
|---|---|---|
| base | `name` `code` `pod` `station` `otp` `runner` `dest` `hours` `amount` `month` `link` | per recipient, at send |
| board | `board_businesses` `board_riders` `board_parcels` `board_date` | **at send, from the live /vhost board** |
| list | `unsubscribe_url` `preferences_url` | per recipient, at send |

**The gating is deliberate, not cosmetic.**

| channel | kind | tokens offered |
|---|---|---|
| sms | transactional | 11 |
| sms | promotional | 15 |
| email | promotional | **17** |
| email | transactional | 11 |

`unsubscribe_url` and `preferences_url` appear **only on promotional email** —
never on transactional, where an unsubscribe link does not belong, and never on
SMS, which opts out with STOP. `board_*` appear only on promotional, and only
as tokens: a figure typed by hand is how a stale number reaches a customer.

**`unsubscribe_url` must be a unique per-recipient token.** A shared link
unsubscribes nobody, and Gmail and Yahoo require a unique one to build the
`List-Unsubscribe-Post` one-click header for bulk senders.

---

---

## 3. The rules are not in this file

They are on the **Email page** of the communications surface:
<https://pinnedcomms.netlify.app/email.html>

This file is canonical for **destinations** — which file goes to which repo,
and what the backend has to resolve. The page is canonical for **rules**.
Stating a rule in both places is how the two drift, and whoever is
implementing follows whichever they found first.

What moved there, and why you want it rather than a copy of it:

| on the page | what it settles |
|---|---|
| [Where mail comes from](https://pinnedcomms.netlify.app/email.html#senders) | The three composition surfaces — a person in Zoho, the Messaging Centre, the system — and which of them can share a template. Zoho cannot, and the page says what it strips. |
| [What is actually configured](https://pinnedcomms.netlify.app/email.html#dns) | The live DNS. **There is no DMARC record at all**, and SPF authorises Zoho and nobody else — so two items that read as pre-send checks are build items. |
| [Three sending classes](https://pinnedcomms.netlify.app/email.html#classes) | Transactional, lifecycle, prospecting: unsubscribe, From line and subdomain for each. |
| [The rules](https://pinnedcomms.netlify.app/email.html#rules) | Nine, including the two codes, never `noreply@` on a class whose success is a reply, and the subject-line rule scoped to transactional only. |
| [Why the markup looks like 2004](https://pinnedcomms.netlify.app/email.html#markup) | Every piece that looks removable and is not. **Read this before editing the HTML.** |
| [Before the first send](https://pinnedcomms.netlify.app/email.html#checklist) | The eight things, in the order they unblock each other. |

Check the lawful basis for the prospecting list under the Data Protection Act
2019 before it goes out — that is a question for counsel, not for this
document, and not for the page either.
