### Changed
- The 12 research article pages moved onto the flat poster system, completing the migration. Header, nav and footer are now byte-identical across all 21 pages of the site (#81)
- Articles were regenerated from structurally-extracted content rather than edited in place. Their markup was minified onto single lines, which is how a brand-bar change once silently skipped all twelve and two contrast failures survived every sweep for months (#81)

### Removed
- `css/styles.css` and `js/reading-aids.js` are deleted. Nothing references them; the site is one stylesheet again (#81)
- `research/demographic-modelling-amazigh-arab-2024.html` is retired to a `noindex` meta-refresh stub pointing at `north-africa-demographic-history-2024.html`, and dropped from `sitemap.xml`. Both pages summarised the same study (Serradell et al. 2024). GitHub Pages has no server-side redirects, hence the stub (#81)

### Fixed
- Display headings now carry `overflow-wrap: break-word`. "Microgeographical" in an article title is wider than a 320px container at 40px and was taking the whole document sideways — the only page-level overflow on the site, and invisible at desktop width (#81)
