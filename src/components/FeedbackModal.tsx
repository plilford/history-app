// Lets a signed-in user send general feedback about the app itself — bugs,
// ideas, copy tweaks, anything not tied to a single occurrence (those use
// FlagIssueModal). Inserts a row into app_feedback; the editor reviews them in
// the "App feedback" tab of IssueFlagsAdmin.
//
// Rendered as a centered modal overlay (z-[60]). If the user isn't signed in
// we show a sign-in prompt instead of the form (RLS requires a matching email).

import { useEffect, useState } from "react";
import { supabase } from "../lib/supabase";
import { useAuth } from "../lib/auth";

type Category = "bug" | "idea" | "copy" | "other";

const CATEGORIES: Array<{ value: Category; label: string }> = [
  { value: "bug", label: "Bug" },
  { value: "idea", label: "Idea / feature" },
  { value: "copy", label: "Copy / wording" },
  { value: "other", label: "Other" },
];

export interface FeedbackModalProps {
  onClose: () => void;
  /** Opens the sign-in modal — shown to signed-out users. */
  onRequestSignIn?: () => void;
  onSubmitted?: () => void;
}

export function FeedbackModal({ onClose, onRequestSignIn, onSubmitted }: FeedbackModalProps) {
  const { user } = useAuth();
  const [category, setCategory] = useState<Category | "">("");
  const [message, setMessage] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [done, setDone] = useState(false);

  // Close on Escape.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [onClose]);

  const canSubmit = !!user && !submitting && message.trim().length > 0;

  const handleSubmit = async () => {
    if (!user?.email) { setError("You must be signed in to send feedback."); return; }
    if (message.trim().length === 0) return;
    setSubmitting(true);
    setError(null);
    const { error: err } = await supabase.from("app_feedback").insert({
      reporter_email: user.email,
      category: category || null,
      message: message.trim(),
      user_agent: typeof navigator !== "undefined" ? navigator.userAgent : null,
      app_path: typeof window !== "undefined" ? window.location.pathname + window.location.search : null,
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
        aria-label="Send feedback"
      >
        <header className="flex items-center justify-between px-4 py-3 border-b border-slate-200 dark:border-slate-700 flex-shrink-0">
          <h2 className="text-base font-semibold text-slate-900 dark:text-slate-100">
            Send feedback
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
            <p>Thanks — your feedback has been recorded.</p>
            <button
              type="button"
              onClick={onClose}
              className="px-3 py-1.5 text-sm rounded bg-blue-600 text-white hover:bg-blue-700"
            >
              Done
            </button>
          </div>
        ) : !user ? (
          <div className="px-4 py-6 text-sm text-slate-700 dark:text-slate-300 space-y-3">
            <p>Please sign in to send feedback — it lets me follow up if I have a question.</p>
            <div className="flex justify-end gap-2">
              <button
                type="button"
                onClick={onClose}
                className="px-3 py-1.5 text-sm rounded border border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={() => { onClose(); onRequestSignIn?.(); }}
                className="px-3 py-1.5 text-sm rounded bg-blue-600 text-white hover:bg-blue-700"
              >
                Sign in
              </button>
            </div>
          </div>
        ) : (
          <div className="px-4 py-3 space-y-4">
            {/* Category (optional). */}
            <div className="space-y-1">
              <label htmlFor="feedback-category" className="text-xs font-medium text-slate-700 dark:text-slate-300">
                Category <span className="text-slate-400">(optional)</span>
              </label>
              <select
                id="feedback-category"
                value={category}
                onChange={(e) => setCategory(e.target.value as Category | "")}
                className="w-full px-2 py-1.5 text-sm rounded border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100"
              >
                <option value="">— Choose one —</option>
                {CATEGORIES.map((c) => (
                  <option key={c.value} value={c.value}>{c.label}</option>
                ))}
              </select>
            </div>

            {/* Message. */}
            <div className="space-y-1">
              <label htmlFor="feedback-message" className="text-xs font-medium text-slate-700 dark:text-slate-300">
                What's on your mind? <span className="text-slate-400">Bugs, ideas, copy tweaks…</span>
              </label>
              <textarea
                id="feedback-message"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                rows={5}
                placeholder="Tell me what's working, what isn't, or what you'd love to see."
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
                {submitting ? "Sending…" : "Send"}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
