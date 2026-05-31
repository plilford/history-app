// Editor-only dashboard for reviewing user-submitted reports. Rendered as a
// full-screen overlay so it doesn't need any client-side routing.
//
// Two tabs:
//   - "Occurrence flags" — issues filed against a single occurrence from its
//     popup (FlagIssueModal → issue_flags).
//   - "App feedback" — general app feedback (bugs/ideas/copy) sent from the
//     settings panel (FeedbackModal → app_feedback).
//
// In both the editor can read, mark resolved (kept for history), reopen, or
// delete. All reads/writes are gated by the editor RLS policy on the tables;
// this UI is also editor-gated at the call site.

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

interface FeedbackRow {
  id: number;
  reporter_email: string;
  category: string | null;
  message: string;
  status: string;
  user_agent: string | null;
  app_path: string | null;
  created_at: string;
  resolved_at: string | null;
}

type Tab = "flags" | "feedback";

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

const CATEGORY_LABELS: Record<string, string> = {
  bug: "Bug",
  idea: "Idea / feature",
  copy: "Copy / wording",
  other: "Other",
};

export function IssueFlagsAdmin({ onClose }: IssueFlagsAdminProps) {
  const [tab, setTab] = useState<Tab>("flags");
  const [rows, setRows] = useState<FlagRow[]>([]);
  const [feedback, setFeedback] = useState<FeedbackRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<"open" | "all">("open");

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    const [flagsRes, feedbackRes] = await Promise.all([
      supabase.from("issue_flags").select("*").order("created_at", { ascending: false }),
      supabase.from("app_feedback").select("*").order("created_at", { ascending: false }),
    ]);
    if (flagsRes.error) { setError(flagsRes.error.message); setRows([]); }
    else setRows((flagsRes.data ?? []) as FlagRow[]);
    if (feedbackRes.error) { setError((prev) => prev ?? feedbackRes.error!.message); setFeedback([]); }
    else setFeedback((feedbackRes.data ?? []) as FeedbackRow[]);
    setLoading(false);
  }, []);

  useEffect(() => { void refresh(); }, [refresh]);

  // Close on Escape.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [onClose]);

  const table = tab === "flags" ? "issue_flags" : "app_feedback";

  const handleResolve = async (id: number, resolve: boolean) => {
    setError(null);
    const patch = resolve
      ? { status: "resolved", resolved_at: new Date().toISOString() }
      : { status: "open", resolved_at: null };
    if (tab === "flags") setRows((prev) => prev.map((r) => (r.id === id ? { ...r, ...patch } : r)));
    else setFeedback((prev) => prev.map((r) => (r.id === id ? { ...r, ...patch } : r)));
    const { error: err } = await supabase.from(table).update(patch).eq("id", id);
    if (err) { setError(err.message); await refresh(); }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Delete this permanently?")) return;
    setError(null);
    if (tab === "flags") setRows((prev) => prev.filter((r) => r.id !== id));
    else setFeedback((prev) => prev.filter((r) => r.id !== id));
    const { error: err } = await supabase.from(table).delete().eq("id", id);
    if (err) { setError(err.message); await refresh(); }
  };

  const visibleFlags = filter === "open" ? rows.filter((r) => r.status === "open") : rows;
  const visibleFeedback = filter === "open" ? feedback.filter((r) => r.status === "open") : feedback;
  const openFlags = rows.filter((r) => r.status === "open").length;
  const openFeedback = feedback.filter((r) => r.status === "open").length;

  const activeOpen = tab === "flags" ? openFlags : openFeedback;
  const activeTotal = tab === "flags" ? rows.length : feedback.length;

  const tabClass = (active: boolean) =>
    `px-3 py-1.5 text-xs font-medium border-b-2 -mb-px ${
      active
        ? "border-blue-600 text-blue-600 dark:text-blue-400"
        : "border-transparent text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200"
    }`;

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
              Review feedback
            </h2>
            <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">
              {activeOpen} open · {activeTotal} total
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

        {/* Tabs. */}
        <div className="flex items-center gap-1 px-4 border-b border-slate-200 dark:border-slate-700 flex-shrink-0">
          <button type="button" className={tabClass(tab === "flags")} onClick={() => setTab("flags")}>
            Occurrence flags{openFlags > 0 ? ` (${openFlags})` : ""}
          </button>
          <button type="button" className={tabClass(tab === "feedback")} onClick={() => setTab("feedback")}>
            App feedback{openFeedback > 0 ? ` (${openFeedback})` : ""}
          </button>
        </div>

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
          ) : tab === "flags" ? (
            visibleFlags.length === 0 ? (
              <div className="px-4 py-6 text-sm text-slate-500 dark:text-slate-400">
                {filter === "open" ? "No open flags. 🎉" : "No flags yet."}
              </div>
            ) : (
              <ul className="divide-y divide-slate-200 dark:divide-slate-800">
                {visibleFlags.map((row) => (
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
            )
          ) : visibleFeedback.length === 0 ? (
            <div className="px-4 py-6 text-sm text-slate-500 dark:text-slate-400">
              {filter === "open" ? "No open feedback. 🎉" : "No feedback yet."}
            </div>
          ) : (
            <ul className="divide-y divide-slate-200 dark:divide-slate-800">
              {visibleFeedback.map((row) => (
                <li key={row.id} className="px-4 py-3 flex items-start gap-3 text-sm">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-baseline gap-2 flex-wrap">
                      {row.category && (
                        <span className="text-[10px] px-1.5 py-0.5 rounded border border-slate-300 dark:border-slate-600 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300">
                          {CATEGORY_LABELS[row.category] ?? row.category}
                        </span>
                      )}
                      {row.status === "resolved" && (
                        <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-100 dark:bg-emerald-900/50 text-emerald-700 dark:text-emerald-300">
                          resolved
                        </span>
                      )}
                    </div>
                    <p className={`mt-1 text-xs whitespace-pre-wrap ${row.status === "resolved" ? "text-slate-400 dark:text-slate-500" : "text-slate-700 dark:text-slate-300"}`}>
                      {row.message}
                    </p>
                    <div className="mt-1 text-[11px] text-slate-400">
                      {row.reporter_email} · {fmtDate(row.created_at)}
                      {row.app_path ? ` · ${row.app_path}` : ""}
                    </div>
                    {row.user_agent && (
                      <div className="mt-0.5 text-[10px] text-slate-300 dark:text-slate-600 truncate" title={row.user_agent}>
                        {row.user_agent}
                      </div>
                    )}
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
