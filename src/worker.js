const LOGIN = "https://login.divinebilling.online";
const PLATFORM_PRICING = "https://platform.divinebilling.online/api/public-pricing";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname.replace(/\/+$/, "") || "/";
    if (path === "/login") {
      return Response.redirect(`${LOGIN}/`, 301);
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
