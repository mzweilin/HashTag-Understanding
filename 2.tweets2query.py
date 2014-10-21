


output = "twitter blade"

class QueryGenerator:
    def __init__(self, freq_n_grams, top_k_terms):
        self.freq_n_grams = freq_n_grams
        self.top_k_terms = top_k_terms

    def get_top_grams(self, string):
        return []


    def generate_query_list(self, hashtag, tweets):
        # 1. #hashtag itself, segmentation without #.
        # 2. top high-frequent n-grams (n: 1, 2, 3)
        return ["#twitterblade", "twitter blade", "twitterblade sufc"]

def test():
    from sample_data import tweet_collection

    qgen = QueryGenerator(freq_n_grams = [1,2,3], top_k_terms = 10)

    for (hashtag, tweets) in tweet_collection.items():
        query_list = qgen.generate_query_list(hashtag, tweets)
        print "Query list for \"%s\" is " % hashtag
        print query_list

if __name__ == "__main__":
    test()