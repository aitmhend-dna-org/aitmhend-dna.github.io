#!/usr/bin/env python3
"""Weekly research scout for northafricanorigins.com.

    candidates   Search Europe PMC for recent peer-reviewed papers, drop the ones the
                 site already lists or has screened, enrich the rest from Crossref.
                 Writes .scout/candidates.json.
    apply        Turn Claude's decisions and prose (.scout/decisions.json,
                 .scout/content/*.json) into an article page, a research.html entry,
                 count/sitemap/date updates, a changelog fragment and ledger entries.
    validate     The merge gate: every listed paper matches Crossref, each article
                 agrees with the index, the paper count reads the same everywhere, and
                 (with --check-changed) only the files a scout run may touch changed.

Facts (title, journal, date, authors, DOI) always come from Crossref, never from the
model; the model supplies prose only. Standard library only, so the workflow needs no
install step.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import os
import re
import subprocess
import textwrap
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WORK = ROOT / ".scout"
LEDGER = HERE / "screened.json"
MAIN_TEMPLATE = HERE / "article-main.html"
INDEX = ROOT / "research.html"
SITEMAP = ROOT / "sitemap.xml"
SITE = "https://northafricanorigins.com"
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
UA = "northafricanorigins-research-scout/1.0 (+https://northafricanorigins.com)"
MAX_ACCEPTS = 2

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

# Human-ancestry terms AND a North African place, in title or abstract. A bare
# "genome"/"genomic" pulled in pathogens and crops, so it is deliberately absent.
TOPIC = ('("ancient DNA" OR aDNA OR ancestry OR admixture OR haplogroup OR haplogroups'
         ' OR mitogenome OR mitogenomes OR "mitochondrial DNA" OR mtDNA OR "Y-chromosome"'
         ' OR "Y chromosome" OR "population history" OR "genetic history"'
         ' OR "demographic history" OR "population structure" OR "gene flow"'
         ' OR paleogenomic OR palaeogenomic OR archaeogenetic OR archaeogenetics)')
PLACE = ('("North Africa" OR "North African" OR "Northwest Africa" OR Maghreb OR Maghrebi'
         ' OR Amazigh OR Berber OR Berbers OR Imazighen OR Tuareg OR Morocco OR Moroccan'
         ' OR Algeria OR Algerian OR Tunisia OR Tunisian OR Libya OR Libyan OR Sahara'
         ' OR Saharan OR Guanche OR Guanches OR "Canary Islands" OR Canarian OR Punic'
         ' OR Phoenician OR Carthage OR Carthaginian OR Gibraltar OR Iberomaurusian'
         ' OR Taforalt)')

# The only files a scout run may change. Anything else fails validation.
ALLOWED = re.compile(
    r"^(research\.html|lineage\.html|sitemap\.xml|research/[a-z0-9-]+\.html"
    r"|changelog/unreleased/[a-z0-9-]+\.md|\.github/research-scout/screened\.json)$")

# Hard limits on the model's prose. PROMPT.md asks for less; the margin means a run is
# only stopped for a real overrun.
LIMITS = {"list_title_chars": 90, "finding_words": 55, "description_chars": (90, 180),
          "summary_words": 280, "summary_paras": (1, 4), "key_points": (3, 5),
          "key_point_words": 45, "relevance_words": 180, "relevance_paras": (1, 3)}
BLOCKS = ["block block--sea", "block", "block block--mountain", "block", "block block--yaz"]
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+){0,7}$")
MARKUP = re.compile(r"[<>*#`]|\]\(")
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF]")

_ONES = ("zero one two three four five six seven eight nine ten eleven twelve thirteen "
         "fourteen fifteen sixteen seventeen eighteen nineteen").split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def number_word(n: int) -> str:
    if n < 20:
        return _ONES[n]
    tens, ones = divmod(n, 10)
    return _TENS[tens] + (f"-{_ONES[ones]}" if ones else "")


NUM = "|".join(sorted((number_word(n) for n in range(1, 100)), key=len, reverse=True))
# Where the site spells out how many papers it summarises, file by file.
COUNT_PHRASES = {
    "index": [rf"\b({NUM}) papers\b", rf"\bthe ({NUM}) peer-reviewed studies\b"],
    "lineage": [rf"\bAll ({NUM}) papers summarised\b"],
    "article": [rf"\bAll ({NUM}) summaries are listed\b"],
}
ITEM = re.compile(r'\n[ \t]*<li class="paper">.*?</li>', re.S)
DOI_LINK = re.compile(r'https://doi\.org/([^"<\s]+)')


# --- small helpers -------------------------------------------------------------------

def clean(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s or "")
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def words(s: str) -> int:
    return len(s.split())


def long_date(iso: str, with_year: bool = True) -> str:
    parts = iso.split("-")
    if len(parts) == 1:
        return parts[0] if with_year else ""
    month = MONTHS[int(parts[1]) - 1]
    s = f"{int(parts[2])} {month}" if len(parts) == 3 else month
    return f"{s} {parts[0]}" if with_year else s


def set_output(key: str, value) -> None:
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"{key}={value}\n")


def step_summary(md: str) -> None:
    print(md)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
            f.write(md + "\n")


def sub_once(pattern: str, repl, text: str, flags: int = 0) -> str:
    out, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f"template pattern not found: {pattern}")
    return out


def get_json(url: str, params: dict | None = None, tries: int = 4):
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    last: Exception | None = None
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            last = e
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            last = e
        time.sleep(2 ** attempt)
    raise SystemExit(f"GET {url} failed after {tries} tries: {last}")


def crossref(doi: str) -> dict | None:
    data = get_json("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/()"))
    if not data:
        return None
    m = data["message"]
    parts = None
    for key in ("published-online", "issued"):  # online first: it is the citation date
        p = (m.get(key) or {}).get("date-parts", [[None]])[0]
        if p and p[0]:
            parts = p
            break
    authors = m.get("author") or []
    return {
        "doi": doi.lower(),
        "type": m.get("type"),
        "title": clean((m.get("title") or [""])[0]).rstrip("."),
        "journal": clean((m.get("container-title") or [""])[0]),
        "date": "-".join([str(parts[0])] + [f"{int(x):02d}" for x in parts[1:]]) if parts else "",
        "authors": [clean(a.get("family") or a.get("name") or "") for a in authors],
        "first_given": clean((authors[0] if authors else {}).get("given", "")),
        "volume": str(m.get("volume") or ""),
        "pages": str(m.get("page") or m.get("article-number") or ""),
    }


def authors_short(c: dict) -> str:
    names = [a for a in c["authors"] if a]
    if not names:
        return c["journal"]
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} and {names[1]}"
    return f"{names[0]} et al."


def citation(c: dict) -> str:
    names = [a for a in c["authors"] if a]
    who = names[0] if names else c["journal"]
    if names and c["first_given"]:
        who += f", {c['first_given'][0]}."
    if len(names) > 1:
        who += " et al."
    out = f"{who} ({c['date'][:4]}). {c['journal']}"
    for part in (c["volume"], c["pages"]):
        if part:
            out += f", {part}"
    return out + "."


def norm_journal(s: str) -> str:
    s = clean(s).casefold().replace("&", "and")
    return re.sub(r"^the ", "", re.sub(r"\s+", " ", s))


def site_dois() -> set[str]:
    found: set[str] = set()
    for f in [INDEX, *sorted((ROOT / "research").glob("*.html"))]:
        found |= {d.lower() for d in DOI_LINK.findall(f.read_text())}
    return found


def load_ledger() -> dict:
    if LEDGER.exists():
        return json.loads(LEDGER.read_text())
    return {"screened": {}}


def index_items(text: str):
    start = text.index('<ul class="papers">') + len('<ul class="papers">')
    end = text.index("</ul>", start)
    body = text[start:end]
    items = ITEM.findall(body)
    tail = body[len("".join(items)):]
    if "".join(items) + tail != body or tail.strip():
        raise SystemExit("research.html paper list has unexpected markup")
    return start, end, items, tail


def item_fields(item: str) -> dict:
    return {
        "doi": re.search(r'href="https://doi\.org/([^"]+)"', item).group(1).lower(),
        "date": re.search(r'<time class="paper__date" datetime="([^"]+)"', item).group(1),
        "journal": clean(re.search(r'<cite class="paper__journal">(.*?)</cite>', item).group(1)),
        "href": re.search(r'<h3 class="paper__title"><a href="([^"]+)"', item).group(1),
    }


def count_targets():
    yield INDEX, COUNT_PHRASES["index"]
    yield ROOT / "lineage.html", COUNT_PHRASES["lineage"]
    for f in sorted((ROOT / "research").glob("*.html")):
        yield f, COUNT_PHRASES["article"]


def sync_counts(n: int) -> list[Path]:
    word = number_word(n)
    changed = []
    for f, patterns in count_targets():
        text = f.read_text()
        new = text
        for p in patterns:
            new = re.sub(p, lambda m: m.group(0).replace(
                m.group(1), word.capitalize() if m.group(1)[0].isupper() else word), new, flags=re.I)
        if new != text:
            f.write_text(new)
            changed.append(f)
    return changed


def bump_modified(paths, today: dt.date) -> None:
    sm = SITEMAP.read_text()
    for f in paths:
        t = f.read_text()
        t = re.sub(r'"dateModified": "\d{4}-\d{2}-\d{2}"', f'"dateModified": "{today}"', t)
        t = re.sub(r"Last updated: \d{1,2} [A-Z][a-z]+ \d{4}", f"Last updated: {long_date(str(today))}", t)
        f.write_text(t)
        rel = f.relative_to(ROOT).as_posix()
        sm = re.sub(rf"(<loc>{re.escape(SITE)}/{re.escape(rel)}</loc>\s*<lastmod>)[^<]+",
                    rf"\g<1>{today}", sm)
    SITEMAP.write_text(sm)


def git_changed() -> list[str]:
    out = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    paths = []
    for line in out.splitlines():
        p = line[3:].split(" -> ")[-1].strip('"')
        if not p.startswith(".scout/"):
            paths.append(p)
    return paths


# --- candidates ----------------------------------------------------------------------

def cmd_candidates(args) -> None:
    today = dt.date.today()
    since = today - dt.timedelta(days=args.days)
    query = (f"(TITLE_ABS:{TOPIC}) AND (TITLE_ABS:{PLACE}) "
             f"AND FIRST_PDATE:[{since} TO {today}] AND SRC:MED")
    results, cursor = [], "*"
    while len(results) < 300:
        page = get_json(EPMC, {"query": query, "format": "json", "pageSize": 100,
                               "resultType": "core", "cursorMark": cursor}) or {}
        batch = page.get("resultList", {}).get("result", [])
        results += batch
        nxt = page.get("nextCursorMark")
        if not batch or not nxt or nxt == cursor:
            break
        cursor = nxt

    known, screened = site_dois(), load_ledger()["screened"]
    out, seen, dropped = [], set(), 0
    for r in results:
        doi = (r.get("doi") or "").lower().strip()
        if not doi or doi in seen or doi in known or doi in screened:
            continue
        seen.add(doi)
        meta = crossref(doi)
        if not meta or meta["type"] != "journal-article" or not meta["date"]:
            dropped += 1
            continue
        out.append({**meta, "authors_short": authors_short(meta),
                    "abstract": clean(r.get("abstractText", "")), "pmid": r.get("pmid", "")})
    out.sort(key=lambda c: c["date"], reverse=True)

    WORK.mkdir(exist_ok=True)
    (WORK / "candidates.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    set_output("count", len(out))
    lines = [f"### Research scout: {len(out)} new candidate(s)",
             f"Searched Europe PMC for {since} to {today}: {len(results)} results; "
             f"{dropped} dropped by Crossref (not a journal article, or no date)."]
    lines += [f"- {c['date']} · {c['journal']} · {c['title']}" for c in out]
    step_summary("\n".join(lines))


# --- apply ---------------------------------------------------------------------------

def check_content(k: dict) -> list[str]:
    need = ["slug", "list_title", "finding", "description", "summary", "key_points", "relevance"]
    missing = [f for f in need if f not in k]
    if missing:
        return [f"missing {', '.join(missing)}"]
    lists_ok = all(isinstance(k[f], list) and k[f] and all(isinstance(x, str) and x.strip() for x in k[f])
                   for f in ("summary", "key_points", "relevance"))
    if not lists_ok or not all(isinstance(k[f], str) for f in ("slug", "list_title", "finding", "description")):
        return ["wrong field types"]
    L, p = LIMITS, []
    if not SLUG.match(k["slug"]) or re.search(r"\d{4}$", k["slug"]):
        p.append("slug must be lowercase words joined by hyphens, without a year")
    if len(k["list_title"]) > L["list_title_chars"]:
        p.append("list_title too long")
    if words(k["finding"]) > L["finding_words"]:
        p.append("finding too long")
    if not L["description_chars"][0] <= len(k["description"]) <= L["description_chars"][1]:
        p.append("description length out of range")
    if not L["summary_paras"][0] <= len(k["summary"]) <= L["summary_paras"][1] \
            or words(" ".join(k["summary"])) > L["summary_words"]:
        p.append("summary too long")
    if not L["key_points"][0] <= len(k["key_points"]) <= L["key_points"][1] \
            or any(words(x) > L["key_point_words"] for x in k["key_points"]):
        p.append("key_points out of range")
    if not L["relevance_paras"][0] <= len(k["relevance"]) <= L["relevance_paras"][1] \
            or words(" ".join(k["relevance"])) > L["relevance_words"]:
        p.append("relevance too long")
    prose = " ".join([k["list_title"], k["finding"], k["description"],
                      *k["summary"], *k["key_points"], *k["relevance"]])
    if MARKUP.search(prose):
        p.append("contains markup")
    if EMOJI.search(prose):
        p.append("contains emoji")
    return p


def unsupported_numbers(k: dict, c: dict) -> list[str]:
    """Numbers in the prose that appear nowhere in the title or abstract.

    Standalone numbers only: the digits inside E-PF2546 or H1-T16189C! are names,
    not claims, and are skipped.
    """
    source = (c["abstract"] + " " + c["title"]).replace(",", "")
    prose = " ".join([k["list_title"], k["finding"], *k["summary"], *k["key_points"], *k["relevance"]])
    missing = set()
    for tok in re.findall(r"(?<![\w-])\d[\d,.]*\d(?![\w-])", prose):
        t = tok.replace(",", "").rstrip(".")
        if t not in source and t != c["date"][:4]:
            missing.add(tok)
    return sorted(missing)


def render_item(c: dict, k: dict, file: str) -> str:
    e = lambda s: html.escape(s, quote=False)
    return (
        '\n                    <li class="paper">'
        '\n                        <div class="paper__when">'
        f'\n                            <span class="paper__year">{c["date"][:4]}</span>'
        f'\n                            <time class="paper__date" datetime="{c["date"]}">{long_date(c["date"], False)}</time>'
        '\n                        </div>'
        '\n                        <div>'
        f'\n                            <h3 class="paper__title"><a href="research/{file}">{e(k["list_title"])}</a></h3>'
        f'\n                            <p class="paper__finding">{e(k["finding"])}</p>'
        f'\n                            <p class="paper__meta">{e(authors_short(c))} &middot; <cite class="paper__journal">{e(c["journal"])}</cite>'
        f' &middot; <a href="https://doi.org/{html.escape(c["doi"])}">doi:{e(c["doi"])}</a></p>'
        '\n                        </div>'
        '\n                    </li>')


def render_page(c: dict, k: dict, file: str, today: dt.date, base: str, count: int) -> str:
    """Build a new article on top of an existing one, so header, nav and footer are
    always the site's current chrome rather than a copy that can drift."""
    e = lambda s: html.escape(s, quote=False)
    a = lambda s: html.escape(s, quote=True)
    url = f"{SITE}/research/{file}"
    doi = html.escape(c["doi"])
    year = c["date"][:4]
    head_title = f"{k['list_title']} | {authors_short(c)} {year}"
    para = lambda xs: "\n".join(f"                    <p>{e(x)}</p>" for x in xs)
    main = MAIN_TEMPLATE.read_text().strip()
    values = {
        "date_iso": c["date"], "date_long": long_date(c["date"]), "journal": e(c["journal"]),
        "paper_title": e(c["title"]), "authors_short": e(authors_short(c)), "doi": doi,
        "summary": para(k["summary"]), "relevance": para(k["relevance"]),
        "key_points": "\n".join(
            f'                    <div class="{BLOCKS[i % len(BLOCKS)]}"><p class="mb-0">{e(x)}</p></div>'
            for i, x in enumerate(k["key_points"])),
        "citation": e(citation(c)), "count_word": number_word(count),
        "updated_long": long_date(str(today)),
    }
    main = re.sub(r"\{\{(\w+)\}\}", lambda m: values[m.group(1)], main)
    ld = json.dumps({"@context": "https://schema.org", "@type": "ScholarlyArticle",
                     "headline": c["title"], "url": url, "inLanguage": "en",
                     "datePublished": c["date"], "dateModified": str(today),
                     "sameAs": f"https://doi.org/{c['doi']}"}, indent=2, ensure_ascii=False)
    ld = '<script type="application/ld+json">\n' + textwrap.indent(ld.replace("</", "<\\/"), "    ") + "\n    </script>"
    swaps = [
        (r"<title>.*?</title>", f"<title>{e(head_title)}</title>"),
        (r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{a(k["description"])}">'),
        (r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{a(head_title)}">'),
        (r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{a(k["description"])}">'),
        (r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">'),
        (r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{a(head_title)}">'),
        (r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{a(k["description"])}">'),
        (r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">'),
        (r'<link rel="alternate" hreflang="en" href="[^"]*">', f'<link rel="alternate" hreflang="en" href="{url}">'),
        (r'<link rel="alternate" hreflang="x-default" href="[^"]*">', f'<link rel="alternate" hreflang="x-default" href="{url}">'),
        (r'<script type="application/ld\+json">.*?</script>', ld),
        (r'<main id="main-content">.*?</main>', main),
    ]
    page = base
    for pattern, repl in swaps:
        page = sub_once(pattern, lambda _m, r=repl: r, page, re.S)
    return sub_once(r'(<a href="\.\./research\.html">Research</a> &rsaquo; )\d{4}',
                    lambda m: m.group(1) + year, page)


def add_to_sitemap(file: str, title: str, today: dt.date) -> None:
    entry = (f"  <!-- Research Article: {title.replace('--', '-')} -->\n"
             f"  <url>\n    <loc>{SITE}/research/{file}</loc>\n    <lastmod>{today}</lastmod>\n"
             f"    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n\n")
    sm = SITEMAP.read_text()
    SITEMAP.write_text(sub_once(r"</urlset>", lambda _m: entry + "</urlset>", sm))


def cmd_apply(args) -> None:
    cand_file = WORK / "candidates.json"
    candidates = {c["doi"]: c for c in json.loads(cand_file.read_text())} if cand_file.exists() else {}
    if not candidates:
        set_output("changed", "false")
        return
    decisions_file = WORK / "decisions.json"
    if not decisions_file.exists():
        raise SystemExit("Claude wrote no .scout/decisions.json")

    decisions, notes = {}, []
    for d in json.loads(decisions_file.read_text()).get("decisions", []):
        doi = str(d.get("doi", "")).lower().strip()
        verdict, reason = d.get("decision"), str(d.get("reason", "")).strip()
        if doi not in candidates:
            notes.append(f"Ignored a decision for `{doi}`, which was not a candidate.")
        elif verdict not in ("accept", "reject", "defer") or not reason:
            notes.append(f"Ignored a malformed decision for `{doi}`.")
        else:
            decisions[doi] = {"decision": verdict, "reason": reason}
    for doi in candidates.keys() - decisions.keys():
        decisions[doi] = {"decision": "defer", "reason": "No decision recorded; screened again next run."}

    contents = {}
    for f in sorted((WORK / "content").glob("*.json")):
        try:
            k = json.loads(f.read_text())
            contents[str(k.get("doi", "")).lower()] = k
        except (json.JSONDecodeError, AttributeError):
            notes.append(f"`{f.name}` is not a valid content file.")

    today = dt.date.today()
    index_text = INDEX.read_text()
    start, end, items, tail = index_items(index_text)
    base_page = (ROOT / item_fields(items[0])["href"]).read_text()
    added, review = [], []
    accepts = sorted((d for d, v in decisions.items() if v["decision"] == "accept"),
                     key=lambda d: candidates[d]["date"], reverse=True)
    for doi in accepts:
        c, k = candidates[doi], contents.get(doi)
        problems = check_content(k) if k else ["no content file"]
        if len(c["date"]) < 7:
            problems.append("Crossref gives no month for this paper")
        if c["date"] > str(today):  # no online date, so Crossref fell back to a future print issue
            problems.append(f"Crossref's date {c['date']} is still in the future")
        if len(added) >= MAX_ACCEPTS:
            problems.append(f"over the limit of {MAX_ACCEPTS} papers per run")
        if problems:
            decisions[doi] = {"decision": "defer", "reason": "Accepted but not published: " + "; ".join(problems)}
            continue
        file, n = f"{k['slug']}-{c['date'][:4]}.html", 2
        while (ROOT / "research" / file).exists():
            file, n = f"{k['slug']}-{c['date'][:4]}-{n}.html", n + 1
        (ROOT / "research" / file).write_text(
            render_page(c, k, file, today, base_page, len(items) + len(added) + 1))
        items.append(render_item(c, k, file))
        add_to_sitemap(file, k["list_title"], today)
        if missing := unsupported_numbers(k, c):
            review.append((c, k, file, missing))
        added.append((c, k, file))

    if added:
        items.sort(key=lambda i: item_fields(i)["date"], reverse=True)
        INDEX.write_text(index_text[:start] + "".join(items) + tail + index_text[end:])
        changed = sync_counts(len(items))
        bump_modified(set(changed) | {INDEX}, today)
        frag = ROOT / "changelog" / "unreleased" / f"research-scout-{today}.md"
        frag.parent.mkdir(parents=True, exist_ok=True)
        frag.write_text("### Added\n" + "".join(
            f"- Research summary: {k['list_title']} ({authors_short(c)}, {c['journal']}, "
            f"{long_date(c['date'])}), added by the weekly research scout\n" for c, k, _ in added))

    ledger = load_ledger()
    before = json.dumps(ledger, sort_keys=True)
    published = {c["doi"] for c, _, _ in added}
    for doi, d in decisions.items():
        if d["decision"] == "reject" or doi in published:
            c = candidates[doi]
            ledger["screened"][doi] = {"decision": d["decision"], "reason": d["reason"],
                                       "title": c["title"], "journal": c["journal"],
                                       "date": c["date"], "screened": str(today)}
    ledger["screened"] = dict(sorted(ledger["screened"].items()))
    ledger_changed = json.dumps(ledger, sort_keys=True) != before
    LEDGER.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n")

    if added:
        s = "y" if len(added) == 1 else "ies"
        subject = f"feat(research): add {len(added)} paper summar{s} from the weekly scout"
        body = "\n".join(f"- {authors_short(c)} ({c['date'][:4]}), {c['journal']}: {k['list_title']}"
                         for c, k, _ in added)
    else:
        s = "" if len(candidates) == 1 else "s"
        subject = f"chore(research-scout): screen {len(candidates)} candidate{s}, none added"
        body = "Every candidate was rejected or deferred; the ledger records why."
    (WORK / "commit-message.txt").write_text(f"{subject}\n\n{body}\n")

    cell = lambda s: s.replace("|", "\\|").replace("\n", " ")
    lines = [f"## Weekly research scout, {long_date(str(today))}", ""]
    if added:
        lines.append("**Added**")
        lines += [f"- [{k['list_title']}](research/{file}): {authors_short(c)}, *{c['journal']}*, "
                  f"{long_date(c['date'])}, [doi:{c['doi']}](https://doi.org/{c['doi']})"
                  for c, k, file in added]
    else:
        lines.append("**Nothing added this week.**")
    if review:
        lines += ["", "**Needs a human, so this PR was not merged automatically.** These summaries use "
                  "numbers that do not appear in the paper's title or abstract:"]
        lines += [f"- `research/{file}`: {', '.join(missing)}" for _, _, file, missing in review]
    lines += ["", "### Screened", "", "| Online | Journal | Paper | Decision | Reason |", "|---|---|---|---|---|"]
    for doi, d in sorted(decisions.items(), key=lambda x: candidates[x[0]]["date"], reverse=True):
        c = candidates[doi]
        lines.append(f"| {c['date']} | {cell(c['journal'])} | [{cell(c['title'])}](https://doi.org/{doi}) "
                     f"| {d['decision']} | {cell(d['reason'])} |")
    lines += ["", "Titles, journals, dates and authors come from Crossref. The summaries were written by "
              "Claude from the abstract alone. Before this PR was opened, `scout.py validate` checked every "
              "DOI, date and journal on the research page against Crossref."]
    if notes:
        lines += ["", "**Notes**", *[f"- {n}" for n in notes]]
    (WORK / "pr-body.md").write_text("\n".join(lines) + "\n")
    step_summary("\n".join(lines))

    set_output("changed", "true" if added or ledger_changed else "false")
    set_output("needs_review", "true" if review else "false")


# --- validate ------------------------------------------------------------------------

def cmd_validate(args) -> None:
    errors: list[str] = []
    _, _, items, _ = index_items(INDEX.read_text())
    listed = [item_fields(i) for i in items]
    n, word = len(listed), number_word(len(listed))
    if [x["date"] for x in listed] != sorted((x["date"] for x in listed), reverse=True):
        errors.append("research.html is not in newest-first order")
    if len({x["doi"] for x in listed}) != n:
        errors.append("research.html lists a DOI twice")

    sitemap, pages = SITEMAP.read_text(), {}
    for x in listed:
        f = ROOT / x["href"]
        if not f.exists():
            errors.append(f"{x['href']} is listed in research.html but does not exist")
            continue
        pages[f.name] = f
        page = f.read_text()
        kicker = re.search(r'class="kicker"><time datetime="([^"]+)">[^<]+</time> &middot; ([^<]+)</span>', page)
        if not kicker or kicker.group(1) != x["date"] or norm_journal(kicker.group(2)) != norm_journal(x["journal"]):
            errors.append(f"{x['href']}: kicker date/journal does not match research.html")
        published = re.search(r'"datePublished": "([^"]+)"', page)
        if not published or published.group(1) != x["date"]:
            errors.append(f"{x['href']}: JSON-LD datePublished does not match research.html")
        same = re.search(r'"sameAs": "https://doi\.org/([^"]+)"', page)
        if not same or same.group(1).lower() != x["doi"]:
            errors.append(f"{x['href']}: JSON-LD sameAs is not the listed DOI")
        for section in ("summary", "takeaways", "relevance"):
            if f'id="{section}"' not in page:
                errors.append(f"{x['href']}: missing the #{section} section")
        if f"<loc>{SITE}/{x['href']}</loc>" not in sitemap:
            errors.append(f"{x['href']} is missing from sitemap.xml")
        if not args.offline:
            cr = crossref(x["doi"])
            if not cr:
                errors.append(f"{x['doi']} does not resolve on Crossref")
            else:
                if cr["date"] != x["date"]:
                    errors.append(f"{x['doi']}: listed {x['date']}, Crossref says {cr['date']}")
                if norm_journal(cr["journal"]) != norm_journal(x["journal"]):
                    errors.append(f"{x['doi']}: listed in {x['journal']}, Crossref says {cr['journal']}")

    for f in sorted((ROOT / "research").glob("*.html")):
        if f.name not in pages and "noindex" not in f.read_text():
            errors.append(f"research/{f.name} exists but is not listed in research.html")

    for f, patterns in count_targets():
        if f.parent.name == "research" and f.name not in pages:
            continue  # the noindex redirect stub
        text = f.read_text()
        found = {m.group(1).lower() for p in patterns for m in re.finditer(p, text, re.I)}
        rel = f.relative_to(ROOT).as_posix()
        if not found:
            errors.append(f"{rel}: the paper-count sentence is missing")
        elif found != {word}:
            errors.append(f"{rel}: says {', '.join(sorted(found))} papers; research.html lists {n} ({word})")

    chrome: dict[str, list[str]] = {}
    for name, f in pages.items():
        t = f.read_text()
        parts = [m.group(0) if (m := re.search(p, t, re.S)) else ""
                 for p in (r'<header class="site-header".*?</nav>', r"<footer.*?</footer>")]
        chrome.setdefault(hashlib.sha1("".join(parts).encode()).hexdigest(), []).append(name)
    if len(chrome) > 1:
        groups = sorted(chrome.values(), key=len)
        errors.append(f"article header/nav/footer differ; odd one(s) out: {', '.join(groups[0])}")

    if args.check_changed:
        stray = [p for p in git_changed() if not ALLOWED.match(p)]
        if stray:
            errors.append("a scout run may not change: " + ", ".join(stray))

    if errors:
        step_summary("### Validation failed\n" + "\n".join(f"- {e}" for e in errors))
        raise SystemExit(1)
    step_summary(f"Validation passed: {n} papers, count reads \"{word}\" everywhere"
                 + ("" if args.offline else ", every DOI matches Crossref") + ".")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("candidates")
    c.add_argument("--days", type=int, default=28)
    sub.add_parser("apply")
    v = sub.add_parser("validate")
    v.add_argument("--offline", action="store_true", help="skip the Crossref checks")
    v.add_argument("--check-changed", action="store_true", help="fail on changes outside the scout allowlist")
    args = ap.parse_args()
    {"candidates": cmd_candidates, "apply": cmd_apply, "validate": cmd_validate}[args.cmd](args)


if __name__ == "__main__":
    main()
