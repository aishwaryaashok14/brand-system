---
name: brand-system
description: Generate a nuanced brand tone & design system — palette, typography, voice, and a reference-image moodboard — through short Q&A and three rendered visual directions. Use when the user wants to define a brand identity, build a moodboard, write a brand voice guide, or extract a design system for a new product/service/personal brand. Triggers on phrases like "build a brand system", "make a moodboard", "design a brand identity", "set up brand tokens", "define our voice", or "/brand-system".
---

# Brand System

Generate a complete brand tone & design system through short, focused Q&A and three rendered visual directions. Output is a `brand-system/` folder containing tokens, type, voice, imagery references, and a composed moodboard.

## Core Principles

1. **Show, Don't Tell** — Generate three rendered HTML moodboards, not abstract descriptions. People discover their brand by seeing it.
2. **Short Questions** — Batch all discovery into one `AskUserQuestion` call (max 4 questions). Never interrogate.
3. **Reference Collage, Not AI Slop** — Imagery is described as concrete reference scenes (subject, light, palette anchors). The user takes prompts to their own tool — we never auto-generate stock-looking visuals.
4. **Distinctive Direction** — Avoid generic indigo gradients, Inter-on-white, "modern minimal nothing." Every direction must commit to a point of view.
5. **Folder Deliverable** — Output is a `brand-system/` folder with portable artifacts (`palette.json`, `type.css`, `tone.md`, `imagery.md`, `moodboard.html`, `README.md`).

## Avoid the AI Slop Aesthetic

You drift toward safe defaults. In brand work this produces interchangeable, forgettable systems. Resist:

- **Fonts:** Inter, Roboto, Arial, system fonts as display
- **Palettes:** `#6366f1` indigo, purple-on-white gradients, "10 shades of grey + one pop"
- **Voice:** "Empower," "elevate," "seamless," "delight" — corporate filler
- **Imagery:** smiling stock people, isometric illustrations, generic gradient meshes
- **Layouts:** centered hero + 3-card grid + CTA — the SaaS template

Commit to a specific aesthetic with a clear cultural reference (editorial print, field manuals, riso zines, brutalist architecture, late-night radio, lab notebooks, etc.).

---

## Phase 0: Detect Mode

- **Mode A: New brand** — Define from scratch. Go to Phase 1.
- **Mode B: Refresh existing** — User has an existing brand they want to evolve. Run **Phase 1.5** on their current site/collateral before Phase 1, then frame Phase 1 around what should change.
- **Mode C: Extract from references** — User has reference images/links and wants the system reverse-engineered. Run **Phase 1.5** on the references, draft a single direction, skip Phase 2's three-way preview, and confirm before Phase 3.

If unclear, ask in one short question.

---

## Phase 1: Brand Discovery

**Ask all four questions in a single `AskUserQuestion` call.** Keep questions short — one sentence each.

**Question 1 — Context** (header: "Context"):
What is this brand for? Options: Product/SaaS / Service or agency / Personal/creator / Event or campaign

**Question 2 — Audience** (header: "Audience"):
Who is the primary audience? Options: Builders/operators / Creatives/designers / Executives/buyers / Everyday consumers

**Question 3 — Feeling** (header: "Feeling", multiSelect: true, max 2):
What should the audience feel? Options:
- Trusted/grounded — competent, calm, considered
- Energized/bold — assertive, fast, alive
- Curious/intelligent — exploratory, witty, sharp
- Warm/intimate — generous, human, slow

**Question 4 — Anchors** (header: "Anchors"):
How should we anchor direction? Options: I'll share references (URLs / images / PDFs) / Vibe only — surprise me / Avoid these brands (I'll name them) / Blank slate

After answers, ask in a single short message for the **brief**:
> "Quick brief — 4 lines max:
> 1. Brand name (or working name)
> 2. One sentence on what it does
> 3. One thing that's sacred (must keep) — or 'none'
> 4. One thing that's forbidden (don't go near) — or 'none'"

**If the user picked "I'll share references" or "Avoid these brands"**, after the brief ask one short follow-up:
> "Drop them in your next message — any mix of:
> - URLs (sites, articles, store pages)
> - Image paths or a folder path
> - PDF paths (brand decks, guidelines)
> - Brand names (I'll search and fetch)
> Mark each one as `[inspire]` (lean toward) or `[avoid]` (deliberately diverge from) if relevant."

Then go to **Phase 1.5**. Otherwise skip directly to Phase 2.

---

## Phase 1.5: Reference Ingestion

Runs whenever the user has shared references (Mode A with anchors, Mode B always, Mode C always).

### Step 1.5.1: Ingest each reference

| Reference | Tool | What to extract |
| --- | --- | --- |
| Live URL | `WebFetch` with prompt: "Extract: (1) any color hex codes in inline styles or class names, (2) all `font-family` declarations, (3) the hero/headline copy verbatim, (4) the navigation labels verbatim, (5) what the brand calls itself in the first 200 words." | Palette signals, type signals, voice signals, self-description |
| Image file or folder | `Read` (multimodal) | 2-3 line description per image: dominant colors (with hex guesses), type style if any, mood, materials/textures shown, lighting. Mark **usable** or **not usable** with reason. |
| PDF (deck, guidelines) | `Read` with `pages` arg (≤20 pages per call; chunk if larger) | Same as image scan, page by page. Pull palette specs and type specs verbatim if listed. |
| Brand name only (no URL) | `WebSearch` for the brand's official site → `WebFetch` the homepage | Same as Live URL |

Process references in parallel where possible (multiple `WebFetch` / `Read` calls in one message).

**WebFetch CSS-blindness fallback.** WebFetch returns markdown-converted HTML — it cannot see linked stylesheets. Modern sites (Webflow, Framer, Next.js, Tailwind) ship their real palette and type in external CSS that WebFetch will never load. After the WebFetch result returns, count the hex codes and `font-family` declarations actually extracted.

If both are zero (or near-zero — fewer than 2 hex codes AND zero explicit `font-family` declarations), surface the limitation immediately to the user with one short message:

> "I couldn't read the site's palette or type — those live in external stylesheets I can't fetch. Two options:
> 1. Drop a screenshot of the homepage in your next message and I'll extract palette/type from the rendered pixels.
> 2. Skip the visual signals — I'll build the digest from voice and positioning only, and the three directions will lean on the brand's *essence* rather than its current site."

Wait for the user's choice before proceeding. If they pick option 1, ingest the screenshot via `Read` (multimodal) the same way the table above describes for image references. If option 2, mark the digest's palette/type sections as `(no visual signals — direction will design these from scratch)`.

Never silently produce a thin digest. The user must know what's missing.

### Step 1.5.2: Build the reference digest

Synthesize a compact digest. Keep it ≤30 lines total. Format:

```markdown
## Reference Digest

### Palette signals
- {hex}, {hex}, {hex} — from {source}
- {hex}, {hex} — from {source}
- (cross-cut) Common across refs: {warm earthy tones / cool muted / high-contrast b&w / etc.}

### Type signals
- Display: {font name(s) seen} — {context}
- Body: {font name(s) seen} — {context}
- (cross-cut) Style trend: {humanist serif / wide grotesk / mono-as-display / etc.}

### Voice signals
- Sample: "{verbatim line}" — {source}
- Sample: "{verbatim line}" — {source}
- (cross-cut) Register: {imperative / conversational / academic / playful}, sentence length: {short / long / mixed}

### Mood / material signals
- {1-3 lines naming materials, light, environments seen}

### [Inspire] anchors → {1-line direction this pulls toward}
### [Avoid] anchors → {1-line direction this pushes away from}
```

### Step 1.5.3: Confirm before Phase 2

Show the digest and ask in one `AskUserQuestion` call (header: "Digest"):
"Does this read of your references match your gut?"
- "Yes, proceed to directions" (recommended)
- "Adjust the digest" (user clarifies what's off)
- "I want to add more references"

Only proceed to Phase 2 once confirmed.

### Step 1.5.4: How the digest shapes Phase 2

- **Mode A (new brand with anchors):** Direction A pulls toward [inspire] signals. Direction B is a controlled departure (same feeling, different visual language). Direction C is a deliberate counter — what the brand could be if it broke from the references.
- **Mode B (refresh existing):** Direction A is "tighten what you have." Direction B is "evolve" (~30% shift). Direction C is "reset" (different visual language, same audience).
- **Mode C (extract):** Skip three previews. Generate one direction directly from the digest, render as a single moodboard preview, confirm, then go to Phase 3.

**[Avoid] signals are bans.** No direction may reuse the [avoid] palette anchors, fonts, or voice register.

---

## Phase 2: Direction Discovery (Show, Don't Tell)

Generate **three distinct moodboard directions** rendered as standalone HTML. Each direction commits to a real point of view — they should feel like work from three different studios, not three sliders on the same theme.

### Step 2.1: Pick three directions

Read [TONE_PRESETS.md](TONE_PRESETS.md). Map the user's feeling(s) to candidate presets:

| Feeling | Candidate presets |
| --- | --- |
| Trusted/grounded | Quiet Editorial, Soft Industrial, Saltwater Modern, Heritage Atelier |
| Energized/bold | Field Manual, Late Night Diner, Risograph Studio, Botanical Brutalism |
| Curious/intelligent | Cosmic Lab, Galaxy Brain, Quiet Editorial, Field Manual |
| Warm/intimate | Late Night Diner, Risograph Studio, Heritage Atelier, Soft Industrial |

Pick three that are **maximally different from each other** within the chosen feeling — not three variations of the same idea. If the user combined two feelings, pull one direction from each candidate set plus one "wildcard" that surprises.

You may also compose a fresh direction from scratch when no preset fits. Do not feel bound to the list — the presets are starting points, not menu items.

**If a Phase 1.5 reference digest exists**, it overrides the table above. Use the rules from §1.5.4 to pick the three directions (lean / depart / counter — or tighten / evolve / reset for refresh mode). Honor every `[avoid]` ban: no direction reuses banned palette anchors, fonts, or voice register.

### Step 2.2: Generate three preview HTML files

Save to `.claude-design/brand-previews/`:
- `direction-a.html`
- `direction-b.html`
- `direction-c.html`

Each preview is a single-page HTML moodboard. **Read [moodboard-base.css](moodboard-base.css) and include its full contents in every preview's `<style>` block.**

Each moodboard must contain, in this order:

1. **Masthead** — direction name + 4-6 word tagline + brand name (the working name from the brief)
2. **Palette strip** — 5-7 swatches with hex labels and semantic names (e.g., "Ink", "Ash", "Signal", "Bone")
3. **Typography specimen** — display word in display font (~6rem) + paragraph in body font (3-4 lines)
4. **Voice sample** — one tagline (display font) + 2-3 short body lines that read like real product copy (not lorem ipsum, not corporate filler)
5. **Imagery references** — 4-6 cards. Each card contains a **short text-described reference scene**, not a generated image. Format: `subject — lighting — material/palette anchor`. Examples:
   - "Concrete loading bay at 6am — overcast, blue hour edge — wet asphalt, sodium streetlight"
   - "Hands kneading rye dough — overhead window light — flour-dusted oak, linen apron"
   - "Lab notebook half-open — desk lamp from left — graphite, Manila card, copper coil"
   - The card itself is a CSS-styled rectangle with the description inside, plus a thin colored bar tying it to the palette. **No image generation, no stock photos.**
6. **Texture/material descriptors** — 5-7 short phrases as a chip/pill row (e.g., "matte clay", "raw kraft", "wet glass", "warm tungsten", "graphite on bond")
7. **Footer** — preset name + small "Direction A/B/C" badge

Use fonts from Fontshare or Google Fonts — never system fonts. Each preview should be ~150-300 lines of HTML.

### Step 2.3: Open all three

Open all three previews automatically:
```bash
open .claude-design/brand-previews/direction-a.html .claude-design/brand-previews/direction-b.html .claude-design/brand-previews/direction-c.html
```

### Step 2.4: Picker

Ask in a single `AskUserQuestion` call (header: "Pick"):
"Which direction feels right?" Options:
- A: [name from preset]
- B: [name from preset]
- C: [name from preset]
- Mix elements (I'll specify)

If the user picks "Mix elements," ask one short follow-up: "Which palette + which type + which imagery direction? (e.g., 'A's palette, B's type, C's imagery')."

---

## Phase 3: Generate brand-system/ Folder

Read [OUTPUT_FORMAT.md](OUTPUT_FORMAT.md) for the complete folder spec.

Create the folder at the user's current working directory unless they specify otherwise. Default path: `./brand-system/`.

Required artifacts (every file uses the chosen direction):

| File | Purpose |
| --- | --- |
| `README.md` | Index: what this is, what each file is for, how to use |
| `palette.json` | Semantic color tokens with hex + role notes + neutral scale |
| `type.css` | `@import` for fonts + CSS custom properties for type scale + ready-to-paste `.display`, `.h1-h6`, `.body`, `.caption` classes |
| `space.css` | Spacing scale (8-10 step `clamp()`-based), layout primitives (`.container`, `.stack`), radius tokens, sparing shadow tokens |
| `logo.md` | Wordmark spec: lockup, clear-space, minimum size, monogram fallback, color usage, don'ts |
| `tone.md` | Voice attributes, "we are / we are not" pairs, 10 do + 10 don't sentences with reasons, 3 microcopy snippets, banned-words list |
| `imagery.md` | Imagery system: subject buckets, lighting rules, palette anchors, materials, **8-10 ready-to-paste reference prompts**, and "do not depict" rules |
| `accessibility.md` | WCAG contrast report — every text-on-background combination computed, AA/AAA flagged, decorative-only colors marked |
| `moodboard.html` | Polished standalone moodboard combining all of the above. Self-contained, includes [moodboard-base.css](moodboard-base.css). |
| `applications.html` | Single page rendering the system on 4 real surfaces — website hero, podcast cover / 1:1 art, social post, email header — using only system tokens. Proves the system composes. |

**Quality bar:**
- Every choice must trace back to the brief. If you can't justify a token, cut it.
- Voice samples must read like actual product copy in the brand's domain — not generic.
- Reference prompts must be specific (subject + light + material). Vague prompts like "a person using the app" are rejected.
- Palette must include at least one signal/accent color with real personality — not "blue".
- **Accessibility is non-negotiable:** compute contrast ratios for every text-on-background pair before delivery. Any decorative-only color (one that fails AA on the page background) must be flagged in `accessibility.md` with a "never use for text" rule.
- **Applications must use only system tokens.** No inline hex codes, no fonts outside the chosen pair, no spacing values outside `--space-*`. If a surface needs something the tokens don't provide, the system is incomplete — extend the tokens, don't bypass them.

---

## Phase 4: Deliver

1. **Clean up** previews: `rm -rf .claude-design/brand-previews/`
2. **Open the deliverables**: `open ./brand-system/moodboard.html ./brand-system/applications.html`
3. **Summarize** in 5-7 lines:
   - Folder location, direction name, token count, accessibility result (`X passes AA, Y decorative-only`)
   - One-line description of the voice
   - One concrete next step (e.g., "drop `palette.json` into your design tool / paste prompts from `imagery.md` into your image-gen tool / use `applications.html` mockups as references for your dev team")
   - How to evolve: "Edit any token file then re-run /brand-system → Refine to rebuild the moodboard and applications"

---

## Phase 5: Iterate (Optional)

If the user wants to refine, ask one short question (header: "Refine"):
"What should change?" Options:
- Tighten palette (swap or remove colors)
- Shift type (different display or body)
- Sharpen voice (more X / less Y)
- Expand imagery (more reference prompts)
- Adjust spacing or radius (tighter / looser / sharper / softer)
- Tune logo lockup (clear space, minimum size, monogram)

Make the change, regenerate only the affected file(s), update `moodboard.html` AND `applications.html`, re-run the contrast check, re-open.

---

## Supporting Files

| File | Purpose | When to Read |
| --- | --- | --- |
| [TONE_PRESETS.md](TONE_PRESETS.md) | 10 curated brand directions with palette, type, voice, imagery cues | Phase 2 (direction picking) |
| [moodboard-base.css](moodboard-base.css) | Mandatory CSS for moodboard previews — include in full | Phase 2 + Phase 3 (HTML generation) |
| [OUTPUT_FORMAT.md](OUTPUT_FORMAT.md) | Schema + examples for every file in the `brand-system/` folder | Phase 3 (folder generation) |

---

## Known Limitations

These are real, named, and intentionally unsolved. Be transparent about them when they bite, don't pretend they aren't there.

### 1. WebFetch can't read external stylesheets
The `WebFetch` tool converts HTML to markdown — it never loads linked CSS. Most modern sites (Webflow, Framer, Next.js, Tailwind builds) keep their real palette hex codes and `font-family` declarations in external stylesheets, which means Phase 1.5 ingestion produces a thin palette/type signal for those sites. **Mitigation:** Step 1.5.1's screenshot fallback. When extraction returns near-zero visual signals, ask the user for a homepage screenshot and ingest via `Read` (multimodal) instead.

### 2. `applications.html` token values are a snapshot
The generated `applications.html` inlines its color/spacing/font tokens at the top of the `<style>` block rather than `@import`-ing `space.css`. This is deliberate — the file must work when double-clicked from a file manager (some browsers refuse cross-origin `@import` from `file://`). The cost: if a token is later edited in `palette.json` or `space.css`, `applications.html` won't auto-update. **Mitigation:** Every generated `applications.html` includes a header comment naming itself a snapshot, and Phase 5 (Iterate) regenerates BOTH HTML files whenever tokens change. The duplication is a snapshot, not a fork.

### 3. `tone.md` domain specificity is model-dependent
The "Do say" / "Don't say" sentences are supposed to read like real product copy in the brand's domain (podcast, SaaS, agency, DTC, etc.). Today this works because the model picks up domain context from the brief and reference digest. There's no quality gate enforcing it. If a generated `tone.md` feels generic — full of "In this episode…" or "Our customers…" sentences that don't anchor on the actual brand — the brief was likely thin. **Mitigation:** Re-run Phase 1 with more domain-specific anchors in Question 4 ("references to share"), and consider adding 2-3 verbatim copy examples from real comparable brands in the user's space. A formal quality-gate check against domain vocabulary may be added in v2 if this fails frequently in practice.

---

## Anti-Patterns (Reject on Sight)

- Generating images instead of describing reference scenes
- Asking more than 4 questions in discovery (batch into one `AskUserQuestion`)
- Showing one direction instead of three (kills "show, don't tell")
- Using system fonts or Inter/Roboto in any preview
- Voice samples that say "empower," "elevate," "seamless," "delight," "unleash"
- Palette with no signal color — just neutrals + one safe accent
- Imagery prompts shorter than `subject — lighting — material` triplets
- Missing the brand name from the brief in any artifact
- **Skipping Phase 1.5 when references were shared** — never just glance at a URL string; fetch it
- **Reusing `[avoid]` signals** — if the user said "not like Stripe," no direction may use Stripe's palette anchors, type pair, or voice register
- **Skipping the digest confirmation step** — always show the digest before generating directions; user must accept or adjust
- **Shipping a folder without `accessibility.md`** — the contrast check is a hard gate, not a nice-to-have
- **Inline hex codes in `applications.html`** — every color/font/space must trace to a token. Inline values mean the system isn't composable
- **Logo specced only as "set in the display font"** — no clear-space, no minimum size, no monogram fallback is incomplete. Edge cases (favicon, profile pic, embed) need rules
- **Skipping the spacing scale** — without `--space-*` tokens, `palette.json` and `type.css` cannot compose into UI
