#
# just experimenting with some basic classification
# we should eventually look into some real machine
# learning algorithms for better results
#

from pattern.db import Datasheet, pd
from pattern.vector import Document, Model, KMEANS, count, COSINE, HIERARCHICAL
from random import choice

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

    i = 0
    for tweet in table:
        if i == 5:
            break
        i = i + 1
        if classify_question(tweet[1]):
            questions.append(tweet[1])
        else:
            statements.append(tweet[1])

    return questions, statements

def kmeans_cluster(inp):
    table = Datasheet.load(pd("tweets.csv"))

    i = 0
    docs = ();
    for tweet in table:
        if i == 100:
            break
        d = Document(tweet[1], name=tweet[1])
        docs = docs + (d,)
        i = i + 1

    # cluster input with similar tweets
    x = Document(inp, name=inp)
    docs = docs + (x,)
    m = Model(docs)
    clusters = m.cluster(method=KMEANS, k=10, iterations=10, distance=COSINE)
    #clusters = m.cluster(method=HIERARCHICAL, k=1, iterations=1000, distance=COSINE)

    responses = []
    for c in clusters:
        for tweet in c:
            if tweet.name == inp:
                for tweet in c:
                    if tweet.name != inp:
                        responses.append(tweet.name)
    return responses

def rank_response(responses, inp):
    best = []
    for r in responses:
        x = num_common_nouns(r, inp)
        best.append({x : r})
    return sorted(best)

def num_common_nouns(r, inp):
    pass
    #words = parse(r)

def latent_semantic_analysis(inp):

    table = Datasheet.load(pd("tweets.csv"))

    i = 0
    docs = ();
    for tweet in table:
        if i == 5:
            break
        d = Document(tweet, name=tweet)
        docs = docs + (d,)
        i = i + 1

    # add input to data
    x = Document(inp, name=inp)
    docs = docs + (x,)
    m = Model(docs)
    m.reduce(2)

    print "the topics are:"
    topics = []
    for topic in m.lsa.concepts[0].keys():
        topics.append(topic)
    print sorted(topics)

    for d in m.documents:
        print
        print "tweet: " + d.name
        for concept, w1 in m.lsa.vectors[d.id].items():
            for feature, w2 in m.lsa.concepts[concept].items():
                if w1 != 0 and w2 != 0:
                    print (feature, w1 * w2)

inp = raw_input("$ ")
while inp != 'exit':
    responses = kmeans_cluster(inp)
    print choice(responses)
    #latent_semantic_analysis(inp)
    inp = raw_input("$ ")

