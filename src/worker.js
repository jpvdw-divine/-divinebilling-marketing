const LOGIN = "https://login.divinebilling.online";
const DASH = "https://dash.divinebilling.online";
const PLATFORM_PRICING = "https://platform.divinebilling.online/api/public-pricing";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname.replace(/\/+$/, "") || "/";
    if (path === "/login") {
      return Response.redirect(`${LOGIN}/`, 301);
    }
    if (path === "/get-started/signup" && request.method === "POST") {
      const headers = new Headers(request.headers);
      headers.delete("host");
      const upstream = await fetch(`${DASH}/get-started/signup`, {
        method: "POST",
        headers,
        body: request.body,
        redirect: "manual",
      });
      if (upstream.status >= 300 && upstream.status < 400) {
        const loc = upstream.headers.get("Location") || "/get-started/signup";
        const next = loc
          .replace("https://dash.divinebilling.online", "https://www.divinebilling.online")
          .replace("https://login.divinebilling.online", "https://www.divinebilling.online");
        return Response.redirect(next, 302);
      }
      return upstream;
    }
    if (path === "/pricing.json") {
      try {
        const upstream = await fetch(PLATFORM_PRICING, {
          headers: { Accept: "application/json" },
        });
        const body = await upstream.text();
        return new Response(body, {
          status: upstream.ok ? 200 : upstream.status,
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
