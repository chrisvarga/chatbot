import re, math
from collections import Counter
from pattern.vector import Document, Model, TFIDF, KMEANS, count, COSINE, HIERARCHICAL
from pattern.db import Datasheet, pd

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

def rank_response(tweets, inp):
    responses = []
    for tweet in tweets:
        x = get_cosine(vec(tweet), vec(inp))
        responses.append({x : tweet})
    return sorted(responses, reverse=True)

def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def vec(text):
    WORD = re.compile(r'\w+')
    words = WORD.findall(text)
    return Counter(words)

def classify_question(tweet):
    if "?" in tweet or tweet.startswith("why") or tweet.startswith("how"):
        return 1
    else:
        return 0

def basic_cluster(tweets):
    questions = []
    statements = []

    for tweet in tweets:
        if classify_question(tweet):
            questions.append(tweet)
        else:
            statements.append(tweet)

    return questions, statements

table = Datasheet.load(pd("tweets.csv"))
tweets = []

for tweet in table:
    tweets.append(tweet[1])

inp = raw_input("$ ")
while inp != 'exit':
    tweets = kmeans_cluster(inp)
    print rank_response(tweets, inp)[0].values()[0]
    inp = raw_input("$ ")

