---
name: personal-salon-frontend-design
description: Build distinctive, claim-safe, high-quality demo LPs for personal salons. Use when building/revising a salon demo LP, removing AI-generic feel, adapting a base variant to a real lead, or preparing a sales-demo-quality page.
---

> Canonical source: demo-generator/skills/personal-salon-frontend-design/SKILL.md. This is the
> plugin-bundled copy; keep them in sync.

# Personal Salon Frontend Design

A demo LP exists to make one specific salon owner feel *"this person actually understood my shop."* That
feeling comes from **specificity** — every choice traceable to a real detail of this store. A page that
would work for any salon works for none.

> Ship test: *"Could I paste a different salon's name into this page and have it still make sense?"* If
> yes, it's generic — go back to the brief.

## When to use

- Building or revising a personal-salon demo LP (real lead or variant instance).
- Improving hero, typography, layout, CTA, menu, reservation flow, or access.
- Removing AI / generic / stock-wellness feel from an existing demo.
- Adapting a base template (e.g. `salon_editorial_variant`) to a specific real lead.

## Do NOT use for

Backend / scoring / crawling code; BTC research; non-web content (Threads/note → content skill);
outreach **sending** (never automatic this phase); compliance-only checks with no design work.

---

## 1. Design principles

### 1.1 Hero is a thesis
The first screen argues *what this salon is*, with the store as the grammatical subject. Lead with the
salon's single most characteristic truth, and keep the **store name legible and primary** — never let an
abstract tagline outrank it. Raw material: store name (always), region, the space (古民家 / 自宅サロン /
完全予約の個室 / 女性専用), category (ドライヘッドスパ / アロマ / よもぎ蒸し / フェイシャル / リンパ),
owner's stance, booking model. **Failure mode:** a huge poetic line with a tiny store name. The visitor
must know *which shop this is* within one second.

### 1.2 Typography carries personality
Type is the page's voice. One display role at most, used sparingly; don't drift into 旅館 / 美術館 /
高級料亭 pastiche just because it's Japanese wellness. Body text genuinely comfortable (line-height,
measure, contrast). Prices, durations, and the reservation line must look **clean and confident** — a
cramped, ugly price block reads amateur and kills trust. Tune warmth to the store: a quiet headspa is not
a bright facial clinic.

### 1.3 Structure is information
Numbering, rules, cards, eyebrows, labels are meaning-bearing, not decoration. **Avoid:** 01/02/03 on
non-sequences; hairline rules used to "look designed"; three cards because that's the default; SaaS-LP
scaffolding (feature grid, "why choose us", logo wall); shipping template sections unedited. **Legitimate:**
予約の流れ / 来店ステップ (real ordered process), メニュー比較 (comparison rows), アクセス (labelled facts).

### 1.4 Distinctive, subject-specific choices
Reject the AI default: *warm cream + serif + terracotta + soft gradient + 3 cards + 癒しの空間.* Where a
design axis is free, don't spend it on the default. Derive the visual language from real material:
- **古民家:** wood, quiet, shadow, generous negative space, restraint.
- **アロマ:** scent-as-mood, soft cloth, hands, small bottles, diffused light.
- **ヘッドスパ:** darkness, head and hands, stillness, slowed time.
- **よもぎ蒸し:** steam, warmth, the chair — *as atmosphere only, never an asserted effect* (see §2.5).
- **フェイシャル:** cleanliness, skin/texture detail, white/pale tones, careful hands.

### 1.5 One memorable signature
Exactly **one** thing a person remembers; keep everything else quiet. No second signature (that's noise).
Spend the boldness once.

### 1.6 Restraint
Quality is precision, not accumulation. Cut decoration that doesn't serve the brief. A calmer page with
one strong idea beats a busy page with five weak ones — and reads as more expensive.

### 1.7 Copy as design material
Each line does one job; concrete, store-specific, conversational. **Ban thin-wellness filler:** "癒しの空間",
"特別な時間", "心も体も整う", "日々の疲れを忘れて". If a sentence fits any salon, rewrite it from a real
detail of *this* one — or delete it.

---

## 2. Personal-salon specifics

### 2.1 Category cues
Match darkness/warmth/pace to the treatment: dry-headspa dim and slow; facial clean and light; aroma soft
and tactile. Mismatched mood reads wrong instantly.

### 2.2 Face-free visuals
KIMOTO STUDIO demos are **face-free.** Build feeling from hands, the space, materials (wood, cloth, steam,
plants, bottles), light, and negative space — tight crops, atmosphere over portraiture. The constraint
*improves* specificity.

### 2.3 Real photo vs baseline visual
Prefer the salon's **own real imagery** when rights are confirmed. Otherwise use honest baseline/atmosphere
visuals framed as "a way of showing it — swap for your real photos." Never present a stock/baseline image
as the salon's own room, staff, or result. Log unknown photo-rights.

### 2.4 Sales demo vs production
A **sales demo** is a proposal ("here's how your shop could look"), not a finished live site — which lowers
the bar on real photos/menu/prices but **raises** the honesty bar: nothing fabricated, nothing pretending
to be confirmed. "Production-ready" is a separate, higher gate reached only after the owner engages.

### 2.5 Claim-safe language (hard rules)
**Forbidden:** 改善 / 効果 / 小顔 / 不眠 / 自律神経 / 妊活 / 脱毛 / 医療 / 診断・治療を思わせる表現 /
before-after / fabricated testimonials / 痩身・矯正 as asserted outcomes. Describe **atmosphere and
experience**, not physiological results ("湯気につつまれる時間" yes; "代謝が上がる" no). **No fake
testimonials. No before/after. No medical/effect claims** — for claim-sensitive categories (よもぎ蒸し,
エステ系), default to OMIT effect language entirely.

### 2.6 Honesty defaults
Real store name, category, area. No invented address, hours, prices, or contact route. Unknown fact → omit,
don't guess. Log unknowns (photo rights, full menu, hours, IG recency).

---

## 3. Process

1. **Brief extraction** — subject (this salon + its single characteristic truth), audience, page's job.
2. **Design plan (before any code)** — 4–6 colour tokens, 1–2 typeface roles with intent, layout concept
   (prose + ASCII wireframe), category cues, the **one signature**, and which AI-defaults you refuse.
3. **Claude review (gate 1)** — plan vs this skill: hero a thesis? store owns the page? generic defaults?
   claim-safe + face-free? Revise until it passes, then build.
4. **Codex build** — implement strictly from the validated plan; stay within target files (scope discipline).
5. **Playwright QA** — screenshot mobile (360/375/390/412) + desktop; run §4; capture hero first-view + image perf.
6. **Claude review (gate 2)** — harsh review of built page + screenshots; short of bar → fix instructions → revise.
7. **Slack manual-send card** — page passes → prepare card. **Deploy is allowed; sending is not** (Yu decides).

---

## 4. QA checklist (any single fail blocks "ready")

- [ ] **Store identity visible** — name legible and primary in the hero.
- [ ] **Category & region correct** — matches the source profile exactly.
- [ ] **Hero hierarchy** — name → characteristic truth → quiet supporting line.
- [ ] **Mobile 360/375/390/412** — no overflow/broken wraps (esp. long カタカナ), clean tap/price/CTA blocks.
- [ ] **Internal labels absent** — no PRIVATE/DRAFT/SAMPLE/サンプル/QA/placeholder/要確認/TODO/lorem/dev banner.
- [ ] **Forbidden claims absent** — 0 hits for 改善/効果/小顔/不眠/自律神経/妊活/脱毛/医療/before-after/痩身/矯正;
      no fake testimonial; no before/after.
- [ ] **CTA natural** — real invitation, not a SaaS "Get Started"; route honest (form/LINE/email as the lead has).
- [ ] **Typography comfortable** — body readable; prices/times/booking intentional and clean.
- [ ] **Image performance acceptable** — optimized (WebP/lazy/preload); mobile first-view ~sub-MB hero.
- [ ] **No AI-template smell** — passes the "swap the name" test; no cream+serif+terracotta default, no
      meaningless gradient, no decorative 3-card row, no thin-wellness copy.
- [ ] **noindex present** while a private/preview demo; honest framing as a sample.

---

## 5. Examples

- **Akazukin (久留米・三瀦町 / 築150年古民家 / ドライヘッドスパ).** Thesis: a 150-year farmhouse to quietly
  rest your head. Signature: old-house negative space, store name as hero. Warm-but-not-ryokan type; dim,
  slow, face-free. Claim-safe ("静かに頭を休める時間", no 不眠/改善).
- **Lea (肌相談 / フェイシャル系).** Thesis: a calm place to *talk about your skin*, not be sold to.
  Signature: editorial, magazine calm. 明朝 + Latin serif + soft sans. Clean and light; claim-safe (no 小顔/効果).
- **Pear (女性専用自宅サロン / リンパ・よもぎ).** Thesis: a women-only home salon that feels safe to visit.
  Relaxation-only language; よもぎ as warmth/atmosphere, effects omitted. Face-free, soft materials/light.

---

## 6. Integration (roles, deploy, send)

- **Codex (Frontend Implementer)** consults this skill before building/modifying any demo UI.
- **Claude (Creative Director / Harsh Reviewer / QA Gatekeeper)** reviews at both gates; 80-point work fails.
- **Yu (final decision maker)** decides the actual send.
- **Deploy is AUTO** (preview and public production) — deploying does not contact anyone.
- **Send is NOT automatic this phase** — outreach / email / form submit / DM / sent=1 stay Yu-manual.
  Deploy ≠ send. The loop ends at a manual-send card; Yu sends.

See: `docs/PRE_SEND_QA_LOOP.md`, `docs/CODEX_FIX_DEPLOY_LOOP.md`, `docs/CLAUDE_REVIEW_GATE_LOOP.md`,
`docs/SLACK_MANUAL_SEND_CARD_LOOP.md`.
