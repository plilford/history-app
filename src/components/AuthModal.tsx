import { useEffect, useRef, useState } from "react";
import { useAuth } from "../lib/auth";

type Mode = "signin" | "signup";

export function AuthModal({ onClose }: { onClose: () => void }) {
  const { signIn, signUp } = useAuth();
  const [mode, setMode] = useState<Mode>("signin");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [info, setInfo] = useState<string | null>(null);
  const emailRef = useRef<HTMLInputElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    emailRef.current?.focus();
  }, []);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [onClose]);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setInfo(null);
    if (!email || !password) {
      setError("Email and password required.");
      return;
    }
    if (mode === "signup" && password.length < 6) {
      setError("Password must be at least 6 characters.");
      return;
    }
    setBusy(true);
    if (mode === "signin") {
      const { error } = await signIn(email, password);
      setBusy(false);
      if (error) setError(error);
      else onClose();
    } else {
      const { error, needsConfirmation } = await signUp(email, password);
      setBusy(false);
      if (error) setError(error);
      else if (needsConfirmation) {
        setInfo(
          "Check your email for a confirmation link, then sign in.",
        );
        setMode("signin");
      } else {
        onClose();
      }
    }
  }

  return (
    <div
      className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center px-4"
      onMouseDown={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div
        ref={containerRef}
        className="w-full max-w-sm rounded-lg border border-slate-700 bg-slate-900 shadow-2xl"
        role="dialog"
        aria-label={mode === "signin" ? "Sign in" : "Sign up"}
      >
        <div className="flex items-center justify-between px-4 pt-4">
          <div className="flex gap-3 text-sm">
            <button
              type="button"
              onClick={() => { setMode("signin"); setError(null); setInfo(null); }}
              className={`pb-1 border-b-2 ${
                mode === "signin"
                  ? "border-slate-100 text-slate-100"
                  : "border-transparent text-slate-400 hover:text-slate-200"
              }`}
            >
              Sign in
            </button>
            <button
              type="button"
              onClick={() => { setMode("signup"); setError(null); setInfo(null); }}
              className={`pb-1 border-b-2 ${
                mode === "signup"
                  ? "border-slate-100 text-slate-100"
                  : "border-transparent text-slate-400 hover:text-slate-200"
              }`}
            >
              Sign up
            </button>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close"
            className="w-8 h-8 flex items-center justify-center rounded text-slate-400 hover:text-slate-100 hover:bg-slate-800"
          >
            <span aria-hidden className="text-lg leading-none">×</span>
          </button>
        </div>

        <form onSubmit={submit} className="px-4 pt-3 pb-4 space-y-3">
          <label className="block text-xs text-slate-400">
            Email
            <input
              ref={emailRef}
              type="email"
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-1 w-full px-2 py-1.5 rounded border border-slate-700 bg-slate-800 text-slate-100 text-sm focus:outline-none focus:border-slate-500"
            />
          </label>
          <label className="block text-xs text-slate-400">
            Password
            <input
              type="password"
              autoComplete={mode === "signin" ? "current-password" : "new-password"}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 w-full px-2 py-1.5 rounded border border-slate-700 bg-slate-800 text-slate-100 text-sm focus:outline-none focus:border-slate-500"
            />
          </label>

          {error && (
            <div className="text-xs text-red-400 bg-red-950/40 border border-red-900 rounded px-2 py-1.5">
              {error}
            </div>
          )}
          {info && (
            <div className="text-xs text-emerald-300 bg-emerald-950/40 border border-emerald-900 rounded px-2 py-1.5">
              {info}
            </div>
          )}

          <button
            type="submit"
            disabled={busy}
            className="w-full px-3 py-2 rounded bg-slate-100 text-slate-900 text-sm font-medium hover:bg-white disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {busy
              ? "…"
              : mode === "signin"
                ? "Sign in"
                : "Create account"}
          </button>

          <p className="text-[10px] text-slate-500 leading-snug">
            Favourites are stored against your account so they follow you between devices.
          </p>
        </form>
      </div>
    </div>
  );
}
