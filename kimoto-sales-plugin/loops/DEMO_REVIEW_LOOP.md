# DEMO REVIEW LOOP

Claude reviews the built demo harshly before it can become send-ready.

## Input
- The deployed demo URL + diff/preview from `DEMO_BUILD_LOOP`, and the source lead record.

## AI judgment step
- **Harsh Claude review** against the personal-salon-frontend-design skill and a QA checklist:
  brand fit, copy quality, atmosphere-not-effects framing, layout, mobile, polish.
- Reject 80-point work — only genuinely send-worthy demos pass.

## Code / safety step
- **Re-run** the forbidden-claim scan and internal-label scan on the live/visitor HTML.
- Confirm secret-free and that the URL actually resolves (no fabricated URL).

## Yu decision step
- **Yu is informed** of the verdict. Yu does not need to review every demo, but the verdict
  and any HOLD/EXCLUDE reasoning are surfaced.

## Output artifact
- A **verdict**: `READY` / `FIX` / `HOLD` / `EXCLUDE`, with reasons and fix instructions.

## Next loop
- `READY` → `MANUAL_SEND_LOOP`.
- `FIX` → back to `DEMO_BUILD_LOOP` with fix instructions.
- `HOLD` / `EXCLUDE` → park or drop the lead (logged).
