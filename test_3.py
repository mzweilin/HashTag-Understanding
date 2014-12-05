import lib.search.bing_search as bing
import string
from collections import Counter

# def match_url_keywords(url, keywords):
#     sentences = get_sentences_from_url(url)
#     weights = Counter()
#     for sentence in sentences:
#         tokens = tokenize(sentence)
#         for token in tokens:
#             if token in keywords:
#                 weights[token] += 1
#     return weights

"http://www.wikipedia.org/"

url_counter = Counter()
# keywords = ['twitter', 'blades', 'sufc']
#queries = ['#twitterblades', 'sufc', 'twitterblades sufc', 'sufc twitterblades']
#queries = ['#pangu', 'pangu jailbreak', 'jailbreak pangu']
queries = ['#pangu', 'jailbreak', 'jailbreak pangu', 'jailbreak pangu']
#queries = ['']
#queries = ['#pangu']
for query in queries:
    if isinstance(query, list):
        query = " ".join(query)
    query = query.replace("#", "%23")
    print query
    on_wiki = False
    query += " -site:twitter.com"
    if on_wiki == True:
        query += " site:wikipedia.org"
    urls = bing.search(query, 20)
    for i in range(len(urls)):
        url = urls[i]
        print url
        url_counter[url] += float(1)/3**float(i)
print url_counter.most_common(10)

