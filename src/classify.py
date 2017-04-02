#
# just experimenting with some basic classification
# we should eventually look into some real machine
# learning algorithms for better results
#

from pattern.db import Datasheet, pd
from pattern.vector import Document, Model, KMEANS, count, COSINE, HIERARCHICAL, TFIDF
from random import choice
from pattern.en import wordnet

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
        if i == 10:
            break
        d = Document(tweet[1], name=tweet[1])
        docs = docs + (d,)
        i = i + 1

    # add input to data
    x = Document(inp, name=inp)
    docs = docs + (x,)
    m = Model(docs)
    m.reduce(5)

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
#############################################################################


#Get subjects based on the imput sentence
def get_input_subjects(sentence):
    words = list(sentence.split())
    newList = list(sentence.split())
    newSentence = words
    #For each word get some new words that deal with it.
    for word in words:
        try:
            newWord = wordnet.synsets(word)[0]
            for synonyms in newWord.synonyms:
                if synonyms not in newList:
                    newList.append(synonyms)
            for antonym in newWord.antonym:
                if antonym not in newList:
                    newList.append(antonym)
            for hypernyms in newWord.hypernyms:
                if hypernyms not in newList:
                    newList.append(hypernyms)
            for hyponyms in newWord.hyponyms:
                if hyponyms not in newList:
                    newList.append(hyponyms)
        
        except:
            pass
    
    #Stick them all back together
    try:
        newSentence = " ".join(newList)
    except:
        pass
    return Document(newSentence).vector

#Get Tweets based on subjects from a set file, maxTweet is the total amount
#of tweets it looks for 
def get_tweets_with_subject(subjects, dbFile, maxTweet):
    
    #Load DB
    table = Datasheet.load(pd(dbFile))

    tweets = []
    #For each tweet check if the subject matchs any from the input
    for tweet in table:
        tweetDoc =  Document(tweet[1])
        #This is where it matches from the list of subjects
        results = any(x in tweetDoc.vector for x in subjects)
        if results:
            tweets.append(tweet[1])
        #If it reaches the maximum end early
        if len(tweets) > maxTweet:
            return tweets
    return tweets

#Uses tfidf with LSA see https://technowiki.wordpress.com/2011/08/27/latent-semantic-analysis-lsa-tutorial/
def get_tfidf(inp, sentences):
    
    #Place the input into the first node
    ds = [Document(inp, name='input')]
    thisType = 0
    
    #For each sentence add a Document node
    for x in range(len(sentences)):
        newDoc = Document(sentences[x], name=str(x))
        ds.append(newDoc)
        thisType = thisType + 1
    
    #Create the TFIDF Model
    model = Model(documents=ds, weight=TFIDF)
    
    bestScore = 0
    bestTweet = ""
    #Find which sentence matches the most.
    for x in range(1, len(ds)):
        if model.similarity(ds[0], ds[x]) > bestScore:
            bestScore = model.similarity(ds[0], ds[x])
            bestTweet = ds[x]
    
    #This will happen when the scores remain all zeros
    if bestTweet == "":
        bestTweet = "I am sorry I do not understand"
    #Turn it back into the sentence
    else:
        bestTweet = sentences[int(bestTweet.name)]

    return bestTweet
    