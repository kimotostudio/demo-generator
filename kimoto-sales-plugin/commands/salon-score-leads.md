# Command: salon-score-leads

## Purpose
After Manus/lead research produces a raw candidate list, score each lead A / B / C / Exclude using AI judgment per the `local-salon-lead-discovery` skill. Produces a clean, deduped, scored list ready for enrichment or demo-build selection.

## When to use
- A new batch of raw salon leads (CSV/JSON/list) has arrived from Manus, Claude, or manual research.
- Before any enrichment or demo build — scoring is the first gate.

## Required inputs
- Raw lead list/CSV/JSON (business name, area, source URL, IG/portal handle, any contact route).
- Current suppression list / already-contacted ledger (to avoid re-scoring contacted leads).
- Forbidden-claim / forbidden-category reference (medical/effect claims).

## Steps
1. Load raw leads; normalize fields (name, area, source URL, route) via code. Trim, lowercase keys, fix encoding.
2. Dedupe (code): collapse by business name + area + source URL; keep the richest row.
3. Suppression / forbidden-category exclude: drop leads already in the ledger, and any whose category implies forbidden claims (改善/効果/小顔/不眠/自律神経/妊活/脱毛/治る/痛みが取れる/医療的効果/集客アップ保証 etc.) — mark `Exclude` with reason.
4. Classify remaining as A / B / C with a one-line reason each (AI judgment, `local-salon-lead-discovery` skill): A = strong fit + reachable + low claim risk; B = decent but needs enrichment; C = weak/uncertain.
5. Write scored CSV/JSON with columns: lead_id, business, area, source_url, route, score, reason, claim_risk.
6. Summarize counts: raw / dedup / excluded / A / B / C.

## Safety rules
- Local data only. No browser automation, no contacting anyone, no form opens.
- Never fabricate contact routes or URLs — leave unknown fields blank/"unknown".
- Scoring is judgment, not promotion to send. A score never authorizes outreach.

## Outputs
- Scored leads file (CSV + JSON) under demo-generator working dir.
- Exclude log with reasons.
- Count summary (raw/dedup/excluded/A/B/C).

## Report path
reports/YYYYMMDD_salon-score-leads.md (under demo-generator/reports/)

## Hard stops
- Manual send only — NO auto-send, NO form submit, NO DM, NO phone, NO Gmail/SMTP/API.
- sent=0 stays 0; scoring never sets sent.
- Deploy (preview AND public production) is AUTO-allowed and deploy ≠ send; nothing is deployed here.
- NO git push.
- Do not edit files outside this task's listed target files. If another file seems necessary, STOP and report instead of editing it.
