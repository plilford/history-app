// =============================================================================
// Per-occurrence colours.
// =============================================================================
//
// Each occurrence gets a stable colour derived from its event id, used for:
//   - the box outline (border)
//   - the thin range line for periods
//
// We use a fixed palette of ~16 hues that are distinguishable on a dark slate
// background. The same event always lands on the same palette slot.
//
// Tailwind's JIT can't see dynamic class strings, so consumers apply these as
// inline styles (style={{ borderColor, backgroundColor }}).
// =============================================================================

export type OccurrenceColor = {
  /** Full-saturation hue used for border and the range line. */
  border: string;
  /** Tinted dark version used as a subtle box background. */
  background: string;
  /** Same as border but with reduced opacity (for the range line). */
  line: string;
};

// 16 hues evenly distributed around the wheel, chosen so each one reads on a
// slate-900 background without being eye-searing. Saturation/lightness are
// tuned per hue family — yellows/greens need lower lightness than blues to
// stay distinguishable.
const PALETTE: OccurrenceColor[] = [
  // hue, sat, light tuned per family
  mk(0,   70, 60),   // red
  mk(22,  78, 56),   // orange
  mk(42,  78, 55),   // amber
  mk(62,  60, 55),   // yellow-green
  mk(95,  55, 55),   // lime
  mk(135, 50, 52),   // green
  mk(165, 55, 50),   // teal
  mk(190, 65, 55),   // cyan
  mk(210, 70, 60),   // sky
  mk(225, 70, 65),   // blue
  mk(250, 65, 68),   // indigo
  mk(275, 60, 67),   // violet
  mk(295, 60, 65),   // purple
  mk(315, 65, 62),   // magenta
  mk(335, 70, 62),   // pink
  mk(355, 70, 60),   // rose
];

function mk(h: number, s: number, l: number): OccurrenceColor {
  return {
    border: `hsl(${h} ${s}% ${l}%)`,
    background: `hsl(${h} ${Math.round(s * 0.55)}% ${Math.round(l * 0.32)}% / 0.55)`,
    line: `hsl(${h} ${s}% ${l}% / 0.8)`,
  };
}

// Knuth multiplicative hash — mixes the low bits of small sequential ids so
// neighbouring event ids don't all end up on adjacent palette slots.
const KNUTH = 2654435761;

export function colorFor(eventId: number): OccurrenceColor {
  // Coerce through Uint32 then take modulo. (eventId can be > 2^31 in v2.)
  const idx = ((eventId >>> 0) * KNUTH) >>> 0;
  return PALETTE[idx % PALETTE.length];
}

export const PALETTE_SIZE = PALETTE.length;
