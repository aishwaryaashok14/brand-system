# Moodboard image generation (optional add-on)

By default the brand-system skill **describes** reference imagery as text prompts
(principle #3 — "Reference Collage, Not AI Slop") and hands you the prompts to use
in your own tool. This optional script closes that loop: it renders a brand's
prompts into real frames with Gemini (Nano Banana Pro) and composes them into one
on-brand grid poster.

It is **brand-agnostic** — it reads the brand name, palette, and prompts from
whatever output folder the skill produced. Nothing is hardcoded to any one brand.

## 1. One-time setup

```bash
python3 -m pip install google-genai pillow
```

Add your key to `.env` (gitignored — never committed):

```
GEMINI_API_KEY=AIza...your-key...
```

Get a key at https://aistudio.google.com/apikey

## 2. Run

```bash
# all frames + grid, auto-detecting the brand folder (./ or ./brand-system)
python3 generate_moodboard.py

# point at a specific brand output folder
python3 generate_moodboard.py ./brand-system

# cheap test: generate only the first 2 frames to validate the look
python3 generate_moodboard.py 2

# recompose the grid from existing frames — no API calls, no cost
python3 generate_moodboard.py --grid-only
```

## 3. Output

Written into `<brand-folder>/moodboard-images/`:

- `frames/NN-<slug>.jpg` — the individual reference frames (gitignored; regenerable)
- `moodboard-final.jpg` — the composed grid poster (10 frames + a palette tile +
  a monogram tile, framed on the brand's `ink`/`ground`/`signal` colors)

## How cohesion is enforced

Each prompt from `imagery.md` gets a shared "house style" suffix appended at
generation time — one light source, muted film grade, fine grain, and a single
accent drawn from the brand's own `signal` color, anchored to `ground` and `ink`.
That shared treatment is what makes ten separate scenes read as **one** visual
language instead of ten unrelated photos.

## Tuning

Edit the constants at the top of `generate_moodboard.py`:

- `RESOLUTION` — `"1K"` (fast/cheap test) · `"2K"` (default, final) · `"4K"` (max)
- `ASPECT` — `"1:1"` square tiles by default; any Gemini ratio works
- `COLS`, `ROWS`, `TILE`, `GUT` — grid shape and tile size
- `HOUSE_STYLE_TMPL` — the shared photographic treatment

## Notes

- All generated images carry Google's SynthID watermark.
- Gemini returns JPEG; frames are saved as `.jpg` accordingly.
- Cost scales with frame count × resolution. Use the `N` arg to test cheaply first.
