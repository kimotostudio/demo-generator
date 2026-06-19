
## Addendum 2026-06-18 (from Hokkaido 0100–0150 list)
- NAME CONFIRMATION: never use a page title/heading as the 屋号. On jimdofree/crayonsite/goope, page titles are
  often generic ("施術メニュー","メニュー表","サービス") → 41% of that batch was 屋号ミス (wrong name in the demo).
  Require a confirmed business name (name_confidence) BEFORE demo generation; otherwise hold for manual naming.
- DEMO-LINEAGE SUPPRESSION: treat `kimotostudio12.netlify.app/<id>` demo URLs as already-demoed → block re-target.
- goope redirector: `r.goope.jp` is a shared redirector root, not a unique own-site → low source quality.
