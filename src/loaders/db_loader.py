import psycopg
from src.adapters.reddit_rss import RedditRSSAdapter
import time
import os
from dotenv import load_dotenv
from collections import Counter
from src.transform.filters import should_reject


load_dotenv()

def main():
    # grab sources, then close the connection so it doesnt sit idle during the sleeps
    # (the db server drops idle connections, which crashed the commit at the end)
    with psycopg.connect(os.getenv("DATABASE_URL")) as conn:
        sources = conn.execute("SELECT id,name FROM sources").fetchall()

    # fetch everything first, no db connection open
    fetched = []
    for i, (source_id, source_name) in enumerate(sources):
        if i > 0:
            time.sleep(65)
        posts = RedditRSSAdapter([source_name]).fetch_all()
        print(f"{source_name}: fetched {len(posts)}")
        fetched.append((source_id, posts))

    total = sum(len(posts) for _, posts in fetched)
    if total == 0:
        # every feed came back empty, fail loudly instead of passing with nothing
        raise SystemExit("fetched 0 posts from every source, reddit feeds are probably blocked")

    # now open a fresh connection just for the inserts
    with psycopg.connect(os.getenv("DATABASE_URL")) as conn:
        for source_id, posts in fetched:
            for post in posts:
                conn.execute(
                    """
                    INSERT INTO raw_questions (source_id, post_id, raw_title, url, author)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (source_id, post_id) DO NOTHING
                    """,
                    ##  old posts wont get inserted into database
                    (source_id, post.post_id, post.title, post.url, post.author),
                )
        conn.commit()

    print(f"total fetched: {total}")


if __name__ == "__main__":
    main()
