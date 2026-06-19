# Command: salon-send-day

## Purpose
Run a manual-send validation day: select 1–3 READY leads, prepare exact Yu actions and Slack cards so Yu can send a small honest batch by hand. Do not force 3. sent stays 0 until Yu confirms.

## When to use
- There are one or more READY leads with manual-send cards available and Yu wants to do a send session.

## Required inputs
- Pool of READY leads (verdict + cards from `salon-review-demo` / `salon-manual-send-card`).
- Send-route, freshness, claim-risk, and rank (A first) per lead.
- `manual-send-validation` skill.

## Steps
1. Filter the pool to READY leads with an email or contact-form route (no phone-only, no auto-DM).
2. Rank: A first, then fresher, then lower claim risk.
3. Pick 1–3 (top of the ranked list). If only 1 qualifies, pick 1 — do NOT pad to 3.
4. For each pick, confirm/produce the manual-send card (件名+本文, demo URL, route, safety status, sent=0).
5. Write the exact Yu action list: which lead, which route, copy to paste, where to send.
6. Send a compact Slack summary of today's manual-send batch (cards + actions). STOP for Yu.

## Safety rules
- Selection and card prep only; the system never sends. Yu performs every send by hand.
- Respect daily restraint: small honest batch, quality over volume.
- Captcha/login-gated/broken forms are not eligible — route to manual list and skip.

## Outputs
- Today's 1–3 selected leads with cards.
- Exact Yu manual action list.
- Compact Slack batch summary.

## Report path
reports/YYYYMMDD_salon-send-day.md (under demo-generator/reports/)

## Hard stops
- Manual send only — NO auto-send, NO form submit, NO DM, NO phone, NO Gmail/SMTP/API.
- sent=0 stays 0 until Yu explicitly says "sent <lead>".
- Deploy (preview AND public production) is AUTO-allowed and deploy ≠ send.
- NO git push.
- Do not edit files outside this task's listed target files. If another file seems necessary, STOP and report instead of editing it.
