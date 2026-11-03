#!/usr/bin/env bash
# One call, results as JSON (waits up to 5 minutes).
curl -s -X POST "https://api.apify.com/v2/acts/tidydata~public-tenders-scraper/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keywords":["software"],"sources":["ted","sam-gov"],"noticeTypes":["tender"],"postedWithinDays":3,"maxResultsPerSource":10}'
