# Output Format — `brand-system/` Folder

This is the contract for Phase 3 of the brand-system skill. Every brand generated must produce a folder containing exactly these ten files. Each file's structure is fixed; the *content* is shaped by the chosen direction.

```
brand-system/
├── README.md          # Index + how to use
├── palette.json       # Semantic color tokens
├── type.css           # Type scale + ready-to-paste classes
├── space.css          # Spacing scale + layout primitives + radius
├── logo.md            # Wordmark spec + clear-space + monogram
├── tone.md            # Voice attributes + do/don't + microcopy
├── imagery.md         # Reference scene system + 8-10 prompts
├── accessibility.md   # WCAG contrast report (computed)
├── moodboard.html     # Composed visual moodboard
└── applications.html  # System rendered on 4 real surfaces
```

---

## 1. `README.md`

```markdown
# {Brand Name} — Brand System

**Direction:** {Direction Name} ({preset name from TONE_PRESETS or "Custom"})
**One-liner:** {one sentence from the brief}
**Generated:** {YYYY-MM-DD}

## What's in this folder

| File | What it gives you |
| --- | --- |
| `palette.json` | Color tokens with semantic names + hex. Drop into Tailwind, Figma variables, CSS. |
| `type.css` | Font imports, type scale, ready classes (`.display`, `.h1-h6`, `.body`, `.caption`). |
| `tone.md` | Voice attributes, do/don't, microcopy snippets. |
| `imagery.md` | Reference-scene system + 8-10 ready-to-paste image prompts. |
| `moodboard.html` | Open in browser to see the system composed. |

## Sacred & forbidden

- **Sacred:** {from the brief}
- **Forbidden:** {from the brief}

## Iterating

Re-run the `brand-system` skill and choose **Refine** to tighten palette, shift type, sharpen voice, or expand imagery. The moodboard rebuilds from the artifacts.
```

---

## 2. `palette.json`

Semantic, role-based tokens. Avoid color names ("red", "blue") in keys — use roles. **Always include at least one `signal` color with personality.**

```json
{
  "$schema": "https://design-tokens.org/schema",
  "brand": "{Brand Name}",
  "direction": "{Direction Name}",
  "tokens": {
    "ground": {
      "value": "#f4f1ea",
      "role": "page background — the canvas everything sits on",
      "usage": "html, body, page surfaces"
    },
    "ink": {
      "value": "#14110f",
      "role": "primary text and structural strokes",
      "usage": "body copy, borders, icons"
    },
    "ink-soft": {
      "value": "#6e6862",
      "role": "secondary text — captions, metadata",
      "usage": "labels, timestamps, footnotes"
    },
    "signal": {
      "value": "#b04a2c",
      "role": "the one color that does work — accents, links, CTAs",
      "usage": "buttons, links, highlights, focus rings"
    },
    "signal-deep": {
      "value": "#7a2e18",
      "role": "darker pair of signal — hover states, pressed states",
      "usage": "interactive deepening only"
    },
    "quiet-1": {
      "value": "#d8d2c4",
      "role": "supporting tone — surfaces that need to recede",
      "usage": "cards, dividers, hover backgrounds"
    },
    "quiet-2": {
      "value": "#4a5743",
      "role": "second supporting tone — adds depth, never primary",
      "usage": "tags, secondary buttons, info states"
    }
  },
  "neutrals": {
    "scale": [
      {"step": 50,  "value": "#fafaf8"},
      {"step": 100, "value": "#f4f1ea"},
      {"step": 200, "value": "#e2dccd"},
      {"step": 300, "value": "#c9c1b0"},
      {"step": 400, "value": "#a39c8a"},
      {"step": 500, "value": "#7d7565"},
      {"step": 600, "value": "#5a5448"},
      {"step": 700, "value": "#3e392f"},
      {"step": 800, "value": "#26221b"},
      {"step": 900, "value": "#14110f"}
    ],
    "note": "Anchored on ground and ink — interpolated, not arbitrary."
  }
}
```

**Rules:**
- Minimum 5 tokens, maximum 8. Include `ground`, `ink`, `signal`, plus 2-5 supporting tones.
- Every token has `value`, `role`, and `usage` fields.
- Always include the 10-step neutral scale interpolated between `ground` and `ink`.
- Never name a token after a literal color (`"red": "#ff0000"`). Use roles (`signal`, `quiet-1`).

---

## 3. `type.css`

Self-contained CSS with font imports, custom properties for the scale, and ready-to-paste classes.

```css
/* ============================================================
   {Brand Name} — Typography
   Direction: {Direction Name}
   Display: {Display Font} — {weight}
   Body:    {Body Font} — {weights}
   Mono:    {Mono Font, if used}
   ============================================================ */

@import url('https://fonts.googleapis.com/css2?family={Display+Font}:wght@{weights}&family={Body+Font}:wght@{weights}&display=swap');

:root {
    --font-display: '{Display Font}', {fallback}, serif;
    --font-body:    '{Body Font}', {fallback}, sans-serif;
    --font-mono:    '{Mono Font}', ui-monospace, monospace;

    /* Modular scale, anchored at 1rem = 16px body */
    --fs-display: clamp(3rem, 7vw, 6rem);     /* hero */
    --fs-h1:      clamp(2rem, 4.5vw, 3.5rem);
    --fs-h2:      clamp(1.5rem, 3vw, 2.25rem);
    --fs-h3:      clamp(1.25rem, 2.2vw, 1.625rem);
    --fs-body:    clamp(1rem, 1.15vw, 1.125rem);
    --fs-small:   clamp(0.8125rem, 0.95vw, 0.875rem);
    --fs-caption: clamp(0.75rem, 0.85vw, 0.8125rem);

    /* Line-height pairs each size with its purpose */
    --lh-tight:   0.95;  /* display only */
    --lh-snug:    1.15;  /* headings */
    --lh-body:    1.55;  /* body copy */
    --lh-loose:   1.7;   /* long-form reading */

    /* Letter-spacing — tight on display, loose on labels */
    --tracking-display: -0.02em;
    --tracking-label:   0.12em;
}

.display {
    font-family: var(--font-display);
    font-size: var(--fs-display);
    font-weight: {display weight};
    line-height: var(--lh-tight);
    letter-spacing: var(--tracking-display);
}

.h1 { font-family: var(--font-display); font-size: var(--fs-h1); line-height: var(--lh-snug); }
.h2 { font-family: var(--font-display); font-size: var(--fs-h2); line-height: var(--lh-snug); }
.h3 { font-family: var(--font-body); font-size: var(--fs-h3); font-weight: 600; line-height: var(--lh-snug); }

.body {
    font-family: var(--font-body);
    font-size: var(--fs-body);
    line-height: var(--lh-body);
}

.body-lead { font-size: calc(var(--fs-body) * 1.15); line-height: var(--lh-loose); }

.caption {
    font-family: var(--font-mono, var(--font-body));
    font-size: var(--fs-caption);
    text-transform: uppercase;
    letter-spacing: var(--tracking-label);
}
```

**Rules:**
- Use Google Fonts or Fontshare — never system fonts as display.
- Always wrap sizes in `clamp(min, vw, max)` — never fixed `px` or `rem` alone.
- Include the modular scale + the line-height + tracking variables. These are non-optional.
- Comment the file with brand name, direction, and font choices.

---

## 4. `tone.md`

```markdown
# Voice — {Brand Name}

## What we sound like

**{Attribute 1}** — {one-line definition specific to this brand}
**{Attribute 2}** — {…}
**{Attribute 3}** — {…}
*(3-5 attributes total. Each one must be specific enough that you could reject a sentence for failing it.)*

## We are / we are not

| We are | We are not |
| --- | --- |
| {specific} | {specific} |
| {specific} | {specific} |
| {specific} | {specific} |
| {specific} | {specific} |
| {specific} | {specific} |

*(5 pairs minimum. Pairs must be specific — "honest, not coy" beats "professional, not casual".)*

## Sample sentences

### Do say
1. {sentence}
2. {sentence}
... 10 total

### Don't say
1. {sentence — and **say why**: "sounds like generic SaaS" / "uses the word 'seamless'"}
2. {sentence — why}
... 10 total

## Microcopy snippets

**Primary CTA:** "{exact label}" — used when {context}
**Empty state:** "{exact copy}" — used when {context}
**Error message:** "{exact copy}" — used when {context}

## Banned words

empower, elevate, seamless, delight, unleash, revolutionize, transform, journey, solutions, world-class, cutting-edge, best-in-class
*(Plus any specific to this brief.)*
```

**Rules:**
- Voice attributes must be brand-specific. "Trustworthy" is not — "earnest the way a high-school physics teacher is earnest" is.
- Do/don't sentences must be in the brand's *actual product domain*. Generic Lorem-flavored examples are rejected.
- The "why" annotation on Don't sentences is mandatory — it teaches the rule.

---

## 5. `imagery.md`

The "moodboard set of prompts" — text-described reference scenes ready to paste into Midjourney, Gemini, FLUX, or shoot live.

```markdown
# Imagery System — {Brand Name}

## Subject buckets

We photograph (or commission):
- **{Bucket 1}** — {what falls in this bucket, what it's for}
- **{Bucket 2}** — {…}
- **{Bucket 3}** — {…}
*(3-5 buckets. Each bucket has a purpose: hero, supporting, texture, portrait, etc.)*

## Lighting rules

- {rule — e.g., "Always natural, never strobe"}
- {rule — e.g., "Time of day matters: 6am or 6pm. Never noon"}
- {rule}

## Material & palette anchors

Every image should contain at least one of: {list of materials/tones from the palette}.
Surfaces lean: {warm/cool/neutral specifics}.

## Reference prompts (8-10)

Format: `subject — lighting — material/palette anchor`

1. **{Scene title}** — {full prompt-ready description with subject, light, material, color anchors}
2. **{Scene title}** — {…}
... 8-10 total

Each prompt must be specific enough to shoot. Vague subjects ("a person", "a workspace") are rejected.

## Do not depict

- {specific thing — e.g., "Smiling people facing camera"}
- {specific thing — e.g., "Isometric illustrations"}
- {specific thing — e.g., "Gradient meshes as background"}
*(5+ items. Specific bans, not "anything cheesy".)*
```

**Rules:**
- Every prompt is `subject — lighting — material/palette anchor`. All three components mandatory.
- 8-10 prompts minimum. Each must be different enough that shooting all of them produces a varied set.
- "Do not depict" must be specific. Bans like "no clichés" are useless.

---

## 6. `moodboard.html`

A polished standalone HTML page composing the entire system. Self-contained: includes the chosen direction's CSS variables, full contents of `moodboard-base.css`, and the @import for fonts.

Sections (in this order):
1. **Masthead** — brand name + direction name + one-liner
2. **Palette strip** — every token from `palette.json` rendered as a swatch
3. **Type specimen** — display sample (the brand name) + body paragraph using real product copy
4. **Voice** — one tagline + one body paragraph from `tone.md`
5. **Imagery references** — the 8-10 reference scenes from `imagery.md` as ref-cards
6. **Materials chips** — texture/material descriptors as chips
7. **Footer** — brand name + direction + generation date

This is the Phase-2 preview format, *upgraded* with all artifacts in place. Open this file to ship the deliverable.

**Rules:**
- Single self-contained `.html` file. All CSS inline. Fonts via Google/Fontshare CDN.
- Include the FULL contents of `moodboard-base.css` in the `<style>` block, then add direction-specific overrides in a second `:root` block.
- Comment every section with `/* === SECTION NAME === */`.
- No `<script>` — this is a static moodboard.

---

## 7. `space.css`

Spacing tokens, layout primitives, and radius/shadow scales. Imports `type.css` so a single `<link rel="stylesheet" href="space.css">` brings the whole system. Every value uses `clamp()`.

```css
/* ============================================================
   {Brand Name} — Spacing & Layout
   Direction: {Direction Name}
   ============================================================ */

@import url('./type.css');

:root {
    /* === SPACING — modular, clamp-based === */
    --space-0:  0;
    --space-1:  clamp(0.25rem, 0.5vw, 0.375rem);
    --space-2:  clamp(0.5rem,  1vw,   0.75rem);
    --space-3:  clamp(0.75rem, 1.5vw, 1rem);
    --space-4:  clamp(1rem,    2vw,   1.5rem);
    --space-5:  clamp(1.5rem,  3vw,   2rem);
    --space-6:  clamp(2rem,    4vw,   3rem);
    --space-8:  clamp(2.5rem,  5vw,   4rem);
    --space-10: clamp(3rem,    6vw,   5rem);
    --space-12: clamp(4rem,    8vw,   7rem);

    /* === LAYOUT === */
    --content-max:    72ch;
    --container-max:  1280px;
    --gutter:         var(--space-5);
    --section-gap:    var(--space-10);

    /* === RADIUS — pick a direction-specific personality === */
    /* Sharp/technical: 0, 2px, 4px */
    /* Editorial: 4px, 8px, 16px */
    /* Playful: 8px, 16px, 999px */
    --radius-sm: {value};
    --radius-md: {value};
    --radius-lg: {value};

    /* === SHADOW — used sparingly, never as default === */
    --shadow-low:  0 1px 2px rgba(0,0,0,0.04);
    --shadow-mid:  0 4px 12px rgba(0,0,0,0.08);
}

.container {
    max-width: var(--container-max);
    margin-inline: auto;
    padding-inline: var(--gutter);
}

.stack > * + * { margin-top: var(--space-4); }
.stack-tight > * + * { margin-top: var(--space-2); }
.stack-loose > * + * { margin-top: var(--space-6); }
```

**Rules:**
- Spacing scale uses Fibonacci-like progression (1, 2, 3, 4, 5, 6, 8, 10, 12) — never include all numbers.
- Radius scale must reflect the direction's personality. Sharp/technical directions use 0-4px; editorial uses 4-16px; playful uses up to 999px (pills).
- Shadow tokens exist but the system should rarely reach for them. Default to no shadow unless the direction explicitly calls for it.

---

## 8. `logo.md`

Wordmark specification. Brand systems without a logo spec feel half-finished — every consumer of the brand needs to know how to set the name, what to do at favicon scale, and what NOT to do.

```markdown
# Wordmark — {Brand Name}

## Primary lockup
The wordmark sets **{Brand Name}** in **{display font}** {weight} at **{tracking}**.
Single line; no inline glyphs, dashes, or "presents:" treatments.

```html
<span class="wordmark">{Brand Name}</span>
```
```css
.wordmark {
    font-family: var(--font-display);
    font-weight: {weight};
    letter-spacing: {tracking};
    color: var(--ink);
}
```

## Clear space
Minimum clear space around the wordmark = **the height of one capital letter** (cap-height) on all four sides. Treat this as the no-fly zone. Never let other elements cross it.

## Minimum size
| Context | Minimum |
| --- | --- |
| Digital | {16px height} |
| Print | {12pt height} |
| Below minimum | Use the **monogram** instead |

## Monogram (icon-only fallback)
The single character or initials that stand in for the wordmark when the full lockup won't read. Used in: favicons, podcast platform icons, social avatars, app tile icons.

**Glyph:** {single character or initials}
**Set in:** {display font} {weight}
**Lockup:** Centered in a {ground / signal / ink} square. Optical centering — visually centered, not pixel-centered.

## Color usage
- **Primary (light):** ink on ground
- **Reverse (dark):** ground on ink
- **On signal background:** ground (never ink-on-signal — fails contrast)
- **Single-color print:** ink only — never tint, never multi-color the wordmark

## Don't
- Don't stretch, condense, or skew
- Don't apply drop shadows, glows, or outlines
- Don't rotate or place on a curve
- Don't combine with other typefaces inline
- Don't recolor the wordmark with non-system colors
- Don't place over a busy photograph without a solid backplate
```

**Rules:**
- Provide both the visual spec and the CSS recipe. Designers and engineers are both consumers.
- Clear-space, minimum size, and monogram are **mandatory** sections. A logo spec without these is incomplete.
- Color usage must call out which combinations fail accessibility (e.g., "never ink on signal").
- Don't list must be 5+ specific bans — generic "don't misuse" is useless.

---

## 9. `accessibility.md`

Computed WCAG contrast report. The skill must mathematically compute each ratio, not estimate. Use the standard formula:
- sRGB → linear RGB (gamma 2.4)
- Relative luminance L = 0.2126·R + 0.7152·G + 0.0722·B
- Contrast ratio = (L_lighter + 0.05) / (L_darker + 0.05)

**WCAG thresholds:**
- AA body text: 4.5:1
- AA large text (18pt+ / 14pt+ bold): 3:1
- AAA body text: 7:1
- AAA large text: 4.5:1

```markdown
# Accessibility — {Brand Name}

## WCAG contrast — every text-on-background pair

| Foreground | Background | Ratio | Body AA | Large AA | Notes |
| --- | --- | --- | --- | --- | --- |
| ink {hex} | ground {hex} | {x.x:1} | ✅/❌ | ✅/❌ | Primary body text |
| ink-soft {hex} | ground {hex} | {x.x:1} | ✅/❌ | ✅/❌ | Secondary text |
| signal {hex} | ground {hex} | {x.x:1} | ✅/❌ | ✅/❌ | {role — body text or decorative-only} |
| signal {hex} | ink {hex} | {x.x:1} | ✅/❌ | ✅/❌ | Signal on dark surfaces |
| ground {hex} | ink {hex} | {x.x:1} | ✅/❌ | ✅/❌ | Reverse / dark mode body |
| ... (all combinations) |

## Decorative-only colors
Colors that fail body AA on the page background. **Never set text in these colors on `ground`.** Use them for shapes, accents, dividers, focus rings, or only on darker surfaces where they pass.

- {token name} — fails on ground; passes on ink → use only on dark surfaces

## Focus ring
2px solid {signal token} with 2px outline-offset. Visible always. Never `outline: none` without a replacement.

## Rules for adding new combinations
The system can't catch off-token combinations. Before introducing any color combination not in this table:
1. Compute the ratio at https://webaim.org/resources/contrastchecker/
2. If it fails AA, add it to the decorative-only list
3. Update this file
```

**Rules:**
- Compute ratios for EVERY foreground/background pair of palette tokens — don't skip combinations.
- Mark each result against AA body and AA large explicitly. Don't just say "passes".
- The `signal` color often fails on `ground` — that's expected. Flag it as decorative-only with explicit usage rules.
- The focus-ring section is mandatory. Inaccessible focus management is the single most common a11y failure.

---

## 10. `applications.html`

A single self-contained HTML page rendering the system on **4 real surfaces**. Every value is a token reference (`var(--space-4)`, `var(--font-body)`, `var(--token-name)`) — no inline hex, no inline px. If a surface needs something the tokens don't provide, the system is incomplete; extend the tokens, don't bypass them.

**Surfaces (all four required):**

1. **Website hero** — full-width section with masthead nav, hero headline (uses display type), subhead (body lead), primary CTA. Tests: type scale, container width, signal color in CTA, focus-ring visibility.
2. **Podcast cover art / square 1:1** — 1024×1024 square (rendered at scale to fit page). Wordmark or monogram, episode/series title, optional guest name, optional issue number. Tests: monogram legibility, palette at large scale, type at extreme size.
3. **Social post / 4:5** — quote-card format. One pulled quote in display type, attribution, brand mark in corner. Tests: voice + type composing into a shareable artifact.
4. **Email header** — wide narrow strip (e.g., 600×120). Brand name on left, optional issue/date on right, signal-color rule beneath. Tests: brand identification at small vertical space.

**Layout:**
The page stacks the 4 surfaces vertically, each in its own section with a section label, the surface itself rendered at correct aspect ratio (`aspect-ratio: 16/9`, `1/1`, `4/5`, `5/1`), and a one-line caption noting which tokens it exercises.

**Rules:**
- Inline the token values (color/spacing/font CSS custom properties) at the top of the `<style>` block — do NOT `@import` `space.css`. The file must work when double-clicked from a file manager (some browsers block cross-origin `@import` from `file://`). Tokens here are a snapshot, regenerated whenever `palette.json` / `space.css` change.
- The first lines of the `<style>` block must be a header comment naming the file as a snapshot:
  ```css
  /* ============================================================
     applications.html — token SNAPSHOT, generated {YYYY-MM-DD}
     Tokens below are copied from palette.json + type.css + space.css
     at generation time. If you edit a token in those files, re-run
     /brand-system → Refine to regenerate this file. Do not hand-edit.
     ============================================================ */
  ```
- Every color: `var(--token-name)` from the inlined snapshot. No raw hex elsewhere in the file.
- Every spacing: `var(--space-N)`. No fixed px.
- Every font: `var(--font-display | --font-body | --font-mono)`. No font-family overrides.
- The 4 surfaces are non-negotiable. If a brand truly doesn't have one (e.g., no podcast → swap cover art for product card), substitute with the nearest analog and note the swap.

---

## Quality gate before delivery

Before opening the moodboard, verify:

- [ ] `palette.json` has 5-8 tokens, all with `value` + `role` + `usage`
- [ ] `palette.json` includes a `signal` color with real personality (not generic blue)
- [ ] `type.css` uses `clamp()` for every size, no fixed px
- [ ] `type.css` imports fonts from Google Fonts or Fontshare (not system fonts)
- [ ] `space.css` has 8-10 step spacing scale, all `clamp()`-wrapped
- [ ] `space.css` defines `--radius-sm/md/lg` consistent with the direction's personality
- [ ] `logo.md` defines lockup, clear-space (in cap-heights), minimum size, monogram fallback, color usage, and 5+ don'ts
- [ ] `tone.md` has 3-5 brand-specific voice attributes, 5+ we-are/we-are-not pairs, 10 do + 10 don't sentences (with reasons)
- [ ] `tone.md` rejects every word in the banned list
- [ ] `imagery.md` has 8-10 reference prompts, each `subject — light — material` triplet
- [ ] `imagery.md` has 5+ "do not depict" specifics
- [ ] `accessibility.md` has computed contrast ratios for EVERY text-on-background combination
- [ ] `accessibility.md` flags decorative-only colors with explicit usage rules
- [ ] `accessibility.md` defines a focus-ring spec
- [ ] `moodboard.html` opens, fonts load, palette renders, no broken layout at 1280×720
- [ ] `applications.html` renders 4 surfaces (hero, cover, social, email) using only system tokens
- [ ] `applications.html` has zero inline hex codes, zero inline px values, zero off-system fonts
- [ ] `README.md` names the brand, the direction, the date, the accessibility result, and what's in each file
- [ ] Folder is at the requested path (default `./brand-system/`)

If any item fails, fix before delivery.
