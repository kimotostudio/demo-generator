# Command: salon-review-demo

## Purpose
Claude harsh review of a built/deployed demo LP to decide send-readiness. Verifies design quality, claim-safety, zero internal labels, and a clean send route, then issues a verdict.

## When to use
- After `salon-build-demo` returns a deliverable + preview/public URL, before any manual-send card is created.

## Required inputs
- Demo LP (local files and/or deployed URL).
- The source candidate row (business, area, route).
- Forbidden-claim list; `personal-salon-frontend-design` + `claim-safe-outreach` skills.

## Steps
1. Inspect hero hierarchy: clear primary message, visual order, no clutter.
2. Verify store identity: correct business name/area, consistent with the real salon, no wrong-salon facts.
3. Check mobile widths (≤375 / 414 / 768): no overflow, tap targets fine, readable.
4. Internal-label / placeholder scan = 0 (no "TODO", "lorem", "{{}}", internal IDs, lead_id leakage).
5. Forbidden-claim scan = 0 (改善/効果/小顔/不眠/自律神経/妊活/脱毛/治る/痛みが取れる/医療的効果/before-after/fake testimonial/guaranteed result/集客アップ保証).
6. Claim-safety judgment: PASS/FAIL with reasons.
7. Confirm send route is sane (email/form preferred; no phone-only, no auto-DM).
8. Assign verdict: READY / FIX_FIRST / HOLD / EXCLUDE, with specific fix instructions if not READY.

## Safety rules
- Be harsh; do not pass 80-point work. Better to FIX_FIRST than ship weak.
- A READY verdict is a quality/safety gate only — it does NOT authorize a send.
- If any claim or secret leak is found in a deployed page: verdict cannot be READY; flag for take-down.

## Outputs
- Review report with per-check pass/fail and quoted issues.
- Verdict (READY / FIX_FIRST / HOLD / EXCLUDE) + fix instructions.

## Report path
reports/YYYYMMDD_salon-review-demo.md (under demo-generator/reports/)

## Hard stops
- Manual send only — NO auto-send, NO form submit, NO DM, NO phone, NO Gmail/SMTP/API.
- sent=0 stays 0; a READY verdict never sets sent.
- Deploy (preview AND public production) is AUTO-allowed and deploy ≠ send.
- NO git push.
- Do not edit files outside this task's listed target files. If another file seems necessary, STOP and report instead of editing it.
