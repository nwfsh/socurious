import psycopg
from src.adapters.reddit_rss import RedditRSSAdapter
import time
import os
from dotenv import load_dotenv
from collections import Counter
from src.transform.filters import should_reject


load_dotenv()

def main():
    conn = psycopg.connect(
        os.getenv("DATABASE_URL")
    )

    # grab sources from database
    sources = conn.execute("SELECT id,name FROM sources").fetchall()

    # PLS COMPLETE QUERY
    for source_id, source_name in sources:
        subreddit = source_name
        adapter = RedditRSSAdapter([subreddit])
        posts = adapter.fetch_all()
        print(f"{source_name}: fetched {len(posts)}")
        time.sleep(65)
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


        print(f"{source_name}: fetched {len(posts)}")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
