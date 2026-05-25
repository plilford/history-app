import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { supabase } from "./supabase";
import { useAuth } from "./auth";

interface FavouritesContextValue {
  /** Set of occurrence IDs the current user has favourited. Empty when
   *  signed out. */
  ids: Set<number>;
  isFavourite: (occurrenceId: number) => boolean;
  /** Toggle the favourite state. Returns the new state (true = now favourited,
   *  false = now un-favourited). Optimistic — updates `ids` immediately and
   *  reverts on DB error. No-ops when signed out. */
  toggle: (occurrenceId: number) => Promise<boolean>;
}

const FavouritesContext = createContext<FavouritesContextValue | null>(null);

export function FavouritesProvider({ children }: { children: ReactNode }) {
  const { user } = useAuth();
  const [ids, setIds] = useState<Set<number>>(() => new Set());

  // Load the user's full favourites list once on sign-in. Subsequent changes
  // go through `toggle()` which keeps `ids` in sync optimistically.
  useEffect(() => {
    if (!user) {
      setIds(new Set());
      return;
    }
    let cancelled = false;
    (async () => {
      const { data, error } = await supabase
        .from("user_favourites")
        .select("occurrence_id")
        .eq("user_id", user.id);
      if (cancelled) return;
      if (error) {
        console.error("favourites load failed", error);
        setIds(new Set());
        return;
      }
      setIds(new Set((data ?? []).map((r) => r.occurrence_id as number)));
    })();
    return () => {
      cancelled = true;
    };
  }, [user]);

  const isFavourite = useCallback(
    (occurrenceId: number) => ids.has(occurrenceId),
    [ids],
  );

  const toggle = useCallback(
    async (occurrenceId: number): Promise<boolean> => {
      if (!user) return false;
      const currentlyFav = ids.has(occurrenceId);
      // Optimistic update.
      setIds((prev) => {
        const next = new Set(prev);
        if (currentlyFav) next.delete(occurrenceId);
        else next.add(occurrenceId);
        return next;
      });
      if (currentlyFav) {
        const { error } = await supabase
          .from("user_favourites")
          .delete()
          .eq("user_id", user.id)
          .eq("occurrence_id", occurrenceId);
        if (error) {
          console.error("favourite remove failed", error);
          // Revert.
          setIds((prev) => {
            const next = new Set(prev);
            next.add(occurrenceId);
            return next;
          });
          return true;
        }
        return false;
      } else {
        const { error } = await supabase
          .from("user_favourites")
          .insert({ user_id: user.id, occurrence_id: occurrenceId });
        if (error) {
          console.error("favourite add failed", error);
          setIds((prev) => {
            const next = new Set(prev);
            next.delete(occurrenceId);
            return next;
          });
          return false;
        }
        return true;
      }
    },
    [user, ids],
  );

  const value = useMemo<FavouritesContextValue>(
    () => ({ ids, isFavourite, toggle }),
    [ids, isFavourite, toggle],
  );

  return (
    <FavouritesContext.Provider value={value}>
      {children}
    </FavouritesContext.Provider>
  );
}

export function useFavourites(): FavouritesContextValue {
  const ctx = useContext(FavouritesContext);
  if (!ctx) throw new Error("useFavourites must be used inside <FavouritesProvider>");
  return ctx;
}
