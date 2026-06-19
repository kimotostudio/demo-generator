---
name: personal-salon-frontend-design
description: Guidance for building distinctive, claim-safe, high-quality demo LPs for personal salons and owner-led small service businesses. Use when building or revising a salon demo LP (hero/typography/layout/menu/CTA/access), removing AI-generic feel, adapting salon_editorial_variant to a real lead, or preparing a sales-demo-quality page. The goal is a page that could only belong to THIS salon — not a generic "relaxing wellness" template.
---

# Personal Salon Frontend Design

A demo LP exists to make one specific salon owner feel *"this person actually understood my shop."*
That feeling does not come from polish. It comes from **specificity** — every choice traceable to a real
detail of this store. A page that would work for any salon works for none. This skill adapts the design
discipline of intentional, non-templated frontend work to the personal-salon sales-demo job, with the
claim-safety and face-free rules KIMOTO STUDIO operates under.

> One-line test before you ship: *"Could I paste a different salon's name into this page and have it still
> make sense?"* If yes, the page is generic — go back to the brief.

---

## When to use this skill

Use it when:
- building or revising a personal-salon demo LP (a real lead, or a variant template instance);
- improving the hero, typography, layout, CTA, menu, reservation flow, or access section;
- removing AI / generic / "stock wellness LP" feel from an existing demo;
- adapting `salon_editorial_variant` (or any base template) to a specific real lead;
- preparing a page to sales-demo quality before Claude review.

## Do NOT use this skill for

- backend / pipeline / scoring code (lead scoring, crawling, filters);
- BTC / criticality research;
- content writing unrelated to a web demo (Threads/note drafts → use the content skill);
- outreach **sending**, email, DM, or form submission (never automatic in current phase);
- compliance-only checks with no design work (use the claim-safety / suppression docs directly).

---

## 1. Design principles (adapted for personal salons)

### 1.1 Hero is a thesis
The first screen is an argument about *what this salon is*, not a decorative banner. It must carry the
store as the grammatical subject. Lead with the salon's single most characteristic truth, drawn from real
brief material, and make the **store name legible and primary** — never let an abstract tagline outrank it.

For a personal salon, the hero's raw material is some subset of:
- store name (always present, always identifiable);
- region / area (e.g. 久留米・三瀦町, 小郡市);
- the space itself (古民家 / 自宅サロン / 完全予約の個室 / 女性専用);
- the treatment category (ドライヘッドスパ / アロマ / よもぎ蒸し / フェイシャル / リンパ);
- the owner's stance (静かに休める / 一人ひとり丁寧に / 相談しやすい);
- the booking model (予約制 / 完全予約制).

**Failure mode:** a huge poetic line ("静寂に、還る。") with a tiny store name beneath it. The visitor must
know *which shop this is* within one second. Abstract copy may exist, but it serves the name — not the reverse.

### 1.2 Typography carries personality
Type is the page's voice, not a neutral container. Choose the type system per salon, tuned to *temperature*:
- don't over-use display faces — one display role at most, used sparingly;
- don't drift into 旅館 / 美術館 / 高級料亭 pastiche just because it's a Japanese wellness business;
- body text must be genuinely comfortable to read (line-height, measure, contrast);
- prices, durations, and the reservation line must look **clean and confident**, never an afterthought —
  a cramped or ugly price block reads as amateur and kills trust;
- adjust the font's warmth to the store: a quiet headspa is not a bright facial clinic.

Reference temperatures (illustrative, not mandatory):
- *Lea (肌相談):* 明朝 + Latin serif + soft sans → calm, consultative, easy to talk to.
- *Akazukin (古民家ヘッドスパ):* enough warmth/age to signal the old house, but stop well short of a
  ryokan or museum; store-name recognition wins over atmosphere.

### 1.3 Structure is information
Numbering, rules, cards, eyebrows, and labels are meaning-bearing devices, not decoration. Use a structural
device only when it encodes real content hierarchy.

**Avoid** (generic structure smell):
- 01 / 02 / 03 numbering applied to things that aren't a sequence;
- hairline rules used to "look designed" / make the page feel rigid;
- three cards in a row because that's the default;
- SaaS-LP scaffolding (feature grid, "why choose us", logo wall);
- stacking template sections in their shipped order with no editing.

**Legitimate** uses:
- 予約の流れ / 来店ステップ (a genuine ordered process → numbering earns its place);
- メニュー比較 (structured rows where comparison is the point);
- アクセス情報 (labelled facts: 住所・最寄り・駐車・営業時間).

### 1.4 Distinctive, subject-specific choices
Reject the AI default look. The clustering pattern to avoid is the *"warm cream + serif + terracotta +
soft gradient + 3 cards + 癒しの空間"* set that every generic wellness LP converges on. Where the brief
leaves a design axis free, **do not** spend that freedom on the default.

Derive the visual language from the salon's real material instead:
- **古民家 / old house:** wood, quiet, shadow, generous negative space, restraint.
- **アロマ:** scent-as-mood, soft cloth, hands, small bottles, gentle diffused light.
- **ヘッドスパ:** darkness, the head and hands, stillness, a sense of slowed time.
- **よもぎ蒸し:** steam, warmth, the chair, "warming from the inside" — *as atmosphere only, never an
  asserted physiological effect* (see claim-safety).
- **フェイシャル:** cleanliness, skin/texture detail, white / pale tones, careful hands.

### 1.5 One memorable signature
Give each page exactly **one** thing a person remembers — and keep everything else quiet around it. Do not
add a second signature; that just produces noise. Spend the boldness once.
- *Akazukin:* the old-house negative space with the store name as the hero subject.
- *Lea:* an editorial, magazine-like calm for skin consultation.
- *Pear:* the warm, approachable feel of a women-only home salon you'd feel safe visiting.

### 1.6 Restraint
Quality is precision, not accumulation. If a decoration doesn't serve the brief, cut it. Minimal work
demands exact spacing, type, and rhythm; the discipline *is* the design. A calmer page with one strong
idea beats a busy page with five weak ones — and reads as more expensive.

### 1.7 Copy as design material
Words are part of the composition and each line does one job. Use concrete, store-specific language in a
natural, conversational register. **Ban the thin-wellness vocabulary** that signals an AI template:
"癒しの空間", "特別な時間", "心も体も整う", "日々の疲れを忘れて", and similar filler. If a sentence would
fit any salon, rewrite it from a real detail of *this* one — or delete it.

---

## 2. Personal-salon specifics

### 2.1 Category-specific cues
Pick the visual/copy cues from the actual category (see 1.4). Match the page's darkness, warmth, and pace
to the treatment: a dry-headspa page is dim and slow; a facial page is clean and light; an aroma page is
soft and tactile. Mismatched mood (a bright clinical headspa, a dark facial) reads as wrong instantly.

### 2.2 Face-free visual strategy
KIMOTO STUDIO demos are **face-free**. Do not depend on a model's face for emotional impact. Build feeling
from: hands, the space, materials (wood, cloth, steam, plants, bottles), light, and negative space, with
tight crops and atmosphere over portraiture. This is a constraint that *improves* specificity — lean into it.

### 2.3 Real photo vs generic visual rule
- Prefer the salon's **own real imagery** when rights are confirmed.
- When real photos aren't available or rights are unconfirmed, use **baseline / atmosphere visuals** that
  are honest about being illustrative, and keep the demo's framing as "a way of showing it — content can be
  swapped for your real photos." Never present a stock/baseline image as if it were the salon's own room,
  staff, or result. Note unknown photo-rights in the QA/ledger.

### 2.4 Sales demo vs production readiness
A **sales demo** is a proposal ("here's how your shop could look"), not the salon's finished live site.
That framing legitimately lowers the bar on real photos / full menu / exact prices — but it **raises** the
bar on honesty: nothing fabricated, nothing that pretends to be confirmed when it isn't. "Production-ready"
(real menu, real prices, real photos, owner-approved) is a separate, higher gate reached only after the
owner engages.

### 2.5 Claim-safe language (hard rules)
The page must stay claim-safe. **Forbidden:** 改善 / 効果 / 小顔 / 不眠 / 自律神経 / 妊活 / 脱毛 / 医療 /
診断・治療を思わせる表現 / before-after / fabricated testimonials / 痩身・矯正 as asserted outcomes.
- Describe **atmosphere and experience**, not physiological results. "湯気につつまれる時間" is fine;
  "代謝が上がる" / "むくみが取れる" is not.
- **No fake testimonials.** No invented reviews, names, ratings, or "お客様の声" that didn't happen.
- **No before/after.** No transformation imagery or implied results.
- **No medical / effect claims.** When a category is claim-sensitive (よもぎ蒸し, エステ系), default to
  OMIT: describe the experience and omit any effect language entirely.

### 2.6 Honesty defaults
Real store name, real category, real area. No invented address, hours, prices, or contact route. If a fact
is unknown, omit it rather than guess. Unknowns (photo rights, full menu, hours, IG recency) are logged,
not papered over.

---

## 3. Process (brainstorm → plan → critique → build → critique again)

Codex does **not** start implementing immediately. The order is:

1. **Brief extraction.** From the lead's source profile, define: *subject* (this exact salon + its single
   most characteristic truth), *audience* (who books it — e.g. local women seeking a quiet hour), and the
   *page's job* (let a first-time visitor feel the atmosphere and see how to book).
2. **Design plan.** A compact, written plan **before any code**: a 4–6 colour token set, 1–2 typeface roles
   with intent, a layout concept (prose + ASCII wireframe), the chosen category cues, and the **one signature
   element**. State explicitly which AI-default axes you are refusing and why.
3. **Claude review (gate 1).** Claude reviews the *plan* against this skill: is the hero a thesis? Does the
   store own the page? Is anything a generic default? Does it stay claim-safe and face-free? Plan is revised
   until it passes — only then build.
4. **Codex build.** Implement strictly from the validated plan. Derive every decision from the plan; don't
   improvise new directions mid-build. Stay within the task's target files (scope discipline).
5. **Playwright QA.** Screenshot mobile widths (360 / 375 / 390 / 412) and desktop; run the QA checklist
   (§4); capture image-performance and the hero first-view.
6. **Claude review (gate 2).** Harsh review of the built page + screenshots against §4. Short of bar →
   specific fix instructions → Codex revises → re-review.
7. **Slack manual-send card.** When the page passes, prepare the manual-send card. **Deploy is allowed;
   sending is not** — Yu decides the actual send (see §6).

---

## 4. QA checklist

Run every item; a single fail blocks "ready".

- [ ] **Store identity visible** — name legible and primary in the hero (not outranked by abstract copy).
- [ ] **Category & region correct** — matches the source profile exactly.
- [ ] **Hero hierarchy** — name → characteristic truth → quiet supporting line; subject is the store.
- [ ] **Mobile 360 / 375 / 390 / 412** — no overflow, no broken wraps (esp. long カタカナ category names),
      tap targets and price/CTA blocks clean at every width.
- [ ] **Internal labels absent** — no PRIVATE / DRAFT / SAMPLE / サンプル / QA / placeholder / 要確認 /
      TODO / lorem / dev banner in visitor-facing HTML.
- [ ] **Forbidden claims absent** — 0 hits for 改善/効果/小顔/不眠/自律神経/妊活/脱毛/医療/before-after/
      痩身/矯正 (and category-sensitive effect language); no fake testimonial; no before/after.
- [ ] **CTA natural** — reservation/contact reads like a real invitation, not a SaaS "Get Started" button;
      route honest (form/LINE/email as the lead actually has).
- [ ] **Typography comfortable** — body readable; prices/times/booking look intentional and clean.
- [ ] **Image performance acceptable** — optimized (WebP/lazy/preload where used); mobile first-view weight
      reasonable (target ~sub-MB hero, not multi-MB).
- [ ] **No AI-template smell** — fails the "swap the name" test? then it's not done. No cream+serif+terracotta
      default, no meaningless gradient, no decorative 3-card row, no thin-wellness copy.
- [ ] **noindex present** while the page is a private/preview demo; honest framing as a sample.

---

## 5. Examples

**Akazukin (久留米・三瀦町 / 築150年古民家 / ドライヘッドスパ).**
Thesis: a 150-year-old farmhouse where you can quietly rest your head. Signature: old-house negative space
with the store name as the hero subject. Type warm enough to signal age, stopped short of ryokan pastiche;
name recognition prioritized. Dim, slow, headspa-appropriate; face-free (hands, wood, shadow). Claim-safe:
"静かに頭を休める時間" — no 不眠/改善 language.

**Lea (肌相談 / フェイシャル系).**
Thesis: a calm place to *talk about your skin*, not be sold to. Signature: an editorial, magazine-like
consultative feel. Type: 明朝 + Latin serif + soft sans for a quiet, easy-to-approach register. Clean and
light, skin/texture detail, careful hands; claim-safe (no 小顔/効果).

**Pear (女性専用自宅サロン / リンパ・よもぎ).**
Thesis: a women-only home salon that feels safe and warm to visit for the first time. Signature: the warm,
approachable "you can relax here" tone. Relaxation-only language; よもぎ described as warmth/atmosphere,
effect claims omitted (claim-sensitive). Face-free, soft materials and light.

---

## 6. Integration (roles, deploy, send)

This skill is the shared reference for the demo-LP loop:
- **Codex (Professional Web Designer / Frontend Implementer)** consults this skill **before building or
  modifying any demo UI** — it drives brief extraction, the design plan, the build, and self-QA.
- **Claude (Creative Director / Harsh Reviewer / QA Gatekeeper)** reviews against this skill at both gates
  (plan review and built-page review); 80-point work does not pass.
- **Yu (final decision maker)** decides the actual send.
- **Deploy is allowed / AUTO** (preview and public production) — deploying a demo does **not** contact anyone.
- **Send is NOT automatic in the current phase.** Outreach / email / form submit / DM / sent=1 stay
  Yu-manual. Deploy ≠ send. The loop ends at a manual-send card; Yu sends.

See: `docs/PRE_SEND_QA_LOOP.md`, `docs/CODEX_FIX_DEPLOY_LOOP.md`, `docs/CLAUDE_REVIEW_GATE_LOOP.md`,
`docs/SLACK_MANUAL_SEND_CARD_LOOP.md`.
