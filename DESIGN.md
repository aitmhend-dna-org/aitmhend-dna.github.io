# Design system

The single source of truth for this site. `.cursorrules`, `.github/copilot-instructions.md`
and `CLAUDE.md` all point here — do not restate rules in them.

Every rule below is true of the shipped CSS. If you change the CSS, change this file
in the same commit. A rule nobody enforces is worse than no rule.

---

## Colour

The palette is warm earth tones. The important part is not the hues — it is that
**each hue has one role**, because the brand colours cannot legally carry text.

### By role

| Role | Token | Value | Use for |
|---|---|---|---|
| Text accent | `--accent-text` | `#94571B` | Links, nav, headings, any coloured text |
| Text accent, hover | `--accent-text-hover` | `#8F531A` | Hover state on the above |
| Solid fill | `--accent-solid` | `#8B4513` | Buttons and pills carrying white text |
| Decoration | `--primary-terracotta` | `#CD7F32` | Borders, rails, dividers, decorative fills |
| Decoration | `--accent-ochre` / `#D4A629` | | Gradients, rails — **never text** |
| Ink | `--primary-dark` | `#3E2723` | Headings and body ink |
| Ground | `--background` | `#FAF8F4` | Page background |

**The rule that matters:** `#CD7F32` scores 2.95:1 and `#D4A629` scores 2.12:1 against
the page ground. Both fail WCAG AA for text. They are decoration only. Text takes
`--accent-text`; white-on-colour takes `--accent-solid` (7.10:1).

Never introduce a colour by literal in HTML or CSS. Add a token or use an existing one.

### Blue

No blue in chrome, type or decoration. This is not because blue is ugly — it is because
a previous incarnation used stock blue gradients that read as generic.

Be aware of the trap that produced: constraining the whole site to one hue is itself the
most recognisable machine-generated look, and it briefly made the site *more* templated,
not less. The answer is role separation and typography, not more brown.

### Data visualisation

Charts and diagrams follow a **luminance-ordered** ramp, because with hue fixed to one
family only lightness separates series:

```
#8B4513  L = 0.098   burnt sienna
#CD7F32  L = 0.284   terracotta
#E2A36B  L = 0.434   warm sand
```

Two series take the ends of that ramp (3.27:1 in greyscale).

**Colour is never the only cue.** Every series also carries a non-colour identifier —
a dash pattern, a point marker, or a distinct border. This is required, not optional.

> Open question (issue #57): whether to license a small desaturated categorical set for
> data encoding only. Three or more series are weakly separated under the current
> constraint. Until that is decided, keep to the ramp above.

---

## Typography

| Role | Family | Notes |
|---|---|---|
| Reading | **Literata** | Body copy, prose. Drawn for long-form reading on screen |
| Chrome | **Archivo** | Headings, nav, buttons, TOC, table headers, kickers |
| Technical | **IBM Plex Mono** | Haplogroup notation, dates, identifiers |

The serif/grotesque split carries meaning: **what you read is Literata, what you
navigate by is Archivo.** Do not blur that.

- Load fonts with a `<link>` in `<head>`, never an `@import` (render-blocking).
- Always declare a real fallback stack. Three silent fallbacks to an unloaded `Lexend`
  shipped for months because nobody checked.
- Body: 17px / 1.7. Running prose gets `max-width: 72ch`.
- Headings use `text-wrap: balance`.
- **Headings are text.** Never `display: flex` on a heading — it turns a text node and a
  nested `<span>` into two side-by-side items, which broke the hero twice.

Do not use Inter or Space Grotesk. Both are strongly associated with machine-generated
layout, and using them together is a tell.

---

## Structure

- **One `<h1>` per page, inside `<main>`.** The header carries the site name as a link,
  identical on every page, so the brand persists as you navigate.
- Heading levels descend sequentially. No skips. Size headings with a class, never by
  picking a lower level for its default size.
- Every page: skip link → header → nav → breadcrumb (not on the homepage) → `<main>` → footer.
- One footer everywhere.

## Layout

- Container max-width 1200px.
- Grids use `minmax(0, 1fr)`, never bare `1fr` — `1fr` cannot shrink below min-content and
  will push the page sideways on a phone.
- Wide content (tables, diagrams) scrolls inside its own container. The body never scrolls
  horizontally, at any width down to 320px.
- Breakpoints: 1024px (rail/desktop), 768px (tablet), 640px (stacked).
- Content pages get a sticky TOC rail ≥1024px. Landing pages opt out with
  `data-reading-aids="off"`.

## Components

Only these exist. Do not invent variants without adding them here.

- `.card` — the content container. Not everything needs to be one.
- `.home-section-card` / `.home-section-lead` — homepage entries. **One lead, the rest
  quiet.** The lead carries the only accent rail on the page.
- `.btn` / `.btn-copper` / `.btn-outline` — min-height 44px. Buttons are not links: keep
  them out of any `.card a` colour rule.
- `.toc-card` — sticky rail on desktop, vertical list on mobile.
- `.page-title`, `.page-updated`, `.sourcing-note`.

Radius 3–8px. No pill shapes. Shadows subtle and rare — border, fill, radius and shadow
each say "separate object", so spend them by role rather than stamping every block.

---

## Content

- **Amazigh** first, "Berber" in parentheses on first mention.
- Haplogroups in full: `E-PF2546`, `H1-T16189C!`.
- Dates carry their range: "~11,400 years ago (range ~9,000–13,700)". A midpoint alone
  overstates the evidence.
- Hedge honestly — "approximately", "estimated", "debated". The genetics pages already
  do this well; hold everything else to that standard.
- **No emoji in headings.** 77 had to be removed.
- Cite at the point of assertion, with a DOI. Where content is not from published
  literature, say so — see the sourcing note on `culture.html`.
- Every page shows a visible "Last updated", matched to JSON-LD `dateModified` and
  `sitemap.xml`. "Updated", not "reviewed": the date reflects a file change, and
  "reviewed" would claim more.

## Accessibility

The floor, not the goal. Lighthouse mobile accessibility must be **100 with zero
failures** before merge.

- 4.5:1 for normal text, 3:1 for large. Check against the actual card ground, which is
  darker than the page ground.
- Visible focus on everything interactive.
- Touch targets ≥44px.
- Alt text on every image, with `width`/`height` to prevent layout shift.

## Performance

- Images: WebP, sized to roughly 2× their real CSS display width. No JPEG/PNG fallbacks —
  shipping both formats defeats the point.
- Photographs q82; maps and charts q90, since they carry fine text.
- Social images stay JPEG (`og-card.jpg`, 1200×630) — crawler support for WebP is uneven.
- The LCP image is eager, preloaded, `fetchpriority="high"`. `loading="lazy"` is for
  below-fold images only.
- No page ships more than ~600 KB of imagery.

## Working on this repo

No build step. Plain HTML, CSS and vanilla JS; edit and open in a browser. Deployment is
automatic from `main` via GitHub Pages.

Before opening a PR: run Lighthouse on the pages you touched, and check 390px for
horizontal overflow.
