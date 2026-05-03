# Output Format — `brand-system/` Folder

This is the contract for Phase 3 of the brand-system skill. Every brand generated must produce a folder containing exactly these six files. Each file's structure is fixed; the *content* is shaped by the chosen direction.

```
brand-system/
├── README.md          # Index + how to use
├── palette.json       # Semantic color tokens
├── type.css           # Type scale + ready-to-paste classes
├── tone.md            # Voice attributes + do/don't + microcopy
├── imagery.md         # Reference scene system + 8-10 prompts
└── moodboard.html     # Composed visual moodboard
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

## Quality gate before delivery

Before opening the moodboard, verify:

- [ ] `palette.json` has 5-8 tokens, all with `value` + `role` + `usage`
- [ ] `palette.json` includes a `signal` color with real personality (not generic blue)
- [ ] `type.css` uses `clamp()` for every size, no fixed px
- [ ] `type.css` imports fonts from Google Fonts or Fontshare (not system fonts)
- [ ] `tone.md` has 3-5 brand-specific voice attributes, 5+ we-are/we-are-not pairs, 10 do + 10 don't sentences (with reasons)
- [ ] `tone.md` rejects every word in the banned list
- [ ] `imagery.md` has 8-10 reference prompts, each `subject — light — material` triplet
- [ ] `imagery.md` has 5+ "do not depict" specifics
- [ ] `moodboard.html` opens, fonts load, palette renders, no broken layout at 1280×720
- [ ] `README.md` names the brand, the direction, the date, and what's in each file
- [ ] Folder is at the requested path (default `./brand-system/`)

If any item fails, fix before delivery.
