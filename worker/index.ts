// Cloudflare Worker entrypoint.
//
// This project deploys as a Worker with static assets (not Cloudflare Pages),
// so there is no functions/ directory routing. This Worker handles the one API
// route (/api/summary) and delegates everything else to the static-assets
// binding, which serves the built React app (with SPA fallback configured in
// wrangler.jsonc).

import { handleSummary, type SummaryEnv } from "./summary";

// Minimal shape of the static-assets binding (avoids depending on
// @cloudflare/workers-types just for this).
type AssetsFetcher = { fetch: (request: Request) => Promise<Response> };

interface Env extends SummaryEnv {
  ASSETS: AssetsFetcher;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    if (url.pathname === "/api/summary") {
      return handleSummary(request, env);
    }
    // Everything else: serve the static site.
    return env.ASSETS.fetch(request);
  },
};
