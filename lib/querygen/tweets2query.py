import string, nltk
from collections import Counter
from nltk.stem.snowball import EnglishStemmer
from wordsegment import segment

stemmer = EnglishStemmer()
tokenizer = nltk.tokenize.treebank.TreebankWordTokenizer()
punc_list = list(string.punctuation)

class QueryGenerator:
    def __init__(self, ngrams_tops = {1:3, 2: 1, 3:1}):
        #self.freq_n_grams = freq_n_grams
        #self.top_k_terms = top_k_terms
        self.ngrams_tops = {1:3, 2: 1, 3:1}
        self.stemming = False

        self.counters = {}
        

    def gen_query_list(self, hashtag, tweets):
        q_list = []
        q_list.append("#"+hashtag)
        segs = segment(hashtag)
        if len(segs) > 1:
        	q_list.append(segs)

        doc_str = ""
        for tweet in tweets:
            #doc_str += tweet['content'] + ' '
            doc_str += tweet + ' '

        self.analyse_doc(doc_str)

        for (n, tops) in self.ngrams_tops.items():
            q_list.append(self.get_sorted_tokens(n, tops))

        return q_list

    def analyse_doc(self, doc):
        tokens = self.str2tokens(doc)

        for n in self.ngrams_tops.keys():
            self.counters[n] = Counter()
            self.counters[n].update(self.tokens2ngrams(tokens, n))

    def get_sorted_counts(self, ngram, tops = None):
        return [tup[1] for tup in self.counters[ngram].most_common(tops)]
    
    def get_sorted_tokens(self, ngram, tops = None):
        return [tup[0] for tup in self.counters[ngram].most_common(tops)]

    def str2tokens(self, doc_str):
        tokens = []
        for token in tokenizer.tokenize(doc_str):
            if token in punc_list:
                continue
            if self.stemming:
            	token_norm = stemmer.stem(token.lower())
            else:
            	token_norm = token.lower()
            tokens.append(token_norm)
        return tokens

    def tokens2ngrams(self, tokens, n):
        if n == 1:
            return tokens
        
        ret = []
        for i in range(0, len(tokens)-n+1):
            ngrams = []
            for j in range(0,n):
                ngrams.append(tokens[i+j])
            ret.append(' '.join(ngrams))
        return ret 
        
    def get_top_grams(self, string):
        return []


    def generate_query_list(self, hashtag, tweets):
        # 1. #hashtag itself, segmentation without #.
        # 2. top high-frequent n-grams (n: 1, 2, 3)
        return ["#twitterblade", "twitter blade", "twitterblade sufc"]

def test():
    #from sample_data import tweet_collection
    #import os
    #os.chdir('../')
    from tweet.parseTwitter import retrieveTweetText

    hashtag = "twitterblades"
    tweets = retrieveTweetText(hashtag)
    tweet_collection = ((hashtag, tweets))

    qgen = QueryGenerator()

    for (hashtag, tweets) in tweet_collection:
        query_list = qgen.gen_query_list(hashtag, tweets)
        print("Query list for \"%s\" is " % hashtag)
        print(query_list)

if __name__ == "__main__":
    test()
