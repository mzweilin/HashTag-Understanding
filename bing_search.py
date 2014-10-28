# Attribution for the following code:
# http://www.guguncube.com/2771/python-using-the-bing-search-api

import urllib
import urllib.request
import json
 
def main():
    query = "#test"
    print(bing_search(query, 'Web'))
 
def bing_search(query, search_type):
    #search_type: Web, Image, News, Video
    key= 'MEL5FOrb1H5G1E78YY8N5mkfcvUK2hNBYsZl1aAEEbE' #TODO free tier key, should probably be in private keys file
    query = urllib.parse.quote(query)
    # create credential for authentication
    user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'
    credentials = (':%s' % key).encode()[:-1]
    auth = 'Basic %s' % credentials
    url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/'+search_type+'?Query=%27'+query+'%27&$top=5&$format=json'
    request = urllib.request.Request(url)
    request.add_header('Authorization', auth)
    request.add_header('User-Agent', user_agent)
    request_opener = urllib.request.build_opener()
    response = request_opener.open(request) 
    response_data = response.read()
    json_result = json.loads(response_data)
    result_list = json_result['d']['results']
    return result_list
 
if __name__ == "__main__":
    main()
