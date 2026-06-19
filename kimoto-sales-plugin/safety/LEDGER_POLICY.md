# LEDGER POLICY

The ledger is the single source of truth for lead status. It must never lie about whether a
message was sent.

## Core rules

- **`sent=0` until Yu confirms** a manual send. No code path sets `sent=1` on its own.
- **An event log is REQUIRED for every status change.** Each event records:
  - `timestamp`
  - `lead_id`
  - `action`
  - `prev_status → new_status`
  - `note`
- **Never silently mutate `sent=1`.** Any flip to sent must be traceable to a Yu confirmation
  and logged as an event.
- **`sent=1` only on Yu's explicit "sent <lead>"**, recorded with:
  - `sent_date`
  - `send_route` (email / form)
  - `message_variant`

## Integrity

- Status changes go through the event log first, then update the ledger row. No direct,
  unlogged edits.
- The event log is append-only. Corrections are new events, never overwrites.
- If a status is uncertain (e.g. Yu reports a send ambiguously), mark it **unknown** and ask —
  never guess `sent=1`.
