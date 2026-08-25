import psycopg
from src.adapters.reddit_rss import RedditRSSAdapter 
import time 
import os
from dotenv import load_dotenv
from collections import Counter
from src.transform.filters import should_reject


load_dotenv()

#psycopg is a python library that allows u to connect
# postgres to python code, for u to run sql commands in python 

# connect to the database 
conn = psycopg.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
)

# grab sources from database 
sources = conn.execute("SELECT id,name FROM sources").fetchall()
raw_rows = conn.execute("SELECT id, raw_title FROM raw_questions").fetchall()

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
            (source_id, post.post_id, post.title, post.url, post.author),
        )
        
        
    print(f"{source_name}: fetched {len(posts)}")



conn.commit()
conn.close()

