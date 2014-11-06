from parseTwitter import retrieveTweetText
from tweets2query import QueryGenerator

if __name__ == "__main__":
    qgen = QueryGenerator()
    hashtag = "bigbang"
    tweets = retrieveTweetText(hashtag)
    print "number of tweets: ", len(tweets)
    query_list = qgen.gen_query_list('#'+hashtag, tweets)
    print "Query list for \"%s\" is " % hashtag
    print query_list

