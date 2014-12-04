from lib.tweet.parseTwitter import retrieveTweetText
from lib.querygen.tweets2query import QueryGenerator

import sys

hashtag = '#'+sys.argv[1]
  
# hashtag = "#twitterblades"
# #hashtag = "#uva"
# hashtag = "#IAD"
# #hashtag = "#lab14"
# #hashtag = "#oitnb"

tweets = retrieveTweetText(hashtag, 3, 1, 1, 1)
for t in tweets:
    print "==>", t

qgen = QueryGenerator()


query_list = qgen.gen_query_list(hashtag, tweets, stopwords_filter=True, stemming=False)
print("Query list for \"%s\" is " % hashtag)
print(query_list)
