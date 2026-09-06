# Changelog

All notable changes to this project are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Three research summaries that had been sitting unpublished on the old fork since PR #8 and never reached the live site: Canary Islands Amazigh history (Santana et al. 2025), demographic modelling of Amazigh–Arab divergence (2024), and Islamic-period Ibiza gene flow (2026). The research index now lists 12 papers
- A Limitations page stating what two haplogroups can and cannot show — two ancestral lines out of more than a thousand, why a haplogroup is not an ethnicity, and how wide the TMRCA ranges actually are (#49)
- A visible "Last updated" date on every page, kept in step with JSON-LD `dateModified` and `sitemap.xml` (#48)
- A sourcing note on the culture page stating plainly that its material comes from community and family knowledge rather than peer-reviewed literature (#47)

### Changed
- Research thumbnails now show each paper's actual study region. Six of the twelve cards had shared one generic Maghreb satellite image while their alt text claimed to show the Canary Islands, the Balearics or Algeria and Tunisia — descriptions the image did not match. Five region crops were cut from the full-resolution original, and every alt text and caption now describes what is really in frame
- Article hero images and captions realigned to the same assignment; `punic-genetic-diversity-2025` had no hero at all
- The nine existing research articles were brought onto the current design: constant brand bar, page title as the `<h1>` in `<main>`, sequential heading levels, WebP imagery, corrected social images and the shared footer. The brand-bar work in #50 had only reached the top-level pages, because the articles' markup is minified and the regex missed them
- Removed emoji from 77 headings across the site; #24 had only covered part of one page (#61)
- One consistent footer on every page — three variants existed, and most research articles had no secondary navigation at all
- The site name is now a constant brand bar on every page; the page title moved into `<main>` as the `<h1>`, so the brand no longer disappears as you navigate (#50)
- Retired the tiled pattern behind the header, and deleted the unused `.hero` block that carried it along with two navy gradients (#54)
- The homepage hero leads with one action and a quiet secondary link instead of three competing buttons (#55)
- Recoloured the site mark: the Tifinagh yaz was `#2574AF` blue with green accents, the last blue on the site
- Removed the homepage "On This Page" strip, which listed the four cards immediately below it. On content pages the table of contents is now a sticky left rail beside the text it indexes, with the active section marked (#51)
- The homepage leads with one entry (the lineage analysis) instead of four identical cards with four identical accent rails; the other three share a quieter treatment (#53)
- New type pairing: Literata for long-form reading, Archivo for headings and chrome, IBM Plex Mono kept for haplogroup notation. Inter and Space Grotesk are the two faces most associated with machine-generated layout, and Inter is a UI face carrying 2,242 words of prose on lineage.html (#56)
- Body text set at 17px/1.7 with a 72ch measure on running prose
- Fonts now load from a `<link>` in `<head>` instead of a render-blocking `@import` at the top of the stylesheet
- All imagery converted to WebP and resized to real display dimensions: `img/` drops from 26 MB to 2.2 MB, and `lineage.html` from 10.77 MB of imagery to roughly 0.9 MB (#58)
- Social previews now use a real 1200x630 `og-card.jpg`. `og:image` had been pointing at a 2340x1334 PNG while declaring 1200x630, so previews were mis-sized; it stays JPEG because crawler support for WebP is still uneven

### Fixed
- `research.html` showed two contradictory dates — "Last updated: 6 September 2026" beside a stale pill reading "Last updated: July 9, 2026"
- Every research thumbnail and hero now carries explicit `width`/`height`, so images reserve their space instead of shifting layout as they load
- Two contrast failures in article-only components: the hero caption used Tailwind's `#6B7280` at 4.39:1 and the paper date `#8B7355` at 4.22:1. Both now use `--text-secondary`
- Five inline `font-family` declarations still asked for Space Grotesk, Inter or Lexend after the type change, none of which are loaded any more, so those elements silently fell back to a browser default
- Cumulative Layout Shift on `lineage.html` dropped from 0.32 to 0.05. The table of contents is injected by JavaScript after parse, and below the rail breakpoint it lands in normal flow — an expanded nine-item list shoved the article down the page. It now starts collapsed there, and the diagram container reserves its height
- `.toc-card.is-collapsed .toc-list` set `display: flex`, so collapsing the table of contents did not actually collapse it
- Paternal and maternal lineages are now distinguishable in the diagrams and charts. Series colours follow a luminance-ordered warm ramp (3.27:1 in greyscale, up from 2.26:1) and carry a non-colour identifier: the maternal branch and node are dashed, the second line series has a dash pattern and its own point marker
- `culture.html`'s food chart had two of three series sharing an identical fill, distinguishable only by border colour
- Chart labels asked for `Lexend`, which no stylesheet ever loaded, so every chart axis and legend silently fell back to the browser default
- The hero headline reads as one phrase again. `.card h2` was `display: flex`, which turned a heading's text node and its accent `<span>` into two side-by-side flex items — the real cause, and why the earlier fix for #23 regressed (#52)
- `.region-map`, `.genetic-diagram` and `.phylogenetic-tree` labels asked for `Lexend`, which was never loaded — a silent fallback to the browser default
- Mobile navigation no longer clips "Contact" — the nav wraps instead of scrolling behind a hidden scrollbar (#32)
- Brand colours now meet WCAG AA: accents are split by role, with `--accent-text` for text and `--accent-solid` for fills carrying white text (#33)
- "On This Page" is a readable vertical list on phones instead of a horizontal scroller with no affordance (#34)
- Heading levels descend sequentially; five timeline headings were `<h4>` under an `<h2>` (#35)
- Removed the second `:root` block that re-injected blue, teal and cyan — the phylogenetic diagrams now render in the site palette (#36)
- `theme-color` is the palette brown rather than a blue that never belonged to the design (#37)
- `--primary-terracotta` holds the spec'd `#CD7F32` instead of gold `#D4A629` (#38)
- The homepage hero is eagerly loaded and preloaded rather than lazy-loaded as the LCP element (#39)
- Removed a Search Console `TODO` placeholder from the shipped homepage (#40)
- Replaced a hardcoded Tailwind `slate-900` with a palette token (#41)
- Dropped the single-item "Home" breadcrumb from the homepage (#42)
- Deleted 12.6 MB of images referenced by nothing (#43)
- Buttons inside cards were repainted by a later `.card a` rule, rendering their labels gold-on-gold; buttons are now excluded (found while fixing #33)
- Two fixed-column grids on lineage.html pushed the page sideways on phones; both now stack (found while fixing #34)

### Removed
- `gemeni-infograph.html`: orphaned, on a second design system (Tailwind CDN), with Gemini buttons that could never work (`apiKey = ""`) (#60)
- `img/berber-pattern-bg.jpg` (2.49 MB), orphaned when the header tile was retired in #54
