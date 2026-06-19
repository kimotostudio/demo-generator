# Salon Booking Template v2

`salon_booking_v2` is the quality-upgraded personal salon landing-page template. It keeps the v1 9-block strategy and slot contract, but raises the presentation toward `templates/variantA.html` quality: layered gradients, serif/sans typography, deeper shadows, interactive transitions, reveal animation, and responsive grid behavior.

## Files

- Template: `templates/salon_booking_v2/template.html`
- Manifest: `templates/salon_booking_v2/manifest.json`
- Kumamoto review renders: `samples/kumamoto_review_20260613/<slug>/index.html`

## What Changed From v1

- Visual quality: v2 adds a gradient first view, layered card and image shadows, polished spacing, interactive hover states, and subtle reveal animation.
- Typography: v2 uses a two-family design system with separate sans and serif stacks and a broader size/weight scale.
- Image handling: image slots remain neutral placeholders and are visibly labeled `サンプル画像（要差し替え・写真許諾後）`.
- Motion: v2 includes local-only CSS transitions, `@keyframes`, and an inline `IntersectionObserver` reveal. There are no external scripts.
- Responsiveness: v2 keeps the 9 blocks but upgrades grid behavior for desktop, tablet, and mobile breakpoints.
- Compliance: v2 keeps the visible `提案サンプル(ドラフト・未送信)` label and placeholder-only customer voice block.

## 9 Blocks

1. First view: salon name, area, price/booking meta, first-visit CTA, and sample image slot.
2. For: soft audience framing for visitors who want quiet time, clarity, and a careful first visit.
3. Reasons: quiet space, first-visit clarity, and personalized strengths.
4. Menu: first-visit menu, regular menu, seasonal menu, and prices.
5. Flow: booking, visit, hearing, menu time, and next guidance.
6. Owner profile: owner name, profile, owner words, and labeled sample photo slot.
7. Customer voices: PLACEHOLDER-only unless real permissioned data exists.
8. Access: area, station, parking, hours, booking route, and map placeholder.
9. Final CTA: booking route and first-visit route.

## Slot Contract

v2 intentionally uses the same rendering slots as v1 so existing safe-local `input.json` files can be re-rendered without changing salon data.

Required strategy slots:

- `SALON_NAME`
- `AREA`
- `MENU_NAME`
- `ATMOSPHERE`
- `OWNER_WORDS`
- `PHOTO_TONE`
- `BOOKING_ROUTE`
- `PRICE_RANGE`
- `TARGET_CUSTOMER`
- `STRENGTHS`
- `FIRST_VISIT_ROUTE`

Additional rendering slots:

- `HERO_IMAGE`
- `OWNER_IMAGE`
- `OWNER_NAME`
- `OWNER_PROFILE`
- `FIRST_VISIT_PRICE`
- `REGULAR_MENU_NAME`
- `REGULAR_PRICE`
- `SEASONAL_MENU_NAME`
- `SEASONAL_PRICE`
- `STATION_INFO`
- `PARKING_INFO`
- `OPEN_HOURS`
- `BOOKING_URL`
- `BOOKING_BUTTON_LABEL`
- `YEAR`

## Guardrails

- Do not invent testimonials. The `お客様の声` section must stay `PLACEHOLDER` unless real customer text and publication permission exist.
- Do not use copied salon photos or generic stock as if it belongs to the salon. Use only clearly labeled sample image slots until Yu confirms permission.
- Do not promise business outcomes, bookings, ranking, or customer acquisition.
- Do not criticize the recipient's current website, booking flow, copy, tools, or competitors.
- Avoid medical, body-shape, and efficacy-style claims. Rendered demos are checked for: `治療`, `改善`, `効果`, `痩身`, `集客保証`, `成果保証`, `医療`.
- Keep `提案サンプル(ドラフト・未送信)` visible in every real-review draft.
- Human review is required before deploy, outreach, or any browser-side workflow.

## Safe-Local Render Command

This does not modify `generate.py` and does not write to `output/`.

```bash
cd /home/kimoto/projects/demo-generator
python3 - <<'PY'
import json
from pathlib import Path

template = Path("templates/salon_booking_v2/template.html").read_text(encoding="utf-8")
for input_path in sorted(Path("samples/kumamoto_review_20260613").glob("*/input.json")):
    data = json.loads(input_path.read_text(encoding="utf-8"))
    html = template
    for key, value in data.items():
        if key.startswith("_"):
            continue
        html = html.replace("{{" + key + "}}", str(value))
    unresolved = sorted(set(part.split("}}", 1)[0] for part in html.split("{{")[1:]))
    if unresolved:
        raise SystemExit(f"{input_path}: unresolved placeholders: {unresolved}")
    output_path = input_path.with_name("index.html")
    output_path.write_text(html, encoding="utf-8")
    print(output_path)
PY
```

## Safe-Local Self-Check

```bash
cd /home/kimoto/projects/demo-generator
python3 - <<'PY'
from pathlib import Path

for path in sorted(Path("samples/kumamoto_review_20260613").glob("*/index.html")):
    html = path.read_text(encoding="utf-8")
    missing_blocks = [f'data-block="{i:02d}-' for i in range(1, 10) if f'data-block="{i:02d}-' not in html]
    forbidden = ["治療", "改善", "効果", "痩身", "集客保証", "成果保証", "医療"]
    forbidden_hits = [word for word in forbidden if word in html]
    checks = {
        "path": str(path),
        "missing_blocks": missing_blocks,
        "forbidden_hits": forbidden_hits,
        "proposal_label": "提案サンプル(ドラフト・未送信)" in html,
        "placeholder_voices": "PLACEHOLDER 01" in html and "許可のない文章や想像で作った感想は掲載しません" in html,
        "image_slot_label": "サンプル画像（要差し替え・写真許諾後）" in html,
        "quality": {
            "font_family": html.count("font-family") >= 6,
            "font_size": html.count("font-size") >= 10,
            "font_weight": html.count("font-weight") >= 10,
            "transition": html.count("transition") >= 10,
            "keyframes": html.count("@keyframes") >= 1,
            "gradient_hero": ".hero" in html and "linear-gradient" in html,
            "box_shadow": html.count("box-shadow") >= 6,
            "responsive": html.count("@media") >= 2,
        },
        "unresolved_placeholders": "{{" in html or "}}" in html,
    }
    print(checks)
    if missing_blocks or forbidden_hits or not checks["proposal_label"] or not checks["placeholder_voices"] or not checks["image_slot_label"] or checks["unresolved_placeholders"] or not all(checks["quality"].values()):
        raise SystemExit(1)
PY
```

Do not open a browser, deploy, write to `output/`, commit, push, send messages, or run Playwright unless a later task explicitly approves that action.
