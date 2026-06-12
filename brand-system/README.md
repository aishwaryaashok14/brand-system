# The Founder's Foyer — Brand System

**Direction:** The Speculative (Galaxy Brain composite, custom-tuned)
**One-liner:** A podcast for early-stage builders — hallway conversations framed as hypotheses, not conclusions.
**Generated:** 2026-05-03 · **Revised:** 2026-06-11 (v1.1)
**Source:** Reverse-engineered from https://www.thefoundersfoyer.com/ via Phase 1.5 reference ingestion

## What's in this folder

| File | What it gives you |
| --- | --- |
| `palette.json` | 8 semantic color tokens + 10-step neutral scale in **W3C DTCG format** (`$value`/`$type`) — loads directly into Style Dictionary v4+, Tokens Studio, Figma variables. |
| `palette.css` | The CSS emission of `palette.json` — all color custom properties. **This is the keystone**; every other CSS file imports it. |
| `type.css` | JetBrains Mono + Manrope, accessible clamp scale (rem + vw), ready classes (`.display`, `.h1`-`.h3`, `.body`, `.caption`, `.code`, `.aside`, `.footnote`). |
| `space.css` | 10-step fluid spacing scale, layout primitives (`.container`, `.stack`, `.cluster`, `.grid-2/3`), sharp 0–4px radius, motion tokens, focus-ring rule (light + dark variants). |
| `components.css` | Interactive layer — links (light/dark, all states), buttons (`.btn-primary`, `.btn-listen`, `.btn-secondary`, disabled), chips, tags. Every state maps to a pair in `accessibility.md`. |
| `logo.md` | Wordmark spec — lockup, U+2019 apostrophe rule, clear-space, minimum size, monogram (`tff/`) + micro mark (`f/`), color usage, required asset checklist, 10-item don't list. |
| `tone.md` | 5 voice attributes, 7 we-are/we-are-not pairs, 10 do + 10 don't sentences (with reasons), episode-title convention, 3 microcopy snippets, banned-words list. |
| `imagery.md` | 3 subject buckets, lighting rules, material anchors, **10 ready-to-paste reference prompts**, 8-item "do not depict" list, show-cover vs episode-cover spec. |
| `motion.md` | The motion vocabulary — stepped/terminal, never eased. Cursor-blink spec (1.2s, steps(1)), one-blink-per-viewport rule, reduced-motion policy. |
| `accessibility.md` | Computed WCAG contrast for every text-on-background pair (18 pairs), decorative-only flagging, SC 1.4.11-compliant focus-ring spec. |
| `moodboard.html` | Open in a browser to see the system composed visually. |
| `applications.html` | The system rendered on 4 real surfaces — website hero, podcast cover, social post, email header. |
| `previews/` | Rendered PNGs of both HTML artifacts (1440px, headless Chrome) — shareable without a browser, and the visual record of each revision. Regenerate after any token change. |

## CSS architecture

One import chain, color tokens at the root:

```
palette.css  →  type.css  →  space.css  →  components.css
```

Link `components.css` and you get everything. Use `var(--token-name)` everywhere — never inline hex. (v1.0 shipped without `palette.css`, so the tokens documented in the README didn't actually exist in CSS. They do now.)

## Direction at a glance

- **Palette:** parchment + circuit-green + cobalt. Cool neutrals with one warm counterpoint (rose). Off-black ink, never pure black. **The green is one idea on two surfaces:** `signal` (#4ad295) on dark, `signal-deep` (#1a7a52) on light — never the bright one for text on parchment.
- **Type:** JetBrains Mono as display (mono-as-display, lab-notebook register, tracking capped at -0.02em to preserve the mono grid) + Manrope as body (humanist sans, recedes, **no italics** — Manrope has no italic cut; asides are set in mono).
- **Voice:** hypothesis-led, builder-specific, compressed, first-person plural, quietly ambitious. Episode titles are hypotheses phrased as questions.
- **Motion:** stepped, terminal-like, never eased. One blinking cursor per viewport.
- **Imagery:** workspace artifacts + threshold spaces + physical evidence of thinking. Never people facing camera, never SaaS-stock aesthetics.

## Sacred & forbidden

Inferred from the existing site. Adjust if the brief should override:

- **Sacred:** the *hallway conversations* thesis — intimacy + builder honesty. The brand exists to be the threshold space, not the keynote stage.
- **Forbidden:** corporate SaaS gloss, gradient meshes, smiling-stock-photo aesthetic, hustle-bro podcast register, "empower / unleash / journey" language.

## Accessibility result

✅ **4 colors safe for body text on ground:** ink, ink-soft, signal-deep, cobalt
✅ **Focus rings pass WCAG 2.2 SC 1.4.11** on both light (signal-deep, 4.7:1) and dark (signal, 9.4:1) surfaces
⚠ **2 decorative-only on ground:** signal (bright green), rose
⚠ **On dark surfaces, secondary text is `quiet`, never `ink-soft`** (3.5:1 fail)

See `accessibility.md` for the full 18-pair table.

## How to use this folder

**For designers:**
1. Open `moodboard.html` to see the system composed
2. Open `applications.html` to see it on real surfaces
3. Load `palette.json` into Figma variables / Tokens Studio — it's standard DTCG
4. Reference `imagery.md` when commissioning photography or generating reference images

**For engineers:**
1. Link `components.css` — it cascades the whole chain (`palette` → `type` → `space`)
2. Use the `var(--token-name)` references everywhere — never inline hex
3. Read `accessibility.md` before adding new color combinations
4. Read `logo.md` before re-rendering the wordmark anywhere — including the U+2019 apostrophe rule

**For the host writing copy:**
1. Read `tone.md` — especially the don't-say sentences, the episode-title convention, and the banned-words list
2. Use the 3 microcopy snippets verbatim where they fit; rewrite them when context shifts but stay in voice

## Changelog

**v1.1 — 2026-06-11**
- `signal-deep` re-derived **#2da775 → #1a7a52** so the working green passes body AA on parchment (4.7:1). The bright green is now explicitly dark-surface-only; the deep green owns light surfaces. All artifacts updated.
- Focus ring now actually passes SC 1.4.11 (was 1.7:1, rationalized in v1.0; now 4.7:1 light / 9.4:1 dark).
- Call-to-listen button re-specced: `ground` on `signal-deep` (was `ground` on `signal` at 1.7:1).
- **Added `palette.css`** — color tokens now exist in CSS (v1.0's engineer instructions referenced vars no file defined).
- **Added `components.css`** — links, buttons, chips, tags, full interactive states.
- **Added `motion.md`** — the cursor blink was shipping unspecced; now codified.
- `palette.json` converted to real W3C DTCG format.
- Neutral ramp smoothed (300/400 re-interpolated; temperature crossover documented); `quiet` unified with neutral-200.
- Typography: smart apostrophes (U+2019) specced and applied; mono tracking capped at -0.02em; italics removed (Manrope has no italic cut — `.aside` replaces them); clamp() middle terms now rem + vw for zoom accessibility; `.code` recolored to pass AA.
- Podcast cover meta text fixed (`ink-soft` on `ink` failed at 3.5:1 → `quiet` at 11.9:1).
- Logo: clear-space metric corrected (ascender, not cap-height); micro mark `f/` added for <24px; asset checklist added; unsanctioned superscript lockup retired.
- Drift swept: show-cover vs episode-cover contradiction resolved in `imagery.md`; materials list synced (12 chips); `--border-accent` and artifacts agree; placeholder nav labels replaced with in-world IA; hero scrim re-specced as ink gradient.
- Episode-title convention added to `tone.md`.

## What's NOT in this system (yet)

These are deferred — add later if needed:
- Dark-mode palette pair — and note: the evidence (terminal aesthetic, signal's 9.4:1 on ink, the cover art) suggests this brand may want to be **dark-first** with parchment as the "print mode." The two-green architecture is ready for it.
- Rendered logo assets (SVG wordmark/monogram/micro mark, favicon set, 3000×3000 cover template) — checklist in `logo.md`
- Audiogram / waveform / chapter-art spec — the most-used weekly surfaces for a podcast
- Iconography library (stroke weight, corner radius, line vs. filled)
- Email-safe inline-CSS templates (the email surface in `applications.html` uses CSS vars, which most clients strip)

If you need any of these, they're ~30 minutes of work each.
