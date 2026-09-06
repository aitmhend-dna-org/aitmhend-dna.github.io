### Changed
- All imagery converted to WebP and resized to real display dimensions: `img/` drops from 26 MB to 2.2 MB, and `lineage.html` from 10.77 MB of imagery to roughly 0.9 MB (#58)
- Social previews now use a real 1200x630 `og-card.jpg`. `og:image` had been pointing at a 2340x1334 PNG while declaring 1200x630, so previews were mis-sized; it stays JPEG because crawler support for WebP is still uneven

### Removed
- `img/berber-pattern-bg.jpg` (2.49 MB), orphaned when the header tile was retired in #54
