# -*- coding: utf-8 -*-
"""Pinned Communications — the content.

Everything the site renders lives here. Touchpoints carry both the copy that
is live in pinned-core today (verbatim, from db/seeds.rb) and the proposed
replacement, so the gap between the two is never an argument about memory.

Status values
  live    — a NotificationTemplate exists and fires
  partial — something fires, but it misses a channel, a rung, or the point
  gap     — the map asks for it and nothing sends it
  defect  — it fires, and what it does is wrong
"""

BUILD = 13
UPDATED = "27 October 2026 · receiver lane against the live page"

SITE = dict(
    name="Pinned Communications",
    tagline="One voice across every parcel, every runner, every pod.",
)

NAV = [
    ("index.html", "The map"),
    ("principles.html", "Voice"),
    ("channels.html", "Channels & rules"),
    ("senders.html", "Senders"),
    ("receivers.html", "Receivers"),
    ("runners.html", "Runners"),
    ("hosts.html", "Hosts"),
    ("admin.html", "Admin"),
    ("prospects.html", "Prospects"),
    ("library.html", "Copy library"),
    ("gaps.html", "Build order"),
]

CHANNEL_LABEL = {
    "sms": "SMS", "push": "Push", "in_app": "In-app",
    "email": "Email", "whatsapp": "WhatsApp", "call": "Call",
}
CHANNEL_CLASS = {
    "sms": "sms", "push": "push", "in_app": "inapp",
    "email": "email", "whatsapp": "whatsapp", "call": "voice",
}

# Representative values, so a character count means something. These are the
# longest realistic values we have seen in production data, not short ones —
# a message that fits a short name and breaks on a long one is not written.
SAMPLES = {
    "name": "Wanjiru", "code": "PN-4K7Q2", "otp": "840 213", "pod": "Shell Kileleshwa",
    "station": "Shell Kileleshwa", "dest": "Lavington", "origin": "Westlands",
    "runner": "Brian M.", "hours": "24", "amount": "1,250", "rate": "50",
    "deadline": "Fri 18:00", "link": "pinnedflow.app/r", "track_url": "pinnedflow.app/t/4K7Q2",
    "from": "Sokoni Stores", "batch": "B-2291", "docs": "driving licence",
    "reason": "the photo was unreadable", "address": "Ngong Road, Kilimani",
    "closing_time": "21:00", "since": "06:40 today", "payout": "640",
    "stops": "4", "km": "15.8", "eta": "14:20", "time": "13:42",
}

LANES = [
    dict(key="sender", page="senders.html", title="Senders",
         colour="accent-mag",
         who="Anyone who books a parcel — an individual in the app, or a business through a virtual host.",
         job="Know it is handled, and be able to prove it was.",
         hook=dict(
             trigger="Booking confirmation lands before they have left the pod counter.",
             action="Drop the parcel, or tap once to send a runner instead.",
             reward="Proof of delivery with a name, a time and a photo — the moment that makes the next send automatic.",
             investment="Saved addresses and repeat receivers; the second send is three taps.")),
    dict(key="receiver", page="receivers.html", title="Receivers",
         colour="accent-lock",
         who="The person the parcel is for. Often has never heard of Pinned before the first SMS.",
         job="Get the parcel without rearranging their day.",
         hook=dict(
             trigger="'Your parcel from Sokoni Stores is at Shell Kileleshwa.'",
             action="Walk in, read the code, collect.",
             reward="Free-storage countdown they beat, and a door-delivery escape hatch they did not expect.",
             investment="Saving the delivery address turns the next parcel into a doorstep drop.")),
    dict(key="runner", page="runners.html", title="Runners",
         colour="accent-flow",
         who="The rider on the road. Pinned is their income, and their phone is their workplace.",
         job="Fill the day with jobs worth taking, and get paid without chasing anyone.",
         hook=dict(
             trigger="An offer push carrying the money, the distance and the clock.",
             action="One tap to accept.",
             reward="Variable by design — payout, stop count and distance differ every time; the earnings reveal at completion is the hit.",
             investment="Documents kept current, rating, completed runs — all of it buys better batches.")),
    dict(key="host", page="hosts.html", title="Hosts",
         colour="accent-org",
         who="Virtual hosts (business senders and parcel handlers) and pod hosts (the physical site).",
         job="Run the counter without surprises, and see the money each week.",
         hook=dict(
             trigger="'A runner is 12 minutes away for 4 parcels.'",
             action="Have them at the counter, scan, release the code.",
             reward="The weekly settlement figure — the number they open the email for.",
             investment="Branch defaults, cut-off times and handover habits that make the station faster each week.")),
    dict(key="admin", page="admin.html", title="Admin interventions",
         colour="accent-ink",
         who="Operations acting on a live job: reassigning, floating back, chasing a delay.",
         job="Change the plan without making anyone feel blamed or lost.",
         hook=dict(
             trigger="A human decision, pushed to the person it affects within seconds.",
             action="Accept the new state, or say what is happening.",
             reward="Being told early, before it becomes their problem.",
             investment="Runners who are told the truth about reassignments keep taking offers.")),
    dict(key="prospect", page="prospects.html", title="Prospects",
         colour="accent-ink",
         who="Everyone who has met Pinned but not sent anything: group members, enquirers, abandoned quotes, and every receiver who has only ever collected.",
         job="Find out, in one line, whether Pinned solves their problem.",
         hook=dict(
             trigger="A reply in the group, or an SMS an hour after they checked a price.",
             action="Get a quote. Ten seconds, no account.",
             reward="A real price and a real time, instantly — not a callback.",
             investment="The quote keeps their route; signing up is one field.")),
]
LANE_BY_KEY = {l["key"]: l for l in LANES}


def T(**kw):
    kw.setdefault("msgs", [])
    kw.setdefault("rules", [])
    kw.setdefault("notes", [])
    kw.setdefault("old", None)
    kw.setdefault("key", None)
    kw.setdefault("source", None)
    kw.setdefault("hook", None)
    return kw


TOUCHPOINTS = [

    # ───────────────────────── SENDERS ─────────────────────────
    T(id="S1", lane="sender", stage="Sign-up", name="Account is open",
      trigger="A new customer sender completes sign-up",
      timing="Immediately · once", channels=["sms", "in_app"],
      status="live", key="sender_onboarding", source="Map · Senders 1",
      hook="Trigger",
      intent="Prove in one line that Pinned does something, and name somewhere they know.",
      old="Welcome, {{name}}! Your account is ready. Find a Pod near you in the app and drop your first parcel.",
      msgs=[
          ("sms", "Welcome to Pinned, {{name}}. Drop a parcel at any pod, or have a runner collect from you.\nYour nearest pod: {{pod}}\n{{link}}"),
          ("in_app", ("Start with one parcel", "Your nearest pod is {{pod}}, {{km}} km away. Booking takes about a minute and you pay after the price is shown.")),
      ],
      rules=["The first message names a real place near them. 'Find a Pod near you' is an instruction; '{{pod}}' is an answer.",
             "No exclamation mark in the first line. Pinned is calm before it is friendly."]),

    T(id="S2", lane="sender", stage="Booking", name="Booked — drop by",
      trigger="Sender completes a booking", timing="Immediately", channels=["sms", "in_app"],
      status="live", key="parcel_booked", source="Map · Senders 2", hook="Action",
      intent="Give them the one thing the pod will ask for, and the time it stops being valid.",
      old="Your parcel {{code}} is booked. Drop it at {{pod}} to start delivery.",
      msgs=[
          ("sms", "Booked. {{code}} is reserved at {{pod}} until {{deadline}}.\nShow this code at the pod — no queue, no paperwork."),
          ("in_app", ("Booked — drop by {{deadline}}", "{{pod}} · open until {{closing_time}}. Directions, or switch to runner collection, in one tap.")),
      ],
      rules=["A booking message states an expiry. A reservation without a deadline is a wish.",
             "The code appears once, on its own line, in DM Mono — the brand reserves mono for codes."]),

    T(id="S2b", lane="sender", stage="Booking", name="Still waiting for your drop",
      trigger="Booking unpaid or not dropped after the hold window",
      timing="Once, at half the hold window", channels=["sms"],
      status="live", key="awaiting_drop", source="Map · Senders 2", hook="Action",
      intent="Remind, and in the same breath remove the reason they have not come.",
      old="Reminder: parcel {{code}} is waiting for drop-off at {{pod}}.",
      msgs=[
          ("sms", "{{code}} is still held for you at {{pod}} until {{deadline}}.\nCan't get there? A runner can collect from you instead: {{track_url}}"),
      ],
      rules=["Every reminder carries the escape hatch. A reminder with no alternative is nagging.",
             "One reminder only. If the hold lapses, the booking message says so — it does not chase."]),

    T(id="S2c", lane="sender", stage="Hand-over", name="Handover code",
      trigger="The sender's handover code is released",
      timing="When a runner is assigned to collect", channels=["sms"],
      status="live", key="handover_code_ready", source="Live template", hook="Action",
      intent="One code, one safety rule, nothing else competing for attention.",
      old="Your handover code is {{otp}}. Please present this code to the runner when dropping off your parcel.",
      msgs=[
          ("sms", "Handover code for {{code}}:\n{{otp}}\nGive it to the runner only after they have scanned the parcel. We never ask for it by phone."),
      ],
      rules=["The security line names the actual attack — 'by phone' — not 'do not share'.",
             "Nothing else ships in a code message. No tracking link, no marketing, no thanks."]),

    T(id="S2d", lane="sender", stage="In transit", name="On the way",
      trigger="The handover code is accepted and the parcel changes hands",
      timing="At hand-over", channels=["sms", "in_app"],
      status="defect", key="parcel_dropped + parcel_handed_to_runner",
      source="Live templates", hook="Reward",
      intent="One event, one message. Today two templates describe the same moment.",
      old="Your parcel {{code}} has been dropped off and is on its way. Track: {{track_url}}\n— and —\nParcel {{code}} has been handed to the runner and is on its way.",
      msgs=[
          ("sms", "{{code}} is with {{runner}} and on the way to {{dest}}.\nFollow it: {{track_url}}"),
          ("in_app", ("Picked up by {{runner}}", "Arriving {{dest}} about {{eta}}. Live map in the app.")),
      ],
      notes=[("warn", "<b>Two SMS for one event.</b> <code>parcel_dropped</code> and <code>parcel_handed_to_runner</code> both fire at hand-over and say the same thing in different words. Retire one, keep the one that names the runner.")],
      rules=["One event, one message, one channel per recipient. Duplicates are not redundancy, they are noise that teaches people to ignore us."]),

    T(id="S3", lane="sender", stage="Delivered", name="Delivered — with proof",
      trigger="The receiver signs for the parcel",
      timing="Immediately", channels=["sms", "in_app"],
      status="partial", key="delivered", source="Map · Senders 3", hook="Reward",
      intent="The payoff moment. A name, a place and a time beats a thank-you.",
      old="Parcel {{code}} has been delivered. Thank you for using Pinned.",
      msgs=[
          ("sms", "Delivered. {{name}} collected {{code}} at {{dest}}, {{time}}.\nSigned proof and photo: {{track_url}}"),
          ("in_app", ("Delivered · {{time}}", "{{name}} collected at {{dest}}. Photo, signature and the full timeline are saved to this parcel.")),
      ],
      rules=["Gratitude is not information. 'Thank you for using Pinned' goes where it costs nothing — the in-app card, not the paid SMS.",
             "Proof is the product. Every delivered message links to it."]),

    T(id="S4a", lane="sender", stage="Not collected", name="Your receiver has not collected",
      trigger="The free storage clock runs out", timing="When 24 countable hours have elapsed", channels=["sms", "in_app"],
      status="live", key="dwell_sender_storage_started_72h", source="Map · Senders 4", hook="Trigger",
      intent="Tell the sender about money before it is charged, not after.",
      old="Parcel {{code}} is still uncollected at {{station}} — Time has passed. Storage fees are now active at Ksh {{rate}}/hr. We've contacted your receiver again. If the parcel isn't collected by {{deadline}}, it will be returned to you.",
      msgs=[
          ("sms", "{{code}} is still at {{station}}. {{name}} has been reminded.\nStorage is now Ksh {{rate}}/hr, charged to you. If it is not collected by {{deadline}} we return it."),
          ("in_app", ("Storage running on {{code}}", "Ksh {{rate}}/hr from today, Ksh {{amount}} so far. Returns to you after {{deadline}}.\n[ Message the receiver ]  [ Return it now ]")),
      ],
      rules=["'Time has passed' says nothing. Name the hour, the rate and who pays.",
             "Say who it is charged to. Ambiguity about money is the fastest way to lose a sender."]),

    T(id="S4b", lane="sender", stage="Not collected", name="Coming back to you",
      trigger="Parcel uncollected 7 days after arrival", timing="Day 7 · final", channels=["sms"],
      status="live", key="dwell_sender_final_notice_7d", source="Map · Senders 4", hook="Trigger",
      intent="State the return as a fact already in motion, with the total.",
      old="Final notice. {{name}}, Parcel {{code}} has not been collected and is being returned to you today. A runner will collect it from {{dest}} and bring it to {{origin}}. Total storage fee: Ksh {{amount}} — charged to your account.",
      msgs=[
          ("sms", "{{code}} was not collected and comes back to you today, from {{dest}} to {{origin}}.\nStorage charged: Ksh {{amount}}."),
      ],
      rules=["'Final notice' is a debt-collector phrase. The fact is final; the words do not need to be.",
             "This is the last message in the chain. Nothing follows it."]),

    T(id="S5", lane="sender", stage="Money", name="Refund sent",
      trigger="A cancellation is refunded", timing="At payout", channels=["sms"],
      status="partial", key="refund_processed", source="Live template", hook="Trigger",
      intent="Money messages answer 'when will I see it' before being asked.",
      old="KSh {{amount}} has been refunded for parcel {{code}}.",
      msgs=[
          ("sms", "Refund sent: Ksh {{amount}} for {{code}}. It reaches your M-Pesa number within 3 working days."),
      ],
      rules=["Currency is written Ksh, consistently, everywhere. Today the templates mix 'KSh', 'KES' and 'Ksh'.",
             "Every money message states the arrival window."]),

    T(id="S6", lane="sender", stage="Exception", name="Delivery did not complete",
      trigger="A runner cannot complete the delivery", timing="Immediately", channels=["sms", "in_app"],
      status="partial", key="failed_delivery", source="Live template", hook="Action",
      intent="Name the reason, the current location, the choice and the clock.",
      old="We couldn't deliver parcel {{code}}. Our team will call you shortly.",
      msgs=[
          ("sms", "{{code}} did not reach {{dest}}: {{reason}}.\nIt is safe at {{station}}. Choose redeliver or return by {{deadline}}: {{track_url}}"),
          ("in_app", ("Held at {{station}}", "{{reason}}. Redeliver tomorrow at no extra cost, or have it returned. Choose by {{deadline}}.")),
      ],
      rules=["'Our team will call you shortly' makes the customer wait for us. Give the choice in the message.",
             "A failure message always says where the parcel is right now. That is the first thing they want to know."]),

    # ───────────────────────── RECEIVERS ─────────────────────────
    T(id="C1", lane="receiver", stage="First contact", name="Someone has sent you a parcel",
      trigger="A parcel is created for a receiver, or a runner collects it",
      timing="At pickup", channels=["sms"],
      status="partial", key="runner_picked_up_receiver", source="Map · Receiver 1", hook="Trigger",
      intent="This may be the first time this person has ever heard of Pinned. Say who sent it.",
      old="Your parcel {{code}} has been picked up and is on its way.",
      msgs=[
          ("sms", "{{from}} has sent you a parcel through Pinned.\n{{runner}} is bringing it to {{dest}}, about {{eta}}.\nFollow it: {{track_url}}"),
      ],
      rules=["A receiver who does not know the sender's name assumes a scam. The sender's name is the trust signal, so it goes first.",
             "Never open a receiver's first message with 'Your parcel {{code}}'. A code they have never seen is not a greeting."]),

    T(id="C2", lane="receiver", stage="Arrived", name="It is here — collect with this code",
      trigger="Parcel reaches the destination pod or station",
      timing="On arrival scan", channels=["sms", "in_app"],
      status="live", key="parcel_arrived", source="Map · Receiver 1", hook="Action",
      intent="Everything needed to walk in and collect, without opening anything.",
      old="Hi {{name}}, parcel {{code}} has arrived at {{station}}. Collect with OTP {{otp}}.",
      msgs=[
          ("sms", "Your parcel from {{from}} is at {{station}}, open until {{closing_time}}.\nCollection code: {{otp}}\nFree storage until {{deadline}}. Can't come? Door delivery: {{track_url}}"),
          ("in_app", ("Ready at {{station}}", "Code {{otp}} · open until {{closing_time}} · free storage until {{deadline}}.\n[ Directions ]  [ Send it to my door ]")),
      ],
      rules=["Two segments is the right price for this message. It carries a code, an address, an opening time, a deadline and an escape hatch — each one saves a call.",
             "Never write 'OTP' to a customer. It is 'collection code'. OTP is our word, not theirs."]),

    T(id="C3", lane="receiver", stage="Exception", name="Running late",
      trigger="Promised delivery time passes while the parcel is in transit",
      timing="At the moment the promise breaks", channels=["sms"],
      status="gap", source="Map · Receiver 2", hook="Trigger",
      intent="A new time, a reason, and when the next message comes.",
      msgs=[
          ("sms", "Your parcel from {{from}} is running late — now about {{eta}}. {{reason}}.\nWe text again the moment it lands at {{station}}."),
      ],
      rules=["Never 'we apologise for any inconvenience caused'. Give a new time instead; that is the apology.",
             "Promise the next message. A delay is tolerable when you know when you will next hear something."]),

    T(id="C4a", lane="receiver", stage="Waiting", name="Still waiting · rung 1",
      trigger="Half the free storage clock has run", timing="12 countable hours left", channels=["sms"],
      status="partial", key="dwell_reminder_24h", source="Map · Receiver 3", hook="Action",
      intent="Neutral. State the facts and the opening hours.",
      old="Your parcel {{code}} is still at {{station}}. Free storage ends in 48 hours. After that: Ksh {{rate}}/hr applies. Your code: {{otp}} Open until: {{closing_time}} Can't make it? Request door delivery: {{track_url}}",
      msgs=[
          ("sms", "Your parcel is still at {{station}}, open until {{closing_time}}.\nCode: {{otp}}\nFree storage until {{deadline}}."),
      ],
      rules=["Rung 1 does not mention the rate. Nothing is being charged yet, so nothing about charging is said.",
             "Retire the 6-hour reminder. It arrives while people are still at work and teaches them we message for no reason.",
             "Scheduled on the storage clock, not the wall clock, so it can never fire overnight or while the pod is shut."]),

    T(id="C4b", lane="receiver", stage="Waiting", name="Still waiting · rung 2",
      trigger="The free storage clock is nearly out", timing="4 countable hours left", channels=["sms"],
      status="partial", key="dwell_reminder_48h", source="Map · Receiver 3", hook="Action",
      intent="Specific. Name the deadline and the rate that starts after it.",
      old="Your parcel {{code}} is still at {{station}}. Free storage ends in 24 hours. After that: Ksh {{rate}}/hr applies. Your code: {{otp}} Open until: {{closing_time}} Can't make it? Request door delivery: {{track_url}}",
      msgs=[
          ("sms", "Free storage on your parcel at {{station}} ends {{deadline}}.\nCode: {{otp}}\nAfter that: Ksh {{rate}}/hr. Can't come? We can bring it to you: {{track_url}}"),
      ],
      rules=["Rung 2 is where the escape hatch earns its place. Most door-delivery conversions happen here.",
             "A deadline, never a countdown. “4 hours left” sent at 17:00 is wrong by the next morning, "
             "because the clock stops at 19:00 and restarts at 08:00."]),

    T(id="C4c", lane="receiver", stage="Waiting", name="Storage has started · rung 3",
      trigger="The free storage clock runs out", timing="After 24 countable hours", channels=["sms"],
      status="defect", key="dwell_storage_started_72h", source="Map · Receiver 3", hook="Trigger",
      intent="Consequence, stated once, with the way to stop it.",
      old="Storage charges have started on parcel {{code}} at KES {{rate}}/hr. Amount so far: KES {{amount}} Charges stop the moment you collect. Your code: {{station}} Collect now to stop the clock. Pay and collect here: {{track_url}}",
      msgs=[
          ("sms", "Storage has started on your parcel at {{station}}: Ksh {{rate}}/hr, Ksh {{amount}} so far.\nIt stops the moment you collect.\nCode: {{otp}}\nPay and collect: {{track_url}}"),
      ],
      notes=[("warn", "<b>Live copy bug.</b> The template reads <code>Your code: {{station}}</code> — it prints the station name where the collection code belongs. Receivers on this rung are being charged and handed the wrong token. Fix before anything else on this page.")],
      rules=["'Charges stop the moment you collect' is the single most useful sentence in the ladder. It stays, and it goes above the code.",
             "Ksh, not KES. One currency spelling across the estate."]),

    T(id="C4d", lane="receiver", stage="Waiting", name="Going back today · rung 4 (7d)",
      trigger="Parcel uncollected 7 days after arrival", timing="Day 7 · final", channels=["sms"],
      status="live", key="dwell_final_notice_7d", source="Map · Receiver 3", hook="Trigger",
      intent="Final rung. A fact, a total, and a human to talk to.",
      old="Final notice, {{name}}. Your parcel {{code}} from {{from}} has not been collected and is being returned to the sender today. Total storage fee charged: Ksh {{amount}}. If you still want this parcel, contact {{from}} to rearrange.",
      msgs=[
          ("sms", "Last day: your parcel from {{from}} goes back to the sender today.\nStorage charged: Ksh {{amount}}.\nStill want it? Contact {{from}} to rearrange."),
      ],
      rules=["Four rungs, never five. Neutral, specific, consequence, final — then silence."]),

    T(id="C5", lane="receiver", stage="Security", name="Collection code",
      trigger="A receiver requests collection", timing="On request", channels=["sms"],
      status="live", key="otp_issued", source="Live template", hook="Action",
      intent="One code, one line of defence.",
      old="Your Pinned collection code is {{otp}}. Do not share it.",
      msgs=[
          ("sms", "Pinned collection code:\n{{otp}}\nIt opens your parcel at {{station}}. We never ask for this code by phone."),
      ],
      rules=["'Do not share it' is advice. 'We never ask for this code by phone' is a rule the customer can use to spot the fraud."]),

    T(id="C6a", lane="receiver", stage="Dwell request", name="Extra time approved",
      trigger="A host approves an extra-time request", timing="On decision", channels=["sms", "in_app"],
      status="live", key="dwell_extension_approved", source="Live template", hook="Reward",
      intent="Confirm the new deadline, not the decision.",
      old="Hold approved for parcel {{code}}: +{{hours}}h extra free storage.",
      msgs=[
          ("sms", "Approved — free storage on your parcel at {{station}} now runs to {{deadline}}.\nCode: {{otp}}"),
          ("in_app", ("Extended to {{deadline}}", "{{hours}} more countable hours of free storage at {{station}}. Code {{otp}}.")),
      ],
      rules=["People do not want the decision, they want the new date. Lead with the deadline.",
             "An extension is granted in countable hours and communicated as a timestamp. The two are "
             "not the same number and the customer only ever sees the timestamp."]),

    T(id="C6b", lane="receiver", stage="Dwell request", name="Extra time declined",
      trigger="A host declines an extra-time request", timing="On decision", channels=["sms", "in_app"],
      status="live", key="dwell_extension_denied", source="Live template", hook="Action",
      intent="A no that ends with a yes to something else.",
      old="Hold denied for parcel {{code}} ({{reason}}). The dwell clock is unchanged.",
      msgs=[
          ("sms", "We can't extend this one: {{reason}}.\nFree storage still ends {{deadline}}. We can bring it to your door instead: {{track_url}}"),
          ("in_app", ("Not extended — {{reason}}", "Free storage still ends {{deadline}}. Door delivery is available today.\n[ Send it to my door ]")),
      ],
      rules=["Every decline offers the alternative in the same message. A no with no door is a complaint waiting to happen.",
             "'Dwell clock' is internal language. Customers hear 'free storage'."]),

    T(id="C7", lane="receiver", stage="Collected", name="Collected — and the next one is easier",
      trigger="Receiver collects the parcel", timing="At collection · once per receiver", channels=["sms"],
      status="gap", source="New · hook: investment", hook="Investment",
      intent="Convert a one-off collection into a saved address.",
      msgs=[
          ("sms", "Collected — thanks, {{name}}.\nNext time {{from}} sends to you, we can bring it to {{dest}} instead. Save your address: {{track_url}}"),
      ],
      rules=["Sent once per receiver, ever. The second one is spam.",
             "This is the only receiver message that asks for something. It asks after we have delivered, never before."]),
]

TOUCHPOINTS += [

    # ───────────────────────── RUNNERS ─────────────────────────
    T(id="R0", lane="runner", stage="Invite", name="Your runner account is open",
      trigger="Admin creates a runner", timing="Immediately", channels=["sms"],
      status="live", key="runner_invite", source="Live template", hook="Trigger",
      intent="Get them to verification while the decision to join is still warm.",
      old="Welcome to Pinned. Sign in at {{link}} to complete your verification.",
      msgs=[
          ("sms", "Welcome to Pinned, {{name}}. Your runner account is open.\nVerification takes about 6 minutes — then you can go online and take jobs.\n{{link}}"),
      ],
      rules=["Say how long it takes. An unquantified task gets postponed.",
             "One link. A runner SMS with two links gets neither tapped."]),

    T(id="R1a", lane="runner", stage="Onboarding", name="Documents received",
      trigger="Runner submits verification documents", timing="Immediately", channels=["sms", "in_app"],
      status="live", key="runner_docs_submitted", source="Map · Runners 1a", hook="Trigger",
      intent="Close the loop so they stop refreshing, and name the hour they will hear.",
      old="Pinned: we've received your documents. Our team is reviewing your application. We'll update you within 24 hours. Need help? hello@pinnedflow.com.",
      msgs=[
          ("sms", "Thanks {{name}} — your documents are in. We review in the order received and you will hear from us by {{deadline}}.\nNothing to do until then."),
          ("in_app", ("In review", "We are checking your {{docs}}. You will get an SMS the moment there is a decision — no need to keep the app open.")),
      ],
      rules=["'Within 24 hours' is a promise nobody tracks. '{{deadline}}' is a promise the system can keep, and be measured against.",
             "'Nothing to do until then' is the most reassuring sentence in onboarding. Keep it.",
             "An email address in a runner SMS is wasted characters — runners call or use in-app help."]),

    T(id="R1b", lane="runner", stage="Onboarding", name="Approved",
      trigger="Admin approves runner verification", timing="On decision", channels=["sms", "email", "in_app"],
      status="partial", key="runner_kyc_approved", source="Map · Runners 1b", hook="Reward",
      intent="The moment they became a Pinned runner. Make it feel earned, then point at the switch.",
      old="Congratulations {{name}}! Your Pinned runner account has been approved. You can now go online and start accepting deliveries.",
      msgs=[
          ("sms", "You're approved, {{name}}. Go online in the app and job offers come straight to this phone.\nWelcome to the network."),
          ("email", ("You're a Pinned runner, {{name}}",
                     "Your verification is complete.\n\nWhat is approved: {{docs}}\nWhen you are paid: every {{deadline}}, to the M-Pesa number on your account\nWhere to get help: in-app Help, or call 0700 000 000\n\nGo online in the app and your first offer will arrive on {{name}}'s phone. Offers show the payout, the number of parcels and the distance before you accept.")),
          ("in_app", ("Approved — you can go online", "Tap Go online and offers near {{origin}} will start arriving.")),
      ],
      rules=["Email carries the things a runner needs twice: pay day, support number, what was verified. SMS carries only the switch.",
             "The map asks for all three channels here. Email is the one missing today."]),

    T(id="R1c", lane="runner", stage="Onboarding", name="Not approved — and why",
      trigger="Admin rejects runner verification", timing="On decision", channels=["sms", "email", "in_app"],
      status="partial", key="runner_kyc_rejected", source="Map · Runners 1c", hook="Action",
      intent="Name exactly one fixable thing and the way back in.",
      old="Your Pinned verification was not approved{{reason}}. Update your documents in the app to reapply.",
      msgs=[
          ("sms", "{{name}}, we couldn't approve your account yet: {{reason}}.\nFix that one item in the app and resubmit — we review again within a day."),
          ("email", ("What to fix on your Pinned application",
                     "We could not approve your application yet.\n\nWhat we need: {{reason}}\nHow to fix it: open the app, go to Documents, replace the {{docs}} and submit.\n\nPhotos work best in daylight, flat on a table, with all four corners in frame. We review again within a day of your resubmission.")),
          ("in_app", ("One thing to fix", "{{reason}}. Replace your {{docs}} and submit again — we review within a day.\n[ Replace document ]")),
      ],
      rules=["A rejection names one item, not a list. A list reads as 'you are not wanted'.",
             "'Not approved' never appears without 'yet'. The relationship is not over."]),

    T(id="R2", lane="runner", stage="First run", name="How a Pinned run works",
      trigger="Runner accepts their first delivery", timing="Once, ever · at acceptance",
      channels=["sms", "email", "in_app"],
      status="gap", source="Map · Runners 2", hook="Investment",
      intent="Teach the three rules at the one moment a runner is guaranteed to be paying attention.",
      msgs=[
          ("sms", "First job accepted, {{name}}. Three things that matter: arrive by {{eta}}, scan every parcel, never hand over without the code.\nFull guide: {{link}}"),
          ("email", ("Your first Pinned run — what happens at each stop",
                     "1. Collect. Scan each parcel at the pod or counter. The app will not let you leave with an unscanned parcel, and that protects you.\n\n2. Custody. From the scan until hand-over, the parcel is yours. If anything looks wrong — open box, wet, wrong label — photograph it in the app before you move.\n\n3. Hand over. The receiver reads you their code. You enter it. Never accept a code sent to you by anyone else, and never read the code out loud first.\n\n4. Get paid. Earnings land every {{deadline}} on the M-Pesa number on your account.\n\nIf a receiver is not there: wait 5 minutes, call from the app, then mark 'not available'. Do not leave a parcel with a neighbour.")),
          ("in_app", ("Three rules for every run", "Arrive on time · scan everything · no hand-over without the code. Tap for the 90-second version.")),
      ],
      rules=["Once, ever. The map is explicit: email and SMS fire a single time.",
             "This is the highest-value message in the runner lane and it does not exist yet."]),

    T(id="R3", lane="runner", stage="Working", name="Delivered — earnings reveal",
      trigger="Runner completes a delivery", timing="At hand-over", channels=["in_app"],
      status="gap", source="Map · Runners 3", hook="Reward",
      intent="The variable reward. The number is the message.",
      msgs=[
          ("in_app", ("Delivered · Ksh {{payout}} added", "{{code}} handed to {{name}} at {{dest}}.\nToday: {{stops}} stops · Ksh {{amount}}")),
      ],
      rules=["In-app only, as the map says. An SMS per delivery would cost more than the delivery earns.",
             "Same place, same shape, every single time. A reward that moves around stops being a reward.",
             "The running day total is what turns one more job into a habit."]),

    T(id="R4", lane="runner", stage="Compliance", name="Document expiry ladder",
      trigger="A runner document approaches expiry",
      timing="Email −30d · SMS −30d, −7d, −1d · in-app from −30d",
      channels=["email", "sms", "in_app"],
      status="partial", key="runner_licence_expiring + runner_kyc_expired", source="Map · Runners 4",
      hook="Action",
      intent="Four rungs that escalate in specificity, not volume. The map asks for tone to change; it changes by naming consequences, not by shouting.",
      old="Your {{docs}} will expire soon. Renew in the app to keep your batch eligibility.\n— then —\nYour {{docs}} has expired. You're restricted from batches until you renew it in the app.",
      msgs=[
          ("email", ("Your {{docs}} expires on {{deadline}}",
                     "Renewing takes two minutes in the app: Documents → {{docs}} → Replace.\n\nIf it lapses, offers pause automatically on {{deadline}}. Nothing else about your account changes, and offers resume within minutes of a successful upload.")),
          ("sms", "{{name}}, your {{docs}} expires {{deadline}}. Upload the new one in the app any time before then — two minutes.\n[−30 days]"),
          ("sms", "7 days left on your {{docs}} ({{deadline}}). After that date, offers pause until it is renewed.\n[−7 days]"),
          ("sms", "Tomorrow your {{docs}} expires and offers stop. Upload the renewal now: {{link}}\n[−1 day]"),
          ("in_app", ("Offers paused — {{docs}} expired", "Upload a current {{docs}} and offers resume within minutes. Everything else on your account is untouched.")),
      ],
      rules=["'Batch eligibility' is internal language. Runners hear 'offers'.",
             "Escalation is specificity: 'expires {{deadline}}' → '7 days left' → 'tomorrow, offers stop' → 'offers paused'. No capital letters, no warnings about warnings.",
             "Always say what does not change. Fear of losing the account is why runners avoid opening these messages."]),

    T(id="R5", lane="runner", stage="Working", name="Running late",
      trigger="A delivery passes its promised time", timing="At the promise", channels=["in_app"],
      status="gap", source="Map · Runners 5", hook="Action",
      intent="Hand the runner the action that fixes the receiver's experience. Never a reprimand.",
      msgs=[
          ("in_app", ("{{code}} is past its time", "You are {{hours}} behind on {{dest}}. One tap sends the receiver a new ETA — that is usually all they want.\n[ Send ETA ]  [ I need help ]")),
      ],
      rules=["A delay message that only states the delay makes the runner defensive. A delay message with a button makes them useful.",
             "Never surface a delay to the runner and the receiver in a way that implies blame to either."]),

    T(id="R6", lane="runner", stage="Working", name="Loaded at the pod",
      trigger="Runner finishes collecting from a pod", timing="At the last scan", channels=["in_app"],
      status="gap", source="Map · Runners 6", hook="Action",
      intent="Close the collection, open the route, in one screen.",
      msgs=[
          ("in_app", ("{{stops}} parcels on board", "Next stop {{dest}} · {{km}} km. Scan each one at hand-over.\n[ Start route ]")),
      ],
      rules=["This message exists to make the next tap obvious. It carries exactly one button."]),

    T(id="R7", lane="runner", stage="Offers", name="New delivery available",
      trigger="A batch offer is created", timing="On offer and every re-offer", channels=["push"],
      status="defect", key="Routing::BatchOffer::Build", source="Live code · not in the map",
      hook="Trigger",
      intent="The single highest-volume message Pinned sends, and the one doing the most damage.",
      old="New delivery available\nPickup: Superior - Gatakaini. Batch distance: 15.8 km.",
      msgs=[
          ("push", ("Ksh {{payout}} · {{stops}} parcels · {{km}} km", "{{origin}} → {{dest}}. Tap to accept — this offer closes {{eta}}.")),
      ],
      notes=[("warn", "<b>Evidence.</b> A runner lock screen on 9 Oct carried four identical notifications — 4m, 5m, 10m and 24m ago — all reading <i>“New delivery available · Pickup: Superior - Gatakaini. Batch distance: 15.8 km.”</i> Same batch, same words, stacked. By the fourth, the notification has taught the runner that Pinned pushes mean nothing."),
             ("warn", "<b>Three causes, all in code.</b> (1) <code>app/services/routing/batch_offer/build.rb</code> notifies every <code>Runner.available</code> — the radius and vehicle-class filters are commented out. (2) Every re-offer sends a fresh notification; nothing collapses them. (3) <code>FcmSender</code> sends no <code>collapse_key</code> / <code>apns-collapse-id</code>, so the OS has no way to replace the previous one."),
             ("hook", "<b>The hook is already here and it is being wasted.</b> A job offer is the purest variable reward in the business — payout, parcel count and distance differ every time. Put those three numbers in the title and the offer becomes the thing runners open the phone to check. Repeat the same seven words four times and it becomes the thing they swipe away.")],
      rules=["<b>One live offer per batch, per runner.</b> Collapse key <code>batch_offer:{batch_id}</code>; a re-offer replaces the notification in place, it never stacks.",
             "<b>Cooldown.</b> No more than 3 offer pushes to one runner in 15 minutes, whatever the batch.",
             "<b>Radius before volume.</b> Restore the proximity and vehicle-class filters. An offer a runner cannot take is a notification that costs trust and returns nothing.",
             "<b>Money in the title.</b> The title is the only part read on a locked phone. Ksh first, parcels second, distance third.",
             "<b>Expiry in the body.</b> An offer with no closing time has no reason to be opened now.",
             "<b>Silence when offline.</b> Runners who are not online do not get offer pushes. Today they do."]),

    # ───────────────────────── ADMIN INTERVENTIONS ─────────────────────────
    T(id="A1a", lane="admin", stage="Reassignment", name="Job reassigned — previous runner",
      trigger="Admin reassigns a job away from a runner", timing="Immediately", channels=["sms", "in_app"],
      status="gap", source="Map · Admin 1a", hook="Trigger",
      intent="Remove the two fears at once: did I do something wrong, and am I owed anything.",
      msgs=[
          ("sms", "{{batch}} has been reassigned to another runner. Nothing is owed from your side and your rating is unchanged.\nNew offers continue as normal."),
          ("in_app", ("{{batch}} reassigned", "Reason: {{reason}}. Your rating and standing are unchanged.")),
      ],
      rules=["Say 'your rating is unchanged' explicitly. Silence on that point is read as a penalty.",
             "Reassignment messages never imply fault unless ops has actually recorded fault — and then it is a conversation, not an SMS."]),

    T(id="A1b", lane="admin", stage="Reassignment", name="Job reassigned — new runner",
      trigger="Admin assigns a job to a runner", timing="Immediately", channels=["sms", "in_app"],
      status="gap", source="Map · Admin 1b", hook="Action",
      intent="An assignment is an offer with the decision already made — it still has to carry the numbers.",
      msgs=[
          ("sms", "Assigned to you: {{stops}} parcels from {{origin}}, Ksh {{payout}}, {{km}} km.\nDetails and route in the app."),
          ("in_app", ("New job assigned", "{{origin}} → {{dest}} · {{stops}} parcels · Ksh {{payout}}\n[ Start route ]  [ I can't take this ]")),
      ],
      rules=["Always give a way to decline in-app. An assignment a runner cannot refuse produces a failed delivery instead of a declined job."]),

    T(id="A2", lane="admin", stage="Reassignment", name="Job floated back to the pool",
      trigger="A job is returned to the system from a runner", timing="Immediately", channels=["sms", "in_app"],
      status="gap", source="Map · Admin 2", hook="Trigger",
      intent="Release them cleanly so they take the next offer without hesitating.",
      msgs=[
          ("sms", "{{batch}} has gone back to the job pool and you are released from it. {{reason}}.\nYou can take new offers now."),
          ("in_app", ("{{batch}} released", "{{reason}}. Your rating and standing are unchanged — offers continue as normal.")),
      ],
      rules=["'You can take new offers now' is the operative sentence. Without it, runners sit and wait."]),

    T(id="A3", lane="admin", stage="Availability", name="You have gone offline",
      trigger="A runner's status goes offline", timing="At the state change", channels=["sms"],
      status="gap", source="Map · Admin 3", hook="Action",
      intent="A system-detected state change, stated as fact, with the one-tap undo.",
      msgs=[
          ("sms", "You are offline on Pinned — no job offers until you are back on.\nIf that wasn't you, open the app and tap Go online."),
      ],
      rules=["Most offline events are a dead battery or a lost connection, not a choice. The message assumes the accident.",
             "Once per offline event. A runner who meant to go offline does not need a second SMS."]),

    T(id="A4", lane="admin", stage="Delay", name="Ops is asking about this job",
      trigger="Ops flags a delayed job", timing="When ops acts", channels=["in_app"],
      status="gap", source="Map · Admin 4", hook="Action",
      intent="A human is watching. Make responding easier than ignoring.",
      msgs=[
          ("in_app", ("Ops is asking about {{code}}", "{{dest}} was due {{deadline}}. Send your ETA — it goes to the receiver and to ops at the same time.\n[ Send ETA ]  [ Call ops ]")),
      ],
      rules=["In-app only. An SMS from 'ops' about a late job reads as a warning letter.",
             "One reply sends to both audiences. Never make a runner tell the same story twice."]),
]

TOUCHPOINTS += [

    # ───────────────────────── HOSTS ─────────────────────────
    T(id="H1a", lane="host", stage="Onboarding", name="Your location is live — business sender",
      trigger="A business-sender host location goes live", timing="At activation",
      channels=["sms", "email", "in_app"],
      status="partial", key="vhost_onboarding_business", source="Map · Virtual Host 1a", hook="Trigger",
      intent="Open the door, then teach the operation in the channel that can hold it.",
      old="Welcome, {{name}}! Your station at {{address}} is now live. You can now send products to your clients using the Pinned network. Open your Pinned Host portal: {{link}}",
      msgs=[
          ("sms", "{{name}}, {{address}} is live on Pinned. You can book deliveries for your clients from today.\nPortal: {{link}}"),
          ("email", ("{{address}} is live — how the operation runs",
                     "Your station is active from today.\n\nBooking: create a delivery in the portal, or let a client book to you. Cut-off for same-day is {{closing_time}}.\n\nCollection: a runner is assigned and you see their name and ETA in the portal. Have the parcels at the counter before they arrive.\n\nHand-over: the runner scans each parcel. Only then do you release the handover code. Never read a code out before the scan.\n\nFailures: if a delivery cannot complete, you choose redeliver or return in the portal. You have until the deadline shown.\n\nMoney: settlement runs every week and the statement arrives by email.\n\nHelp: 0700 000 000, or Help in the portal.")),
          ("in_app", ("Welcome — three things to set up", "Cut-off time, counter contact and your settlement number. Two minutes.")),
      ],
      rules=["The map says this one message carries 'important info on the operations'. That does not fit in an SMS, so the SMS opens the door and the email does the teaching.",
             "Never 'Welcome, {{name}}!' with an exclamation mark on a business account. Warm, not excitable."]),

    T(id="H1b", lane="host", stage="Onboarding", name="Your location is live — pod host",
      trigger="A pod-host location goes live", timing="At activation", channels=["sms", "email", "in_app"],
      status="partial", key="vhost_onboarding_pod", source="Map · Virtual Host 1a", hook="Trigger",
      intent="Same moment, different job: this host receives parcels rather than sending them.",
      old="Welcome, {{name}}! Your location at {{address}} is now registered in the Pinned network. Runners can now start collecting parcels. Open your Pinned Host portal: {{link}}",
      msgs=[
          ("sms", "{{name}}, {{address}} is registered. Runners can start collecting from today.\nPortal: {{link}}"),
          ("email", ("{{address}} is on the network — what to expect at the counter",
                     "Runners will start arriving from today.\n\nWhat a runner shows you: their name in the app, and a scan for every parcel. No scan, no hand-over.\n\nWhat you release: the handover code, after the scan, never before.\n\nCollections by customers: the customer reads you their collection code. Enter it in the portal and the parcel is signed off.\n\nIf the pod is offline: you will get an SMS. Check power and the router first; if both are fine, call 0700 000 000.\n\nSettlement: weekly, with a statement by email.")),
          ("in_app", ("{{address}} is on the network", "Set your counter contact and opening hours so runners arrive when you are open. Two minutes.")),
      ],
      rules=["Two onboarding templates for two different jobs is correct. Merging them would make both vague."]),

    T(id="H2", lane="host", stage="Collection", name="A runner is on the way",
      trigger="A runner is assigned to collect from the host",
      timing="At assignment · email the first time only", channels=["email", "in_app"],
      status="partial", key="runner_accepted_host", source="Map · Virtual Host 2", hook="Action",
      intent="The first time, explain the hand-over. Every time after, just state it.",
      old="A runner has accepted delivery {{batch}} from {{origin}}. Runner: {{runner}}. Pickup starting soon.",
      msgs=[
          ("in_app", ("{{runner}} is collecting {{stops}} parcels · ETA {{eta}}", "Have them at the counter. Release the handover code only after the scan.")),
          ("email", ("How hand-over works at {{address}}",
                     "A runner is on the way for the first time, so here is the sequence.\n\n1. They arrive and identify themselves in the app — you see the same name in your portal.\n2. They scan each parcel. The scan is what transfers responsibility from you to Pinned.\n3. You release the handover code. After the scan, never before.\n\nThat is the whole process. You will not get this email again — from now on it is a line in the portal.")),
      ],
      rules=["The map is explicit: email once. The rule generalises — the first time a host meets a process, email explains it; after that, in-app states it.",
             "'Pickup starting soon' is not a time. Give the ETA or give nothing."]),

    T(id="H3", lane="host", stage="Exception", name="A delivery did not complete",
      trigger="A runner cannot complete a delivery from this host", timing="Immediately", channels=["sms", "in_app"],
      status="partial", key="failed_delivery", source="Map · Virtual Host 3", hook="Action",
      intent="Reason, location, choice, deadline — in that order.",
      old="We couldn't deliver parcel {{code}}. Our team will call you shortly.",
      msgs=[
          ("sms", "{{code}} to {{dest}} did not complete: {{reason}}.\nIt is held at {{station}}. Choose redeliver or return by {{deadline}}: {{link}}"),
          ("in_app", ("Held at {{station}} — your call", "{{reason}}. Redeliver tomorrow, or return to you. If nothing is chosen by {{deadline}} we redeliver.")),
      ],
      rules=["State the default. 'If nothing is chosen by {{deadline}} we redeliver' saves a phone call from every host who is busy."]),

    T(id="H4", lane="host", stage="Money", name="Weekly settlement",
      trigger="The weekly settlement run completes", timing="Weekly", channels=["email", "in_app"],
      status="partial", key="Vhost::WeeklySettlementNotifier", source="Map · Virtual Host 4", hook="Reward",
      intent="The number hosts open the email for. Put it in the subject line.",
      msgs=[
          ("email", ("Pinned settlement — Ksh {{amount}} for week to {{deadline}}",
                     "Ksh {{amount}} for {{stops}} parcels, week ending {{deadline}}.\n\nPaid to the M-Pesa number on your account, within one working day.\n\nThe full statement — every parcel, every fee — is attached and in the portal under Settlements.")),
          ("in_app", ("Ksh {{amount}} settled", "{{stops}} parcels, week to {{deadline}}. Statement in Settlements.")),
      ],
      rules=["The amount goes in the subject line. A settlement email that makes a host open it to learn the number is a worse email.",
             "The reward is weekly and variable — this is the host hook. It should never be late, and never silent in a zero week; a zero week gets its own line: 'No parcels this week, nothing to settle.'"]),

    T(id="H5", lane="host", stage="Hardware", name="Your pod is offline",
      trigger="A pod misses its heartbeat", timing="After the grace window", channels=["sms"],
      status="partial", key="station_offline", source="Live template", hook="Action",
      intent="Say what stopped working for the customer, not what the sensor saw.",
      old="Your Pinned pod{{pod}} appears offline (no heartbeat since {{since}}). Please check its power and network.",
      msgs=[
          ("sms", "{{pod}} has been offline since {{since}} — collections there are paused.\nCheck the power and the router. If both look fine, call 0700 000 000."),
      ],
      rules=["'No heartbeat' is our word. The host's word is 'offline', and what they need to know is that customers cannot collect.",
             "Give the phone number in full. A host standing next to a dead pod is not going to open a portal."]),

    T(id="H6", lane="host", stage="Invite", name="Invitation to host a pod",
      trigger="Admin invites a host user", timing="On invite", channels=["email"],
      status="partial", key="host_invite", source="Live template · currently inactive", hook="Trigger",
      intent="A cold invitation has to answer 'what do I get' before 'click here'.",
      old="You've been invited to host a Pinned Pod. Accept at {{link}}.",
      msgs=[
          ("email", ("An invitation to host a Pinned pod at {{address}}",
                     "A Pinned pod is a parcel point inside your premises. It brings people through your door who would not otherwise come, and it pays a fee on every parcel that passes through.\n\nIt takes about 2 m² and we install, maintain and insure it.\n\nAccept and we will arrange a site visit: {{link}}")),
      ],
      rules=["This template is seeded inactive. Either it carries a real offer or it should not exist.",
             "A one-line invitation to install hardware in someone's business will not convert. Say what it takes and what it pays."]),

    T(id="H7", lane="host", stage="Dwell request", name="A receiver is asking for more time",
      trigger="A receiver requests a dwell extension", timing="On request", channels=["in_app"],
      status="gap", source="New · completes the dwell loop", hook="Action",
      intent="The receiver-side approval and denial messages exist. Nothing tells the host there is a decision to make.",
      msgs=[
          ("in_app", ("{{name}} wants {{hours}}h more on a parcel", "At {{station}}, free storage ends {{deadline}}. They are told either way.\n[ Approve ]  [ Decline ]")),
      ],
      rules=["Never build the answer before the question. Two live templates answer a request that has no notification."]),

    # ───────────────────────── PROSPECTS ─────────────────────────
    T(id="P1", lane="prospect", stage="Groups", name="Marketplace group reply",
      trigger="A delivery question in a Nairobi buy-and-sell or courier group",
      timing="Within the hour, by a human", channels=["whatsapp"],
      status="gap", source="New · acquisition", hook="Trigger",
      intent="Three sentences: proof, price-and-speed, link. The fourth sentence is what makes it an advert.",
      msgs=[
          ("whatsapp", "We deliver across Nairobi — drop at any Pinned pod, or a runner collects from your shop.\nSame-day inside town, and the receiver gets a code to collect.\nPrice in ten seconds, no account: pinnedflow.app"),
      ],
      rules=["Never post a star rating or an invented review count. Only figures the live board can prove.",
             "One link, no emoji wall, no all-caps. Groups mute sellers who shout.",
             "Reply to the question that was asked before describing the service. A reply that ignores the question is an advert."]),

    T(id="P2", lane="prospect", stage="Enquiry", name="First reply to an enquiry",
      trigger="A direct message or call-back request", timing="Within 5 minutes in working hours",
      channels=["whatsapp"],
      status="gap", source="New · acquisition", hook="Action",
      intent="Ask for the two things that produce a price. Nothing else.",
      msgs=[
          ("whatsapp", "Hi — Pinned here. Tell me the pickup area and the drop area and I'll send the price and the time right away."),
      ],
      rules=["Two questions maximum in a first reply. Every extra question halves the replies.",
             "Never open with 'Thank you for contacting Pinned'. It is the sentence people scroll past."]),

    T(id="P3", lane="prospect", stage="Quote", name="You checked a price",
      trigger="A quote is generated on the web and not booked",
      timing="Once, within the hour", channels=["sms"],
      status="gap", source="New · acquisition", hook="Trigger",
      intent="The quote already did the persuading. Repeat it exactly and get out of the way.",
      msgs=[
          ("sms", "You checked a Pinned price: {{origin}} to {{dest}}, Ksh {{amount}}, about {{eta}}.\nStill available: {{link}}\nReply STOP to opt out."),
      ],
      rules=["Promotional, so it carries an opt-out — the code already refuses to save promotional copy without one.",
             "Once. There is no second message in this sequence, ever.",
             "Repeat the exact figures they saw. A different number reads as a bait and switch."]),

    T(id="P4", lane="prospect", stage="Conversion", name="You have received — now send",
      trigger="A receiver collects their first parcel and has never sent one",
      timing="24h after collection · once ever", channels=["sms"],
      status="gap", source="New · the largest warm audience Pinned has", hook="Investment",
      intent="Every receiver has already seen the product work. That is the whole pitch.",
      msgs=[
          ("sms", "You collected a parcel with Pinned yesterday, {{name}}.\nSending one starts at Ksh {{amount}} and a runner can collect from you: {{link}}\nReply STOP to opt out."),
      ],
      rules=["Once per person, ever, and never to someone who has already sent.",
             "Lead with what they experienced, not with what we sell."]),

    T(id="P5", lane="prospect", stage="Referral", name="Someone sent you a parcel",
      trigger="A receiver's first collection, where the sender is on a referral plan",
      timing="With the collected message", channels=["sms"],
      status="gap", source="New · acquisition", hook="Investment",
      intent="The referral rides on a delivery that already happened. It never interrupts one.",
      msgs=[
          ("sms", "{{from}} sent you this parcel with Pinned. Your first send is Ksh {{amount}} off: {{link}}\nReply STOP to opt out."),
      ],
      rules=["Never send a referral message before the parcel is in the receiver's hands.",
             "Maximum one promotional SMS per person per week, across every sequence on this page."]),
]


# ───────────────────────── the system ─────────────────────────

PRINCIPLES = [
    dict(n="01", t="Say what happened, first",
         p="The event goes in the first four words. Not a greeting, not the brand, not a preamble. A person reading a lock screen in the sun gets one line — spend it on the fact.",
         yes="Delivered. Wanjiru collected PN-4K7Q2 at Lavington, 13:42.",
         no="Greetings from Pinned! We are pleased to inform you that your parcel has now been successfully delivered."),
    dict(n="02", t="One message, one action",
         p="If a message cannot name a single next step, it is not a message, it is a thought. Two actions in one SMS means neither gets done.",
         yes="Code: 840 213 — show it at the counter.",
         no="You can collect it, or request door delivery, or extend your storage, or contact the sender."),
    dict(n="03", t="Name names",
         p="The pod, the street, the runner, the amount, the hour. Specifics are what turn a notification into information. Generic words are the sound of a system talking to itself.",
         yes="Your parcel from Sokoni Stores is at Shell Kileleshwa, open until 21:00.",
         no="Your parcel has arrived at the designated collection point."),
    dict(n="04", t="Numbers are facts, never threats",
         p="Charges, deadlines and returns are stated once, calmly, with the way to avoid them in the same breath. Pinned never raises its voice at someone who owes it fifty shillings.",
         yes="Storage has started: Ksh 50/hr. It stops the moment you collect.",
         no="FINAL NOTICE! Storage charges are ACCRUING. Immediate collection is required to avoid further penalties."),
    dict(n="05", t="Never make someone open an app to learn something a line could tell them",
         p="'Open the app for details' is a tax we charge the customer for our own convenience. If it fits in the SMS, it goes in the SMS.",
         yes="Now arriving about 14:20 — the rain has closed Ngong Road.",
         no="There has been an update to your delivery. Open the app to see the details."),
    dict(n="06", t="The code is the hero",
         p="Codes, OTPs and tracking references sit alone on their own line, in DM Mono, never mid-sentence and never split across a line break. The brand reserves mono for exactly this.",
         yes="Collection code:\n840 213",
         no="Please use the one-time-password 840213 at the locker to retrieve your item."),
    dict(n="07", t="Kenyan, not American",
         p="Collect, not pick up. Ksh, written one way everywhere. 24-hour clock. Petrol station. Estate. Ordinary Kenyan English, written the way the counter staff speak.",
         yes="Open until 21:00. Ksh 50/hr after Friday.",
         no="Available until 9 PM. A fee of KES 50.00 per hour shall apply thereafter."),
    dict(n="08", t="Apologise once, then fix it",
         p="One short apology, then the new time or the new plan. Repeated sorries read as a system that knows it is unreliable and expects to stay that way.",
         yes="Sorry — late. Now about 14:20, and we text when it lands.",
         no="We sincerely apologise for the inconvenience. We apologise again for any disruption this may have caused."),
    dict(n="09", t="First contact names the pain, not the feature",
         p="The first message any audience gets has one job beyond its own: say what Pinned takes off their hands. A runner hears “six minutes to jobs”, a host hears what the pod pays, a sender hears the end of ringing people to ask where things are. Features come later, to people who already care.",
         yes="Karibu Pinned, Wanjiru — your answer to UKO WAPI?",
         no="Welcome to Pinned. Your sign-up code is 840 213."),
]

CONTRACT = [
    ("What happened", "The event, in the first line. Past tense for facts, present for states."),
    ("What it means for me", "Only if it is not obvious. Money, deadlines and location always qualify."),
    ("What I do now", "Exactly one action. If there is no action, say 'nothing to do until then'."),
    ("What I need to do it", "The code, the link, the address, the hour. Nothing that is not needed for the action."),
]

HOOK_FRAME = [
    dict(n="Trigger", t="External, then internal",
         p="Every Pinned message is an external trigger. It earns its place by eventually becoming an internal one: the runner who checks the phone for the next offer, the receiver who thinks 'the code came by SMS last time'. Triggers that fire without information are how the internal one is destroyed."),
    dict(n="Action", t="The simplest thing that moves the parcel",
         p="One tap, one code, one walk-in. Measure every message by how many actions it asks for; the answer is always one. If the action needs the app, the message carries the deep link; if it does not, the message carries everything."),
    dict(n="Variable reward", t="What differs every time",
         p="The runner's payout, stop count and distance. The host's weekly figure. The sender's proof photo and the name of the person who signed. The receiver's free-storage countdown they beat. Pinned has genuine variable rewards already — they are currently buried."),
    dict(n="Investment", t="What makes the next one better",
         p="A saved address, a renewed document, a rating, a branch default, a repeat receiver. Each one is asked for at the moment immediately after a success, never before one, and never more than once."),
]

CHANNELS = [
    dict(k="sms", t="SMS", role="Lands anywhere, costs money, cannot be taken back",
         use="Anything that must reach a person who is not in the app: arrival, codes, money, deadlines, failures.",
         avoid="Progress updates, thank-yous, anything a push or an in-app card can carry.",
         rules=["160 GSM-7 characters is one segment. Two segments are allowed when the message carries money, a deadline and an action — and once per audience for first contact, where the second segment buys the reason to care.",
                "Sender ID PINNED on everything.",
                "No link shorteners the customer cannot read. The domain is the trust signal.",
                "Non-urgent SMS is held between 21:00 and 06:30 EAT."]),
    dict(k="push", t="Push", role="Free, instant, and the easiest thing in the world to turn off",
         use="Live operational state while the app is where the action happens: offers, route changes, ETAs, in-run prompts.",
         avoid="Anything the runner must still be told if they never open the phone. Push is not delivery, it is a nudge.",
         rules=["Every push carries a collapse key. A second push about the same thing replaces the first; it never stacks.",
                "Maximum 3 pushes to one person in 15 minutes, across all types.",
                "Title ≤ 45 characters, body ≤ 110 — past that, the lock screen truncates and the sentence is wasted.",
                "Never push to someone who is offline or off shift."]),
    dict(k="in_app", t="In-app", role="The record. Everything that happened, in order, forever",
         use="Every event, without exception, including ones that also went out by SMS.",
         avoid="Being the only channel for money, deadlines or a code. If it matters off-app, it goes off-app too.",
         rules=["The in-app entry is written first; the SMS is a compression of it.",
                "Earnings and settlement figures always appear in the same place, in the same shape.",
                "Nothing in the in-app feed disappears. A customer should be able to prove what we told them."]),
    dict(k="email", t="Email", role="The channel that can hold a process or a document",
         use="Onboarding primers, settlement statements, approvals and rejections with detail, anything with an attachment.",
         avoid="Urgency. Nobody in this business reads email on the road.",
         rules=["On transactional, the subject line carries the fact — the amount, the date, "
                "the decision. Outreach earns its open with a hook instead; see <a href=\"email.html#rules\">Email</a>.",
                "From notifications@pinnedflow.app, display name Pinned — and never "
                "<code>noreply@</code> on a class whose success is a reply.",
                "Three sending classes on three subdomains, so a complaint about a cold pitch "
                "cannot delay a collection code. <a href=\"email.html#classes\">The classes</a>.",
                "One-time explanatory emails say in the message that they are one-time."]),
    dict(k="whatsapp", t="WhatsApp", role="Two-way, where Kenyan commerce actually happens",
         use="Enquiries, group replies, and anything where the answer is a conversation.",
         avoid="Automated transactional blasts. The moment it feels like SMS, the thread gets blocked.",
         rules=["Replies come from a human within 5 minutes in working hours, or the channel is not open.",
                "Template-initiated messages only where the person has written to us first.",
                "Priced like SMS. It is not free, and it is not a dumping ground."]),
    dict(k="call", t="Call", role="The exception path, by a person",
         use="A failed delivery with something valuable in it, a dispute, a safety issue.",
         avoid="Everything else. Pinned does not make automated calls.",
         rules=["A call is always preceded by the SMS that explains why someone is about to ring.",
                "Never an automated voice. If it is worth a call, it is worth a person."]),
]

LAWS = [
    dict(t="One event, one message",
         p="A single thing that happened produces a single message per person. Two templates describing the same moment is a bug, not thoroughness. Today the hand-over fires twice and the batch offer fires as many times as the system re-offers."),
    dict(t="Channel ladder, not channel broadcast",
         p="In-app always. SMS only when the action happens away from the app. Push only when the app is the destination. Email only when it is a document or a process. The map's '(sms, email, in-app)' means a ladder of three different jobs, not the same sentence three times."),
    dict(t="Collapse before you send",
         p="Every push carries a collapse key built from what it is about — <code>batch_offer:{batch_id}</code>, <code>parcel:{code}</code>. The second notification replaces the first. Four identical notifications on a lock screen is the single clearest evidence of a system that does not know what it has already said."),
    dict(t="Quiet hours, 21:00 – 06:30 EAT",
         p="Non-urgent SMS and push are held until morning. Urgent is defined narrowly and in code: a delivery in progress, a collection code, a security event, money leaving an account. Nothing else is urgent at 23:00."),
    dict(t="Four rungs, then silence",
         p="Reminder ladders escalate by specificity — neutral, specific, consequence, final — and stop. Pinned does not send a fifth message, and it never sends one after the final notice. The 6-hour dwell reminder is a fifth rung at the wrong end and should go."),
    dict(t="One promotional message per person per week",
         p="Across every sequence, every lane. Transactional messages are uncapped, but each one must pass the clarity contract — a transactional message that fails it is promotional with extra steps."),
    dict(t="Every escape hatch is in the message",
         p="If there is an alternative — door delivery, redeliver, extend, decline — it appears in the message that creates the problem, not in a later one. Rung 2 of the storage ladder converts because the escape hatch is right there."),
    dict(t="Internal words stay internal",
         p="Dwell, batch, OTP, eligibility, heartbeat, float, SLA, vhost. None of these reach a customer or a runner. The customer-facing word is listed beside each one in the glossary."),
]

POSITIONING = dict(
    line="Uko wapi?",
    body="The question every delivery in Nairobi collapses into. The sender rings the rider, the receiver "
         "rings the sender, the shop rings everybody, and nobody has an answer. Pinned's product is the "
         "answer — a code, a map and a pod instead of four phone calls.",
    where=[
        ("First contact, once per person", "The sign-up message, and nowhere else in the sender journey. "
                                           "A line this good survives exactly as long as it stays rare."),
        ("Marketing, freely", "Groups, print, the landing, the merch. Repetition is the job there."),
        ("Never in a transactional message", "A storage charge, a failed delivery or a collection code is "
                                             "not the moment for a slogan. It reads as a company enjoying "
                                             "itself while the customer has a problem."),
        ("Never translated into English in copy", "“Your answer to where are you?” is a different, worse "
                                                  "sentence. It works because it is the words people "
                                                  "actually use."),
    ])

GLOSSARY = [
    ("dwell", "free storage"), ("batch", "job, or run"), ("OTP", "collection code"),
    ("handover code", "handover code — keep it, runners and hosts use it daily"),
    ("batch eligibility", "offers"), ("heartbeat", "online / offline"),
    ("floated back", "gone back to the job pool"), ("vhost", "your station, your location"),
    ("pod", "pod — it is on the hardware, customers learn it"),
    ("KES / KSh / Ksh", "Ksh, everywhere, no exceptions"),
    ("parcel", "parcel — never 'package', never 'item', never 'shipment'"),
    ("trip", "trip — the app's word for the delivery and its fee (SENDER_APP_V2_SURFACES.md). "
             "It stays in the app, where a button can carry it. In an SMS, say what the person is "
             "doing: 'send your first package'"),
]

EVIDENCE = dict(
    title="Four notifications, one job, twenty minutes",
    body="A Pinned Runner lock screen on the morning of 9 October: four notifications at 4, 5, 10 and 24 minutes, every one of them reading <i>New delivery available — Pickup: Superior - Gatakaini. Batch distance: 15.8 km.</i> Same batch. Same words. No payout, no parcel count, no closing time, nothing to tell the fourth from the first.",
    close="This is not a copy problem, it is a system that does not know what it has already said. Everything on this site exists to stop that specific lock screen from happening again.",
)

BUILD_ORDER = [
    dict(w="Week 1", t="Stop the bleeding",
         items=[("C4c", "Fix the <code>{{station}}</code> token printing where the collection code belongs — receivers on the paid rung are getting the wrong value."),
                ("R7", "Add a collapse key to <code>FcmSender</code> and key offers on <code>batch_offer:{batch_id}</code>."),
                ("R7", "Restore the proximity and vehicle-class filters in <code>BatchOffer::Build</code>; stop pushing offers to runners who are offline."),
                ("S2d", "Retire one of <code>parcel_dropped</code> / <code>parcel_handed_to_runner</code>."),
                ("—", "Normalise currency to Ksh across all 33 live templates."),
                ("R8b", "Retire the per-sign-in code SMS in favour of a device PIN — the single biggest "
                        "SMS saving on the estate, and the review has already approved it.")]),
    dict(w="Week 2", t="Rewrite what already fires",
         items=[("—", "Replace the body of every live template with the copy in the library. No schema change, no new triggers — it is a content migration against <code>NotificationTemplate</code> keys."),
                ("R7", "Put payout, stop count and distance in the offer title."),
                ("C4a", "Retire the 6-hour dwell reminder; the ladder becomes four rungs."),
                ("C4a C4b C4c", "Re-time the ladder onto the 24-hour storage clock. The seeded keys "
                                "<code>dwell_reminder_24h</code>, <code>_48h</code> and "
                                "<code>_storage_started_72h</code> describe a 72-hour free window that "
                                "does not exist — the names become misleading the day the schedule changes."),
                ("H4", "Move the settlement amount into the email subject line."),
                ("—", "Apply the review's channel decisions: 9 touchpoints change channel, 1 is retired. "
                      "Most are a channel flag, not new copy."),
                ("S0 S0b", "Replace “Your OTP code is …” with the detailed sign-up and sign-in messages.")]),
    dict(w="Week 3", t="Close the map's gaps",
         items=[("R2", "First-run primer — SMS, email and in-app, once ever. The highest-value missing message in the business."),
                ("R3", "Delivery-completed earnings reveal in-app."),
                ("R5 R6", "In-run prompts: running late, loaded at the pod."),
                ("A1a A1b A2 A3 A4", "The five admin interventions. None of them exist today."),
                ("C3", "Receiver delay message."),
                ("H7", "Host-side dwell request — the question behind two answers that already ship."),
                ("R9 R10 R11", "Suspension, reinstatement and account deletion. None of them exist, and "
                               "the first one is the most frightening message Pinned can send."),
                ("H5b", "Pod back online. An alert with no all-clear trains hosts to ignore alerts."),
                ("C1 C1b", "Split the receiver's first contact: a parcel created is not a parcel moving.")]),
    dict(w="Week 4", t="Make it compound",
         items=[("C7", "Collected → save your address."),
                ("P3 P4 P5", "The three prospect sequences, each capped at one message."),
                ("—", "Quiet hours and the per-person frequency cap, enforced in <code>Notifications::DispatchWorker</code> rather than per caller."),
                ("—", "A send log per recipient, so the cap and the one-event-one-message law can be checked rather than hoped for.")]),
]

CODE_NOTES = [
    ("<code>NotificationTemplate</code>", "33 seeded keys with editable bodies and a token set. Every rewrite on this site is a change to <code>body</code> — no migration needed."),
    ("<code>Notifications::DispatchWorker</code>", "The one place every channel passes through. Quiet hours, frequency caps and the send log belong here, not in each caller."),
    ("<code>FcmSender</code>", "Posts title, body, tokens and data. No collapse key, no priority, no TTL — add all three."),
    ("<code>Routing::BatchOffer::Build</code>", "Builds the offer push. Radius and vehicle-class filters are commented out; the body is assembled inline rather than from a template."),
    ("<code>MessageTemplate</code>", "Campaign copy, with a validator that already refuses promotional bodies without an opt-out. The prospect sequences belong here."),
    ("<code>MessageSender</code>", "Sender identity: PINNED for SMS and WhatsApp, notifications@pinnedflow.app for email."),
]


# ═════════════════════════════════════════════════════════════════════════════
# ROUND 2 — the team review, 13 October 2026
#
# Three documents and one annotated screenshot came back from the team:
#   Senders Communication Touchpoints.docx  — copy + keep/remove per channel
#   PINNED RUNNERS COMMS.docx               — rewritten copy, warmer
#   PINNED HOST TOUCHPOINTS REVIEW.docx     — channel decisions + policy flags
#   Runner comms screenshot                 — keep / move / missing messages
#
# Their decisions are applied below rather than edited into the round-1 block,
# so the provenance of every change stays readable. REVIEW merges onto the
# touchpoint of the same id; NEW_TOUCHPOINTS adds what the review asked for.
# ═════════════════════════════════════════════════════════════════════════════

SAMPLES["reason_short"] = "your ID photo was unreadable"

REVIEW_SOURCES = [
    ("Senders Communication Touchpoints.docx", "Copy rewrites and a keep/remove recommendation on every sender touchpoint."),
    ("PINNED RUNNERS COMMS.docx", "Six runner messages rewritten warmer, in the team's own voice."),
    ("PINNED HOST TOUCHPOINTS REVIEW .docx", "Channel decisions plus three policy questions that have to be answered before the copy can ship."),
    ("Runner comms screenshot, 9 Oct", "Keep / move markings per channel, and four messages that do not exist yet."),
]

# ── the warmth layer ─────────────────────────────────────────────────────────

WARMTH_INTRO = (
    "Round one was correct and cold. It answered <i>what happened, what do I do</i> and never "
    "<i>why should I care</i>. Warmth is not decoration and it is not exclamation marks — it is "
    "the four or five places in a journey where a person has something at stake, and we show that "
    "we know it. Everywhere else, warmth is noise.")

WARMTH_MOVES = [
    dict(n="01", t="Use their name where there is a person, not a parcel",
         p="At the start, at a milestone, at a failure and anywhere money moves. Not on routine status.",
         yes="Wanjiru, your refund of Ksh 1,250 for Parcel PN-4K7Q2 has been processed.",
         no="Hi Wanjiru! Parcel PN-4K7Q2 is now in transit, Wanjiru."),
    dict(n="02", t="Name the stake, not the record",
         p="“Your first job”, “someone has sent you something”, “your account is open”. The sentence that tells them why this message is about them and not about our database.",
         yes="Congratulations Brian on your first job.",
         no="Batch B-2291 status: accepted."),
    dict(n="03", t="Acknowledge the wait or the effort — once",
         p="A single line of recognition where someone has given us time, documents or patience. One line. Never two, never in every message.",
         yes="Thank you Brian for submitting your documents. We appreciate your patience.",
         no="We appreciate your patience. Thank you for bearing with us. Sorry for the wait."),
    dict(n="04", t="Celebrate the real milestone, ignore the fake one",
         p="Approval, first run, first delivery, the week they beat their own record. Not “your parcel has moved to the next stage”.",
         yes="Delivery complete · Ksh 640 earned. Keep going — your next job is waiting.",
         no="Congratulations! Your parcel has successfully entered the sorting process!"),
    dict(n="05", t="Assume the kind reason",
         p="People go offline because the battery died, miss a drop-off because the day ran away with them, and fail to collect because they are at work. Write as if that is true, because it usually is.",
         yes="If that wasn't you, open the app and tap Go online.",
         no="You have failed to remain available as required."),
    dict(n="06", t="Leave the door open on a no",
         p="Every rejection, denial, suspension or failure names the way back in the same message — and says it in a sentence a person would actually say out loud.",
         yes="If you think this is wrong, you can appeal here.",
         no="This decision is final. Contact support for further information."),
]

WARMTH_BUDGET = [
    ("Senders", "Sign-up, handover code, delivered, refund, return. Five warm moments in a journey of a dozen messages."),
    ("Receivers", "The first message — someone has sent you something — and the collected message. The ladder in between stays plain; warmth inside a charging notice reads as sarcasm."),
    ("Runners", "Welcome, documents received, approved or not approved, first job, every job completion, suspension and its reversal. The runner lane carries the most warmth because it carries the most at stake."),
    ("Hosts", "Activation and the weekly settlement. A host is a business, and a business wants the number and the facts — but the first week and the money are still human moments."),
]


# ── what the team changed ────────────────────────────────────────────────────
# status "change" = the message stays, the channel mix does not
# status "retire" = the message goes away entirely

REVIEW = {

    # ── SENDERS ──
    "S1": dict(
        channels=["in_app"], status="change",
        review="<b>In-app only.</b> The welcome SMS is dropped — nothing in it is time-critical, "
               "and the sign-up code SMS has already landed on the same phone a minute earlier.",
        warmth="Their name, and a pod they can picture. That is the whole warmth budget for a welcome.",
        msgs=[("in_app", ("Welcome to Pinned, {{name}}",
                          "Your nearest pod is {{pod}}, {{km}} km away. Booking takes about a minute, and you pay after the price is shown."))]),

    "S2": dict(
        channels=["in_app", "sms"], status="change",
        review="<b>In-app only — with one exception.</b> The SMS fires only when no drop-off slot was "
               "booked, because then the code is the only thing the sender is holding.",
        rules=["A booking message states an expiry. A reservation without a deadline is a wish.",
               "The in-app card carries no code because the app already holds it. The SMS exception does, "
               "on its own line, in DM Mono — the brand reserves mono for codes."],
        msgs=[("in_app", ("Booked — drop by {{deadline}}",
                          "{{pod}} · open until {{closing_time}}. Directions, or switch to runner collection, in one tap.")),
              ("sms", "Booked. Parcel {{code}} is reserved at {{pod}} until {{deadline}}. Enter this code at the pod — no queue, no paperwork.\n[only when no slot was booked]")]),

    "S2b": dict(
        channels=["sms"], status="live",
        review="<b>SMS works.</b> Kept as it is.",
        warmth="Lead with the favour, not the chase. The message exists to save them a journey.",
        rules=["This is not a reminder, it is an offer — so the offer goes first and the reminder "
               "second. “You have not dropped your parcel” is a complaint; “save yourself the trip” "
               "is a service.",
               "One message only. If the hold lapses, the booking card says so; we do not chase twice."],
        msgs=[("sms", "{{name}}, save yourself the trip — a runner can collect Parcel {{code}} from you instead: {{track_url}}\nOtherwise it stays held at {{pod}} until {{deadline}}.")]),

    "S2c": dict(
        channels=["sms", "in_app"], status="change",
        review="<b>Add in-app.</b> The code should be readable in the app as well as the SMS — senders "
               "at a counter with a flat battery are the whole reason this message exists twice.<br><br>"
               "<b>No scan.</b> An earlier draft said to give the code “once they have scanned the parcel”. "
               "That is not the procedure: on the sender side the code <i>is</i> the hand-over. There is no "
               "scan action for a sender to wait for.",
        rules=["The code is the hand-over. Nothing precedes it and nothing has to be witnessed first, so "
               "the copy must not invent a step the sender will stand there waiting for.",
               "The security line names the actual attack — “by phone” — not “do not share”.",
               "Nothing else ships in a code message. No tracking link, no marketing, no thanks."],
        msgs=[("sms", "Your handover code for Parcel {{code}} is {{otp}}.\nGive it to {{runner}} as you hand the parcel over. We never ask for this code by phone."),
              ("in_app", ("Handover code for Parcel {{code}}", "{{otp}}\nGive it to the runner as you hand the parcel over."))]),

    "S2d": dict(
        channels=["in_app"], status="change",
        review="<b>In-app only.</b> This also settles the round-one defect: with the SMS dropped, "
               "<code>parcel_dropped</code> and <code>parcel_handed_to_runner</code> stop competing — "
               "one in-app card replaces both.",
        msgs=[("in_app", ("Picked up by {{runner}}", "Parcel {{code}} arriving {{dest}} about {{eta}}. Live map in the app."))]),

    "S3": dict(
        channels=["sms", "in_app"], status="live",
        review="<b>Looks good.</b> Two segments, and the team kept the thank-you — this is the one "
               "message in the sender journey that has earned it.",
        warmth="Celebrate the real milestone. The parcel arrived, a named person took it, and we can prove it.",
        rules=["Round one said gratitude belongs where it costs nothing. The team overruled that here and "
               "they are right: this is the one sender message that has earned a thank-you, because it is "
               "the one that reports a success.",
               "Proof is the product. Every delivered message links to it.",
               "Two segments. A delivery confirmation that drops the name, the place or the time to save "
               "a segment is a worse message and a cheaper one."],
        msgs=[("sms", "Delivered. {{name}} collected Parcel {{code}} at {{dest}}, {{time}}.\nPhoto, signature and the full timeline are saved to this parcel. Thank you for using Pinned."),
              ("in_app", ("Delivered · {{time}}", "{{name}} collected Parcel {{code}} at {{dest}}. Photo, signature and the full timeline are saved to this parcel."))]),

    "S4a": dict(
        channels=["sms", "in_app"], status="live",
        review="<b>Looks good.</b>",
        msgs=[("sms", "Parcel {{code}} is still at {{station}}. {{name}} has been reminded.\nStorage is now Ksh {{rate}}/hr, charged to you. If it is not collected by {{deadline}} it will be returned to you."),
              ("in_app", ("Storage running on Parcel {{code}}",
                          "Ksh {{rate}}/hr from today, Ksh {{amount}} so far. Returns to you after {{deadline}}.\n[ Message the receiver ]  [ Return it now ]"))]),

    "S4b": dict(
        channels=["sms", "in_app"], status="change",
        review="<b>Add in-app.</b> A return is a thing the sender has to plan around, so it belongs in "
               "the parcel record, not only in a text they will scroll past.",
        warmth="No scolding of the receiver, and no 'final notice'. State the fact, carry the cost once.",
        msgs=[("sms", "Parcel {{code}} comes back to you today — {{name}} did not collect it.\nA runner brings it from {{dest}} to {{origin}}. Storage charged: Ksh {{amount}}."),
              ("in_app", ("Returning to you today", "Parcel {{code}} from {{dest}}. A runner brings it to {{origin}}. Storage charged: Ksh {{amount}}."))]),

    "S5": dict(
        channels=["sms"], status="live",
        review="<b>Looks good.</b> The team's wording is used as written — it is warmer than round one and "
               "answers the only question a refund raises.",
        warmth="Thank them for the patience the refund cost them.",
        msgs=[("sms", "{{name}}, your refund of Ksh {{amount}} for Parcel {{code}} has been processed.\nIt will reflect on your M-Pesa within 3 working days. Thank you for your patience.")]),

    "S6": dict(
        channels=["sms", "in_app"], status="live",
        review="<b>Looks good.</b>",
        msgs=[("sms", "Parcel {{code}} did not reach {{dest}}: {{reason}}.\nIt is safe at {{station}}. Choose redeliver or return by {{deadline}}: {{track_url}}"),
              ("in_app", ("Parcel {{code}} held at {{station}}",
                          "{{reason}}. Redeliver tomorrow at no extra cost, or have it returned. Choose by {{deadline}}."))]),

    # ── RUNNERS ──
    "R0": dict(
        channels=["sms"], status="live",
        review="<b>Keep.</b> The team's own wording, used as written.",
        warmth="Name the stake — six minutes between here and earning.",
        msgs=[("sms", "Hello {{name}}, welcome to Pinned Runners.\nIn just 6 minutes you will be able to access jobs on your app. Follow these simple steps to complete verification: {{link}}")]),

    "R1a": dict(
        channels=["in_app"], status="change",
        review="<b>Move to in-app.</b> The screenshot marks the document-upload SMS <i>move to in app</i> "
               "and the application-under-review card <i>keep</i>. So the warm copy the team wrote for the "
               "SMS carries over to the card, and the SMS is dropped.",
        warmth="Thank them for the documents, and own the wait rather than explaining it away.",
        rules=["{{hours}} is filled from a real review clock, not written into the sentence. “Within 24 "
               "hours” is a promise nobody can measure us against; a number the system computes is one "
               "we can be held to.",
               "“We appreciate your patience” does the job “nothing to do until then” did in round one — "
               "it tells them to stop refreshing. Keep one of the two, never both.",
               "The support email in the live SMS goes nowhere: runners call or use in-app help. It is "
               "dropped with the SMS."],
        msgs=[("in_app", ("We're reviewing your documents",
                          "Thank you {{name}} for submitting your documents. We are reviewing them and you will hear from us within {{hours}} hours. We appreciate your patience."))]),

    "R1b": dict(
        channels=["sms", "in_app"], status="change",
        review="<b>SMS, kept.</b> Email is dropped here — the screenshot lists this one as SMS only. "
               "Pay day, the support number and what was verified move to the first-run email (R2), which "
               "is where a runner actually needs them.",
        warmth="Congratulations, by name. This is the moment they became a Pinned runner.",
        rules=["Pay day, the support number and what was verified are the things a runner needs twice. "
               "Round one put them in an approval email; the review drops that email, so they move to the "
               "first-run email at R2 — the point where a runner actually goes looking for them.",
               "An exclamation mark is allowed here and almost nowhere else. Somebody just got a job."],
        msgs=[("sms", "Congratulations {{name}}! Your application has been approved.\nClick the link below or download the app to access available jobs. Welcome to Pinned.\n{{link}}"),
              ("in_app", ("Approved — you can go online", "Tap Go online and offers near {{origin}} will start arriving."))]),

    "R1c": dict(
        channels=["sms", "in_app"], status="change",
        review="<b>SMS, kept.</b> Email dropped — the screenshot lists SMS only, and a rejection that needs "
               "an email to be understood has been written badly.",
        warmth="Leave the door open: one fixable thing, and a day to a second answer.",
        msgs=[("sms", "Unfortunately {{name}}, we couldn't approve your account yet.\nKindly {{reason}}. Resubmit your application to be reviewed within a day."),
              ("in_app", ("One thing to fix", "{{reason}}. Replace your {{docs}} and submit again — we review within a day.\n[ Replace document ]"))]),

    "R2": dict(
        channels=["sms", "email", "in_app"], status="gap",
        review="<b>Still to build.</b> The team wrote the SMS; note they replaced “scan every parcel” with "
               "“leave your app open during delivery”. Both matter — the open app is what gives live "
               "tracking, the scan is what transfers custody — so the SMS carries the team's three, and "
               "the scan rule stays in the email where it can be explained.",
        warmth="Congratulate the first job. It is the only first job they will ever have.",
        msgs=[("sms", "Congratulations {{name}} on your first job.\nThree things that matter: arrive by {{eta}}, leave your app open during delivery, and never hand over without the code.\nFull guide: {{link}}"),
              ("email", ("Your first Pinned run — what happens at each stop",
                         "Congratulations on your first job.\n\n1. Collect. Scan each parcel at the pod or counter. The app will not let you leave with an unscanned parcel, and that is what protects you if anything is questioned later.\n\n2. Keep the app open. That is what gives the sender and the receiver live tracking, and what proves where you were.\n\n3. Custody. From the scan until hand-over the parcel is yours. If anything looks wrong — open box, wet, wrong label — photograph it in the app before you move.\n\n4. Hand over. The receiver reads you their code. You enter it. Never accept a code sent to you by anyone else, and never read the code out first.\n\n5. Get paid. Earnings land every {{deadline}} on the M-Pesa number on your account.\n\nIf a receiver is not there: wait 5 minutes, call from the app, then mark 'not available'. Do not leave a parcel with a neighbour.\n\nHelp, any time: 0700 000 000.")),
              ("in_app", ("Three rules for every run", "Arrive on time · keep the app open · no hand-over without the code.\n[ 90-second guide ]"))]),

    "R3": dict(
        channels=["in_app"], status="gap",
        review="<b>Still to build.</b> The screenshot calls it a job-completion pop-up and gives the "
               "closing line. It is merged with the earnings reveal — the money and the encouragement "
               "belong in the same card, not two.",
        warmth="Celebrate, then point at the next one. This is the single most repeated warm moment in the business.",
        msgs=[("in_app", ("Delivery complete · Ksh {{payout}} earned",
                          "Parcel {{code}} handed to {{name}} at {{dest}}.\nToday: {{stops}} stops · Ksh {{amount}}\nKeep going — accept your next job to earn more."))]),

    "R5": dict(
        channels=["in_app"], status="gap",
        review="<b>Still to build.</b> The team's wording, with the live-updates line they added.",
        warmth="No reprimand. Hand them the button that fixes it for the receiver.",
        msgs=[("in_app", ("Running late to {{dest}}",
                          "You are running late for your delivery to {{dest}}. Send the receiver a new ETA, and leave the app open for live updates.\n[ Send ETA ]  [ I need help ]"))]),

    "R7": dict(
        review="<b>Team wording:</b> <i>“New pinned delivery available near you, Pick up {{origin}} batch "
               "distance {{km}} km, view in app.”</i> “Near you” is kept — it is the reason to look. The "
               "money still has to lead, because the title is the only line read on a locked phone, and "
               "because four identical titles are what caused the damage in the first place.",
        msgs=[("push", ("Ksh {{payout}} · {{stops}} parcels · {{km}} km",
                        "New delivery near you from {{origin}}. Tap to view and accept — closes {{eta}}."))]),

    # ── HOSTS ──
    "H1a": dict(
        channels=["sms", "email", "in_app"], status="partial",
        review="<b>Keep all three — but stop them repeating each other.</b> SMS activates, email teaches "
               "the operation (booking, same-day cut-off, collection, handover codes, failed deliveries, "
               "weekly settlement), in-app asks for exactly three things: cut-off time, counter contact, "
               "settlement number."),

    "H1b": dict(
        channels=["sms", "email", "in_app"], status="partial",
        review="<b>Keep it separate from H1a.</b> A pod host receives, stores and releases; a business "
               "sender sends. The email covers verifying a runner, scanning every parcel, releasing the "
               "handover code only after the scan, and verifying a customer's collection code. The in-app "
               "card asks for opening hours and counter contact."),

    "H2": dict(
        channels=["in_app", "email"], status="partial",
        review="<b>In-app, plus the explanatory email the first time only.</b> Fire once per assignment, "
               "and never repeat it without a meaningful change — an updated ETA goes out only when the "
               "estimate moves materially.",
        msgs=[("in_app", ("{{runner}} is collecting {{stops}} parcels · ETA {{eta}}",
                          "Have them at the counter. Release the handover code only after the scan.")),
              ("email", ("How hand-over works at {{address}}",
                         "A runner is on the way for the first time, so here is the sequence.\n\n1. They arrive and identify themselves in the app — you see the same name in your portal.\n2. They scan each parcel. The scan is what transfers responsibility from you to Pinned.\n3. You release the handover code. After the scan, never before.\n\nThat is the whole process. You will not get this email again — from now on it is a line in the portal."))]),

    "H3": dict(
        channels=["sms", "in_app"], status="partial",
        review="<b>Keep both, fire immediately.</b> The portal carries Redeliver and Return as actions and "
               "states what happens if the host does nothing. The vague “our team will call you shortly” "
               "is removed.",
        notes_add=[("warn", "<b>Policy to confirm.</b> Automatic redelivery as the no-response default is "
                            "only correct if that is the approved operational policy. If it is not, the "
                            "in-app copy below has to change before it ships.")]),

    "H4": dict(
        channels=["email", "in_app"], status="partial",
        review="<b>Keep both.</b> Amount in the subject line, and the email states the amount, the parcel "
               "count, the period, when the money arrives and where the statement is. Statement stays "
               "available as an attachment and in the portal under Settlements.",
        notes_add=[("warn", "<b>Policy to confirm.</b> “Within one working day” must match what finance "
                            "actually does. If it does not, change the sentence rather than the finance "
                            "process — a settlement promise we miss costs more than a vaguer one.")]),

    "H5": dict(
        channels=["sms"], status="partial",
        review="<b>Keep the SMS, after the approved grace period.</b> Support number stays in the message "
               "so the host never has to open a portal while standing next to a dead pod. Prolonged "
               "outages escalate to operations."),

    "H6": dict(
        channels=["email"], status="partial",
        review="<b>Keep email — but activate the template and finish it first.</b> It has to explain the "
               "offer, the benefit to the host, the space needed, who installs and maintains, the "
               "commercial terms, and how to proceed. Sell the opportunity before asking for the click.",
        notes_add=[("warn", "<b>Policy to confirm.</b> The 2 m², installation, maintenance and insurance "
                            "commitments, and the fee structure, must be confirmed as real before this "
                            "goes out. State the approved fee rather than implying unspecified earnings.")]),

    "H7": dict(
        channels=["in_app"], status="gap",
        review="<b>Build it.</b> Show who is asking, how long for, the pod and when free storage ends, with "
               "Approve and Decline. The receiver already gets an answer; the host currently gets no question.",
        msgs=[("in_app", ("{{name}} wants {{hours}}h more on a parcel",
                          "At {{station}}, free storage ends {{deadline}}.\n[ Approve ]  [ Decline ]"))],
        notes_add=[("warn", "<b>Policy to confirm.</b> What happens if the host does not answer before the "
                            "deadline? Auto-approve, auto-decline or escalate — the copy cannot be finished "
                            "until that is decided.")]),
}


# The receiver lane was not in the review pack, so these two changes come from
# the brief directly: a parcel that has merely been created is a different
# message from a parcel that is actually on its way.
REVIEW["C1"] = dict(
    name="A parcel has been created for you",
    stage="First contact",
    trigger="A sender or a virtual host creates a parcel addressed to this person",
    timing="At creation", channels=["sms"], status="change",
    intent="A heads-up, not an instruction. Nothing is moving yet and there is nothing to do.",
    review="<b>Split in two.</b> A notification that a parcel exists and a parcel that is actually on "
           "its way are different messages with different jobs. This one tells them something is coming "
           "and asks for nothing; C1b tells them it is moving and gives them a time.",
    warmth="Name the stake: someone thought of them. It is the only message in the lane that gets to be nice.",
    msgs=[("sms", "Good news {{name}} — {{from}} is sending you a parcel through Pinned.\nIt is being prepared at {{origin}}. Nothing to do yet; we will text you the moment it is on its way.")])

NEW_TOUCHPOINTS = [

    # ── sender and runner access ──
    T(id="S0", lane="sender", stage="Access", name="Sign-up code",
      trigger="A new sender requests a verification code", timing="On request · expires in 5 minutes",
      channels=["sms"], status="gap", source="Brief · 13 Oct", hook="Action",
      intent="The first message Pinned ever sends a sender. It carries the code, and it names the pain Pinned exists to remove.",
      old="Your OTP code is ….",
      warmth="Their name, and a promise in the language the problem is actually argued in.",
      review="<b>Lead with the painkiller.</b> An earlier draft — <i>“Welcome to Pinned. Your sign-up code "
             "is …”</i> — was correct and said nothing. It carried no name and no reason to care. "
             "<b>Uko wapi?</b> is the question every delivery in this city turns into: the sender ringing "
             "the rider, the receiver ringing the sender, nobody with an answer. Pinned <i>is</i> the "
             "answer, and the first message is the one place that claim belongs.",
      msgs=[("sms", "Karibu Pinned, {{name}} — your answer to UKO WAPI?\nSign-up code: {{otp}}\nSend your first package and watch it move, every second.\nOTP Expires in 5 minutes. We never ask for this code by phone.")],
      notes=[("warn", "<b>Two words for one thing, twice.</b> This copy is approved as written, and it "
                      "carries two unresolved vocabulary questions that reach past this message. "
                      "<b>“package”</b> — every live template, the team's sender review and the rest of "
                      "this site say <i>parcel</i>; the brand guide's own push mock-up says "
                      "<i>“Your package has arrived…”</i>. One of them has to give. "
                      "<b>“OTP”</b> — line two calls it a sign-up code and line four calls it an OTP, "
                      "four lines apart. Kenyan customers genuinely know the word OTP from M-Pesa and "
                      "banking, so the rule against it may be the thing that is wrong — but not both "
                      "names in one SMS. Both are on the Build order page as open questions.")],
      rules=["<b>The sign-up code is the one code message allowed to sell.</b> It is first contact as well "
             "as authentication. Every later code — sign-in, collection, handover — ships bare.",
             "The expiry and the fraud line survive the rewrite. They are the two questions every code "
             "message raises, and dropping them to make room for the promise would be the wrong trade.",
             "“Watch it move, every second” is a promise the runner app has to keep. Live tracking depends "
             "on the runner's app staying open — which is exactly why R2 teaches that on day one.",
             "Two segments, and the only message in the lane where the second one is spent on warmth."]),

    T(id="S0b", lane="sender", stage="Access", name="Sign-in code",
      trigger="A sender signs in", timing="Each sign-in · expires in 5 minutes",
      channels=["sms"], status="gap", source="Brief · 13 Oct", hook="Trigger",
      intent="A sign-in code is also a security alert. It should read like one — without claiming to know things we do not know.",
      old="Your OTP code is ….",
      warmth="Reassure in the same line as the warning. Ignoring it is enough; they do not have to do anything.",
      review="<b>No device name.</b> An earlier draft read <i>“Someone is signing in on a Samsung A14”</i>. "
             "We have no device visibility, so that sentence is void. What is left still does the job: "
             "what the code is for, how long it lasts, what to do if it was not them, and the fraud line.",
      msgs=[("sms", "{{name}}, your Pinned sign-in code is {{otp}}.\nIt expires in 5 minutes. If you did not ask to sign in, ignore this message — your account stays locked and we never call or text to ask for this code.")],
      rules=["Write only what the system can actually see. A security message that names a device we "
             "cannot identify is worse than one that does not, because the first time it is wrong the "
             "customer stops believing all of them.",
             "Naming the device and the town is the upgrade the moment device data exists. Until then "
             "this copy stands.",
             "Never include a link in a sign-in message. Every phishing SMS in this market has one."]),

    T(id="R8a", lane="runner", stage="Access", name="Sign-up code",
      trigger="A runner requests a verification code at sign-up", timing="Once, at sign-up",
      channels=["sms"], status="partial", source="Review screenshot", hook="Action",
      intent="One code, once. After this the device is trusted and the PIN takes over.",
      warmth="Welcome, then the code. The runner lane earns warmth at every door.",
      msgs=[("sms", "Welcome to Pinned Runners. Your sign-up code is {{otp}}.\nIt sets up this phone as yours and expires in 5 minutes. We never call or text to ask for this code.")],
      rules=["This is the only code SMS a runner should ever receive on a device they keep."]),

    T(id="R8b", lane="runner", stage="Access", name="Sign-in code on every sign-in",
      trigger="A runner signs in", timing="Every sign-in, today",
      channels=["sms"], status="retire", source="Review screenshot", hook="Action",
      intent="A runner signs in several times a day. An SMS each time is a cost, a delay and a habit that teaches them codes are routine.",
      old="OTP to log in to the account",
      review="<b>Retire.</b> The screenshot is explicit: move to a PIN at sign-in after the first code at "
             "sign-up. Riders sign in on the roadside with one bar of signal — a four-digit PIN on a "
             "trusted device is faster, cheaper and safer than an SMS that may take a minute to arrive.",
      msgs=[],
      notes=[("team", "<b>Replaced by nothing.</b> After the sign-up code, sign-in is a 4-digit PIN on the "
                      "trusted device. A code SMS fires again only on a new device, a PIN reset, or 30 days "
                      "of inactivity.")],
      rules=["Dropping this removes the single highest-volume SMS in the runner lane.",
             "A new device, a PIN reset or 30 days of inactivity still earns one code SMS. Nothing else does."]),

    # ── runner account state, from the review screenshot ──
    T(id="R9", lane="runner", stage="Account state", name="Account suspended",
      trigger="Admin suspends a runner account", timing="Immediately", channels=["sms", "in_app"],
      status="gap", source="Review screenshot · missing", hook="Action",
      intent="The most frightening message Pinned sends. It has to carry the reason and the way back, in that order.",
      warmth="Leave the door open, in a sentence a person would say out loud.",
      review="<b>Missing — build it.</b> The team's wording, with the appeal link made explicit.",
      msgs=[("sms", "Hi {{name}}, your Pinned account has been suspended: {{reason}}.\nIf you feel this was wrong, you can appeal here: {{link}}"),
            ("in_app", ("Account suspended", "{{reason}}. Offers are paused while this is open.\n[ Appeal this ]  [ Call support ]"))],
      rules=["Never suspend silently. A runner who finds out by seeing no offers assumes the app is broken, and tells other runners it is broken.",
             "The reason is specific and in plain words — never a policy code.",
             "The appeal route is in the first message, not in a follow-up."]),

    T(id="R10", lane="runner", stage="Account state", name="Suspension lifted",
      trigger="Admin reverses a suspension", timing="Immediately", channels=["sms", "in_app"],
      status="gap", source="Review screenshot · missing", hook="Reward",
      intent="Get them earning again in one sentence, and say the record is clear.",
      warmth="Good news, said as good news. This person has been out of work.",
      msgs=[("sms", "Good news {{name}} — your account has been reviewed and the suspension lifted.\nYou can go online and start accepting jobs again."),
            ("in_app", ("You're back online", "The suspension has been lifted and your rating is unchanged.\n[ Go online ]"))],
      rules=["Say the rating and standing are unchanged, if they are. Silence on that point reads as a permanent mark.",
             "This message goes out the moment the decision is made, not on the next batch run. Every hour of delay is money the runner did not earn."]),

    T(id="R11", lane="runner", stage="Account state", name="Account deleted",
      trigger="A runner deletes their account", timing="Immediately", channels=["sms", "email"],
      status="gap", source="Review screenshot · missing", hook="Trigger",
      intent="Confirm it happened, and give a human a window to undo a mistake.",
      warmth="No guilt, no win-back offer. They asked; we confirm and leave the door unlocked.",
      msgs=[("sms", "Hi {{name}}, your Pinned account has been deleted.\nIf this was an error, contact customer care on 0102482883 within 30 days and we can restore it."),
            ("email", ("Your Pinned account has been deleted",
                       "Your account is closed and you will not receive job offers.\n\nAny earnings already approved are paid on the normal settlement date to the M-Pesa number on the account.\n\nYour delivery records are kept for the period the law requires and are not used for anything else.\n\nIf this was a mistake, call 0102482883 within 30 days and we can restore the account exactly as it was."))],
      rules=["No retention offer, no survey, no “are you sure” after the fact. They already decided.",
             "Say what happens to money and to records. Those are the two things people worry about after they press delete."]),

    # ── receiver: the parcel that is actually moving ──
    T(id="C1b", lane="receiver", stage="First contact", name="It is on its way to you",
      trigger="A runner collects the parcel and it is moving toward the receiver",
      timing="At pickup", channels=["sms"], status="partial", key="runner_picked_up_receiver",
      source="Brief · 13 Oct", hook="Trigger",
      intent="The expected parcel. Now there is a person, a place and a time.",
      review="<b>The second half of the split.</b> C1 says something is coming; this one says it is moving "
             "and gives them a time they can plan around.",
      msgs=[("sms", "Your parcel from {{from}} is on the way to {{dest}} with {{runner}}, arriving about {{eta}}.\nFollow it: {{track_url}}")],
      rules=["A time is the whole point of this message. If there is no reliable ETA, do not send it — wait for the arrival message instead.",
             "For a pod delivery this message is optional. For a door delivery it is not, because somebody has to be home."]),

    # ── host: the other half of the offline alert ──
    T(id="H5b", lane="host", stage="Hardware", name="Your pod is back online",
      trigger="A pod resumes its heartbeat after an outage", timing="On recovery", channels=["sms"],
      status="gap", source="Host review · missing", hook="Reward",
      intent="Close the loop the offline alert opened. An alert with no all-clear trains hosts to ignore alerts.",
      warmth="Good news, and a thank-you for whatever they did.",
      review="<b>Add it.</b> The host review asks for a recovery notification, and for prolonged outages to "
             "escalate to operations.",
      msgs=[("sms", "Good news — {{pod}} is back online since {{since}} and collections have resumed. Thank you for sorting it out.")],
      rules=["Only sent if an offline alert went out first. No alert, no all-clear.",
             "If the outage passes the escalation window, operations calls the host before this SMS exists."]),
]


# ── merge the review onto round one ──────────────────────────────────────────

TOUCHPOINTS += NEW_TOUCHPOINTS
for _t in TOUCHPOINTS:
    _t.setdefault("review", None)
    _t.setdefault("warmth", None)

_by_id = {t["id"]: t for t in TOUCHPOINTS}
for _id, _patch in REVIEW.items():
    _tp = _by_id.get(_id)
    if _tp is None:
        raise KeyError("review targets an unknown touchpoint: %s" % _id)
    for _k, _v in _patch.items():
        if _k == "notes_add":
            _tp["notes"] = list(_tp["notes"]) + list(_v)
        else:
            _tp[_k] = _v

ORDER = [
    "S0", "S0b", "S1", "S2", "S2b", "S2c", "S2d", "S3", "S4a", "S4b", "S5", "S6",
    "C1", "C1b", "C2", "C3", "C4a", "C4b", "C4c", "C4d", "C5", "C6a", "C6b", "C7",
    "R0", "R8a", "R8b", "R1a", "R1b", "R1c", "R2", "R7", "R6", "R5", "R3", "R4",
    "R9", "R10", "R11",
    "H6", "H1a", "H1b", "H2", "H3", "H7", "H5", "H5b", "H4",
    "A1a", "A1b", "A2", "A3", "A4",
    "P1", "P2", "P3", "P4", "P5",
]
_missing = [t["id"] for t in TOUCHPOINTS if t["id"] not in ORDER]
if _missing:
    raise KeyError("touchpoints missing from ORDER: %s" % _missing)
TOUCHPOINTS.sort(key=lambda t: ORDER.index(t["id"]))

STATUS_WORD = {
    "live": "Live", "partial": "Partial", "gap": "Not built",
    "defect": "Defect", "change": "Channel change", "retire": "Retire",
}


# ── the SMS journey, per lane ────────────────────────────────────────────────
# ch: the channel that carries this moment. "sms" steps are the budget; every
# other step is a deliberate decision NOT to spend an SMS on it.

def J(n, when, tp, ch, what, why, flag=None, off=False, grp=None):
    """off=True marks a step that only happens when something goes wrong, so the
    SMS budget quoted on each lane is the budget for a journey that works.
    grp opens a titled block in the summary, so a reader can find the moment they
    came for instead of reading the whole ladder."""
    return dict(n=n, when=when, tp=tp, ch=ch, what=what, why=why, flag=flag,
                off=off or n in ("+", "—"), grp=grp)


JOURNEYS = {

    "sender": dict(
        headline="Four SMS on a journey that works — three once sign-in moves to a PIN",
        sub="Sign-up code, sign-in code, handover code, delivered — and the sign-in code should become a "
            "PIN. Everything between them is in-app, because the sender is holding the app. That is the "
            "whole difference between a sender and a receiver.",
        steps=[
            J("1", "Creates an account", "S0", "sms", "Sign-up code, with the expiry and the fraud line", "The only way to prove the phone is theirs."),
            J("2", "Signs in", "S0b", "sms", "Sign-in code naming the device", "Security, not convenience. Moves to a device PIN if we follow the runner decision.", flag="open"),
            J("3", "Account opens", "S1", "in_app", "Welcome and the nearest pod", "Nothing time-critical. The code SMS landed a minute ago."),
            J("4", "Books a parcel", "S2", "in_app", "Booked — drop by, with directions", "They are in the app, looking at the booking they just made."),
            J("—", "…booked with no drop-off slot", "S2", "sms", "The reservation code", "The exception: with no slot, the code is the only thing they hold."),
            J("+", "Has not dropped it", "S2b", "sms", "Still held for you, plus runner collection", "They are away from the app. This is what SMS is for."),
            J("5", "Pays / runner assigned", "S2c", "sms", "Handover code — and nothing else", "The one message that must survive a flat battery at a counter."),
            J("6", "Runner collects", "S2d", "in_app", "Picked up by {{runner}}, ETA", "A status update, not an instruction. One in-app card replaces the two SMS firing today."),
            J("7", "Delivered", "S3", "sms", "Who collected it, where, at what time", "The payoff. Two segments, and worth every one."),
            J("+", "Receiver has not collected", "S4a", "sms", "Storage started, charged to you", "Money moving against them. Always SMS."),
            J("+", "Day 7", "S4b", "sms", "Coming back to you today", "A thing they have to plan around."),
            J("+", "Refund", "S5", "sms", "Amount, and when it reaches M-Pesa", "Money moving toward them. Always SMS."),
            J("+", "Delivery failed", "S6", "sms", "Reason, location, choice, deadline", "A decision only they can make, on a clock."),
        ]),

    "receiver": dict(
        headline="Four SMS on a journey that works — and the receiver has no app",
        sub="Every receiver rule is the inverse of the sender rules. There is no in-app to fall back on, "
            "so SMS carries everything — which is exactly why the ladder has to stop at four rungs. "
            "A parcel that has been created and a parcel that is moving are two different messages.",
        steps=[
            J("1", "Parcel created for them", "C1", "sms", "Someone is sending you a parcel. Nothing to do yet", "The notification. Informational, no action, no code."),
            J("2", "Runner collects it", "C1b", "sms", "On its way, with a runner and an ETA", "The expected parcel. Optional for a pod drop, required for a door delivery."),
            J("3a", "Arrives at a pod", "C2", "sms", "Station, opening hours, collection code, free-storage deadline, door-delivery escape", "Two segments. Each line in it saves a phone call."),
            J("3b", "Arrives at the door", "C1b", "sms", "Runner at the door — code at hand-over", "The alternative branch: a door delivery skips the pod message entirely.", off=True),
            J("+", "Running late", "C3", "sms", "New time, reason, and when we will text next", "A broken promise gets its own message."),
            J("+", "Half the clock gone", "C4a", "sms", "Still here, code, opening hours, deadline", "Rung 1. No mention of charges — none apply yet."),
            J("+", "4 clock-hours left", "C4b", "sms", "Free storage ends {{deadline}}, then the rate", "Rung 2. Where most door-delivery conversions happen."),
            J("+", "Clock runs out", "C4c", "sms", "Storage started, and how to stop it", "Rung 3. Money is moving."),
            J("+", "Day 7", "C4d", "sms", "Goes back today, total charged", "Rung 4. Then silence."),
            J("+", "Requests more time", "C6a", "sms", "Approved — new deadline", "A decision they are waiting on."),
            J("+", "…declined", "C6b", "sms", "Declined, with door delivery offered instead", "A no that ends with a yes."),
            J("4", "Collects", "C7", "sms", "Thanks — save your address for next time", "Once per receiver, ever. The only ask in the lane."),
        ]),

    "runner": dict(
        headline="Four SMS to get someone working, then almost none",
        sub="Retiring the sign-in code removes the highest-volume SMS in the business. What is left is "
            "the account lifecycle — the messages that decide whether somebody can work today — and "
            "everything about the job itself moves to push and in-app, where the runner already is.",
        steps=[
            J("1", "Admin creates the runner", "R0", "sms", "Welcome, six minutes to verification", "They are not in the app yet. There is no other channel."),
            J("2", "Signs up", "R8a", "sms", "Sign-up code, once", "The device becomes trusted here."),
            J("3", "Signs in, every time", "R8b", "retire", "Nothing — a 4-digit PIN on the trusted device", "Retired. Roadside, one bar of signal, several times a day.", flag="retire"),
            J("4", "Submits documents", "R1a", "in_app", "We're reviewing your documents", "Moved off SMS by the review. They are in the app, having just uploaded."),
            J("5", "Approved", "R1b", "sms", "Congratulations, go online", "The moment they can start earning. Email dropped."),
            J("+", "Not approved", "R1c", "sms", "The one thing to fix, and a day to a second answer", "Email dropped — a rejection that needs an email is badly written."),
            J("6", "First job accepted", "R2", "sms", "Three things that matter, once ever", "Peak attention. SMS, email and in-app all fire — once."),
            J("7", "A job is offered", "R7", "push", "Payout, parcels, distance, closing time", "Free, instant, collapsible. One live offer per batch."),
            J("8", "Loaded at the pod", "R6", "in_app", "{{stops}} on board, next stop", "One button."),
            J("9", "Running late", "R5", "in_app", "Send the receiver a new ETA", "A button, not a reprimand."),
            J("10", "Delivery complete", "R3", "in_app", "Ksh earned, day total, next job", "The reward moment, repeated several times a day."),
            J("+", "Document expiring", "R4", "sms", "−30, −7 and −1 days, plus an email at −30", "Their ability to work. Three SMS, escalating by specificity."),
            J("+", "Suspended", "R9", "sms", "Reason, and the appeal link", "Never suspend silently."),
            J("+", "Reinstated", "R10", "sms", "You can go online again", "Every hour of delay is money they did not earn."),
            J("+", "Account deleted", "R11", "sms", "Confirmed, and 30 days to undo", "Plus an email covering money and records."),
        ]),

    "host": dict(
        headline="One SMS to open the counter — email does the teaching",
        sub="A host is a business at a counter. SMS is reserved for the two things that stop the counter "
            "working: a failed delivery they must decide about, and a dead pod. The operation itself is "
            "taught by email, once, and stated in the portal every time after.",
        steps=[
            J("1", "Invited", "H6", "email", "The offer, the space, the terms, the fee", "Sell before asking for the click.", flag="open"),
            J("2", "Location goes live", "H1a", "sms", "You are live, portal link", "Short. The email behind it teaches the operation."),
            J("—", "…and the primer", "H1a", "email", "Booking, cut-off, collection, handover codes, failures, settlement", "The only channel that can hold a process."),
            J("—", "…and the setup card", "H1a", "in_app", "Cut-off time, counter contact, settlement number", "Exactly three actions, no more."),
            J("3", "Runner assigned", "H2", "in_app", "{{runner}}, {{stops}} parcels, real ETA", "Once per assignment. Updated only on a material change."),
            J("—", "…first time only", "H2", "email", "How hand-over works", "Explained once, stated thereafter."),
            J("+", "Delivery fails", "H3", "sms", "Reason, where it is held, the choice, the deadline", "A decision on a clock, away from the portal.", flag="open"),
            J("+", "Receiver asks for more time", "H7", "in_app", "Approve or decline", "Build it — the receiver already gets the answer.", flag="open"),
            J("+", "Pod goes offline", "H5", "sms", "Offline since, collections paused, call this number", "They are standing next to it, not sitting at a screen."),
            J("+", "Pod recovers", "H5b", "sms", "Back online, collections resumed", "An alert with no all-clear trains hosts to ignore alerts."),
            J("4", "Weekly settlement", "H4", "email", "Amount in the subject line", "The number they open the week for.", flag="open"),
            J("—", "…and in the portal", "H4", "in_app", "Amount, parcel count, link to the statement", "Same place, same shape, every week."),
        ]),

    "admin": dict(
        headline="Four SMS, all of them about somebody's income",
        sub="Every message in this lane is a human changing a runner's plan. Each one answers the two "
            "questions a runner actually has: did I do something wrong, and can I work now.",
        steps=[
            J("1", "Job reassigned away", "A1a", "sms", "Reassigned, nothing owed, rating unchanged", "Silence here is read as a penalty."),
            J("2", "Job assigned to them", "A1b", "sms", "Parcels, origin, payout, distance", "An assignment is an offer with the decision already made."),
            J("3", "Job floated back", "A2", "sms", "Released — you can take new offers now", "Without that sentence, runners sit and wait."),
            J("4", "Goes offline", "A3", "sms", "No offers until you are back on", "Usually a flat battery. Write as if it is."),
            J("5", "Ops chases a delay", "A4", "in_app", "Send your ETA to the receiver and ops at once", "In-app only. An SMS from 'ops' reads as a warning letter."),
        ]),

    "prospect": dict(
        headline="One message per person, once, ever",
        sub="Nobody in this lane has asked to hear from us. Each sequence is capped at a single message, "
            "carries an opt-out, and counts against the one-promotional-per-week cap across the estate.",
        steps=[
            J("1", "Asks in a group", "P1", "whatsapp", "Answer the question, then the price and the link", "A human, within the hour."),
            J("2", "Messages us", "P2", "whatsapp", "Two questions: pickup area, drop area", "Every extra question halves the replies."),
            J("3", "Checks a price, does not book", "P3", "sms", "The same figures they saw, and the link", "Once, within the hour. Never twice."),
            J("4", "Collected but never sent", "P4", "sms", "You have seen it work — sending starts at…", "The largest warm audience Pinned has."),
            J("5", "Referred by a sender", "P5", "sms", "Their first send, discounted", "Rides on a delivery that already landed."),
        ]),
}

STORAGE_CLOCK = dict(
    headline="Free storage is 24 hours, and the clock is not the wall clock",
    body="A parcel gets <b>24 countable hours</b> of free storage. The clock does not run between "
         "<b>19:00 and 08:00</b>, and it does not run while the pod is closed. A parcel that lands at "
         "15:00 on Monday is therefore free until the middle of Wednesday, not until Tuesday afternoon.",
    rules=[
        ("Never state a duration to a customer",
         "“24 hours of free storage” is true in our database and wrong on their phone. Every message "
         "states <code>{{deadline}}</code> — a day and a time the person can plan around."),
        ("Schedule the ladder on the storage clock",
         "Rungs fire at 12 countable hours left, 4 countable hours left, and at expiry. Because they are "
         "scheduled on the clock rather than on elapsed time, no rung can arrive overnight or while the "
         "pod the parcel is sitting in is shut."),
        ("Charging starts when the clock does, and stops when they collect",
         "The paused hours are free hours. If a customer disputes a charge, the answer has to be a line "
         "they can check themselves — which is why the amount so far appears in rung 3."),
        ("An extension is granted in hours and communicated as a time",
         "Hosts approve “+24 hours”; receivers are told “now runs to Thursday 11:00”. The two numbers "
         "are never the same, and only one of them belongs in an SMS."),
    ])

OPEN_QUESTIONS = [
    dict(q="Is it a parcel or a package?",
         why="All 33 live templates, the team's sender review and every message on this site say "
             "<i>parcel</i>. The brand guide's push mock-up and the approved sign-up SMS say "
             "<i>package</i>. Either is defensible; using both is not, and the cost of choosing late "
             "is a find-and-replace across the template table plus the app strings. "
             "<b>Recommendation: parcel</b>, because it is already in production and in the team's own "
             "copy — and change the brand guide mock-up to match.",
         who="Brand"),
    dict(q="Do we say OTP to customers, or not at all?",
         why="The site's rule says never — OTP is our word. The counter-argument is strong: Kenyans meet "
             "the term daily through M-Pesa and banking, so it may be the clearest word available. What "
             "cannot stand is the approved sign-up SMS calling it a <i>sign-up code</i> on line two and "
             "an <i>OTP</i> on line four. "
             "<b>Recommendation: pick OTP for codes people type to sign in, and keep “collection code” "
             "for the one they read out at a pod</b> — those are different objects and the difference is "
             "worth the two words.",
         who="Product"),
    dict(q="Does a runner scan at a host counter, or is the code the whole hand-over there too?",
         why="On the sender side the code <i>is</i> the hand-over — there is no scan action, and the "
             "sender copy has been corrected. But the host review document asks for the opposite: its "
             "H1b email is to explain “how to verify a runner, scan every parcel, release the handover "
             "code only after scanning”. Either hosts scan and senders do not, or the host copy is "
             "describing a step that does not exist. Until this is settled the host and runner lanes "
             "still say “after the scan”.",
         who="Operations"),
    dict(q="Does sender sign-in move to a device PIN, the way the runner app is doing?",
         why="The runner review retires the per-sign-in code SMS in favour of a PIN after the first "
             "sign-up code. The same argument applies to senders, and it is the single biggest SMS "
             "saving available. The site currently keeps the sender code SMS until this is decided.",
         who="Product"),
    dict(q="If a host does not answer a dwell-extension request before the deadline, what happens?",
         why="Auto-approve, auto-decline or escalate to ops. The receiver-facing approval and denial "
             "messages already exist, so the copy for H7 cannot be finished until the default is set.",
         who="Operations"),
    dict(q="Is automatic redelivery the approved default when a host does not respond to a failed delivery?",
         why="H3 tells the host what happens if they do nothing. If that sentence is wrong, it is worse "
             "than having no sentence.",
         who="Operations"),
    dict(q="Does settlement actually reach a host within one working day?",
         why="H4 puts the amount in the subject line and the timing in the body. A settlement promise we "
             "miss costs more than a vaguer one — change the sentence, not the finance process.",
         who="Finance"),
    dict(q="What are the real pod-host commercial terms?",
         why="H6 is currently inactive and the draft promises 2 m², installation, maintenance and "
             "insurance. It must state the approved fee structure rather than implying unspecified "
             "earnings, and none of it ships until the terms are confirmed.",
         who="Commercial"),
    dict(q="The receiver lane was not in the review pack.",
         why="Senders, runners and hosts came back marked. The receiver changes on this site — splitting "
             "the created notification from the moving parcel, and dropping the 6-hour rung — come from "
             "the brief rather than from the team, and still need the same keep/remove pass.",
         who="The team"),
]


# ═════════════════════════════════════════════════════════════════════════════
# ROUND 3 — the receiver pack, against the live page, 27 October 2026
#
# Two inputs, and they disagree.
#
#   PINNED RECEIVERS COMMS(1).docx — the lane missing from round two.
#   publicchoicepage.netlify.app   — the page every receiver SMS links to,
#                                    and from today the reference for tone.
#
# The page wins on voice, because it is the surface a receiver is holding when
# they read the SMS: if the two do not sound like the same company, the link
# looks like a phishing link. It also wins on one substantive point the pack
# missed entirely, which is the free-collection offer.
# ═════════════════════════════════════════════════════════════════════════════

# The reference page's own sample values. Character counts on this site are
# measured with these, so a count here is a count of the real thing.
SAMPLES.update({
    "name": "Charlotte", "from": "Amina's Shop", "station": "Pinned Kilimani",
    "pod": "Pinned Kilimani", "code": "P7X4K", "otp": "934727",
    "track_url": "pinnedflow.app/p/7K4QX", "dest": "Imani Apartments, Ruiru",
    "runner": "Brian K.", "amount": "2,400", "origin": "Pinned Kilimani",
})

TONE_REFERENCE = dict(
    url="publicchoicepage.netlify.app",
    title="The receiver page is the reference",
    body="Every receiver SMS ends in a link to this page, and the two are read forty seconds apart. If "
         "they do not sound like the same company, the link looks like a phishing link — which in this "
         "market is the end of the conversation. From 27 October the page is the reference for tone, and "
         "receiver copy is harmonised to it rather than written against this site.",
    rules=[
        ("Free first, every time",
         "The page says <i>“I'll collect it myself · Free”</i>, <i>“Collecting it yourself is always "
         "free”</i>, <i>“Rather not pay? Collect it free”</i> and <i>“no charge, no pressure”</i>. The "
         "SMS matches: <b>Collect it free, or have it delivered to your door.</b> Free is named first "
         "and it is named plainly."),
        ("“Good news” when it is news, “Hi” when it has travelled",
         "A parcel created for someone opens <i>Good news {{name}} —</i>. A parcel that has actually "
         "arrived from another town opens <i>Hi {{name}} —</i>. The page uses both and the difference is "
         "real: one is a surprise, the other is a thing they were waiting for."),
        ("Money gets its own sentence, with the method and the payee",
         "<i>“On delivery you'll pay the Ksh 735 trip fee by M-Pesa, and Ksh 2,400 for the goods to "
         "Amina's Shop.”</i> Amount, channel, recipient. Never a total that hides what it is made of."),
        ("The gate is stated, never threatened",
         "<i>“Your handover code appears once it's paid.”</i> Not “you will not receive your parcel "
         "until”. The same fact, told as a mechanism rather than a consequence."),
        ("Contractions, and the limits up front",
         "It's, you'll, we'll, can't. And every cap said before it is hit: <i>“One update per delivery, "
         "up to 3 km”</i>, <i>“One extension only”</i>, <i>“returns to the branch after a 20-min wait — "
         "no charge”</i>."),
        ("The link stands alone",
         "No “click the link below”. The page is the next step and the URL is the whole invitation."),
    ])

PACK_VS_PAGE = [
    dict(t="The pack never mentions free collection",
         p="Every first-contact draft in the pack opens with the paid option — <i>“Save yourself the "
           "trip, we will bring it to you… see the pricing”</i> — and the free alternative does not "
           "appear at all. The live page offers free collection four separate times and goes out of its "
           "way to say there is no pressure. Shipping the pack's wording would quietly turn a generous "
           "product into a pushy one, in the first message a receiver ever gets.",
         v="<b>Page wins.</b> Free first, then the door option."),
    dict(t="A second SMS when the address is known",
         p="The pack proposes a separate first message for the case where the shop already has an "
           "address — <i>“we are bringing it to your doorstep… confirm your location”</i>. The live "
           "page's “Address known · confirm &amp; pay” flow sends the <i>same</i> SMS and handles the "
           "confirmation on the page, which is where the address field already is.",
         v="<b>Page wins, with one exception.</b> The pre-paid individual flow does have its own SMS, "
           "because there is genuinely no choice to make. That is C1a."),
    dict(t="Free storage: 6 hours, 12 hours, or 24 countable hours",
         p="The pack says six hours on pod arrival and twelve on both waiting rungs. This site carries "
           "24 countable hours with the clock paused overnight, which is what was stated on 13 October. "
           "The page does not mention storage at all, so it cannot settle it.",
         v="<b>Unresolved.</b> Nothing has been changed on the strength of a draft. Top of the open "
           "questions."),
    dict(t="“Do not share the code for security purposes”",
         p="The pack's collection-code message carries a line headed DISCLAIMER. The page says "
           "<i>“Give this only to your Pinned runner at the door.”</i> — the same protection, as an "
           "instruction a person can actually follow.",
         v="<b>Page wins.</b>"),
    dict(t="“is on his way”",
         p="The pack's in-transit message assumes the runner is a man. The page never does.",
         v="<b>Page wins.</b> “On the way”, which is also shorter."),
    dict(t="What the pack has that the page does not",
         p="Branch triggers. The pack is the only source that says the in-transit message fires when "
           "<i>the shop owner inputs the runner's handover code</i>, that door arrival fires on the "
           "runner's GPS ping, and that rung 4 should still offer a doorstep delivery on the last day. "
           "All three are adopted.",
         v="<b>Pack wins.</b> Operations knows what fires when; the page knows how it sounds."),
]


SAMPLES.update({"fee": "735", "goods": "2,400"})

RECEIVER_REVIEW = {

    "C1": dict(
        name="A parcel has been created for you",
        stage="First contact",
        trigger="A business sender creates a parcel addressed to this person",
        timing="At creation", channels=["sms"], status="change",
        source="Receiver page · 27 Oct", hook="Trigger",
        intent="First contact, and a choice. Two ways to get it, the free one named first.",
        old="Hi {{name}} Your Parcel from {{from}} is ready. Save yourself the trip, we will bring it to you. Click the link below to pin point your location and see the pricing. {{track_url}}",
        warmth="“Good news” is doing real work here. Somebody thought of them, and the message says so before it says anything operational.",
        review="<b>Taken from the live page, not from the pack.</b> The pack's draft sells the doorstep "
               "delivery and never mentions that collecting is free. The page offers free collection four "
               "times over and adds <i>“no charge, no pressure”</i> — so the SMS leads with free too, or "
               "the link lands on a page that contradicts the text that sent them there.<br><br>"
               "<b>Money, when there is money.</b> It gets its own sentence naming the amount, the "
               "method and who it goes to, and the code gate is stated as a mechanism: "
               "<i>“Your handover code appears once it's paid.”</i>",
        msgs=[("sms", "Good news {{name}} — {{from}} has created a parcel for you, ready at {{station}}.\nCollect it free, or have it delivered to your door:\n{{track_url}}"),
              ("sms", "Good news {{name}} — {{from}} has created a parcel for you and is covering the delivery, ready at {{station}}.\nCollect it free, or have it delivered to your door:\n{{track_url}}\n[sender covers the trip fee]"),
              ("sms", "Good news {{name}} — {{from}} has created a parcel for you, ready at {{station}}.\nCollect it free, or have it delivered to your door:\n{{track_url}}\nOn delivery you'll pay Ksh {{fee}} for the trip by M-Pesa and Ksh {{goods}} for the goods to {{from}}. Your code appears once both are paid.\n[pay on delivery, with goods owed]")],
        rules=["<b>Free is named before the paid option, in every variant.</b> It is the single clearest "
               "signal that Pinned is not trying to extract something from a person who did not choose "
               "to be a customer.",
               "The money line never appears when there is nothing to pay. Four variants exist so that "
               "three of them can stay short.",
               "No code, no deadline, nothing else to act on. The link is the only action.",
               "The link stands on its own line with no “click below”. The page is the invitation."]),

    "C1a": dict(
        name="It's paid, and already heading to you",
        stage="First contact",
        trigger="An individual sender books and pays, with the receiver's address already set",
        timing="At booking", channels=["sms"], status="gap",
        source="Receiver page · 27 Oct", hook="Trigger",
        intent="No choice to offer. Someone has paid, it is coming, and the only thing they might need to fix is the address.",
        warmth="Name the person who sent it. For an individual sender that name is the whole message.",
        review="<b>The one case that earns its own SMS.</b> The pack wanted a second first-contact message "
               "whenever the address is known; the live page sends the same SMS for business senders and "
               "confirms the address on the page. The exception is a pre-paid individual send, where "
               "there is genuinely no choice to present — so the page's own variant drops the offer and "
               "goes straight to tracking, on a <code>/track/</code> link rather than <code>/p/</code>.",
        msgs=[("sms", "Good news {{name}} — {{sender_name}} has sent you a parcel through Pinned.\nIt's at {{station}}, heading to you now.\nTrack it: {{track_url}}")],
        rules=["A different link. <code>/p/</code> is the choice page; <code>/track/</code> is the "
               "tracking page. Sending a pre-paid receiver to a page with a price on it is how you "
               "generate a support call.",
               "The address is still editable on the tracking page — the sender set it, and the person "
               "living there is the one who knows if it is wrong."]),

    "C1c": dict(
        name="Your parcel has arrived from upcountry",
        stage="First contact",
        trigger="A parcel handler receives a parcel addressed to this person",
        timing="On arrival at the handler", channels=["sms"], status="gap",
        source="Receiver page · 27 Oct", hook="Trigger",
        intent="The parcel genuinely travelled. That changes the opener and the verb.",
        warmth="Restrained on purpose. This person was already waiting for this parcel; the news is that it is here, not that it exists.",
        review="<b>“Hi”, not “Good news”.</b> The page uses both openers and the difference is real: a "
               "parcel created for you is a surprise, a parcel that has come from Nakuru is a thing you "
               "have been waiting for. Telling someone it is good news when they already knew it was "
               "coming is the small false note that makes a brand sound automated.",
        msgs=[("sms", "Hi {{name}} — your parcel from {{from}} has arrived at {{station}}.\nCollect it free, or have it delivered to your door:\n{{track_url}}")],
        rules=["The sender is written as name plus town — <i>Amalia (Nakuru)</i> — because for a handler "
               "shipment the town is half the identification.",
               "The station is the handler's own business name and street, not a Pinned name. It is where "
               "the person will actually walk."]),

    "C1b": dict(
        name="A runner has your parcel",
        stage="In transit",
        trigger="The shop enters the runner's handover code",
        timing="At hand-over", channels=["sms"], status="partial",
        source="Receiver pack · 27 Oct", hook="Trigger",
        intent="It is moving, with a name and a time on it.",
        review="<b>Trigger from the pack, voice from the page.</b> The pack names the trigger precisely — "
               "<i>the shop owner inputs the runner's handover code</i> — which is also the second piece "
               "of evidence that a counter hand-over is a code being typed, not a parcel being "
               "scanned.<br><br>"
               "<b>Changed from the draft:</b> <i>“is on his way”</i> becomes <i>“is on the way”</i>. Not "
               "every runner is a man. <i>“Arrives in {{eta}}”</i> becomes an arrival time, because a "
               "text read forty minutes late makes a countdown a lie.",
        msgs=[("sms", "{{runner}} has your parcel from {{from}} and is on the way to {{dest}}, arriving about {{eta}}.\nFollow it live: {{track_url}}")],
        rules=["Never a gendered pronoun for a runner, a host or a receiver.",
               "An arrival time, never a countdown."]),

    "C2": dict(
        channels=["sms", "in_app"], status="live",
        review="<b>Kept, with the page's offer restored.</b> The pack's pod arrival says the storage is "
               "<i>“free for 6 hours after the drop”</i>; this site states a deadline instead, because "
               "the clock pauses overnight and a duration is wrong by morning. The number itself is "
               "contested — see the open questions — and has not been changed on the strength of a draft.",
        msgs=[("sms", "Hi {{name}}, your parcel from {{from}} is at {{station}}, open until {{closing_time}}.\nCollection code: {{otp}}\nFree storage until {{deadline}}. Can't make it? We'll bring it to you: {{track_url}}"),
              ("in_app", ("Ready at {{station}}", "Code {{otp}} · open until {{closing_time}} · free storage until {{deadline}}.\n[ Directions ]  [ Send it to my door ]"))]),

    "C2b": dict(
        name="Your runner is at the door",
        stage="Arrived",
        trigger="The runner's GPS pings at the delivery address",
        timing="On arrival", channels=["sms"], status="gap",
        source="Receiver pack + page · 27 Oct", hook="Action",
        intent="Hand-over in one message. What it says depends entirely on whether the trip is already paid for.",
        warmth="None. Somebody is standing outside; this is the one moment that wants no personality at all.",
        review="<b>Trigger from the pack, both branches from the page.</b> The pack covers the unpaid "
               "case — <i>“settle the delivery account to see the handover code”</i> — which matches the "
               "page's gate exactly. The paid case needs its own line, or a receiver who has already paid "
               "is sent to a payment screen and assumes they are being charged twice.<br><br>"
               "<b>Changed from the draft:</b> <i>“Settle the Delivery account”</i> becomes "
               "<i>“pay the Ksh {{fee}} trip fee”</i>. Nobody outside the company has a delivery account, "
               "and the page always names the amount.",
        msgs=[("sms", "{{runner}} is outside {{dest}} with your parcel.\nYour handover code: {{otp}}\nGive this only to your Pinned runner at the door.\n[trip already paid]"),
              ("sms", "{{runner}} is outside {{dest}} with your parcel.\nPay the Ksh {{fee}} trip fee by M-Pesa and your handover code appears: {{track_url}}\n[pay on delivery]")],
        rules=["Two branches, never one message that covers both.",
               "<i>“Give this only to your Pinned runner at the door”</i> is the page's own line, and it "
               "beats every abstract warning: it tells a person exactly who may hear the code."]),

    "C3": dict(
        channels=["sms"], status="gap", source="Receiver pack · 27 Oct",
        review="<b>Kept, trimmed.</b> <i>“Unfortunately”</i> and <i>“Thank you for your patience”</i> in "
               "four lines is apologising twice. The thanks stays — it is house language the team already "
               "use in the refund SMS — and <i>unfortunately</i> goes, because the new time is the apology.",
        msgs=[("sms", "Your parcel is running late — {{reason}}. New arrival time: {{eta}}.\nThanks for your patience. Follow it here: {{track_url}}")]),

    "C4b": dict(
        channels=["sms"], status="partial",
        review="<b>Changed from the draft.</b> <i>“Failure to collect it before then, will attract a "
               "charge”</i> is a letter from a council. Numbers are facts, never threats — so the rate is "
               "stated next to the deadline and the way out comes straight after it.",
        msgs=[("sms", "Your parcel is still at {{station}}. Free storage ends {{deadline}}, then Ksh {{rate}}/hr.\nCode: {{otp}}\nCan't make it? We'll bring it to you: {{track_url}}")]),

    "C4c": dict(
        channels=["sms"], status="defect",
        review="<b>The pack keeps the best sentence in the ladder</b> — <i>the charges stop the moment you "
               "collect</i> — and adds something this site had missed: at this rung the door-delivery link "
               "has to settle the storage charge too, or it sends somebody to a page that cannot finish "
               "the job.",
        msgs=[("sms", "Free storage has ended on your parcel at {{station}}: Ksh {{rate}}/hr, Ksh {{amount}} so far.\nIt stops the moment you collect.\nCode: {{otp}}\nPay and collect, or we'll bring it to you: {{track_url}}")]),

    "C4d": dict(
        channels=["sms"], status="change",
        intent="Final rung. A fact already in motion, the total, and — new in this pack — a last chance.",
        review="<b>The pack improves on this site.</b> Round two ended the ladder with “contact {{from}} "
               "to rearrange”, which hands the problem to the sender. The pack keeps the doorstep offer "
               "alive to the last message, which is kinder and the only version that can still recover "
               "both the delivery and the storage fee on the day.",
        warmth="A last door, held open on the day it closes.",
        msgs=[("sms", "Hi {{name}}, your parcel goes back to {{from}} today at {{time}}, after 7 days at {{station}}.\nStorage owed: Ksh {{amount}}.\nStill want it? We can bring it to you today: {{track_url}}")],
        rules=["Four rungs, then silence — and the fourth still offers a way to keep the parcel.",
               "The total is stated once, because there is no later message."]),

    "C5": dict(
        channels=["sms"], status="live",
        review="<b>Changed from the draft.</b> <i>“DISCLAIMER; Do not share the code for security "
               "purposes”</i> becomes the page's own line. A customer cannot act on “for security "
               "purposes”; they can act on being told exactly who is allowed to hear it. "
               "<i>“Dear {{name}}”</i> goes too — it is the register of a bank letter.",
        msgs=[("sms", "{{name}}, your collection code is {{otp}}.\nShow it at {{station}} to collect. Give it only to Pinned staff at the counter — we never call or text to ask for it.")]),

    "C7": dict(
        name="Delivered — and how was your runner?",
        channels=["sms"], status="gap", source="Receiver pack + page · 27 Oct",
        review="<b>Both sources agree, and the page adds the rating.</b> The pack asks for the saved "
               "address; the page ends on <i>“Your runner just wrapped up — were they 5-star?”</i>. One "
               "message carries both, because they are the same moment and a second SMS would not be sent.",
        msgs=[("sms", "Delivered — it's all yours, {{name}}. Thanks for choosing Pinned.\nHow was {{runner}}? Rate them, and save your address so the next one comes straight to your door: {{track_url}}")]),
}


SAMPLES.update({"spot": "Kitengela Mall", "ext_fee": "150", "ext_km": "2.1",
                "sender_name": "David"})

# Scaffolds for the touchpoints RECEIVER_REVIEW fills, plus two the live page
# carries that neither this site nor the pack had.
TOUCHPOINTS += [
    T(id="C1a", lane="receiver", stage="First contact", name="(filled by review)",
      trigger="—", timing="—", channels=["sms"], status="gap", intent="—"),
    T(id="C1c", lane="receiver", stage="First contact", name="(filled by review)",
      trigger="—", timing="—", channels=["sms"], status="gap", intent="—"),
    T(id="C2b", lane="receiver", stage="Arrived", name="(filled by review)",
      trigger="—", timing="—", channels=["sms"], status="gap", intent="—"),

    T(id="C8", lane="receiver", stage="Arrived", name="Your runner can't find you",
      trigger="The runner is at the address and cannot reach the receiver",
      timing="On the runner reporting it", channels=["sms"],
      status="gap", source="Receiver page · 27 Oct", hook="Action",
      intent="Somebody is standing in the wrong place. Fix it in one tap, without blaming anyone.",
      warmth="“Moved on?” is the whole trick. It assumes the ordinary explanation instead of asking why they are not where they said.",
      review="<b>Only the live page has this.</b> Neither the Communication Map nor the receiver pack "
             "includes it, and it is the moment a delivery is most likely to fail. The page's wording is "
             "used almost as written, because it is already the voice.",
      msgs=[("sms", "{{runner}} is at {{spot}} and can't find you at {{dest}}.\nMoved on? Tell us where you are now: {{track_url}}")],
      rules=["The page states the limit before anyone hits it: <i>one update per delivery, up to 3 km "
             "from your first address</i>. That sentence belongs on the page, not in the SMS — the SMS "
             "has one job, which is to get them to the page.",
             "The fallback is generous and it is said out loud on the page: <i>if we can't reach you at "
             "your door, it returns to the branch after a 20-min wait — no charge</i>. A failed delivery "
             "that costs the receiver nothing is the reason this message can stay calm.",
             "Never “you were not available”. The runner is the one who cannot find them, and that is "
             "how the sentence is built."]),

    T(id="C9", lane="receiver", stage="Arrived", name="Moving the drop — priced",
      trigger="The receiver gives a new location within the cap",
      timing="Immediately after C8", channels=["sms"],
      status="gap", source="Receiver page · 27 Oct", hook="Action",
      intent="A priced change of plan. Every number shown, including where the money goes.",
      warmth="Telling them the runner keeps the whole fee. It costs nothing to say and it changes what the charge feels like.",
      review="<b>Not the same thing as a storage extension.</b> C6a and C6b extend free storage at a pod; "
             "this extends a <i>delivery</i> to a new address and it is priced. Two different objects "
             "that were both being called an extension.",
      msgs=[("sms", "Moving your delivery to {{spot}} is {{ext_km}} km further — Ksh {{ext_fee}} by M-Pesa.\nPay and your handover code unlocks: {{track_url}}\n{{runner}} keeps the full fee.")],
      rules=["The fee is broken down on the page — base plus distance — never presented as one unexplained number.",
             "<i>“Your handover code stays locked until this clears.”</i> The gate is a mechanism, stated plainly, exactly as on the page.",
             "One extension, up to 3 km, said before it is needed."]),
]
for _t in TOUCHPOINTS:
    _t.setdefault("review", None)
    _t.setdefault("warmth", None)

_by_id = {t["id"]: t for t in TOUCHPOINTS}
for _id, _patch in RECEIVER_REVIEW.items():
    _tp = _by_id.get(_id)
    if _tp is None:
        raise KeyError("receiver review targets an unknown touchpoint: %s" % _id)
    _tp.update(_patch)

for _new, _after in (("C1a", "C1"), ("C1c", "C1a"), ("C2b", "C2"), ("C8", "C2b"), ("C9", "C8")):
    ORDER.insert(ORDER.index(_after) + 1, _new)
TOUCHPOINTS.sort(key=lambda t: ORDER.index(t["id"]))

JOURNEYS["receiver"] = dict(
    headline="Four SMS on a journey that works — and the receiver has no app",
    sub="Every receiver rule is the inverse of the sender rules. There is no in-app to fall back on, so "
        "SMS carries everything, and each message hands over to publicchoicepage.netlify.app — which is "
        "why the two have to sound like one company. First contact branches on who sent it and whether "
        "anything is owed; arrival branches between a door and a pod.",
    steps=[
        J("1", "Business sender creates it", "C1", "sms", "Collect it free, or have it delivered", "First contact. Free is named first, every time."),
        J("1b", "…an individual pre-paid it", "C1a", "sms", "It's paid and heading to you — track it", "No choice to offer, so none is presented.", off=True),
        J("1c", "…or it came from a handler", "C1c", "sms", "Hi — your parcel has arrived at {{station}}", "“Hi”, not “Good news”. They were already waiting.", off=True),
        J("2", "Shop enters the runner's code", "C1b", "sms", "{{runner}} has it, arriving about {{eta}}", "A counter hand-over is a code typed, not a parcel scanned."),
        J("3", "Runner reaches the door", "C2b", "sms", "Handover code — or pay the trip fee to unlock it", "Branches on whether the trip is already paid."),
        J("3b", "…or it arrives at a pod", "C2", "sms", "Station, hours, code, deadline, door-delivery offer", "Two segments. Each line saves a phone call.", off=True),
        J("4", "Collects", "C7", "sms", "It's all yours — rate your runner, save your address", "The page ends on the rating; so does the SMS."),
        J("+", "Runner can't find them", "C8", "sms", "Moved on? Tell us where you are now", "The moment a delivery is most likely to fail."),
        J("+", "They give a new spot", "C9", "sms", "Ksh {{ext_fee}} to move it — the runner keeps it all", "Priced, capped, and the code stays locked until it clears."),
        J("+", "Running late", "C3", "sms", "New arrival time, reason, tracking", "A broken promise gets its own message."),
        J("+", "Half the clock gone", "C4a", "sms", "Still here, code, opening hours, deadline", "Rung 1. No charges apply, so none are mentioned."),
        J("+", "Clock nearly out", "C4b", "sms", "Free storage ends {{deadline}}, then the rate", "Rung 2. Where most door-delivery conversions happen."),
        J("+", "Clock runs out", "C4c", "sms", "Storage started, and how to stop it", "Rung 3. The link has to settle the charge, not just book a delivery."),
        J("+", "Day 7", "C4d", "sms", "Goes back today — or we bring it to you today", "Rung 4. The pack keeps the door open to the last message."),
        J("+", "Asks for more storage time", "C6a", "sms", "Approved — new deadline", "Not the same thing as C9. One is time, the other is distance."),
    ])

OPEN_QUESTIONS = [
    dict(q="How long is free storage — 6 hours, 12 hours, or 24 countable hours?",
         why="Three numbers in one document. The receiver pack says <i>“free for 6 hours after the "
             "drop”</i> on pod arrival and <i>“{{12hrs after drop off}}”</i> on both waiting rungs; this "
             "site carries 24 countable hours with the clock paused 19:00–08:00 and whenever the pod is "
             "shut, which is what was stated on 13 October. The live page does not mention storage, so "
             "it cannot settle it. Nothing here has been changed on the strength of a draft, because the "
             "whole ladder, the charging trigger and the sender-side return all hang off this number. "
             "<b>One answer, and it is a ten-minute change on this site.</b>",
         who="Operations"),
    dict(q="Can the notification layer supply a sender's name?",
         why="The live page's pre-paid variant reads <i>“David has sent you a parcel”</i>. "
             "<code>{{sender_name}}</code> has been added to the token set here so C1a reads correctly, "
             "but <code>NotificationTemplate::TOKENS</code> in pinned-core has no such token and nothing "
             "currently resolves it. For an individual send it is the most important word in the message "
             "— without it the SMS cannot say who the parcel is from.",
         who="Engineering"),
] + OPEN_QUESTIONS


# ═══════════════════════════════════════════════════════════════════════════
# ROUND FOUR · 27 October — the dispatch cases, and the SMS count that follows
#
# "How many SMS does a receiver get, and which one" has never been written in
# one place, so every review re-argues it. Two rules settle it for every
# combination of sender type, pickup mode, money and address; everything below
# is those two rules applied.
# ═══════════════════════════════════════════════════════════════════════════

BUILD = 14
UPDATED = "27 October 2026 · the dispatch cases, on a left-hand menu"

DISPATCH_INTRO = (
    "An individual, a business sender and a parcel handler all create the same object and all "
    "produce a different first SMS. The difference is never the number of messages — it is the "
    "<b>origin</b> and the <b>status</b> the first sentence carries, and whether money is attached. "
    "Four axes, nine cases, and the same two messages in every one of them.")

DISPATCH_RULES = [
    dict(n="01", t="One SMS when the parcel is created",
         p="Whoever created it, exactly one SMS goes out at creation. What varies is where the parcel "
           "is, what is happening to it, and whether a money line is attached. Nothing varies the count."),
    dict(n="02", t="A second SMS only when a code is coming — and it carries only the code",
         p="The first message promises a code, so the second one delivers it, on the event that "
           "unlocks it: the payment clearing, or the parcel reaching the counter they chose. The live "
           "page already commits us to this in its own words — <i>“Your handover code is also sent by "
           "SMS.”</i> A receiver who owes nothing still gets a code, so a receiver who owes nothing "
           "still gets two messages."),
    dict(n="03", t="The address changes the page, never the message",
         p="An unknown address is collected on the choice page, under the same link, in the same "
           "session. It does not earn an SMS of its own. A second first-contact message is the "
           "fastest way to make a stranger decide they are being marketed at."),
    dict(n="04", t="The sender is told what to do once — drop, or hand over",
         p="A booking that will be dropped gets the drop SMS and never a handover code. A booking a "
           "runner will collect gets the handover code and never a drop reminder. Today both can fire "
           "against the same booking, because nothing in the code treats them as alternatives."),
]

# Rows render as: case · what the first SMS carries · 1st SMS · 2nd SMS · sender SMS
DISPATCH = [
    dict(key="individual", title="Individual sender", colour="accent-mag",
         who="One person sending to another, in the app.",
         axis="The trip is paid before it starts, so there is never money owed at the far end and "
              "never a choice to present. The only variable is how the parcel leaves the sender — "
              "which is exactly what the first sentence has to say.",
         rows=[
             dict(case="Creates a drop",
                  var="Sender carries it to a pod",
                  first="Names the sender, the pod it is waiting at, and that it is already paid.",
                  c1=[("C1a", "drop variant")], c2=[("C2c", "handover code")],
                  s=[("S2", "drop instruction + pod code")]),
             dict(case="Creates a trip",
                  var="A runner collects from the sender",
                  first="Names the sender, where it is being collected from, and that a runner is on it.",
                  c1=[("C1a", "runner variant")], c2=[("C2c", "handover code")],
                  s=[("S2c", "handover code")]),
         ]),

    dict(key="business", title="Business sender", colour="accent-lock",
         who="A shop or a business sending through a virtual host.",
         axis="Three axes at once — how it leaves the shop, who pays what, and whether we know where "
              "the receiver lives. Only the money axis changes the copy. Pickup mode changes one "
              "clause. The address changes nothing at all.",
         rows=[
             dict(case="Pay now", var="Trip fee settled on the page",
                  first="Free collection first, the door option second. The fee is shown on the page, not in the SMS.",
                  c1=[("C1", "variant 1")], c2=[("C2c", "on payment")], s=[("S2", "if dropped"), ("S2c", "if a runner collects")]),
             dict(case="Pay now + goods", var="Trip fee and the goods settled on the page",
                  first="Same opening. The goods line names the amount, the method and that it goes to the shop.",
                  c1=[("C1", "variant 3")], c2=[("C2c", "on payment")], s=[("S2", "if dropped"), ("S2c", "if a runner collects")]),
             dict(case="Pay on delivery", var="Trip fee owed at the door",
                  first="Same opening, plus the money sentence and the gate — your code appears once it is paid.",
                  c1=[("C1", "variant 3")], c2=[("C2c", "on payment at the door")], s=[("S2", "if dropped"), ("S2c", "if a runner collects")]),
             dict(case="Pay on delivery + goods", var="Trip fee and goods owed at the door",
                  first="Both amounts, both payees, one sentence each. The longest message in the estate at two segments.",
                  c1=[("C1", "variant 3")], c2=[("C2c", "on payment at the door")], s=[("S2", "if dropped"), ("S2c", "if a runner collects")]),
             dict(case="Covered by sender", var="The shop pays the trip",
                  first="“…and is covering the delivery.” No money line, because there is no money.",
                  c1=[("C1", "variant 2")], c2=[("C2c", "on runner assignment")], s=[("S2", "if dropped"), ("S2c", "if a runner collects")]),
             dict(case="Address known", var="The shop already has the address",
                  first="Unchanged. The page confirms the address instead of asking for it.",
                  c1=[("C1", "same variant")], c2=[("C2c", "")], s=[("S2", "if dropped"), ("S2c", "if a runner collects")]),
         ]),

    dict(key="handler", title="Parcel handler", colour="accent-org",
         who="A sacco, a bus parcel office or a shop receiving on someone's behalf.",
         axis="One case, and the narrowest of the three: always pay-now, never goods owed, and never "
              "a Pinned pod anywhere in the chain. The parcel has genuinely travelled, which is why "
              "the opener and the register both change.",
         rows=[
             dict(case="Arrives at the handler",
                  var="Always pay-now · no goods · no pod",
                  first="“Hi”, not “Good news”. Names the end client, the town it came from, and the handler's own premises.",
                  c1=[("C1c", "handler variant")], c2=[("C2c", "on payment")],
                  s=[("—", "the handler is not a Pinned sender")]),
         ]),
]

DISPATCH_SENDER = [
    dict(case="The sender will drop it at a pod",
         sms="S2", what="The reservation code to enter at the pod, and the hold deadline.",
         never="S2c", why="There is no runner at the counter, so there is nobody to hand a code to."),
    dict(case="A runner will collect it",
         sms="S2c", what="The handover code to give the runner, and the one safety line.",
         never="S2", why="There is no drop to remind them about, and a drop reminder against a "
                         "runner booking is the single most confusing message we send."),
]

DISPATCH_NOTE = (
    "<b>The one thing this changes.</b> On a pay-on-delivery journey the plan was three messages — "
    "created, runner is outside, here is your code. The runner is standing at the door with a phone "
    "in their hand and the page is open in front of the receiver, so the middle one is retired. "
    "<b>C2b</b> is the only touchpoint on this site that is retired before it is ever built.")


SAMPLES.update({"client": "Charlotte", "town": "Nakuru", "handler": "4NTE Sacco, Cross Road"})

TOUCHPOINTS += [
    T(id="C2c", lane="receiver", stage="The code", name="Your handover code",
      trigger="The money clears, or a runner is assigned on a journey with nothing owed",
      timing="The second and last SMS of a journey that works", channels=["sms"],
      status="gap", source="Receiver page · 27 Oct", hook="Action",
      intent="The promise the first SMS made, kept. One code, one safety line, nothing else.",
      warmth="“That's paid — thank you.” Three words that tell somebody the money landed, which is "
             "the thing they are actually anxious about.",
      review="<b>The page commits us to this message.</b> Its payment screen ends on <i>“Your handover "
             "code is also sent by SMS”</i>, so the SMS is not a choice — it is a promise already made "
             "to every receiver who reaches that screen. It is also the message the first SMS pointed "
             "at when it said <i>your code appears once it's paid</i>.",
      msgs=[("sms", "{{name}}, that's paid — thank you. Your handover code is {{otp}}.\nGive it only to your Pinned runner at the door. We never call or text to ask for it."),
            ("sms", "{{name}}, {{runner}} is bringing your parcel. Your handover code is {{otp}}.\nGive it only to your Pinned runner at the door. We never call or text to ask for it.\n[nothing owed — the sender covered it]")],
      rules=["Nothing else ships in a code message. No tracking link, no thanks for choosing Pinned, "
             "no marketing. It is the one message that has to survive being read on a cracked screen "
             "in the rain.",
             "<i>“Give this only to your Pinned runner at the door”</i> is the page's own line. It beats "
             "every abstract warning because it names exactly who may hear the code.",
             "On a free-collection journey this message is <b>C2</b> instead — same job, same position, "
             "a counter rather than a door. Either way the receiver gets exactly one code message."]),
]
for _t in TOUCHPOINTS:
    _t.setdefault("review", None)
    _t.setdefault("warmth", None)

_by_id = {t["id"]: t for t in TOUCHPOINTS}

# C2b is retired into C2c — see DISPATCH_NOTE.
_by_id["C2b"].update(dict(
    status="retire", channels=["sms"],
    name="Your runner is at the door — retired",
    intent="Written, measured, and then cut. The moment is real; the SMS is not needed to carry it.",
    review="<b>Retired before it was built.</b> Both branches of this message were drafted on 27 October "
           "and both are now cut. The paid branch repeated a code the receiver already had; the "
           "pay-on-delivery branch asked for money from somebody standing in front of a runner who "
           "could point at the page. Keeping it would have made pay-on-delivery the only journey in "
           "the estate that costs three SMS, for the one moment where a human being is physically "
           "present to help.<br><br>"
           "<b>What carries it instead:</b> live tracking on the page, which the receiver already has "
           "open, and the runner's own phone.",
    rules=["The test that retired it: if a person is standing at the door, an SMS is the slowest way "
           "to tell them anything.",
           "The copy stays on this page on purpose. A message that was considered and rejected is "
           "cheaper to look up than to re-argue."]))

ORDER.insert(ORDER.index("C2b") + 1, "C2c")
TOUCHPOINTS.sort(key=lambda t: ORDER.index(t["id"]))

# ── the journeys, grouped ───────────────────────────────────────────────────
# grp opens a titled block in the summary, so the reader can find the moment
# they came for instead of reading thirteen rows.

JOURNEYS["receiver"] = dict(
    headline="Three SMS the first time, two every time after",
    sub="Getting the parcel is the same two messages in every case — one when it is created, one "
        "carrying the code — and the rating ask fires once per receiver, ever. The sender type, the "
        "pickup mode and the money all change what the first message <b>says</b>; none of them "
        "change how many there are. Everything below the code is an exception.",
    steps=[
        J("1", "Business sender creates it", "C1", "sms", "Collect it free, or have it delivered", "First contact. Free is named first, every time.", grp="First contact · one message, three shapes"),
        J("1b", "…an individual pre-paid it", "C1a", "sms", "{{sender_name}} has sent you a parcel — track it", "No choice to offer, so none is presented.", off=True),
        J("1c", "…or a handler received it", "C1c", "sms", "Hi — your parcel from {{town}} has arrived", "“Hi”, not “Good news”. They were already waiting.", off=True),
        J("2", "The money clears", "C2c", "sms", "That's paid — your handover code is {{otp}}", "The second message, and the last one on a journey that works.", grp="The code · the second and last message"),
        J("2b", "…or they chose to collect", "C2", "sms", "Station, hours, code, deadline", "Same position, same job, a counter instead of a door.", off=True),
        J("—", "Runner reaches the door", "C2b", "retire", "Nothing — the page is tracking live and the runner is there", "Retired. An SMS is the slowest way to talk to someone standing in front of a runner.", flag="retire"),
        J("—", "Shop enters the runner's code", "C1b", "in_app", "Tracking goes live on the page", "A status change the page shows, not a message. The pack's trigger, kept; its SMS, dropped."),
        J("+", "Runner can't find them", "C8", "sms", "Moved on? Tell us where you are now", "The moment a delivery is most likely to fail.", grp="Exceptions · only when something goes wrong"),
        J("+", "They give a new spot", "C9", "sms", "Ksh {{ext_fee}} to move it — the runner keeps it all", "Priced, capped, and the code stays locked until it clears."),
        J("+", "Running late", "C3", "sms", "New arrival time, reason, tracking", "A broken promise gets its own message."),
        J("+", "Half the clock gone", "C4a", "sms", "Still here, code, opening hours, deadline", "Rung 1. No charges apply, so none are mentioned.", grp="Nobody collected · four rungs, then silence"),
        J("+", "Clock nearly out", "C4b", "sms", "Free storage ends {{deadline}}, then the rate", "Rung 2. Where most door-delivery conversions happen."),
        J("+", "Clock runs out", "C4c", "sms", "Storage started, and how to stop it", "Rung 3. The link has to settle the charge, not just book a delivery."),
        J("+", "Day 7", "C4d", "sms", "Goes back today — or we bring it to you today", "Rung 4. The pack keeps the door open to the last message."),
        J("+", "Asks for more storage time", "C6a", "sms", "Approved — new deadline", "Time, not distance. C9 is the other one."),
        J("4", "Collects", "C7", "sms", "It's all yours — rate your runner, save your address", "Once per receiver, ever. The only ask in the lane.", grp="Afterwards · once per receiver, ever"),
    ])

JOURNEYS["sender"] = dict(
    headline="Four SMS on a journey that works — three once sign-in moves to a PIN",
    sub="Two codes to get into the account, one instruction about the parcel, and the proof at the "
        "end. The instruction is the one that keeps going wrong: a booking gets <b>either</b> the "
        "drop SMS <b>or</b> the handover code, never both, and which one depends entirely on whether "
        "a runner is coming.",
    steps=[
        J("1", "Creates an account", "S0", "sms", "Sign-up code, with the expiry and the fraud line", "The only way to prove the phone is theirs.", grp="Access · two codes, and one of them should go"),
        J("2", "Signs in", "S0b", "sms", "Sign-in code naming the device", "Security, not convenience. Moves to a device PIN if we follow the runner decision.", flag="open"),
        J("3", "Account opens", "S1", "in_app", "Welcome and the nearest pod", "Nothing time-critical. The code SMS landed a minute ago."),
        J("4a", "Books a drop", "S2", "sms", "Reservation code to enter at the pod, and the deadline", "The instruction. One of two, never both.", grp="The one instruction · drop, or hand over"),
        J("4b", "…or books a runner collection", "S2c", "sms", "Handover code to give the runner, and the safety line", "The other one. The same booking must never receive both.", off=True),
        J("—", "Either way", "S2", "in_app", "Booked — directions, or switch to a runner in one tap", "They are in the app, looking at the booking they just made."),
        J("+", "Has not dropped it", "S2b", "sms", "Save yourself the trip — a runner can collect", "They are away from the app. This is what SMS is for."),
        J("5", "Runner collects", "S2d", "in_app", "Picked up by {{runner}}, ETA", "A status update, not an instruction. One card replaces the two SMS firing today.", grp="On the road"),
        J("6", "Delivered", "S3", "sms", "Who collected it, where, at what time", "The payoff. Two segments, and worth every one."),
        J("+", "Receiver has not collected", "S4a", "sms", "Storage started, charged to you", "Money moving against them. Always SMS.", grp="Exceptions · only when something goes wrong"),
        J("+", "Day 7", "S4b", "sms", "Coming back to you today", "A thing they have to plan around."),
        J("+", "Refund", "S5", "sms", "Amount, and when it reaches M-Pesa", "Money moving toward them. Always SMS."),
        J("+", "Delivery failed", "S6", "sms", "Reason, location, choice, deadline", "A decision only they can make, on a clock."),
    ])

# ── copy the dispatch cases needed that round three did not have ────────────

_by_id["C1a"]["msgs"] = [
    ("sms", "Good news {{name}} — {{sender_name}} has sent you a parcel.\nIt's paid and waiting at {{station}}, heading to you now.\nTrack it: {{track_url}}\n[sender dropped it at a pod]"),
    ("sms", "Good news {{name}} — {{sender_name}} has sent you a parcel.\nIt's paid, and {{runner}} is collecting it from {{origin}} now.\nTrack it: {{track_url}}\n[a runner is collecting from the sender]"),
]
_by_id["C1a"]["intent"] = ("No choice to offer. Someone has paid, it is coming, and the only variable "
                           "is whether it left through a pod or through a runner.")
_by_id["C1a"]["review"] += (
    "<br><br><b>Round four · two variants, not one.</b> An individual either drops the parcel or has "
    "a runner collect it, and the first sentence has to say which — a receiver told it is “waiting at "
    "Shell Kileleshwa” when a runner has not even reached the sender yet will go to the pod.")

_by_id["C1c"]["review"] += (
    "<br><br><b>Round four · checked against the live handler flow.</b> The flow was read again on "
    "27 October to settle whether a handler parcel offers collection at all. It does: the page's own "
    "handler SMS reads <i>“Hi Charlotte — your parcel from Amalia (Nakuru) has arrived at 4NTE Sacco, "
    "Cross Road. Collect it free, or have it delivered to your door”</i>, and its choice screen carries "
    "<i>“I'll collect it myself · Free”</i>. What is absent is the <b>Pinned pod</b> — free collection "
    "means walking into the handler's own counter — and the fee section, because a handler trip is "
    "always pay-now with no goods owed. See the open question.")

_by_id["C1b"].update(dict(
    channels=["in_app"], status="change",
    name="The shop hands it to the runner",
    intent="A status change, shown where the receiver is already looking.",
    review=_by_id["C1b"]["review"] + (
        "<br><br><b>Round four · off SMS.</b> The trigger is right and the sentence is good, but it "
        "would be a third message on a journey that is meant to cost two. The receiver has the choice "
        "page open and that page tracks live — so the hand-over lights up the tracker instead. The "
        "copy below is kept as the in-app line."),
    msgs=[("in_app", ("{{runner}} has your parcel", "From {{from}}, on the way to {{dest}} · arriving about {{eta}}."))],
    rules=["Never a gendered pronoun for a runner, a host or a receiver.",
           "An arrival time, never a countdown."]))

for _id in ("S2", "S2c"):
    _by_id[_id]["rules"] = _by_id[_id]["rules"] + [
        "<b>One instruction per booking.</b> A drop booking gets S2 and never S2c; a runner collection "
        "gets S2c and never S2. Nothing in <code>pinned-core</code> treats them as alternatives today, "
        "so both can fire against the same parcel."]

OPEN_QUESTIONS = [
    dict(q="Does a parcel-handler SMS offer free collection, or go straight to delivery?",
         why="The note from 27 October says a handler trip has <i>no pod option and goes straight into "
             "saving the trip</i>. The live handler flow does the opposite: its SMS reads <i>“Collect it "
             "free, or have it delivered to your door”</i> and its choice screen carries <i>“I'll collect "
             "it myself · Free”</i>. The two reconcile if <i>no pod option</i> means no <b>Pinned pod</b> "
             "is in the chain — free collection is from the handler's own counter — which is what this "
             "site now says. <b>If the intent was that handler parcels are delivery-only, C1c and the "
             "handler flow both change</b>, and the page changes first, because it is the one customers "
             "are already reading.",
         who="Product"),
] + OPEN_QUESTIONS


NAV_GROUPS = [
    ("Foundations", [("index.html", "The map"), ("principles.html", "Voice"),
                     ("channels.html", "Channels & rules")]),
    ("Lanes", [("senders.html", "Senders"), ("receivers.html", "Receivers"),
               ("runners.html", "Runners"), ("hosts.html", "Hosts"),
               ("admin.html", "Admin"), ("prospects.html", "Prospects")]),
    ("Reference", [("library.html", "Copy library"), ("gaps.html", "Build order")]),
]


# ═══════════════════════════════════════════════════════════════════════════
# ROUND FIVE · 1 November — the entry, and the gate
#
# Resynced against the receiver surface as it now stands on the dev branch
# (receiver-flows-prototype, head 59a4c68b + the origin-language worktree):
# the 16-journey harness at ~/pinned-core-receiver, ParcelOrigin,
# DeliveryModesHelper#handover_code_held?, Receiver::DeliveryAddressUpdate and
# Receiver::Extensions.
#
# What moved: first contact no longer branches only on WHO sent the parcel. It
# branches on WHAT THE RECEIVER HAS TO DO when they open the link — confirm an
# address, choose how to get it, or just track it. The verb of the first
# sentence is the entry state. Round four's nine cases are re-cut on that axis.
# ═══════════════════════════════════════════════════════════════════════════

BUILD = 15
UPDATED = "1 November 2026 · the entry state, and the two gate rails"

SAMPLES.update({"addr": "Brookside Grove, Westlands", "branch": "Pinned Westlands",
                "seller": "Amina Stores"})

DISPATCH_INTRO = (
    "The first SMS is not an announcement, it is an instruction — and the instruction depends on "
    "what the person has to do when the link opens. The dev page derives that from one field: "
    "<code>receiver_data.sender_address</code>. If the sender supplied an address, the receiver "
    "<b>confirms</b> it and there is no choice and no distance screen. If not, they <b>choose</b>, "
    "and for pay-on-delivery and covered trips the trip is booked the moment they type an address. "
    "An individual's receiver never reaches that page at all — they get the tracker, and the ask is "
    "<b>track it and confirm your address</b>. Three verbs, eleven cases, and in every one of them "
    "the same two messages.")

DISPATCH_RULES = [
    dict(n="01", t="The verb of the first sentence is the entry state",
         p="<b>Confirm</b> when the sender gave us an address. <b>Choose</b> when they did not. "
           "<b>Track and confirm</b> for an individual send, which lands on "
           "<code>/track/&lt;token&gt;</code> and never on the choice page. Getting this wrong is "
           "not a tone problem: a receiver told to “collect it free, or have it delivered” opens a "
           "page with neither option on it."),
    dict(n="02", t="Money is a trailing clause, never the lead",
         p="On a confirm journey the primary action is identical across all three fee modes, so the "
           "fee goes last and pay-now reads like the covered case rather than like a bill. The page "
           "already does this; the SMS has to match it or the two read as different companies."),
    dict(n="03", t="One SMS when the parcel is created",
         p="Whoever created it, exactly one SMS goes out at creation. The entry state and the money "
           "change what it says. Nothing changes the count."),
    dict(n="04", t="A second SMS only when a code is coming — and it carries only the code",
         p="The first message promises a code, so the second one delivers it, on whichever event "
           "releases it. The live page commits us to this in its own words — <i>“Your handover code "
           "is also sent by SMS.”</i> There are three release events, not one; see the gate below."),
    dict(n="05", t="A create-time message is in the future tense",
         p="At creation nothing has moved: no drop, no pickup, no runner assigned. "
           "<code>ParcelOrigin.individual_create_line</code> exists because this site previously "
           "told a receiver their parcel was <i>“waiting at {{station}}”</i> in the message that "
           "fires before the sender has left the house."),
    dict(n="06", t="The sender is told what to do once — drop, or hand over",
         p="A booking that will be dropped gets the drop SMS and never a handover code. A booking a "
           "runner will collect gets the handover code and never a drop reminder."),
]

DISPATCH = [
    dict(key="individual", title="Individual sender → the tracker", colour="accent-mag",
         who="One person sending to another, settled and paid in the sender wizard.",
         axis="They never reach the choice page. <code>Receiver::DropNotifier</code> sends them to "
              "<code>/track/&lt;token&gt;</code>, which opens on an address confirm and then runs "
              "live tracking. The address is already set, so the only variable is how the parcel "
              "gets out of the sender's hands — and the first sentence has to say which, in the "
              "future tense.",
         rows=[
             dict(case="Drops it at a Pod", act="Track &amp; confirm",
                  var="Future tense · /track link",
                  first="“It'll be dropped at {{station}}, then brought to your door.”",
                  c1=[("C1a", "pod-drop variant")], c2=[("C2c", "handover code")],
                  s=[("S2", "drop instruction + pod code")]),
             dict(case="A runner collects it", act="Track &amp; confirm",
                  var="Future tense · /track link",
                  first="“A runner will pick it up and bring it to your door.”",
                  c1=[("C1a", "runner variant")], c2=[("C2c", "handover code")],
                  s=[("S2c", "handover code")]),
         ]),

    dict(key="biz-known", title="Business sender · address known", colour="accent-lock",
         who="The shop supplied the address, so <code>receiver_data.sender_address</code> is set.",
         axis="The page opens straight on <i>Confirm your delivery address</i> — no choice screen, "
              "no “see how far it is from you”, because the trip is already settled or floated. "
              "The receiver may nudge the pin up to <b>500 m</b> without the price changing; "
              "further than that is refused and they are sent back to the sender.",
         rows=[
             dict(case="Pay now", act="Confirm", var="Trip fee settled on the page",
                  first="Confirm the address, then a trailing line: a trip fee to settle before dispatch.",
                  c1=[("C1d", "confirm · pay now")], c2=[("C2c", "on payment")],
                  s=[("S2", "if dropped"), ("S2c", "if a runner collects")]),
             dict(case="Pay on delivery", act="Confirm", var="Trip fee owed at the door",
                  first="Confirm the address, then the fee, the method, and the gate.",
                  c1=[("C1d", "confirm · on delivery")], c2=[("C2c", "on payment")],
                  s=[("S2", "if dropped"), ("S2c", "if a runner collects")]),
             dict(case="Covered by sender", act="Confirm", var="The shop pays the trip",
                  first="“…is covering the delivery — just confirm your address is correct.” No money line.",
                  c1=[("C1d", "confirm · covered")], c2=[("C2c", "on runner assignment")],
                  s=[("S2", "if dropped"), ("S2c", "if a runner collects")]),
         ]),

    dict(key="biz-unknown", title="Business sender · address unknown", colour="accent-flow",
         who="No address on the parcel, so the receiver has a real choice to make.",
         axis="The choice page, with the distance screen. Free collection is named first, every "
              "time. For pay-on-delivery and covered trips <b>the trip is booked the moment the "
              "address is entered</b> — which is also when the receiver first sees the amount.",
         rows=[
             dict(case="Pay now", act="Choose", var="Quote at address",
                  first="Free collection first, the door option second. The fee is on the page, not in the SMS.",
                  c1=[("C1", "variant 1")], c2=[("C2c", "on payment")],
                  s=[("S2", "if dropped"), ("S2c", "if a runner collects")]),
             dict(case="Pay now + goods", act="Choose", var="Quote at address · goods owed",
                  first="Same opening. The goods line names the amount, the method and that it goes to the shop.",
                  c1=[("C1", "variant 3")], c2=[("C2c", "when the seller releases it")],
                  s=[("S2", "if dropped"), ("S2c", "if a runner collects")]),
             dict(case="Pay on delivery", act="Choose", var="Books at address",
                  first="Same opening, plus the money sentence and the gate.",
                  c1=[("C1", "variant 3")], c2=[("C2c", "on payment")],
                  s=[("S2", "if dropped"), ("S2c", "if a runner collects")]),
             dict(case="Pay on delivery + goods", act="Choose", var="Books at address · goods owed",
                  first="Both amounts, both payees, one sentence each. Two segments.",
                  c1=[("C1", "variant 3")], c2=[("C2c", "both rails must clear")],
                  s=[("S2", "if dropped"), ("S2c", "if a runner collects")]),
             dict(case="Covered by sender", act="Choose", var="Books at address · nothing owed",
                  first="“…and is covering the delivery.” No money line, because there is no money.",
                  c1=[("C1", "variant 2")], c2=[("C2c", "on runner assignment")],
                  s=[("S2", "if dropped"), ("S2c", "if a runner collects")]),
         ]),

    dict(key="handler", title="Parcel handler", colour="accent-org",
         who="A sacco, a bus parcel office or a shop receiving on someone's behalf.",
         axis="Always address-unknown, always pay-now, never goods, and never a Pinned pod in the "
              "chain. The choose step doubles as the <b>consent</b> step — this is the first time "
              "the end client has been asked anything at all.",
         rows=[
             dict(case="Arrives at the handler", act="Choose &amp; consent",
                  var="Always pay-now · no goods · no pod",
                  first="“Hi”, not “Good news”. Names the end client, the town it came from, and the handler's premises.",
                  c1=[("C1c", "handler variant")], c2=[("C2c", "on payment")],
                  s=[("—", "the handler is not a Pinned sender")]),
         ]),
]

DISPATCH_NOTE = (
    "<b>What round five changed.</b> Round four cut the cases by who sent the parcel and how the "
    "money works. The dev page cuts them by <code>receiver_data.sender_address</code> first, "
    "because that is what decides which screen opens — and therefore what the SMS has to ask for. "
    "<b>C1d</b> is new: the confirm-only first contact, which had no message on this site at all "
    "and is the most common business case on the branch.")

GATE_INTRO = (
    "The doorstep code is the only thing Pinned withholds from anybody, so the rule behind it is "
    "worth stating exactly. It is <b>not</b> a property of the fee mode — <code>pay_now + goods</code> "
    "and <code>covered + goods</code> hold the code too — and the two things that hold it are "
    "released by different people, on different rails, which the copy must never blur.")

GATE_RAILS = [
    dict(t="The rule, verbatim",
         p="<code>handover_code_held? = (pay_on_delivery &amp;&amp; !trip_fee_paid) || "
           "(goods_owed &amp;&amp; !goods_confirmed)</code>. Two conditions, either of which is "
           "enough. A journey with both has to satisfy both before a single character of the code "
           "is sent."),
    dict(t="Rail one · the trip fee releases itself",
         p="An M-Pesa STK the receiver starts on the page. It clears the moment it settles, nobody "
           "has to approve it, and <b>the runner never touches money</b>. This is the rail the copy "
           "already describes correctly: <i>“your handover code appears once it's paid.”</i>"),
    dict(t="Rail two · the goods are released by the seller",
         p="Goods are paid to the seller on the seller's own rails. <b>Pinned cannot see that "
           "money.</b> The receiver tells the seller they have paid "
           "(<code>goods_payment_claimed</code>) and the seller releases the code from the host "
           "portal. The page can only notify — so the receiver is waiting on a human, and the copy "
           "has to say so rather than implying a machine is checking."),
    dict(t="Three release events, one message",
         p="The code SMS has three triggers — the trip fee clearing, the seller releasing the "
           "goods, or a runner being assigned on a journey with nothing owed. It is still one "
           "message, and it still carries only the code."),
    dict(t="One disclosure path, for every channel",
         p="Every disclosure of the doorstep code goes through "
           "<code>disclosable_handover_code</code> — page, SMS and JSON alike. In the helper's own "
           "words: <i>if the raw column reaches a client while held, the hold is cosmetic.</i> "
           "That applies to the SMS layer exactly as it applies to the view."),
    dict(t="The collection code is never gated",
         p="<code>virtual_host_otps.otp_code</code> — the code for walking into the branch — is a "
           "different object and is never held. Free collection is free, so there is nothing to "
           "hold it against. Two codes, two words, never used interchangeably."),
]


TOUCHPOINTS += [
    T(id="C1d", lane="receiver", stage="First contact",
      name="Just confirm your address is correct",
      trigger="A business sender creates a parcel with the receiver's address already on it",
      timing="At creation", channels=["sms"], status="gap",
      source="Dev branch · receiver-flows-prototype · 1 Nov", hook="Action",
      intent="There is nothing to choose. One thing to check, and the money comes after it.",
      warmth="“Just” is carrying the whole message. It tells somebody this will take ten seconds before they have opened anything.",
      review="<b>New, and the most common business case on the branch.</b> When "
             "<code>receiver_data.sender_address</code> is set the page opens on <i>Confirm your "
             "delivery address</i> — no choice screen, no distance screen. This site had no message "
             "for that, so it was sending <i>“Collect it free, or have it delivered to your door”</i> "
             "to people whose page offers neither.<br><br>"
             "<b>The fee is last in all three variants.</b> The primary action is identical whatever "
             "the money is doing, so pay-now reads like the covered case rather than like a bill — "
             "which is how the page reads.",
      msgs=[("sms", "Good news {{name}} — {{from}} has created a parcel for you, coming to {{addr}}. {{from}} is covering the delivery — just confirm your address is correct:\n{{track_url}}\n[covered]"),
            ("sms", "Good news {{name}} — {{from}} has created a parcel for you, coming to {{addr}}.\nJust confirm your address is correct: {{track_url}}\nThe Ksh {{fee}} trip fee is paid by M-Pesa on delivery — your code appears once it's paid.\n[pay on delivery]"),
            ("sms", "Good news {{name}} — {{from}} has created a parcel for you, coming to {{addr}}.\nJust confirm your address is correct: {{track_url}}\nThere's a Ksh {{fee}} trip fee to settle on the page before we dispatch.\n[pay now]")],
      rules=["The address is quoted back in the SMS. A person who sees their own street name knows "
             "within a second whether anything is wrong, without opening anything.",
             "The receiver can move the pin up to <b>500 m</b> and the price does not change. Beyond "
             "that the page refuses and names the sender: <i>“That's more than 500 m from the "
             "address {{from}} set. Please contact {{from}} to change it.”</i> The SMS never mentions "
             "the cap — it is a limit you meet only if you need it.",
             "Never “verify”. A person confirms an address; a system verifies one."]),

    T(id="C10", lane="receiver", stage="Exception",
      name="Nobody answered — it is going back",
      trigger="A receiver-not-found extension request lapses unanswered",
      timing="At the end of the ask window", channels=["sms"], status="gap",
      source="Dev branch · Receiver::Extensions::Expire · 1 Nov", hook="Trigger",
      intent="The runner has left and the parcel is moving away from them. Say so, and leave a door open.",
      warmth="“No charge” in the second sentence. A failed delivery that costs them nothing is the only reason this message can be calm.",
      review="<b>Found in the code, not in any pack.</b> <code>Receiver::Extensions::Expire</code> "
             "flips the request to <i>expired</i>, records a <code>ParcelEvent</code> and broadcasts "
             "to the tracking page — and sends <b>nothing</b>. So the one receiver who definitely is "
             "not looking at their phone, because they did not answer the last message, is the one "
             "we tell by updating a web page.<br><br>"
             "C8 and C9 both ship an SMS. The third outcome of the same flow does not.",
      msgs=[("sms", "{{runner}} waited at {{dest}} and we didn't hear back, so your parcel is going back to {{branch}}. No charge.\nTell us where to bring it and we'll try again: {{track_url}}")],
      rules=["Never “you failed to respond”. The runner waited and left; that is the fact, and it "
             "does not need a culprit.",
             "The ask window is a real deadline and the expiry copy on the page already states the "
             "consequence — <i>“Your runner is returning the parcel to the branch.”</i> The SMS says "
             "the same thing in the same words.",
             "This is the fourth and last message of the exception path. Nothing follows it."]),
]
for _t in TOUCHPOINTS:
    _t.setdefault("review", None)
    _t.setdefault("warmth", None)
_by_id = {t["id"]: t for t in TOUCHPOINTS}

ORDER.insert(ORDER.index("C1") + 1, "C1d")
ORDER.insert(ORDER.index("C9") + 1, "C10")
TOUCHPOINTS.sort(key=lambda t: ORDER.index(t["id"]))

# ── C1a: the create SMS is future tense, and it is not the choice page ──────
_by_id["C1a"].update(dict(
    name="It's on its way — track it and confirm your address",
    trigger="An individual completes a Send Now booking in the sender wizard",
    timing="At creation · the only SMS until the code",
    intent="Nothing has moved yet. Say what will happen, in the order it will happen, and ask for the one thing only they can check.",
    source="Dev branch · ParcelOrigin + DropNotifier · 1 Nov",
    warmth="The sender's own name, first. For an individual send that name is the whole message.",
    review="<b>Rewritten against <code>ParcelOrigin</code>, which was written against this site.</b> "
           "Round four had two variants, drop and runner, and got the tense wrong in both: the create "
           "SMS fires before the sender has left the house, so <i>“It's paid and waiting at "
           "{{station}}”</i> describes something that has not happened. The dev split it — "
           "<code>individual_create_line</code> is future tense for this message, "
           "<code>individual_status_line</code> is present tense for the drop SMS and the live "
           "page — and this site now follows that split.<br><br>"
           "<b>A different surface, and a different ask.</b> Individuals never reach "
           "<code>/p/</code>. <code>Receiver::DropNotifier</code> sends them to "
           "<code>/track/&lt;token&gt;</code>, which opens on an address confirm. So the link is a "
           "tracker link and the ask is <i>confirm your address</i>, not <i>track it</i>.",
    msgs=[("sms", "Good news {{name}} — {{sender_name}} is sending you a parcel through Pinned.\nIt's paid — it'll be dropped at {{station}}, then brought to your door.\nTrack it and confirm your address: {{track_url}}\n[the sender drops it at a Pod]"),
          ("sms", "Good news {{name}} — {{sender_name}} is sending you a parcel through Pinned.\nIt's paid — a runner will pick it up and bring it to your door.\nTrack it and confirm your address: {{track_url}}\n[a runner collects from the sender]")],
    rules=["Future tense, because nothing has happened yet. The present-tense line belongs to the "
           "drop SMS, which fires when the parcel actually reaches the Pod.",
           "<code>/track/</code>, never <code>/p/</code>. Sending a pre-paid receiver to a page with "
           "a price on it is how you generate a support call.",
           "The same 500 m rule applies here: the receiver may nudge a pre-set destination without "
           "re-pricing, and beyond that they are sent back to the sender."]))

# ── C2c: three release events, one message ──────────────────────────────────
_by_id["C2c"].update(dict(
    trigger="Whatever releases the hold: the trip fee clearing, the seller releasing the goods, or a runner assigned with nothing owed",
    review=_by_id["C2c"]["review"] + (
        "<br><br><b>Round five · three triggers, not one.</b> "
        "<code>handover_code_held?</code> is not a property of the fee mode — "
        "<code>pay_now + goods</code> and <code>covered + goods</code> hold the code too. The two "
        "rails release differently and the copy must not blur them: the trip fee is an M-Pesa STK "
        "that clears itself, while <b>goods are released by the seller</b>, because Pinned cannot "
        "see money paid on the seller's own rails. A receiver waiting on goods is waiting on a "
        "person, and the third variant says so."),
    msgs=_by_id["C2c"]["msgs"] + [
        ("sms", "{{name}}, {{from}} has confirmed your goods payment. Your handover code is {{otp}}.\nGive it only to your Pinned runner at the door. We never call or text to ask for it.\n[the seller released it]")],
    rules=_by_id["C2c"]["rules"] + [
        "Routed through <code>disclosable_handover_code</code> like every other disclosure. If the "
        "raw column reaches the SMS layer while the code is held, the hold is cosmetic."]))

# ── C8 / C9: the extension flow as it actually shipped ──────────────────────
_by_id["C8"].update(dict(
    status="live", source="Dev branch · Receiver::ExtensionNotifier · 1 Nov",
    review=_by_id["C8"]["review"] + (
        "<br><br><b>Round five · it shipped, verbatim.</b> "
        "<code>Receiver::ExtensionNotifier.not_found</code> carries this copy as the fallback behind "
        "the <code>receiver_not_found</code> template key. <code>Extensions::Open</code> enforces "
        "<b>one ask per delivery</b> and only while the parcel is <code>assigned</code> or "
        "<code>in_transit</code>. The ask has a window, and when it lapses nothing is sent — "
        "see <a href=\"#C10\">C10</a>."),
    rules=["One ask per delivery, enforced in <code>Extensions::Open</code>: <i>“The receiver has "
           "already been asked once for this delivery.”</i>",
           "The 3 km figure this site published came from the prototype page and is <b>not</b> in "
           "the shipped service — the quote prices whatever distance comes back. The only hard "
           "radius in the code is the 500 m self-adjust cap on the confirm screen, which is a "
           "different mechanism with a different purpose.",
           "Never “you were not available”. The runner is the one who cannot find them."]))

_by_id["C9"].update(dict(
    status="live", source="Dev branch · Receiver::Extensions::Quote · 1 Nov",
    review=_by_id["C9"]["review"] + (
        "<br><br><b>Round five · corrected against the shipped service.</b> The fee is "
        "<code>base_kes + distance_kes</code> on the route distance from where the runner is "
        "standing, priced by <code>Pricing.call</code> — there is no 3 km cap, and the breakdown "
        "the rule below promises is real. The priced SMS fires on the <b>first</b> price only, and "
        "only when <code>fee_mode == \"pay_now\"</code>; the other fee modes are silent here, which "
        "is logged as an open question."),
    rules=["The fee is base plus distance, from the runner's current position — not from the "
           "original address. That is why it can be quoted at all.",
           "<i>“Your handover code stays locked until this clears.”</i> The gate is a mechanism, "
           "stated plainly, exactly as on the page.",
           "One ask per delivery. The cap this site used to publish was the prototype's, not the "
           "service's."]))

OPEN_QUESTIONS = [
    dict(q="How long is the extension ask window, and why is the priced SMS only sent for pay-now?",
         why="<code>ParcelExtension::ASK_WINDOW</code> sets the deadline on both the “can't find "
             "you” ask and the price that follows it, and the model is outside the receiver sparse "
             "cone here, so the number could not be read. The copy for <a href=\"#C10\">C10</a> is "
             "written but cannot state the window until somebody says what it is. Separately, "
             "<code>Extensions::Quote</code> publishes the priced SMS only when "
             "<code>first_price &amp;&amp; fee_mode == \"pay_now\"</code> — so a pay-on-delivery or "
             "covered receiver is quoted a relocation fee on the page and never texted it. "
             "<b>Deliberate, or an oversight?</b>",
         who="Engineering"),
    dict(q="Who tells the receiver what the gate code is, or which block it is?",
         why="<code>parcel.receiver_note</code> renders only on the live screen, as <i>“Note from "
             "&lt;sender&gt;”</i>, and it is written by the <b>sender</b> at trip creation. There "
             "is no free-text field anywhere on the receiver surface — checkout captures an "
             "address, a phone number and a map pin, and nothing else. A shop sending to a stranger "
             "cannot know their gate code, their block or that the lift is broken, yet the person "
             "who does know has nowhere to put it. Today that gap is what produces "
             "<a href=\"#C8\">C8</a>.",
         who="Product"),
] + OPEN_QUESTIONS


JOURNEYS["receiver"] = dict(
    headline="Three SMS the first time, two every time after",
    sub="Getting the parcel is the same two messages in every case — one when it is created, one "
        "carrying the code — and the rating ask fires once per receiver, ever. What the first "
        "message <b>says</b> is set by the entry state: confirm an address, choose how to get it, "
        "or track it. Everything below the code is an exception.",
    steps=[
        J("1", "Address already known", "C1d", "sms", "Just confirm your address is correct", "The commonest business case. No choice, no distance screen.", grp="First contact · the verb is the entry state"),
        J("1b", "…no address on the parcel", "C1", "sms", "Collect it free, or have it delivered", "A real choice, so free is named first.", off=True),
        J("1c", "…an individual sent it", "C1a", "sms", "It's paid — track it and confirm your address", "A different surface. /track, never /p/, and future tense.", off=True),
        J("1d", "…or a handler received it", "C1c", "sms", "Hi — your parcel from {{town}} has arrived", "“Hi”, not “Good news”. The choose step is also the consent step.", off=True),
        J("2", "Whatever releases the hold", "C2c", "sms", "Your handover code is {{otp}}", "Three triggers, one message: trip fee cleared, goods released, or nothing owed.", grp="The code · the second and last message"),
        J("2b", "…or they chose to collect", "C2", "sms", "Station, hours, code, deadline", "The collection code is never gated. Free collection is free.", off=True),
        J("—", "Runner reaches the door", "C2b", "retire", "Nothing — the page is tracking live and the runner is there", "Retired. An SMS is the slowest way to talk to someone standing in front of a runner.", flag="retire"),
        J("—", "Shop hands it to the runner", "C1b", "in_app", "Tracking goes live on the page", "A status change the page shows, not a message."),
        J("+", "Runner can't find them", "C8", "sms", "Moved on? Tell us where you are now", "Live on the branch. One ask per delivery, while assigned or in transit.", grp="Exceptions · only when something goes wrong"),
        J("+", "They give a new spot", "C9", "sms", "Ksh {{ext_fee}} to move it — the runner keeps it all", "Base plus distance from where the runner is standing.", flag="open"),
        J("+", "Nobody answers in time", "C10", "sms", "Going back to {{branch}}. No charge", "Not built. Today the request lapses and nothing is sent.", flag="open"),
        J("+", "Running late", "C3", "sms", "New arrival time, reason, tracking", "A broken promise gets its own message."),
        J("+", "Half the clock gone", "C4a", "sms", "Still here, code, opening hours, deadline", "Rung 1. No charges apply, so none are mentioned.", grp="Nobody collected · four rungs, then silence"),
        J("+", "Clock nearly out", "C4b", "sms", "Free storage ends {{deadline}}, then the rate", "Rung 2. Where most door-delivery conversions happen."),
        J("+", "Clock runs out", "C4c", "sms", "Storage started, and how to stop it", "Rung 3. The link has to settle the charge, not just book a delivery."),
        J("+", "Day 7", "C4d", "sms", "Goes back today — or we bring it to you today", "Rung 4. The pack keeps the door open to the last message."),
        J("+", "Asks for more storage time", "C6a", "sms", "Approved — new deadline", "Time, not distance. C9 is the other one."),
        J("4", "Collects", "C7", "sms", "It's all yours — rate your runner, save your address", "Once per receiver, ever. The only ask in the lane.", grp="Afterwards · once per receiver, ever"),
    ])


# ── ASK_WINDOW resolved · ParcelExtension::ASK_WINDOW = 20.minutes ──────────
# One constant, used at both call sites (Extensions::Open and Extensions::Quote
# both set expires_at: ASK_WINDOW.from_now), so pricing RESETS the clock: a
# receiver who answers buys a fresh twenty minutes to pay.

BUILD = 16
UPDATED = "1 November 2026 · the twenty-minute window, stated before it runs out"

_by_id = {t["id"]: t for t in TOUCHPOINTS}

_by_id["C8"].update(dict(
    intent="Somebody is standing in the wrong place, on a clock. Fix it in one tap, say how long there is, and blame nobody.",
    msgs=[("sms", "{{runner}} is at {{spot}} and can't find you at {{dest}}.\nMoved on? Tell us where you are now: {{track_url}}\nWe'll wait 20 minutes, then it goes back to the branch — no charge.")],
    review=_by_id["C8"]["review"] + (
        "<br><br><b>The window is twenty minutes, and it now appears in the message.</b> "
        "<code>ParcelExtension::ASK_WINDOW = 20.minutes</code>. The shipped body does not say so, "
        "which makes the lapse arrive with no warning — and the lapse is the expensive outcome, "
        "because the parcel physically leaves. <b>This adds one line to the live copy and takes the "
        "message to two segments.</b> That is the right place to spend it: better to pay for the "
        "warning than for <a href=\"#C10\">C10</a>, which only exists because the warning was "
        "missed."),
    rules=_by_id["C8"]["rules"] + [
        "The clock is reset by answering. <code>Extensions::Quote</code> sets "
        "<code>expires_at: ASK_WINDOW.from_now</code> again when it prices, so a receiver who "
        "replies gets a fresh twenty minutes to pay — which is worth knowing before anyone writes "
        "copy implying the first twenty minutes covers everything."]))

_by_id["C10"]["msgs"] = [
    ("sms", "{{runner}} waited 20 minutes at {{dest}} and we didn't hear back, so your parcel is going back to {{branch}}. No charge.\nTell us where to bring it and we'll try again: {{track_url}}")]
_by_id["C10"]["review"] += (
    "<br><br><b>The window is twenty minutes</b> (<code>ParcelExtension::ASK_WINDOW</code>), the "
    "same constant behind the ask in <a href=\"#C8\">C8</a> — and the same clock as the prototype "
    "page's <i>“returns to the branch after a 20-min wait — no charge”</i>. Both messages now name "
    "it, so the number a receiver is told is the number the job actually runs on.")

OPEN_QUESTIONS = [
    (dict(q="Why is the priced extension SMS sent only for pay-now?",
          why="<code>Extensions::Quote</code> publishes the priced message only when "
              "<code>first_price &amp;&amp; fee_mode == \"pay_now\"</code>. A pay-on-delivery or "
              "covered receiver is therefore quoted a relocation fee on the page and never texted "
              "it — so if they close the tab inside the twenty-minute window, nothing reaches them "
              "and the parcel goes back. <b>Deliberate, because those fee modes settle elsewhere, "
              "or an oversight?</b> <a href=\"#C9\">C9</a> is written as if every fee mode gets it.",
          who="Engineering")
     if q["q"].startswith("How long is the extension ask window") else q)
    for q in OPEN_QUESTIONS
]

_by_id["C10"]["timing"] = "20 minutes after the ask, unanswered"


# ── The priced-extension silence, resolved — and one half of it is a hole ───
# Confirmed with the public choice session and read in Extensions::Apply:
#   charge += extension.fee_kes if fee_mode.in?(%w[pay_on_delivery covered])
# pay-now is the only mode where the relocation fee is a separate payment the
# receiver must make, which is why Quote publishes the priced SMS only there.
# For covered the business absorbs it and the receiver is unaffected. For
# pay-on-delivery the fee is folded into the DOOR CHARGE — so the amount this
# site already texted them is now wrong, and nothing tells them.

BUILD = 17
UPDATED = "1 November 2026 · the door total that moves without a message"

_by_id = {t["id"]: t for t in TOUCHPOINTS}

_by_id["C9"].update(dict(
    name="Moving the drop — priced, or folded in",
    intent="A priced change of plan. Every number shown, including the one that just changed behind it.",
    review=_by_id["C9"]["review"] + (
        "<br><br><b>Why only pay-now gets the priced SMS, and why that is right.</b> "
        "<code>Extensions::Quote</code> publishes it when "
        "<code>first_price &amp;&amp; fee_mode == \"pay_now\"</code>, because pay-now is the only "
        "mode where the relocation fee is a <i>separate payment the receiver must make</i> — "
        "<code>payment_due?</code> is true and the code is gated behind it. Reserving SMS for "
        "“you must act” is this site's own rule, applied correctly.<br><br>"
        "<b>But the fee does not vanish in the other two modes.</b> "
        "<code>Extensions::Apply</code> does "
        "<code>charge += extension.fee_kes if fee_mode.in?(%w[pay_on_delivery covered])</code>. "
        "For <b>covered</b> the business absorbs it and the receiver is genuinely unaffected — "
        "silence is correct. For <b>pay-on-delivery</b> it is added to "
        "<code>confirmed_charge_kes</code>: the receiver pays more at the door than the figure we "
        "texted them at creation, and nothing tells them. That is not a fee they can ignore — it "
        "is cash they have to be holding when the runner arrives. Hence the second variant."),
    msgs=_by_id["C9"]["msgs"] + [
        ("sms", "Moving your delivery to {{spot}} is {{ext_km}} km further — Ksh {{ext_fee}} more.\nYou'll now pay Ksh {{amount}} at the door, not Ksh {{fee}}. Nothing to do now: {{runner}} is on the way.\n[pay on delivery — folded into the door charge]")],
    rules=_by_id["C9"]["rules"] + [
        "<b>Three fee modes, two messages.</b> Pay-now is asked to pay and the code is gated. "
        "Pay-on-delivery is told the door total moved, and asked for nothing. Covered is told "
        "nothing, because the business absorbed it and there is no fact about them that changed.",
        "The second variant states the old figure next to the new one. A number that silently "
        "replaces a number we texted is how a delivery turns into an argument on a doorstep."]))

OPEN_QUESTIONS = [q for q in OPEN_QUESTIONS
                  if not q["q"].startswith("Why is the priced extension SMS sent only for pay-now")]


# ═══════════════════════════════════════════════════════════════════════════
# ROUND SIX · 1 November — the count was wrong, and the gate has three rails
#
# The public choice session walked the prototype head (59a4c68b) and corrected
# three things this site was publishing. All three verified here against the
# tree before being written down:
#   · code_held? has THREE rails — a priced pay-now relocation holds the code.
#   · "Two SMS" does not survive contact with the code. A first-time business
#     door delivery is three; an individual send is four.
#   · The individual's SMS link is /track/<token>, but HomeController#track
#     redirects a private-link individual to /p/<token>. Link and page differ.
# ═══════════════════════════════════════════════════════════════════════════

BUILD = 18
UPDATED = "1 November 2026 · the real count, and the third rail"

_by_id = {t["id"]: t for t in TOUCHPOINTS}

DISPATCH_RULES[2] = dict(
    n="03", t="One SMS when the parcel is created",
    p="Whoever created it, exactly one SMS goes out at creation. The entry state and the money "
      "change what it says. Nothing changes the count. This is the only part of the old "
      "“two messages” rule that survived reading the code.")

DISPATCH_RULES[3] = dict(
    n="04", t="Then a code, then — once ever — a rating. Four on an individual send",
    p="The honest count, per journey: a <b>business door delivery</b> is three the first time "
      "(created, the code, the rating) and two after, because "
      "<code>DeliveredNotifier.asked_before?</code> keys on the receiver's phone across every "
      "parcel they have ever had. An <b>individual send</b> is four the first time, because the "
      "parcel physically leaves the sender and "
      "<code>parcel_dropped</code>/<code>parcel_dropped_runner</code> says so. "
      "<b>Free collection is two</b>, and gets no rating at all — "
      "<code>DeliveredNotifier</code> returns early without a <code>dest_address</code> and a "
      "runner. Quoting “two” at every journey was tidy and false.")

GATE_INTRO = (
    "The doorstep code is the only thing Pinned withholds from anybody, so the rule behind it is "
    "worth stating exactly. It is <b>not</b> a property of the fee mode — <code>pay_now + goods</code> "
    "and <code>covered + goods</code> hold the code too — and the <b>three</b> things that hold it "
    "are released by three different parties, which the copy must never blur.")

GATE_RAILS = [
    dict(t="The rule, verbatim",
         p="<code>code_held? = trip_fee_due? || goods_owed? || extension_payment_due?</code>, from "
           "<code>Parcel::FeeMode</code>. Three conditions, any one of which is enough. A journey "
           "that trips two of them has to satisfy both before a single character is sent."),
    dict(t="Rail one · the trip fee releases itself",
         p="<code>cod_flag? &amp;&amp; !business_covered? &amp;&amp; !fully_paid?</code>. An M-Pesa "
           "STK the receiver starts on the page; it clears when "
           "<code>payment_confirmed_at</code> is set. Nobody approves it, and <b>the runner never "
           "touches money</b>. This is the rail the copy already describes correctly."),
    dict(t="Rail two · the goods are released by the seller",
         p="<code>goods_enabled? &amp;&amp; goods_confirmed_at.nil?</code>. Goods are paid on the "
           "seller's own rails and <b>Pinned cannot see that money</b>. The receiver files a "
           "<code>goods_payment_claimed</code> interaction and the seller releases the code from "
           "the host portal. The receiver is waiting on a person, and the copy has to say so "
           "rather than implying a machine is checking."),
    dict(t="Rail three · an unpaid relocation holds it too",
         p="<code>extension.open? &amp;&amp; extension.payment_due?</code>. A pay-now receiver who "
           "has been quoted a relocation fee and not yet paid it has their code held — on a parcel "
           "that may have had nothing owed ten minutes earlier. <b>This site missed it entirely</b>, "
           "which is why <a href=\"#C9\">C9</a>'s line <i>“your handover code stays locked until "
           "this clears”</i> is a statement of fact and not a flourish."),
    dict(t="Three release events, one message",
         p="<code>parcel.handover_code_released</code> fires once, whichever rail cleared last, and "
           "<code>handover_code_ready</code> / <code>handover_code_ready_covered</code> carry the "
           "code. It is still one message, and it still carries only the code."),
    dict(t="One disclosure path, for every channel",
         p="Every disclosure of the doorstep code goes through "
           "<code>disclosable_handover_code</code> — page, SMS and JSON alike. In the helper's own "
           "words: <i>if the raw column reaches a client while held, the hold is cosmetic.</i>"),
    dict(t="The pickup code is never gated",
         p="<code>virtual_host_otps.otp_code</code> is a different object and is never held — in "
           "<code>Parcel::FeeMode</code>'s own comment, <i>a runner must always be able to collect "
           "from the host branch regardless of what the receiver owes</i>. Two codes, two words, "
           "never used interchangeably."),
]


TOUCHPOINTS += [
    T(id="C1e", lane="receiver", stage="In transit", name="It has left the sender",
      trigger="An individual's parcel is dropped at a Pod, or collected from the sender by a runner",
      timing="At the drop or the pickup · once", channels=["sms"], status="live",
      key="parcel_dropped / parcel_dropped_runner",
      source="Dev branch · Receiver::DropNotifier · 1 Nov", hook="Reward",
      intent="The create message said this would happen. This is the message that says it did.",
      warmth="Nothing extra. The fact is the reward — a stranger's promise turned into a movement they can watch.",
      review="<b>The message this site did not know existed, and the reason the count was wrong.</b> "
             "<code>Receiver::DropNotifier.notify_parcel_dropped</code> fires on the sender-drop "
             "path with two template keys — <code>parcel_dropped</code> when there is an "
             "<code>origin_station</code>, <code>parcel_dropped_runner</code> when a runner "
             "collected — guarded once by a <code>receiver_drop_notified</code> event.<br><br>"
             "<b>It is the present-tense half of the C1a split.</b> "
             "<code>ParcelOrigin.individual_status_line</code> belongs here, not at creation, and "
             "this is the message it was written for. An individual send therefore costs four SMS "
             "the first time, not three.",
      msgs=[("sms", "Good news {{name}} — {{sender_name}} has sent you a parcel.\nIt's paid and waiting at {{station}}, heading to you now.\nTrack it: {{track_url}}\n[dropped at a Pod]"),
            ("sms", "Good news {{name}} — {{sender_name}} has sent you a parcel.\nIt's paid, and {{runner}} is collecting it from {{origin}} now.\nTrack it: {{track_url}}\n[a runner collected it]")],
      rules=["Present tense, because something has now actually happened. The future-tense version "
             "is <a href=\"#C1a\">C1a</a> and fires at creation.",
             "Once per parcel, guarded by the <code>receiver_drop_notified</code> event. A second "
             "drop notification against one parcel is a bug, not a reminder.",
             "This is the only receiver message that exists purely to confirm a promise. It earns "
             "its segment because the promise was made to somebody who had never heard of us."]),

    T(id="S7", lane="sender", stage="In transit", name="Your receiver moved the drop",
      trigger="The receiver changes the delivery address, by confirm-page nudge or by extension",
      timing="On the address change", channels=["sms"], status="live",
      source="Dev branch · ParcelHandler#notify_sender_address_changed · 1 Nov", hook="Trigger",
      intent="Somebody changed the sender's instruction. Tell them, with both addresses, and ask for nothing.",
      warmth="None, deliberately. This is a fact about their parcel, and the shortest version is the kindest.",
      review="<b>Live today, and absent from this site until now.</b> "
             "<code>parcel.delivery_address_changed</code> notifies the <b>sender and the "
             "runner</b> — never the receiver, who made the change and already knows. The sender "
             "body is built inline in <code>Subscribers::ParcelHandler</code> rather than from a "
             "<code>NotificationTemplate</code>, so it is the one receiver-driven sender message "
             "that cannot be edited without a deploy.<br><br>"
             "<b>Changed from the live body:</b> <i>“parcel {{code}} should be delivered to…”</i> "
             "is passive and buries the change. Both addresses belong in the message, in the order "
             "old-then-new, because the sender is checking whether this is a correction or a "
             "problem.",
      old="{{name}} has changed where parcel {{code}} should be delivered to {{dest}}. It was {{origin}}.",
      msgs=[("sms", "{{name}} moved the delivery for Parcel {{code}} from {{origin}} to {{dest}}.\n{{runner}} has the new address. Nothing for you to do.")],
      rules=["The last line is the point. A sender who reads that their receiver changed something "
             "will assume they have to act unless the message says otherwise.",
             "Pull this into a <code>NotificationTemplate</code> key. Every other message in the "
             "estate is editable without a deploy; this one is not, and there is no reason for it."]),
]
for _t in TOUCHPOINTS:
    _t.setdefault("review", None)
    _t.setdefault("warmth", None)
_by_id = {t["id"]: t for t in TOUCHPOINTS}

ORDER.insert(ORDER.index("C1b") + 1, "C1e")
ORDER.insert(ORDER.index("S3"), "S7")
TOUCHPOINTS.sort(key=lambda t: ORDER.index(t["id"]))

# ── C1a: the link and the page are not the same thing ──────────────────────
_by_id["C1a"]["rules"] = [
    "Future tense, because nothing has happened yet. The present-tense version is "
    "<a href=\"#C1e\">C1e</a>, which fires when the parcel actually leaves the sender.",
    "<b>The link is <code>/track/</code>; the page is <code>/p/</code>.</b> "
    "<code>HomeController#track</code> redirects a private-link individual straight to the choice "
    "page, where <code>_delivery_live</code> renders the confirm-address step on top of the live "
    "timeline. The link stays <code>/track/</code> because that is the surface a typed parcel "
    "reference reaches, and only the private link proves who is holding the phone.",
    "The 500 m nudge is <b>individuals only</b> — "
    "<code>DeliveryAddressUpdate.editable?</code> requires <code>individual_send_now?</code>. "
    "Business and handler confirm screens change an address by a different path, with no cap.",
]
_by_id["C1a"]["review"] += (
    "<br><br><b>Round six · corrected.</b> This site said <i>“<code>/track/</code>, never "
    "<code>/p/</code>”</i>. The link is <code>/track/</code> and the page is <code>/p/</code>: "
    "<code>HomeController#track</code> redirects on "
    "<code>private_link &amp;&amp; individual_send_now? &amp;&amp; !turbo_frame</code>. The "
    "practical consequence for copy is nil — the receiver sees a tracker link and lands on a page "
    "that opens with their address — but a rule stated wrongly gets followed wrongly.")

# ── C9: fire it from Apply, on its own event ───────────────────────────────
_by_id["C9"]["rules"] = _by_id["C9"]["rules"] + [
    "<b>The pay-on-delivery variant fires from <code>Extensions::Apply</code>, not "
    "<code>Quote</code>.</b> At quote time the fee is only <i>priced</i> — a proposal that can "
    "lapse in twenty minutes — and <code>confirmed_charge_kes</code> is untouched, so nothing "
    "about their door total is true yet. It becomes true in <code>Apply#update_parcel!</code>.",
    "It needs its own event. <code>parcel.delivery_address_changed</code> is also published by the "
    "500 m confirm-page update, so subscribing to it would text a door total to individuals who "
    "nudged a pin. A dedicated <code>parcel.extension_applied</code>, gated on "
    "<code>fee_mode == \"pay_on_delivery\"</code>, is the clean seam.",
]

# ── C7: it is once per receiver in the code, and not on every journey ──────
_by_id["C7"]["review"] += (
    "<br><br><b>Round six · confirmed in the code, with one limit this site had not stated.</b> "
    "<code>DeliveredNotifier.asked_before?</code> keys on the receiver's <i>phone number</i> "
    "across every parcel it has ever appeared on, so “once per receiver, ever” is literally true. "
    "It also returns early unless there is a <code>dest_address</code> and an assigned runner — "
    "so <b>nobody who collects for free is ever asked to rate anything</b>. That is defensible "
    "(there is no runner to rate) but it means the rating sample is doorstep-only, and the lane's "
    "SMS count differs by journey.")

OPEN_QUESTIONS = [
    dict(q="Should the 500 m nudge and the runner's relocation be one mechanism?",
         why="They are two code paths with opposite rules today. "
             "<code>Receiver::DeliveryAddressUpdate</code> is individuals-only, caps the move at "
             "<b>500 m</b>, never re-prices, and <b>hard-blocks</b> beyond the cap — <i>“contact "
             "{{from}} to change it”</i>. <code>Receiver::Extensions</code> is runner-initiated, "
             "has no distance cap at all, and prices whatever comes back. A receiver can therefore "
             "be refused a 600 m correction at breakfast and sold a 6 km one at the door. The "
             "stated intent is to unify them — under 500 m no change, beyond it recalculate the "
             "delivery fee for the new location — and <b>until that lands, no copy on this site "
             "may imply a single “move your delivery” rule</b>, because there isn't one.",
         who="Product"),
] + OPEN_QUESTIONS


JOURNEYS["receiver"] = dict(
    headline="Three SMS on a business door delivery, four on an individual send, two to collect",
    sub="The count is not one number, and pretending it was is how this site got it wrong. What is "
        "constant: <b>one</b> message at creation, whose verb is set by the entry state — confirm, "
        "choose, or track and confirm — and <b>one</b> carrying the code, whenever the last of the "
        "three gate rails clears. An individual send adds a message when the parcel actually leaves "
        "the sender. A door delivery adds the rating, once per receiver ever. Free collection gets "
        "neither.",
    steps=[
        J("1", "Address already known", "C1d", "sms", "Just confirm your address is correct", "The commonest business case. No choice, no distance screen.", grp="First contact · the verb is the entry state"),
        J("1b", "…no address on the parcel", "C1", "sms", "Collect it free, or have it delivered", "A real choice, so free is named first.", off=True),
        J("1c", "…an individual sent it", "C1a", "sms", "It's paid — track it and confirm your address", "Future tense. The link is /track/, the page it lands on is /p/.", off=True),
        J("1d", "…or a handler received it", "C1c", "sms", "Hi — your parcel from {{town}} has arrived", "“Hi”, not “Good news”. The choose step is also the consent step.", off=True),
        J("2", "It leaves the sender", "C1e", "sms", "Dropped at {{station}} / {{runner}} is collecting it now", "Individual sends only. The present-tense half of the C1a split.", grp="On the move · individual sends only"),
        J("—", "Shop hands it to the runner", "C1b", "in_app", "Tracking goes live on the page", "A business parcel never left anybody's house. No message."),
        J("3", "The last rail clears", "C2c", "sms", "Your handover code is {{otp}}", "Trip fee, goods, or an unpaid relocation — whichever cleared last.", grp="The code · one message, three rails"),
        J("3b", "…or they chose to collect", "C2", "sms", "Station, hours, code, deadline", "The pickup code is never gated. Free collection is free.", off=True),
        J("—", "Runner reaches the door", "C2b", "retire", "Nothing — the page is tracking live and the runner is there", "Retired. An SMS is the slowest way to talk to someone standing in front of a runner.", flag="retire"),
        J("4", "Delivered", "C7", "sms", "It's all yours — rate your runner", "Once per receiver, ever, and never on a free collection.", grp="Afterwards · once per phone number, ever"),
        J("+", "Runner can't find them", "C8", "sms", "Moved on? 20 minutes, then it goes back", "One ask per delivery, while assigned or in transit.", grp="Exceptions · only when something goes wrong"),
        J("+", "They give a new spot", "C9", "sms", "Priced, or folded into the door total", "Two variants. Covered hears nothing, because nothing about them changed."),
        J("+", "Nobody answers in time", "C10", "sms", "Going back to {{branch}}. No charge", "Not built. Today the request lapses and nothing is sent.", flag="open"),
        J("+", "Running late", "C3", "sms", "New arrival time, reason, tracking", "A broken promise gets its own message."),
        J("+", "Half the clock gone", "C4a", "sms", "Still here, code, opening hours, deadline", "Rung 1. No charges apply, so none are mentioned.", grp="Nobody collected · four rungs, then silence"),
        J("+", "Clock nearly out", "C4b", "sms", "Free storage ends {{deadline}}, then the rate", "Rung 2. Where most door-delivery conversions happen."),
        J("+", "Clock runs out", "C4c", "sms", "Storage started, and how to stop it", "Rung 3. The link has to settle the charge, not just book a delivery."),
        J("+", "Day 7", "C4d", "sms", "Goes back today — or we bring it to you today", "Rung 4. The pack keeps the door open to the last message."),
        J("+", "Asks for more storage time", "C6a", "sms", "Approved — new deadline", "Time, not distance. C9 is the other one."),
    ])

JOURNEYS["sender"]["steps"].insert(
    [i for i, s in enumerate(JOURNEYS["sender"]["steps"]) if s["tp"] == "S3"][0],
    J("+", "The receiver moves the drop", "S7", "sms", "Moved from {{origin}} to {{dest}} — nothing to do", "Live today, and built inline rather than from a template."))

JOURNEYS["receiver"]["budget"] = ("3 SMS on a business door delivery · 4 on an individual send · 2 to collect")


# ── The wait window becomes a token, because the template now has one ──────
# receiver-flows/extension-ask-deadline (9a4ecc3f) adds
# ParcelExtension::WAIT_LABEL = ASK_WINDOW.inspect and passes it to the
# receiver_not_found template as {{wait}}. Publishing "20 minutes" as a literal
# here would reintroduce exactly the drift that commit exists to prevent.

BUILD = 19
UPDATED = "1 November 2026 · the wait window is a token, not a number"

SAMPLES.update({"wait": "20 minutes"})
_by_id = {t["id"]: t for t in TOUCHPOINTS}

_by_id["C8"]["msgs"] = [
    ("sms", "{{runner}} is at {{spot}} and can't find you at {{dest}}.\nMoved on? Tell us where you are now: {{track_url}}\nWe'll wait {{wait}}, then it goes back to the branch — no charge.")]
_by_id["C8"]["review"] += (
    "<br><br><b>Shipped, and the window is a token now.</b> Branch "
    "<code>receiver-flows/extension-ask-deadline</code> (<code>9a4ecc3f</code>) adds the third "
    "line to both carriers of this copy and derives the label from the clock: "
    "<code>ParcelExtension::WAIT_LABEL = ASK_WINDOW.inspect</code>, passed into the template as "
    "<code>{{wait}}</code>. A migration rewrites the existing row only where it still holds the "
    "exact two-line body, so any hand-edited environment is left alone.<br><br>"
    "This site therefore publishes <code>{{wait}}</code> rather than the words “20 minutes”. "
    "Writing the number here would reintroduce the drift the commit exists to prevent — the day "
    "somebody tunes the window, the copy follows it everywhere or nowhere.")
_by_id["C8"]["rules"] = _by_id["C8"]["rules"] + [
    "<b>Never write a duration this system controls as a literal.</b> The window is "
    "<code>{{wait}}</code>, the self-move cap is <code>MAX_SHIFT_LABEL</code>, and both exist "
    "because a number typed into copy survives the change that makes it wrong. The storage clock "
    "is the counter-example — it is a <code>{{deadline}}</code>, because a duration is the wrong "
    "shape to give a customer in the first place."]

_by_id["C10"]["msgs"] = [
    ("sms", "{{runner}} waited {{wait}} at {{dest}} and we didn't hear back, so your parcel is going back to {{branch}}. No charge.\nTell us where to bring it and we'll try again: {{track_url}}")]
_by_id["C10"]["review"] += (
    "<br><br>When this is built it takes <code>{{wait}}</code> from the same "
    "<code>ParcelExtension::WAIT_LABEL</code> that <a href=\"#C8\">C8</a> now uses, so the ask and "
    "the lapse quote one number that neither of them owns.")


# ═══════════════════════════════════════════════════════════════════════════
# ROUND SEVEN · 10 November — who the message is from
#
# The email template set arrived on branch email/transactional-templates with
# a question attached: the campaign fixtures send from pinnedflow.com while the
# brand is PinnedFlow.app, and that might just be stale fixture data.
#
# It is not. Grepping app/ and config/ in pinned-core returns five addresses
# across two domains, and the split runs straight through the live estate.
# ═══════════════════════════════════════════════════════════════════════════

BUILD = 20
UPDATED = "10 November 2026 · one estate, two domains"

LAWS = LAWS + [
    dict(t="One identity per class, and never one role on two domains",
         p="Pinned sends three classes of mail and they cannot share a sending identity: "
           "<b>transactional</b> (a code, a receipt, a statement — must arrive), "
           "<b>operational</b> (a host primer, a runner notice), and <b>outreach</b> (cold pitches, "
           "campaigns). They are separated so that a complaint about the third can never delay the "
           "first. That separation is worthless if the same role answers on two domains, which is "
           "what the estate does today — see the open question."),
]

OPEN_QUESTIONS = [
    dict(q="Is Pinned pinnedflow.app or pinnedflow.com — and which one has the DNS?",
         why="This is not stale fixture data. <code>pinned-core</code> carries <b>five addresses "
             "across two domains</b>, and they are split by accident rather than by role:<br><br>"
             "<b>The only real From header is <code>.app</code>.</b> "
             "<code>config/initializers/devise.rb</code> sets "
             "<i>Pinned Support &lt;support@pinnedflow.app&gt;</i>. So is the runner portal's "
             "<code>runners@pinnedflow.app</code>.<br><br>"
             "<b>Everywhere a customer is told to write to us, it is <code>.com</code>.</b> "
             "<code>batch_subscriber.rb</code>, <code>runner_subscriber.rb</code> and "
             "<code>route_batch/admin_actions.rb</code> all end on "
             "<i>“Questions? hello@pinnedflow.com”</i> — and so do "
             "<code>config/content/site.yml</code> and <code>legal.yml</code>, which is where the "
             "refund route and the complaints route live. Those two are legally operative "
             "addresses, not copy.<br><br>"
             "<b>And one message already disagrees with the others.</b> "
             "<code>dwell/notifier.rb</code> gives the same contact address as "
             "<code>hello@pinnedflow<b>.app</b></code>. Two live messages, one role, two domains.<br><br>"
             "Three things ride on the answer. <b>Deliverability</b> — DKIM, DMARC and later BIMI "
             "attach to the From domain, and signing one while sending as the other is how a "
             "collection code lands in spam. <b>Trust</b> — a receiver holding a parcel from "
             "<i>pinnedflow.app</i> who is asked to email <i>.com</i> has a phishing question to "
             "answer, and the honest answer is that we do not know either. <b>Reachability</b> — "
             "if <code>.com</code> has no MX record, every refund and complaint route in the legal "
             "pages is a dead letter. <b>Check that before anything else.</b>",
         who="Founder"),
] + OPEN_QUESTIONS


# ── The DNS settles it ──────────────────────────────────────────────────────
# dig, 10 Nov 2026:
#   pinnedflow.app  MX mx{,2,3}.zoho.com · NS digitalocean · SPF include:zohomail.com
#   pinnedflow.com  no MX, no NS, no SPF — not delegated at all
#   pinned.app      NS sedoparking.com · MX 0 localhost · SPF "v=spf1 -all"
# So .com is not a choice, it is a dead letter; and pinned.app — which THIS SITE
# was publishing as the From identity until today — is a parked domain that
# belongs to somebody else.

BUILD = 21
UPDATED = "10 November 2026 · the From line, checked against the DNS"

OPEN_QUESTIONS[0] = dict(
    q="Every address we publish on pinnedflow.com is a dead letter — who fixes the three live messages?",
    why="The email brief asked whether <code>pinnedflow.com</code> was stale fixture data. It is "
        "worse than that. <b>A DNS lookup on 10 November returns nothing for it</b> — no MX, no "
        "SPF, no nameservers; the domain is not delegated. Mail to "
        "<code>hello@pinnedflow.com</code> cannot be delivered to anybody.<br><br>"
        "<b>pinnedflow.app is the real one.</b> Zoho MX, DigitalOcean nameservers, "
        "<code>v=spf1 include:zohomail.com ~all</code>. It is also the only domain in a live "
        "From header — <code>devise.rb</code> sends as "
        "<i>Pinned Support &lt;support@pinnedflow.app&gt;</i>.<br><br>"
        "<b>So this is not a branding choice, it is three broken messages.</b> "
        "<code>batch_subscriber.rb</code>, <code>runner_subscriber.rb</code> and "
        "<code>route_batch/admin_actions.rb</code> each end on <i>“Questions? "
        "hello@pinnedflow.com”</i>, and <code>config/content/site.yml</code> and "
        "<code>legal.yml</code> route refunds and complaints there. Every one of those is an "
        "instruction to write to an address that does not exist. "
        "<code>dwell/notifier.rb</code> already says <code>.app</code>, so the fix is to make the "
        "other five match it, not to decide anything.<br><br>"
        "<b>One thing still to confirm:</b> that <code>hello@</code> and "
        "<code>notifications@</code> mailboxes exist on the Zoho tenant. The domain is right; "
        "whether those two names are provisioned is not something DNS can answer.",
    who="Founder")

OPEN_QUESTIONS = [
    dict(q="Did anything ever send as notifications@pinned.app?",
         why="<b>This site published that address as the email From identity until today</b>, "
             "recorded from <code>MessageSender</code> in round one. It is not Pinned's domain. "
             "<code>pinned.app</code> is parked — nameservers at <code>sedoparking.com</code>, "
             "<code>MX 0 localhost</code>, and an SPF record of <code>v=spf1 -all</code>, which "
             "says in as many words that <b>nobody is authorised to send mail as it</b>.<br><br>"
             "Any message that went out with that From line would have failed SPF outright: "
             "spam-foldered at best, rejected at worst, and attributed to a domain a parking "
             "service controls. It no longer appears anywhere in <code>pinned-core</code>'s "
             "<code>app/</code> or <code>config/</code>, so it may already have been fixed, or it "
             "may have been wrong in this document and never in production. "
             "<b>Worth ten minutes in the mail logs to know which</b>, because the two answers "
             "have very different consequences for sender reputation.<br><br>"
             "Corrected here to <code>notifications@pinnedflow.app</code>.",
         who="Engineering"),
] + OPEN_QUESTIONS


# ═══════════════════════════════════════════════════════════════════════════
# ROUND EIGHT · 10 November — email gets a page
#
# The rules were living in email/IMPLEMENTATION.md on an unmerged branch,
# which is to say nowhere a developer could reach them. They move here. The
# brief keeps the destinations — which file, which repo — and points back.
#
# The rules are stated in ONE place. If the page and the brief both describe
# the sending classes they will drift, and whoever is implementing will follow
# whichever they found first.
# ═══════════════════════════════════════════════════════════════════════════

BUILD = 22
UPDATED = "10 November 2026 · email gets a page, and three senders get one voice"

NAV.insert(3, ("email.html", "Email"))
NAV_GROUPS[0] = ("Foundations", NAV_GROUPS[0][1][:3] + [("email.html", "Email")])

EMAIL_LEDE = (
    "Pinned will send mail from three places — a person typing in Zoho, the Messaging Centre on "
    "pinnedflow.app, and the system itself. Only two of them can share a template, and the third "
    "should not try. This page is the rule set; the markup and the destinations live in "
    "<a href=\"email/IMPLEMENTATION.md\">the implementation brief</a> beside it.")

EMAIL_SURFACES = [
    dict(k="A person, in Zoho", colour="accent-org",
         who="A reply, a one-off note, a follow-up after a call. Low volume, high trust.",
         tmpl="<b>A Zoho Mail template, or nothing.</b> Zoho does have Templates — Settings → "
              "Templates, inserted into a compose window — and they are right for a signature and "
              "for short standard replies.",
         cant="<b>They cannot carry the production shell.</b> Zoho's composer sanitises what you "
              "paste: <code>&lt;!--[if mso]&gt;</code> conditional comments are stripped, the "
              "<code>&lt;style&gt;</code> block very likely goes with them — taking dark mode and "
              "every <code>px-*</code> class — and VML will not survive. Inline styles mostly do. "
              "The result looks close in Apple Mail and falls apart in Outlook, which is the exact "
              "failure the markup was built to prevent.<br><br>"
              "There is also no merge: a Zoho template has no way to resolve "
              "<code>{{name}}</code> against Pinned's data.",
         do="<b>Send plain, and let the signature carry the brand.</b> A reply from a named person "
            "should not look like a template — it should look like a person wrote it. What makes "
            "it Pinned is the vocabulary and a small, simple HTML signature, which is the one "
            "thing Zoho does reliably."),

    dict(k="The Messaging Centre", colour="accent-mag",
         who="Campaigns and outreach, composed by a human in the admin on pinnedflow.app.",
         tmpl="<b>The blocks.</b> The composer inserts them into the body and the app wraps them "
              "in the same layout at send time, so a campaign and a receipt come out of one "
              "shell. Merge tokens resolve here, against "
              "<code>AdminApi::Fixture::Messaging.merge_tokens</code>.",
         cant="Nothing structural. The two things it does not have yet are the "
              "<code>board_*</code> endpoint and a logo on a stable HTTPS path.",
         do="<b>Anything designed goes through here, not Zoho.</b> Send the PSV pitch by hand from "
            "a mailbox and you lose the <code>List-Unsubscribe</code> header, you lose the "
            "per-recipient <code>unsubscribe_url</code>, and you put cold outreach on the same "
            "reputation as the collection codes."),

    dict(k="The system", colour="accent-flow",
         who="Collection codes, statements, approvals — ActionMailer, no human in the loop.",
         tmpl="<b>The shell, as the mailer layout.</b> "
              "<code>app/views/layouts/mailer.html.erb</code> becomes the shell and everything "
              "between the headline block and the footer becomes <code>yield</code>.",
         cant="Nothing. This is the case the markup was written for.",
         do="<b>This is where consistency is actually won.</b> It is the highest volume and the "
            "least negotiable, and it is a code problem rather than a discipline problem — which "
            "is why it is the one to solve first."),
]

EMAIL_ANSWER = dict(
    t="So: one shell for the machines, plain text for the people",
    p="Do not try to make all three render the same HTML — one of them cannot, and forcing it "
      "produces a broken Outlook render nobody tests. Make the two machine surfaces share one "
      "shell and one block library, which is where the volume is and where consistency is "
      "enforceable in code. Let the human surface be plain, carrying the brand through voice and a "
      "signature.<br><br>"
      "<b>If a human needs to send a designed email, the answer is to send it from the Messaging "
      "Centre</b>, not to rebuild the template in Zoho. "
      "<b>Zoho Campaigns</b> — a different product from Zoho Mail — does do templates, merge "
      "fields and unsubscribe handling, and is a legitimate alternative to building outreach in "
      "the admin. But pick one. Running both means two sending reputations, two unsubscribe "
      "lists, and two places a stale figure can come from.")

EMAIL_DNS = dict(
    headline="What the DNS says today, checked 10 November",
    body="The brief's checklist asks for DMARC at <code>p=quarantine</code> or <code>p=reject</code>. "
         "There is no DMARC record at all to tighten — <code>_dmarc.pinnedflow.app</code> returns "
         "nothing — so the first move is to publish one at <code>p=none</code> with a reporting "
         "address, read the reports for a fortnight to find out who is really sending as Pinned, "
         "and only then tighten.",
    rows=[("SPF", "<code>v=spf1 include:zohomail.com ~all</code> — <b>Zoho and nobody else.</b> "
                  "The moment the Rails app sends through SendGrid, Postmark, SES or Mailgun, "
                  "those messages fail SPF. Either route system mail through Zoho's SMTP too, or "
                  "add the provider before the first send — not after."),
          ("DKIM", "Live for Zoho (<code>zmail._domainkey</code>). Any second sending provider "
                   "needs its own selector published."),
          ("DMARC", "<b>Absent.</b> Not <code>p=none</code> — absent. Nothing is being reported, "
                    "so nobody knows what is currently sending as pinnedflow.app."),
          ("Subdomains", "<code>mail.</code>, <code>marketing.</code>, <code>news.</code> and "
                         "<code>send.</code> all return nothing. The three-class separation is a "
                         "plan, not a configuration."),
          ("The trade-off", "SPF naming only Zoho makes Zoho SMTP the cheapest path to "
                            "all-three-pass on day one. It is also the path that makes class "
                            "separation hardest, because one tenant's reputation is shared. "
                            "<b>Worth deciding deliberately rather than by default.</b>")])


EMAIL_CLASSES = [
    dict(k="Transactional", colour="accent-flow",
         ex="Collection code, ready for collection, collected, host statement.",
         unsub="No — an unsubscribe link does not belong on a message somebody needs.",
         frm="<code>Pinned &lt;notifications@pinnedflow.app&gt;</code>",
         dom="<code>mail.pinnedflow.app</code>, never throttled."),
    dict(k="Lifecycle / service", colour="accent-lock",
         ex="A new Pod, a new feature, a change to how something works.",
         unsub="Yes, plus a preferences link.",
         frm="<code>Pinned &lt;notifications@pinnedflow.app&gt;</code>",
         dom="A separate marketing subdomain."),
    dict(k="Prospecting", colour="accent-org",
         ex="PSV operators, cold business senders, the pitch on this site.",
         unsub="Yes, and prominent.",
         frm="<code>Pinned Flow &lt;hello@pinnedflow.app&gt;</code> — <b>monitored, never "
             "<code>noreply@</code></b>.",
         dom="A third subdomain, warmed slowly."),
]

EMAIL_RULES = [
    dict(t="Separate the classes by subdomain, not by good intentions",
         p="A complaint about a cold pitch must not be able to delay the collection-code email "
           "that lets somebody open a Pod. That is the entire reason for the split, and it is a "
           "DNS job rather than a copy job."),
    dict(t="Never noreply@ on a class whose success is a reply",
         p="The pitch ends on <i>“Book a 15-minute walkthrough… or call”</i>. A SACCO manager's "
           "first instinct is to hit reply. Prospecting sends from a mailbox somebody reads."),
    dict(t="The subject line carries the fact — on transactional",
         p="The amount, the date, the decision. <b>This rule is scoped to transactional and it was "
           "not before.</b> Outreach earns its open with a hook instead: <i>“Still on your Nairobi "
           "shelf tonight”</i> carries no fact at all, and is right."),
    dict(t="Name which code it is",
         p="The <b>collection code</b> is read at a counter and is never withheld. The "
           "<b>handover code</b> is given to a runner at a door and is held until what is owed "
           "clears. Never <i>PIN</i> — that is the runner app's device unlock. Never <i>OTP</i> — "
           "that is our word, not theirs."),
    dict(t="Figures come from the live board, pulled the morning you send, and dated",
         p="Never typed by hand, which is how a stale number reaches a customer. No ratings. The "
           "retired 480 / 12,000+ / 4.8 figures stay retired."),
    dict(t="One call to action, and it carries the link",
         p="No gating, no “reply to find out”, no keyword barrier. The address travels with the "
           "call."),
    dict(t="DM Mono is reserved, and in email it is also a signal",
         p="Codes, prices, timestamps and IDs only. In an inbox it is the fastest way a receiver "
           "tells a real Pinned message from a copy of one."),
    dict(t="Flow lane colours only",
         p="<code>#C8005A</code> <code>#C0DB86</code> <code>#7AAF2A</code> <code>#E8520A</code> "
           "<code>#2B2B2B</code>. PinnedOS Blue never appears on a Flow asset."),
    dict(t="UKO WAPI? is rationed",
         p="It belongs to the sign-up message and nowhere else in the sender journey."),
]

EMAIL_MARKUP = [
    ("Tables and inline CSS", "Outlook renders with Word's engine. No flexbox, no grid, no external stylesheet."),
    ("XHTML doctype + the MSO block", "Without it Outlook scales everything by its own DPI."),
    ("The VML <code>&lt;v:roundrect&gt;</code>", "Without it the magenta button is a blue underlined link in Outlook."),
    ("<code>mso-line-height-rule: exactly</code>", "On every text cell, or Outlook ignores line height."),
    ("The hidden preheader div", "The grey line beside the subject. Left empty, clients scrape the first visible text instead."),
    ("Dark mode, and two logos", "Gmail and Apple Mail invert colours on their own and do it badly. Blocks 3 and 4 deliberately do not invert — anthracite and Locker Green are brand grounds, not theme colours."),
    ("DM Sans only renders in Apple Mail and iOS", "Gmail and Outlook fall back to Arial. That is expected. Never set headlines as images to force the font — it costs accessibility and spam score."),
]

EMAIL_FILES = [
    ("email/pinned-email-template.html", "The shell", "→ <code>app/views/layouts/mailer.html.erb</code> in <code>pinned_systemadmin</code>. Everything between the headline block and the footer becomes <code>yield</code>."),
    ("email/pinned-email-blocks.html", "Seven blocks", "→ the Messaging Centre composer. They already use <code>{{…}}</code>, the syntax the composer documents."),
    ("email/psv-pitch.html", "A worked example", "→ one record in <code>AdminApi.messaging.templates</code>, <code>channel: \"email\"</code>, <code>kind: \"promotional\"</code>."),
    ("email/assets/pinned-email-logo-*.png", "The lockup, 2×", "→ a stable HTTPS path on <code>pinnedflow.app</code>. Email clients cannot read a <code>file://</code> path, an asset-pipeline digest URL that changes on deploy, or SVG, which Gmail and Outlook strip."),
]

EMAIL_CHECKLIST = [
    ("Publish a DMARC record", "There is none. Start at <code>p=none</code> with a reporting address, read a fortnight of reports, then tighten to <code>p=quarantine</code>."),
    ("Authorise every sender in SPF", "Today it is Zoho only. Decide whether system mail goes through Zoho SMTP or a provider, and publish the record before the first send."),
    ("Logos on a stable HTTPS path", "Then point <code>{{asset_base}}</code> at the folder."),
    ("<code>List-Unsubscribe</code> and <code>List-Unsubscribe-Post</code>", "On bulk sends. <code>unsubscribe_url</code> must be unique per recipient — a shared link unsubscribes nobody, and Gmail and Yahoo require a unique one for the one-click header."),
    ("A <code>text/plain</code> alternative on every send", "Missing it costs deliverability on its own."),
    ("The <code>board_*</code> endpoint", "A small endpoint or cached read of the <code>/vhost</code> board. Until it exists those four tokens have nothing behind them."),
    ("Render it in five places", "Gmail web, Gmail Android, Apple Mail iOS, Outlook desktop, and Gmail dark mode."),
    ("BIMI is a 2027 item", "The logo beside the subject line needs DMARC enforcement plus a Verified Mark Certificate, which needs a registered trademark and runs about $1,000 a year. Do the DMARC work now for its own sake."),
]
