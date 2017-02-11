#
# db.py
#  grow tweets.csv with new unique tweets
#

import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from pattern.web import Twitter, hashtags
from pattern.db  import Datasheet, pprint, pd

try:
    table = Datasheet.load(pd("tweets.csv"))
    index = set(table.columns[0])
except:
    table = Datasheet()
    index = set()

engine = Twitter(language="en")
prev = None

for i in range(2):
    print(i)
    for tweet in engine.search("i", start=prev, count=100, cached=False):
        print("")
        print(tweet.text)
        print(tweet.author)
        print(tweet.date)
        print(hashtags(tweet.text))  # Keywords in tweets start with a "#"
        print("")
        # Only add the tweet to the table if it doesn't already exist
        if len(table) == 0 or tweet.id not in index:
            table.append([tweet.id, tweet.text])
            index.add(tweet.id)
        # Continue mining older tweets in next iteration
        prev = tweet.id

# save to .csv in current directory
table.save(pd("tweets.csv"))

print("Total results: %s" % len(table))
print("")

# Print all the rows in the table.
# Since it is stored as a CSV-file it grows comfortably each time the script runs.
# We can also open the table later on: in other scripts, for further analysis, ...
pprint(table, truncate=100)

# Note: we can also search tweets by author:
# Twitter().search("from:funtime_bobby")
