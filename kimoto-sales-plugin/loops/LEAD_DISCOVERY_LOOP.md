# LEAD DISCOVERY LOOP

Discover and score personal-salon leads worth building a demo for.

## Input
- Target region/category hints, existing ledger (for dedup), suppression list.
- Seed sources (search results, directories, Yu-named targets).

## AI judgment step
- Seed candidate salons, then **enrich** (read their public site/social for fit signals).
- **Classify** demo-fit: A (strong demo candidate) / B (maybe) / C (skip), with a short reason.
- Judge atmosphere/brand to estimate how compelling a claim-safe demo would be.

## Code / safety step
- **Dedup** against the ledger by canonical name/URL/phone.
- **Suppression** scan: drop anyone on the do-not-contact / already-engaged list.
- **Normalize** fields (name, region, category, URL, contact channel) to ledger schema.
- No live form/contact actions — discovery is read-only.

## Yu decision step
- Yu picks the **region/category** focus or **approves the seed set** before enrichment scales.

## Output artifact
- A **scored CSV/JSON** of leads with fit grade, reason, contact channel, dedup/suppression flags.

## Next loop
- → `DEMO_BUILD_LOOP` for each approved **A** lead.
