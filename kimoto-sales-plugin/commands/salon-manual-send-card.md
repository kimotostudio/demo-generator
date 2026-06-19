# Command: salon-manual-send-card

## Purpose
Create the Slack manual-send card plus the final outreach copy (standard message filled in) for a READY lead, so Yu can review and send manually in one glance. This command NEVER sends.

## When to use
- A demo LP has passed `salon-review-demo` (READY) and the lead has a clear email/form send route.

## Required inputs
- READY lead row (business, source URL, demo URL, category, area, freshness, send route).
- Review verdict + claim-safety status.
- Standard outreach message template (`claim-safe-outreach` skill).

## Steps
1. Confirm verdict = READY and send route is email or contact form (no phone, no auto-DM).
2. Fill the standard message: signature 木許 only (never full name), no phone, no birth date, email kimoto.studio21@gmail.com; never the phrase "興味ありと返信".
3. Compose 件名 (subject) + 本文 (body) — honest, anti-hype, claim-safe; include the ignore-this-message line.
4. Build the Slack card with fields: business, source URL, demo URL, category/area, freshness, send route, safety status, 件名+本文, Yu manual action, sent=0 confirmation.
5. Re-scan the filled copy for forbidden claims and secret leakage = 0.
6. Present the card for Yu's manual send. Do not submit anything.

## Safety rules
- This produces a CARD and COPY only. Yu sends manually; the system never sends.
- Email/form route preferred; phone and auto-DM are not send routes here.
- Signature/identity rules are mandatory: 木許 only, kimoto.studio21@gmail.com, no phone/birth date, no "興味ありと返信".

## Outputs
- Slack manual-send card (text block) with all fields.
- Final 件名 + 本文 outreach copy.
- sent=0 confirmation line.

## Report path
reports/YYYYMMDD_salon-manual-send-card.md (under demo-generator/reports/)

## Hard stops
- Manual send only — NO auto-send, NO form submit, NO DM, NO phone, NO Gmail/SMTP/API.
- sent=0 stays 0 until Yu explicitly says "sent <lead>".
- Deploy (preview AND public production) is AUTO-allowed and deploy ≠ send.
- NO git push.
- Do not edit files outside this task's listed target files. If another file seems necessary, STOP and report instead of editing it.
