# AGENTS.md

## Repository Purpose

`demo-generator` is the page-generation layer in a broader outreach workflow:

`lead-finder -> demo-generator -> outreach automation`

Its job is to turn approved prospect data into reviewable demo pages or preview assets that can be used in real outreach. Treat it as an operational, template-driven generator. Do not describe it as an AI copy generator unless that behavior exists in code.

## Recommended Entry Points

Use these in this order when explaining or maintaining the repository:

1. `auto_generate.py`
   Main operational entry point. Reads Excel-based worklogs from `input/` or `--excel`, assigns images, writes HTML under `output/<template>/`, and writes `output/generation_log.csv`.

2. `generate.py`
   Simpler TSV-based path for local preview and repo-safe examples. Reads `input/list.tsv` and writes `output/*_index.html`.

3. `scripts/create_sns_site.py`
   Optional preview/demo generator. Builds `sns/` variants from the existing templates and images.

4. `scripts/generate_by_id_range.py`
   Narrow helper for targeted generation ranges. Not the recommended public entry point.

5. `extract_and_run.py` and zero-byte helper scripts in `scripts/`
   Treat these as inactive placeholders unless they are implemented later.

## Important Directories and Files

- `templates/`
  Source HTML templates. These are core repository assets and should remain tracked.

- `input/`
  Mixed directory containing sample input, source images, and operational worklogs. Public cleanup should distinguish sample assets from private work data.

- `input/images/`
  Source images used by the simple path and some preview flows. Keep only assets that are safe and necessary to publish.

- `output/`
  Generated HTML, logs, and batch artifacts. This is operational output, not source.

- `sns/`
  Generated preview/demo pages and copied images. This is derived output.

- `scripts/`
  Helper scripts. Some are active, some are placeholders.

- `auto_generate.py`
  Main operational generator.

- `generate.py`
  Small sample/demo generator.

- `README.md`
  Public-facing repository overview.

- `AI_GUIDE.md`, `CLAUDE.md`, `CONSTITUTION.md`
  Internal maintenance notes. These are not the main public entry point and should not drive the public README.

## Working Rules

- Preserve behavior of `auto_generate.py` and `generate.py`.
- Prefer minimal, high-impact cleanup over structural refactors.
- Do not move `templates/` or change template filenames casually.
- Do not change placeholder names without checking every template and both generators.
- Do not commit real client data, private worklogs, or bulk generated output.
- Keep the public repo grounded in actual implementation, not aspirational architecture.

## Output Consistency Rules

- `auto_generate.py` writes HTML to `output/<output_template>/<id><output_template>.html`.
- `auto_generate.py` writes `output/generation_log.csv` with keys currently derived from:
  - `id`
  - `brand_name`
  - `reference_url`
  - `template`
  - `image`
  - `therapist_image`
  - `atmosphere`
- `generate.py` writes `output/<id><template>_index.html`.
- Current template placeholders are:
  - `{{BRAND_NAME}}`
  - `{{IMAGE_URL}}`
  - `{{REFERENCE_URL}}`
  - `{{YEAR}}`
  - `{{THERAPIST_IMAGE_URL}}`
- Path behavior differs by entry point:
  - `auto_generate.py` expects images under `output/<template>/images/`
  - `generate.py` points to `input/images/`
- If you change output naming or placeholder contracts, update code, sample commands, and README together.

## Documentation Rules

- Keep the root README concise and truthful.
- Present `auto_generate.py` as the main operational path.
- Present `generate.py` as the simple sample path.
- Do not claim LLM-based generation unless that exists in code.
- Use real commands and actual file paths from the repository.
- Call out when directories are generated output rather than maintained source.
- Mention the Japan/local-business outreach context explicitly.

## Cleanup and Refactor Rules

Safe cleanup:

- README and maintenance docs
- `.gitignore` improvements
- Small non-breaking helper cleanup
- Redacted sample data additions
- Removing tracked caches or generated artifacts in a deliberate, reviewed pass

Risky cleanup:

- Moving or renaming template files
- Changing image path conventions
- Restructuring `input/`, `output/`, or `sns/` without tracing script expectations
- Deleting helper scripts just because they look old
- Removing tracked assets without confirming whether they are still needed for generation

If the root looks cluttered, document the split between source and generated data first. Do not force a refactor just for appearance.

## Current Priorities for Public Portfolio Quality

1. Keep the README easy to scan in under a minute.
2. Make the operational path and sample path obvious.
3. Reduce tracked generated output and private worklogs over time.
4. Add a pinned dependency file or a minimal reproducible setup path.
5. Keep one small public sample dataset and one small sample output set.
6. Leave the generator logic stable while improving repo hygiene.

## Public Tracking Guidance

Should usually stay tracked:

- `templates/`
- core generator scripts
- small redacted sample input such as `input/list.tsv`
- only the minimum safe image assets required for public examples

Should usually be ignored or removed from public tracking:

- `__pycache__/`
- `.venv/`
- `.claude/`
- `output/`
- `sns/`
- private Excel and CSV worklogs under `input/`
- editor cruft, logs, and shortcuts

Important: updating `.gitignore` does not remove files that are already tracked. If you want a truly clean public repo, follow up with a deliberate de-tracking pass.