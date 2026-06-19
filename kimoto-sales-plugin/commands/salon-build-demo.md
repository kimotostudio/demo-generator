# Command: salon-build-demo

## Purpose
Build a claim-safe demo LP for one A-rated salon candidate. Codex is the worker: consult the `personal-salon-frontend-design` skill FIRST, produce a design plan for Claude review, then build and QA. Deploy (preview or public) is allowed; sending is not.

## When to use
- An A candidate (post score/enrich) is selected for a demo LP to show what KIMOTO STUDIO can deliver.

## Required inputs
- The A candidate row (business, area, source URL, menu, route, claim_risk).
- `personal-salon-frontend-design` skill (consult before building).
- Forbidden-claim list and claim-safe copy guidance.

## Steps
1. Read `personal-salon-frontend-design` skill FIRST; note layout/hierarchy/mobile rules.
2. Draft a short design plan (hero, store identity, sections, send route placement) → submit to Claude for review BEFORE building.
3. On Claude approval, build the demo LP: hero hierarchy, store identity, claim-safe copy, mobile-first.
4. Use only verifiable facts about the salon; no fabricated testimonials, no face/before-after imagery, no invented results.
5. Run QA: forbidden-claim scan = 0, internal-label/placeholder scan = 0, secret scan = 0, mobile widths (≤375 / 414 / 768) render clean.
6. Optionally deploy a preview or public production build (AUTO-allowed). Record the URL.
7. Hand the deliverable + diff + preview URL + QA results back to Claude for `salon-review-demo`.

## Safety rules
- Claim-safe: none of 改善/効果/小顔/不眠/自律神経/妊活/脱毛/治る/痛みが取れる/医療的効果/before-after/fake testimonial/guaranteed result/集客アップ保証.
- Face-free; no fabricated facts, reviews, or stats.
- Secret-free: no .env/tokens/webhooks in any built or deployed file.
- Deploy ≠ send: deploying (even publicly) does NOT contact the salon.

## Outputs
- Demo LP files in the demo-generator output dir.
- Deploy URL (preview or public), if deployed.
- QA report (claim/internal-label/secret scans + mobile check).

## Report path
reports/YYYYMMDD_salon-build-demo.md (under demo-generator/reports/)

## Hard stops
- Manual send only — NO auto-send, NO form submit, NO DM, NO phone, NO Gmail/SMTP/API.
- sent=0 stays 0; building/deploying never sets sent.
- Deploy (preview AND public production) is AUTO-allowed and deploy ≠ send.
- NO git push.
- Do not edit files outside this task's listed target files. If another file seems necessary, STOP and report instead of editing it.
