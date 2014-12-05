import lib.search.bing_search as bing

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

# keywords = ['twitter', 'blades', 'sufc']
#queries = ['#twitterblades', 'sufc', 'twitterblades sufc', 'sufc twitterblades']
#queries = ['#pangu', 'pangu jailbreak', 'jailbreak pangu']
queries = ['#pangu', 'jailbreak', 'jailbreak pangu', 'jailbreak pangu']
#queries = ['']
#queries = ['#pangu']

urls = bing.group_search(queries, 2)
print urls