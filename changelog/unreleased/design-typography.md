### Changed
- New type pairing: Literata for long-form reading, Archivo for headings and chrome, IBM Plex Mono kept for haplogroup notation. Inter and Space Grotesk are the two faces most associated with machine-generated layout, and Inter is a UI face carrying 2,242 words of prose on lineage.html (#56)
- Body text set at 17px/1.7 with a 72ch measure on running prose
- Fonts now load from a `<link>` in `<head>` instead of a render-blocking `@import` at the top of the stylesheet

### Fixed
- `.region-map`, `.genetic-diagram` and `.phylogenetic-tree` labels asked for `Lexend`, which was never loaded — a silent fallback to the browser default
