// Open tenders from the last 3 days. npm i apify-client
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('tidydata/public-tenders-scraper').call({
    keywords: ['software'],
    sources: ['ted', 'uk-find-a-tender', 'uk-contracts-finder', 'sam-gov'],
    noticeTypes: ['tender'],
    postedWithinDays: 3,
    maxResultsPerSource: 20,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const t of items) console.log(t.source, '|', t.title, '|', t.buyerName, '|', t.deadline);
