// Editor-only dashboard for the AI summary allowlist. Rendered as a full-screen
// overlay so it doesn't need any client-side routing.
//
// Users you add here can sign in and use the Summarise feature. Toggling
// `is_active` off keeps the row (and any notes) but blocks access — useful for
// "pause this friend's access" without losing the entry.
//
// All reads/writes are gated by the editor RLS policy on ai_summary_allowlist;
// this UI is also editor-gated at the call site.

import { useCallback, useEffect, useState } from "react";
import { supabase } from "../lib/supabase";
import { useAuth } from "../lib/auth";

interface AllowlistRow {
  email: string;
  is_active: boolean;
  added_at: string;
  added_by: string | null;
  notes: string | null;
}

export interface AiAccessAdminProps {
  onClose: () => void;
}

function isPlausibleEmail(s: string): boolean {
  const v = s.trim();
  return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v);
}

function fmtDate(iso: string): string {
  try { return new Date(iso).toLocaleDateString(); } catch { return iso; }
}

export function AiAccessAdmin({ onClose }: AiAccessAdminProps) {
  const { user } = useAuth();
  const [rows, setRows] = useState<AllowlistRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newEmail, setNewEmail] = useState("");
  const [newNotes, setNewNotes] = useState("");
  const [adding, setAdding] = useState(false);
  // Per-row inline notes edit state (kept tiny — only the row being edited).
  const [notesDraft, setNotesDraft] = useState<{ email: string; text: string } | null>(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    const { data, error: err } = await supabase
      .from("ai_summary_allowlist")
      .select("email, is_active, added_at, added_by, notes")
      .order("added_at", { ascending: false });
    if (err) {
      setError(err.message);
      setRows([]);
    } else {
      setRows((data ?? []) as AllowlistRow[]);
    }
    setLoading(false);
  }, []);

  useEffect(() => { void refresh(); }, [refresh]);

  // Close on Escape.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [onClose]);

  const handleAdd = async () => {
    const email = newEmail.trim().toLowerCase();
    if (!isPlausibleEmail(email)) {
      setError("That doesn't look like a valid email.");
      return;
    }
    setAdding(true);
    setError(null);
    const { error: err } = await supabase
      .from("ai_summary_allowlist")
      .upsert({
        email,
        is_active: true,
        added_by: user?.email ?? null,
        notes: newNotes.trim() || null,
      }, { onConflict: "email" });
    setAdding(false);
    if (err) { setError(err.message); return; }
    setNewEmail("");
    setNewNotes("");
    await refresh();
  };

  const handleToggle = async (email: string, next: boolean) => {
    setError(null);
    // Optimistic.
    setRows((prev) => prev.map((r) => (r.email === email ? { ...r, is_active: next } : r)));
    const { error: err } = await supabase
      .from("ai_summary_allowlist")
      .update({ is_active: next })
      .eq("email", email);
    if (err) { setError(err.message); await refresh(); }
  };

  const handleRemove = async (email: string) => {
    if (!confirm(`Remove ${email} from the AI summary allowlist?`)) return;
    setError(null);
    setRows((prev) => prev.filter((r) => r.email !== email));
    const { error: err } = await supabase
      .from("ai_summary_allowlist")
      .delete()
      .eq("email", email);
    if (err) { setError(err.message); await refresh(); }
  };

  const handleSaveNotes = async () => {
    if (!notesDraft) return;
    const { email, text } = notesDraft;
    setError(null);
    setRows((prev) => prev.map((r) => (r.email === email ? { ...r, notes: text || null } : r)));
    setNotesDraft(null);
    const { error: err } = await supabase
      .from("ai_summary_allowlist")
      .update({ notes: text.trim() || null })
      .eq("email", email);
    if (err) { setError(err.message); await refresh(); }
  };

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
              Manage AI summary access
            </h2>
            <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">
              People you add here can use the Summarise feature when signed in.
            </p>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close"
            className="text-2xl leading-none px-2 py-0.5 rounded hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-500"
          >
            ×
          </button>
        </header>

        <div className="px-4 py-3 border-b border-slate-200 dark:border-slate-700 flex-shrink-0">
          <div className="flex flex-col sm:flex-row gap-2">
            <input
              type="email"
              value={newEmail}
              onChange={(e) => setNewEmail(e.target.value)}
              placeholder="email@example.com"
              className="flex-1 px-2 py-1.5 text-sm rounded border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100"
            />
            <input
              type="text"
              value={newNotes}
              onChange={(e) => setNewNotes(e.target.value)}
              placeholder="Optional note (e.g. friend testing)"
              className="flex-1 px-2 py-1.5 text-sm rounded border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100"
            />
            <button
              type="button"
              onClick={() => void handleAdd()}
              disabled={adding || !newEmail.trim()}
              className="px-3 py-1.5 text-sm rounded bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50"
            >
              {adding ? "Adding…" : "Add"}
            </button>
          </div>
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
          ) : rows.length === 0 ? (
            <div className="px-4 py-6 text-sm text-slate-500 dark:text-slate-400">
              Nobody on the allowlist yet. Add an email above to grant access.
            </div>
          ) : (
            <ul className="divide-y divide-slate-200 dark:divide-slate-800">
              {rows.map((row) => (
                <li key={row.email} className="px-4 py-3 flex items-start gap-3 text-sm">
                  <label className="flex items-center pt-1 cursor-pointer" title={row.is_active ? "Active — block access" : "Inactive — grant access"}>
                    <input
                      type="checkbox"
                      checked={row.is_active}
                      onChange={(e) => void handleToggle(row.email, e.target.checked)}
                      className="accent-blue-600 w-4 h-4"
                    />
                  </label>

                  <div className="flex-1 min-w-0">
                    <div className="flex items-baseline gap-2 flex-wrap">
                      <span className={`font-medium truncate ${row.is_active ? "text-slate-900 dark:text-slate-100" : "text-slate-400 dark:text-slate-500 line-through"}`}>
                        {row.email}
                      </span>
                      <span className="text-[11px] text-slate-400">
                        added {fmtDate(row.added_at)}
                        {row.added_by ? ` by ${row.added_by}` : ""}
                      </span>
                    </div>
                    {notesDraft?.email === row.email ? (
                      <div className="mt-1 flex gap-2">
                        <input
                          type="text"
                          value={notesDraft.text}
                          onChange={(e) => setNotesDraft({ email: row.email, text: e.target.value })}
                          autoFocus
                          onKeyDown={(e) => {
                            if (e.key === "Enter") void handleSaveNotes();
                            if (e.key === "Escape") setNotesDraft(null);
                          }}
                          className="flex-1 px-2 py-1 text-xs rounded border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800"
                        />
                        <button onClick={() => void handleSaveNotes()} className="text-xs px-2 py-1 rounded bg-blue-600 text-white hover:bg-blue-700">Save</button>
                        <button onClick={() => setNotesDraft(null)} className="text-xs px-2 py-1 rounded border border-slate-300 dark:border-slate-600">Cancel</button>
                      </div>
                    ) : (
                      <button
                        type="button"
                        onClick={() => setNotesDraft({ email: row.email, text: row.notes ?? "" })}
                        className="mt-0.5 text-[12px] text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-blue-400 text-left"
                      >
                        {row.notes ? row.notes : <em className="opacity-60">add note…</em>}
                      </button>
                    )}
                  </div>

                  <button
                    type="button"
                    onClick={() => void handleRemove(row.email)}
                    title="Remove"
                    className="text-slate-400 hover:text-red-600 dark:hover:text-red-400 text-lg leading-none px-2"
                  >
                    ×
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}
