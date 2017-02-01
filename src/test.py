from pattern.web import Twitter, plaintext
from pattern.en import tag, parse

twitter = Twitter(language='en')

question = "How are you?"

print parse(question).split()
        
for tweet in twitter.search('"A am feeling"', count=1, cached=False):
    print plaintext(tweet.text)
    
question = "Do you like apple pie?"

print parse(question).split()
for tweet in twitter.search('"like apple pie"', count=1, cached=False):
    print plaintext(tweet.text)

