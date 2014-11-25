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
        urls = []
        generator = QueryGenerator()
        tweets = twitter.retrieveTweetText(self.hashtag, 5)
        queries = generator.gen_query_list(self.hashtag, tweets)
        for query in queries: 
            if isinstance(query, list): 
                query = " ".join(query)
            urls.append(bing.search(query, 5))
        return urls

if __name__ == "__main__":
    main()
