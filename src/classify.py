#
# just experimenting with some basic classification
# we should eventually look into some real machine
# learning algorithms for better results
#

from pattern.db import Datasheet, pd

def classify_question(tweet):
    if "?" in tweet or tweet.startswith("why") or tweet.startswith("how"):
        return 1
    else:
        return 0

table = Datasheet.load(pd("tweets.csv"))

num_questions = 0
num_tweets = len(table)

for tweet in table:
    num_questions += classify_question(tweet[1])

print("total tweets: " + str(num_tweets))
print("number of questions: " + str(num_questions))
print("percentage of questions: " +
        str(round(float(num_questions)/num_tweets,2)) + "%")
