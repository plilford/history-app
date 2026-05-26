import { useEffect, useState } from "react";
import { useAuth } from "../lib/auth";
import { supabase } from "../lib/supabase";

/** Email allowlist mirroring `editor_emails()` in
 *  `supabase/migrations/001_init_schema.sql`. Only these accounts can write
 *  to the DB, so only they care about the freshness reminder. If you add new
 *  editors to the DB function, mirror them here too. */
const EDITOR_EMAILS = new Set<string>([
  "p.lilford@gmail.com",
]);

const AMBER_AT_DAYS = 30;
const RED_AT_DAYS = 60;

/**
 * Tiny header chip that shows how many days ago the most recent occurrence
 * row was written. Visible only to signed-in editors — non-editors see
 * nothing.
 *
 * Click: opens a tooltip with the exact timestamp + a reminder to run the
 * `/monthly-update` skill in Claude Code.
 */
export function DataFreshnessChip() {
  const { user } = useAuth();
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);
  const [loading, setLoading] = useState(true);
  const [tipOpen, setTipOpen] = useState(false);

  const isEditor = !!user?.email && EDITOR_EMAILS.has(user.email);

  useEffect(() => {
    if (!isEditor) return;
    let cancelled = false;
    (async () => {
      const { data, error } = await supabase
        .from("occurrences")
        .select("updated_at")
        .order("updated_at", { ascending: false })
        .limit(1);
      if (cancelled) return;
      if (error || !data || data.length === 0) {
        setLoading(false);
        return;
      }
      const ts = (data[0] as { updated_at?: string }).updated_at;
      if (ts) setLastUpdate(new Date(ts));
      setLoading(false);
    })();
    return () => { cancelled = true; };
  }, [isEditor]);

  if (!isEditor) return null;
  if (loading) return null;
  if (!lastUpdate) return null;

  const days = Math.floor(
    (Date.now() - lastUpdate.getTime()) / (1000 * 60 * 60 * 24),
  );
  const colorClass =
    days >= RED_AT_DAYS
      ? "border-rose-400 text-rose-700 dark:border-rose-500 dark:text-rose-300"
      : days >= AMBER_AT_DAYS
        ? "border-amber-400 text-amber-700 dark:border-amber-500 dark:text-amber-300"
        : "border-slate-300 text-slate-600 dark:border-slate-600 dark:text-slate-400";

  return (
    <div className="relative">
      <button
        type="button"
        onClick={() => setTipOpen((v) => !v)}
        onBlur={() => setTipOpen(false)}
        title={`DB updated ${lastUpdate.toLocaleDateString()} (click for details)`}
        className={`text-[10px] px-1.5 py-0.5 rounded border tabular-nums ${colorClass} bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800`}
      >
        DB {days}d
      </button>
      {tipOpen && (
        <div
          className="absolute right-0 mt-1 z-50 w-72 rounded border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-200 text-xs shadow-lg p-2"
          onMouseDown={(e) => e.preventDefault()}
        >
          <div className="font-medium">Data freshness</div>
          <div className="mt-1">
            Most recent write:{" "}
            <span className="tabular-nums">
              {lastUpdate.toLocaleString()}
            </span>
            {" "}
            (<span className="tabular-nums">{days}d</span> ago)
          </div>
          {days >= AMBER_AT_DAYS && (
            <div className="mt-2 text-slate-600 dark:text-slate-400">
              Time for a refresh. From your terminal, run{" "}
              <code className="font-mono text-[11px]">/monthly-update</code>{" "}
              inside Claude Code in the project directory — the skill walks
              through new podcast episodes, ongoing-entry closures, and any
              recent additions worth making.
            </div>
          )}
        </div>
      )}
    </div>
  );
}
