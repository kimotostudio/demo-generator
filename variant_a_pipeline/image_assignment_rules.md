# Image assignment rules — Variant A salon demo LP (v0)

Images are managed in code (no Figma). Five logical slots; v0 implements hero + owner,
with atmosphere/menu/access reusing hero-tone placeholders until real assets are permitted.

## Slots
- hero_image — first-view background
- atmosphere_image — mood (v0: shares hero tone)
- menu_image — menu visual (v0: shares hero tone)
- owner_image — owner/therapist
- access_or_room_image — room/access (v0: shares hero tone)

## Rules (enforced by generate_salon_lp.py)
1. Use a provided/source image ONLY if it is **locally present** AND `images.permission_to_use = true`.
2. If no suitable permitted image → neutral, on-brand **SVG placeholder** (gradient tinted by
   atmosphere/category) carrying the label "サンプル画像（要差し替え・写真許諾後）".
3. **Owner faces are NEVER auto-assigned** — even with permission, a real owner photo must be an
   explicit local file; otherwise a neutral silhouette placeholder is used. No generic beauty/medical
   stock as "the owner".
4. Do not copy/host the salon's real photos. Do not use unrelated stock unless explicitly allowed.
5. Every render records `image_source` + `confidence` + `type` in `render_meta.json`
   (placeholder = low confidence; local_permitted = high).

## v0 status
Default output uses neutral SVG placeholders (honest, compliant, deploy-safe). Real photos are a
post-approval, per-salon step (photo permission required) — never assumed.
