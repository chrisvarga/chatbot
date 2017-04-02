from all_imports import *

#Common values for easy use
databaseFileName = "tweets.csv"
groupsize = 20
maxRounds = 2


db.update_db(databaseFileName, "i", 1000, False)

#This Whole loop thing needs to be fixed. Other options wont take the first input
inp = None    
while inp != 'exit':
    #Get input
    inp = raw_input("$ ")
    
    
    #Get all of inputs subjects
    subjects = classify.get_input_subjects(inp)
    
    
    #Get tweets until group size is reached, stops if rounds get to high to
    #prevent over requesting from twitter
    rounds = 0
    similarTweets = []
    while len(similarTweets) < groupsize:
        #This is where it gets the similar tweets from the DB
        similarTweets = classify.get_tweets_with_subject(subjects, databaseFileName, groupsize)
        if rounds > maxRounds:
            break
        db.update_db(databaseFileName, inp.split(' ')[0], 1000, False) 
        rounds = rounds + 1
    
    #Print the best result from all that was found.
    print (classify.get_tfidf(inp, similarTweets))
    