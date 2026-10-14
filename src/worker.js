const LOGIN = "https://login.divinebilling.online";
const MONITOR = "https://monitor.divinebilling.one/api/collections";
const PLATFORM_PRICING = "https://platform.divinebilling.online/api/public-pricing";
const WWW = "https://www.divinebilling.online";
const FORM_POSTS = ["/get-started/signup", "/contact", "/become-a-reseller"];

async function monitorJson(path) {
  const resp = await fetch(MONITOR + path, {
    headers: { Accept: "application/json", "User-Agent": "DivineBilling-status/1" },
  });
  if (!resp.ok) throw new Error("monitor " + resp.status);
  return resp.json();
}

function statusLabel(status) {
  if (status === "up") return ["Up", true];
  if (status === "down") return ["Down", false];
  if (status === "warning") return ["Degraded", false];
  if (status === "paused") return ["Paused", false];
  return ["Unknown", false];
}

async function platformStatus() {
  const now = new Date().toISOString().slice(0, 16).replace("T", " ") + " UTC";
  try {
    const pages = (await monitorJson("/operational_page/records?perPage=20")).items || [];
    const page = pages.find((row) => row.slug === "Platform" && row.is_public === "true");
    if (!page) throw new Error("Platform status page is not public");
    const filter = encodeURIComponent("(operational_status_id='" + page.id + "')");
    const components = (await monitorJson("/status_page_components/records?perPage=50&filter=" + filter)).items || [];
    components.sort((a, b) => (a.display_order || 0) - (b.display_order || 0));
    const checks = [];
    let latest = "";
    for (const comp of components) {
      let service = {};
      if (comp.service_id) {
        try {
          service = await monitorJson("/services/records/" + encodeURIComponent(comp.service_id));
        } catch (err) {
          service = {};
        }
      }
      const status = String(service.status || "unknown").toLowerCase();
      const [label, ok] = statusLabel(status);
      const ms = Number(service.response_time || 0);
      const checked = service.last_checked || "";
      if (checked > latest) latest = checked;
      let detail = label;
      if (ok) detail = "Responding" + (ms ? " · " + ms + " ms" : "");
      else if (status === "down") detail = "Not responding";
      checks.push({
        name: comp.name || service.name || "Service",
        url: service.host || service.domain || "",
        ok,
        label,
        detail,
      });
    }
    return {
      ok: checks.length > 0 && checks.every((row) => row.ok),
      checked_at: latest
        ? latest.replace("T", " ").replace(".000Z", " UTC").replace("Z", " UTC")
        : now,
      note: "Live status from the platform monitor. This is not an SLA and we do not publish an uptime percentage.",
      checks,
    };
  } catch (err) {
    return {
      ok: false,
      checked_at: now,
      note: "The platform monitor could not be read just now.",
      checks: [{
        name: "Platform monitor",
        url: "monitor.divinebilling.one",
        ok: false,
        label: "Down",
        detail: String(err && err.message ? err.message : err).slice(0, 140),
      }],
    };
  }
}

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
    if (path === "/status.json") {
      const payload = await platformStatus();
      return new Response(JSON.stringify(payload), {
        status: payload.ok ? 200 : 503,
        headers: {
          "Content-Type": "application/json; charset=utf-8",
          "Cache-Control": "no-store",
        },
      });
    }
    // Marketing forms post to www. dash.divinebilling.online answers with an
    // nginx redirect and drops the body, so these go to the login host, which
    // forwards them onto the DivineOnline books.
    if (FORM_POSTS.includes(path) && request.method === "POST") {
      const headers = new Headers(request.headers);
      headers.delete("host");
      const upstream = await fetch(`${LOGIN}${path}`, {
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
