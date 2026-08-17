const LOGIN = "https://login.divinebilling.online";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname.replace(/\/+$/, "") || "/";
    if (path === "/login") {
      return Response.redirect(`${LOGIN}/`, 301);
    }
    if (!env.ASSETS) {
      return new Response("Marketing assets are not bound", { status: 500 });
    }
    return env.ASSETS.fetch(request);
  },
};
