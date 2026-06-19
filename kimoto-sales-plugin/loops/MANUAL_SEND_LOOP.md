# MANUAL SEND LOOP

Prepare send material for Yu. **The system never sends. Yu sends manually.**

## Input
- `READY` demos from `DEMO_REVIEW_LOOP` and their lead records.

## AI judgment step
- **Select 1–3** best send candidates for this batch.
- **Draft** the outreach copy (honest, anti-hype, signed, with the ignore-this-message line)
  and a **Slack manual-send card** per lead (salon, demo URL, channel, copy).

## Code / safety step
- Confirm **`sent=0`** in the ledger for each candidate (see `safety/LEDGER_POLICY.md`).
- Verify ledger fields are present and the demo URL is real/resolving.
- **No system send** — code only prepares the card; it never submits a form or emails.

## Yu decision step
- **Yu sends manually** (email/form), then confirms the send back to the system.

## Output artifact
- **Manual-send cards** in Slack (1–3), each ready for Yu to copy/send by hand.

## Next loop
- → `REPLY_LOGGING_LOOP` once Yu reports a send and any reply.
