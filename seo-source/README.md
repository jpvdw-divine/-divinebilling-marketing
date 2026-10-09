# SEO source (not served)

The source that generated the SEO pages published in `public/` (commit 1110534: `/faq`,
four SA guides, `robots.txt`, `sitemap.xml`, `llms.txt`, canonical URLs, Open Graph and
JSON-LD on every page). It lives here, not in the DivineBilling product repo.

Only `public/` is deployed (see `wrangler.toml`), so nothing in this folder reaches the website.

## What is here

| Path | What it is |
| --- | --- |
| `files/seo_site.py` | Page metadata, JSON-LD, `robots.txt` / `sitemap.xml` / `llms.txt` bodies, FAQ and guide routes |
| `files/guides_content.py` | Text of the four SA guides |
| `files/templates/faq_public.html`, `guides_index.html`, `guide_public.html` | FAQ and guide page templates |
| `tests/test_seo_site.py` | Tests for the above |
| `divinebilling-changes.patch` | Edits to existing DivineBilling files: SEO tags in the public page templates, `marketing.css` (FAQ and guide styles), and the freeze tool (`files/` and `tools/freeze_marketing_public.py`) so it also writes `/faq`, `/guides/*`, `robots.txt`, `sitemap.xml` and `llms.txt` |

## Regenerating the pages

The pages are rendered by the DivineBilling app and frozen into `public/`. To rebuild them:

1. In a DivineBilling checkout, copy `files/` and `tests/` from here over the repo, then
   `git apply seo-source/divinebilling-changes.patch` (it applied cleanly to DivineBilling v2.10.350).
2. Wire the routes into `files/app.py`:
   - after `register_marketing_site(app)`: `from seo_site import register_seo` and `register_seo(app)`;
   - `robots_txt()` and `sitemap_xml()` return `seo_site.robots_body()` / `seo_site.sitemap_body()`;
   - add `'llms_txt'` to `_PORTAL_PUBLIC_ENDPOINTS` and to the endpoint skip list in `_portal_session_heal`;
   - add `'/faq'` and `path.startswith('/guides')` to the public paths in `_no_store_auth_pages`.
3. Run `python tools/freeze_marketing_public.py`, copy the output into this repo's `public/`, commit and push.

Do not commit these files to the DivineBilling repo: a release once shipped `from seo_site import register_seo`
without `seo_site.py` and took the login server down.
