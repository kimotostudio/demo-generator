# AGENTS.md

## Role

`demo-generator` is responsible for local demo generation, clean public deploy bundles, and public-demo handoff generation.

Pipeline position:

```text
lead-finder -> demo-generator -> human review -> playwright-automation
```

## Current State

- Consumes lead-finder normalized handoff CSV.
- Generated 22/22 local HTML demo files.
- Produced `output/handoff_with_demo_paths.csv`.
- Public demo URL handoff builder exists and is committed:
  - `afbe5bd Add public demo URL handoff builder`
- Public URL builder:
  - `scripts/build_public_demo_handoff.py`
- Placeholder-base test succeeded:
  - 22/22 HTTPS demo URLs
  - `demo_url_http=22`
  - `url(デモ)` HTTPS count = 22
  - Playwright strict preflight returned `status=ready`

## Main Entry Points

- `auto_generate.py`
  - Main operational generator.
  - Reads Excel worklogs or `--csv` normalized handoff inputs.
  - Writes HTML under `output/<template>/`.
  - Writes `output/generation_log.csv`.
- `scripts/merge_demo_paths.py`
  - Merges generated local demo paths back into a normalized handoff CSV.
- `scripts/build_public_demo_handoff.py`
  - Converts local demo paths to public demo URLs using `--demo-url-base`.
- `scripts/build_clean_deploy_folder.py`
  - Creates a public-safe deploy folder from referenced demo HTML/assets.

## Safe Work

- Local HTML generation.
- Local CSV transforms.
- Public URL handoff generation using a provided base URL.
- Clean deploy folder creation.
- `python3 -m py_compile` and local smoke tests.

## Do Not Do

- Do not perform outreach.
- Do not deploy without explicit permission.
- Do not publish internal CSVs.
- Do not commit generated output CSVs or bulk generated HTML.
- Do not add fake testimonials, fake client results, or misleading generated claims.
- Do not deploy `output/` directly if it contains CSVs, historical files, or lead-derived internal data.

## Public Deployment Rule

Create or use a clean `deploy_public/` folder for public deployment. It should contain only public-safe HTML/assets, preserving paths such as:

```text
A/<file>.html
A/images/<asset>
```

If `deploy_public/` is deployed as the site root, public demo URLs should resolve as:

```text
https://REAL_PUBLIC_DEMO_BASE/A/<file>.html
```

## Working Rules

- Read `/home/kimoto/projects/PROJECT_STATE.md` first.
- Inspect `git status --short` before edits.
- Keep patches small and repo-specific.
- Keep generated output ignored/local unless explicitly approved.
- End with a detailed `Report for ChatGPT` following `/home/kimoto/projects/prompts/final_report_template.md`, plus Discord notification when possible.
