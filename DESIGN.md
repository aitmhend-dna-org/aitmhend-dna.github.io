# Design system

The single source of truth for this site. `.cursorrules`, `.github/copilot-instructions.md`
and `CLAUDE.md` all point here — do not restate rules in them.

Every rule below is true of the shipped CSS. If you change the CSS, change this file
in the same commit. A rule nobody enforces is worse than no rule.

---

## What this site is trying to be

A bright, flat, poster-like site about one Amazigh family's deep ancestry, built for
readers who are curious but not academic — teenagers and young adults first, specialists
second. The evidence is scholarly. The presentation is not.

The previous system failed on this point in a specific, diagnosable way: one hue
(warm brown) across every surface, a reading serif at every size, and a uniform grid
of equal cards. That is the visual signature of a generated document, and it read as a
journal paper. The corrective is not a different single hue. It is **four colours with
real hue separation, a hard split between display and reading type, and blocks of
deliberately unequal weight.**

---

## Colour

The palette is the **Amazigh flag** — sea blue, mountain green, sand yellow, and the
red of the yaz (ⵣ) — on bright paper with near-black ink.

This is not decoration borrowed from somewhere else. These are the colours the subject
of the site already uses to identify itself, which is why the palette is allowed to be
loud: it is not a mood, it is a flag.

### Tokens

| Role | Token | Value | Contrast |
|---|---|---|---|
| Paper | `--paper` | `#FFFCF5` | ground |
| On colour | `--on-colour` | `#FFFFFF` | type on sea/mountain/yaz/ink |
| Paper, sunk | `--paper-sunk` | `#F6F1E6` | band ground |
| Ink | `--ink` | `#16130F` | 18.07:1 on paper |
| Ink, quiet | `--ink-quiet` | `#57504A` | 7.36:1 on paper |
| Sea | `--sea` | `#1746C4` | 7.75:1 w/ white · 7.56:1 as text |
| Mountain | `--mountain` | `#0B7A41` | 5.42:1 w/ white · 5.29:1 as text |
| Yaz | `--yaz` | `#D11810` | 5.46:1 w/ white · 5.32:1 as text |
| Sand | `--sand` | `#FFC61E` | 11.77:1 w/ ink · **never white** |

### The rule that matters

**Sea, mountain and yaz are dual-role.** Each one clears AA both as white-on-colour and
as colour-on-paper, so the same token fills a block and sets a link. That is the whole
simplification over the old system, where no brand colour could legally carry text and
every colour needed a second "text-safe" twin.

**Sand is a fill, and only ever a fill.** It scores 1.63:1 against white and 1.54:1 as
text on paper. Sand blocks carry ink. Sand never sets type on paper, never carries white,
and never appears as a link colour. If you find yourself wanting yellow text, you want
ink on a sand block instead.

Never introduce a colour by literal in HTML or CSS — including inside inline SVG, where
`fill` and `stroke` take `var(--token)` like anything else. White is `--on-colour`, not
`#fff`. Add a token or use an existing one; the only hex values in the stylesheet are the
token definitions themselves.

### On blue

Blue is not merely allowed, it leads. The previous system banned it because an early
incarnation used stock blue gradients that read as generic — but the fix for a generic
blue is a *specific* blue, not the absence of one. `--sea` is the flag's blue and it
carries the brand.

### Data visualisation

Four hues with genuine separation, so series are distinguished by hue, not by lightness:

```
--sea       #1746C4     paternal line, Africa, deep time
--yaz       #D11810     maternal line, Europe, migration
--mountain  #0B7A41     land, place, the living present
--sand      #FFC61E     emphasis and ground only, never a series
```

Series colour is stable across the whole site: **the father's line is always sea, the
mother's line is always yaz.** A reader who learns that on the homepage should not have
to relearn it on any other page.

**Colour is never the only cue.** Every series also carries a non-colour identifier — a
dash pattern, a distinct marker shape, or a text label placed directly on the mark.
This is required, not optional, and it is what keeps the diagrams readable in greyscale
and for colour-blind readers.

---

## Typography

| Role | Family | Notes |
|---|---|---|
| Display | **Bricolage Grotesque** | Headings, numbers, kickers, buttons. 700–800, tight tracking |
| Reading | **Instrument Sans** | Body copy. Humanist, quiet, gets out of the way |
| Technical | **IBM Plex Mono** | Haplogroup notation, dates, coordinates, identifiers |
| Tifinagh | **Noto Sans Tifinagh** | The ⵣ yaz and any Tifinagh glyph. Subset to the glyphs used |

The split carries meaning: **what shouts is Bricolage, what you read is Instrument,
what is a precise identifier is Plex Mono.** Do not blur that.

- Load fonts with a `<link>` in `<head>`, never an `@import` (render-blocking).
- Always declare a real fallback stack. Three silent fallbacks to an unloaded `Lexend`
  shipped for months because nobody checked.
- **Tifinagh glyphs need Noto Sans Tifinagh or they render as tofu.** Any `ⵣ` in markup
  must be inside an element that resolves to that family. The Google Fonts request is
  subset with `&text=` so it costs well under 5 KB.
- Body: 17px / 1.65, `max-width: 68ch` on running prose.
- Display headings use `text-wrap: balance` and negative tracking (`-0.03em` and tighter
  as size grows). At poster sizes, default tracking looks loose and accidental.
- Display type is set in sentence case, not all-caps, except kickers and stat labels,
  which are all-caps at small sizes with positive tracking.
- **Headings are text.** Never `display: flex` on a heading — it turns a text node and a
  nested `<span>` into two side-by-side items, which broke the hero twice.

Do not use Inter or Space Grotesk. Both are strongly associated with machine-generated
layout, and using them together is a tell.

---

## Form language

Three rules produce the poster feel. They are cheap to state and easy to violate.

1. **Flat.** No shadows, no gradients, no blurs, no glass. A block is one solid colour.
   Depth is communicated by colour weight and scale, never by a drop shadow.
2. **Hard-edged.** Border radius is `0` on blocks, bands and buttons. The only radius on
   the site is the fully-round `--radius-dot` used for legend markers.
3. **Unequal.** Blocks in a group must differ in size, colour or weight. A row of four
   identical cards is the failure mode this design replaced; if a grid looks like a table
   of equals, it is wrong.

Separation comes from **colour change and the stripe rule**, never from a border on
every side of every box.

### The stripe

The site's one ornament is a band of unequal vertical stripes in the four palette
colours (`.stripe`). It is drawn from the striated `haik` and `tahaikt` textiles woven by
Ait Moussa women, whose stripe patterns are — unusually among Amazigh weaving traditions —
purely decorative rather than protective. An ornament that is openly ornamental is the
right one for this site to borrow.

Stripe widths are deliberately irregular. Do not make them even.

### The mark

`ⵣ` — yaz, the Tifinagh letter that stands for *Amazigh*, "free people". It appears as
the brand mark in the header and as the section marker on content pages. It is set in
Noto Sans Tifinagh, in `--yaz` on paper or white on colour.

---

## Structure

- **One `<h1>` per page, inside `<main>`.** The header carries the site name as a link,
  identical on every page, so the brand persists as you navigate.
- Heading levels descend sequentially. No skips. Size headings with a class, never by
  picking a lower level for its default size.
- Every page: skip link → header → nav → breadcrumb (not on the homepage) → `<main>` → footer.
- One footer everywhere.

## Layout

- Container max-width 1180px; full-bleed colour bands break out of it, their content does not.
- Grids use `minmax(0, 1fr)`, never bare `1fr` — `1fr` cannot shrink below min-content and
  will push the page sideways on a phone.
- Wide content (tables, diagrams) scrolls inside its own container. The body never scrolls
  horizontally, at any width down to 320px.
- Breakpoints: 1024px (desktop), 768px (tablet), 560px (stacked).
- Vertical rhythm is carried by band padding, not by margins between arbitrary elements.

## Components

Only these exist. Do not invent variants without adding them here.

- `.band` — a full-bleed horizontal section. `.band--sea` / `--yaz` / `--mountain` /
  `--sand` / `--sunk` set its ground. Consecutive bands must not repeat a ground.
- `.block` — a solid rectangle of colour carrying text. `.block--lead` is the oversized one.
- `.stripe` — the woven rule. Section separator and hero ornament.
- `.kicker` — all-caps mono or display label above a heading.
- `.stat` — a big display number with a small label. Numbers are the loudest type on the site.
- `.btn` — square, solid, min-height 48px. `.btn--ghost` is the outline variant.
- `.door` — the large tappable entry blocks (DNA / Land / Language).
- `.figure` — an authored SVG diagram with a caption. Never a photograph. Inside a colour
  band the caption switches to `--on-colour`; a dimmed white is not an option, because it
  fails 4.5:1 against `--yaz`.
- `.note` — the honesty callout: what the evidence does not support.
- `.page-title`, `.page-updated`, `.sourcing-note`.

## Imagery

**Diagrams, not photographs.** Every explanatory visual is authored inline SVG committed
to the repo: timelines, haplogroup trees, maps, comparison schemas.

This is a hard constraint with a practical cause — the site's photographs were generated
under a Stable Diffusion subscription that has lapsed, so that library cannot be extended
and the existing images cannot be matched. It is also the better answer: an authored
diagram is editable forever, weighs a few kilobytes, scales to any screen, inherits the
palette tokens, and adapts to the reader's theme. A generated photograph of a place does
none of that and quietly implies a documentary authority it has not earned.

- Inline SVG, not `<img src="*.svg">`, so diagrams inherit CSS custom properties.
- Every diagram carries `role="img"` and an `<title>`, plus a text caption that states
  the finding — not "Figure 3" but the sentence the diagram exists to make.
- Any diagram encoding data follows the data-visualisation rules above.
- Photographs are permitted only where the subject is a real, specific place or object
  and the image is genuine. Generated imagery is not permitted anywhere.
- Social images stay JPEG (`og-card.jpg`, 1200×630) — crawler support for WebP is uneven.

## Content

- **Amazigh** first, "Berber" in parentheses on first mention.
- Haplogroups in full: `E-PF2546`, `H1-T16189C!`, set in Plex Mono.
- Dates carry their range: "~11,000 years ago (range ~8,000–11,000)". A midpoint alone
  overstates the evidence.
- Hedge honestly — "approximately", "estimated", "debated".
- Cite at the point of assertion. Where content is not from published literature, say so.
- **No emoji.** Not in headings, not in body, not in nav. The yaz and the stripe are the
  site's ornament; emoji would compete with them and cheapen both. 77 had to be removed once.
- Every page shows a visible "Last updated", matched to JSON-LD `dateModified` and
  `sitemap.xml`. "Updated", not "reviewed": the date reflects a file change.

### Register, and the trap in shortening

Write for a curious sixteen-year-old: short sentences, concrete nouns, the finding before
the method. Lead with the claim, then support it.

**Concision comes from structure, never from stripping the qualifications.** The date
ranges, the DOIs and the words "estimated" and "debated" are not padding — they are what
separates this site from the confident nonsense that fills the rest of the genetic-ancestry
internet. Cut a page by moving detail to a diagram, a deeper page or a disclosure, not by
deleting the range from a date or the citation from a claim.

Target: **no more than ~900 words of running prose** per top-level page. Tables,
figure captions and source lists are scanned rather than read and are counted
separately — a five-row comparison table does not cost the reader what 180 words of
prose would. Measure the prose, not the raw word count, and do not game the rule by
turning prose into a table that nobody would naturally tabulate.

## Accessibility

The floor, not the goal. Lighthouse mobile accessibility must be **100 with zero
failures** before merge.

- 4.5:1 for normal text, 3:1 for large. Check against the actual block ground, not the page.
- Visible focus on everything interactive. On colour blocks the focus ring switches to
  paper so it stays visible.
- Touch targets ≥48px.
- Colour is never the only carrier of meaning — see the data-visualisation rules.
- `prefers-reduced-motion` is respected; all transitions collapse to none.
- Alt text on every image, with `width`/`height` to prevent layout shift. Inline SVG uses
  `role="img"` + `<title>` instead.

## Performance

- No page ships more than ~250 KB of imagery. Diagrams are inline SVG and cost almost nothing.
- Any remaining photographs: WebP, sized to roughly 2× their real CSS display width,
  q82 for photographs. No JPEG/PNG fallbacks.
- The LCP element is text, not an image. Nothing above the fold should need to download
  before the page reads.
- Fonts: four families, all variable or subset, loaded from one `<link>` with `display=swap`.

## Migration state

This system ships in `css/main.css`. The previous system's `css/styles.css` is still
served by the pages not yet migrated, and is deleted when the last page moves over.
A page uses one stylesheet or the other, never both.

Migrated: `index.html`, `lineage.html`.

## Working on this repo

No build step. Plain HTML, CSS and vanilla JS; edit and open in a browser. Deployment is
automatic from `main` via GitHub Pages.

Before opening a PR: run Lighthouse on the pages you touched, and check 320px for
horizontal overflow.
