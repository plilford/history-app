// =============================================================================
// Per-occurrence colours — region-based.
// =============================================================================
//
// Each occurrence gets a colour derived from its DOMINANT region (the highest
// region_weight on the row), with intra-region hue variation seeded from the
// occurrence id so adjacent entries on the same region stay distinguishable.
//
// Region → base hue:
//   europe       → 220° (blue)
//   americas     → 135° (green)
//   asia         →  10° (red)
//   africa       →  40° (amber)
//   australasia  → 280° (purple)
//   global       →   —  (neutral grey, sat=0)
//
// The exported palette covers two surfaces:
//   - `fill`        background of the occurrence box (semi-transparent)
//   - `line`        range line for periods (same hue family, higher alpha)
//
// The BOX OUTLINE (border) is theme-driven (black on light, white on dark)
// and style-driven (solid for event, dashed for person, dotted for art);
// it's computed in App.tsx alongside the box render, not here.
// =============================================================================

import type { Occurrence } from "../types/database";

export type Region =
  | "europe"
  | "americas"
  | "asia"
  | "africa"
  | "australasia"
  | "global";

export type OccurrenceColor = {
  region: Region;
  /** Base hue (degrees) including the per-occurrence intra-region offset. */
  hue: number;
  /** Semi-transparent fill for the box background. */
  fill: string;
  /** Fully-opaque outline colour. Same hue family as the fill — used for the
   *  box border so the outline matches the region. */
  border: string;
  /** Range-line colour (used for the period extent indicator). */
  line: string;
};

const REGION_BASE_HUE: Record<Exclude<Region, "global">, number> = {
  europe: 220,
  americas: 135,
  asia: 10,
  africa: 40,
  australasia: 280,
};

// Maximum hue deflection from the region's base hue (degrees).
// 25° gives a visible but still region-recognisable variation — across the
// 16 distinct buckets we land on, each "Europe" entry stays in the blue
// family but is differentiable from its neighbours.
const HUE_VARIATION = 25;

// Knuth multiplicative hash — same as the old palette code. Mixes the low
// bits of small sequential ids so neighbouring event ids land on different
// hue offsets.
const KNUTH = 2654435761;

function dominantRegion(occ: Pick<Occurrence,
  | "weight_europe"
  | "weight_americas"
  | "weight_asia"
  | "weight_australasia"
  | "weight_africa"
>): Region {
  const e = occ.weight_europe ?? 5;
  const a = occ.weight_americas ?? 5;
  const s = occ.weight_asia ?? 5;
  const u = occ.weight_australasia ?? 5;
  const f = occ.weight_africa ?? 5;
  // All equal → treat as global (no regional anchor). This covers entries
  // that omit region_weights entirely (defaulted to 5 across the board).
  if (e === a && a === s && s === u && u === f) return "global";
  // Otherwise pick the max. Ties go to Europe → Americas → Asia → Africa →
  // Australasia by virtue of left-to-right comparison.
  let best: Region = "europe";
  let bestVal = e;
  if (a > bestVal) { best = "americas"; bestVal = a; }
  if (s > bestVal) { best = "asia"; bestVal = s; }
  if (f > bestVal) { best = "africa"; bestVal = f; }
  if (u > bestVal) { best = "australasia"; bestVal = u; }
  return best;
}

export function colorFor(occ: Pick<Occurrence,
  | "id"
  | "weight_europe"
  | "weight_americas"
  | "weight_asia"
  | "weight_australasia"
  | "weight_africa"
  | "occurrence_type"
> & { resource_palette?: "teal" | "purple" }): OccurrenceColor {
  // Resource-type occurrences override the region scheme entirely — they
  // live in their own dedicated timelines and use a uniform palette:
  // teal for non-fiction (podcasts, history books, documentaries) and
  // purple for fiction (historical novels). The caller passes the palette
  // hint based on the timeline slug; default = teal.
  if (occ.occurrence_type === "resource") {
    const palette = occ.resource_palette ?? "teal";
    if (palette === "purple") {
      return {
        region: "global",
        hue: 280,
        fill: "hsl(280 55% 50% / 0.35)",
        border: "hsl(280 60% 42%)",
        line: "hsl(280 65% 55% / 0.8)",
      };
    }
    return {
      region: "global",
      hue: 180,
      fill: "hsl(180 55% 38% / 0.35)",
      border: "hsl(180 60% 30%)",
      line: "hsl(180 65% 40% / 0.8)",
    };
  }
  const region = dominantRegion(occ);

  // Per-occurrence hue offset in [-HUE_VARIATION, +HUE_VARIATION].
  // Coerce through Uint32 (ids can exceed 2^31 in v2).
  const mixed = ((occ.id >>> 0) * KNUTH) >>> 0;
  const t = (mixed % 1000) / 1000;          // 0..1
  const offset = (t - 0.5) * 2 * HUE_VARIATION;

  if (region === "global") {
    // Neutral grey — fill, border, line all have no hue (sat 0).
    return {
      region,
      hue: 0,
      fill: "hsl(0 0% 55% / 0.35)",
      border: "hsl(0 0% 45%)",
      line: "hsl(0 0% 60% / 0.7)",
    };
  }

  const baseHue = REGION_BASE_HUE[region];
  const hue = (baseHue + offset + 360) % 360;

  return {
    region,
    hue,
    // Semi-transparent fill: mid lightness + 35% alpha works on both light
    // and dark backgrounds. The slate-50 light bg darkens the fill enough
    // to read; the slate-900 dark bg keeps the same fill recognisable.
    fill: `hsl(${hue} 55% 50% / 0.35)`,
    // Border: same hue, fully opaque, slightly darker than the fill so the
    // outline reads cleanly against both the fill and the surrounding bg.
    // Used in place of the previous theme-driven black/white outline so the
    // box border matches its fill colour.
    border: `hsl(${hue} 60% 42%)`,
    // Period range line: same hue family, more opacity so the line stays
    // legible when crossing dim backgrounds.
    line: `hsl(${hue} 65% 55% / 0.8)`,
  };
}
