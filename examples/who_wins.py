"""Contract awards: who wins public IT contracts and for how much (EU TED + UK). pip install apify-client"""
import collections, os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("tidydata/public-tenders-scraper").call(run_input={
    "cpvCodes": ["72000000", "48000000"],   # IT services + software packages
    "sources": ["ted", "uk-find-a-tender", "uk-contracts-finder"],
    "noticeTypes": ["award"],
    "postedWithinDays": 30,
    "onlyOpen": False,
    "maxResultsPerSource": 300,
})
count = collections.Counter()
value = collections.defaultdict(collections.Counter)   # winner -> {currency: total}
for a in client.dataset(run["defaultDatasetId"]).iterate_items():
    for w in a.get("winners") or []:
        count[w] += 1
        if a.get("awardValue"):
            value[w][a.get("awardCurrency") or "?"] += a["awardValue"]
for w, n in count.most_common(15):
    money = ", ".join(f"{v:,.0f} {c}" for c, v in value[w].items()) or "value not published"
    print(f"{n:3} awards  {w}  ({money})")
