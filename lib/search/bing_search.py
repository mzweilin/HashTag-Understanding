import logging
from collections import Counter
from bing_search_api import BingSearchAPI
my_key = "urTuvjb7b6dFiCmC3Jj6ZAxuX8DqyXwQRDccSEQJVbc"
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

def group_search(query_list, num_results, category='Web', on_wiki=False, on_ubd=False, exclude_twitter=True, weight_step=3):
    url_counter = Counter()
    for j in range(len(query_list)):
        query = query_list[j]
        if exclude_twitter == True and on_wiki == False and on_ubd == False:
            query += " -site:twitter.com"
        if on_wiki == True:
            query += " site:en.wikipedia.org"
        if on_ubd == True:
            query += " site:www.urbandictionary.com"
        urls = search(query, num_results+5, category)
        if on_wiki == True or on_ubd == True:
            stop_urls = ['http://www.wikipedia.org/', 'http://en.wikipedia.org/wiki/Main_Page', 'http://www.urbandictionary.com/', 'http://www.urbandictionary.com/random.php']
            for stop_url in stop_urls:
                if stop_url in urls:
                    urls.remove(stop_url)
        for i in range(len(urls)):
            url = urls[i]
            url_counter[url] += float(1)/weight_step**float(i) /(0.1*j+1)
    logging.info(url_counter.most_common(num_results+1))
    return [tup[0] for tup in url_counter.most_common(num_results)]

if __name__ == "__main__":
    main()
