const LOGIN = "https://login.divinebilling.online";
const DASH = "https://dash.divinebilling.online";
const PLATFORM_PRICING = "https://platform.divinebilling.online/api/public-pricing";
const WWW = "https://www.divinebilling.online";
const FORM_POSTS = ["/get-started/signup", "/contact", "/become-a-reseller"];

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname.replace(/\/+$/, "") || "/";
    // One canonical host for search engines: fold the apex onto www.
    if (url.hostname === "divinebilling.online" && (request.method === "GET" || request.method === "HEAD")) {
      url.hostname = new URL(WWW).hostname;
      return Response.redirect(url.toString(), 301);
    }
    if (path === "/login") {
      return Response.redirect(`${LOGIN}/`, 301);
    }
    // Marketing forms post to www; the app on Dash handles them.
    if (FORM_POSTS.includes(path) && request.method === "POST") {
      const headers = new Headers(request.headers);
      headers.delete("host");
      const upstream = await fetch(`${DASH}${path}`, {
        method: "POST",
        headers,
        body: request.body,
        redirect: "manual",
      });
      if (upstream.status >= 300 && upstream.status < 400) {
        const loc = (upstream.headers.get("Location") || path)
          .replace("https://dash.divinebilling.online", WWW)
          .replace("https://login.divinebilling.online", WWW);
        return Response.redirect(new URL(loc, WWW).toString(), 302);
      }
      return upstream;
    }
    if (path === "/pricing.json") {
      try {
        const upstream = await fetch(PLATFORM_PRICING, {
          headers: { Accept: "application/json" },
        });
        if (!upstream.ok) {
          // Platform 404/500 pages are HTML; never pass them off as JSON.
          throw new Error(`pricing upstream ${upstream.status}`);
        }
        const body = await upstream.text();
        return new Response(body, {
          status: 200,
          headers: {
            "Content-Type": "application/json; charset=utf-8",
            "Cache-Control": "public, max-age=60",
          },
        });
      } catch (err) {
        return new Response(JSON.stringify({ error: "pricing unavailable" }), {
          status: 502,
          headers: { "Content-Type": "application/json; charset=utf-8" },
        });
      }
    }
    if (!env.ASSETS) {
      return new Response("Marketing assets are not bound", { status: 500 });
    }
    return env.ASSETS.fetch(request);
  },
};
