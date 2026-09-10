### Added
- `llms.txt`, a plain-text map of the site for AI assistants and agents: every top-level page with its description, and every research summary with its authors, journal, date and DOI. The research scout rebuilds it when it adds a paper, and its validation fails if a listed paper is missing from it (#95)
- A custom 404 page, so a mistyped or old address leads back into the site instead of to GitHub's generic error page (#95)
- Richer structured data: the homepage now declares the site's publisher (name and logo), and the One family page carries its author, image, publication date and subjects (#95)

### Fixed
- The structured data on the French and Arabic pages used single-quoted strings, which is invalid JSON, so search engines ignored it; it now parses on all six pages (#95)
- `sitemap.xml` listed eight images that do not exist on the site; the dead entries are removed (#95)
