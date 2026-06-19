#!/usr/bin/env python3
"""
salon_editorial_variant — asset-first, magazine-style demo LP renderer.

Design intent: a small editorial feature page for ONE personal salon, made by a
real studio. Image / air → layout → copy → CTA (asset-first, not text-first).

Three themes: warm-natural / clean-minimal / quiet-editorial.

Asset honesty:
- If a profile gives a real, license-clear local image, it is used (full-bleed, art-directed).
- Otherwise an art-directed CSS/SVG visual (duotone gradient mesh + grain) stands in — clearly
  better than a flat wireframe block, but NOT photography. Every image carries a 要差し替え label.
- No human/owner portraits are ever auto-placed (fabrication risk).

Copy honesty (Phase-4 standard, scanned over the whole page):
- forbidden clichés/医療效果/hype blocked; short, specific, evocative copy preferred.
- no fabricated menus/prices/owner/testimonials/before-after.

Safe-local: stdlib only, synthetic data, no network at render time.
"""
import html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Phase-4 expanded forbidden list (clichés + 医療/效果 + hype). Used only when NOT backed by specifics.
FORBIDDEN = [
    "心も体も整う", "極上", "至福", "特別な時間", "ワンランク上", "癒しの空間", "あなただけの",
    "丁寧に寄り添う", "本来の自分", "根本から", "根本改善", "改善します", "効果を実感", "効果保証",
    "改善", "小顔効果", "小顔", "美白", "実感", "before/after", "ビフォーアフター",
    "必ず", "選ばれる理由", "こんなお悩みありませんか", "売上アップ", "集客アップ", "集客保証",
    "集客", "成果保証", "治ります", "治る", "治療", "痩身", "非日常", "贅沢な時間", "上質な時間",
    "自律神経", "脳脊髄液", "血流", "不眠", "眼精疲労", "妊活", "不妊", "脱毛", "wax", "Wax", "WAX",
]
WHITELIST = ["スクロール"]
KEEP_INLINE_TERMS = ("ドライヘッドスパ",)


def esc(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def inline_keep_terms(s):
    text = esc(s)
    for term in KEEP_INLINE_TERMS:
        safe_term = esc(term)
        text = text.replace(safe_term, f'<span class="nowrap">{safe_term}</span>')
    return text


def scan_forbidden(text):
    t = text
    for w in WHITELIST:
        t = t.replace(w, "")
    return [w for w in FORBIDDEN if w in t]


# --- grain texture (SVG feTurbulence) as a tiny data URI; kills flat-gradient AI smell ----
GRAIN = (
    "data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20width='180'%20height='180'%3E"
    "%3Cfilter%20id='n'%3E%3CfeTurbulence%20type='fractalNoise'%20baseFrequency='0.9'%20numOctaves='2'%20stitchTiles='stitch'/%3E"
    "%3CfeColorMatrix%20type='saturate'%20values='0'/%3E%3C/filter%3E"
    "%3Crect%20width='180'%20height='180'%20filter='url(%23n)'%20opacity='0.55'/%3E%3C/svg%3E"
)


def art_hero_svg(theme):
    """Art-directed duotone gradient-mesh hero stand-in (NOT a flat block, NOT photography)."""
    pals = {
        "warm-natural": ("%23efe2d2", "%23d8b89a", "%23b07f5c", "%238a5a3c"),
        "clean-minimal": ("%23f3f4f2", "%23dfe5e3", "%23c2cdc9", "%239fb0ab"),
        "quiet-editorial": ("%23ece9e3", "%23d6cfc4", "%23b3a furcation", "%238d8576"),
    }
    a, b, c, d = pals.get(theme, pals["warm-natural"])
    d = d.replace("a furcation", "aa9a86")  # guard against accidental typo
    return (
        "data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201200%201500'%3E"
        "%3Cdefs%3E"
        f"%3CradialGradient%20id='m1'%20cx='0.7'%20cy='0.25'%20r='0.8'%3E%3Cstop%20offset='0'%20stop-color='{b}'/%3E%3Cstop%20offset='1'%20stop-color='{a}'/%3E%3C/radialGradient%3E"
        f"%3CradialGradient%20id='m2'%20cx='0.2'%20cy='0.85'%20r='0.7'%3E%3Cstop%20offset='0'%20stop-color='{c}'%20stop-opacity='0.85'/%3E%3Cstop%20offset='1'%20stop-color='{a}'%20stop-opacity='0'/%3E%3C/radialGradient%3E"
        "%3C/defs%3E"
        f"%3Crect%20width='1200'%20height='1500'%20fill='{a}'/%3E"
        "%3Crect%20width='1200'%20height='1500'%20fill='url(%23m1)'/%3E"
        "%3Crect%20width='1200'%20height='1500'%20fill='url(%23m2)'/%3E"
        f"%3Cpath%20d='M0%201160%20C300%201050%20520%201110%20760%201020%20C980%20940%201080%20960%201200%201010%20L1200%201500%20L0%201500%20Z'%20fill='{d}'%20opacity='0.16'/%3E"
        f"%3Ccircle%20cx='905'%20cy='360'%20r='150'%20fill='%23ffffff'%20opacity='0.18'/%3E"
        "%3C/svg%3E"
    )


THEME_CSS = {
    "warm-natural": """
--paper:#f7efe4; --paper2:#efe5d6; --ink:#2b2620; --ink2:#5e554a; --muted:#938876;
--accent:#9c5f3c; --line:rgba(43,38,32,.14); --hairline:rgba(43,38,32,.22);
--serif:"Shippori Mincho","Hiragino Mincho ProN","Yu Mincho","Noto Serif JP",serif; --sans:"Zen Kaku Gothic New","Hiragino Sans","Yu Gothic","Noto Sans JP",system-ui,sans-serif;
--duotone-a:#2b2016; --duotone-b:#e7c9a6;
--shadow:0 18px 48px rgba(43,38,32,.12);
""",
    "clean-minimal": """
--paper:#fbfbfa; --paper2:#f1f3f2; --ink:#23282a; --ink2:#525a5c; --muted:#8a9290;
--accent:#3f6b62; --line:rgba(35,40,42,.12); --hairline:rgba(35,40,42,.2);
--serif:"Shippori Mincho","Hiragino Mincho ProN","Yu Mincho","Noto Serif JP",serif; --sans:"Zen Kaku Gothic New","Hiragino Sans","Yu Gothic","Noto Sans JP",system-ui,sans-serif;
--duotone-a:#1f2b29; --duotone-b:#e9efed;
--shadow:0 18px 48px rgba(35,40,42,.1);
""",
    "quiet-editorial": """
--paper:#f4f1ec; --paper2:#eae5dc; --ink:#262220; --ink2:#574f48; --muted:#8c8275;
--accent:#7a6a55; --line:rgba(38,34,32,.13); --hairline:rgba(38,34,32,.2);
--serif:"Shippori Mincho","Hiragino Mincho ProN","Yu Mincho","Noto Serif JP",serif; --sans:"Zen Kaku Gothic New","Hiragino Sans","Yu Gothic","Noto Sans JP",system-ui,sans-serif;
--duotone-a:#241f1b; --duotone-b:#e6ddd0;
--shadow:0 18px 48px rgba(38,34,32,.11);
""",
    "lea-editorial": """
--color-text-primary:#3a322c; --color-text-body:#5e5953; --color-text-muted:#837c73;
--color-bg-base:#fbfaf7; --color-accent:#8a4f5a;
--paper:var(--color-bg-base); --paper2:#eee9e4; --ink:var(--color-text-primary); --ink2:var(--color-text-body); --muted:var(--color-text-muted);
--accent:var(--color-accent); --accent2:#66736c; --line:rgba(36,33,31,.13); --hairline:rgba(36,33,31,.24);
--serif:"Shippori Mincho","Hiragino Mincho ProN","Yu Mincho","Noto Serif JP",serif; --sans:"Zen Kaku Gothic New","Hiragino Sans","Yu Gothic","Noto Sans JP",system-ui,sans-serif;
--duotone-a:#211c1b; --duotone-b:#eadbd2; --shadow:0 20px 54px rgba(36,33,31,.12);
--color-text-on-hero:var(--color-text-primary); --hero-overlay-top:rgba(251,247,242,.30); --hero-overlay-bottom:rgba(251,247,242,.55);
""",
}


def base_css(theme, grain_on=True):
    if theme not in THEME_CSS:
        theme = "warm-natural"
    grain = f"""
body::after{{content:"";position:fixed;inset:0;z-index:9;pointer-events:none;mix-blend-mode:multiply;
  opacity:.05;background-image:url("{GRAIN}");background-size:180px}}""" if grain_on else ""
    lea_extra = """
/* v8 final Lea optical pass: Option A, current font system with micro-tuned rhythm. */
.theme-lea-editorial .narrow{width:min(620px,calc(100% - 48px))}
.theme-lea-editorial{
  --hero-ink:var(--color-text-on-hero);
  --hero-muted:var(--color-text-on-hero);
  --hero-paper:rgba(251,250,247,.78);
  --heading-serif:var(--serif);
}
.brand-lockup{display:inline-flex;flex-direction:column;align-items:flex-start;gap:5px;line-height:1}
.brand-lockup .brand-kicker{font-family:var(--sans);font-size:12px;line-height:1;color:var(--ink2);font-weight:400}
.brand-lockup .brand-latin{font-family:var(--brand-serif);font-size:1em;line-height:.9;font-weight:500;color:inherit}
.theme-lea-editorial footer .brand-lockup-footer{gap:4px}
.theme-lea-editorial footer .brand-lockup-footer .brand-kicker{font-size:10.5px;color:var(--muted)}
.theme-lea-editorial footer .brand-lockup-footer .brand-latin{font-size:28px;color:var(--ink)}
.hero.light .bg img{filter:saturate(.95) contrast(.99) brightness(1.03)}
.hero.light .bg::after{content:none}
.hero.light .scrim{display:none}
.hero.light h1,.hero.light .eyebrow,.hero.light .sub,.hero.light .go{color:var(--hero-ink);text-shadow:none}
.hero.light .eyebrow{color:var(--hero-ink);opacity:.84;font-size:12px;letter-spacing:.06em}
.hero.light .sub{color:var(--hero-muted);opacity:1}
.hero.light .go{border-color:rgba(41,36,31,.44)}
.hero.light .go.primary{border-color:rgba(41,36,31,.34);background:rgba(255,255,255,.46);box-shadow:0 14px 34px rgba(58,47,37,.1);backdrop-filter:blur(6px)}
.hero.light .hero-cta-note{color:var(--hero-muted);text-shadow:none}
.hero.light .tag{color:var(--muted)}
.hero.lea-v6{min-height:88svh}
.hero.lea-v6 .col{padding-bottom:9vh}
.hero.lea-v6 h1{font-size:88px;line-height:.96;font-weight:400}
.hero.lea-v6 .brand-lockup-hero{gap:10px}
.hero.lea-v6 .brand-lockup-hero .brand-kicker{font-size:14px;color:var(--hero-muted)}
.hero.lea-v6 .brand-lockup-hero .brand-latin{font-size:96px;color:var(--hero-ink)}
.hero.lea-v6 .sub{font-family:var(--heading-serif);font-size:26px;line-height:1.62;max-width:16em;margin-top:20px;font-weight:400}
.hero.lea-v6 .hero-actions{margin-top:24px;gap:16px}
.hero.lea-v8-optical .brand-lockup-hero{gap:9px}
.hero.lea-v8-optical .sub{margin-top:19px}
.hero.lea-v8-optical .hero-actions{margin-top:25px}
.hero.lea-v6 .go.primary{
  position:relative;min-width:0;min-height:44px;justify-content:flex-start;border:0;
  border-radius:0;background:transparent;box-shadow:none;backdrop-filter:none;padding:0 2px;
  font-size:13.5px;line-height:1;color:var(--hero-ink);gap:.58em
}
.hero.lea-v6 .go.primary::after{
  content:"";position:absolute;left:2px;right:2px;bottom:9px;height:1px;background:currentColor;
  opacity:.48;transform-origin:left center;transition:opacity .22s ease,transform .22s ease
}
.hero.lea-v6 .go.primary span,.theme-lea-editorial .res .go span{transition:transform .22s ease}
.hero.lea-v6 .go.primary:hover{gap:.58em;color:var(--hero-ink)}
.hero.lea-v6 .go.primary:hover::after{opacity:.72;transform:scaleX(1.04)}
.hero.lea-v6 .go.primary:hover span,.theme-lea-editorial .res .go:hover span{transform:translateX(3px)}
.hero.lea-v6 .go.primary:active span,.theme-lea-editorial .res .go:active span{transform:translateX(1px)}
.hero.lea-v6 .go.primary:focus-visible,.theme-lea-editorial .res .go:focus-visible{
  outline:1px solid currentColor;outline-offset:5px
}
.theme-lea-editorial .body,
.theme-lea-editorial .menu-intro,
.theme-lea-editorial .menu .dt,
.theme-lea-editorial .flow p,
.theme-lea-editorial .story .lede,
.theme-lea-editorial .access-intro,
.theme-lea-editorial .info .r,
.theme-lea-editorial .res .note{font-family:var(--sans);font-weight:400}
.theme-lea-editorial .lede{line-height:1.78;max-width:21.5em}
.theme-lea-editorial .body{max-width:32.5em;line-height:1.94;color:var(--ink2)}
.theme-lea-editorial .s{padding:clamp(52px,7vw,92px) 0}
.theme-lea-editorial .s.tight{padding:clamp(40px,5.8vw,66px) 0}
.theme-lea-editorial .kick{font-family:var(--heading-serif);font-size:13px;line-height:1.58;font-weight:400;margin-bottom:14px;color:var(--accent2);letter-spacing:.055em}
.hero.lea-v4 .col{padding-bottom:8.8vh}
.hero.lea-v4 .go.primary{min-width:0;justify-content:flex-start;border-radius:0;padding:0 2px}
.hero.lea-v4 .go:hover{gap:.7em}
.theme-lea-editorial .menu-intro{max-width:30.5em;margin-bottom:19px;color:var(--ink2);line-height:1.88}
.theme-lea-editorial .menu .row{grid-template-columns:34px minmax(0,1fr) minmax(92px,auto);gap:18px;padding:22px 0;align-items:start}
.theme-lea-editorial .menu .row:nth-child(2){padding-top:22px;padding-bottom:22px}
.theme-lea-editorial .menu .idx{font-size:12px;line-height:1.4;color:var(--accent2);padding-top:4px}
.theme-lea-editorial .menu .nm{font-family:var(--heading-serif);font-size:19px;line-height:1.52;font-weight:400}
.theme-lea-editorial .menu .dt{max-width:33em;font-size:13.5px;line-height:1.84;margin-top:5px;color:var(--ink2)}
.theme-lea-editorial .menu .pr{display:flex;flex-direction:column;align-items:flex-end;gap:2px;min-width:92px;padding-top:3px;padding-left:16px;border-left:1px solid var(--line);line-height:1.45;color:var(--ink2)}
.theme-lea-editorial .menu .pr .time{font-size:12.2px;color:var(--muted)}
.theme-lea-editorial .menu .pr .yen{font-size:13.8px;font-weight:500;font-variant-numeric:tabular-nums;color:var(--ink)}
.theme-lea-editorial .flow .r{grid-template-columns:38px 1fr;gap:18px;padding:18px 0}
.theme-lea-editorial .flow .no{font-size:12px;line-height:1.6;color:var(--accent2);font-weight:400;opacity:.86}
.theme-lea-editorial .flow h3{font-family:var(--heading-serif);font-size:16px;line-height:1.58;font-weight:400;color:var(--ink)}
.theme-lea-editorial .flow p{font-size:13.5px;line-height:1.84;margin-top:3px}
.theme-lea-editorial .story{padding-top:clamp(34px,4.6vw,60px);padding-bottom:clamp(44px,5.4vw,70px)}
.theme-lea-editorial .story .lede{font-family:var(--heading-serif);font-size:18px;line-height:1.96;font-weight:400;max-width:27em;color:var(--ink2)}
.theme-lea-editorial #access{padding-top:clamp(40px,5vw,66px);padding-bottom:clamp(44px,5.4vw,72px)}
.theme-lea-editorial .acc{align-items:start}
.theme-lea-editorial .res .go{
  display:inline-flex;min-width:0;min-height:44px;justify-content:center;align-items:center;
  border:0;border-top:1px solid rgba(138,79,90,.2);border-bottom:1px solid rgba(138,79,90,.58);
  border-radius:0;padding:0 14px;color:var(--accent);font-size:13.5px;line-height:1;background:transparent;gap:.62em
}
.theme-lea-editorial .res .go:hover{gap:.62em;border-top-color:rgba(138,79,90,.32);border-bottom-color:rgba(138,79,90,.82);background:rgba(138,79,90,.025)}
.theme-lea-editorial .sample-note{padding:14px 0;background:rgba(238,233,228,.58)}
.theme-lea-editorial .sample-note p{font-size:11.5px;line-height:1.8;color:var(--muted);opacity:.76}
.theme-lea-editorial footer{padding:34px 0}
.theme-lea-editorial.ui-soft-line,
.theme-lea-editorial.ui-soft-surface{
  --paper:var(--color-bg-base); --paper2:#f3ebe2; --ink:var(--color-text-primary); --ink2:var(--color-text-body); --muted:var(--color-text-muted);
  --accent:var(--color-accent); --accent2:#8f766a; --line:rgba(122,92,78,.08); --hairline:rgba(122,92,78,.14);
  --soft-line:rgba(122,92,78,.095); --soft-surface:rgba(247,238,228,.68);
  --soft-pill:#edd9d2; --soft-pill-hover:#e7cec6; --soft-shadow:0 7px 20px rgba(83,61,51,.045);
}
body.theme-lea-editorial.ui-soft-line,
body.theme-lea-editorial.ui-soft-surface{background:var(--paper);letter-spacing:0}
.theme-lea-editorial.ui-soft-line .hero.light .overlay,
.theme-lea-editorial.ui-soft-surface .hero.light .overlay{
  background:linear-gradient(to bottom,var(--hero-overlay-top) 0%,var(--hero-overlay-bottom) 100%);
}
.theme-lea-editorial.ui-soft-line .hero.lea-v6 .go.primary,
.theme-lea-editorial.ui-soft-surface .hero.lea-v6 .go.primary{
  min-height:40px;border:0;border-radius:999px;background:rgba(237,217,210,.72);color:var(--color-text-on-hero);
  box-shadow:none;padding:0 17px;gap:.54em;font-size:13.5px;line-height:1;
}
.theme-lea-editorial.ui-soft-line .res .go,
.theme-lea-editorial.ui-soft-surface .res .go{
  min-height:43px;border:0;border-radius:999px;background:var(--soft-pill);color:var(--accent);
  box-shadow:var(--soft-shadow);padding:0 20px;gap:.56em;font-size:13.5px;line-height:1;
}
.theme-lea-editorial.ui-soft-line .hero.lea-v6 .go.primary::after,
.theme-lea-editorial.ui-soft-surface .hero.lea-v6 .go.primary::after{content:none}
.theme-lea-editorial.ui-soft-line .hero.lea-v6 .go.primary:hover,
.theme-lea-editorial.ui-soft-surface .hero.lea-v6 .go.primary:hover{background:rgba(231,206,198,.78);color:var(--color-text-on-hero);box-shadow:none;gap:.54em}
.theme-lea-editorial.ui-soft-line .res .go:hover,
.theme-lea-editorial.ui-soft-surface .res .go:hover{background:var(--soft-pill-hover);box-shadow:0 14px 34px rgba(83,61,51,.1);gap:.56em}
.theme-lea-editorial.ui-soft-line .hero-cta-note,
.theme-lea-editorial.ui-soft-surface .hero-cta-note{font-size:12.5px;line-height:1.72;color:var(--hero-muted)}
.theme-lea-editorial.ui-soft-line .kick,
.theme-lea-editorial.ui-soft-surface .kick{font-family:var(--sans);font-weight:400;font-size:12px;line-height:1.58;color:var(--accent2);letter-spacing:.055em}
.theme-lea-editorial.ui-soft-line .s.tight .kick,
.theme-lea-editorial.ui-soft-surface .s.tight .kick{font-size:11.8px}
.theme-lea-editorial.ui-soft-line .lede,
.theme-lea-editorial.ui-soft-surface .lede{font-weight:400}
.theme-lea-editorial.ui-soft-line .menu .idx,
.theme-lea-editorial.ui-soft-surface .menu .idx{font-family:var(--sans);font-size:10.5px;color:var(--muted);opacity:.72}
.theme-lea-editorial.ui-soft-line .flow .no,
.theme-lea-editorial.ui-soft-surface .flow .no{font-family:var(--sans);font-size:11px;color:var(--accent2);opacity:.72}
.theme-lea-editorial.ui-soft-line .menu .pr,
.theme-lea-editorial.ui-soft-surface .menu .pr{border-left:0;padding-left:0;color:var(--ink2)}
.theme-lea-editorial.ui-soft-line .menu .pr .yen,
.theme-lea-editorial.ui-soft-surface .menu .pr .yen{font-weight:500;color:var(--ink2)}
.theme-lea-editorial.ui-soft-line .method-list li,
.theme-lea-editorial.ui-soft-surface .method-list li{border:0;border-radius:0;background:transparent;color:var(--ink2);padding:0;font-size:12.5px}
.theme-lea-editorial.ui-soft-line .method-list li + li::before,
.theme-lea-editorial.ui-soft-surface .method-list li + li::before{content:"/";display:inline-block;margin:0 .7em;color:var(--muted);opacity:.45}
.theme-lea-editorial.ui-soft-line .info .k,
.theme-lea-editorial.ui-soft-surface .info .k{font-size:11.5px;color:var(--muted);padding-top:1px}
.theme-lea-editorial.ui-soft-line .res .note,
.theme-lea-editorial.ui-soft-surface .res .note{color:var(--muted);font-size:12.8px;line-height:1.86}
.theme-lea-editorial.ui-soft-line .sample-note,
.theme-lea-editorial.ui-soft-surface .sample-note{background:rgba(243,235,226,.58);border-top:0}
.theme-lea-editorial.ui-soft-line footer,
.theme-lea-editorial.ui-soft-surface footer{border-top:0;background:rgba(243,235,226,.24)}
.theme-lea-editorial.ui-soft-line .menu .row,
.theme-lea-editorial.ui-soft-line .flow .r,
.theme-lea-editorial.ui-soft-line .info .r{border-top:0;border-bottom:0}
.theme-lea-editorial.ui-soft-line .menu .row + .row,
.theme-lea-editorial.ui-soft-line .flow .r + .r,
.theme-lea-editorial.ui-soft-line .info .r + .r{border-top:1px solid var(--soft-line)}
.theme-lea-editorial.ui-soft-line .menu .row{padding:24px 0}
.theme-lea-editorial.ui-soft-line .flow .r{padding:17px 0}
.theme-lea-editorial.ui-soft-line .info .r{grid-template-columns:72px 1fr;padding:13px 0;font-size:14px}
.theme-lea-editorial.ui-soft-line .access-intro{max-width:28em}
.theme-lea-editorial.ui-soft-surface .menu,
.theme-lea-editorial.ui-soft-surface .flow{display:block;background:var(--soft-surface);border-radius:14px;padding:8px 18px}
.theme-lea-editorial.ui-soft-surface .info{display:block}
.theme-lea-editorial.ui-soft-surface .menu .row,
.theme-lea-editorial.ui-soft-surface .flow .r,
.theme-lea-editorial.ui-soft-surface .info .r{border:0;background:transparent;border-radius:0}
.theme-lea-editorial.ui-soft-surface .menu .row{grid-template-columns:minmax(0,1fr) minmax(88px,auto);padding:18px 0;gap:16px}
.theme-lea-editorial.ui-soft-surface .menu .idx{display:none}
.theme-lea-editorial.ui-soft-surface .flow .r{grid-template-columns:30px 1fr;padding:15px 0;gap:14px}
.theme-lea-editorial.ui-soft-surface .flow .no{display:block;width:auto;height:auto;border-radius:0;background:transparent;font-size:11px;line-height:1.5;color:var(--accent2);opacity:.62;padding-top:2px}
.theme-lea-editorial.ui-soft-surface .info .r{grid-template-columns:72px 1fr;padding:12px 0;font-size:14px}
.theme-lea-editorial.ui-soft-surface .res{background:transparent;border-radius:0;padding:0;align-self:center}
.theme-lea-editorial.ui-soft-surface .acc{gap:clamp(20px,4vw,44px);background:var(--soft-surface);border-radius:14px;padding:clamp(20px,3.6vw,34px)}
@media(max-width:760px){
  .theme-lea-editorial.ui-soft-line .hero.light .overlay,
  .theme-lea-editorial.ui-soft-surface .hero.light .overlay{background:linear-gradient(to bottom,var(--hero-overlay-top) 0%,var(--hero-overlay-bottom) 100%)}
  .theme-lea-editorial.ui-soft-line .hero.lea-v6 .go.primary,
  .theme-lea-editorial.ui-soft-surface .hero.lea-v6 .go.primary,
  .theme-lea-editorial.ui-soft-line .res .go,
  .theme-lea-editorial.ui-soft-surface .res .go{min-height:41px;padding:0 16px}
  .theme-lea-editorial.ui-soft-surface .menu,
  .theme-lea-editorial.ui-soft-surface .flow{border-radius:12px;padding:7px 15px}
  .theme-lea-editorial.ui-soft-line .info .r,
  .theme-lea-editorial.ui-soft-surface .info .r{grid-template-columns:1fr;gap:4px}
  .theme-lea-editorial.ui-soft-surface .menu .row{grid-template-columns:1fr;padding:16px 0}
  .theme-lea-editorial.ui-soft-surface .menu .pr{grid-column:1;align-items:flex-start;flex-direction:row;gap:8px}
  .theme-lea-editorial.ui-soft-surface .flow .r{grid-template-columns:26px 1fr;padding:14px 0;gap:11px}
  .theme-lea-editorial.ui-soft-surface .acc{border-radius:12px;padding:20px 17px 22px}
  .theme-lea-editorial.ui-soft-surface .res{padding:0}
}
.theme-lea-editorial.typo-a .lede{font-family:var(--heading-serif);font-weight:400}
.theme-lea-editorial.typo-a .res .lede{font-family:var(--heading-serif);font-weight:400}
.theme-lea-editorial.typo-b .kick,
.theme-lea-editorial.typo-b .menu .nm,
.theme-lea-editorial.typo-b .res .lede,
.theme-lea-editorial.typo-b .story .lede{font-family:var(--sans)}
.theme-lea-editorial.typo-b .kick{font-size:12.5px;font-weight:500;color:var(--accent2)}
.theme-lea-editorial.typo-b .lede{font-family:var(--serif);font-size:23px;line-height:1.82;font-weight:400}
.theme-lea-editorial.typo-b .menu .nm{font-size:18px;font-weight:400;line-height:1.55}
.theme-lea-editorial.typo-b .flow h3{font-family:var(--heading-serif);font-size:15px;font-weight:400;line-height:1.6}
.theme-lea-editorial.typo-b .res .lede{font-size:20px;line-height:1.74;font-weight:400}
.theme-lea-editorial.typo-c .hero.lea-v6 .brand-lockup-hero .brand-latin{font-size:88px;font-weight:400}
.theme-lea-editorial.typo-c .hero.lea-v6 .brand-lockup-hero .brand-kicker{font-size:13px}
.theme-lea-editorial.typo-c .hero.lea-v6 .sub{font-size:24px;line-height:1.68}
.theme-lea-editorial.typo-c .kick{font-size:12px;font-weight:400;margin-bottom:14px}
.theme-lea-editorial.typo-c .lede{font-size:22px;line-height:1.9;font-weight:400}
.theme-lea-editorial.typo-c .menu .nm{font-size:18px;line-height:1.6;font-weight:400}
.theme-lea-editorial.typo-c .flow h3{font-size:15px;line-height:1.68;font-weight:400}
.theme-lea-editorial.typo-c .story .lede{font-size:17px;line-height:1.92}
.theme-lea-editorial.typo-c .res .lede{font-size:21px;line-height:1.78}
.theme-lea-editorial .hero.copy-focus h1{font-size:68px;line-height:1.14;font-weight:400;max-width:9em;word-break:keep-all;overflow-wrap:normal}
.theme-lea-editorial .hero.copy-focus .sub{max-width:22em;white-space:pre-line}
.theme-lea-editorial .hero.akazukin-hero{--hero-ink:var(--color-text-on-hero);--hero-muted:var(--color-text-on-hero)}
.theme-lea-editorial .hero.akazukin-hero .eyebrow{color:var(--color-text-on-hero)}
.theme-lea-editorial.ui-soft-surface .hero.akazukin-hero.lea-v6 .go.primary,
.theme-lea-editorial.ui-soft-surface .hero.akazukin-hero.lea-v6 .go.primary:hover{color:var(--color-text-on-hero)}
@media(max-width:760px){
  .theme-lea-editorial .narrow{width:min(100% - 34px,620px)}
  .hero.light .overlay{background:linear-gradient(to bottom,var(--hero-overlay-top) 0%,var(--hero-overlay-bottom) 100%)}
  .hero.lea-v4{min-height:100svh}
  .hero.lea-v6{min-height:100svh}
  .hero.lea-v6 .col{padding-bottom:8.4vh}
  .hero.lea-v6 .brand-lockup-hero{gap:8px}
  .hero.lea-v6 .brand-lockup-hero .brand-kicker{font-size:12px}
  .hero.lea-v6 .brand-lockup-hero .brand-latin{font-size:66px}
  .hero.lea-v6 .sub{font-size:22px;line-height:1.58;max-width:16em;margin-top:16px}
  .theme-lea-editorial.typo-c .hero.lea-v6 .brand-lockup-hero .brand-latin{font-size:60px}
  .theme-lea-editorial.typo-c .hero.lea-v6 .sub{font-size:20px;line-height:1.66}
  .theme-lea-editorial .hero.copy-focus h1{font-size:43px;line-height:1.22;max-width:7.6em}
  .theme-lea-editorial .hero.copy-focus .sub{max-width:17em}
  .hero.lea-v4 .col{padding-bottom:8.4vh}
  .hero.lea-v4 .hero-actions{margin-top:22px}
  .hero.lea-v8-optical .hero-actions{margin-top:23px}
  .hero.lea-v4 .go.primary{width:auto;padding:0 2px}
  .hero.lea-v4 .hero-cta-note{font-size:11.7px;line-height:1.7;max-width:19em}
  .theme-lea-editorial .s{padding:48px 0}
  .theme-lea-editorial .s.tight{padding:40px 0}
  .theme-lea-editorial .lede{font-size:20px;line-height:1.74}
  .theme-lea-editorial .body{font-size:14px;line-height:1.94;margin-top:16px;max-width:32.5em}
  .theme-lea-editorial .kick{font-size:12.5px;margin-bottom:12px}
  .theme-lea-editorial .menu-intro{font-size:14px;line-height:1.86;margin-bottom:13px}
  .theme-lea-editorial .menu .row{grid-template-columns:30px 1fr;gap:11px;padding:20px 0}
  .theme-lea-editorial .menu .nm{font-size:18px;line-height:1.48}
  .theme-lea-editorial .menu .dt{font-size:13px;line-height:1.8;margin-top:4px}
  .theme-lea-editorial .menu .pr{grid-column:2;align-items:flex-start;border-left:0;padding-left:0;padding-top:3px;min-width:0;flex-direction:row;gap:9px}
  .theme-lea-editorial .flow .r{grid-template-columns:30px 1fr;gap:14px;padding:16px 0}
  .theme-lea-editorial .flow h3{font-size:15px;line-height:1.62}
  .theme-lea-editorial .flow p{font-size:13px;line-height:1.74}
  .theme-lea-editorial .story{padding-top:36px;padding-bottom:42px}
  .theme-lea-editorial .story .lede{font-size:16.5px;line-height:1.84}
  .theme-lea-editorial #access{padding-top:38px;padding-bottom:44px}
  .theme-lea-editorial .res .go{width:auto;padding:0 12px}
  .theme-lea-editorial .sample-note{padding:14px 0}
  .theme-lea-editorial footer{padding:30px 0}
}
""" if theme == "lea-editorial" else ""
    lea_extra = (lea_extra.strip() + "\n") if lea_extra else ""
    return f""":root{{{THEME_CSS[theme]}
--brand-serif:"Cormorant Garamond","EB Garamond","Spectral",Georgia,serif;
--heading-serif:var(--serif);
--color-text-on-hero:var(--color-text-primary,var(--ink));
--hero-overlay-top:rgba(251,247,242,.30);
--hero-overlay-bottom:rgba(251,247,242,.55);
}}
*{{box-sizing:border-box}} html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);
  font-size:16px;line-height:1.9;font-weight:400;-webkit-font-smoothing:antialiased;letter-spacing:.02em}}
img{{display:block;max-width:100%}} a{{color:inherit;text-decoration:none}}
h1,h2,h3,p,figure,ul,blockquote{{margin:0}} li{{list-style:none}}
.col{{width:min(1080px,calc(100% - 48px));margin:0 auto}}
.narrow{{width:min(680px,calc(100% - 48px));margin:0 auto}}
{grain}
.draft{{font-size:11px;letter-spacing:.14em;color:var(--muted);text-align:center;padding:9px;background:var(--paper2);white-space:normal;overflow-wrap:anywhere}}
.top{{position:absolute;top:36px;left:0;right:0;z-index:8}}
.top .col{{display:flex;justify-content:flex-end;align-items:center;padding:26px 0}}
.wordmark{{font-family:var(--serif);font-size:17px;letter-spacing:.12em;font-weight:600}}
.top .loc{{font-size:11px;letter-spacing:.22em;color:var(--muted)}}
.top.dark .loc{{color:#fff;text-shadow:0 1px 18px rgba(0,0,0,.35)}}

/* HERO — full-bleed, image-led, text in a quiet corner */
.hero{{position:relative;min-height:92vh;display:flex;align-items:flex-end;overflow:hidden}}
.hero .bg{{position:absolute;inset:0;z-index:0}}
.hero .bg img{{width:100%;height:100%;object-fit:cover;object-position:var(--hero-pos,center center)}}
.hero.duo .bg img{{filter:grayscale(1) contrast(1.04)}}
.hero.duo .bg::after{{content:none}}
.hero.soft .bg img{{filter:saturate(.98) contrast(.99) brightness(1)}}
.hero.soft .bg::after{{content:none}}
.hero .overlay{{position:absolute;inset:0;z-index:1;pointer-events:none;background:linear-gradient(to bottom,var(--hero-overlay-top,rgba(251,247,242,.30)) 0%,var(--hero-overlay-bottom,rgba(251,247,242,.55)) 100%)}}
.hero .scrim{{display:none}}
.hero .col{{position:relative;z-index:2;padding:0 0 9vh}}
.hero .eyebrow{{font-size:12px;letter-spacing:.3em;color:var(--color-text-on-hero,var(--ink));opacity:.95;margin-bottom:20px;text-shadow:none}}
.hero h1{{font-family:var(--serif);font-weight:600;color:var(--color-text-on-hero,var(--ink));font-size:clamp(34px,6.2vw,62px);line-height:1.42;letter-spacing:.04em;text-shadow:none}}
.hero .sub{{margin-top:22px;color:var(--color-text-on-hero,var(--ink));opacity:.86;font-size:15px;letter-spacing:.06em;max-width:24em;text-shadow:none;text-wrap:pretty}}
.hero .nowrap{{white-space:nowrap}}
.hero-meta{{display:flex;flex-wrap:wrap;gap:8px;margin:24px 0 0;padding:0;max-width:420px}}
.hero-meta li{{border:1px solid rgba(58,50,44,.18);background:rgba(251,247,242,.62);color:var(--color-text-on-hero,var(--ink));
  font-size:12px;line-height:1.5;padding:5px 9px;text-shadow:none}}
.hero-actions{{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin-top:34px}}
.hero .go{{display:inline-flex;align-items:center;gap:.7em;color:var(--color-text-on-hero,var(--ink));font-size:14px;letter-spacing:.14em;border-bottom:1px solid rgba(58,50,44,.48);padding-bottom:6px}}
.hero .go.primary{{border:1px solid rgba(58,50,44,.18);background:rgba(251,247,242,.74);padding:12px 18px;color:var(--color-text-on-hero,var(--ink));box-shadow:0 12px 28px rgba(83,61,51,.09)}}
.hero-cta-note{{color:var(--color-text-on-hero,var(--ink));opacity:.78;font-size:12.5px;line-height:1.8;max-width:20em;text-shadow:none}}
.hero .go:hover{{gap:1.1em}}
.hero .tag{{position:absolute;right:0;bottom:9vh;z-index:2;font-size:10px;letter-spacing:.1em;color:var(--color-text-on-hero,var(--ink));opacity:.56}}
.hero.brand-focus h1{{font-size:74px;line-height:1.06}}
.hero.brand-focus .eyebrow{{font-size:13px;margin-bottom:16px}}
.hero.brand-focus .sub{{max-width:31em}}
.theme-lea-editorial .top{{top:26px}}
.hero.lea-v4{{min-height:88svh}}
.hero.lea-v4 .bg img{{filter:saturate(.96) contrast(1) brightness(1)}}
.hero.lea-v4 .bg::after{{content:none}}
.hero.lea-v4 .scrim{{display:none}}
.hero.lea-v4 .col{{padding-bottom:8vh}}
.hero.lea-v4 .eyebrow{{font-size:12px;margin-bottom:14px;opacity:.9}}
.hero.lea-v4 h1{{font-size:clamp(64px,8.4vw,94px);line-height:.96;font-weight:500}}
.hero.lea-v4 .sub{{font-family:var(--serif);font-size:clamp(22px,2.3vw,30px);line-height:1.55;max-width:16em;margin-top:18px;opacity:.96}}
.hero.lea-v4 .hero-actions{{margin-top:28px;gap:14px}}
.hero.lea-v4 .go.primary{{border-color:rgba(58,50,44,.18);background:rgba(251,247,242,.74);padding:10px 15px;font-size:13.5px;box-shadow:0 12px 28px rgba(83,61,51,.09);backdrop-filter:blur(8px)}}
.hero.lea-v4 .hero-cta-note{{font-size:12px;line-height:1.75;max-width:19em;color:var(--color-text-on-hero,var(--ink));opacity:.76}}

/* art-directed (no-photo) hero variant keeps text dark-on-light for contrast */
.hero.art h1,.hero.art .eyebrow,.hero.art .sub,.hero.art .go{{color:var(--ink);text-shadow:none}}
.hero.art .eyebrow{{color:var(--accent)}}
.hero.art .go{{border-color:var(--hairline)}}
.hero.art .overlay{{background:linear-gradient(to bottom,rgba(255,255,255,0),rgba(255,255,255,.55))}}
.hero.art .scrim{{display:none}}
.hero.art .tag{{color:var(--muted);opacity:.8}}

/* sections — generous editorial rhythm */
.s{{padding:clamp(64px,11vw,128px) 0}}
.s.tight{{padding:clamp(48px,8vw,92px) 0}}
.kick{{font-family:var(--serif);color:var(--accent);font-size:13px;letter-spacing:.18em;margin-bottom:26px}}
.lede{{font-family:var(--serif);font-size:clamp(20px,2.6vw,27px);line-height:2.05;letter-spacing:.04em;color:var(--ink)}}
.lede .soft{{color:var(--ink2)}}
.body{{color:var(--ink2);font-size:15px;line-height:1.95;margin-top:20px}}

/* visual break band */
.band{{position:relative;height:46vh;min-height:300px;overflow:hidden}}
.band img{{width:100%;height:100%;object-fit:cover;object-position:var(--band-pos,center center)}}
.band.inset{{height:auto;min-height:0;overflow:visible;padding:0 0 clamp(48px,7vw,88px);background:var(--paper)}}
.band.inset img{{width:min(1080px,calc(100% - 48px));height:clamp(220px,31vw,400px);margin:0 auto;object-fit:cover;border-radius:2px}}
.band.duo img{{filter:grayscale(1) contrast(1.06);object-position:center 72%;transform:scale(1.18)}}
.band.duo::after{{content:"";position:absolute;inset:0;background:linear-gradient(160deg,var(--duotone-a),var(--duotone-b));mix-blend-mode:screen;opacity:.62}}
.band.lea-band{{height:clamp(320px,46vh,520px)}}
.band.lea-band img{{filter:saturate(.9) contrast(1.01) brightness(.94)}}
.band.lea-band::after{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(35,27,20,0),rgba(35,27,20,.18));pointer-events:none}}
.band.art{{background:var(--paper2)}}
.band .cap{{position:absolute;left:24px;bottom:16px;font-size:10px;letter-spacing:.1em;color:#fff;opacity:.7}}
.band.art .cap{{color:var(--muted)}}

/* menu — editorial list with dotted leaders */
.menu{{margin-top:14px}}
.menu .row{{display:grid;grid-template-columns:1fr auto;align-items:baseline;gap:14px;padding:26px 0;border-top:1px solid var(--line)}}
.menu .row:last-child{{border-bottom:1px solid var(--line)}}
.menu-intro{{color:var(--ink2);font-size:14.5px;line-height:1.9;margin:0 0 22px}}
.menu .idx{{font-family:var(--serif);font-size:13px;color:var(--accent);padding-top:5px}}
.menu .nm{{font-family:var(--serif);font-size:19px;letter-spacing:.03em}}
.menu .dt{{display:block;color:var(--muted);font-size:13px;margin-top:6px;letter-spacing:.04em}}
.menu .pr{{font-size:14.5px;color:var(--ink2);letter-spacing:.04em;white-space:nowrap;font-variant-numeric:tabular-nums}}
.menu .pr.tbd{{color:var(--muted);font-size:12.5px}}

/* flow — numbered, hairline, short */
.flow{{margin-top:10px}}
.flow .r{{display:grid;grid-template-columns:54px 1fr;gap:22px;padding:22px 0;border-top:1px solid var(--line)}}
.flow .r:last-child{{border-bottom:1px solid var(--line)}}
.flow .no{{font-family:var(--serif);color:var(--accent);font-size:15px;letter-spacing:.1em}}
.flow h3{{font-size:15px;font-weight:600;letter-spacing:.04em}}
.flow p{{color:var(--ink2);font-size:14px;margin-top:4px}}

/* story */
.story .lede{{max-width:24em}}
.story .sign{{margin-top:24px;font-family:var(--serif);font-size:15px;color:var(--ink2);letter-spacing:.08em}}
.story-grid{{display:grid;grid-template-columns:1fr .82fr;gap:clamp(28px,5vw,60px);align-items:center}}
.story-grid figure{{border-radius:2px;overflow:hidden;box-shadow:var(--shadow);aspect-ratio:4/5}}
.story-grid figure img{{width:100%;height:100%;object-fit:cover;object-position:var(--story-pos,center center)}}
.story-grid .ph{{font-size:10px;color:var(--muted);margin-top:8px;letter-spacing:.06em}}
.theme-lea-editorial .s{{padding:clamp(58px,8vw,104px) 0}}
.theme-lea-editorial .s.tight{{padding:clamp(42px,6.5vw,76px) 0}}
.theme-lea-editorial .kick{{margin-bottom:18px;color:var(--accent2)}}
.theme-lea-editorial .menu{{margin-top:10px}}
.theme-lea-editorial .menu .row{{grid-template-columns:38px minmax(0,1fr) minmax(104px,auto);padding:24px 0}}
.theme-lea-editorial .menu .pr{{text-align:right;font-size:14px}}
.theme-lea-editorial .story-grid figure img{{filter:saturate(.88) contrast(1.02) brightness(.95)}}
@media(max-width:760px){{.story-grid{{grid-template-columns:1fr;gap:26px}}.story-grid figure{{aspect-ratio:5/4;max-width:420px}}}}

/* access + reservation */
.acc{{display:grid;grid-template-columns:1.1fr .9fr;gap:clamp(28px,5vw,64px)}}
.info .r{{display:grid;grid-template-columns:84px 1fr;gap:16px;padding:15px 0;border-top:1px solid var(--line);font-size:14.5px}}
.info .r:last-child{{border-bottom:1px solid var(--line)}}
.info .k{{color:var(--accent);font-size:12.5px;letter-spacing:.08em;padding-top:2px}}
.res{{align-self:start}}
.res .lede{{font-size:21px}}
.res .go{{display:inline-flex;align-items:center;gap:.7em;margin-top:22px;color:var(--accent);font-size:15px;letter-spacing:.1em;border-bottom:1px solid var(--accent);padding-bottom:6px}}
.res .go:hover{{gap:1.1em}}
.res .note{{margin-top:14px;color:var(--muted);font-size:12.5px}}
.method-list{{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px;padding:0}}
.method-list li{{border:1px solid var(--line);padding:5px 9px;font-size:12.5px;color:var(--ink2);background:rgba(255,255,255,.28)}}
.access-intro{{color:var(--ink2);font-size:14px;line-height:1.9;margin:0 0 16px}}

.menu-note{{margin-top:22px;color:var(--muted);font-size:12.5px;letter-spacing:.03em}}
.demo-notes{{padding:34px 0;background:var(--paper2);border-top:1px solid var(--line)}}
.demo-notes .dn-kick{{font-size:11px;letter-spacing:.14em;color:var(--muted)}}
.demo-notes .dn-lead{{margin-top:8px;color:var(--ink2);font-size:13px}}
.demo-notes ul{{margin:14px 0 0;padding:0}}
.demo-notes li{{position:relative;padding:6px 0 6px 18px;color:var(--ink2);font-size:13px;border-top:1px solid var(--line)}}
.demo-notes li::before{{content:"–";position:absolute;left:2px;color:var(--muted)}}
.sample-note{{padding:24px 0;background:var(--paper2);border-top:1px solid var(--line)}}
.sample-note p{{color:var(--muted);font-size:12px;line-height:1.8;text-align:center}}
footer{{padding:46px 0;border-top:1px solid var(--line)}}
footer .col{{display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;align-items:baseline}}
footer .wordmark{{font-size:15px}}
footer .fn{{color:var(--muted);font-size:11px;letter-spacing:.1em}}

.js .rv{{opacity:0;transform:translateY(22px)}}
.js .rv{{transition:opacity .9s ease,transform .9s ease}}
.js .rv.in{{opacity:1;transform:none}}

@media(max-width:760px){{
  .hero{{min-height:90vh}}
  .hero .bg img{{object-position:var(--hero-pos-mobile,var(--hero-pos,center center))}}
  .hero h1{{font-size:clamp(30px,8.5vw,40px);line-height:1.5}}
  .hero-meta{{gap:6px;max-width:320px}}
  .hero-actions{{align-items:flex-start;flex-direction:column;gap:14px;margin-top:28px}}
  .hero .go.primary{{width:auto;padding:11px 15px}}
  .acc{{grid-template-columns:1fr;gap:34px}}
  .band{{height:38vh}}
  .band.inset{{height:auto;padding-bottom:56px}}
  .band.inset img{{width:calc(100% - 34px);height:210px}}
  .top{{top:42px}}
  .top .col{{padding:18px 0}}
  .menu .row{{grid-template-columns:36px 1fr;gap:12px}}
  .menu .pr{{grid-column:2}}
}}
/* v1 professional pass: remove mechanical tracking and viewport-scaled type. */
body,.draft,.wordmark,.top .loc,.hero .eyebrow,.hero h1,.hero .sub,.hero .go,.hero-meta li,
.kick,.lede,.body,.menu .nm,.menu .dt,.menu .pr,.flow .no,.flow h3,.story .sign,
.info .k,.res .go,.menu-note,.demo-notes .dn-kick,.demo-notes li,footer .fn{{letter-spacing:0}}
.hero h1{{font-size:56px;line-height:1.28}}
.hero.brand-focus h1{{font-size:74px;line-height:1.06}}
.hero.brand-focus .eyebrow{{font-size:13px;margin-bottom:16px}}
.hero.brand-focus .sub{{max-width:31em}}
.lede{{font-size:24px;line-height:1.85}}
.hero .eyebrow{{font-size:13px;margin-bottom:18px}}
.hero .sub{{font-size:16px;line-height:1.95;max-width:30em}}
.menu .row{{grid-template-columns:44px 1fr auto;gap:16px;align-items:start;padding:30px 0}}
.menu .nm{{font-size:20px;line-height:1.55}}
.menu .dt{{font-size:14px;line-height:1.85}}
.menu .pr{{padding-top:4px}}
.res .lede{{font-size:24px;line-height:1.75}}
.hero.brand-focus.lea-v4 h1{{font-size:clamp(64px,8.4vw,94px);line-height:.96;font-weight:500}}
.hero.brand-focus.lea-v4 .sub{{font-family:var(--serif);font-size:clamp(22px,2.3vw,30px);line-height:1.55;max-width:16em;margin-top:18px;opacity:.96}}
@media(max-width:760px){{
  .col,.narrow{{width:min(100% - 34px,680px)}}
  .draft{{font-size:10.5px;line-height:1.6;padding:8px 18px}}
  .hero{{min-height:91vh}}
  .hero .col{{padding-bottom:7vh}}
  .hero h1{{font-size:38px;line-height:1.28}}
  .hero.brand-focus h1{{font-size:56px;line-height:1.04}}
  .hero .sub{{font-size:14.5px;line-height:1.85;max-width:22em}}
  .theme-lea-editorial .top{{top:24px}}
  .hero.lea-v4{{min-height:86svh}}
  .hero.lea-v4 .col{{padding-bottom:6.5vh}}
  .hero.lea-v4 .eyebrow{{font-size:12px;margin-bottom:12px}}
  .hero.lea-v4 h1{{font-size:58px;line-height:.98}}
  .hero.lea-v4 .sub{{font-size:22px;line-height:1.55;max-width:16em;margin-top:14px}}
  .hero.brand-focus.lea-v4 h1{{font-size:58px;line-height:.98}}
  .hero.brand-focus.lea-v4 .sub{{font-size:22px;line-height:1.55;max-width:16em;margin-top:14px}}
  .hero.lea-v4 .hero-actions{{margin-top:24px;gap:12px}}
  .hero.lea-v4 .hero-cta-note{{font-size:11.8px;max-width:18em}}
  .lede{{font-size:21px;line-height:1.85}}
  .body{{font-size:14.5px;line-height:1.9}}
  .s{{padding:72px 0}}
  .s.tight{{padding:58px 0}}
  .theme-lea-editorial .s{{padding:60px 0}}
  .theme-lea-editorial .s.tight{{padding:48px 0}}
  .band.lea-band{{height:34vh;min-height:250px}}
  .menu .row{{grid-template-columns:34px 1fr;gap:12px;padding:24px 0}}
  .menu .pr{{grid-column:2}}
  .theme-lea-editorial .menu .row{{grid-template-columns:32px 1fr;padding:22px 0}}
  .theme-lea-editorial .menu .pr{{grid-column:2;text-align:left;padding-top:0}}
  .sample-note p{{text-align:left}}
  .story-grid figure{{aspect-ratio:4/3}}
}}
{lea_extra}\
@media(prefers-reduced-motion:reduce){{*{{transition:none!important}}.rv{{opacity:1;transform:none}}}}
"""


def has(v):
    if v is None: return False
    if isinstance(v, str): return bool(v.strip()) and not v.strip().startswith("[要確認")
    if isinstance(v, list): return any(has(x) for x in v)
    return bool(v)


def render(p):
    theme = p.get("theme", "warm-natural")
    style_theme = p.get("style_theme") or theme
    if style_theme not in THEME_CSS:
        style_theme = theme if theme in THEME_CSS else "warm-natural"
    theme_class = "theme-" + re.sub(r"[^a-zA-Z0-9_-]", "-", str(style_theme)).strip("-")
    profile_theme_class = ""
    if style_theme != theme:
        profile_theme_class = "profile-theme-" + re.sub(r"[^a-zA-Z0-9_-]", "-", str(theme)).strip("-")
    typo = str(p.get("typography_variant", "")).strip().lower()
    typo_class = "typo-" + re.sub(r"[^a-z0-9_-]", "", typo) if typo else ""
    ui_variant = str(p.get("ui_variant", "")).strip().lower()
    ui_class = "ui-" + re.sub(r"[^a-z0-9_-]", "", ui_variant) if ui_variant else ""
    body_class = " ".join(x for x in [theme_class, profile_theme_class, typo_class, ui_class] if x)
    brand_raw = p["brand"]
    loc_raw = p.get("locality", "")
    brand = esc(brand_raw); loc = esc(loc_raw)
    def brand_lockup(area):
        kicker = esc(p.get("brand_kicker", "プライベートサロン"))
        mark = esc(p.get("brand_mark", p.get("top_brand", brand_raw)))
        return (
            f'<span class="brand-lockup brand-lockup-{area}">'
            f'<span class="brand-kicker">{kicker}</span>'
            f'<span class="brand-latin">{mark}</span>'
            f'</span>'
        )
    use_lockup = bool(p.get("brand_lockup"))
    footer_brand = brand_lockup("footer") if use_lockup else brand
    top_label = p.get("top_label", loc_raw)
    top_label_text = str(top_label).strip() if has(top_label) else ""
    duplicate_top_label = top_label_text in {
        str(p.get("top_brand", "")).strip(),
        str(brand_raw).strip(),
    }
    top_label_html = "" if duplicate_top_label else (f'<span class="loc">{esc(top_label_text)}</span>' if top_label_text else "")
    footer_note = esc(p.get("footer_note", "提案サンプル・未送信・2026"))
    eyebrow = esc(p.get("category_label", ""))
    def disp(v):  # local relative asset -> basename (copied next to index.html); else as-is
        if has(v) and not str(v).startswith(("http", "data:", "/")):
            return Path(v).name
        return v
    subtle = bool(p.get("subtle_labels", False))  # v2: keep visitor flow clean, push 要確認 to a bottom layer
    draft_note = esc(p.get("draft_note", "提案サンプル（ドラフト・未送信）｜公開情報をもとにした構成案 / 写真は要差し替え"))
    hero_img = disp(p.get("hero_image"))
    hero_treat = p.get("hero_treatment", "duo")  # duo | soft | light | plain | art
    cta = esc(p.get("cta_label", "ご予約・お問い合わせ"))
    res_url = p.get("reservation_url") or p.get("website_url") or "#access"
    def css_val(v, fallback):
        s = str(v if has(v) else fallback)
        return re.sub(r"[^a-zA-Z0-9% .,_-]", "", s).strip() or fallback
    def price_html(value):
        text = str(value).strip()
        if "/" not in text:
            return esc(text)
        left, right = [x.strip() for x in text.split("/", 1)]
        return f'<span class="time">{esc(left)}</span><span class="yen">{esc(right)}</span>'
    hero_style = (
        f' style="--hero-pos:{css_val(p.get("hero_position"), "center center")};'
        f'--hero-pos-mobile:{css_val(p.get("hero_mobile_position"), p.get("hero_position") or "center center")}"'
    )

    # hero markup
    if has(hero_img):
        bg = f'<div class="bg"><img src="{esc(hero_img)}" alt="{brand}の店内"></div>'
        extra_hero_cls = re.sub(r"[^a-zA-Z0-9 _-]", "", str(p.get("hero_class", ""))).strip()
        hero_cls = " ".join(x for x in ["hero", hero_treat, extra_hero_cls] if x)
        top_cls = "top" if hero_treat == "light" else "top dark"
        tag = '' if subtle else '<span class="tag">サンプル画像（要差し替え・写真許諾後）</span>'
    else:
        bg = f'<div class="bg"><img src="{art_hero_svg(theme)}" alt="アートワーク（要写真差し替え）"></div>'
        extra_hero_cls = re.sub(r"[^a-zA-Z0-9 _-]", "", str(p.get("hero_class", ""))).strip()
        hero_cls = " ".join(x for x in ["hero", "art", extra_hero_cls] if x)
        top_cls = "top"
        tag = '<span class="tag">アートワーク（写真の差し替え推奨）</span>'

    header_html = f'<header class="{top_cls}"><div class="col">{top_label_html}</div></header>' if top_label_html else ""

    if p.get("hero_lockup"):
        hero_lines = brand_lockup("hero")
    else:
        hero_lines = "<br>".join(esc(x) for x in p.get("hero_lines", [brand]))
    sub = f'<p class="sub rv">{inline_keep_terms(p["hero_sub"])}</p>' if has(p.get("hero_sub")) else ""
    hero_meta = ""
    if p.get("hero_meta"):
        items = "".join(f"<li>{esc(x)}</li>" for x in p["hero_meta"] if has(x))
        hero_meta = f'<ul class="hero-meta rv">{items}</ul>' if items else ""
    hero_cta_note = f'<p class="hero-cta-note rv">{esc(p["hero_cta_note"])}</p>' if has(p.get("hero_cta_note")) else ""

    # intro
    intro = ""
    if has(p.get("intro")):
        body = f'<p class="body rv">{esc(p["intro_body"])}</p>' if has(p.get("intro_body")) else ""
        intro = (f'<section class="s narrow-sec"><div class="narrow">'
                 f'<p class="kick rv">{esc(p.get("intro_kick","はじめに"))}</p>'
                 f'<p class="lede rv">{esc(p["intro"])}</p>{body}</div></section>')

    # visual break band
    band = ""
    bimg = disp(p.get("band_image"))
    if has(bimg):
        bcap = '' if subtle else '<span class="cap">サンプル画像（要差し替え）</span>'
        band_style = f' style="--band-pos:{css_val(p.get("band_position"), "center center")}"'
        band = (f'<section class="band {p.get("band_treatment","duo")}">'
                f'<img{band_style} src="{esc(bimg)}" alt="店内の様子">{bcap}</section>')
    elif p.get("band_art", True):
        band = ('<section class="band art"><svg width="100%" height="100%" preserveAspectRatio="xMidYMid slice" '
                'viewBox="0 0 1200 500" xmlns="http://www.w3.org/2000/svg">'
                '<rect width="1200" height="500" fill="var(--paper2)"/></svg>'
                '<span class="cap">写真の差し替え推奨</span></section>')

    # menu
    menu = ""
    if p.get("menu"):
        rows = []
        for i, m in enumerate(p["menu"], 1):
            idx = esc(m.get("index") or f"{i:02d}")
            dt = f'<span class="dt">{esc(m["detail"])}</span>' if has(m.get("detail")) else ""
            if has(m.get("price")):
                pr = f'<div class="pr">{price_html(m["price"])}</div>'
            elif subtle:
                pr = ""  # no repeated "要確認" in the visitor flow; covered by one section note
            else:
                pr = '<div class="pr tbd">料金はお問い合わせ</div>'
            rows.append(f'<div class="row rv"><div class="idx">{idx}</div><div><div class="nm">{esc(m["name"])}</div>{dt}</div>{pr}</div>')
        mintro = f'<p class="menu-intro rv">{esc(p["menu_intro"])}</p>' if has(p.get("menu_intro")) else ""
        mnote = f'<p class="menu-note rv">{esc(p["menu_note"])}</p>' if has(p.get("menu_note")) else ""
        menu = (f'<section class="s tight"><div class="narrow"><p class="kick rv">{esc(p.get("menu_kick","おしながき"))}</p>'
                f'{mintro}<div class="menu">{"".join(rows)}</div>{mnote}</div></section>')

    # flow
    flow = ""
    if p.get("flow"):
        rows = "".join(f'<div class="r rv"><div class="no">0{i}</div><div><h3>{esc(f["label"])}</h3>'
                       f'<p>{esc(f["text"])}</p></div></div>' for i, f in enumerate(p["flow"], 1))
        flow = (f'<section class="s tight"><div class="narrow"><p class="kick rv">{esc(p.get("flow_kick","ご来店の流れ"))}</p>'
                f'<div class="flow">{rows}</div></div></section>')

    # story (optionally with an atmosphere image beside it)
    story = ""
    if has(p.get("story")):
        sign = f'<p class="sign rv">{esc(p["story_sign"])}</p>' if has(p.get("story_sign")) else ""
        simg = disp(p.get("story_image"))
        kick = esc(p.get("story_kick", "このお店のこと"))
        if has(simg):
            sph = '' if subtle else '<p class="ph">サンプル画像（要差し替え）</p>'
            story_style = f' style="--story-pos:{css_val(p.get("story_position"), "center center")}"'
            story = (f'<section class="s story"><div class="col"><div class="story-grid">'
                     f'<div><p class="kick rv">{kick}</p><p class="lede rv">{esc(p["story"])}</p>{sign}</div>'
                     f'<figure class="rv"><img{story_style} src="{esc(simg)}" alt="店内の様子">{sph}</figure>'
                     f'</div></div></section>')
        else:
            story = (f'<section class="s story"><div class="narrow"><p class="kick rv">{kick}</p>'
                     f'<p class="lede rv">{esc(p["story"])}</p>{sign}</div></section>')

    # access + reservation
    info_rows = []
    for k, v in p.get("access", []):
        if has(v):
            info_rows.append(f'<div class="r"><div class="k">{esc(k)}</div><div>{esc(v)}</div></div>')
    res_note = f'<p class="note">{esc(p["res_note"])}</p>' if has(p.get("res_note")) else ""
    access_intro = f'<p class="access-intro rv">{esc(p["access_intro"])}</p>' if has(p.get("access_intro")) else ""
    methods = "".join(f"<li>{esc(x)}</li>" for x in p.get("reservation_methods", []) if has(x))
    methods_html = f'<ul class="method-list">{methods}</ul>' if methods else ""
    access = (f'<section class="s" id="access"><div class="col"><div class="acc">'
              f'<div><p class="kick rv">アクセス</p>{access_intro}<div class="info rv">{"".join(info_rows)}</div></div>'
              f'<div class="res rv"><p class="lede">{esc(p.get("res_line","ご予約・お問い合わせ"))}</p>'
              f'<a class="go" href="{esc(res_url)}">{cta} <span>&rarr;</span></a>{methods_html}{res_note}</div>'
              f'</div></div></section>')

    # bottom "このデモについて" layer — collects 要確認/差し替え items off the visitor flow
    demo_notes_html = ""
    if p.get("demo_notes"):
        items = "".join(f"<li>{esc(n)}</li>" for n in p["demo_notes"] if has(n))
        demo_notes_html = (f'<section class="demo-notes"><div class="narrow">'
                           f'<p class="dn-kick">このデモについて（確認用メモ）</p>'
                           f'<p class="dn-lead">{esc(p.get("demo_notes_lead","以下は、実際のお店の内容に差し替える前提の項目です。"))}</p>'
                           f'<ul>{items}</ul></div></section>')
    sample_note_html = ""
    if has(p.get("sample_lp_note")):
        sample_note_html = f'<section class="sample-note"><div class="narrow"><p>{esc(p["sample_lp_note"])}</p></div></section>'

    draft_html = f'<div class="draft">{draft_note}</div>' if p.get("show_draft_note", True) else ""

    page = f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex,nofollow">
<title>{brand}｜{loc}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Shippori+Mincho:wght@400;500;600&family=Zen+Kaku+Gothic+New:wght@400;500;700&display=swap" rel="stylesheet">
<style>{base_css(style_theme)}</style></head>
<body class="{esc(body_class)}">
{draft_html}
{header_html}

<section class="{hero_cls}"{hero_style}>
  {bg}<div class="overlay"></div>
  <div class="col">
    <p class="eyebrow rv">{eyebrow}</p>
    <h1 class="rv">{hero_lines}</h1>
    {sub}
    {hero_meta}
    <div class="hero-actions"><a class="go primary rv" href="#access">{cta} <span>&rarr;</span></a>{hero_cta_note}</div>
  </div>
  {tag}
</section>

{intro}
{band}
{menu}
{flow}
{story}
{access}
{demo_notes_html}
{sample_note_html}

<footer><div class="col"><span class="wordmark">{footer_brand}</span><span class="fn">{loc}　/　{footer_note}</span></div></footer>
<script>
document.documentElement.classList.add('js');
const revealAll=()=>document.querySelectorAll('.rv').forEach(el=>el.classList.add('in'));
if('IntersectionObserver' in window){{
  const io=new IntersectionObserver((es)=>{{es.forEach(e=>{{if(e.isIntersecting){{e.target.classList.add('in');io.unobserve(e.target)}}}})}},{{threshold:.12,rootMargin:'0px 0px 12% 0px'}});
  document.querySelectorAll('.rv').forEach((el,i)=>{{el.style.transitionDelay=Math.min(i*0.05,0.3)+'s';io.observe(el)}});
  setTimeout(revealAll,1400);
}}else{{
  revealAll();
}}
</script>
</body></html>"""
    return page


def main():
    prof = ROOT / "profiles"
    out = ROOT.parent.parent / "generated_demos" / "salon_100_point_samples"
    out.mkdir(parents=True, exist_ok=True)
    bad = 0
    for pf in sorted(prof.glob("*.json")):
        p = json.loads(pf.read_text(encoding="utf-8"))
        page = render(p)
        hits = scan_forbidden(page)
        d = out / pf.stem; d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page, encoding="utf-8")
        # copy referenced local asset alongside if relative
        for key in ("hero_image", "band_image"):
            v = p.get(key)
            if has(v) and not str(v).startswith(("http", "data:", "/")):
                src = ROOT / v
                if src.exists():
                    (d / Path(v).name).write_bytes(src.read_bytes())
        print(f"[{'PASS' if not hits else 'FORBIDDEN '+str(hits)}] {pf.stem} ({len(page)}b, theme={p.get('theme')})")
        bad += 1 if hits else 0
    print("OVERALL:", "PASS" if not bad else "FAIL")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
