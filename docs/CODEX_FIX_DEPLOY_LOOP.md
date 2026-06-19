# CODEX_FIX_DEPLOY_LOOP

How Codex (Professional Web Designer / Frontend Implementer) applies fixes to a personal-salon demo LP and
deploys it for review. Codex is the hands; Claude reviews; Yu decides the send.

## Skill requirement
> **Before modifying any demo UI, Codex must consult `skills/personal-salon-frontend-design/SKILL.md`.**
> Fixes are derived from the validated design plan and the skill's principles — not improvised mid-build.

## Loop
1. **Receive fix instructions** from the Claude review gate (specific, scoped to listed target files).
2. **Apply fixes** per the skill (typography temperature, hero hierarchy, structure-with-meaning, remove
   AI-default smell, claim-safe copy, face-free visuals). Stay within the task's `## Target files`.
3. **Local self-QA** — re-run the §4 checklist before deploying.
4. **Deploy** — preview or public production is **allowed/AUTO** (deploy ≠ send). Re-deploys/rollbacks allowed;
   prefer fixing forward or taking a page down over leaving a bad page up.
5. **Return deliverable** — diff + preview/public URL + screenshots + report (safety status, files changed,
   checks run, next blocker, approval needed?). `sent=0`.

## Hard rails
- Scope discipline: do not edit files outside the listed target files; if another file seems necessary, STOP
  and report instead of editing it.
- Deployed content must stay honest, claim-safe, and secret-free (no .env/tokens/webhooks).
- No send / email / form submit / DM / `sent=1` — those are Yu-manual.
