#!/usr/bin/env python3
"""
Generate a brand's reference moodboard with Gemini (Nano Banana Pro) and
compose the frames into one on-brand grid poster.

This is a GENERAL tool for the brand-system skill: it reads the brand name,
palette, and image prompts from whatever output folder the skill produced
(palette.json + imagery.md). Nothing here is specific to any one brand.

Usage:
    python3 generate_moodboard.py [BRAND_DIR] [N] [--grid-only]

    BRAND_DIR    folder containing palette.json + imagery.md
                 (default: auto-detect ./ or ./brand-system)
    N            generate only the first N frames (cheap test pass)
    --grid-only  recompose the grid from existing frames, no API calls

Examples:
    python3 generate_moodboard.py                 # all frames + grid, auto-detect brand
    python3 generate_moodboard.py ./brand-system  # point at a specific brand folder
    python3 generate_moodboard.py 2               # first 2 frames only (validate the look)
    python3 generate_moodboard.py --grid-only     # re-stitch grid without paying for the API

Key is read from .env (GEMINI_API_KEY=...), then $GEMINI_API_KEY, then .gemini_key.
"""

import os
import re
import sys
import json
import pathlib

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = pathlib.Path(__file__).resolve().parent

# ── Generation settings ──────────────────────────────────────────────
MODEL = "gemini-3-pro-image-preview"   # Nano Banana Pro
ASPECT = "1:1"                          # square tiles read cleanly in a grid
RESOLUTION = "2K"                       # "1K" = faster/cheaper test, "2K" = final, "4K" = max

# Shared photographic treatment appended to EVERY prompt — this is what makes
# N separate scenes read as ONE visual language. The brand's own ground/ink/
# signal hexes are injected at runtime so the whole set stays anchored to the
# palette. Per-scene materials and lighting come from imagery.md's prompts.
HOUSE_STYLE_TMPL = (
    "Shot as an editorial reference photograph, documentary register, not a stock photo. "
    "One dominant light source — no flash, no ring light, no glamour glow. "
    "Muted, desaturated film grade, fine grain, gentle vignette, shallow-to-medium depth of field. "
    "Anchor the whole palette to {ground} (light) and {ink} (dark/neutral), with a SINGLE "
    "restrained accent of {signal} — never any other saturated color. Tactile and slightly imperfect. "
    "No people facing the camera, no faces, no readable text, no logos, no captions, no watermark-like marks."
)

# ── Grid layout ──────────────────────────────────────────────────────
COLS, ROWS = 4, 3          # 12 cells: up to 10 photos + palette tile + monogram tile
TILE = 560
GUT = 18
MARGIN = 72
HEADER_H = 210
FOOTER_H = 96
STOPWORDS = {"the", "a", "an", "of", "and", "for", "to", "&", "with", "by"}


# ── small color helpers ──────────────────────────────────────────────
def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb


def lum(rgb):
    return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]


def sat(rgb):
    return max(rgb) - min(rgb)


def blend(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def on(rgb, light, dark):
    """Pick readable text color for a swatch background."""
    return dark if lum(rgb) > 140 else light


# ── fonts (brand display is typically a mono; Menlo stands in locally) ──
def _font(size, bold=False):
    candidates = [
        (str((pathlib.Path.home() / ("Library/Fonts/JetBrainsMono-Bold.ttf" if bold
              else "Library/Fonts/JetBrainsMono-Regular.ttf"))), 0),
        ("/Library/Fonts/JetBrainsMono-Bold.ttf" if bold else "/Library/Fonts/JetBrainsMono-Regular.ttf", 0),
        ("/System/Library/Fonts/Menlo.ttc", 1 if bold else 0),
        ("/System/Library/Fonts/Supplemental/Andale Mono.ttf", 0),
        ("/System/Library/Fonts/Monaco.ttf", 0),
    ]
    for path, idx in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size, index=idx)
            except Exception:
                continue
    return ImageFont.load_default()


def fit_font(draw, text, max_w, start, bold=False, floor=20):
    size = start
    while size > floor:
        f = _font(size, bold=bold)
        if draw.textbbox((0, 0), text, font=f)[2] <= max_w:
            return f
        size -= 2
    return _font(floor, bold=bold)


# ── brand data (read from palette.json) ──────────────────────────────
def _val(node):
    if isinstance(node, dict):
        return node.get("$value", node.get("value"))
    return node


def load_brand(brand_dir):
    palette = json.loads((brand_dir / "palette.json").read_text())
    colors = {}
    for name, node in palette.get("color", {}).items():
        v = _val(node)
        if isinstance(v, str) and v.startswith("#"):
            colors[name] = hex_to_rgb(v)
    if not colors:
        sys.exit("No color tokens found in palette.json")

    def pick(role, fallback):
        return colors.get(role, fallback())

    ground = pick("ground", lambda: max(colors.values(), key=lum))
    ink = pick("ink", lambda: min(colors.values(), key=lum))
    signal = pick("signal", lambda: max(
        (c for n, c in colors.items() if n not in ("ground", "ink")), key=sat, default=ground))

    brand = palette.get("brand", {})
    name = _val(brand.get("name")) or brand_dir.name
    direction = _val(brand.get("direction")) or "Reference moodboard"
    version = _val(brand.get("version")) or "1.0"

    return {
        "name": name, "direction": direction, "version": version,
        "colors": colors, "ground": ground, "ink": ink, "signal": signal,
    }


def monogram(name):
    words = [w for w in re.split(r"[\s\-]+", name) if w.strip("'\".") and w.lower() not in STOPWORDS]
    if len(words) >= 2:
        return "".join(w[0] for w in words[:3]).upper()
    base = re.sub(r"[^A-Za-z]", "", name) or name
    return base[:2].upper()


# ── prompts (read from imagery.md) ───────────────────────────────────
def parse_prompts(brand_dir):
    text = (brand_dir / "imagery.md").read_text()
    m = re.search(r"## Reference prompts.*?\n(.*?)(?:\n## |\Z)", text, re.S)
    body = m.group(1) if m else text
    out = []
    for line in body.splitlines():
        lm = re.match(r"\s*\d+\.\s+(.*\S)", line)
        if lm:
            out.append(lm.group(1).replace("**", "").strip())
    return out


def slug(prompt, i):
    title = re.split(r"\s+[—-]\s+", prompt)[0]
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return f"{i + 1:02d}-{s or 'frame'}"


# ── locate brand folder + key ────────────────────────────────────────
def find_brand_dir(explicit):
    if explicit:
        p = pathlib.Path(explicit).resolve()
        if not (p / "palette.json").exists():
            sys.exit(f"{p} has no palette.json")
        return p
    for cand in (pathlib.Path.cwd(), pathlib.Path.cwd() / "brand-system", HERE / "brand-system"):
        if (cand / "palette.json").exists() and (cand / "imagery.md").exists():
            return cand.resolve()
    sys.exit("Could not find a brand folder (palette.json + imagery.md). Pass the path explicitly.")


def load_key():
    for var in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        if os.environ.get(var):
            return os.environ[var]
    for base in (pathlib.Path.cwd(), HERE):
        env = base / ".env"
        if env.exists():
            for line in env.read_text().splitlines():
                line = line.strip()
                if line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() in ("GEMINI_API_KEY", "GOOGLE_API_KEY") and v.strip():
                    return v.strip().strip('"').strip("'")
        kf = base / ".gemini_key"
        if kf.exists() and kf.read_text().strip():
            return kf.read_text().strip()
    return None


# ── generation ───────────────────────────────────────────────────────
def generate(brand, prompts, frames_dir, limit=None):
    from google import genai
    from google.genai import types

    key = load_key()
    if not key:
        sys.exit("No API key. Add GEMINI_API_KEY=... to .env (see that file's comments).")

    client = genai.Client(api_key=key)
    frames_dir.mkdir(parents=True, exist_ok=True)
    house = HOUSE_STYLE_TMPL.format(
        ground=rgb_to_hex(brand["ground"]),
        ink=rgb_to_hex(brand["ink"]),
        signal=rgb_to_hex(brand["signal"]),
    )

    todo = prompts[:limit] if limit else prompts
    print(f"Brand: {brand['name']}  |  {len(todo)} frame(s) @ {RESOLUTION} {ASPECT}  |  {MODEL}\n")

    for i, prompt in enumerate(todo):
        name = slug(prompt, i)
        dest = frames_dir / f"{name}.jpg"
        print(f"  [{i + 1:02d}/{len(todo)}] {name} … ", end="", flush=True)
        try:
            resp = client.models.generate_content(
                model=MODEL,
                contents=[f"{prompt}. {house}"],
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT", "IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio=ASPECT, image_size=RESOLUTION),
                ),
            )
            saved = False
            for part in resp.parts:
                if getattr(part, "inline_data", None):
                    part.as_image().save(dest, "JPEG", quality=95)
                    saved = True
                    break
            print("ok" if saved else "no image returned")
        except Exception as e:
            print(f"FAILED: {e}")


# ── tiles ────────────────────────────────────────────────────────────
def photo_tile(path, border):
    img = Image.open(path).convert("RGB")
    tile = ImageOps.fit(img, (TILE, TILE), Image.LANCZOS, centering=(0.5, 0.5))
    ImageDraw.Draw(tile).rectangle([0, 0, TILE - 1, TILE - 1], outline=border, width=1)
    return tile


def palette_tile(brand):
    tile = Image.new("RGB", (TILE, TILE), blend(brand["ink"], brand["ground"], 0.08))
    d = ImageDraw.Draw(tile)
    pad = 28
    d.text((pad, pad - 4), "PALETTE", font=_font(22, bold=True),
           fill=blend(brand["ground"], brand["ink"], 0.15))
    top = pad + 34
    items = list(brand["colors"].items())
    bar_h = (TILE - top - pad) // max(len(items), 1)
    lf = _font(20)
    for k, (nm, rgb) in enumerate(items):
        y0 = top + k * bar_h
        d.rectangle([pad, y0, TILE - pad, y0 + bar_h - 6], fill=rgb)
        d.text((pad + 14, y0 + (bar_h - 6) // 2 - 11), f"{nm}  {rgb_to_hex(rgb)}",
               font=lf, fill=on(rgb, brand["ground"], brand["ink"]))
    return tile


def monogram_tile(brand):
    tile = Image.new("RGB", (TILE, TILE), brand["ink"])
    d = ImageDraw.Draw(tile)
    d.rectangle([28, 28, 98, 34], fill=brand["signal"])
    mark = monogram(brand["name"])
    mono = fit_font(d, mark, TILE - 120, 220, bold=True, floor=80)
    bb = d.textbbox((0, 0), mark, font=mono)
    d.text(((TILE - (bb[2] - bb[0])) / 2 - bb[0], (TILE - (bb[3] - bb[1])) / 2 - bb[1] - 18),
           mark, font=mono, fill=brand["signal"])
    cap = brand["direction"].upper()
    cf = fit_font(d, cap, TILE - 56, 22, bold=True, floor=14)
    cb = d.textbbox((0, 0), cap, font=cf)
    d.text(((TILE - (cb[2] - cb[0])) / 2, TILE - 70), cap, font=cf,
           fill=blend(brand["ground"], brand["ink"], 0.2))
    return tile


# ── grid composition ─────────────────────────────────────────────────
def compose(brand, frames_dir, final_path):
    frame_files = sorted(frames_dir.glob("*.jpg")) if frames_dir.exists() else []
    if not frame_files:
        sys.exit(f"No frames in {frames_dir} — run generation first.")

    ink, ground, signal = brand["ink"], brand["ground"], brand["signal"]
    muted = blend(ground, ink, 0.45)
    hairline = blend(ink, ground, 0.18)

    canvas_w = MARGIN * 2 + COLS * TILE + (COLS - 1) * GUT
    canvas_h = MARGIN * 2 + HEADER_H + ROWS * TILE + (ROWS - 1) * GUT + FOOTER_H
    canvas = Image.new("RGB", (canvas_w, canvas_h), ink)
    d = ImageDraw.Draw(canvas)
    content_w = canvas_w - MARGIN * 2

    # header
    d.rectangle([MARGIN, MARGIN, MARGIN + 70, MARGIN + 7], fill=signal)
    wm = brand["name"].upper()
    d.text((MARGIN, MARGIN + 26), wm, font=fit_font(d, wm, content_w, 58, bold=True, floor=30), fill=ground)
    d.text((MARGIN, MARGIN + 104),
           f"Reference moodboard · {brand['direction']} · v{brand['version']}",
           font=_font(24), fill=muted)
    rule_y = MARGIN + HEADER_H - 24
    d.rectangle([MARGIN, rule_y, MARGIN + content_w, rule_y + 3], fill=signal)

    # tiles: photos, then palette, then monogram
    grid_top = MARGIN + HEADER_H
    tiles = [photo_tile(f, hairline) for f in frame_files[:10]]
    tiles.append(palette_tile(brand))
    tiles.append(monogram_tile(brand))
    for cell, tile in enumerate(tiles[: COLS * ROWS]):
        r, c = divmod(cell, COLS)
        canvas.paste(tile, (MARGIN + c * (TILE + GUT), grid_top + r * (TILE + GUT)))

    # footer
    fy = grid_top + ROWS * TILE + (ROWS - 1) * GUT + 40
    d.rectangle([MARGIN, fy, MARGIN + content_w, fy + 1], fill=hairline)
    foot = _font(20)
    d.text((MARGIN, fy + 18), f"{len(frame_files[:10])} reference frames · one visual language",
           font=foot, fill=muted)
    right = "Gemini · Nano Banana Pro"
    rb = d.textbbox((0, 0), right, font=foot)
    d.text((MARGIN + content_w - (rb[2] - rb[0]), fy + 18), right, font=foot, fill=muted)

    final_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(final_path, "JPEG", quality=94)
    print(f"\nComposed grid → {final_path}  ({canvas_w}×{canvas_h})")


# ── entry ────────────────────────────────────────────────────────────
def main():
    args = sys.argv[1:]
    grid_only = "--grid-only" in args
    rest = [a for a in args if a != "--grid-only"]
    limit = next((int(a) for a in rest if a.isdigit()), None)
    path_arg = next((a for a in rest if not a.isdigit()), None)

    brand_dir = find_brand_dir(path_arg)
    out = brand_dir / "moodboard-images"
    frames = out / "frames"
    final = out / "moodboard-final.jpg"

    brand = load_brand(brand_dir)
    prompts = parse_prompts(brand_dir)
    if not prompts:
        sys.exit(f"No prompts parsed from {brand_dir / 'imagery.md'}")

    if not grid_only:
        generate(brand, prompts, frames, limit=limit)
    compose(brand, frames, final)


if __name__ == "__main__":
    main()
