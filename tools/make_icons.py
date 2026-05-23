"""
Generate placeholder PWA icons for the History Timelines app.

Outputs three PNGs into ../public/:
  - icon-192.png         192x192 — required by manifest
  - icon-512.png         512x512 — required by manifest
  - icon-512-maskable.png 512x512 with safe-zone padding for Android adaptive icons

Theme: dark navy background (matches manifest theme_color), a stylised timeline
with five markers, year-tick accents in gold. Easy to replace with a designed
icon later — overwrite the files in public/ and rebuild.

Usage (from tools/):
    .venv\\Scripts\\activate
    python make_icons.py
"""
from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent.parent / "public"
OUT.mkdir(parents=True, exist_ok=True)

BG       = (15, 23, 42)        # #0f172a — matches manifest theme/background
LINE     = (203, 213, 225)     # #cbd5e1 — slate-300, the timeline rule
MARKER   = (251, 191, 36)      # #fbbf24 — amber-400 marker dots
ACCENT   = (96, 165, 250)      # #60a5fa — blue-400 for the "now" marker


def render(size: int, maskable: bool = False) -> Image.Image:
    img  = Image.new("RGBA", (size, size), BG)
    d    = ImageDraw.Draw(img)

    # Safe zone for maskable: Android clips ~10% on each side, but the spec
    # asks for content within an 80% centred circle.
    pad  = int(size * 0.20) if maskable else int(size * 0.12)

    # Timeline rule — horizontal line across the centre.
    y    = size // 2
    line_w = max(2, size // 96)
    d.rounded_rectangle(
        (pad, y - line_w // 2, size - pad, y + line_w // 2),
        radius=line_w // 2,
        fill=LINE,
    )

    # Five evenly-spaced markers; the rightmost is the "now" marker (blue).
    n_markers = 5
    span = (size - 2 * pad)
    step = span // (n_markers - 1)
    r    = max(6, size // 20)
    for i in range(n_markers):
        cx = pad + i * step
        colour = ACCENT if i == n_markers - 1 else MARKER
        d.ellipse((cx - r, y - r, cx + r, y + r), fill=colour)
        # Year-tick down from each marker
        tick_h = r * 2
        tick_w = max(2, size // 128)
        d.rounded_rectangle(
            (cx - tick_w // 2, y + r, cx + tick_w // 2, y + r + tick_h),
            radius=tick_w // 2,
            fill=LINE,
        )

    return img


def main() -> None:
    for size, name, maskable in [
        (192, "icon-192.png", False),
        (512, "icon-512.png", False),
        (512, "icon-512-maskable.png", True),
    ]:
        img  = render(size, maskable=maskable)
        path = OUT / name
        img.save(path, "PNG", optimize=True)
        print(f"  wrote {path} ({size}x{size}{', maskable' if maskable else ''})")

    print(f"Done. Icons in {OUT}/")


if __name__ == "__main__":
    main()
