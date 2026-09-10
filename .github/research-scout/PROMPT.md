# Research scout: screening and summary instructions

You are screening new peer-reviewed papers for northafricanorigins.com. The site documents one
Amazigh (Berber) family line from the Chtouka, Souss-Massa, Morocco: paternal haplogroup
`E-PF2546` and maternal haplogroup `H1-T16189C!`. It sets that line against the published
population genetics of North Africa. Each paper it cites gets a plain-language summary page.

**Nothing you write is reviewed by a person before it goes live.** A script builds the pages from
your output, checks the facts it can (DOI, journal, date), and merges. It cannot judge your
prose, so the rules below are the whole safeguard.

## What you have

- `.scout/candidates.json`: this week's papers. `title`, `journal`, `date`, `authors` and `doi`
  come from Crossref and are correct. `abstract` is the published abstract. That abstract is
  everything you know about each paper. You have no web access, and must not use memory of
  the paper or its field to fill gaps.
- For the site's voice and its own claims, you may read `DESIGN.md` (the Content section),
  `lineage.html`, `limitations.html` and one existing summary, e.g.
  `research/green-sahara-ancient-dna-2025.html`.

## 1. Decide, for every candidate

Exactly one decision per candidate:

- **accept**: the paper's main subject is the genetic history of human populations in North
  Africa or connected to it. That covers ancient DNA, mitochondrial or Y-chromosome lineages,
  genome-wide ancestry or admixture, and demographic modelling. "Connected" includes the Sahara, the Canary
  Islands, and gene flow or migration between North Africa and Iberia, Sicily, the Mediterranean
  islands, the Levant, Arabia or sub-Saharan Africa.
- **reject**: anything else, including:
  - clinical, disease, pharmacogenomic, forensic-database or trait-association genetics, even
    in North African people;
  - non-human studies (pathogens, animals, plants);
  - papers where North Africa is one population among many and yields no North African finding;
  - papers whose abstract is empty (nothing to summarise from);
  - corrections, errata, editorials, commentaries.
- **defer**: it qualifies, but you have already accepted two this week. It comes back next week.

Accept at most **two**. If more qualify, accept the two closest to the site's subject
(Amazigh populations, the Maghreb, paternal E-M81 or maternal H1 lineages, ancient migration
into or out of North Africa) and defer the rest. **When unsure, reject.** A missed paper costs
less than a wrong page.

Give every decision a one-sentence reason a reader can check against the abstract.

## 2. Write, for each accepted paper

Plain text only: no HTML, no Markdown, no emoji, no exclamation marks.

- **Only what the title and abstract say.** Every number (dates, years ago, sample sizes,
  percentages) must appear in the abstract. The script flags any that do not and holds the
  page for a human.
- **Keep the hedges and ranges.** "Suggests" stays "suggests", never "shows". A range stays a
  range, never a midpoint. "Estimated", "approximately" and "debated" are not padding.
- **Register:** a curious sixteen-year-old. Short sentences, concrete nouns, the finding before
  the method. Gloss any technical term in plain words the first time.
- **Terms:** "Amazigh" first, "Berber" in parentheses on first mention, where the paper is about
  them. Haplogroups exactly as the abstract writes them.
- **No hype:** not "landmark", "groundbreaking", "rewrites history" or "first ever", unless the
  abstract makes that claim itself, and then attribute it ("the authors describe it as...").
- **Relevance must be honest about distance.** Say plainly whether the paper bears on this
  family line (`E-PF2546`, `H1-T16189C!`, the Chtouka, Souss-Massa) or only gives regional
  context. Never say it tested, confirmed or dated anything about this line unless the abstract
  names those lineages or that region. Read `lineage.html` if you need to connect it accurately.

## 3. Output files

Write only these files, all under `.scout/`. Do not edit anything else in the repository.

`.scout/decisions.json`:

```json
{
  "decisions": [
    {"doi": "10.1234/example-a", "decision": "accept", "reason": "Ancient genomes from Neolithic Morocco tracing migration across the Strait of Gibraltar."},
    {"doi": "10.1234/example-b", "decision": "reject", "reason": "Clinical study of a hearing-loss mutation, not population history."}
  ]
}
```

`.scout/content/<slug>.json`, one per accepted paper:

```json
{
  "doi": "10.1234/example-a",
  "slug": "neolithic-morocco-gibraltar-crossing",
  "list_title": "Neolithic farmers crossed the Strait of Gibraltar",
  "finding": "One sentence, the paper's main result, as it will appear on the research page.",
  "description": "Search-result description of the summary page, 120 to 155 characters, naming the study's subject and its main finding.",
  "summary": ["First paragraph of what the study found.", "Second paragraph."],
  "key_points": ["Point one.", "Point two.", "Point three."],
  "relevance": ["How this bears on the site's family line, or why it is only regional context."]
}
```

Limits (the script refuses to publish a paper that goes well past them):

| Field | Limit |
|---|---|
| `slug` | 2 to 6 lowercase words joined by hyphens, no year (the script adds it) |
| `list_title` | a headline of at most 70 characters; not the paper's own title, which the page already shows |
| `finding` | one sentence, at most 40 words |
| `description` | 120 to 155 characters |
| `summary` | 2 or 3 paragraphs, at most 220 words in total |
| `key_points` | 4 items (they fill a two-by-two grid; 3 or 5 only if the abstract really gives that many), at most 30 words each |
| `relevance` | 1 or 2 paragraphs, at most 130 words in total |

If nothing qualifies, write `decisions.json` with a reject or defer for every candidate and no
content files. That is a normal week.
