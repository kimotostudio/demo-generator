# KIMOTO STUDIO Sales Plugin / Ops Kit

An **internal working structure** for running the Personal Salon AI Sales Factory with Claude Code + Codex —
so lead discovery, demo build, demo review, manual send, the Sales Console, and Bayesian learning can be run
with short, stable commands instead of long one-off prompts each time.

This is **not** a public package and **not** an external plugin release. It is a set of markdown skills,
commands, safety gates, and loop docs that Claude/Codex read to stay consistent and safe.

## What this kit is
- `commands/` — reusable task prompts (the "verbs": score, enrich, build, review, card, send-day, sync, ledger, bayes).
- `skills/` — judgment guidance (the "how to think well": discovery, frontend-design, claim-safe outreach, validation, console ops, learning).
- `safety/` — the hard gates (`HARD_BOUNDARIES`, `FORBIDDEN_CLAIMS`, `SEND_POLICY`, `LEDGER_POLICY`).
- `loops/` — the end-to-end flow, one doc per stage, each chaining to the next.
- `plugin_manifest.md` — the index of everything above.

## How it relates to the rest of the system
- **demo-generator** (this repo) builds and deploys the claim-safe demo LPs. The canonical
  `personal-salon-frontend-design` skill lives at `demo-generator/skills/...`; the plugin bundles a synced copy.
- **Sales Console** (`/home/kimoto/projects/sales-console`) is the cockpit that manages leads, statuses, outreach
  copy, the event log, and (later) Thompson-sampling logs. The kit's `sales-console-ops` skill +
  `sales-console-sync` / `ledger-update-after-yu` commands govern how data flows in and out.
- **Slack** delivers manual-send cards. **Yu** sends manually. The ledger records `sent`/`reply` only after Yu confirms.

## When to use each command
- After Manus/lead research → `salon-score-leads`, then `salon-enrich-leads` for thin candidates.
- Have an A lead → `salon-build-demo` (Codex builds) → `salon-review-demo` (Claude reviews).
- Demo passes review → `salon-manual-send-card`; on a validation day → `salon-send-day` (pick 1–3).
- Keeping the cockpit current → `sales-console-sync`; after Yu acts → `ledger-update-after-yu`.
- Enough outcomes logged → `bayes-update-plan`.

## When to use each skill
- Finding leads → `local-salon-lead-discovery`. Building/revising a demo → `personal-salon-frontend-design`.
- Writing outreach → `claim-safe-outreach`. Running a send day → `manual-send-validation`.
- Operating the Console → `sales-console-ops`. Thinking about optimization → `bayesian-sales-learning`.

## What is never allowed (see `safety/HARD_BOUNDARIES.md`)
auto-send · form submit · DM · phone · Gmail/SMTP/API · marking `sent=1` before Yu confirms · fabricated URLs ·
fake testimonials · before/after · medical/beauty efficacy claims · git push without Yu.
Deploy (preview AND public production) **is** allowed/AUTO — deploying a demo does not contact anyone (deploy ≠ send).

## Recommended daily workflow
1. Check the Sales Console / daily runner output.
2. Enrich/score leads if the queue is thin (`salon-enrich-leads` / `salon-score-leads`).
3. Review the demo queue (`salon-review-demo`).
4. Pick 1–3 manual sends (`salon-send-day` → `salon-manual-send-card`).
5. **Yu sends manually** (email/form; no phone, no auto-DM).
6. Update the ledger after Yu confirms (`ledger-update-after-yu`; `sent=0` until then).
7. Log replies/rejections as they come (`REPLY_LOGGING_LOOP`).
8. Periodically summarize learning (`bayes-update-plan`).

## Anti-overbuild note
Keep it lean. These are working docs, not a framework. Add a command/skill only when a real, repeated need
appears. The point is fewer long prompts and steadier safety — not more structure.
