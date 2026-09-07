### Added
- French (`/fr/`) and Arabic (`/ar/`) versions of the three pages that carry the argument — the homepage, the two lineages, and what the evidence cannot show. Every date range, hedge and citation is preserved; each page links back to the English site for depth (#84)
- A page-aware language switcher in the header of all 27 pages. On a translated page it links to the exact equivalent; elsewhere it links to that language's home, never to a page that does not exist (#84)
- Right-to-left support: `dir="rtl"`, mirrored stripe, Arabic typefaces (Noto Kufi Arabic for display, Noto Sans Arabic for reading), more leading and zero letter-spacing, and Latin identifiers bidi-isolated so `E-PF2546` is not reordered inside Arabic text (#84)

### Fixed
- **The site had been claiming an Arabic version that never existed.** `index.html` declared `hreflang="ar"` and `og:locale:alternate=ar_MA`, both pointing at the English page. All 27 pages now carry accurate reciprocal `hreflang`, and no page claims a translation it does not have (#84)
- `lineage.html` had no `hreflang` at all — it was written without alternates in the redesign and nothing had noticed (#84)
- Long unbreakable tokens (DOIs, URLs) overflowed a 280px container. Only surfaced on the Arabic pages, where the Arabic body face renders a Latin run wider, but the hazard was language-independent (#84)
- Arabic web fonts swapping in late measured CLS 0.297 on `ar/lineage.html`. The Arabic faces now load with `display=optional` — still fetched and cached, never causing a shift. The Latin faces keep `swap`, being metric-close to their fallback (#84)
