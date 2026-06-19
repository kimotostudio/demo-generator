# Salon Lead Discovery Playbook v1 (2026-06-18)

Operating guide for the personal-salon demo-LP lead pipeline. Pairs with `salon_editorial_variant` (Lea v8 baseline).
**Standing rule: sent=0. No outreach/contact/deploy of real-salon demos without Yu. Demo generation is gated on A + Yu-OK.**

## 1. Good lead (target A)
An **active** personal/owner-led salon, in a target category, **low regulatory risk**, with a **reachable contact route**, and
**a weak or absent conversion LP** — i.e. the business is getting customers (IG-active / HotPepper-listed) but its own page
under-sells it. Enough source info exists (name, area, ≥1 menu, contact, some atmosphere/visual) to build a demo, OR it's
seedable to that with a quick enrich. *Own site OR a strong active Instagram both qualify.*

## 2. Bad lead (Exclude)
Chain/clinic · closed (休業中) · wrong region · medical/痩身/小顔/美白-claim-heavy · 整体/医療色強 · no contact path ·
school-primary or visiting-care-primary (not a booking salon) · strong-spiritual/occult tone · portal-only with no own
identity · host bot-blocked AND not active-confirmable elsewhere.

## 3. Source strategy (priority order)
1. **Instagram-first** (primary): find active personal salons by category+area; confirm recency (posts within ~1–2 months);
   note menu/atmosphere/contact (DM/LINE); check if they have a real LP gap.
2. **Google Maps / portal active-confirm** (secondary): HotPepper/EPARK/Maps to confirm the business is open + get name/area/phone,
   then find their own site/IG.
3. **Own site / Wix / WordPress / Ameba** (enrich): fetch for menu/contact/atmosphere (Ameba is fetchable; peraichi/jimdosite
   often 403 — use as hint only, don't rely on fetching).
4. **Platform weak-site query** (hint only): `site:jimdofree.com <area> <category>` — surfaces weak sites but closed/thin-heavy.

## 4. Query examples
- IG/general: `<area> ドライヘッドスパ 個人サロン`, `<area> よもぎ蒸し サロン 予約`, `<area> アロマ リラクゼーション 女性専用`
- portal: `<area> ヘッドスパ ホットペッパー`, then open the salon's own-site/IG link
- weak-site hint: `site:jimdofree.com <area> アロマ`, `site:ameblo.jp <area> リンパ 個人サロン`
- AVOID generic `個人サロン スピリチュアル / 資格 / スクール` phrasings (noise).

## 5. Target categories (first rounds)
Lead: **ドライヘッドスパ · よもぎ蒸し · リンパ · アロマ-relaxation (booking-focused).**
Down-weight: フェイシャル/エステ (claim risk), リフレ (改善-prone). Avoid first: 整体/ボディケア (medical), strong-spiritual healing.

## 6. Scoring rules (0–5 each; overall + rank)
owner_presence · active_business · category_fit · contactability · **lp_gap (demo-fit: active but weak/absent LP)** ·
source_richness · visual_availability · **regulatory_risk (reverse: high risk = low score)** · portal_dependency (reverse).
Active_business and region-correct are **gates** (fail → Exclude). regulatory: esthetic/痩身/小顔/美白-heavy → Exclude.

## 7. A / B / C / Exclude
- **A — demo now:** active(gate) + personal + category-fit + low-risk + reachable + enough info (name/area/≥1 menu/contact/visual).
- **B — Yu review queue → promotable:** active + personal + category-fit + low-risk + reachable BUT info-thin / needs
  active-confirm / needs a URL. Salvage via Yu-seed or a quick enrich, then promote to A. **Do not discard B.**
- **C — record only:** marginal/uncertain.
- **Exclude:** §2 list (strict; safety never loosened).

## 8. Yu seed workflow (fastest quality)
1. Yu pastes 2–5 salon URLs (own site/IG) worth approaching → 2) Codex profiles (source-backed only) → 3) Claude scores A/B+risk
→ 4) reverse-engineer the good-lead signature → refine queries → 5) demo only on A + Yu-OK (private/noindex). sent=0.

## 9. Demo generation gate
Generate a private/noindex demo ONLY when: lead is **A** (or B promoted by Yu) AND Yu approves generation. Use the Lea v8
baseline; **clean claim-free copy** (never echo a salon's 改善/効果); real menu if visible, else category-fallback marked
internal; face-free baseline visuals unless the salon's own rights-clear photos are confirmed; CTA = real reservation route.

## 10. sent=0 safety rule (FOREVER, unless Yu names an auto-send lane)
No outreach, no form submit, no DM/email/phone, no public production deploy of real-salon demos, no scraping at scale,
no login-gated pages. All sending is Yu-manual. Every pipeline run reports sent=0.

## 11. Source-comparison learnings (2026-06-18, 久留米 run)
- **portal/Maps → own-site enrich = primary engine** (best clean signal + active-confirm).
- **Instagram-first is NOT executable via WebSearch** (US-geo; IG not indexed) → use Yu-seed or direct IG for the IG lane.
- weak-site site: queries = secondary hint source (noisy: school/spiritual/mens/mis-region).
- **dry-head-spa / yomogi in regional cities (久留米) = high yield** (low claim, strong atmosphere, owner-run). This combo > broad aroma/relax.
- Verification obstacles to expect: TLS-broken self-sites + peraichi/jimdosite 403 → confirm "active" via portal/Maps instead.
- A+B demo-ready ≈ 42% achievable with active-first + B-salvage (vs ~6% old method).
## v2 targeting decisions (Yu-adopted 2026-06-18, from historical lead-learning)
Target = owner-led local salon + appointment route + ACTIVE evidence + weak/dated self-presentation
(NOT "the weakest site"). 30–50 candidate batch, aim A+B ≥60% after dedup.

1. spiritual-first = EXCLUDE (スピリチュアルカウンセリング/チャネリング/霊視/占い/レイキ講座/波動/エネルギーワーク主体).
   relaxation/salon-first with only minor healing wording → B.
2. Geography: Fukuoka core = 久留米 / 筑後 / 小郡 / 八女 / 鳥栖 (priority: continue 久留米・筑後 first).
   Optional extra later: 福岡市郊外 or 岡山.
3. portal-only: NOT auto-Exclude → conditional B. If active-confirmed on HotPepper/Maps/portal AND enrichable
   to IG/LINE/own-site/reservation route → B. If not enrichable → Exclude.
4. Freshness: A = activity evidence within ~3–6 months. B = 6–12 months or "looks active, needs confirm".
   Exclude = no update >1yr / closed / dead reservation route / looks shut.
5. Treatment-adjacent: 治療院/整骨院/改善/効果/痛み/自律神経/不眠/妊活/小顔/痩身 → NOT A. Relax/body-care/
   lymph/head-spa-first that can be a claim-free demo → B.
Priority categories: ドライヘッドスパ・よもぎ蒸し・リンパ・アロマ・フェイシャル・リラクゼーション.
Avoid categories: spiritual主体・占い・レイキ講座・スクール・治療院・整骨院・クリニック・痛み改善・小顔効果・
自律神経・妊活・不眠改善・痩身効果.
