import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# Connect to the database
conn = sqlite3.connect('politicsdata.sqlite')

# Read the threads table
threads_df = pd.read_sql_query("SELECT id AS thread_id, thread_title, title_sentiment FROM Threads", conn)

# Read the comments table
comments_df = pd.read_sql_query("SELECT thread_id, comment_sentiment FROM comments", conn)

# Join the two tables on thread_id
joined_df = pd.merge(threads_df, comments_df, on='thread_id')

# Select required columns
final_df = joined_df[['thread_title', 'title_sentiment', 'comment_sentiment']]

# Group by thread_title and calculate mean sentiment
grouped_df = final_df.groupby('thread_title').agg({'title_sentiment': 'mean', 'comment_sentiment': 'mean'})

# Plot the sentiment values
fig, ax = plt.subplots(figsize=(10,8))
grouped_df.plot(kind='barh', ax=ax)
ax.set_xlabel('Sentiment')
ax.set_ylabel('Thread Title')
ax.set_title('Thread Sentiment and Overall Comment Sentiment')
plt.show()

