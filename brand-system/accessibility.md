# Accessibility — The Founder's Foyer

Computed contrast ratios for every text-on-background pair in the palette.

**Method:** sRGB → linear RGB (gamma 2.4) → relative luminance (0.2126·R + 0.7152·G + 0.0722·B) → contrast ratio (L_lighter + 0.05) / (L_darker + 0.05). WCAG 2.1 thresholds: AA body ≥ 4.5:1, AA large (18pt+/14pt+ bold) ≥ 3:1, AAA body ≥ 7:1. WCAG 2.2 SC 1.4.11 non-text (focus rings, UI component boundaries) ≥ 3:1.

> **v1.1 change:** `signal-deep` is now **#1a7a52** (was #2da775). The old value sat at 2.7:1 on ground — decorative-only — while the artifacts were quietly using it for label text. The new value passes body AA on ground. The two greens are one idea on two surfaces: `signal` (#4ad295) works on dark, `signal-deep` works on light.

## WCAG contrast — every text-on-background pair

| Foreground | Background | Ratio | Body AA | Large AA | Body AAA | Notes |
| --- | --- | --- | :---: | :---: | :---: | --- |
| ink `#15171a` | ground `#f6f1e3` | **15.9 : 1** | ✅ | ✅ | ✅ | Primary body text |
| ink-soft `#6c6e74` | ground `#f6f1e3` | **4.5 : 1** | ✅ | ✅ | ❌ | Secondary text — captions, metadata. Marginal; prefer larger sizes |
| signal `#4ad295` | ground `#f6f1e3` | **1.7 : 1** | ❌ | ❌ | ❌ | **DECORATIVE ONLY on light** — never set text; fails non-text 3:1 too |
| signal `#4ad295` | ink `#15171a` | **9.4 : 1** | ✅ | ✅ | ✅ | Signal text on dark — links, cursors, episode numbers |
| signal-deep `#1a7a52` | ground `#f6f1e3` | **4.7 : 1** | ✅ | ✅ | ❌ | The working green on light — labels, code, links, focus rings |
| signal-deep `#1a7a52` | quiet `#d8d2c4` | **3.5 : 1** | ❌ | ✅ | ❌ | Large/bold only on quiet cards |
| ground `#f6f1e3` | signal-deep `#1a7a52` | **4.7 : 1** | ✅ | ✅ | ❌ | The call-to-listen filled button |
| cobalt `#2a4cd0` | ground `#f6f1e3` | **6.1 : 1** | ✅ | ✅ | ❌ | Inline notation, footnote markers, link hover |
| cobalt `#2a4cd0` | quiet `#d8d2c4` | **4.6 : 1** | ✅ | ✅ | ❌ | Notation on quiet cards |
| cobalt `#2a4cd0` | ink `#15171a` | **2.6 : 1** | ❌ | ❌ | ❌ | **Never use cobalt on dark** |
| rose `#c97a8b` | ground `#f6f1e3` | **2.8 : 1** | ❌ | ❌ | ❌ | **DECORATIVE ONLY on light** — never body text |
| rose `#c97a8b` | ink `#15171a` | **5.7 : 1** | ✅ | ✅ | ❌ | Rose text on dark — tags, warm labels |
| ink `#15171a` | rose `#c97a8b` | **5.7 : 1** | ✅ | ✅ | ❌ | Tag component — ink text on rose fill |
| ground `#f6f1e3` | ink `#15171a` | **15.9 : 1** | ✅ | ✅ | ✅ | Reverse / dark mode body |
| quiet `#d8d2c4` | ink `#15171a` | **11.9 : 1** | ✅ | ✅ | ✅ | Secondary text on dark — use this, NOT ink-soft |
| ink `#15171a` | quiet `#d8d2c4` | **11.9 : 1** | ✅ | ✅ | ✅ | Body on muted card backgrounds |
| ink-soft `#6c6e74` | quiet `#d8d2c4` | **3.4 : 1** | ❌ | ✅ | ❌ | Large only on quiet — never small text |
| ink-soft `#6c6e74` | ink `#15171a` | **3.5 : 1** | ❌ | ✅ | ❌ | **Avoid** — for secondary text on dark, use `quiet` instead |

## Decorative-only colors on light surfaces

Two colors fail body AA on `ground` and must NEVER be used for text on light surfaces:

- **`signal` (bright circuit-green #4ad295)** — 1.7:1 on ground. On light surfaces it is exclusively decorative: shapes, large icons (24px+), photographic accents. For any *working* use on light (text, links, rings, code), use `signal-deep`. On dark surfaces (`ink`, neutral-700+) it is the primary accent.
- **`rose` (#c97a8b)** — 2.8:1 on ground. Use as fill behind ink text (5.7:1, the `.tag` component), decorative accents, photographic tints. Never body text on ground.

## Secondary text on dark surfaces

`ink-soft` fails on `ink` (3.5:1). For metadata and secondary text on dark surfaces — podcast cover meta, dark-mode captions — use **`quiet`** (11.9:1). This was a live bug in v1.0's cover art; fixed in v1.1.

## Focus ring spec

```css
:focus-visible {
    outline: 2px solid var(--signal-deep);  /* 4.7:1 on ground — passes SC 1.4.11 (≥3:1) */
    outline-offset: 2px;
}
.on-dark :focus-visible,
[data-surface="dark"] :focus-visible {
    outline-color: var(--signal);           /* 9.4:1 on ink */
}
```

WCAG 2.2 SC 1.4.11 requires **3:1 non-text contrast** for focus indicators against adjacent colors. The v1.0 spec used bright signal on light surfaces at 1.7:1 and argued the eye would "pick up the green fringe" — that was a documented failure, not a pass. v1.1 uses the deep green on light (4.7:1) and the bright green on dark (9.4:1). Never `outline: none` without an equivalent replacement.

## Rules for adding new combinations

The system can't catch off-token combinations. Before introducing any color combination not in the table above:

1. Compute the ratio (https://webaim.org/resources/contrastchecker/ or the method at the top of this file)
2. If it fails AA body, mark it decorative-only and update the rules
3. Never set body text in a color that fails body AA on its background
4. Focus indicators and component boundaries need ≥3:1 against adjacent colors (SC 1.4.11)
5. Update this file with the new pair

## Caveats

- Ratios are computed in sRGB. Wide-gamut displays render slightly different perceptual contrast, but the ratios remain the conformance measure.
- Anti-aliasing on small type at marginal ratios (4.5–5:1) can feel thin — `ink-soft` on ground (4.5:1) and `signal-deep` on ground (4.7:1) both live here. When in doubt, increase weight or size before deepening color.

## Summary

- **4 colors** safe for body text on `ground`: ink, ink-soft, signal-deep, cobalt
- **3 colors** safe for body text on `ink`: ground, signal, rose (quiet also passes, 11.9:1)
- **2 decorative-only colors** on `ground`: signal, rose
- **Focus rings:** signal-deep on light, signal on dark — both clear SC 1.4.11
