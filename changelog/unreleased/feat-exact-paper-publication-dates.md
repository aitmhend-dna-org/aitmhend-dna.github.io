### Added
- Exact publication dates on all eleven papers — day, month and year, taken from each paper's Crossref record — under the year on `research.html` and in each article's kicker, marked up as `<time datetime>`. JSON-LD `datePublished` now carries the full ISO date rather than the year alone. The dates are first online publication; `research.html` says so, since print issues follow weeks later (#86)

### Changed
- The journal name on `research.html` is set in ink instead of quiet grey. It was always there, just easy to miss (#86)

### Fixed
- `research.html` said "newest first" but was only ordered by year: within 2024 and 2025 the papers were out of order, which visible exact dates would have exposed. The list is now sorted by date (#86)
