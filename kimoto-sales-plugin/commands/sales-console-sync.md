# Command: sales-console-sync

## Purpose
Sync demo/lead/ledger data into the Sales Console seed/state so the console reflects current reality. Reads demo-generator ledgers + reports and updates the Sales Console seed JSON / export. Local data only, no sending.

## When to use
- After scoring/enrichment/demo builds/ledger updates, when the Sales Console (`/home/kimoto/projects/sales-console`) is stale.

## Required inputs
- demo-generator ledgers (under demo-generator/ledgers/) and recent reports.
- Sales Console seed file: /home/kimoto/projects/sales-console/seed/leads_seed.json.
- `sales-console-ops` skill.

## Steps
1. Read current demo-generator ledgers + latest score/enrich/review/send reports.
2. Read the existing Sales Console seed (leads_seed.json) to know current state.
3. Reconcile: for each lead, merge score, demo URL, verdict, route, freshness, sent status — ledger is source of truth for sent.
4. Update the seed JSON / export with reconciled rows; preserve fields the console owns that the ledger doesn't.
5. Validate JSON (parse-clean, no schema breakage, no duplicate lead_ids).
6. Summarize: leads added / updated / unchanged, and any conflicts left for review.

## Safety rules
- Local data only — no network, no sending, no deploy required.
- Ledger sent status is authoritative; never flip sent during a sync.
- Do not invent leads or fields; only sync what the ledgers/reports contain.

## Outputs
- Updated Sales Console seed JSON / export.
- Sync summary (added/updated/unchanged/conflicts).

## Report path
reports/YYYYMMDD_sales-console-sync.md (under sales-console/reports/)

## Hard stops
- Manual send only — NO auto-send, NO form submit, NO DM, NO phone, NO Gmail/SMTP/API.
- sent=0 stays 0; a sync never sets sent=1.
- Deploy (preview AND public production) is AUTO-allowed and deploy ≠ send; nothing is sent here.
- NO git push.
- Do not edit files outside this task's listed target files (sales-console seed/export + this report). If another file seems necessary, STOP and report instead of editing it.
