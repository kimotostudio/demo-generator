import os
import shutil
import glob
from pathlib import Path

ROOT = Path('.')
SNS_DIR = ROOT / 'sns'
TEMPLATES_SRC = ROOT / 'templates'
TEMPLATES_DST = SNS_DIR / 'templates'

# prefer images from output/A/images; fallback to input/images
IMG_SRC1 = ROOT / 'output' / 'A' / 'images'
IMG_SRC2 = ROOT / 'input' / 'images'
IMG_DST = SNS_DIR / 'images'

os.makedirs(SNS_DIR, exist_ok=True)

# copy templates folder
if TEMPLATES_SRC.exists():
    if TEMPLATES_DST.exists():
        shutil.rmtree(TEMPLATES_DST)
    shutil.copytree(TEMPLATES_SRC, TEMPLATES_DST)
else:
    print('templates/ not found — aborting')
    raise SystemExit(1)

# copy images
if IMG_SRC1.exists():
    src_images = IMG_SRC1
elif IMG_SRC2.exists():
    src_images = IMG_SRC2
else:
    print('No images folder found under output/A/images or input/images — aborting')
    raise SystemExit(1)

if IMG_DST.exists():
    shutil.rmtree(IMG_DST)
shutil.copytree(src_images, IMG_DST)

# list available image filenames
image_files = [p.name for p in sorted(IMG_DST.iterdir()) if p.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp', '.gif')]
if not image_files:
    print('No image files found in', IMG_DST)
    raise SystemExit(1)

# templates A-F
templates = [c for c in 'ABCDEF']

for tpl in templates:
    tpl_path = TEMPLATES_DST / f'variant{tpl}.html'
    if not tpl_path.exists():
        # skip missing template but create folder
        out_folder = SNS_DIR / tpl
        out_folder.mkdir(parents=True, exist_ok=True)
        continue

    tpl_text = tpl_path.read_text(encoding='utf-8')
    out_folder = SNS_DIR / tpl
    out_folder.mkdir(parents=True, exist_ok=True)

    # generate 5 variations
    for i in range(5):
        main_img = image_files[i % len(image_files)]
        therapist_img = image_files[(i+1) % len(image_files)]

        html = tpl_text
        html = html.replace('{{BRAND_NAME}}', 'demo site')
        html = html.replace('{{IMAGE_URL}}', f'images/{main_img}')
        html = html.replace('{{THERAPIST_IMAGE_URL}}', f'images/{therapist_img}')
        html = html.replace('{{REFERENCE_URL}}', '')
        html = html.replace('{{YEAR}}', '')
        html = html.replace('{{GALLERY_HTML}}', '')

        # neutralize some CTAs
        html = html.replace('予約', '詳細')
        html = html.replace('お問い合わせ', '詳しくはこちら')
        html = html.replace('キャンペーン', 'お知らせ')
        html = html.replace('初回限定', 'お試し')

        out_name = f'demo_site_{i+1}{tpl}.html'
        out_path = out_folder / out_name
        out_path.write_text(html, encoding='utf-8')

    # copy images into this template folder (so images/ at same level)
    dst_images = out_folder / 'images'
    if dst_images.exists():
        shutil.rmtree(dst_images)
    shutil.copytree(IMG_DST, dst_images)

print('SNS demo generation complete. Check the sns/ folder.')
