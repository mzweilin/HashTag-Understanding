import string, nltk
from collections import Counter
from nltk.stem.snowball import EnglishStemmer
from wordsegment import segment
from lib.tweet import parseTwitter

stemmer = EnglishStemmer()
tokenizer = nltk.tokenize.treebank.TreebankWordTokenizer()
punc_list = list(string.punctuation)

def get_stopwords(file_name = './stopwords.txt'):
    lines = open(file_name).readlines()
    return [line.strip()  for line in lines]

stopwords = get_stopwords('./english.stop')
extra_stopwords = ["'s", "''", "...", "--", "n't", "\\n"]
for word in extra_stopwords:
    stopwords.append(word)

class QueryGenerator:
    def __init__(self, segmt_flag=False, stemming_flag=False, stopwords_flag=True, ngram_threshold=0.15, distinct_query=False, top_k_unigram=2):
        self.set_params(segmt_flag, stemming_flag, stopwords_flag, ngram_threshold, distinct_query, top_k_unigram)
        self.ngrams_tops = {1:2, 2: 1, 3:1}
        self.counters = {}

    def set_params(self, segmt_flag=False, stemming_flag=False, stopwords_flag=True, ngram_threshold=0.15, distinct_query=False, top_k_unigram=2):
        self.segmentation = segmt_flag
        self.stemming = stemming_flag
        self.stopwords_filter = stopwords_flag

        # only if the count of top 1 bigram/trigram reaches 
        # the certain fraction of the count of top 1 unigram, 
        # do we consider it as a search query.
        self.n_gram_threshold = ngram_threshold

        # Sometimes the combined unigrams may be the same combination as those in bigram/trigram.
        self.dinstinct_query = distinct_query

        # combine top k unigram to form a query.
        self.top_k_unigram = top_k_unigram
        
    #expected input likes: hashtag="#twitterblades"
    def gen_query_list(self, hashtag, tweets):
        q_list = []
        q_list.append(hashtag)

        
        if self.segmentation:
            segs = segment(hashtag[1:])
            if len(segs) > 1:
                q_list.append(' '.join(segs))

        # relatedHashtags = parseTwitter.retrieveRelatedHashtags(hashtag)
        # if self.segmentation:
        #     for tag in relatedHashtags:
        #         segs = segment(tag[1:])
        #         if len(segs) > 1:
        #             q_list.append(' '.join(segs))


        # doc_str = ""
        # for tweet in tweets:
        #     #doc_str += tweet['content'] + ' '
        #     doc_str += tweet + ' '

        # self.analyse_doc(doc_str)

        for n in self.ngrams_tops.keys():
            self.counters[n] = Counter()

        for tweet in tweets:
            tokens = self.str2tokens(tweet)

            for n in self.ngrams_tops.keys():
                #self.counters[n] = Counter()
                ngrams_list = self.tokens2ngrams(tokens, n)
                ngrams_list = list(set(ngrams_list))
                self.counters[n].update(ngrams_list)

        #for ngram in [1,2,3]:
        #    print self.counters[ngram].most_common(10)

        tops_unigram = self.get_sorted_tokens(1, self.top_k_unigram)
        if len(tops_unigram) > 0:
            for i in range(2, len(tops_unigram)+1):
                subset = tops_unigram[:i]
                if len(subset) > 0:
                    q_list.append(' '.join(subset))
            #q_list.append(' '.join(tops_unigram))
            # without the hashtag itself.
            q_list.append(' '.join(tops_unigram[1:]))

        unigram_top1_count = self.get_sorted_counts(1, 1)[0]

        for n in [2,3]:
            ngram_top1_count = self.get_sorted_counts(n, 1)[0]

            if ngram_top1_count > unigram_top1_count * self.n_gram_threshold:
                q_list.append(' '.join(self.get_sorted_tokens(n, 1)))

        if self.dinstinct_query == True:
            q_list = self.distinct_query_list(q_list)
        return q_list

    def preview_counters(self):
        ret = ''
        for ngram in [1,2,3]:
            ret += "%s\n" % str(self.counters[ngram].most_common(10))
        return ret

    def distinct_query_list(self, query_list):
        for i in range(len(query_list)):
            q = query_list[i]
            q = q.split()
            q.sort()
            q = ' '.join(q)
            query_list[i] = q
        query_set = set(query_list)
        ret = list(query_set)
        return ret

    # def analyse_doc(self, doc):
    #     tokens = self.str2tokens(doc)
    #
    #     for n in self.ngrams_tops.keys():
    #         self.counters[n] = Counter()
    #         self.counters[n].update(self.tokens2ngrams(tokens, n))

    def get_sorted_counts(self, ngram, tops = 1):
        length = len(self.counters[ngram])
        if length < 1:
            return [0]
        if length < tops:
            tops = length
        return [tup[1] for tup in self.counters[ngram].most_common(tops)]
    
    def get_sorted_tokens(self, ngram, tops = None):
        return [tup[0] for tup in self.counters[ngram].most_common(tops)]

    def str2tokens(self, doc_str):
        tokens = []
        for token in tokenizer.tokenize(doc_str):
            if token in punc_list:
                continue
            if self.stemming:
                token_norm = stemmer.stem(token)
            else:
                token_norm = token.lower()

            if self.stopwords_filter and token_norm in stopwords:
                continue
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
