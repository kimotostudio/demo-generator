#!/usr/bin/env python3
"""Merge generated demo paths back into a normalized handoff CSV."""

import argparse
import csv
import os


def read_csv(path):
    with open(path, 'r', encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def pick(row, *keys):
    for key in keys:
        value = row.get(key)
        if value and str(value).strip():
            return str(value).strip()
    return ''


def build_numbered_path(index, start_number, number_width):
    return f"{start_number + index:0{number_width}d}"


def build_demo_value(log_row, demo_url_base, *, url_style='file', netlify_path=''):
    relative_path = pick(log_row, 'relative_output_path', 'output_path')
    if not demo_url_base:
        return relative_path
    if url_style == 'numbered' and netlify_path:
        path_value = netlify_path
    else:
        filename = pick(log_row, 'output_filename')
        path_value = filename or os.path.basename(relative_path)
    return demo_url_base.rstrip('/') + '/' + path_value.lstrip('/')


def main():
    parser = argparse.ArgumentParser(
        description='Add demo_path/demo_url values to a normalized handoff CSV.'
    )
    parser.add_argument('--handoff-csv', required=True, help='Normalized handoff CSV')
    parser.add_argument('--generation-log', required=True, help='demo-generator output/generation_log.csv')
    parser.add_argument('--output', required=True, help='Merged output CSV path')
    parser.add_argument(
        '--demo-url-base',
        default='',
        help='Optional URL base. When omitted, demo_url/url(デモ) use the relative output path.',
    )
    parser.add_argument(
        '--url-style',
        choices=['file', 'numbered'],
        default='file',
        help='Build demo URLs from output filenames or numbered Netlify-style paths.',
    )
    parser.add_argument('--start-number', type=int, default=100, help='First number for --url-style numbered.')
    parser.add_argument('--number-width', type=int, default=4, help='Zero padding width for --url-style numbered.')
    args = parser.parse_args()

    handoff_rows = read_csv(args.handoff_csv)
    log_rows = read_csv(args.generation_log)
    log_by_id = {pick(row, 'id', 'lead_id'): row for row in log_rows if pick(row, 'id', 'lead_id')}

    if not handoff_rows:
        raise SystemExit('No handoff rows found')

    fieldnames = list(handoff_rows[0].keys())
    for field in [
        'demo_path',
        'demo_url',
        'url(デモ)',
        'netlify_path',
        'output_filename',
        'output_path',
        'relative_output_path',
        'display_name',
    ]:
        if field not in fieldnames:
            fieldnames.append(field)

    filled = 0
    for index, row in enumerate(handoff_rows):
        row_id = pick(row, 'id', 'lead_id')
        log_row = log_by_id.get(row_id)
        if not log_row:
            continue

        demo_path = pick(log_row, 'relative_output_path', 'output_path')
        netlify_path = ''
        if args.url_style == 'numbered':
            netlify_path = build_numbered_path(index, args.start_number, args.number_width)
        demo_value = build_demo_value(
            log_row,
            args.demo_url_base,
            url_style=args.url_style,
            netlify_path=netlify_path,
        )

        if demo_path:
            row['demo_path'] = demo_path
            row['output_filename'] = pick(log_row, 'output_filename')
            row['relative_output_path'] = pick(log_row, 'relative_output_path')
            row['output_path'] = pick(log_row, 'output_path')
        if netlify_path:
            row['netlify_path'] = netlify_path
        if demo_value:
            row['demo_url'] = demo_value
            row['url(デモ)'] = demo_value
        if not pick(row, 'display_name'):
            row['display_name'] = pick(row, 'business_name', 'salon_name', 'company_name', 'brand_name')
        filled += 1

    with open(args.output, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(handoff_rows)

    print(f'Merged demo paths for {filled}/{len(handoff_rows)} rows into {args.output}')


if __name__ == '__main__':
    main()
