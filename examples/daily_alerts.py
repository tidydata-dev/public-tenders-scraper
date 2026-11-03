"""Daily tender alerts: only notices not seen before, appended to tenders.csv. Run it from cron or GitHub Actions.
pip install apify-client"""
import csv, os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("tidydata/public-tenders-scraper").call(run_input={
    "keywords": ["software", "cyber security"],
    "sources": ["ted", "uk-find-a-tender", "uk-contracts-finder", "sam-gov"],
    "noticeTypes": ["tender", "planned"],
    "postedWithinDays": 2,
    "onlyOpen": True,
    "onlyNew": True,                 # remembers what earlier runs returned
    "memoryName": "my-daily-alert",  # one memory per search or client
    "maxResultsPerSource": 200,
})
cols = ["source", "noticeType", "title", "buyerName", "buyerCountry", "deadline", "estimatedValue", "currency", "cpvDescription", "url"]
rows = list(client.dataset(run["defaultDatasetId"]).iterate_items())
new_file = not os.path.exists("tenders.csv")
with open("tenders.csv", "a", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
    if new_file:
        w.writeheader()
    w.writerows(rows)
print(f"{len(rows)} new notices added to tenders.csv")
