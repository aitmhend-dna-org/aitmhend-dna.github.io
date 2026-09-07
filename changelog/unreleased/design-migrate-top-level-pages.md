### Changed
- The remaining eight top-level pages moved onto the flat poster system, so the whole top level is now one design: `start-here`, `glossary`, `maps-sites`, `limitations`, `research`, `genetics`, `culture` and `contact`. Header, nav and footer are byte-identical across all ten pages (#79)
- `genetics.html` rewritten around what a haplogroup actually is, with a diagram of 32 ancestors showing that Y-DNA and mtDNA describe two of them and nothing else, and a chart of two published age ranges for `E-M81` that disagree by two millennia (#79)
- `research.html` is now typographic — eleven papers with year, journal, one-line finding and DOI — replacing twelve image thumbnails of uncertain provenance (#79)
- `culture.html` keeps its sourcing note at the top, and its Tachelhit phrases now actually render: the Tifinagh font subset was widened from the single yaz glyph to all thirteen the page uses (#79)
- `maps-sites.html` drops the third-party Google Maps `iframe` in favour of plain links (#79)
- `contact.html` forms restyled and de-emoji'd, both Formspree endpoints unchanged (#79)
- `glossary.html` expanded from five terms to twelve, covering the vocabulary the rewritten pages introduced — subclade, coalescence, molecular clock, admixture, patrilocality, star-like expansion, control region (#79)
- Site name is now "North African Origins" everywhere rather than on two pages (#79)

### Fixed
- **A factual inconsistency between pages.** `limitations.html` gave the H1 arrival estimate as "~11,400 years ago (range 9,000–13,700)" while `lineage.html` gave 8,000–11,000. These are two different quantities — the global coalescence of H1 versus its coalescence within North Africa — and the site had conflated them. Both pages now say which is which, and `limitations.html` uses the discrepancy as its worked example of why published dates disagree (#79)
- **A duplicate paper.** `demographic-modelling-amazigh-arab-2024.html` and `north-africa-demographic-history-2024.html` summarise the same study (Serradell et al. 2024, `10.1186/s13059-024-03341-4`). The site claimed twelve peer-reviewed papers; it has eleven. The homepage stat and `lineage.html` now say eleven (#79)
- Figure captions inside a colour band used ink-on-ink and were unreadable at 1.00:1 and 2.34:1. They now use `--on-colour` — a dimmed white is not an option, as it fails AA against `--yaz` (#79)
- `.phrase__gloss` used 85%-opacity white, which composites to 4.38:1 over `--mountain` and fails AA. Caught by Lighthouse, not by the project's own contrast script, which was treating translucent foregrounds as opaque; the script now composites alpha and resolves SVG text against the `<rect>` it is painted on (#79)
