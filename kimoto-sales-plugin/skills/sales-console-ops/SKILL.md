---
name: sales-console-ops
description: Operate the Sales Console — a cockpit for managing salon leads, status, outreach copy, demo/source links, and the event log. It is NOT a sender. Use when working in the leads/outreach console.
---

# Sales Console Ops

The Sales Console is a **COCKPIT, not a sender.** It helps Yu see and manage leads, copy outreach, open
demos, and track status — but it never contacts anyone. Every "send" action is a *status change*, not a
real message.

App location: `/home/kimoto/projects/sales-console`.

## What the console does

- **Status management.** Each lead carries one status:
  `pending` → `manual_ready` → `sent` → `replied` → `interested` / `rejected` / `hold` / `excluded`.
  Statuses are advanced **manually** by Yu (or by a confirmed event), never auto-progressed by sending.
- **Copy outreach.** One-click copy of the claim-safe message (business name + demo URL filled) so Yu can
  paste it into email/form.
- **Open demo / source.** Jump to the deployed demo LP and to the lead's source (IG/listing/site) to verify
  fidelity before sending.
- **Mark sent / replied / rejected MANUALLY.** Yu sets these by hand. **"Mark sent" only changes local
  status — it does NOT perform a real send.**
- **Event log.** Append-only record of status changes and notes (who/what/when) for audit and later analysis.
- **Recommendation panel.** Surfaces suggested next candidates / actions — advisory only, Yu decides.

## v0.1 boundaries

- **NO Gmail / API / form automation in v0.1.** The console does not send email, submit forms, DM, or call
  any messaging API. It is a viewer + status tracker + copy helper.
- Manual send only; `sent=0` until Yu explicitly confirms "sent <lead>" and marks it.
- Deploy (preview AND public production) is AUTO-allowed; **deploy ≠ send.** Opening a demo from the console
  does not contact the salon.
- NO git push from console actions.

## Data & sync

- The console is the working surface; the **ledger** (`sent`/`reply` events) and **reports** are the system
  of record.
- **Sync with ledger and reports later** — keep console status and the ledger reconcilable. When Yu marks a
  lead `sent`/`replied`/`rejected`, that maps to a ledger event; reconcile so the two never silently diverge.
- The append-only event log is the bridge: it captures every manual status change for later ledger/report sync
  and for the future Bayesian learning layer.

## Hard rails

- Console = cockpit, never a sender. NO auto-send, NO form submit, NO DM, NO phone, NO Gmail/SMTP/API.
- "Mark sent" = local status only; real sending stays Yu-manual outside the console.
- Deploy ≠ send. NO git push.
