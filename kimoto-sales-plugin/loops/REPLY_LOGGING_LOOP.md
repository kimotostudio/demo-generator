# REPLY LOGGING LOOP

Record outcomes after Yu reports a send and any reply.

## Input
- Yu's report: which lead was sent, send route/date, and any reply or rejection text.

## AI judgment step
- **Summarize** the reply and **classify sentiment** (interested / neutral / not-now / reject),
  with a short rationale.

## Code / safety step
- **Append an event-log row** (timestamp, lead_id, action, prev→new status, note).
- Update ledger status; set `sent=1` with `sent_date` / `send_route` / `message_variant`
  **only on Yu's explicit confirmation** (see `safety/LEDGER_POLICY.md`).
- Never silently mutate status; uncertain outcome → mark **unknown** and ask.

## Yu decision step
- **Yu confirms** the outcome (send happened, reply classification, next status).

## Output artifact
- **Updated ledger + event log** reflecting the send and reply.

## Next loop
- → `BAYESIAN_LEARNING_LOOP` (periodically, once enough outcomes accumulate).
