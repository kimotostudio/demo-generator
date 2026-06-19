---
name: bayesian-sales-learning
description: Plan the future Bayesian / Thompson-sampling learning layer for the salon sales pipeline. Use when designing outcome logging or thinking about optimizing arms. Do NOT optimize before enough logs exist.
---

# Bayesian Sales Learning

**Do NOT optimize before enough logs exist.** Premature Thompson sampling on a handful of sends just
amplifies noise. The v0.1 job is humble: **just log outcomes honestly.** Learning is a later layer, not a
v0.1 blocker.

## Phase 0 (now): just log

Record each lead's journey through the funnel — nothing fancier:
- `sent`, `reply`, `reject`, `interested` (and the no-reply window passing).
- Tag each event with its arm values (below) so the data is analyzable later.
- Keep it append-only and reconcilable with the ledger / Sales Console event log.

That's it for now. No optimization, no auto-selection. Build the dataset first.

## Arms (the levers to learn over, later)

- `category` — ドライヘッドスパ / よもぎ蒸し / リンパ / アロマ / フェイシャル / リラク / ボディケア
- `city` — 久留米 / 八女 / 小郡 / 鳥栖 / 筑後 / Fukuoka core
- `message_variant` — which outreach template lineage
- `demo_style` — which LP design direction
- `lead_source` — where the lead came from
- `send_route` — email / form

## Outcomes

`sent`, `reply`, `positive_reply`, `rejected`, `converted`.

## Beta-binomial initial plan

- Prior: **alpha = 1, beta = 1** (uniform) per arm value.
- **success = positive_reply.**
- **failure = rejected OR no_reply_after_window** (define the window explicitly when logging, e.g. N days;
  an outcome stays open until reply or window expiry).
- Update each arm's Beta posterior as outcomes land. Report posterior means + intervals before acting.

## Thompson sampling (later — NOT a v0.1 blocker)

Thompson sampling over the arms comes **after** there is enough data to be meaningful. It is explicitly not
required for v0.1 and must not gate the manual-send pipeline. When the time comes, sample from each arm's
posterior to pick the next candidate mix — but only once volume justifies it.

Fuller design: `/home/kimoto/projects/sales-console/docs/THOMPSON_SAMPLING_PLAN.md`.

## Hard rails

- Logging/learning never triggers a send. NO auto-send, NO form submit, NO DM, NO phone, NO Gmail/SMTP/API.
- `sent=0` until Yu confirms "sent <lead>"; learning only reads confirmed events.
- Deploy ≠ send. NO git push.
- Math (Beta-binomial, posterior updates, sampling) is **code's job**; arm/outcome definitions and "is there
  enough data yet" judgment is reviewed before acting.
