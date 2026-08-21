# ADR 001: Use Reddit RSS Feeds Instead of the Official Data API (PRAW)

## Status
Accepted

## Context
Original plan was to extract reddit posts via PRAW using reddit's official data API,
registering for script. It was cooked cus as of 2026, reddit closed their self-service registration for new Data API access. Hence, page for singing up fails and requires manual approval, where odds are you'll get a rejection weeks later for a small, non-commercial, personal project. I tried signing up manually, but dev are expected to work on their new devvit and if you can't reason why not, and your app has to be something to serve of the reddit community. 

## My Other Options 
Webscraping vs RSS 
SSR is better architecturally and safer, as its very legal + no perms bypssed, and reddit built it
Webscraping no no because kinda illegal ( reddit doesnt permit ) + need to work around bot detection, captcha, very much need maintainance, also scrappers fetch html n slowly look for
info, if reddit redesign, its also cooked

## Decision
Extract Reddit data via public RSS feeds (`reddit.com/r/<subreddit>/new/.rss`)
instead of PRAW/the official Data API.

This required no change to the pipeline's overall architecture: the
`RedditDataSource` extraction layer was already designed behind an
adapter-pattern interface, specifically to isolate the pipeline from
changes to how any one source is accessed. Swapping the internal
implementation from PRAW to an RSS parser (`feedparser`) required no
changes to downstream transform, classification, dedup, or load logic.


## Consequences

**Positive:**
- Unblocked development immediately, no approval wait
- No API credentials to manage/secure for this source
- RSS is a publicly offered, sanctioned Reddit feature — lower legal/ToS
  ambiguity than scraping rendered pages
- Validates the adapter-pattern design decision made earlier: source
  volatility was anticipated, and the pivot cost nothing architecturally

**Trade-offs / limitations accepted:**
- RSS feeds return only recent posts (no deep historical backfill)
- Limited fields available (title, summary/snippet, link, publish date) —
  no full post body guaranteed, no comments ( which we dont need anyways)
- Feed format/availability is not contractually guaranteed by Reddit the
  way an API would be; could change without notice
- If official Data API access is later approved, may be worth migrating
  back for richer data — the `RedditDataSource` interface makes this a
  contained change, not a rebuild

  "RSS is rate-limited to ~1 req/min globally, so a full source sweep takes ~6 min; acceptable for scheduled runs, and fetch is decoupled from transform so development doesn't require re-fetching." T