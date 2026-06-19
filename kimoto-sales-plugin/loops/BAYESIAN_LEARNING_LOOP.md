# BAYESIAN LEARNING LOOP

Periodically summarize outcomes and propose refined targeting.

## Input
- Ledger + event-log history: sends, replies, sentiment, per-segment outcomes.

## AI judgment step
- **Propose** what is working: which region/category/message variant ("arms") draw better
  replies, and what to try next. Proposals only — not auto-applied.

## Code / safety step
- **Aggregate counts per arm** (sends, replies, positive replies) deterministically in code.
- Keep the math auditable and reproducible.
- **Note:** Thompson sampling / full Bayesian bandit math is **future, not v0.1**. v0.1 is
  simple per-arm counts and rates.

## Yu decision step
- **Yu decides** any strategy change (shift targeting, retire a variant, adjust focus).

## Output artifact
- A **learning summary** (per-arm counts/rates + proposed adjustments).

## Next loop
- → back to `LEAD_DISCOVERY_LOOP` with refined region/category/message targeting.
