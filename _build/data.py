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

BUILD = 4
UPDATED = "9 October 2026"

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
      trigger="Parcel handed to the runner and scanned",
      timing="At scan", channels=["sms", "in_app"],
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
      trigger="Free storage window elapses (72h)", timing="72h after arrival", channels=["sms", "in_app"],
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

    T(id="C4a", lane="receiver", stage="Waiting", name="Still waiting · rung 1 (24h)",
      trigger="Parcel uncollected 24h after arrival", timing="24h", channels=["sms"],
      status="partial", key="dwell_reminder_24h", source="Map · Receiver 3", hook="Action",
      intent="Neutral. State the facts and the opening hours.",
      old="Your parcel {{code}} is still at {{station}}. Free storage ends in 48 hours. After that: Ksh {{rate}}/hr applies. Your code: {{otp}} Open until: {{closing_time}} Can't make it? Request door delivery: {{track_url}}",
      msgs=[
          ("sms", "Your parcel is still at {{station}}, open until {{closing_time}}.\nCode: {{otp}}\nFree storage until {{deadline}}."),
      ],
      rules=["Rung 1 does not mention the rate. Nothing is being charged yet, so nothing about charging is said.",
             "Retire the 6-hour reminder. It arrives while people are still at work and teaches them we message for no reason."]),

    T(id="C4b", lane="receiver", stage="Waiting", name="Still waiting · rung 2 (48h)",
      trigger="Parcel uncollected 48h after arrival", timing="48h", channels=["sms"],
      status="partial", key="dwell_reminder_48h", source="Map · Receiver 3", hook="Action",
      intent="Specific. Name the deadline and the rate that starts after it.",
      old="Your parcel {{code}} is still at {{station}}. Free storage ends in 24 hours. After that: Ksh {{rate}}/hr applies. Your code: {{otp}} Open until: {{closing_time}} Can't make it? Request door delivery: {{track_url}}",
      msgs=[
          ("sms", "24 hours of free storage left on your parcel at {{station}}.\nCode: {{otp}}\nFrom {{deadline}}: Ksh {{rate}}/hr. Can't come? Door delivery: {{track_url}}"),
      ],
      rules=["Rung 2 is where the escape hatch earns its place. Most door-delivery conversions happen here."]),

    T(id="C4c", lane="receiver", stage="Waiting", name="Storage has started · rung 3 (72h)",
      trigger="The free storage window elapses", timing="72h", channels=["sms"],
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
          ("sms", "Approved — {{hours}} more hours free on your parcel at {{station}}.\nNew deadline: {{deadline}}\nCode: {{otp}}"),
          ("in_app", ("Extended to {{deadline}}", "{{hours}} more hours of free storage at {{station}}. Code {{otp}}.")),
      ],
      rules=["People do not want the decision, they want the new date. Lead with the deadline."]),

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
         rules=["160 GSM-7 characters is one segment. Two segments are allowed when the message carries money, a deadline and an action — never for warmth.",
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
         rules=["The subject line carries the fact — the amount, the date, the decision.",
                "From notifications@pinned.app, display name Pinned.",
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
         p="If there is an alternative — door delivery, redeliver, extend, decline — it appears in the message that creates the problem, not in a later one. The 48-hour dwell reminder converts because the escape hatch is right there."),
    dict(t="Internal words stay internal",
         p="Dwell, batch, OTP, eligibility, heartbeat, float, SLA, vhost. None of these reach a customer or a runner. The customer-facing word is listed beside each one in the glossary."),
]

GLOSSARY = [
    ("dwell", "free storage"), ("batch", "job, or run"), ("OTP", "collection code"),
    ("handover code", "handover code — keep it, runners and hosts use it daily"),
    ("batch eligibility", "offers"), ("heartbeat", "online / offline"),
    ("floated back", "gone back to the job pool"), ("vhost", "your station, your location"),
    ("pod", "pod — it is on the hardware, customers learn it"),
    ("KES / KSh / Ksh", "Ksh, everywhere, no exceptions"),
    ("parcel", "parcel — never 'package', never 'item', never 'shipment'"),
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
                ("—", "Normalise currency to Ksh across all 33 live templates.")]),
    dict(w="Week 2", t="Rewrite what already fires",
         items=[("—", "Replace the body of every live template with the copy in the library. No schema change, no new triggers — it is a content migration against <code>NotificationTemplate</code> keys."),
                ("R7", "Put payout, stop count and distance in the offer title."),
                ("C4a", "Retire the 6-hour dwell reminder; the ladder becomes four rungs."),
                ("H4", "Move the settlement amount into the email subject line.")]),
    dict(w="Week 3", t="Close the map's gaps",
         items=[("R2", "First-run primer — SMS, email and in-app, once ever. The highest-value missing message in the business."),
                ("R3", "Delivery-completed earnings reveal in-app."),
                ("R5 R6", "In-run prompts: running late, loaded at the pod."),
                ("A1a A1b A2 A3 A4", "The five admin interventions. None of them exist today."),
                ("C3", "Receiver delay message."),
                ("H7", "Host-side dwell request — the question behind two answers that already ship.")]),
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
    ("<code>MessageSender</code>", "Sender identity: PINNED for SMS and WhatsApp, notifications@pinned.app for email."),
]
