# Command: salon-enrich-leads

## Purpose
Enrich IG-only or portal-only B/C candidates so they can be re-scored or promoted: gather freshness (last IG post), menu, reservation/contact route, and claim risk — marking anything unknown honestly.

## When to use
- After `salon-score-leads` leaves B/C candidates that are thin (IG-only, portal-only) and need more signal before a demo build or send decision.

## Required inputs
- B/C candidate list from the scored leads file (lead_id, business, area, source URL/handle).
- `local-salon-lead-discovery` and `claim-safe-outreach` skills for judgment.

## Steps
1. For each candidate, identify the public source already on file (IG handle, portal page, site URL). Do not hunt new identities.
2. Collect freshness: last visible IG post date / activity signal. If not determinable, mark `freshness=unknown`.
3. Collect menu/service summary and reservation/contact route (email / contact form / portal DM). Mark each `unknown` if not clearly present.
4. Assess claim risk: scan visible copy for forbidden claims (改善/効果/小顔/不眠/自律神経/妊活/脱毛/治る/痛みが取れる/医療的効果/before-after/集客アップ保証). Note risk level + any flagged phrase.
5. Write enriched rows back to the leads file (new columns: freshness, menu, route, claim_risk, enrich_notes).
6. Suggest re-score deltas (B→A, C→B, C→Exclude) with reasons — proposal only; re-scoring runs via `salon-score-leads`.

## Safety rules
- NEVER fabricate URLs, handles, dates, menus, or contacts. "unknown" is a valid, preferred value.
- Read-only public info; no login-gated scraping, no captcha bypass, no DMs.
- Enrichment does not authorize contact.

## Outputs
- Enriched leads file (CSV/JSON) with freshness/menu/route/claim_risk/notes.
- Re-score proposal list (delta + reason).

## Report path
reports/YYYYMMDD_salon-enrich-leads.md (under demo-generator/reports/)

## Hard stops
- Manual send only — NO auto-send, NO form submit, NO DM, NO phone, NO Gmail/SMTP/API.
- sent=0 stays 0.
- Deploy (preview AND public production) is AUTO-allowed and deploy ≠ send; nothing is deployed here.
- NO git push.
- Do not edit files outside this task's listed target files. If another file seems necessary, STOP and report instead of editing it.
