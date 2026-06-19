#!/usr/bin/env python3
"""
Variant A salon demo-LP generator (v0)  —  Figma-free, code-template path.

profile JSON (salon_lead_profile.schema.json)
  -> slot mapping + copy rules + image-slot assignment + compliance guard
  -> renders templates/salon_booking_v2/template.html
  -> generated_demo/<slug>/index.html  (+ render_meta.json, quality.json)

Safe-local only: no network, no send, no deploy, stdlib only. Honesty first:
unknown fields stay as explicit [要確認: ...]; menus/prices/owner facts/testimonials
are NEVER invented; owner faces are NEVER auto-assigned.
"""
import argparse
import json
import os
import re
import sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TEMPLATE = os.path.join(REPO, "templates", "salon_booking_v2", "template.html")
DEFAULT_YEAR = "2026"

# --- compliance: copy that must never reach the recipient ----------------------
FORBIDDEN = [
    "治ります", "治る", "完治", "改善します", "改善", "効果保証", "効果",
    "必ず集客", "必ず", "集客保証", "売上アップ保証", "売上アップ",
    "医療", "治療", "痩身", "成果保証", "保証します",
]
# Benign template-internal strings that contain a forbidden substring but are not claims.
BENIGN_WHITELIST = ["スクロール効果"]  # JS comment in the design system, never a claim

SAMPLE_IMAGE_LABEL = "サンプル画像（要差し替え・写真許諾後）"

ATMOSPHERE_TINT = {
    "natural": ("#dfeade", "#6f8a7b"),
    "elegant": ("#efe6e8", "#bd806a"),
    "calm":    ("#e6e8ef", "#7b829a"),
    "warm":    ("#f1e6db", "#c08a52"),
}


def pick_tint(profile):
    kw = " ".join(profile.get("atmosphere_keywords", []) or []) + " " + profile.get("category", "")
    kw = kw.lower() + kw
    if any(w in kw for w in ["ナチュラル", "緑", "植物", "natural", "ヒーリング", "癒"]):
        return ATMOSPHERE_TINT["natural"]
    if any(w in kw for w in ["モダン", "シンプル", "カウンセリング", "calm", "静"]):
        return ATMOSPHERE_TINT["calm"]
    if any(w in kw for w in ["温", "よもぎ", "アロマ", "warm"]):
        return ATMOSPHERE_TINT["warm"]
    return ATMOSPHERE_TINT["elegant"]


def placeholder_svg(slug, kind, profile):
    """Elegant, on-brand SVG placeholder (data URI). No debug text; the page itself carries the
    'サンプル画像（要差し替え・写真許諾後）' caption/alt. Never a real photo or a real face."""
    bg, accent = pick_tint(profile)
    if kind == "owner":
        defs = (
            f"<defs><linearGradient id='og' x1='0' y1='0' x2='0' y2='1'>"
            f"<stop offset='0' stop-color='#fbf7f3'/><stop offset='1' stop-color='{bg}'/></linearGradient>"
            f"<radialGradient id='oh' cx='0.5' cy='0.42' r='0.6'>"
            f"<stop offset='0' stop-color='{accent}' stop-opacity='0.5'/>"
            f"<stop offset='1' stop-color='{accent}' stop-opacity='0'/></radialGradient></defs>"
        )
        body = (
            f"<rect width='800' height='1000' fill='url(#og)'/>"
            f"<rect width='800' height='1000' fill='url(#oh)'/>"
            f"<circle cx='400' cy='360' r='132' fill='{accent}' opacity='0.55'/>"
            f"<path d='M196 920 C232 700 318 596 400 596 C482 596 568 700 604 920 Z' fill='{accent}' opacity='0.5'/>"
            f"<rect x='70' y='66' width='660' height='868' rx='28' fill='none' stroke='{accent}' stroke-width='6' opacity='0.4'/>"
        )
        vb = "0 0 800 1000"
    else:
        defs = (
            f"<defs><linearGradient id='hg' x1='0' y1='0' x2='1' y2='1'>"
            f"<stop offset='0' stop-color='#fdfbf7'/><stop offset='0.55' stop-color='{bg}'/>"
            f"<stop offset='1' stop-color='{accent}'/></linearGradient>"
            f"<radialGradient id='hr' cx='0.78' cy='0.28' r='0.5'>"
            f"<stop offset='0' stop-color='#ffffff' stop-opacity='0.7'/>"
            f"<stop offset='1' stop-color='#ffffff' stop-opacity='0'/></radialGradient></defs>"
        )
        body = (
            f"<rect width='1600' height='1000' fill='url(#hg)'/>"
            f"<path d='M0 760 C320 650 520 700 760 600 C1010 496 1240 470 1600 600 L1600 1000 L0 1000 Z' fill='#ffffff' opacity='0.34'/>"
            f"<path d='M0 858 C360 780 560 812 820 740 C1080 668 1320 690 1600 800 L1600 1000 L0 1000 Z' fill='#ffffff' opacity='0.45'/>"
            f"<circle cx='1268' cy='286' r='150' fill='#ffffff' opacity='0.45'/>"
            f"<rect width='1600' height='1000' fill='url(#hr)'/>"
        )
        vb = "0 0 1600 1000"
    svg = f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='{vb}'>{defs}{body}</svg>"
    return "data:image/svg+xml," + quote(svg)


def assign_images(profile, slug):
    """v0 image-slot logic. Local+permitted images only; else neutral placeholder.
    Owner faces are NEVER auto-assigned. Records source + confidence."""
    meta = {}
    imgs = profile.get("images", {}) or {}
    permitted = bool(imgs.get("permission_to_use"))

    hero_local = imgs.get("hero_image_local_path")
    if hero_local and permitted and os.path.isfile(os.path.join(REPO, hero_local)):
        hero = os.path.relpath(os.path.join(REPO, hero_local), os.path.join(HERE, "generated_demo", slug))
        meta["hero_image"] = {"source": hero_local, "confidence": "high", "type": "local_permitted"}
    else:
        hero = placeholder_svg(slug, "hero", profile)
        meta["hero_image"] = {"source": "neutral_svg_placeholder", "confidence": "low", "type": "placeholder"}

    # Owner image: placeholder unless explicitly local+permitted (still never a generic face stock).
    owner_local = imgs.get("owner_image_local_path")
    if owner_local and permitted and os.path.isfile(os.path.join(REPO, owner_local)):
        owner = os.path.relpath(os.path.join(REPO, owner_local), os.path.join(HERE, "generated_demo", slug))
        meta["owner_image"] = {"source": owner_local, "confidence": "high", "type": "local_permitted"}
    else:
        owner = placeholder_svg(slug, "owner", profile)
        meta["owner_image"] = {"source": "neutral_svg_placeholder", "confidence": "low",
                               "type": "placeholder", "note": "owner faces never auto-assigned"}
    return hero, owner, meta


CONTACT_LABELS = {
    "form": "お問い合わせフォーム", "フォーム": "お問い合わせフォーム",
    "line": "LINE", "tel": "お電話", "電話": "お電話", "phone": "お電話",
    "ig_dm": "Instagram DM", "instagram": "Instagram", "dm": "Instagram DM",
    "hotpepper": "ホットペッパー", "reserva": "予約フォーム", "mail": "メール",
}


def humanize_contact(raw, fallback_label="予約・連絡導線"):
    """'form;LINE;tel' -> 'お問い合わせフォーム・LINE・お電話' (natural, customer-facing)."""
    if not raw or not str(raw).strip():
        return tbd(fallback_label)
    parts, seen = [], set()
    for tok in re.split(r"[;,/、・\s]+", str(raw).strip()):
        if not tok:
            continue
        label = CONTACT_LABELS.get(tok.lower().strip(), tok.strip())
        if label not in seen:
            seen.add(label)
            parts.append(label)
    return "・".join(parts) if parts else tbd(fallback_label)


def tbd(label):
    return f"[要確認: {label}]"


def join_or_tbd(items, label):
    items = [i for i in (items or []) if str(i).strip()]
    return "・".join(items) if items else tbd(label)


def derive_copy(profile):
    """Copy rules: build personalized, soft, non-medical strings from real fields."""
    area = " ".join(x for x in [profile.get("city", ""), profile.get("area_or_station", "")] if x).strip()
    cat = profile.get("category", "").strip()
    atmos = "・".join(profile.get("atmosphere_keywords", []) or [])
    name = profile.get("business_name", "").strip() or "サロン"

    hero = profile.get("hero_copy") or (
        f"{area or '地域'}の{cat or 'サロン'}｜{atmos or '落ち着いた'}空間で、自分のための時間を"
    )
    cta = profile.get("cta_text") or "ご予約・お問い合わせ"

    target = profile.get("target_customer") or (
        f"{area}で{cat}を初めて検討する方に、雰囲気と流れが伝わりやすいご案内です" if area and cat
        else tbd("対象となるお客様像")
    )
    strengths = join_or_tbd(profile.get("visible_strengths"), "サロンの強み（公開情報から）")

    op = profile.get("owner_presence", "unknown")
    if op in ("high", "medium") and profile.get("owner_name"):
        owner_name = profile["owner_name"]
        owner_words = profile.get("owner_words") or tbd("代表者ご本人の一言に差し替え")
        owner_profile = profile.get("owner_profile") or tbd("掲載してよいプロフィール文（公開情報あり）")
    else:
        owner_name = profile.get("owner_name") or tbd("代表者名")
        owner_words = tbd("代表者ご本人の一言に差し替え")
        owner_profile = tbd("掲載してよいプロフィール文")

    return {
        "hero": hero, "cta": cta, "target": target, "strengths": strengths,
        "owner_name": owner_name, "owner_words": owner_words, "owner_profile": owner_profile,
        "area": area or tbd("地域表記"), "name": name, "atmos": atmos or tbd("雰囲気キーワード"),
    }


def build_slots(profile, year):
    c = derive_copy(profile)
    booking_url = (profile.get("reservation_url") or profile.get("website_url")
                   or profile.get("instagram_url") or "#")
    contact_human = humanize_contact(profile.get("contact_method"))
    photo_tone = f"写真トーン: {c['atmos']}"
    first_visit = (f"まずはメニューの違いをご覧いただき、{contact_human}"
                   "からお気軽にお問い合わせください。"
                   if not str(contact_human).startswith("[要確認")
                   else "まずはメニューの違いをご覧いただき、ご希望の方法でお問い合わせください。")
    slots = {
        "SALON_NAME": c["name"],
        "AREA": c["area"],
        "MENU_NAME": join_or_tbd(profile.get("main_menu_names"), "主要メニュー名（実在情報）"),
        "ATMOSPHERE": c["atmos"],
        "OWNER_WORDS": c["owner_words"],
        "PHOTO_TONE": photo_tone,
        "BOOKING_ROUTE": contact_human,
        "PRICE_RANGE": profile.get("price_range") or tbd("正しい価格帯"),
        "TARGET_CUSTOMER": c["target"],
        "STRENGTHS": c["strengths"],
        "FIRST_VISIT_ROUTE": first_visit,
        "OWNER_NAME": c["owner_name"],
        "OWNER_PROFILE": c["owner_profile"],
        "FIRST_VISIT_PRICE": profile.get("first_visit_price") or tbd("初回向け料金"),
        "REGULAR_MENU_NAME": profile.get("regular_menu_name") or tbd("通常コース名"),
        "REGULAR_PRICE": profile.get("regular_price") or tbd("通常料金"),
        "SEASONAL_MENU_NAME": profile.get("seasonal_menu_name") or tbd("季節/新メニュー名"),
        "SEASONAL_PRICE": profile.get("seasonal_price") or tbd("掲載する料金"),
        "STATION_INFO": profile.get("area_or_station") or tbd("最寄り駅・アクセス"),
        "PARKING_INFO": profile.get("parking_info") or tbd("駐車場案内"),
        "OPEN_HOURS": profile.get("open_hours") or tbd("営業時間・最終受付"),
        "BOOKING_URL": booking_url,
        "BOOKING_BUTTON_LABEL": c["cta"],
        "YEAR": str(year),
    }
    return slots


def scan_forbidden(text):
    hits = []
    for w in FORBIDDEN:
        idx = 0
        while True:
            i = text.find(w, idx)
            if i == -1:
                break
            ctx = text[max(0, i - 6):i + len(w) + 6]
            if not any(b in ctx for b in BENIGN_WHITELIST):
                hits.append((w, ctx))
            idx = i + len(w)
    return hits


def render(profile, year, out_dir):
    with open(TEMPLATE, encoding="utf-8") as f:
        tpl = f.read()
    slug = profile.get("slug") or re.sub(r"[^a-zA-Z0-9_-]+", "-",
                                         profile.get("business_name", "salon")).strip("-").lower() or "salon"
    dest = os.path.join(out_dir, slug)
    os.makedirs(dest, exist_ok=True)

    slots = build_slots(profile, year)
    hero_img, owner_img, img_meta = assign_images(profile, slug)
    slots["HERO_IMAGE"] = hero_img
    slots["OWNER_IMAGE"] = owner_img

    # Compliance guard on INJECTED VALUES (precise — avoids template false positives).
    injected_text = "\n".join(v for k, v in slots.items() if k not in ("HERO_IMAGE", "OWNER_IMAGE"))
    value_hits = scan_forbidden(injected_text)

    html = tpl
    for k, v in slots.items():
        html = html.replace("{{" + k + "}}", str(v))
    # tidy: collapse accidental double punctuation from template+value concatenation
    html = html.replace("。。", "。").replace("、。", "。")

    leftover = sorted(set(re.findall(r"\{\{([A-Z_0-9]+)\}\}", html)))
    full_hits = scan_forbidden(html)

    with open(os.path.join(dest, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    with open(os.path.join(dest, "render_meta.json"), "w", encoding="utf-8") as f:
        json.dump({"slug": slug, "images": img_meta,
                   "source_notes": profile.get("source_notes", ""),
                   "risk_flags": profile.get("risk_flags", [])}, f, ensure_ascii=False, indent=2)

    quality = run_quality_checklist(profile, html, slots, leftover, value_hits, full_hits, img_meta)
    with open(os.path.join(dest, "quality.json"), "w", encoding="utf-8") as f:
        json.dump(quality, f, ensure_ascii=False, indent=2)
    return slug, dest, quality


def run_quality_checklist(profile, html, slots, leftover, value_hits, full_hits, img_meta):
    def has_real(v):
        return bool(v) and not str(v).startswith("[要確認")
    checks = {
        "salon_name_present": has_real(slots["SALON_NAME"]),
        "area_present": has_real(slots["AREA"]),
        "category_known": bool(profile.get("category")),
        "menu_from_real_info": has_real(slots["MENU_NAME"]),
        "no_forbidden_in_injected_copy": len(value_hits) == 0,
        "no_forbidden_in_full_page": len(full_hits) == 0,
        "booking_route_present": slots["BOOKING_URL"] not in ("#", ""),
        "owner_or_atmosphere_reflected": has_real(slots["OWNER_NAME"]) or has_real(slots["ATMOSPHERE"]),
        "no_invented_owner_photo": all(m.get("type") == "placeholder" or m.get("type") == "local_permitted"
                                       for m in img_meta.values()),
        "sample_image_label_present": "サンプル画像" in html,
        "proposal_draft_label_present": "提案サンプル" in html,
        "all_slots_filled": len(leftover) == 0,
        "no_external_send_performed": True,
    }
    checks["_leftover_slots"] = leftover
    checks["_forbidden_in_copy"] = value_hits
    checks["_forbidden_in_page"] = full_hits
    checks["_open_to_confirm"] = sorted(k for k, v in slots.items()
                                        if isinstance(v, str) and v.startswith("[要確認"))
    hard = [k for k in checks if k.startswith(("no_", "all_", "sample_", "proposal_", "salon_"))
            and isinstance(checks[k], bool)]
    checks["_pass"] = all(checks[k] for k in hard)
    return checks


def main():
    ap = argparse.ArgumentParser(description="Variant A salon demo-LP generator (v0)")
    ap.add_argument("--profile", help="single profile JSON")
    ap.add_argument("--all", action="store_true", help="render every JSON in sample_leads/")
    ap.add_argument("--year", default=DEFAULT_YEAR)
    ap.add_argument("--out", default=os.path.join(HERE, "generated_demo"))
    args = ap.parse_args()

    profiles = []
    if args.profile:
        profiles = [args.profile]
    elif args.all:
        d = os.path.join(HERE, "sample_leads")
        profiles = [os.path.join(d, f) for f in sorted(os.listdir(d)) if f.endswith(".json")]
    else:
        ap.error("pass --profile <file> or --all")

    overall = True
    for p in profiles:
        with open(p, encoding="utf-8") as f:
            profile = json.load(f)
        slug, dest, q = render(profile, args.year, args.out)
        status = "PASS" if q["_pass"] else "FAIL"
        print(f"[{status}] {slug} -> {os.path.relpath(dest, REPO)}  "
              f"(要確認 {len(q['_open_to_confirm'])} / forbidden {len(q['_forbidden_in_page'])})")
        overall = overall and q["_pass"]
    print("\nOVERALL:", "PASS" if overall else "FAIL")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()
