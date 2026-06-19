---
name: local-salon-lead-discovery
description: Find active, owner-led local personal salons suitable for demo-first outreach. Use when sourcing/enriching/classifying new salon leads for the KIMOTO STUDIO sales pipeline.
---

# Local Salon Lead Discovery

The job: find **active, owner-led, local personal salons** that are a good fit for demo-first outreach.
Quality over volume — one strong A lead beats ten weak ones.

**Best lead profile:** active local owner-led salon + a real reservation route + visible atmosphere
(photos/IG that convey the space) + weak self-presentation (the page undersells the shop) + low claim risk.
That combination means a demo LP will *visibly* help and the owner will feel understood.

---

## Use AI judgment aggressively for

This is judgment-heavy discovery work — lean on reasoning, not rigid rules:
- **Seed URL discovery** — surfacing candidate salons from search, maps, portals, IG.
- **Enrichment** — reading the Instagram / portal listing / official site to understand the shop:
  category, area, owner-led vs chain, activity/recency, atmosphere, reservation route, claim risk.
- **A/B/C classification** — judging demo-readiness from the enriched picture.
- **Demo-fit reasoning** — would a claim-safe demo LP plausibly help THIS salon? Is there a real route to
  reach the owner?
- **Salvage of B candidates** — a promising-but-incomplete lead: decide what one piece of enrichment would
  move it to A, or flag it for Yu review.

## Preferred categories

ドライヘッドスパ, よもぎ蒸し, リンパ, アロマ, フェイシャル, リラク, ボディケア.

## Preferred areas

久留米, 八女, 小郡, 鳥栖, 筑後, and the nearby Fukuoka core.

## Exclude (not suitable — record as Exclude, do not enrich)

- spiritual-first, 占い, タロット, 霊視, レイキ講座
- 治療院, 整骨院, 鍼灸, クリニック, 美容医療 (medical / quasi-medical)
- 痩身メイン, 小顔効果メイン, 妊活効果メイン, 体質改善メイン (efficacy-led — high claim risk)
- まつげ主体, school / 講座主体
- chain / franchise (not owner-led)
- inactive / stale (no recent posts, dead listing)
- no contact route (no form/email/IG DM/booking link the owner controls)

---

## A / B / C / Exclude

- **A — demo-ready seed.** Active, owner-led, clear category + area, real reservation route, atmosphere
  visible, low claim risk. Ready to brief a demo LP.
- **B — promising but needs enrichment / Yu review.** Fits the profile but a key fact is missing or
  ambiguous (recency unclear, contact route uncertain, claim risk borderline). Note exactly what's missing.
- **C — record only.** Real salon, logged for the corpus, but not actionable now (weak fit, low priority).
- **Exclude — not suitable.** Hits an exclusion above; record the reason, do not pursue.

Default conservatively: if claim risk or owner-led status is genuinely unclear, hold at B for Yu review
rather than promoting to A.

---

## Code vs judgment

- **Python / code does:** dedup (normalize names/URLs, collapse duplicates), normalization (area/category
  canonicalization), suppression scan (already-contacted / excluded / blocklist), schema validation, and
  writing candidate rows to the lead store. Deterministic, repeatable bookkeeping.
- **AI does:** the discovery and classification *reasoning* — finding seeds, reading IG/portals/sites,
  judging fit, assigning A/B/C/Exclude with a one-line rationale. Judgment that a script can't fake.

Run the suppression/dedup scan BEFORE classifying so you never spend judgment on a lead already handled.

---

## Hard rails (every cycle)

- This skill **discovers and classifies only** — it never contacts anyone.
- NO auto-send, NO form submit, NO DM, NO phone, NO Gmail/SMTP/API.
- `sent=0` until Yu explicitly says "sent <lead>".
- Deploy (preview AND public production) is AUTO-allowed; deploy ≠ send. Discovery does not deploy.
- NO git push. NO bypassing captcha / bot protections during any lookup.
- If search engines return 403/429/captcha: STOP live searching, report WARNING, do not retry repeatedly.

## Output per lead

`business_name · category · area · A/B/C/Exclude · reservation route · claim-risk note ·
one-line rationale · source URL(s)`. B leads must state the single missing piece. Excluded leads must
state the exclusion reason.
