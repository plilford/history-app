// Lets a signed-in user report an issue / suggest an improvement for a single
// occurrence. Shows a read-only summary of the occurrence (title, date,
// description, related resources), an aspect picker, and an optional note
// (required only when "Other" is chosen). Inserts a row into issue_flags; the
// editor reviews them via IssueFlagsAdmin.
//
// Rendered as a centered modal overlay (z-[60], above the EventPopup's z-50).

import { useEffect, useState } from "react";
import { supabase } from "../lib/supabase";
import { useAuth } from "../lib/auth";
import type { EventWithPriority } from "../types/database";

type Aspect = "title" | "description" | "date" | "resources" | "priority" | "other";

const ASPECTS: Array<{ value: Aspect; label: string }> = [
  { value: "title", label: "Title" },
  { value: "description", label: "Description" },
  { value: "date", label: "Date" },
  { value: "resources", label: "Listed resources" },
  { value: "priority", label: "Priority level" },
  { value: "other", label: "Other" },
];

export interface FlagIssueModalProps {
  event: EventWithPriority;
  /** Ids of the occurrences tied to this one as resources — podcasts/books
   *  about a normal occurrence, or the subjects a resource tags. Titles are
   *  fetched here (reads on occurrences are public). */
  relatedResourceIds: number[];
  onClose: () => void;
  onSubmitted?: () => void;
}

export function FlagIssueModal({ event, relatedResourceIds, onClose, onSubmitted }: FlagIssueModalProps) {
  const { user } = useAuth();
  const [aspect, setAspect] = useState<Aspect>("title");
  const [note, setNote] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [done, setDone] = useState(false);
  const [relatedResources, setRelatedResources] = useState<Array<{ id: number; title: string }>>([]);

  // Stable key so the fetch doesn't re-run on every parent re-render (the array
  // prop is recreated each render).
  const idsKey = relatedResourceIds.slice().sort((a, b) => a - b).join(",");
  useEffect(() => {
    const ids = idsKey ? idsKey.split(",").map(Number) : [];
    if (ids.length === 0) { setRelatedResources([]); return; }
    let cancelled = false;
    (async () => {
      const { data } = await supabase
        .from("occurrences")
        .select("id, title")
        .in("id", ids);
      if (cancelled) return;
      const rows = (data ?? []) as Array<{ id: number; title: string }>;
      setRelatedResources(rows.sort((a, b) => a.title.localeCompare(b.title)));
    })();
    return () => { cancelled = true; };
  }, [idsKey]);

  // Close on Escape.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [onClose]);

  const dateLabel =
    (event.display_date ?? event.start_year ?? "") +
    (event.date_uncertain && !String(event.display_date ?? "").endsWith("*") ? "*" : "");

  const noteRequired = aspect === "other";
  const canSubmit = !!user && !submitting && (!noteRequired || note.trim().length > 0);

  const handleSubmit = async () => {
    if (!user?.email) { setError("You must be signed in to flag an issue."); return; }
    if (noteRequired && note.trim().length === 0) return;
    setSubmitting(true);
    setError(null);
    const { error: err } = await supabase.from("issue_flags").insert({
      occurrence_id: event.id,
      occurrence_title: event.title,
      reporter_email: user.email,
      aspect,
      note: note.trim() || null,
    });
    setSubmitting(false);
    if (err) { setError(err.message); return; }
    setDone(true);
    onSubmitted?.();
  };

  return (
    <div
      className="fixed inset-0 z-[60] bg-black/50 flex items-start justify-center p-4 overflow-y-auto"
      onClick={onClose}
    >
      <div
        className="w-full max-w-md mt-8 mb-8 bg-white dark:bg-slate-900 rounded-lg shadow-xl border border-slate-200 dark:border-slate-700 flex flex-col"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-label="Flag an issue"
      >
        <header className="flex items-center justify-between px-4 py-3 border-b border-slate-200 dark:border-slate-700 flex-shrink-0">
          <h2 className="text-base font-semibold text-slate-900 dark:text-slate-100">
            Flag an issue or suggest a change
          </h2>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close"
            className="text-2xl leading-none px-2 py-0.5 rounded hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-500"
          >
            ×
          </button>
        </header>

        {done ? (
          <div className="px-4 py-6 text-sm text-slate-700 dark:text-slate-300 space-y-3">
            <p>Thanks — your report has been recorded.</p>
            <button
              type="button"
              onClick={onClose}
              className="px-3 py-1.5 text-sm rounded bg-blue-600 text-white hover:bg-blue-700"
            >
              Done
            </button>
          </div>
        ) : (
          <div className="px-4 py-3 space-y-4">
            {/* Read-only summary of the occurrence. */}
            <div className="rounded border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50 px-3 py-2 space-y-1">
              <div className="flex items-baseline justify-between gap-2">
                <span className="text-sm font-semibold text-slate-900 dark:text-slate-100">{event.title}</span>
                <span className="text-[11px] text-slate-400 shrink-0">{dateLabel}</span>
              </div>
              {event.description && (
                <p className="text-xs text-slate-600 dark:text-slate-400 leading-snug">{event.description}</p>
              )}
              {relatedResources.length > 0 && (
                <div className="pt-1">
                  <div className="text-[10px] uppercase tracking-wide text-slate-500 mb-0.5">Listed resources</div>
                  <ul className="text-xs text-slate-600 dark:text-slate-400 list-disc list-inside">
                    {relatedResources.map((r) => (
                      <li key={r.id} className="truncate">{r.title}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* Aspect picker. */}
            <fieldset className="space-y-1.5">
              <legend className="text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                What does this relate to?
              </legend>
              {ASPECTS.map((a) => {
                const disabled = a.value === "resources" && relatedResources.length === 0;
                return (
                  <label
                    key={a.value}
                    className={`flex items-center gap-2 text-sm ${disabled ? "opacity-40 cursor-not-allowed" : "cursor-pointer"}`}
                  >
                    <input
                      type="radio"
                      name="aspect"
                      value={a.value}
                      checked={aspect === a.value}
                      disabled={disabled}
                      onChange={() => setAspect(a.value)}
                      className="accent-blue-600"
                    />
                    <span className="text-slate-800 dark:text-slate-200">{a.label}</span>
                  </label>
                );
              })}
            </fieldset>

            {/* Note. */}
            <div className="space-y-1">
              <label htmlFor="flag-note" className="text-xs font-medium text-slate-700 dark:text-slate-300">
                What's the issue / what should change?
                {noteRequired ? <span className="text-red-500"> (required)</span> : <span className="text-slate-400"> (optional)</span>}
              </label>
              <textarea
                id="flag-note"
                value={note}
                onChange={(e) => setNote(e.target.value)}
                rows={3}
                placeholder={noteRequired ? "Please describe the issue" : "Add detail (optional)"}
                className="w-full px-2 py-1.5 text-sm rounded border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 resize-y"
              />
            </div>

            {error && (
              <div className="text-xs text-red-600 dark:text-red-400">{error}</div>
            )}

            <div className="flex justify-end gap-2 pt-1">
              <button
                type="button"
                onClick={onClose}
                className="px-3 py-1.5 text-sm rounded border border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={() => void handleSubmit()}
                disabled={!canSubmit}
                className="px-3 py-1.5 text-sm rounded bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50"
              >
                {submitting ? "Submitting…" : "Submit"}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
