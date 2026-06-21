#!/usr/bin/env python3
"""gen_naturally_lp — generate the Naturally per-lead demo LP from the sales_lp_demo_v2 standard.

Naturally is NOT in console_state.json (sent=0; no Console entry until demo QA passes), so the
main gen_per_lead_lp pipeline (which reads console_state) cannot emit it. This driver reuses the
SAME deterministic gen() (fixed v2 template, prices stripped, claim-safe, source-faithful) with a
hand-built, source-backed lead dict for Naturally.

Source of fields: lead-finder route verification + executive handoff + sales-plugin enriched CSV
(2026-06-20). Claim scope = dry-head-spa / relaxation ONLY (exclude 痩身/小顔/Before-After/効果/改善).
Safe-local: writes index.html + copies the standard face-free asset set. No network, no deploy, no send.
"""
import sys, importlib.util, os

DG = "/home/kimoto/projects/demo-generator"
spec = importlib.util.spec_from_file_location("gpll", f"{DG}/scripts/gen_per_lead_lp.py")
gpll = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gpll)

# --- source-backed Naturally lead (claim-safe head-spa scope) ---
naturally = {
    "lead_id": "naturally",
    "business_name": "Naturally（ナチュラリー）",
    "category": "ドライヘッドスパ",          # head-spa scope only (esthe pages excluded by claim scope)
    "city": "佐賀県小城市",
    # route = booking_plus_inquiry: contact form + Reserva booking + LINE + Instagram
    "send_route": "お問い合わせフォーム / ご予約サイト / LINE / Instagram",
    # source confirms dry head spa; second line kept generic + claim-safe (no efficacy wording)
    "services": ["ドライヘッドスパ", "リラクゼーション"],
}

disclosure = ("このページは初回提案用にお作りした一例です。"
              "文章・写真・メニュー内容は、ご相談しながら調整できます。")

out_dir = f"{DG}/generated_demos/real_salon_drafts/20260621/naturally"
path = gpll.gen(naturally, out_dir, disclosure_extra=disclosure)
print(f"generated: {path}")
