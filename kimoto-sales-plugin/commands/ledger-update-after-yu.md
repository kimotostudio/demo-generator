# Command: ledger-update-after-yu

## Purpose
Update the pre-send ledger ONLY after Yu explicitly reports an outcome (he sent / got a reply / was rejected). This is the single place sent=1 may ever be set, and only on an explicit "sent <lead>".

## When to use
- Yu says in-session: "sent <lead>", "<lead> replied", "<lead> positive", or "<lead> rejected".
- Never run speculatively or to "catch up" the ledger without Yu's words.

## Required inputs
- Yu's explicit statement (which lead, what outcome).
- The salon pre-send ledger under demo-generator/ledgers/.
- Send route + message variant used (for a sent event).

## Steps
1. Parse Yu's statement into: lead_id, action (sent / reply / positive_reply / rejected), note.
2. Append an event-log row: timestamp, lead_id, action, prev_status → new_status, note.
3. ONLY on explicit "sent <lead>": set sent=1, sent_date, send_route, message_variant for that lead.
4. For reply/positive_reply/rejected: update status fields, leave sent as-is (must already be 1).
5. Validate: no silent sent=1, no duplicate event rows, lead_id exists.
6. Summarize the applied change (prev→new) for confirmation.

## Safety rules
- NEVER set sent=1 without Yu's explicit "sent <lead>" — no inference, no batch defaulting.
- Append-only event log; do not rewrite history.
- One lead per explicit statement; if ambiguous, STOP and ask Yu which lead.

## Outputs
- Appended event-log row(s).
- Updated lead status fields (sent/sent_date/route/variant only on explicit sent).
- Change summary (prev→new).

## Report path
reports/YYYYMMDD_ledger-update-after-yu.md (under demo-generator/reports/)

## Hard stops
- Manual send only — NO auto-send, NO form submit, NO DM, NO phone, NO Gmail/SMTP/API.
- sent stays 0 until Yu explicitly says "sent <lead>"; never silently mutate sent=1.
- Deploy (preview AND public production) is AUTO-allowed and deploy ≠ send.
- NO git push.
- Do not edit files outside this task's listed target files (the ledger + this report). If another file seems necessary, STOP and report instead of editing it.
