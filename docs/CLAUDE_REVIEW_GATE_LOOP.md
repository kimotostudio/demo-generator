# CLAUDE_REVIEW_GATE_LOOP

The two harsh-review gates Claude (Creative Director / Harsh Reviewer / QA Gatekeeper) runs on a
personal-salon demo LP. Claude does not implement production artifacts and must not skip review.

## Skill requirement
> **Claude reviews against `skills/personal-salon-frontend-design/SKILL.md` at both gates.** The skill's
> principles (§1) and QA checklist (§4) are the rubric. 80-point work does not pass.

## Gate 1 — Plan review (before build)
Review the design plan, not code. Ask:
- Is the **hero a thesis**, with the **store as subject** (name primary, not outranked by abstract copy)?
- Does the type system have an intentional **temperature** for this salon?
- Is every structural device **meaningful**, not decorative?
- Are the visuals **subject-specific** (real category cues), not the cream+serif+terracotta AI default?
- Exactly **one signature**? Restraint elsewhere?
- **Claim-safe** and **face-free** by design?

Revise until pass → only then authorize build.

## Gate 2 — Built-page review (after build + Playwright QA)
Review the deployed page + screenshots against the §4 checklist. Score each dimension; identify generic-default
smells and claim risks. Short of bar → **specific** fix instructions (not vague) → Codex revises → re-review.

## Output
A send-readiness verdict + decision material for Yu (quality score, claim-safety PASS/FAIL, what's confirmed
vs unknown). `sent=0`. No send is authorized by this gate — only "ready for manual-send card".

## Hard rails
- No self-approval by Codex; no passing 80-point work.
- Deploy allowed; send/email/form/DM/`sent=1`/git-push stay Yu-manual.
