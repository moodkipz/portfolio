import praw
import sqlite3
import os
from dotenv import load_dotenv
from textblob import TextBlob

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
id = os.getenv("CLIENT_ID")
secret = os.getenv("SECRET_KEY")
user = os.getenv("USER_AGENT")

# Creating a read-only PRAW instance
reddit_read_only = praw.Reddit(client_id = id,
                               client_secret = secret,
                               user_agent = user)

# Initialize DB connection and DB handle
conn = sqlite3.connect('politicsdata.sqlite')
cur = conn.cursor()

# Create tables only if they don't exist
cur.executescript('''
CREATE TABLE IF NOT EXISTS Threads (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    thread_title TEXT UNIQUE,
    utc_posted TEXT,
    upvotes INTEGER,
    title_sentiment REAL
);

CREATE TABLE IF NOT EXISTS Comments (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    thread_id INTEGER,
    author_id INTEGER,
    comment_text TEXT,
    comment_sentiment REAL
);

CREATE TABLE IF NOT EXISTS Authors(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
)

''')

# Get the top 10 hot /r/politics threads
politics_sub = reddit_read_only.subreddit('politics')

# Loop through each thread
for thread in politics_sub.hot(limit=10):
    # Analyze thread title sentiment
    title_sentiment = TextBlob(thread.title).sentiment.polarity

    # Insert data into threads table
    cur.execute('''INSERT INTO Threads (thread_title, utc_posted, upvotes, title_sentiment) 
    VALUES (?, ?, ?, ?)''', (thread.title, thread.created_utc, thread.score, title_sentiment))

    # Set thread_id var to prepare insertion into comments table
    thread_id = cur.lastrowid
    conn.commit()
    # Loop through comments in thread and insert data
    for comment in thread.comments.list():
        
        if isinstance(comment, praw.models.MoreComments):
            continue
        
        # Analyze comment sentiment
        comment_sentiment = TextBlob(comment.body).sentiment.polarity

        if comment.author is None:
            continue
        # Check if author exists in Authors table, if not, inserts author
        author = comment.author

        cur.execute(
            '''SELECT * FROM Authors WHERE name = ?''',
            (author.name,),
        )
        row = cur.fetchone()
        if row is None:
            cur.execute('''INSERT INTO Authors (name) VALUES (?)''',
                        (author.name,),
                        )
            author_id = cur.lastrowid
        else:
            author_id = row[0]

        # Insert comment data into Comments table
        cur.execute('''INSERT INTO Comments (thread_id, author_id, comment_text, comment_sentiment)
        VALUES (?, ?, ?, ?)''', (thread_id, author_id, comment.body, comment_sentiment))

# Commit changes to the database
conn.commit()