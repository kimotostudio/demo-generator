#!/usr/bin/env python3
"""
LP生成スクリプト
input/list.tsvを読み込み、テンプレートを適用してHTMLファイルを生成します
"""

import csv
import os
from datetime import datetime


def read_template(template_name):
    """テンプレートファイルを読み込む"""
    template_path = os.path.join('templates', f'variant{template_name}.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def replace_placeholders(template, brand_name, image_url, reference_url, year, therapist_image_url):
    """プレースホルダーを実際の値に置換"""
    result = template.replace('{{BRAND_NAME}}', brand_name)
    result = result.replace('{{IMAGE_URL}}', image_url)
    result = result.replace('{{REFERENCE_URL}}', reference_url)
    result = result.replace('{{YEAR}}', str(year))
    result = result.replace('{{THERAPIST_IMAGE_URL}}', therapist_image_url)
    return result


def generate_html(row, year):
    """1行分のHTMLを生成"""
    id_val = row['id']
    brand_name = row['brand_name']
    reference_url = row['reference_url']
    template = row['template']
    image = row['image']
    therapist_image = row.get('therapist_image', '')

    # 画像パスを相対パスに変換
    image_url = f'../input/images/{image}'
    therapist_image_url = f'../input/images/{therapist_image}' if therapist_image else ''

    # テンプレート読み込み
    template_content = read_template(template)

    # プレースホルダー置換
    html_content = replace_placeholders(
        template_content,
        brand_name,
        image_url,
        reference_url,
        year,
        therapist_image_url
    )

    # 出力ファイル名
    output_filename = f'{id_val}{template}_index.html'
    output_path = os.path.join('output', output_filename)

    # ファイル書き出し
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f'[OK] {output_filename} を生成しました')


def main():
    """メイン処理"""
    # 現在の年を取得
    current_year = datetime.now().year

    # outputディレクトリが存在しない場合は作成
    os.makedirs('output', exist_ok=True)

    # TSVファイル読み込み
    tsv_path = os.path.join('input', 'list.tsv')

    with open(tsv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')

        for row in reader:
            generate_html(row, current_year)

    print(f'\n生成完了！output/ フォルダを確認してください。')


if __name__ == '__main__':
    main()
