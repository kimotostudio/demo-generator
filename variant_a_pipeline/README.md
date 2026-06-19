# Variant A salon demo-LP pipeline (v0)

Figma-free, code-template path. Turns a structured salon lead profile into a personalized,
compliance-guarded demo LP using `templates/salon_booking_v2/template.html` (variantA-level quality,
9 blocks, sample/draft labels baked in).

## Why this exists
`auto_generate.py` + `variantA.html` personalize ONLY the brand name — menu/owner/prices/testimonials
are hardcoded, so every demo reads generic and ships fabricated testimonials. `salon_booking_v2` fixed
the template (26 slots, labels) but had **no renderer**. This pipeline is that renderer + the rules
around it (schema, copy rules, image slots, compliance guard, quality checks).

## Usage (safe-local; no network/send/deploy)
```bash
cd demo-generator
python3 variant_a_pipeline/generate_salon_lp.py --all          # render every sample_leads/*.json
python3 variant_a_pipeline/generate_salon_lp.py --profile path/to/profile.json
```
Output: `variant_a_pipeline/generated_demo/<slug>/{index.html, render_meta.json, quality.json}`.
Exit code is nonzero if any hard quality check fails (e.g. a forbidden phrase slipped into copy).

## Files
- `schema/salon_lead_profile.schema.json` — the lead profile contract (Yu's field spec)
- `generate_salon_lp.py` — profile → LP renderer (mapping + copy rules + image slots + guard + checks)
- `copy_rules.md` / `image_assignment_rules.md` / `quality_checklist.md` — the rules
- `sample_leads/*.json` — SYNTHETIC samples (fictional; not scraped)
- `generated_demo/` — rendered samples

## Boundaries
No external outreach, no auto-send, no scraping new leads, no public deploy (noindex draft only after
Yu approval), no paid APIs, no Figma. Unknowns stay `[要確認]`; menus/prices/owner facts/testimonials
are never invented; owner faces are never auto-assigned.
