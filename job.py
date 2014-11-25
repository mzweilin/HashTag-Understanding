import bing_search as bing
import parseTwitter as twitter
from tweets2query import QueryGenerator 
import string

def main():
    job  = Job(" #hello_world")
    urls = job.execute()
    print(urls)

class Job: 
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
