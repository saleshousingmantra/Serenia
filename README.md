# Serenia by House of Jets

Landing site and guides for Serenia (C Tower), Kiwale, Pune. Live address: https://sereniakiwale.com

Plain static HTML, CSS and JavaScript. No framework.

Build: `npm run build` (output directory: `dist`).

## Before launch, replace these placeholders
- Possession date
- 30 vs 32 floors for C Tower (highlights card)
- Simplex area label: carpet or total
- Exact map pin (Location section)
- Relationship manager email in `js/config.js` (`DEFAULT_MANAGER_EMAIL`)
- Written permission to use the promoter name and photos
- Analytics IDs in `js/config.js` (GA4, GTM, Meta Pixel), if used

MahaRERA No. PM1260002602794 is shown in the footer, About section, FAQ and page description.

Leads are saved to the shared Supabase `enquiries` table, tagged with `project = "Serenia by House of Jets"`.

## 2026-11-27 upgrade
`scripts/retrofit.py` applies the Ceratec-era upgrades to the built site (keywords/geo meta, About, Privacy and Cookie pages, footer links and consent line, noscript form fallback, accessibility and contrast fixes, honest sitemap `lastmod` in `scripts/lastmod.json`, `llms.txt`, caching and security headers). **Run `python3 scripts/retrofit.py .` after `node scripts/build.mjs`** so regenerated pages keep the fixes. Then run `python3 scripts/audit_seo.py . https://sereniakiwale.com` and `python3 scripts/audit_deep.py .` (both must pass).

TODO for the client: confirm the map pin (latitude/longitude) and set `lat`/`lon` in `scripts/retrofit.json` to add `geo.position`, `ICBM` and GeoCoordinates; have the policy pages reviewed by a lawyer; add the operator's registered name and contact details.

## 2026-11-28 keyword pages
Run `python3 scripts/kwpages.py .` then `python3 scripts/retrofit.py .` after `node scripts/build.mjs` or the scheduled `apply-schedule.py`. `kwpages.py` writes 18 keyword pages from `scripts/kwpages.json`; the `/flat-guides/` hub is linked from the footer by the retrofit. The daily guide job rewrites the sitemap and hub, so it must end with `retrofit.py`.
