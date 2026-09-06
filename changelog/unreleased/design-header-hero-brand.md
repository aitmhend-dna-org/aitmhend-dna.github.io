### Changed
- The site name is now a constant brand bar on every page; the page title moved into `<main>` as the `<h1>`, so the brand no longer disappears as you navigate (#50)
- Retired the tiled pattern behind the header, and deleted the unused `.hero` block that carried it along with two navy gradients (#54)
- The homepage hero leads with one action and a quiet secondary link instead of three competing buttons (#55)
- Recoloured the site mark: the Tifinagh yaz was `#2574AF` blue with green accents, the last blue on the site

### Fixed
- The hero headline reads as one phrase again. `.card h2` was `display: flex`, which turned a heading's text node and its accent `<span>` into two side-by-side flex items — the real cause, and why the earlier fix for #23 regressed (#52)
