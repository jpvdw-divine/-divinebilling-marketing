# DivineBilling public marketing site

Cloudflare Worker that serves **www.divinebilling.online** and **divinebilling.online**.

- Assets: `public/` (frozen catalog)
- Worker: `src/worker.js` (login redirect, signup POST, live pricing JSON)
- Source of pages: freeze from the product repo, then `python tools/publish_marketing_site.py`

Deploy:

```bash
npx wrangler deploy
```

GitHub Actions deploys `main` when `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` are set as repository secrets.
