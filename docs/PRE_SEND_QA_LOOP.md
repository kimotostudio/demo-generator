# PRE_SEND_QA_LOOP

The quality gate a personal-salon demo LP passes **before** it can become a manual-send candidate. No send,
no email, no form submit, no DM, no `sent=1` happens in this loop — it ends at "ready for manual-send card".

## Skill requirement
> **Consult `skills/personal-salon-frontend-design/SKILL.md` before Codex modifies any demo UI**, and use its
> §4 QA checklist as the authoritative pre-send QA list. A page that fails the "swap the name" test or any
> claim-safety item is not pre-send ready.

## Loop
1. **Build / revise** the demo per the frontend-design skill (hero-as-thesis, store-as-subject, claim-safe,
   face-free, one signature).
2. **Playwright QA** — screenshot mobile 360 / 375 / 390 / 412 + desktop; capture hero first-view and
   image-performance.
3. **Run the §4 checklist** — store identity visible, category/region correct, hero hierarchy, mobile clean,
   internal labels absent, forbidden claims absent, CTA natural, typography comfortable, image perf acceptable,
   no AI-template smell, noindex present.
4. **Record** results in the QA scores CSV + pre-send ledger; log any unknowns (photo rights, full menu, hours,
   IG recency). Keep `sent=0`.
5. **Verdict** — PASS → eligible for Claude review gate; FAIL → fix instructions back to Codex.

## Hard rails
- Deploy (preview/public) is allowed; **send is not** (Yu-manual). Deploy ≠ send.
- `sent=0` stays until Yu manually sends. No outreach in this loop.
