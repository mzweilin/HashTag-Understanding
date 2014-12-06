import lib.search.bing_search as bing
import lib.tweet.parseTwitter as twitter
from lib.querygen.tweets2query import QueryGenerator 
import lib.summarization.tagdef as tagdef
from lib.summarization import extractor
import string

import logging
logging.basicConfig(level=logging.INFO)
logger = logging

def main():
    import sys
    if len(sys.argv) >= 2:
        hashtag = '#'+sys.argv[1]
    job  = Job(hashtag)
    urls = job.execute()
    print(urls)

class Job: 
    def __init__(self, hashtag):
        self.hashtag = hashtag.strip("#" + string.whitespace)

    def execute(self):
        results = {}
        results['references'] = self.getURLs()
        #results['similar-tags'] = self.getSimilarHashTags()
        #results['tagdef-summary'] = self.getTagDefSummary()
        urls = results['references']['ubd'] + results['references']['wiki'] + results['references']['web'] + results['references']['news']
        #results['summary'] = self.getSummary(urls)
        return urls

    def getSimilarHashTags(self):
        return twitter.retrieveRelatedHashtags('#' + self.hashtag)

    def getSummary(self, urls):
        num_sentences = 10
        return extractor.summarize(urls, num_sentences)

    def getTagDefSummary(self):
        return tagdef.lookup(self.hashtag)

    def getURLs(self):
        generator = QueryGenerator()
        tweets = twitter.retrieveTweetText('#'+self.hashtag, 5)
        queries = generator.gen_query_list('#'+self.hashtag, tweets)

        logger.info(generator.preview_counters())
        logger.info(queries)

        urls_ubd = bing.group_search(queries, 2, on_ubd=True, weight_step=3)
        urls_wiki = bing.group_search(queries, 2, on_wiki=True)
        urls_news = bing.group_search(queries, 2, category='News', on_wiki=False)
        urls_web = bing.group_search(queries, 2, on_wiki=False)
        return {'ubd':urls_ubd, 'wiki': urls_wiki, 'news': urls_news, 'web': urls_web}


if __name__ == "__main__":
    main()
