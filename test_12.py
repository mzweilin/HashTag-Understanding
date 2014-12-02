from lib.tweet.parseTwitter import retrieveTweetText
from lib.querygen.tweets2query import QueryGenerator
    
hashtag = "twitterblades"
tweets = retrieveTweetText(hashtag)

qgen = QueryGenerator()


query_list = qgen.gen_query_list(hashtag, tweets)
print("Query list for \"%s\" is " % hashtag)
print(query_list)
