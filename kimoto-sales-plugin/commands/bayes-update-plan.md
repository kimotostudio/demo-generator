# Command: bayes-update-plan

## Purpose
Summarize outcome logs (sent / reply / positive_reply / rejected) and PROPOSE future Thompson-sampling updates per the `bayesian-sales-learning` skill. Read-only analysis — do NOT implement the bandit in v0.1.

## When to use
- After enough send outcomes have accumulated in the ledger and Yu wants direction on which lead segments / message variants to favor next.

## Required inputs
- Outcome event logs from the ledger (sent/reply/positive_reply/rejected, with route, variant, segment).
- `bayesian-sales-learning` skill (for the proposed update math/framing).

## Steps
1. Read outcome events; group by relevant arms (e.g. message_variant, lead segment A/B/C, area, send route).
2. Tally per arm: sends, replies, positive_replies, rejections; compute simple observed rates.
3. Frame as Beta(α, β) per arm (α = successes + prior, β = failures + prior) — describe, don't deploy.
4. PROPOSE Thompson-sampling updates: which arms look promising, which to keep exploring, prior choices, and sample-size caveats.
5. Flag low-data arms (too few sends to conclude) and recommend more data before acting.
6. Output a proposal table + a short narrative recommendation for Yu/Claude review.

## Safety rules
- Read-only: analyze logs, do not modify the ledger or implement any bandit/auto-selection.
- Be honest about small samples; do not over-claim significance.
- Proposals are decision material only; Yu/Claude decide whether to adopt.

## Outputs
- Per-arm tally + observed rates.
- Proposed Beta priors / posteriors per arm.
- Thompson-sampling update proposal + caveats (narrative + table).

## Report path
reports/YYYYMMDD_bayes-update-plan.md (under demo-generator/reports/)

## Hard stops
- Manual send only — NO auto-send, NO form submit, NO DM, NO phone, NO Gmail/SMTP/API.
- sent=0 stays 0; analysis never sets sent.
- Deploy (preview AND public production) is AUTO-allowed and deploy ≠ send.
- NO git push.
- Do not implement the bandit in v0.1. Do not edit files outside this task's listed target files (this report). If another file seems necessary, STOP and report instead of editing it.
