import psycopg
from src.adapters.reddit_rss import RedditRSSAdapter 

#psycopg is a python library that allows u to connect
# postgres to python code, for u to run sql commands in python 

# connect to the database 
conn = psycopg.connect("dbname=question_pipeline user=averychong")

#run a query
result = conn.execute("SELECT * FROM sources")

for row in result:
    print(row)

conn.close()