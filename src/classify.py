#
# just experimenting with some basic classification
# we should eventually look into some real machine
# learning algorithms for better results
#

from pattern.db import Datasheet, pd
from pattern.vector import Document, Model, KMEANS, count, COSINE

def classify_question(tweet):
    if "?" in tweet or tweet.startswith("why") or tweet.startswith("how"):
        return 1
    else:
        return 0

def get_total_questions(file_name):
    table = Datasheet.load(pd(file_name))

    num_questions = 0
    num_tweets = len(table)

    for tweet in table:
        num_questions += classify_question(tweet[1])

    print("total tweets: " + str(num_tweets))
    print("number of questions: " + str(num_questions))
    print("percentage of questions: " +
            str(round(float(num_questions)/num_tweets,2)*100) + "%")
    return num_questions

def basic_cluster():
    table = Datasheet.load(pd("tweets.csv"))

    questions = []
    statements = []

    for tweet in table:
        if classify_question(tweet[1]):
            questions.append(tweet[1])
        else:
            statements.append(tweet[1])

    return questions, statements

def kmeans_cluster():
    table = Datasheet.load(pd("tweets.csv"))

    i = 0
    docs = ();
    for tweet in table:
        if i == 100:
            break
        d = Document(tweet[1], name=tweet[1])
        docs = docs + (d,)
        i = i + 1

    m = Model(docs)
    clusters = m.cluster(method=KMEANS, k=10, iterations=10, distance=COSINE)
    for c in clusters:
        print "cluster"
        for tweet in c:
            print tweet.name
        print

def latent_semantic_analysis():

    table = Datasheet.load(pd("tweets.csv"))
    i = 0

    docs = ();
    for tweet in table:
        if i == 10:
            break
        d = Document(tweet[1], name=tweet[1])
        docs = docs + (d,)
        i = i + 1

    m = Model(docs)
    m.reduce(5)


    for d in m.documents:
        print
        print "tweet: " + d.name
        for concept, w1 in m.lsa.vectors[d.id].items():
            for feature, w2 in m.lsa.concepts[concept].items():
                if w1 != 0 and w2 != 0:
                    print (feature, w1 * w2)

# print each tweet with a probability of it being in each topic
latent_semantic_analysis()
