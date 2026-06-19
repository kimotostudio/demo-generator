# SLACK_MANUAL_SEND_CARD_LOOP

The final step of the demo-LP loop: turn a review-passed, deployed demo into a **manual-send card** that lets
Yu send with minimal thinking. The system never sends — it prepares; Yu decides.

## Skill requirement
> A card is only produced for a page that passed the Claude review gate, which reviews against
> `skills/personal-salon-frontend-design/SKILL.md`. If the UI was modified, the skill was consulted first.

## Card contents (one card per recommended candidate)
- business name · category · region
- source URL (verified) · public demo URL (noindex, reachable)
- recommended **send route** — email / contact-form preferred; **not** phone, **not** automatic DM
- freshness / active evidence (and honest unknowns)
- safety status (claim-safe PASS, internal-labels absent)
- final 件名 + 本文 (ready to paste; sender = KIMOTO STUDIO / 木許 / kimoto.studio21@gmail.com)
- explicit **Yu manual action**
- `sent=0` confirmation

## Loop
1. Confirm the page passed gate 2 and is deployed.
2. Verify send route (prefer email/form); fill the standard message with 屋号 + lead.
3. Update the pre-send ledger: `Yu_review_status = manual_send_ready` (or `review_before_send`),
   `outreach_draft_created = 1`, demo_url + send_route recorded, **`sent = 0`**.
4. Post a compact Slack summary + one card per candidate.
5. **Stop.** Yu sends manually. Only when Yu says "sent <lead>" → set `sent=1` + sent_date + send_route +
   message_version. No automatic follow-up.

## Hard rails
- No auto-send / auto-post. Send/email/form submit/DM/`sent=1` are Yu-manual in the current phase.
- Never expose webhook URLs/tokens/secrets in any notification.
