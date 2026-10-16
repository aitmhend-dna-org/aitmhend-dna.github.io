# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static website hosted on GitHub Pages explaining how migrations shaped North Africa's population, from peer-reviewed genetics (the homepage timeline is built only from the papers summarised in `research/`). One Amazigh (Berber) family from Souss-Massa, Morocco (Y-DNA E-PF2546, mtDNA H1-T16189C!) is the worked example on the "One family" page, `lineage.html`. Also covers the history and culture of the Chtouka confederation.

**Live site:** https://northafricanorigins.com

## Development

This is a **no-build static site** — plain HTML, CSS, and vanilla JS. No package manager, bundler, or framework.

- **Edit and preview directly** — open any `.html` file in a browser
- **Deployment** — automatic via GitHub Pages from main branch
- **External deps (CDN only):** Google Fonts (Bricolage Grotesque, Instrument Sans, IBM Plex Mono, Noto Sans Tifinagh; Noto Sans Arabic and Noto Kufi Arabic on the `ar/` pages). No JavaScript libraries
- **Google Analytics 4** (`G-ZVDSQHZ2Q2`), loaded by `js/consent.js` only after the reader accepts the cookie question — see Analytics and consent in `DESIGN.md`
- **Contact form:** Formspree (ID: myzbzgjn)

## Architecture

- `index.html`, `lineage.html`, `genetics.html`, `culture.html`, `research.html`, `contact.html`,
  `start-here.html`, `glossary.html`, `maps-sites.html`, `limitations.html` — the site pages
- `privacy.html` — what Google Analytics counts once the reader accepts, and how to withdraw
- `fr/` and `ar/` — French and Arabic translations of `index.html`, `lineage.html`, `limitations.html` and `privacy.html`, linked by reciprocal `hreflang` (`ar/` is right-to-left). Change a translated page's English original and its counterparts together
- `research/*.html` — one summary per paper listed on `research.html` (the scout adds new ones)
- `css/main.css` — the only stylesheet (see `DESIGN.md`)
- `js/consent.js` — the only shared script: the cookie question in EN/FR/AR and Google Analytics behind it. Every page loads it with `defer` and `data-ga="G-ZVDSQHZ2Q2"`; add that line to any new page
- `img/` — `og-card.jpg` for social, the logo mark, and older WebP imagery. Pages use authored inline SVG diagrams instead of photographs — see the Imagery section of `DESIGN.md`
- `docs/` — research notes and SEO documentation
- `.github/research-scout/` + `.github/workflows/research-scout.yml` — the weekly research scout, which adds new papers to `research.html` and `research/` on its own. Its page template and count-sync logic live in `scout.py`; if you change the article layout or the "All N summaries" wording, change them there too, or `scout.py validate` will fail the next run. See its `README.md`
- `llms.txt` — the plain-text site map for AI assistants and agents (llmstxt.org). It is generated: run `python3 .github/research-scout/scout.py llms` after changing a top-level page's title or description, and the scout rebuilds it whenever it adds a paper. Do not hand-edit it
- `404.html` — served by GitHub Pages at any missing URL, so every link in it is root-absolute (`/css/main.css`). It is the one page whose chrome differs from the rest; leave it out of site-wide chrome sweeps and hash checks. `noindex`, not in the sitemap

Every page follows the same structure: constant brand `<header>` → sticky `<nav>` → breadcrumb → `<main id="main-content">` carrying the page `<h1>` → shared `<footer>`. Each page includes full SEO markup (Open Graph, Twitter Cards, JSON-LD structured data, canonical URLs, geo-tags).

## Design System

**All design rules live in `DESIGN.md` at the repository root.** Read it before
changing any styling.

`.cursorrules` and `.github/copilot-instructions.md` only point to it. Keep design
rules in `DESIGN.md` alone: separate copies drifted apart and contradicted the stylesheet.

## Content & Terminology

- Use **"Amazigh"** as primary term, "Berber" in parentheses for SEO context
- Haplogroup notation: "E-PF2546" (Y-DNA), "H1-T16189C!" (mtDNA)
- Date format with context: "~400 BCE (2,400 years before present)"
- Geographic: "Souss-Massa" (primary), "Souss Valley" (descriptive)
- Language reference: "Tachelhit" (the specific Amazigh language)
- Tone: written for a curious sixteen-year-old — short sentences, concrete nouns, the finding before the method. The evidence stays scholarly: date ranges, hedging and citations are never cut to shorten a page

## SEO Checklist (for any page changes)

- Title tags: 40-50 characters
- Meta descriptions: 150-160 characters
- All images: descriptive alt text, explicit width/height; `loading="lazy"` below the fold only
- Maintain JSON-LD schema markup (WebSite, Article, ScholarlyArticle, ContactPage)
- Update `sitemap.xml` lastmod dates when pages change
