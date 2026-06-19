# salon_editorial_variant — APPROVED Sample-LP TEMPLATE BASELINE (Yu, 2026-06-18)

**Status: TEMPLATE BASELINE (approved).** Yu formally approved Lea v8 as the demo-generator individual-salon
Sample-LP template baseline on 2026-06-18. This **supersedes `salon_pro_v3` (Warm Natural, approved 2026-06-17)**
as the salon demo standard. Older templates (salon_pro_v3, salon_booking_v1/v2, variantA–F) are retained as
references only.

Canonical config: `real_profiles/lea.json` (Lea v8) — the reference build of this template.

## Approved quality (Claude harsh review, v8)
Sample-LP Quality **93.5/100** · UI softness **9/10** · Typography comfort **9/10** · CTA warmth **9/10** ·
remaining discomfort 1 (residual mincho formality — intentional identity). Reads 「静かだけど、相談しやすい」.

## Non-regression invariants (do NOT break in future edits)
- Editorial, image-led, calm; **face-free** imagery (no auto owner/client faces).
- Light fresh hero; **Latin serif** for the "Lea"/brand mark; **light Shippori-Mincho** JP headings + readable sans body.
- **Soft warm rounded surface blocks** for menu/flow/access (NOT hairline-rule tables, NOT cheap card UI).
- **Warm pill CTA** (muted-rose, soft, small arrow) — never a cold text-link, never an ad button; reservation methods de-boxed.
- Honesty: clearly-labeled SAMPLE (subtle top note + bottom "このデモについて" layer); **no fabricated** menu*/owner/
  testimonials/before-after; **no medical/efficacy** copy. Forbidden-phrase scanner must stay 0
  (効果保証/改善/小顔/小顔効果/美白/治る/実感/before-after/集客/成果保証/必ず/癒し/至福/極上 …).
  *Sample menu prices are SAMPLE content for the template only; a real send must use the salon's real menu.
- Robust without JS + with missing data; mobile-first (verified 360/375/390/412).

## Ceiling / next track
94–95 is **asset-bound** (synthetic-image AI-render sheen) — design/typography/UI/warmth are maxed. Bespoke imagery
exists only on the **real-salon track**: adapt this baseline to a specific salon's OWN face-free photos + THEIR real
menu; the send stays **Yu-manual** (never auto-send).

Reports: `…/reports/20260617_lea_final_typography_ui_optical_polish_loop_v8.md` (+ v5/v6/v7 + qa).
Usage: `python3 real_render.py` (renders real_profiles/*.json → generated_demos/real_lead_review_20260617/).
