#!/usr/bin/env python3
import os
import re
from datetime import datetime
import auto_generate as ag


def main():
    excel_path = os.path.join('input', '営業リスト(北海道、愛知、福岡).xlsx')
    print('読み込み: ', excel_path)
    rows = ag.read_excel(excel_path)
    if not rows:
        print('Excelからデータが読み取れませんでした。openpyxlが必要です。')
        return

    start = 8018
    end = 8055
    generated = 0

    for row in rows:
        normalized = ag.normalize_column_names(row)
        id_val = normalized.get('id', '')
        nums = re.findall(r"\d+", str(id_val))
        if not nums:
            continue
        id_int = int(nums[0])
        if start <= id_int <= end:
            # 生成（テンプレートはデフォルト 'A' を使用）
            res = ag.generate_html_from_row(row, datetime.now().year, template='A')
            if res:
                generated += 1

    print(f'完了: {generated} 件のHTMLを生成しました（ID {start:05d} - {end:05d} を対象）。')


if __name__ == '__main__':
    main()
