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
qgen.set_params(segmt_flag=True, stemming_flag=False, stopwords_flag=True, ngram_threshold=0.15, distinct_query=True, top_k_unigram=2)

query_list = qgen.gen_query_list(hashtag, tweets)

print("\nQuery list for \"%s\" is " % hashtag)
print(query_list)
