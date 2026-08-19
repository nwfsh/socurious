import feedparser
from dataclasses import dataclass, field
from datetime import datetime, timezone

# feedparser is python library that reads and process RSS


REDDIT_RSS_URL = "https://www.reddit.com/r/{subreddit}/new/.rss"
# adding user_agent since reddit blocks user agents 
USER_AGENT = "socurious-pipeline/0.1 (personal project, read-only RSS)"


@dataclass
class RawPost:
    source_name: str    # name of subreddit r/AskReddit 
    post_id: str        # reddit short post id 
    author: str | None # reddit username incase of potential problems 
    title: str
    body: str | None
    url: str
    scraped_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class RedditRSSAdapter:
    def __init__(self, subreddits: list[str]):
        self.subreddits = subreddits
    
    # loops through subreddit list and calls fetch on all
    def fetch_all(self) -> list[RawPost]:
        posts = []
        for subreddit in self.subreddits:
            posts.extend(self._fetch(subreddit))
        return posts

    # builds RSS URL and hands to feedparser, then wrap every entry in raw post 
    def _fetch(self, subreddit: str) -> list[RawPost]:
        url = REDDIT_RSS_URL.format(subreddit=subreddit)
        feed = feedparser.parse(url, agent=USER_AGENT)

        posts = []
        for entry in feed.entries:
            author = entry.get("author") or None
            if author and author.startswith("/u/"):
                author = author[3:] # ignores the /u/ and grab the rest of their username

              # how the data is stored work   
            posts.append(RawPost(
                source_name=f"r/{subreddit}",
                post_id=_extract_post_id(entry.link),
                author=author,
                title=entry.title,
                body=entry.get("summary") or None,
                url=entry.link,
            ))
        return posts


# helper function to extract an id, using /comments/ as a stopping point 
def _extract_post_id(link: str) -> str:
    # https://www.reddit.com/r/AskReddit/comments/abc123/title/ → abc123
    parts = link.split("/comments/")
    if len(parts) > 1:
        return parts[1].split("/")[0]
    return link
