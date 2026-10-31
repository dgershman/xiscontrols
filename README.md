# xiscontrols.com

The new XIS Controls website: a searchable catalog of turnstile replacement parts with an order-request cart,
a "send us a photo" identification form, the Library of manuals and drawings, and a web admin so prices and parts
can be edited in a browser.

Built from the April 2026 discovery call. The goals from that call:

- Get people to the right part the first time (search by part number, OEM number, brand, model, or shop-floor words like "dog" for pawl).
- Keep the phone number in front of everyone, and give confused customers a photo path instead of a guess.
- No sign-in, ever. Prices are public.
- Keep the personality of the old site.
- Make the business less dependent on one person answering the phone.

## Stack

- [Astro](https://astro.build) static site. Every part is a Markdown file in `src/content/parts/`.
- Client-side search with [Fuse.js](https://fusejs.io) over `/search-index.json` (built at deploy time), plus a synonym list in `src/lib/catalog-synonyms.ts`.
- Order requests and photo uploads go to two Cloudflare Pages Functions in `functions/api/`, which email via [Resend](https://resend.com).
- Web admin at `/admin/` is [Sveltia CMS](https://github.com/sveltia/sveltia-cms). Saves commit to this repo; the site rebuilds automatically.

## Run it locally

```bash
npm install
npm run dev        # http://localhost:4321
npm run build      # static output in dist/
```

## Deploy on Cloudflare Pages

1. Cloudflare dashboard > Workers & Pages > Create > Pages > Connect to Git > `dgershman/xiscontrols`.
2. Build command `npm run build`, output directory `dist`. Node 22.
3. Settings > Environment variables (Production):
   - `RESEND_API_KEY`: from resend.com (free tier covers this volume)
   - `MAIL_FROM`: e.g. `XIS Controls <orders@xiscontrols.com>` (verify the domain in Resend first)
   - `ORDER_TO`: optional, defaults to `xiscontrols@gmail.com`
4. Point the `xiscontrols.com` DNS at the Pages project (Custom domains tab). HTTPS is automatic, which also fixes the old "no valid certificate" warning.

Until mail is configured, the order and photo forms fail gracefully: the order page offers a pre-filled email instead.

`public/_redirects` sends every old URL (`/About.htm`, `/Manuals/Library.htm`, old PDF and photo paths) to its new home, so existing Google results and bookmarks keep working.

## Editing the site (for Albert)

Go to `https://xiscontrols.com/admin/`, sign in, and pick a part. Change the price, availability, photos, manuals, or
description, then Save. The live site updates in about a minute.

Sign-in options for the admin:

- **Simplest:** sign in with a GitHub personal access token (Sveltia shows this option). Albert needs a GitHub account with write access to this repo.
- **Nicer:** deploy [sveltia-cms-auth](https://github.com/sveltia/sveltia-cms-auth) as a free Cloudflare Worker and set `base_url` in `public/admin/config.yml` to get a "Sign in with GitHub" button.

Analytics: put a Cloudflare Web Analytics token or a Google Analytics ID in Site settings > Contact info > Analytics.

## Where things live

| What | Where |
| --- | --- |
| Parts (one file each) | `src/content/parts/*.md` |
| Categories, blurbs and the sticky-note jokes | `src/data/categories.json` |
| Brands and the "who bought whom" notes | `src/data/brands.json` |
| Phone, email, address, analytics | `src/data/site.json` |
| Library documents | `src/data/library.json` |
| Photos, PDFs, drawings | `public/media/` |
| Search synonyms ("dog" means pawl) | `src/lib/catalog-synonyms.ts` |
| Old-site import scripts | `tools/legacy-import/` |
| Import report (parts that need a human look) | `src/data/import-report.json` |

## Open items to review with Albert

- Titles were generated from the old descriptions. Most read fine; some are long or odd and are quick fixes in the admin.
- Rows the import flagged are listed in `src/data/import-report.json` (e.g. counters 80-5Cxx with two prices, 45-019F sale price).
- Confirm the "1,700 boards in the field" line on the home page.
- Some fun images are well-known characters (the Batman panel, the cartoon alligator, King Kong, the Indiana Jones warehouse). They came from the old site, but they're copyrighted, which matters more if the business is being sold. Consider swapping them for originals.
- Not yet ported: the THT-100 recommended spare parts comparison, the Parts Bin clearance page, the Model 600 Event Controller page, and Specialty PLCs.
- Phase 2 ideas from the call: card checkout for repeat customers, shipping automation, clickable exploded drawings, picture search, and the AI assistant with escalation to Albert.
