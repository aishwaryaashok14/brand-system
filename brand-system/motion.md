# Motion — The Founder's Foyer

Motion was already shipping in this system (the blinking cursor) before it was specced. This file makes it deliberate.

## Principle: motion is stepped, never eased

Terminals don't ease. The brand's motion vocabulary is binary — a thing is in one state, then it is in the other. No spring curves, no bounces, no fades longer than an eye blink. If a transition needs an easing curve to feel good, it doesn't belong in this system.

- **Allowed:** stepped animation (`steps(1)`), instant state changes, hard cuts
- **Forbidden:** ease-in-out anything, parallax, scroll-jacking, hover lifts/scales, skeleton shimmer

## The cursor blink — the one signature animation

```css
/* tokens (defined in space.css) */
--blink-duration: 1.2s;
--blink-timing:   steps(1);

@keyframes blink { 50% { opacity: 0; } }

.cursor::after {
    content: '_';
    color: var(--signal);        /* on dark surfaces */
    /* color: var(--signal-deep);   on light surfaces */
    animation: blink var(--blink-duration) var(--blink-timing) infinite;
}
```

**1.2s, square wave, 50% duty cycle.** This matches real terminal cursor cadence — faster reads as urgent, slower reads as broken. Do not change the duration per-surface; the blink is one heartbeat across the whole brand.

**Where it appears:** the primary CTA, the display-type cursor in the moodboard, episode-player "now playing" indicator. Nowhere else. One blinking thing per viewport, maximum — two cursors blinking out of phase reads as a bug.

## Reduced motion — non-negotiable

Every artifact must carry:

```css
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation: none !important; }
}
```

The cursor degrades to a solid `_` — still present, just not blinking. The brand survives entirely without motion; that's the test any new animation must also pass.

## If you add a new animation

1. Can it be expressed with `steps()`? If not, stop.
2. Does the artifact work with the animation removed? If not, stop.
3. Add it to this file with its duration and rationale.
