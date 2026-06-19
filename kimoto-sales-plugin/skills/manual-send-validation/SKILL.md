---
name: manual-send-validation
description: Run a manual-send validation day — pick 1–3 demo candidates, verify them, and prepare Yu to send by hand. The goal is safe channel validation, not sales. Manual send only.
---

# Manual Send Validation

The first goal is **NOT sales.** It is **safe market contact** — validating that the channel works
(messages land, demos open, owners can reply) without any automation risk. Treat each send as an
experiment in the channel, not a deal to close.

## The validation day procedure

1. **Pick only 1–3 candidates.** Small, deliberate batch. Quality over volume. Prefer A leads; a strong B
   only if Yu wants it reviewed.
2. **Confirm freshness.** Re-check the lead is still active (recent IG/listing activity, reservation route
   still live). A stale salon is dropped — don't send to a dead shop.
3. **Open the demo on a smartphone.** Owners read on mobile. Check the real phone view: hero, name, mobile
   layout, no overflow, tap targets and CTA clean. If it looks wrong on a phone, fix before sending.
4. **Verify source fidelity.** Store name, category, and area are correct; the demo actually matches the
   real salon (right category cues, honest framing, claim-safe). If the demo doesn't represent THIS salon,
   stop and fix — do not send a mismatched page.
5. **Copy the message.** Use the claim-safe standard message with `{business_name}` and `{demo_url}` filled
   correctly. No criticism tone, no "興味ありと返信", signature 木許 only.
6. **Yu sends manually.** Yu sends via email or the salon's contact form, by hand. The system never sends.
7. **Update the ledger ONLY after Yu says "sent <lead>".** Until that confirmation, `sent=0`.

## Route preferences

- Prefer **email / form** routes.
- **Do not** recommend phone. **Do not** recommend automatic DM. DM only if Yu explicitly chooses it for a
  specific lead.

## Hard rails

- **Manual send only.** NO auto-send, NO form submit by the system, NO DM, NO phone, NO Gmail/SMTP/API.
- `sent=0` until Yu explicitly confirms "sent <lead>"; only then is the ledger updated.
- Deploy (preview AND public production) is AUTO-allowed; **deploy ≠ send.** Opening/deploying the demo
  does not contact the salon.
- NO git push.

## What "done" for the day looks like

1–3 verified candidates, each with: a fresh active lead, a phone-checked demo that matches the real salon,
and a correctly filled message ready for Yu. Nothing is marked sent until Yu confirms. The day succeeds if
the channel was exercised safely — sales are a later goal.
