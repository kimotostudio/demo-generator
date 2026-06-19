# Demo quality checklist — Variant A salon LP (v0)

Each render writes `quality.json`. Hard checks must all pass (`_pass: true`); `[要確認]` items are
surfaced for human confirmation, not auto-filled.

## Automated checks (in quality.json)
| Check | Meaning |
|---|---|
| salon_name_present | 店名が正しく入っている（[要確認]でない） |
| area_present | 地域が入っている |
| category_known | 業種が判定できている |
| menu_from_real_info | メニュー名が実在情報に基づく（捏造でない） |
| no_forbidden_in_injected_copy | 注入コピーに禁止語ゼロ |
| no_forbidden_in_full_page | ページ全体に禁止語ゼロ（JSコメントの「スクロール効果」は除外） |
| booking_route_present | 予約導線（URL）がある |
| owner_or_atmosphere_reflected | オーナー or 雰囲気が反映されている |
| no_invented_owner_photo | オーナー写真を捏造していない |
| sample_image_label_present | 画像に「サンプル画像」ラベルあり |
| proposal_draft_label_present | 「提案サンプル（ドラフト・未送信）」ラベルあり |
| all_slots_filled | 未置換 {{SLOT}} が残っていない |
| no_external_send_performed | 外部送信していない（常にtrue：生成は送信しない） |

## Manual review (human, before any deploy/outreach)
- [ ] 店名・地域・業種が実態と一致
- [ ] メニュー名・価格が実在情報（または[要確認]のまま）
- [ ] 医療/効果/保証の断定なし
- [ ] お客様の声はプレースホルダーのまま（捏造なし）
- [ ] オーナー/雰囲気が伝わる、generic感が弱い
- [ ] スマホ表示OK（要 screenshot 確認 — v0は手動ブラウザ確認）
- [ ] deploy するなら noindex draft のみ・Yu承認後
- [ ] 外部送信は行わない（手動アウトリーチのみ）

## Known v0 gap
- ローカルにブラウザ/Playwrightが無いため自動スクリーンショット未対応。
  スマホ表示確認は手動、または別途軽量スクショ用Codexタスクで補完する。
