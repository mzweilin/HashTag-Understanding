from collections import Counter
from bing_search_api import BingSearchAPI
my_key = "MEL5FOrb1H5G1E78YY8N5mkfcvUK2hNBYsZl1aAEEbE"
bing = BingSearchAPI(my_key)

def main():
    print(search("Hello", 3))

# category='Web' or category='News'
def search(query_string, num_results, category='Web'):
    query_string = query_string.replace("#", "%23")
    params = {'ImageFilters':'"Face:Face"',
              '$format': 'json',
              '$top': num_results,
              '$skip': 0}
    results = bing.search(category,query_string,params).json() # requests 1.0+ 

    return [result['Url'] for result in results['d']['results'][0][category]]

def group_search(query_list, num_results, category='Web', on_wiki=True, exclude_twitter=True):
    url_counter = Counter()
    for query in query_list:
        if exclude_twitter == True:
            query += " -site:twitter.com"
        if on_wiki == True:
            query += " site:wikipedia.org"
        urls = search(query, num_results)
        for i in range(len(urls)):
            url = urls[i]
            url_counter[url] += float(1)/3**float(i)
        
    return [tup[0] for tup in url_counter.most_common(num_results)]

if __name__ == "__main__":
    main()
