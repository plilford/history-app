"""
One-shot conversion: every dark-only Tailwind class in the React source gets
a paired light-mode default. Run once; safe to re-run (the regex
negative-lookbehind for `dark:` prevents double-prefixing).

Usage:  python tools/theme_sweep.py
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

# Each rule: (existing-class regex, replacement that includes the light
# default AND the dark: prefix on the original). The leading
# `(?<!dark:)(?<!hover:dark:)(?<!focus:dark:)(?<![\w:-])` negative lookbehind
# blocks double-prefixing if the script is re-run, and also stops the regex
# from matching inside another longer class name.
RULES: list[tuple[str, str]] = [
    # ----- Background ----------------------------------------------------
    (r"bg-slate-900",  "bg-white dark:bg-slate-900"),
    (r"bg-slate-800",  "bg-slate-50 dark:bg-slate-800"),
    (r"bg-slate-700",  "bg-slate-200 dark:bg-slate-700"),
    # ----- Text ----------------------------------------------------------
    (r"text-slate-100", "text-slate-900 dark:text-slate-100"),
    (r"text-slate-200", "text-slate-800 dark:text-slate-200"),
    (r"text-slate-300", "text-slate-700 dark:text-slate-300"),
    # 400/500 are mid-grey — they read fine on both backgrounds, leave them.
    # ----- Border --------------------------------------------------------
    (r"border-slate-700", "border-slate-200 dark:border-slate-700"),
    (r"border-slate-800", "border-slate-200 dark:border-slate-800"),
    (r"border-slate-600", "border-slate-300 dark:border-slate-600"),
    (r"border-slate-500", "border-slate-400 dark:border-slate-500"),
    (r"border-slate-100", "border-slate-900 dark:border-slate-100"),
    # ----- Hover ---------------------------------------------------------
    (r"hover:bg-slate-800",   "hover:bg-slate-100 dark:hover:bg-slate-800"),
    (r"hover:bg-slate-700",   "hover:bg-slate-200 dark:hover:bg-slate-700"),
    (r"hover:text-slate-100", "hover:text-slate-900 dark:hover:text-slate-100"),
    (r"hover:text-slate-200", "hover:text-slate-800 dark:hover:text-slate-200"),
    # ----- Focus ---------------------------------------------------------
    (r"focus:bg-slate-800",       "focus:bg-slate-100 dark:focus:bg-slate-800"),
    (r"focus:bg-slate-700",       "focus:bg-slate-200 dark:focus:bg-slate-700"),
    (r"focus:border-slate-500",   "focus:border-slate-400 dark:focus:border-slate-500"),
]


def transform(text: str) -> tuple[str, int]:
    total = 0
    for find, repl in RULES:
        # Negative lookbehind on `dark:` and on any other class-prefix
        # character so we don't double-prefix on re-run. `\b` at the end
        # ensures we stop at a class boundary.
        pattern = re.compile(rf"(?<![\w:-])(?<!dark:){find}\b")
        text, n = pattern.subn(repl, text)
        total += n
    return text, total


def main() -> int:
    files = list(SRC.glob("*.tsx")) + list((SRC / "components").glob("*.tsx"))
    grand_total = 0
    for f in files:
        original = f.read_text(encoding="utf-8")
        new, n = transform(original)
        if n > 0:
            f.write_text(new, encoding="utf-8")
            print(f"  {f.relative_to(ROOT)}: {n} replacements")
            grand_total += n
    print(f"Total: {grand_total} replacements across {len(files)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
