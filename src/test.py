from pattern.web import Twitter, plaintext
from pattern.en import tag, parse

def classify_qa(tweet):
    if "?" in tweet:
        return "question"
    else:
        return "statement"

twitter = Twitter(language='en')

input = raw_input(">>> ")
while input != "exit":
    if classify_qa(input) == "question":
        print("question")
    else:
        print("statement")
    input = raw_input(">>> ")

'''
question = "How are you?"

print parse(question).split()
        
for tweet in twitter.search('"A am feeling"', count=1, cached=False):
    print plaintext(tweet.text)
    
question = "Do you like apple pie?"

print parse(question).split()
for tweet in twitter.search('"like apple pie"', count=1, cached=False):
    print plaintext(tweet.text)
'''
