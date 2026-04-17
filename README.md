# Demo Generator

Template-based generation of personalized demo landing pages and outreach assets for Japanese small-business prospects.

## Overview

Demo Generator turns approved lead or worklog data into lightweight, shareable HTML demo pages. In the broader workflow, `lead-finder` identifies promising businesses, this repository generates a tailored demo page or preview asset for each target, and the outreach layer uses those assets during contact or follow-up. The current implementation is practical and operational: it reads TSV or Excel-based lead lists, applies existing HTML templates, assigns images, and writes static output files for review.

## Why This Project Exists

For local-business outreach, a generic pitch is weak. A fast, concrete demo page gives the prospect something specific to react to. This repository reduces the manual work of building those first-pass assets one by one and keeps the process repeatable across batches.

## Core Features

- Generate static HTML demo pages from operational Excel worklogs or a small TSV sample list
- Maintain multiple reusable template variants (`A` through `F`)
- Auto-assign page images from existing pools using simple atmosphere heuristics
- Support deterministic batch generation with `--start-id`, `--template`, `--output-template`, and `--excel`
- Write generation logs to CSV for batch review
- Produce optional SNS/demo preview sets from the same templates and images

## Workflow

1. Start with approved leads from `lead-finder` or an internal worklog.
2. Prepare input data in `input/` as either an Excel file for the operational path or `input/list.tsv` for the simple sample path.
3. Run the generator against a selected template.
4. Review the generated HTML and `output/generation_log.csv`.
5. Use the page or asset in the downstream outreach workflow.

Pipeline context:

`lead-finder -> demo-generator -> outreach automation`

## Recommended Usage

### 1. Main operational path: `auto_generate.py`

Use this when generating pages from Excel-based worklogs.

```bash
pip install openpyxl
python auto_generate.py
```

Behavior:

- scans `input/` for the first Excel file whose name includes `営業`
- reads the active sheet
- normalizes brand name, URL, and ID fields
- writes HTML under `output/<TEMPLATE>/`
- writes `output/generation_log.csv`

Useful examples:

```bash
python auto_generate.py --excel "input/営業ログ(東京).xlsx" --template A --output-template A
python auto_generate.py --start-id 8000 --template B --output-template B
```

Operational note:

- `auto_generate.py` expects page images to already exist under `output/<template>/images/`

### 2. Simple sample path: `generate.py`

Use this for a quick, repo-local preview based on `input/list.tsv`.

```bash
python generate.py
```

This writes files like `output/demo01A_index.html` and references images from `input/images/`.

### 3. Optional preview asset path: `scripts/create_sns_site.py`

Use this to generate preview/demo variants into `sns/`.

```bash
python scripts/create_sns_site.py
```

## Tech Stack

- Python
- Standard library: `csv`, `os`, `argparse`, `datetime`, `random`
- `openpyxl` for Excel input
- Static HTML/CSS templates in `templates/`
- Local image assets in `input/images/` and `output/<template>/images/`

## Project Structure

```text
demo-generator/
|-- auto_generate.py        # Main operational generator
|-- generate.py             # Simple TSV-based generator
|-- templates/              # Source HTML templates (A-F)
|-- input/                  # Sample input, source images, operational worklogs
|-- output/                 # Generated HTML and logs
|-- scripts/                # Helper scripts and preview generation
|-- sns/                    # Generated preview/demo pages
|-- README.md
|-- AGENTS.md
`-- .gitignore
```

Notes:

- `auto_generate.py` is the recommended public starting point.
- `generate.py` is the simpler sample path.
- `scripts/generate_by_id_range.py` is a narrow helper, not the main interface.
- `extract_and_run.py` and some files in `scripts/` are currently empty placeholders.

## Setup

Requirements in the current checkout are minimal:

- Python 3
- `openpyxl` for the Excel-based workflow

Install:

```bash
pip install openpyxl
```

The repository does not currently include a pinned `requirements.txt` or `pyproject.toml`.

## Usage

### Excel-based batch generation

```bash
python auto_generate.py
python auto_generate.py --excel "input/営業ログ(東京).xlsx"
python auto_generate.py --start-id 8000 --template A --output-template A
```

### TSV-based sample generation

```bash
python generate.py
```

### Preview or SNS sample generation

```bash
python scripts/create_sns_site.py
```

## Example Output

Main operational output:

```text
output/
|-- A/
|   |-- 08000A.html
|   |-- 08001A.html
|   `-- images/
`-- generation_log.csv
```

Simple sample output:

```text
output/demo01A_index.html
output/demo06B_index.html
```

Sample TSV row:

```tsv
id	brand_name	reference_url	template	image	therapist_image
demo01	Demo Site	https://example.com	A	image01.jpg	image26.jpg
```

## Limitations

- Personalization is currently template-driven; it does not generate custom copy with an LLM
- The Excel path assumes operational worklogs with recognizable columns for brand name, URL, and optional ID
- The repository currently mixes source files with generated output and local working data
- There is no automated test suite or pinned dependency manifest in the current checkout
- Some tracked folders in the current repo, especially `output/`, `sns/`, and private worklogs under `input/`, are better treated as local or generated data than permanent public source

## Related Repositories

- `lead-finder`: discovers and scores candidate businesses
- `demo-generator`: generates personalized demo pages and assets
- `playwright-automation`: uses approved outputs during outreach execution

## Roadmap

- Keep the public README centered on the operational path and the sample path
- Separate source assets from generated outputs more cleanly
- Add a small redacted sample dataset for public use
- Add a pinned dependency file and a lightweight verification path
- Reduce tracked bulk output so the repository is easier to review