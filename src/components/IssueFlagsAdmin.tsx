// Editor-only dashboard for reviewing user-reported issue flags. Rendered as a
// full-screen overlay so it doesn't need any client-side routing.
//
// Users file flags from an occurrence popup (FlagIssueModal). Here the editor
// can read them, mark them resolved (kept for history), reopen, or delete.
//
// All reads/writes are gated by the editor RLS policy on issue_flags; this UI
// is also editor-gated at the call site.

import { useCallback, useEffect, useState } from "react";
import { supabase } from "../lib/supabase";

interface FlagRow {
  id: number;
  occurrence_id: number;
  occurrence_title: string;
  reporter_email: string;
  aspect: string;
  note: string | null;
  status: string;
  created_at: string;
  resolved_at: string | null;
}

export interface IssueFlagsAdminProps {
  onClose: () => void;
}

function fmtDate(iso: string): string {
  try { return new Date(iso).toLocaleString(); } catch { return iso; }
}

const ASPECT_LABELS: Record<string, string> = {
  title: "Title",
  description: "Description",
  date: "Date",
  resources: "Listed resources",
  priority: "Priority level",
  other: "Other",
};

export function IssueFlagsAdmin({ onClose }: IssueFlagsAdminProps) {
  const [rows, setRows] = useState<FlagRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<"open" | "all">("open");

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    const { data, error: err } = await supabase
      .from("issue_flags")
      .select("*")
      .order("created_at", { ascending: false });
    if (err) { setError(err.message); setRows([]); setLoading(false); return; }
    setRows((data ?? []) as FlagRow[]);
    setLoading(false);
  }, []);

  useEffect(() => { void refresh(); }, [refresh]);

  // Close on Escape.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [onClose]);

  const handleResolve = async (id: number, resolve: boolean) => {
    setError(null);
    const patch = resolve
      ? { status: "resolved", resolved_at: new Date().toISOString() }
      : { status: "open", resolved_at: null };
    setRows((prev) => prev.map((r) => (r.id === id ? { ...r, ...patch } : r)));
    const { error: err } = await supabase.from("issue_flags").update(patch).eq("id", id);
    if (err) { setError(err.message); await refresh(); }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Delete this flag permanently?")) return;
    setError(null);
    setRows((prev) => prev.filter((r) => r.id !== id));
    const { error: err } = await supabase.from("issue_flags").delete().eq("id", id);
    if (err) { setError(err.message); await refresh(); }
  };

  const visible = filter === "open" ? rows.filter((r) => r.status === "open") : rows;
  const openCount = rows.filter((r) => r.status === "open").length;

  return (
    <div
      className="fixed inset-0 z-50 bg-black/50 flex items-start justify-center p-4 overflow-y-auto"
      onClick={onClose}
    >
      <div
        className="w-full max-w-2xl mt-8 mb-8 bg-white dark:bg-slate-900 rounded-lg shadow-xl border border-slate-200 dark:border-slate-700 flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        <header className="flex items-center justify-between px-4 py-3 border-b border-slate-200 dark:border-slate-700 flex-shrink-0">
          <div>
            <h2 className="text-base font-semibold text-slate-900 dark:text-slate-100">
              Review flagged issues
            </h2>
            <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">
              {openCount} open · {rows.length} total
            </p>
          </div>
          <div className="flex items-center gap-2">
            <div className="flex rounded border border-slate-300 dark:border-slate-600 overflow-hidden text-xs">
              <button
                type="button"
                onClick={() => setFilter("open")}
                className={filter === "open" ? "px-2 py-1 bg-blue-600 text-white" : "px-2 py-1 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800"}
              >
                Open
              </button>
              <button
                type="button"
                onClick={() => setFilter("all")}
                className={filter === "all" ? "px-2 py-1 bg-blue-600 text-white" : "px-2 py-1 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800"}
              >
                All
              </button>
            </div>
            <button
              type="button"
              onClick={onClose}
              aria-label="Close"
              className="text-2xl leading-none px-2 py-0.5 rounded hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-500"
            >
              ×
            </button>
          </div>
        </header>

        {error && (
          <div className="px-4 py-2 text-xs text-red-600 dark:text-red-400 border-b border-slate-200 dark:border-slate-700">
            {error}
          </div>
        )}

        <div className="flex-1 overflow-y-auto">
          {loading ? (
            <div className="px-4 py-6 text-sm text-slate-500 dark:text-slate-400 animate-pulse">
              Loading…
            </div>
          ) : visible.length === 0 ? (
            <div className="px-4 py-6 text-sm text-slate-500 dark:text-slate-400">
              {filter === "open" ? "No open flags. 🎉" : "No flags yet."}
            </div>
          ) : (
            <ul className="divide-y divide-slate-200 dark:divide-slate-800">
              {visible.map((row) => (
                <li key={row.id} className="px-4 py-3 flex items-start gap-3 text-sm">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-baseline gap-2 flex-wrap">
                      <span className={`font-medium ${row.status === "resolved" ? "text-slate-400 dark:text-slate-500 line-through" : "text-slate-900 dark:text-slate-100"}`}>
                        {row.occurrence_title}
                      </span>
                      <span className="text-[10px] px-1.5 py-0.5 rounded border border-slate-300 dark:border-slate-600 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300">
                        {ASPECT_LABELS[row.aspect] ?? row.aspect}
                      </span>
                      {row.status === "resolved" && (
                        <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-100 dark:bg-emerald-900/50 text-emerald-700 dark:text-emerald-300">
                          resolved
                        </span>
                      )}
                    </div>
                    {row.note && (
                      <p className="mt-1 text-xs text-slate-700 dark:text-slate-300 whitespace-pre-wrap">{row.note}</p>
                    )}
                    <div className="mt-1 text-[11px] text-slate-400">
                      {row.reporter_email} · {fmtDate(row.created_at)} · #{row.occurrence_id}
                    </div>
                  </div>

                  <div className="flex flex-col items-end gap-1 shrink-0">
                    {row.status === "open" ? (
                      <button
                        type="button"
                        onClick={() => void handleResolve(row.id, true)}
                        className="text-xs px-2 py-1 rounded bg-emerald-600 text-white hover:bg-emerald-700"
                      >
                        Resolve
                      </button>
                    ) : (
                      <button
                        type="button"
                        onClick={() => void handleResolve(row.id, false)}
                        className="text-xs px-2 py-1 rounded border border-slate-300 dark:border-slate-600 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800"
                      >
                        Reopen
                      </button>
                    )}
                    <button
                      type="button"
                      onClick={() => void handleDelete(row.id)}
                      className="text-xs px-2 py-1 rounded text-slate-400 hover:text-red-600 dark:hover:text-red-400"
                    >
                      Delete
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}
