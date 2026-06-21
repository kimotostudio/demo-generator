# Claude Code Instructions

This file is for Claude Code / Claude AI coding assistants working in `demo-generator`.

## Project

`demo-generator` generates and reviews per-lead, claim-safe first-outreach demo landing pages for
KIMOTO STUDIO / AI Sales Factory.

It does **not** do lead discovery, outreach, sent-state updates, Sales Console state changes,
content drafts for sending, public posting, or production deployment decisions.

Pipeline position:

```text
lead-finder -> demo-generator -> public demo URL -> Playwright preflight -> SEMI_AUTO
```

## Read First

Before changing anything, read in this order:

1. `CONSTITUTION.md`
2. `AI_GUIDE.md`
3. `AGENTS.md`

Also check `git status --short` before edits and keep changes scoped to this repository.

## Operating Principles

- **Demo-First:** build concrete, reviewable demo LPs before any human outreach decision.
- **Template-Based:** reuse the established demo structures and local helper scripts.
- **Stats-First where relevant:** report what changed, what passed, what failed, and what remains
  blocked.
- Keep generated operational data, private lead data, screenshots, logs, ledgers, and review queues
  local unless explicitly approved.

## Skills

Use the local skills in `.claude/skills/` when the task matches:

- `demo-build-review`: build or harshly review a claim-safe first-outreach demo LP.
- `lightweight-demo-build`: apply the image/performance standard for demo LPs.

Active image/performance standard:

- `docs/sales_lp_demo_lightweight_standard.md`
- Label: `SALES_LP_DEMO_V2_STANDARD_ACTIVE`
- Required targets include hero ≤120 KB, band/atmosphere ≤90 KB, and responsive `<picture>`
  markup with AVIF/WebP sources and fallback.

## Rules

Obey `.claude/rules/`.

Common synced rules are copied from `portfolio-manager/.claude/rules/` and include no-send,
no-submit, sent-state, no-git-push, no-overbuilding, and claim-safe. Project-specific rules include
`demo-qa-standard.md` and `lightweight-images.md`.

Do not edit synced common rules here. Change them upstream in `portfolio-manager` and re-sync.

## Guards Before A Build

Run the read-only guard preflight before a build:

```bash
python3 /home/kimoto/projects/portfolio-manager/tools/guards/run_guards.py
```

For rendered customer-facing copy, `claim_guard.py` must return 0 before the demo can be treated as
review-ready:

```bash
python3 /home/kimoto/projects/portfolio-manager/tools/guards/claim_guard.py <rendered-copy-path>
```

For any proposed deploy target, validate the target with `deploy_guard.py` before proceeding:

```bash
python3 /home/kimoto/projects/portfolio-manager/tools/guards/deploy_guard.py --site-id per_lead_demos --slug <slug>
```

Deploy validation is not permission to deploy. Deploy ≠ send.

## Review After A Build

Use the Demo QA Reviewer subagent after a build. Canonical spec:

```text
/home/kimoto/projects/portfolio-manager/.claude/agents/demo-qa-reviewer.md
```

The reviewer returns one of:

- `READY_FOR_REVIEW`
- `REVISE`
- `FAIL`

Claim wording can also be reviewed with the Claim Safety Officer:

```text
/home/kimoto/projects/portfolio-manager/.claude/agents/claim-safety-officer.md
```

## Hard Boundaries

- **Build ≠ send.**
- **Deploy ≠ send.**
- Never send email, DM, phone, booking, or outreach.
- Never submit forms or click final submit buttons.
- Never bypass captcha or bot protection.
- Never change sent-state, Sales Console state, ledgers, or review queues from this repository.
- Never push, commit, deploy, or publicly post without explicit approval.
- Build only route-confirmed candidates. Do not overbuild route-unclear leads.
