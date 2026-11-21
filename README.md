# Serenia by House of Jets

Landing site and guides for Serenia (C Tower), Kiwale, Pune. Live address: https://sereniakiwale.com

Plain static HTML, CSS and JavaScript. No framework.

Build: `npm run build` (output directory: `dist`).

## Before launch, replace these placeholders
- MahaRERA registration number (footer, About, FAQ)
- Possession date
- 30 vs 32 floors for C Tower (highlights card)
- Simplex area label: carpet or total
- Exact map pin (Location section)
- Relationship manager email in `js/config.js` (`DEFAULT_MANAGER_EMAIL`)
- Written permission to use the promoter name and photos
- Analytics IDs in `js/config.js` (GA4, GTM, Meta Pixel), if used

Leads are saved to the shared Supabase `enquiries` table, tagged with `project = "Serenia by House of Jets"`.
