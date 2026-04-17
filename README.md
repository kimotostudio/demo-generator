# Demo Generator

スピリチュアル・ヒーリングサロン向けLP自動生成ツール

## 概要

営業ログ（Excel/CSV）から自動でプロフェッショナルなHTMLランディングページを一括生成します。
画像は店舗の雰囲気に合わせて自動で割り当てられます。

## 特徴

✨ **自動生成**: 営業リストから一括でLP生成
🎨 **画像自動割り当て**: 店舗名から雰囲気を推測して最適な画像を選択
📊 **Excel対応**: .xlsx/.xls形式の営業ログを直接読み込み
🎯 **プロ品質**: 月額1万円で販売できるクオリティのデザイン
📱 **完全レスポンシブ**: モバイルファーストデザイン

## 使い方

### 方法1: 営業ログから自動生成（推奨）

```bash
# 営業ログ(Excel)をinput/フォルダに配置
# ファイル名に「営業」を含める必要があります

python auto_generate.py
```

**営業ログのフォーマット:**
- 必須列: `店名` または `ブランド名`
- 任意列: `url`, `id`
- 店名が入っていれば自動で検出します

**自動機能:**
- 画像の雰囲気自動判定
  - `モダン/modern/スタジオ` → モダンな画像（image17-25）
  - `ナチュラル/natural/森/緑` → ナチュラルな画像（image09-16）
  - その他 → エレガントな画像（image01-08）
- 施術者画像の自動割り当て（image26-33）
- IDの自動生成（店名のハッシュ値から生成）
- 生成ログの出力（output/generation_log.csv）

### 方法2: TSVファイルから生成

```bash
# input/list.tsv を編集
python generate.py
```

**list.tsvのフォーマット:**
```tsv
id	brand_name	reference_url	template	image	therapist_image
0001	KIMOTO STUDIO	https://kimotostudio21.netlify.app	A	image01.jpg	image26.jpg
```

## 必要環境

- Python 3.6以上
- openpyxl（Excel読み込み用）

```bash
pip install openpyxl
```

## フォルダ構成

```
demo-generator/
├── input/
│   ├── 営業ログ(東京).xlsx    # 営業リスト（自動生成用）
│   ├── list.tsv               # 手動生成用リスト
│   └── images/                # 画像ファイル（image01.jpg～image33.jpg）
├── templates/
│   └── variantA.html          # テンプレートファイル
├── output/                    # 生成されたHTML
│   └── generation_log.csv     # 生成ログ
├── generate.py                # TSVから生成
├── auto_generate.py           # Excelから自動生成
└── README.md
```

## 画像について

### メインビジュアル画像（全25枚）
- **image01-08**: エレガント・上品な雰囲気
- **image09-16**: ナチュラル・癒し系
- **image17-25**: モダン・洗練された雰囲気

### 施術者画像（全8枚）
- **image26-33**: 施術者プロフィール用

## テンプレートについて

### Variant A（variantA.html）
- **デザイン**: スピリチュアル・ヒーリングサロン向け
- **カラー**: 淡いピンク・ベージュ系
- **特徴**:
  - 固定ヘッダー（Glassmorphism）
  - 100vhファーストビュー（パララックス）
  - 施術者プロフィールセクション
  - スクロール連動アニメーション
  - モバイルファースト

### セクション構成
1. 固定ヘッダー
2. ファーストビュー（100vh、パララックス背景）
3. コンセプト
4. 施術者プロフィール
5. サービスメニュー
6. お客様の声
7. アクセス・料金
8. CTA（お問い合わせ）
9. フッター（SNSアイコン付き）

### プレースホルダー
- `{{BRAND_NAME}}`: サロン名
- `{{IMAGE_URL}}`: メインビジュアル画像のパス
- `{{THERAPIST_IMAGE_URL}}`: 施術者画像のパス
- `{{REFERENCE_URL}}`: 公式サイトURL
- `{{YEAR}}`: 現在の年（自動取得）

## 出力例

```
output/0001A_index.html  # KIMOTO STUDIO
output/0002A_index.html  # 癒しの空間 ひかり
output/0003A_index.html  # Reiki Salon 和
...
```

各HTMLファイルは約44KBで、すべてのCSS/JSがインライン化されているため、
1ファイルで完結します。

## カスタマイズ

### 新しいテンプレートを追加
1. `templates/variantB.html` を作成
2. `list.tsv` の `template` 列に `B` を指定
3. `python generate.py` を実行

### 雰囲気の判定ルールをカスタマイズ
`auto_generate.py` の `detect_atmosphere()` 関数を編集してください。

### 画像プールを変更
`auto_generate.py` の `IMAGE_POOLS` 辞書を編集してください。

## トラブルシューティング

### openpyxlがインストールされていない
```bash
pip install openpyxl
```

### 営業ログが読み込めない
- ファイル名に「営業」が含まれているか確認
- Excel形式（.xlsx または .xls）であることを確認
- 「店名」または「ブランド名」の列があることを確認

### 画像が表示されない
- input/images/ に image01.jpg～image33.jpg があることを確認
- HTMLファイルから見た相対パス `../input/images/` が正しいか確認

## パフォーマンス

- 146件の営業ログから約10秒で140件のHTMLを生成
- 各HTMLファイルは約44KB
- 生成ログCSVで結果を確認可能

## ライセンス

MIT License

## サポート

問題が発生した場合は、`output/generation_log.csv` を確認してください。
各ファイルがどの画像・雰囲気で生成されたかが記録されています。
