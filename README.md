# Public Tenders & Procurement API — EU TED, UK Find a Tender, SAM.gov (Python, Node.js, cURL)

![Public tenders and contract awards from EU TED, UK Find a Tender, Contracts Finder, SAM.gov and Grants.gov in one table](https://raw.githubusercontent.com/tidydata-dev/tidydata-dev/main/assets/apify/public-tenders-scraper.png)

Search **government tenders, public procurement opportunities and contract awards** from the official sources of the **EU, the UK and the US** with one call, and get them back in **one schema**: buyer, contact, deadline, estimated value, CPV / NAICS codes, documents and submission links, and for awards the **winning companies and awarded value**.

| Source | Coverage |
|---|---|
| **EU TED** (Tenders Electronic Daily) | 27 EU countries + EEA, above-threshold tenders, prior information notices, awards |
| **UK Find a Tender** | UK above-threshold + Procurement Act 2023 notices |
| **UK Contracts Finder** | UK below-threshold public contracts |
| **US SAM.gov** | Federal contract opportunities (solicitations, sources sought, awards) |
| **US Grants.gov** | Federal grants (posted and forecasted) |

This repo shows how to call the hosted **[Public Tenders & Procurement Scraper on Apify](https://apify.com/tidydata/public-tenders-scraper?fpr=wtg6qt)** from your code. It costs **$3 per 1,000 notices**; empty searches are free. No SAM.gov API key, no TED account, no proxies.

## Why not call TED, SAM.gov and Contracts Finder directly?

You can — they are open data. But each one has its own query language, paging rules and quirks: TED's expert search syntax and its 1,000-result window, SAM.gov's `application/hal+json` and API key, OCDS releases on the UK side, different value and date formats everywhere. The Actor turns all five into the same columns, filters by keyword, CPV (children included), NAICS, country, value and date, and remembers what you already saw for **daily alerts**.

## Quick start (Python)

```bash
pip install apify-client
export APIFY_TOKEN=...   # free account at apify.com → Settings → API & Integrations
```

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("tidydata/public-tenders-scraper").call(run_input={
    "keywords": ["software", "cloud"],
    "sources": ["ted", "uk-find-a-tender", "uk-contracts-finder", "sam-gov"],
    "noticeTypes": ["tender"],          # also "planned", "award", "grant"
    "postedWithinDays": 3,
    "onlyOpen": True,
    "maxResultsPerSource": 50,
})
for t in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(t["source"], "|", t["title"][:70], "|", t.get("buyerName"), "|", t.get("deadline"), t.get("estimatedValue"), t.get("currency"))
```

More: [`examples/daily_alerts.py`](examples/daily_alerts.py) (only new tenders, appended to a CSV, ready for cron) · [`examples/who_wins.py`](examples/who_wins.py) (contract awards: who wins what, and for how much) · [`examples/node.mjs`](examples/node.mjs) · [`examples/curl.sh`](examples/curl.sh) · [`sample_output.json`](sample_output.json) (a real run)

## Daily tender alerts

Set `"onlyNew": true` and a `memoryName` per client or search: each run returns **only the notices you have not received yet**. Run it from cron, GitHub Actions or an Apify schedule and send the result to email, Slack or Google Sheets.

```python
run = client.actor("tidydata/public-tenders-scraper").call(run_input={
    "cpvCodes": ["72000000"],           # all IT services (children included)
    "countries": ["DE", "FR", "NL"],
    "minValue": 100000,
    "postedWithinDays": 2,
    "onlyNew": True,
    "memoryName": "it-benelux-dach",
})
```

## What you get per notice

| field | what it is |
|---|---|
| `source`, `sourceName`, `noticeId`, `url`, `pdfUrl` | where it comes from and the official notice |
| `noticeType`, `noticeTypeOriginal` | `tender`, `planned`, `award` or `grant`, plus the source's own type |
| `title`, `titleEn`, `description`, `language` | original title, TED's English heading, scope as text |
| `buyerName`, `buyerCountry`, `buyerCity`, `buyerEmail`, `buyerPhone`, `buyerWebsite`, `contactName` | who buys and how to reach them |
| `publishedAt`, `deadline` | publication date and submission deadline |
| `estimatedValue`, `currency` | estimated value as published |
| `cpvCodes`, `cpvMain`, `cpvDescription`, `naicsCodes`, `pscCode` | classification codes |
| `category`, `procedureType`, `isFramework`, `setAside` | services / supplies / works, procedure, framework, SAM.gov set-asides |
| `documentsUrl`, `submissionUrl`, `placeOfPerformance` | tender documents and where to submit |
| `winners`, `awardValue`, `awardCurrency` | awards: winning companies and value |

A real run (12 notices, contacts hidden here) is in [`sample_output.json`](sample_output.json).

## Use it from no-code tools

The Actor works with **Make, Zapier, n8n**, webhooks and schedules, and as a tool for AI agents through the Apify MCP server — see the [Actor page](https://apify.com/tidydata/public-tenders-scraper?fpr=wtg6qt).

## Data and licences

All sources are official open data: EU TED (free reuse, including commercial, from the Publications Office of the EU), UK notices under the Open Government Licence v3.0, SAM.gov and Grants.gov US federal public data. Buyer contact details are published by the buyers for bidders; use them for that purpose and follow the privacy rules that apply to you.

## Related

- [Merge, Deduplicate & Transform Datasets](https://apify.com/tidydata/merge-dedupe-datasets?fpr=wtg6qt) — combine several tender searches into one deduplicated sheet.
- [Google Sheets Export & Import](https://apify.com/tidydata/google-sheets-export-import?fpr=wtg6qt) — send the alerts straight to a Google Sheet.
- [Company Registry Lookup](https://apify.com/tidydata/company-registry-lookup?fpr=wtg6qt) — look up winners and buyers in official company registers.

Examples in this repo are MIT-licensed.

---
<sub>Links to apify.com include our affiliate ID: if you start a paid Apify plan through them, Apify pays TidyData a commission at no extra cost to you.</sub>
