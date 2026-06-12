# Wordmark — The Founder's Foyer

## Primary lockup

The wordmark sets **the founder’s foyer** in lowercase **JetBrains Mono 700** at **-0.02em** letter-spacing. Lowercase is intentional — it matches the direction's quiet, lab-notebook register. Uppercase or title-case versions are off-system.

Tracking is a whisper, not a squeeze: JetBrains Mono is monospaced, and its fixed advance width is the point. Tighter than -0.02em breaks the grid and causes glyph collisions at display sizes.

**The apostrophe is U+2019 (’), the typographic right single quote — never the typewriter apostrophe (').** This brand's register is precision; a dumb quote in the wordmark is a typo on the cover.

**HTML:**
```html
<span class="wordmark">the founder&rsquo;s foyer</span>
```

**CSS:**
```css
.wordmark {
    font-family: var(--font-display);   /* JetBrains Mono */
    font-weight: 700;
    letter-spacing: -0.02em;
    color: var(--ink);
    text-transform: lowercase;
}
```

## Clear space

Minimum clear space around the wordmark = **the ascender height of the lowercase ‘f’ (≈0.75× of the type size)** on all four sides. (Lowercase letters don't have a cap-height; the ‘f’ ascender is the tallest stroke in the mark.) No element may cross this boundary. When in doubt, give it more room — this is a quiet brand.

```
┌──────────────────────────────────────────┐
│           ↑ f-ascender                   │
│ ←  the founder’s foyer  →                │
│           ↓ f-ascender                   │
└──────────────────────────────────────────┘
```

## Minimum size

| Context | Minimum height |
| --- | --- |
| Digital | 14px (use larger when possible) |
| Print | 10pt |
| Below minimum | Use the **monogram** (≥24px) or **micro mark** (<24px) |

Below 14px the lowercase mono becomes hard to scan — it stops reading as a wordmark and starts reading as filename text. Switch to the monogram.

## Monogram (icon fallback, ≥24px)

**Glyph:** `tff/`

The trailing slash is intentional — it's a path notation borrowed from URLs and lab-notebook section markers. It signals "you are entering" — same gesture as the foyer metaphor. Set in JetBrains Mono 800.

**Used in:**
- Podcast platform icons (Spotify, Apple Podcasts, YouTube)
- Social media profile pictures
- App tile / home-screen icons
- Anywhere the full wordmark drops below minimum size and the canvas is ≥24px

## Micro mark (<24px)

**Glyph:** `f/`

Four glyphs in a 16px favicon is mush. Below 24px — favicons at 16×16, browser-tab scale, tiny avatars — the monogram drops to two glyphs: the brand's initial plus the threshold slash. Same construction rules as the monogram.

| Canvas | Mark |
| --- | --- |
| ≥24px | `tff/` |
| <24px (16×16 favicon, etc.) | `f/` |

**Construction (monogram and micro mark):**
- Background: `var(--ground)` — parchment
- Text: `var(--ink)` — off-black
- Optical centering: shift glyph slightly up and left to compensate for trailing-slash whitespace
- No border, no shadow, no inner stroke

**Reverse (dark backgrounds):**
- Background: `var(--ink)`
- Text: `var(--ground)`

## Color usage

| Combination | Use case |
| --- | --- |
| `ink` on `ground` | Primary — default light context |
| `ground` on `ink` | Reverse — dark backgrounds, dark mode |
| `ink` on `quiet` | Muted contexts — newsletter sidebar, footer |
| `ground` on `signal-deep` | Reserved — only on the call-to-listen button (4.7:1, passes body AA) |
| Single-color print | `ink` only — never tint the wordmark |

**Never use** `signal` (bright circuit-green) as a wordmark color or as a fill behind the wordmark on light surfaces — `ground` on `signal` is 1.7:1, a catastrophic failure on the brand's most important button. The filled-green CTA uses `signal-deep` only. And never set the wordmark itself in either green; it reads as a system-status color, not a brand.

## Required assets (to produce)

The wordmark currently exists only as CSS-styled live text. These exports are required before the brand ships anywhere off-web:

- [ ] `wordmark.svg` (ink on transparent, text converted to outlines)
- [ ] `wordmark-reverse.svg` (ground on transparent)
- [ ] `monogram.svg` + `monogram-reverse.svg` (`tff/`)
- [ ] `micromark.svg` (`f/`) + favicon set (16, 32, 180, 512)
- [ ] Podcast cover template at **3000×3000** (Apple/Spotify require ≥1400×1400 raster; live text doesn't exist there)

## Don't

- Don't title-case or uppercase the wordmark — lowercase is part of the system
- Don't stretch, condense, or skew the type
- Don't apply drop shadows, glows, gradients, or outlines
- Don't rotate or place on a curve
- Don't add a tagline inline ("the founder’s foyer · podcast" — break it onto a second line if needed)
- Don't combine with other typefaces inline
- Don't attach superscripts, version numbers, or annotations to the wordmark — the annotated lockup in early moodboard drafts is retired
- Don't recolor the wordmark with any color outside the palette
- Don't place over a busy photograph without a solid `ground` or `ink` backplate
- Don't drop the apostrophe — it's "founder’s" (singular possessive), not "founders" or "founders’" — and don't set it as a straight quote

## The `/` slash in the monogram

The slash references:
1. **URLs** (`/foyer/episodes/`) — this is a digital-first brand
2. **Lab-notebook section markers** (`§ 1.2 / hypotheses`) — matches the direction's intellectual register
3. **The literal foyer/threshold** — a slash is a doorframe, edge, place-of-passing

If a designer or engineer needs to reproduce the monogram in another tool, this is the rationale to defend it — not aesthetic, structural.
