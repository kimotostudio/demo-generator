# KIMOTO STUDIO Sales Plugin — Manifest

- **Name:** KIMOTO STUDIO Sales Plugin / Ops Kit
- **Version:** v0.1
- **Type:** INTERNAL Claude Code / Codex working structure (NOT a public package, NOT an external plugin release)
- **Location:** `demo-generator/kimoto-sales-plugin/`
- **Purpose:** run lead discovery → demo build → demo review → manual send → Sales Console → Bayesian learning
  without rewriting long prompts each time. Skills carry judgment guidance; commands are reusable task prompts;
  safety docs are the hard gates; loops define the end-to-end flow.

## Core philosophy
- **AI judgment** (Claude/Codex/Manus) for: seed discovery, enrichment, A/B/C classification, demo-fit, demo design, review.
- **Code/Python** for: normalization, dedup, ledger, forbidden-claim scan, internal-label scan, audit/event logs,
  send caps, future Bayesian math.
- **External actions stay hard-gated:** no auto-send, no form submit, no DM, no phone, no `sent=1` until Yu confirms.
  Deploy (preview AND public production) is allowed/AUTO — deploy ≠ send.

## Commands (`commands/`) — reusable task prompts
| Command | Use it to… |
|---|---|
| `salon-score-leads` | score raw research into A/B/C/Exclude (after Manus/lead research) |
| `salon-enrich-leads` | enrich IG-only/portal-only candidates (freshness, menu, route, claim risk) |
| `salon-build-demo` | build a claim-safe demo LP from an A candidate (Codex; consult frontend-design skill) |
| `salon-review-demo` | harshly review a deployed/local demo → READY / FIX_FIRST / HOLD / EXCLUDE |
| `salon-manual-send-card` | produce the Slack manual-send card + filled outreach copy (no sending) |
| `salon-send-day` | manual-send validation day: pick 1–3, prep exact Yu actions |
| `sales-console-sync` | sync demo/lead/ledger data into the Sales Console |
| `ledger-update-after-yu` | update ledger ONLY after Yu says sent/replied/rejected |
| `bayes-update-plan` | summarize outcome logs, propose future Thompson-sampling updates |

## Skills (`skills/`) — judgment guidance
| Skill | Covers |
|---|---|
| `local-salon-lead-discovery` | what a good demo-first lead is; categories/areas; exclude list; A/B/C |
| `personal-salon-frontend-design` | distinctive, claim-safe demo LP design (plugin copy; canonical in `skills/`) |
| `claim-safe-outreach` | gift-not-criticism tone; the standard message; 木許-only signature |
| `manual-send-validation` | validation-day procedure; first goal = safe contact, not sales |
| `sales-console-ops` | the Console is a cockpit, not a sender; status/event-log/recommendation |
| `bayesian-sales-learning` | log first; beta-binomial plan; Thompson later (not v0.1) |

## Safety (`safety/`) — hard gates
`HARD_BOUNDARIES.md` · `FORBIDDEN_CLAIMS.md` · `SEND_POLICY.md` · `LEDGER_POLICY.md`

## Loops (`loops/`) — end-to-end flow (each: Input → AI step → Code/safety step → Yu decision → Output → Next)
`LEAD_DISCOVERY_LOOP` → `DEMO_BUILD_LOOP` → `DEMO_REVIEW_LOOP` → `MANUAL_SEND_LOOP` → `REPLY_LOGGING_LOOP` → `BAYESIAN_LEARNING_LOOP` → (back to discovery)

## Never (without explicit Yu approval)
auto-send · form submit · DM · phone · Gmail/SMTP/API · `sent=1` before Yu · fabricated URLs · fake testimonials ·
before/after · medical/beauty efficacy claims · git push.
