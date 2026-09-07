# Changelog

All notable changes to this project are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- `css/main.css`, the new design system. `css/styles.css` continues to serve the 21 pages not yet migrated and is deleted when the last one moves over (#77)
- Authored inline SVG diagrams in place of photography on the migrated pages. The site's images were generated under a Stable Diffusion subscription that has lapsed, so the library could not be extended; authored diagrams cost nothing, inherit the palette tokens and stay editable (#77)
- Three research summaries that had been sitting unpublished on the old fork since PR #8 and never reached the live site: Canary Islands Amazigh history (Santana et al. 2025), demographic modelling of Amazigh–Arab divergence (2024), and Islamic-period Ibiza gene flow (2026). The research index now lists 12 papers
- A Limitations page stating what two haplogroups can and cannot show — two ancestral lines out of more than a thousand, why a haplogroup is not an ethnicity, and how wide the TMRCA ranges actually are (#49)
- A visible "Last updated" date on every page, kept in step with JSON-LD `dateModified` and `sitemap.xml` (#48)
- A sourcing note on the culture page stating plainly that its material comes from community and family knowledge rather than peer-reviewed literature (#47)

### Changed
- The remaining eight top-level pages moved onto the flat poster system, so the whole top level is now one design: `start-here`, `glossary`, `maps-sites`, `limitations`, `research`, `genetics`, `culture` and `contact`. Header, nav and footer are byte-identical across all ten pages (#79)
- `genetics.html` rewritten around what a haplogroup actually is, with a diagram of 32 ancestors showing that Y-DNA and mtDNA describe two of them and nothing else, and a chart of two published age ranges for `E-M81` that disagree by two millennia (#79)
- `research.html` is now typographic — eleven papers with year, journal, one-line finding and DOI — replacing twelve image thumbnails of uncertain provenance (#79)
- `culture.html` keeps its sourcing note at the top, and its Tachelhit phrases now actually render: the Tifinagh font subset was widened from the single yaz glyph to all thirteen the page uses (#79)
- `maps-sites.html` drops the third-party Google Maps `iframe` in favour of plain links (#79)
- `contact.html` forms restyled and de-emoji'd, both Formspree endpoints unchanged (#79)
- `glossary.html` expanded from five terms to twelve, covering the vocabulary the rewritten pages introduced — subclade, coalescence, molecular clock, admixture, patrilocality, star-like expansion, control region (#79)
- Site name is now "North African Origins" everywhere rather than on two pages (#79)
- The 12 research article pages moved onto the flat poster system, completing the migration. Header, nav and footer are now byte-identical across all 21 pages of the site (#81)
- Articles were regenerated from structurally-extracted content rather than edited in place. Their markup was minified onto single lines, which is how a brand-bar change once silently skipped all twelve and two contrast failures survived every sweep for months (#81)
- New visual identity, piloted on the homepage and `lineage.html`: a bright flat-colour poster system built on the Amazigh flag palette — sea blue, mountain green, sand yellow and yaz red — with Bricolage Grotesque for display, Instrument Sans for reading, and the yaz (ⵣ) as the brand mark. Retiring the old "no blue" rule is what made the flag's own colours available. `DESIGN.md` was rewritten against it; the accessibility, performance and structural rules carried over unchanged (#77)
- `lineage.html` cut from roughly 2,100 words of prose to 824, with the argument now carried by a vertical deep-time timeline, an E-PF2546 frequency chart and a scored comparison of the five competing explanations for how a European maternal line reached North Africa. No date range, hedge or citation was dropped to achieve it (#77)
- Site ornament is now a band of irregular stripes taken from the striated `haik` and `tahaikt` textiles woven by Ait Moussa women, whose patterns are decorative rather than protective (#77)
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

### Removed
- `css/styles.css` and `js/reading-aids.js` are deleted. Nothing references them; the site is one stylesheet again (#81)
- `research/demographic-modelling-amazigh-arab-2024.html` is retired to a `noindex` meta-refresh stub pointing at `north-africa-demographic-history-2024.html`, and dropped from `sitemap.xml`. Both pages summarised the same study (Serradell et al. 2024). GitHub Pages has no server-side redirects, hence the stub (#81)
- `gemeni-infograph.html`: orphaned, on a second design system (Tailwind CDN), with Gemini buttons that could never work (`apiKey = ""`) (#60)
- `img/berber-pattern-bg.jpg` (2.49 MB), orphaned when the header tile was retired in #54

### Fixed
- The "Skip to main content" link no longer shows as a brown sliver in the top-left corner of every page. `.skip-to-main` was declared twice in `css/styles.css`; the second declaration replaced the working off-screen offset with `top: -40px`, which the link's own height out-ran. Both declarations, and the separate `.skip-link` class used by the research articles, are now one rule that hides the link with the clip-based visually-hidden pattern and reveals it in a single consistent position on keyboard focus (#75)
- **A factual inconsistency between pages.** `limitations.html` gave the H1 arrival estimate as "~11,400 years ago (range 9,000–13,700)" while `lineage.html` gave 8,000–11,000. These are two different quantities — the global coalescence of H1 versus its coalescence within North Africa — and the site had conflated them. Both pages now say which is which, and `limitations.html` uses the discrepancy as its worked example of why published dates disagree (#79)
- **A duplicate paper.** `demographic-modelling-amazigh-arab-2024.html` and `north-africa-demographic-history-2024.html` summarise the same study (Serradell et al. 2024, `10.1186/s13059-024-03341-4`). The site claimed twelve peer-reviewed papers; it has eleven. The homepage stat and `lineage.html` now say eleven (#79)
- Figure captions inside a colour band used ink-on-ink and were unreadable at 1.00:1 and 2.34:1. They now use `--on-colour` — a dimmed white is not an option, as it fails AA against `--yaz` (#79)
- `.phrase__gloss` used 85%-opacity white, which composites to 4.38:1 over `--mountain` and fails AA. Caught by Lighthouse, not by the project's own contrast script, which was treating translucent foregrounds as opaque; the script now composites alpha and resolves SVG text against the `<rect>` it is painted on (#79)
- Display headings now carry `overflow-wrap: break-word`. "Microgeographical" in an article title is wider than a 320px container at 40px and was taking the whole document sideways — the only page-level overflow on the site, and invisible at desktop width (#81)
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
