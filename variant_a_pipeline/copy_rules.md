# Copy rules — Variant A salon demo LP (v0)

The LP must feel **tailored to this salon**, never generic, and never make medical/efficacy/guarantee claims.

## Required personalized elements (must reflect real source signals)
- 店名 (business_name) — the real 屋号, not a page title/heading/snippet
- 地域 (city + area_or_station)
- 業種 (category)
- 既存メニュー名 (main_menu_names — real only, never invented)
- 店舗の雰囲気 (atmosphere_keywords)
- オーナー/施術者の存在 (owner_presence/owner_name — only if publicly visible)
- 初回予約導線 / 予約方法 (demo_angle, contact_method, reservation_url)
- 価格帯 (price_range — only if observed; else [要確認])
- 写真トーン (PHOTO_TONE — labeled as sample)
- 既存サイト/Instagramから見える強み (visible_strengths)

## Forbidden copy (generator FAILS if any reach injected content)
治ります / 治る / 完治 / 改善します / 改善 / 効果 / 効果保証 / 必ず / 必ず集客 /
集客保証 / 売上アップ / 売上アップ保証 / 医療 / 治療 / 痩身 / 成果保証 / 保証します
- Also forbidden structurally: 口コミ捏造 / 実績捏造 / Before-After捏造 (template keeps お客様の声 as a labeled PLACEHOLDER; the generator never fills testimonials).
- "AIで作りました" must not be foregrounded.

## Safe wording (preferred)
整えます / 伝わりやすくします / 初めての方に分かりやすく / 予約まで迷わない導線 /
雰囲気が伝わる構成 / 安心して相談しやすい見せ方

## Honesty rules
- Unknown fields render as explicit `[要確認: …]` — never guessed.
- `site_weaknesses` is INTERNAL ONLY (picks the demo angle); it is NEVER rendered (no criticism of the recipient's current site).
- All image slots carry the "サンプル画像（要差し替え・写真許諾後）" label.
- The "提案サンプル（ドラフト・未送信）" label stays visible.
