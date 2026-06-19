# Salon Booking Template v1

`salon_booking_v1` is a safe-local demo landing-page template for personal salons. It implements the 9-block structure from `ai-sales-automation-system/reports/20260613_personal_salon_target_and_lead_supply_strategy.md` section 9.

## Files

- Template: `templates/salon_booking_v1/template.html`
- Manifest: `templates/salon_booking_v1/manifest.json`
- Fictional sample input: `samples/salon_sample_fictional_20260613/sample_input.json`
- Rendered fictional sample: `samples/salon_sample_fictional_20260613/index.html`

## 9 Blocks

1. First view: area, audience, atmosphere, photo tone, price band, and first-visit CTA.
2. For: soft audience framing for visitors who want quiet time, clarity, and a careful first visit.
3. Reasons: private room, pre-session listening, and personalized strengths.
4. Menu: first-visit menu, regular menu, seasonal menu, and prices.
5. Flow: booking, visit, counseling, session, and after guidance.
6. Owner profile: owner name, profile, and owner words.
7. Customer voices: PLACEHOLDER-only unless real permissioned data exists.
8. Access: area, station, parking, hours, and booking route.
9. Final CTA: booking route and first-visit route.

## Personalization Slots

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

- Use invented data for samples and label samples as `FICTIONAL`.
- Do not use real business data unless the row has passed human review.
- Do not assert medical treatment, improvement, efficacy, body-shape, or outcome claims.
- Do not promise lead generation, bookings, sales, ranking, or other business results.
- Do not criticize the recipient's current website, booking flow, copy, competitors, or tools.
- Keep wording soft and optional: "ご案内", "確認できます", "必要な方にだけ" are preferred.
- The `お客様の声` block must stay `PLACEHOLDER` unless real customer text and publication permission exist.
- Before outreach use, a human must review every rendered page for unsupported claims, fake testimonials, real-business accuracy, and tone.

## Render Steps

This template intentionally does not require changes to `generate.py`. It follows the repo's placeholder convention by replacing `{{SLOT_NAME}}` tokens.

Local sample render command:

```bash
cd /home/kimoto/projects/demo-generator
python3 - <<'PY'
import json
from pathlib import Path

template_path = Path("templates/salon_booking_v1/template.html")
input_path = Path("samples/salon_sample_fictional_20260613/sample_input.json")
output_path = Path("samples/salon_sample_fictional_20260613/index.html")

html = template_path.read_text(encoding="utf-8")
data = json.loads(input_path.read_text(encoding="utf-8"))
for key, value in data.items():
    html = html.replace("{{" + key + "}}", str(value))
unresolved = sorted(set(part.split("}}", 1)[0] for part in html.split("{{")[1:]))
if unresolved:
    raise SystemExit(f"Unresolved placeholders: {unresolved}")
output_path.write_text(html, encoding="utf-8")
print(output_path)
PY
```

Local self-check command:

```bash
cd /home/kimoto/projects/demo-generator
python3 - <<'PY'
from pathlib import Path

html = Path("samples/salon_sample_fictional_20260613/index.html").read_text(encoding="utf-8")
blocks = [f'data-block="{i:02d}-' for i in range(1, 10)]
missing_blocks = [marker for marker in blocks if marker not in html]
forbidden = ["治療", "改善", "効果保証", "痩身", "集客保証"]
hits = [word for word in forbidden if word in html]
checks = {
    "missing_blocks": missing_blocks,
    "forbidden_hits": hits,
    "fictional_label": "FICTIONAL SAMPLE" in html and "架空サロン" in html,
    "placeholder_voices": "PLACEHOLDER 01" in html and "実際のお客様から許可" in html,
    "unresolved_placeholders": "{{" in html or "}}" in html,
}
print(checks)
if missing_blocks or hits or not checks["fictional_label"] or not checks["placeholder_voices"] or checks["unresolved_placeholders"]:
    raise SystemExit(1)
PY
```

Open locally:

```bash
xdg-open /home/kimoto/projects/demo-generator/samples/salon_sample_fictional_20260613/index.html
```

Do not run browser/open commands during safe-local no-browser tasks unless the task explicitly approves that action.
