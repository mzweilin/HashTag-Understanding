import lib.search.bing_search as bing
import lib.tweet.parseTwitter as twitter
from lib.querygen.tweets2query import QueryGenerator 
import string

def main():
    job  = Job(" #hello_world")
    urls = job.execute()
    print(urls)

class Job: 
    def __init__(self, hashtag):
        self.hashtag = hashtag.strip("#" + string.whitespace)

    def execute(self):
        results = {}
        results['references'] = self.getURLs()
        results['similar-tags'] = self.getSimilarHashTags()
        return results

    def getSimilarHashTags(self):
        return twitter.retrieveRelatedHashtags(self.hashtag)

    def getURLs(self):
        urls = []
        generator = QueryGenerator()
        tweets = twitter.retrieveTweetText(self.hashtag, 5)
        queries = generator.gen_query_list(self.hashtag, tweets)
        for query in queries: 
            if isinstance(query, list): 
                query = " ".join(query)
            urls = urls + bing.search(query, 5)
        return urls

if __name__ == "__main__":
    main()
