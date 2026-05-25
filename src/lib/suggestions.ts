import { supabase } from "./supabase";
import type { Occurrence } from "../types/database";

export interface Suggestion {
  occurrence: Occurrence;
  reason: string;
}

// Reason precedence — used when an occurrence is reachable via multiple paths
// (e.g. both a sibling under the same umbrella AND in the top slug list).
// Lower number wins. Same numbers fall through to main_priority desc.
const REASON_RANK: Record<string, number> = {
  "Same umbrella": 1,
  "Parent umbrella": 2,
  "Inside this": 3,
};

/**
 * Find ~10 occurrences related to the given seed that the user hasn't
 * favourited yet. "Related" = sharing an umbrella, OR top-ranked on the
 * seed's primary (non-master) timeline slug.
 *
 * Called immediately after a user favourites an occurrence; results are
 * shown in the SuggestionsPopup so they can quickly fav several at once.
 */
export async function fetchSuggestions(
  seedId: number,
  userId: string | null,
  limit = 10,
): Promise<Suggestion[]> {
  const { data: seedRow, error: seedErr } = await supabase
    .from("occurrences")
    .select("*")
    .eq("id", seedId)
    .single();
  if (seedErr || !seedRow) return [];
  const seed = seedRow as Occurrence;

  // Build the exclusion set: seed + everything the user has already favourited.
  const excluded = new Set<number>([seedId]);
  if (userId) {
    const { data: favRows } = await supabase
      .from("user_favourites")
      .select("occurrence_id")
      .eq("user_id", userId);
    for (const r of favRows ?? []) excluded.add((r as any).occurrence_id);
  }

  // Per-candidate best (lowest-rank) reason. Wins ties go to higher
  // main_priority at the end of the function.
  const suggestions = new Map<number, Suggestion>();
  const consider = (occ: Occurrence, reason: string) => {
    if (excluded.has(occ.id)) return;
    const existing = suggestions.get(occ.id);
    if (!existing) {
      suggestions.set(occ.id, { occurrence: occ, reason });
      return;
    }
    const existingRank = REASON_RANK[existing.reason] ?? 99;
    const newRank = REASON_RANK[reason] ?? 99;
    if (newRank < existingRank) {
      suggestions.set(occ.id, { occurrence: occ, reason });
    }
  };

  // 1. Sibling occurrences sharing the seed's first_zoom_out umbrella.
  if (seed.first_zoom_out_id != null) {
    const { data } = await supabase
      .from("occurrences")
      .select("*")
      .eq("first_zoom_out_id", seed.first_zoom_out_id)
      .neq("id", seedId)
      .order("main_priority", { ascending: false, nullsFirst: false })
      .limit(30);
    for (const o of (data ?? []) as Occurrence[]) {
      consider(o, "Same umbrella");
    }
  }

  // 2. The seed's umbrella(s) themselves — useful when the user just
  //    favourited a leaf event and might want the bigger period too.
  const umbrellaIds = [seed.first_zoom_out_id, seed.second_zoom_out_id]
    .filter((x): x is number => x != null);
  if (umbrellaIds.length > 0) {
    const { data } = await supabase
      .from("occurrences")
      .select("*")
      .in("id", umbrellaIds);
    for (const o of (data ?? []) as Occurrence[]) {
      consider(o, "Parent umbrella");
    }
  }

  // 3. Children of the seed — if seed is itself an umbrella, the user
  //    might want to drill into specific events inside it.
  {
    const { data } = await supabase
      .from("occurrences")
      .select("*")
      .or(`first_zoom_out_id.eq.${seedId},second_zoom_out_id.eq.${seedId}`)
      .neq("id", seedId)
      .order("main_priority", { ascending: false, nullsFirst: false })
      .limit(30);
    for (const o of (data ?? []) as Occurrence[]) {
      consider(o, "Inside this");
    }
  }

  // 4. Top-ranked entries on the seed's primary non-master slug. This is the
  //    slug-based fallback: e.g. favouriting a Tudor monarch surfaces other
  //    high-priority Tudor entries even if they're not in the same umbrella.
  {
    const { data: topPrio } = await supabase
      .from("occurrence_timeline_priorities")
      .select("priority, timelines!inner(id, name, slug)")
      .eq("occurrence_id", seedId)
      .neq("timelines.slug", "master")
      .order("priority", { ascending: false })
      .limit(1);
    const top = (topPrio ?? [])[0] as any;
    if (top?.timelines?.id) {
      const tlName = top.timelines.name as string;
      const { data: slugTop } = await supabase
        .from("occurrence_timeline_priorities")
        .select("priority, occurrences!inner(*)")
        .eq("timeline_id", top.timelines.id)
        .neq("occurrence_id", seedId)
        .order("priority", { ascending: false })
        .limit(30);
      for (const r of (slugTop ?? []) as any[]) {
        const o = r.occurrences as Occurrence;
        consider(o, `Top of ${tlName}`);
      }
    }
  }

  return [...suggestions.values()]
    .sort((a, b) => {
      const ra = REASON_RANK[a.reason] ?? 99;
      const rb = REASON_RANK[b.reason] ?? 99;
      if (ra !== rb) return ra - rb;
      return (b.occurrence.main_priority ?? 0) - (a.occurrence.main_priority ?? 0);
    })
    .slice(0, limit);
}
