// useAiSummaryAccess — does the current signed-in user have access to the AI
// summary feature?
//
//   - The editor (EDITOR_EMAIL) is always allowed (hardcoded fallback so the
//     allowlist dashboard can never lock the owner out).
//   - Everyone else must have an active row in ai_summary_allowlist.
//
// The allowlist's RLS policy lets each user read their own row only, so this
// query is safe — it doesn't leak the rest of the list.

import { useEffect, useState } from "react";
import { useAuth } from "./auth";
import { supabase } from "./supabase";

// Must match worker/summary.ts DEFAULT_EDITOR_EMAIL and src/App.tsx EDITOR_EMAIL.
// Kept here too so the hook is self-contained.
const EDITOR_EMAIL = "p.lilford@gmail.com";

export interface AiAccess {
  /** Definitive answer: may the current user click Summarise? */
  canSummarise: boolean;
  /** True while we're still asking Supabase. UI should hide the controls
   *  during this brief moment rather than flashing then hiding. */
  loading: boolean;
}

export function useAiSummaryAccess(): AiAccess {
  const { user, loading: authLoading } = useAuth();
  const [state, setState] = useState<AiAccess>({ canSummarise: false, loading: true });

  useEffect(() => {
    // Still resolving the session — don't decide yet.
    if (authLoading) {
      setState({ canSummarise: false, loading: true });
      return;
    }
    // Signed out.
    if (!user) {
      setState({ canSummarise: false, loading: false });
      return;
    }
    const email = (user.email ?? "").toLowerCase();
    // Editor: instant allow, no DB round-trip.
    if (email === EDITOR_EMAIL.toLowerCase()) {
      setState({ canSummarise: true, loading: false });
      return;
    }
    // Everyone else: check the allowlist for their own row.
    let cancelled = false;
    (async () => {
      const { data, error } = await supabase
        .from("ai_summary_allowlist")
        .select("is_active")
        .ilike("email", email)
        .maybeSingle();
      if (cancelled) return;
      if (error) {
        // Safest on failure: deny access. The Worker enforces too.
        setState({ canSummarise: false, loading: false });
        return;
      }
      setState({ canSummarise: !!data?.is_active, loading: false });
    })();
    return () => { cancelled = true; };
  }, [user, authLoading]);

  return state;
}
