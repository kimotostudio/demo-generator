# DEMO BUILD LOOP

Build a claim-safe demo LP from an A-grade lead.

## Input
- One A-grade lead from `LEAD_DISCOVERY_LOOP` (salon name, brand, source material, assets).

## AI judgment step
- AI/Codex builds the demo per the **personal-salon-frontend-design skill**.
- Translate source material into atmosphere/experience copy (never asserted effects).
- Choose layout, imagery direction, and tone that fit the salon's brand.

## Code / safety step
- Run the **forbidden-claim scan** (see `safety/FORBIDDEN_CLAIMS.md`) on visitor HTML.
- Run the **internal-label scan** (no internal labels, lead IDs, grades, or notes leak to the page).
- Secret-free check: no .env / tokens / webhooks in deployed files.

## Yu decision step
- **Yu is not required to build.** Codex builds safe-local; no Yu gate to construct or deploy.

## Output artifact
- A **deployed demo URL** (preview or public production — deploy is AUTO/allowed; deploy ≠ send).

## Next loop
- → `DEMO_REVIEW_LOOP` for Claude's harsh review.
