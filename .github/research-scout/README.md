# Research scout

Every Monday at 06:00 UTC, `.github/workflows/research-scout.yml` looks for new peer-reviewed
papers on North African population genetics and ancient migrations. It adds up to two a week to
the site, then opens a PR, merges it and deploys.

| Step | Who | What |
|---|---|---|
| `scout.py candidates` | script | Europe PMC search (PubMed-indexed journals only) over the last 28 days. DOIs already on the site or in `screened.json` are skipped. Everything else is checked against Crossref, and anything that isn't a journal article is dropped. No candidates means the run stops here and Claude is never called. |
| Claude step | Claude Opus 5 | Reads `PROMPT.md` and the candidates. Accepts or rejects each one and writes the prose for at most two. It has only Read/Write tools and may write only under `.scout/`; the next step fails the run if it wrote anywhere else. |
| `scout.py apply` | script | Builds the article page on top of an existing one (so header, nav and footer stay current), inserts it in `research.html` by date, updates the paper count everywhere it is spelled out, and updates the sitemap, `llms.txt`, `Last updated` dates, a changelog fragment and `screened.json`. |
| `scout.py validate` | script | The merge gate. Every DOI on the research page must match Crossref's date and journal. Each article must agree with the index, the count must read the same everywhere, the chrome must be identical, every paper must be listed in `llms.txt`, and only allowed files may have changed. |
| PR step | workflow | Branch, PR, merge, Pages build. |

Titles, journals, dates and authors always come from Crossref; Claude supplies prose only.
A summary that uses a number not found in the paper's abstract is **not** merged: its PR stays
open for a human to read.

## One-time setup (repository owner)

This is done by the owner account, since it needs admin rights on the repo.

1. **Secret**: Settings → Secrets and variables → Actions → New repository secret,
   name `CLAUDE_CODE_OAUTH_TOKEN`. The value is printed by `claude setup-token`, run on a machine
   logged in to the Claude subscription that should pay for the runs.
2. **PR permission**: Settings → Actions → General → Workflow permissions: choose
   **Read and write permissions** and tick **Allow GitHub Actions to create and approve pull requests**.

Until the secret exists, scheduled runs skip with a notice rather than fail.

## Everyday use

- **Run it now:** Actions → Research scout → Run workflow. Set `days` to look further back,
  e.g. `120` for a first catch-up.
- **Review before publishing:** set `AUTO_MERGE: "false"` in the workflow. It then stops at an
  open PR.
- **Re-screen a paper it rejected:** delete its entry from `screened.json`.
- **Check the site by hand:** `python3 .github/research-scout/scout.py validate`. Add
  `--offline` to skip Crossref.
- GitHub disables scheduled workflows in public repos after 60 days without activity. Any week
  with candidates merges a small PR (at least the ledger), which counts as activity. After a
  long quiet spell, re-enable the workflow from the Actions tab.
