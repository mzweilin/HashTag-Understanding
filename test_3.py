import lib.search.bing_search as bing
import string

urls = []
queries = ['sufc twitterblades', 'blades twitter', '#twitterblades']
for query in queries:
    if isinstance(query, list):
        query = " ".join(query)
    query = query.replace("#", "%23")
    print query
    urls = urls + bing.search(query, 5)
print urls

