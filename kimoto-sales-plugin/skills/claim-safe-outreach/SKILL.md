---
name: claim-safe-outreach
description: Write soft, honest, claim-safe outreach for salon demo LPs. Use when drafting the email/form message that accompanies a demo page. Manual send only.
---

# Claim-Safe Outreach

Outreach is a **proposal / gift, not criticism.** The demo is "here's a way your shop could look," never a
list of the salon's faults. The owner should feel *understood and helped*, not graded.

## Tone rules

- **Outreach is NOT criticism.** The demo is a sample/gift, not a fault list.
- **Avoid any "改善点があります" / "ここがダメ" tone.** Never imply the current page is bad.
- **Never use the phrase "興味ありと返信".** Do not pressure a specific reply.
- Keep it **short and soft.** A few honest lines, easy to ignore.
- Always leave an easy out ("ご不要でしたら、そのままスルーしていただいて大丈夫です。").
- Invite a question, not a commitment.

## Identity & contact rules

- **Signature uses 木許 only** — never the full name 木許裕輔.
- **No phone number.** **No birth date.** No personal identifiers beyond the studio name + reply email.
- Real identity only: KIMOTO STUDIO / 木許 / kimoto.studio21@gmail.com. Never a fake identity, never
  someone else's contact.

## Channel rules

- **Email / form only** for now.
- **No DM** unless Yu explicitly chooses it for a specific lead.
- **NO auto-send.** This skill drafts; Yu sends. NO form submit, NO Gmail/SMTP/API, NO phone.
- `sent=0` until Yu explicitly says "sent <lead>". Deploy ≠ send.
- NO git push.

---

## STANDARD MESSAGE (verbatim)

Use this template; fill `{business_name}`, `{demo_url}`, and
`{{salon_atmosphere_or_category_appeal}}` only. Do not add claims, do not add pressure.

件名:
【ご確認】{business_name}様向けのデモページについて

本文:
{business_name}様

はじめまして。
KIMOTO STUDIOの木許と申します。

貴店のページを拝見し、{{salon_atmosphere_or_category_appeal}}が、初めての方にももう少し伝わりやすくなる見せ方ができそうだと思い、簡単なデモページを作成しました。

デモページ：
{demo_url}

あくまで一つの見せ方のサンプルです。
文章・写真・メニュー内容などは、実際の内容に合わせて調整できます。

ご不要でしたら、そのままスルーしていただいて大丈夫です。
もし気になる点があれば、ご質問だけでもお気軽にご返信ください。

お忙しいところ失礼いたしました。

――――――――
KIMOTO STUDIO
木許
Email: kimoto.studio21@gmail.com
――――――――

---

## Source-aware atmosphere/category phrase

`{{salon_atmosphere_or_category_appeal}}` must be short, source-aware, and either human-curated or
grounded in visible lead/profile evidence. If no curated phrase exists, use the neutral fallback:
`雰囲気やメニューの魅力`.

Safe example phrases:

- 落ち着いた雰囲気やリラクゼーションメニューの魅力
- やさしい雰囲気やヘッドスパメニューの魅力
- 清潔感のある空間やメニューの見やすさ
- 通いやすそうな雰囲気や予約前に知りたい情報
- プライベートサロンらしい落ち着きやメニューの魅力

Do not overpraise. Do not invent specifics. No medical-beauty-effect or guaranteed-result claims.

---

## Before handing to the manual-send step

- `{business_name}` matches the real store name; `{demo_url}` is the correct, live demo for THIS lead.
- `{{salon_atmosphere_or_category_appeal}}` is either curated from source-aware evidence or the neutral fallback.
- No forbidden claims, no criticism tone, no "興味ありと返信", no full name, no phone, no birth date.
- Signature is 木許 + kimoto.studio21@gmail.com only.
- The message is short, soft, and easy to ignore.
