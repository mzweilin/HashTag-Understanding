import bing_search as bing
import parseTwitter as twitter
from tweets2query import QueryGenerator 
import string

def main():
    req  = Request(" #hello_world")
    urls = req.execute()
    print(urls)

class Request:
    def __init__(self, hashtag):
        self.hashtag = hashtag.strip("#" + string.whitespace)

    def execute(self):
        generator = QueryGenerator()
        tweets = twitter.retrieveTweetText(self.hashtag)
        query_terms = generator.gen_query_list(self.hashtag, tweets)
        self.query = query_terms[0] #TODO fix this
        urls = bing.search(self.query, 10)
        return urls

if __name__ == "__main__":
    main()
