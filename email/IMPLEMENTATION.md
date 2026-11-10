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

## 3. Three sending classes

They differ for legal and deliverability reasons, not visual ones. Same shell
for all three.

| class | examples | unsubscribe | sending domain |
|---|---|---|---|
| **Transactional** | collection code, ready for collection, collected, host statement | no | `mail.pinnedflow.app` — never throttled |
| **Lifecycle / service** | new Pod, new feature, service change | yes + preferences | separate marketing subdomain |
| **Prospecting** | PSV operators, cold business senders | yes, prominent | third subdomain, warmed slowly |

**Keep them on separate subdomains.** A complaint from cold outreach must not
be able to delay the collection-code email that lets someone open a Pod. Check the lawful
basis for the prospecting list under the Data Protection Act 2019 before it
goes out — that is a question for counsel, not for this document.

---

## 4. Why the markup looks like 2004

Do not "modernise" it. Each of these is load-bearing:

- **Tables and inline CSS.** Outlook renders with Word's engine. No flexbox,
  no grid, no external stylesheet.
- **XHTML transitional doctype + the MSO conditional block.** Without it
  Outlook scales everything by its own DPI.
- **The VML `<v:roundrect>` behind the CTA.** Without it the magenta button is
  a blue underlined link in Outlook.
- **`mso-line-height-rule: exactly`** on every text cell, or Outlook ignores
  line height.
- **The hidden preheader div.** It is the grey line beside the subject in the
  inbox. Left empty, clients scrape the first visible text instead.
- **The dark-mode block and the two logos.** Gmail and Apple Mail invert
  colours on their own and do it badly; the `@media (prefers-color-scheme)` and
  `[data-ogsc]` rules hold the brand and swap to the white-wordmark logo.
  Blocks 3 and 4 deliberately do **not** invert — anthracite and Locker Green
  are brand grounds, not theme colours.
- **DM Sans only renders in Apple Mail and iOS.** Gmail and Outlook strip the
  `@import` and fall back to Arial. That is expected. Do not set headlines as
  images to force the font — it costs accessibility and spam score.

---

## 5. Brand rules the markup already encodes

From the Growth Desk playbook §06–07 and the comms principles:

- **Flow lane colours only.** `#C8005A` `#C0DB86` `#7AAF2A` `#E8520A` `#2B2B2B`.
  **PinnedOS Blue never appears on a Flow asset.**
- **DM Mono is reserved for codes, prices, timestamps and IDs.** In email it is
  also an anti-phishing signal — it is the fastest way a receiver tells a real
  Pinned message from a copy.
- **One call to action, and it always carries the link.** No gating, no "reply
  to find out". The address travels with the call.
- **Figures come from the live board, pulled the morning you send, and dated.**
  No ratings. The retired 480 / 12,000+ / 4.8 figures stay retired.
- **"UKO WAPI?" is rationed.** It belongs to the sign-up message and nowhere
  else in the sender journey.

---

## 6. Before the first send

- [ ] Logos live at a stable HTTPS path; `{{asset_base}}` points at it
- [ ] SPF, DKIM and **DMARC at `p=quarantine` or `p=reject`** — not `p=none`
- [ ] `List-Unsubscribe` and `List-Unsubscribe-Post` headers on bulk sends
- [ ] A `text/plain` alternative on every send — missing it costs deliverability
- [ ] From name set **per class**, and never `noreply@` on a class whose
      success is a reply:
      - transactional — `Pinned <notifications@pinnedflow.app>`
      - lifecycle — `Pinned <notifications@pinnedflow.app>`
      - prospecting — `Pinned Flow <hello@pinnedflow.app>`, **monitored**. This
        email ends on *"Book a 15-minute walkthrough… or call"*; a SACCO
        manager's first instinct is to hit reply, and `noreply@` throws away
        the conversion on the one class where a reply *is* the conversion.
- [ ] Rendered in Gmail web, Gmail Android, Apple Mail iOS, Outlook desktop,
      and Gmail dark mode

**BIMI — the logo beside the subject line — is a 2027 item.** It needs DMARC
enforcement plus a Verified Mark Certificate, which needs a registered
trademark on the mark and runs ~$1,000/year. Do the DMARC work now for its own
sake; treat the avatar as later.

---

## 7. Open, and needing a decision

1. ~~**`pinnedflow.com` vs `pinnedflow.app`**~~ — **settled, 10 Nov.** It was
   not a choice. A DNS lookup returns *nothing* for `pinnedflow.com`: no MX, no
   SPF, no nameservers. The domain is not delegated, so mail to
   `hello@pinnedflow.com` cannot reach anybody. `pinnedflow.app` is the real
   one — Zoho MX, DigitalOcean NS, `v=spf1 include:zohomail.com ~all` — and is
   already the only domain in a live From header (`devise.rb` sends as
   *Pinned Support <support@pinnedflow.app>*).

   **Use `.app` everywhere.** Three live SMS in `pinned-core` still end on
   *"Questions? hello@pinnedflow.com"* (`batch_subscriber.rb`,
   `runner_subscriber.rb`, `route_batch/admin_actions.rb`), and
   `config/content/site.yml` and `legal.yml` route refunds and complaints
   there — all dead letters. `dwell/notifier.rb` already says `.app`.

   **Still to confirm:** that `hello@` and `notifications@` mailboxes are
   provisioned on the Zoho tenant. DNS cannot answer that.
2. **Does Pinned integrate with a partner's parcel software, or does their
   clerk re-enter it?** `psv-pitch.html` step 01 says *"we work alongside it"*.
   Confirmed by the founder as true; the implementation has to make it true.
3. **Board figures at send time.** Needs a small endpoint or cached read of
   the `/vhost` board so `board_*` can resolve. Until it exists, those four
   tokens have nothing behind them.
