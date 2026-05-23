// Minimal client for the Wikipedia REST page-summary endpoint.
// CORS is permitted, no API key needed.
// Docs: https://en.wikipedia.org/api/rest_v1/

export type WikiSummary = {
  title: string;
  description?: string;
  extract?: string;
  thumbnail?: { source: string; width: number; height: number };
  originalimage?: { source: string; width: number; height: number };
  content_urls?: { desktop?: { page?: string } };
};

const cache = new Map<string, Promise<WikiSummary | null>>();

/** Extract the article title from a wikipedia URL. Returns null if not wiki. */
export function wikiTitleFromUrl(url: string | null | undefined): string | null {
  if (!url) return null;
  try {
    const u = new URL(url);
    if (!u.hostname.endsWith("wikipedia.org")) return null;
    const m = u.pathname.match(/^\/wiki\/(.+)$/);
    if (!m) return null;
    return decodeURIComponent(m[1]).split("#")[0]; // strip fragment
  } catch {
    return null;
  }
}

/** Returns null if the article doesn't exist or the request fails. Cached. */
export function fetchWikiSummary(title: string): Promise<WikiSummary | null> {
  const key = title;
  const cached = cache.get(key);
  if (cached) return cached;
  const url =
    "https://en.wikipedia.org/api/rest_v1/page/summary/" +
    encodeURIComponent(title.replace(/ /g, "_"));
  const p: Promise<WikiSummary | null> = fetch(url, {
    headers: { accept: "application/json" },
  })
    .then((r) => (r.ok ? (r.json() as Promise<WikiSummary>) : null))
    .catch(() => null);
  cache.set(key, p);
  return p;
}
