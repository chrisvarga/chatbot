from all_imports import *

#Common values for easy use
databaseFileName = "tweets.csv"
groupsize = 100
maxRounds = 2


#db.update_db(databaseFileName, "i", 1000, False)


total = 0
found = 0
#This Whole loop thing needs to be fixed. Other options wont take the first input
f = open("testSentences.txt")
line = f.readline()
while line != "":
    #Get input
    inp = line
    print(inp)
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
        #db.update_db(databaseFileName, inp.split(' ')[0], 1000, False) 
        rounds = rounds + 1
    
    #Print the best result from all that was found.
    response = classify.get_tfidf(inp, similarTweets)
    print (response)
    if response != "I am sorry I do not understand":
        found = found + 1
    total = total + 1
    line = f.readline()
print("Total sentences:", total)
print("Total found:", found)
print("percentage:", (float(found)/float(total)))

