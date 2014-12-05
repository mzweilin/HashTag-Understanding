import twitter
import json
import unicodedata
import re
import operator

jsonResults = []
twitter_api = ''
K = 2

# Use this module by running either 
# getJSON(hashtag), or retrieveTweetText(hashtag)
# both return an array of either JSON or tweet text elements
# After calling retrieveTweetText(), you can call 
# getOtherHashtags(hashtag), which returns all other 
# hashtags in the tweets with the original hashtag




def retrieveTweetText(hashtag, hundredsOfTweets=2, filterTrends=False, caseSensitive = False, filterURL=True, filterEmoticons=True):
	
	
	global K

	K = hundredsOfTweets
	initOauth()
	global jsonResults
	jsonResults = collectSearchResults(hashtag)
	status_texts = [ result['text'] for result in jsonResults ]

	#Find current trending hashtags
	if (filterTrends == True):
		currTrends = getTrendingHashtags()
		try:
			currTrends.remove(hashtag)
		except ValueError:
			pass
	else:
		currTrends = []

	#print currTrends


	tweetTexts = []
	for i in range(0,len(status_texts)):
		json_i = jsonResults[i]
		tags = [ unicodedata.normalize('NFKD', hTag['text']).encode('ascii','ignore').translate(None, '#') for hTag in json_i['entities']['hashtags'] ]
		otherTags = [x for x in tags if x.lower() != hashtag.replace("#","").lower()]

		#Count number of trending hashtags
		count = 0
		for trend in currTrends:
			#print unicodedata.normalize('NFKD', trend).encode('ascii','ignore').translate(None, '#')
			if (unicodedata.normalize('NFKD', trend).encode('ascii','ignore').translate(None, '#').replace("#","") in otherTags):
				count += 1

		#Remove links
		if filterURL == True:
			status_texts[i] = re.sub(r"(http|https)://\S+", "", status_texts[i])

		#Remove emoticons
		if filterEmoticons == True:
			status_texts[i] = unicode(re.sub(r"\\u\S+", "", unicodedata.normalize('NFKD', status_texts[i]).encode('ascii','ignore')))

		#Remove usernames
		#status_texts[i] = unicode(re.sub(r"(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)", "", unicodedata.normalize('NFKD', status_texts[i]).encode('ascii','ignore')))

		if count < 2:
			TEXT = (json.dumps(status_texts[i], indent=1))[1:-1]
			if caseSensitive == True:
				if hashtag in TEXT:
					tweetTexts.append(TEXT)
			else:
				tweetTexts.append(TEXT)

	return tweetTexts


# returns a list of related hashtags
def retrieveRelatedHashtags(hashtag, hundredsOfTweets=2, filterTrends=True, caseSensitive=True):
	global K
	initOauth3()
	global jsonResults
	jsonResults = collectSearchResults(hashtag)
	status_texts = [ result['text'] for result in jsonResults ]
	K = hundredsOfTweets
	tags = [ unicodedata.normalize('NFKD', hTag['text']).encode('ascii','ignore') for json_i in jsonResults for hTag in json_i['entities']['hashtags'] ]

	#Find current trending hashtags
	if (filterTrends == True):
		currTrends = getTrendingHashtags()
		try:
			currTrends.remove(hashtag)
		except ValueError:
			pass

	else:
		currTrends = []

	print tags
	hashtagsDict = {}
	hashtagNoPound = hashtag.replace("#","")

	stoptags = ['viral', 'trendingcontentnow', 'now', 'trending', 'news']
	for i in range(0,len(tags)):
		if (tags[i].lower() != hashtagNoPound.lower()):
			key = (tags[i])
			if caseSensitive==True:
				key = key.lower()
			if key in hashtagsDict:
				hashtagsDict[key] += 1
			else:
				if (not any(key in s for s in stoptags)):
					hashtagsDict[key] = 1

		
	hashtagsDict = sorted(hashtagsDict.items(), key=operator.itemgetter(1), reverse=True)	

	print hashtagsDict

	hashtags = []
	for i in range(0,5):
		try:
			add = True
			for trend in currTrends:
				if hashtagsDict[i][0] == trend.replace("#",""):
					add = False
			if add == True:
				hashtags.append(hashtagsDict[i][0])
		except IndexError:
			pass

	return hashtags

def getJSON(hashtag, hundredsOfTweets):
	global K
	K = hundredsOfTweets
	initOauth()
	global jsonResults
	jsonResults = collectSearchResults(hashtag)

	jsonFormatted = []
	for i in range(0,len(jsonResults)):
		jsonFormatted.append(str(json.dumps(jsonResults[i], indent=1)))

	return jsonFormatted


######################################################################
######################################################################
######################################################################
######################################################################


def initOauth():
    CONSUMER_KEY = 'K1CCjIXC8ELhqMAkkupTWdQXG'
    CONSUMER_SECRET ='bHo0rpEE4QdFB881I84fs5SiUGY5iTjhGTHz5mjOYmT48cmIHX'
    OAUTH_TOKEN = '2600337966-UyPLjWM0h4HXzJkMvZjakCYtyRdaTi6mMZn6sBd'
    OAUTH_TOKEN_SECRET = 'vfocB9vdoLCF6xRXgultKxtIbGAUnUO3N9x80EYKsk6lC'

    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

    global twitter_api
    twitter_api = twitter.Twitter(auth=auth)

def initOauth2():
    CONSUMER_KEY = 'QgDCQP2o0CG9tWEsRhZRtJLVC'
    CONSUMER_SECRET ='6QkU5doMb7cWScAiIA7ctAG9tnFUbwBphEB6TtKRVP64UzOGbM'
    OAUTH_TOKEN = '2600337966-AuLnwDSIx3k5FwRskDrOr8CfDkuVZVseN2cMt4e'
    OAUTH_TOKEN_SECRET = 'r33d6YKClInk7yeMsLcllWvSMpK0OhSSQbqO4DTEGlBVY'

    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

    global twitter_api
    twitter_api = twitter.Twitter(auth=auth)

def initOauth3():
    CONSUMER_KEY = 'gnu6shRgmWWJujZo0CTIunCij'
    CONSUMER_SECRET ='AvtUORKpdwEfINtXdT0nCGZGWsZNQYf1oYBEl9zlv9mzbrwfqR'
    OAUTH_TOKEN = '2600337966-yLgN6hjuWGAF7sA3D0FoGJNwGoQbflc6yGfdL10'
    OAUTH_TOKEN_SECRET = 'Bm8OZVZPTVrrcL01dPuLkVBoBdIb50iwTAZhGg7qifx8Q'

    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

    global twitter_api
    twitter_api = twitter.Twitter(auth=auth)

    

#################### Retrieving trends #####################
def getTrendingHashtags():
    # The Yahoo! Where On Earth ID for the entire world is 1.
    # See https://dev.twitter.com/docs/api/1.1/get/trends/place and
    # http://developer.yahoo.com/geo/geoplanet/

	WORLD_WOE_ID = 1
	US_WOE_ID = 23424977

    # Prefix ID with the underscore for query string parameterization.
    # Without the underscore, the twitter package appends the ID value
    # to the URL itself as a special case keyword argument.

	world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
	us_trends = twitter_api.trends.place(_id=US_WOE_ID)

	trendingHashtags = []
	for trend in us_trends[0]['trends']:
		if "#" in trend['name']:
			trendingHashtags.append(trend['name'])

    #print type(json.dumps(world_trends, indent=1))
	return trendingHashtags


################ Collecting search results #################
def collectSearchResults(hashtag):

    count = 100

    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets
    removedRT = hashtag + '-filter:retweets'
    search_results = twitter_api.search.tweets(q=removedRT, count=count)

    jsonResults = search_results['statuses']


    # Iterate through K more batches of results by following the cursor
    global K
    K = K - 1
    for _ in range(K):
        #print("Length of jsonResults", len(jsonResults))
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError as e: # No more results when next_results doesn't exist
            break
            
        # Create a dictionary from next_results, which has the following form:
        # ?max_id=313519052523986943&q=NCAA&include_entities=1
        kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])
        
        x = unicodedata.normalize('NFKD',  kwargs[u'max_id']).encode('ascii','ignore')

        search_results = twitter_api.search.tweets(q=removedRT, count=count, max_id=x)
        jsonResults += search_results['statuses']


    # Show one sample search result by slicing the list...
    # print(str(json.dumps(jsonResults[0], indent=1)))

    return jsonResults

  




    #############################################################
    ## Extracting text, screen names, and hashtags from tweets ##
    #############################################################
def getData(jsonResults):     

	jsonResults = jsonResults

	status_texts = [ status['text'] for status in jsonResults ]

	screen_names = [ user_mention['screen_name'] 
	                 for status in jsonResults
	                     for user_mention in status['entities']['user_mentions'] ]

	hashtags = [ hashtag['text'] 
	             for status in jsonResults
	                 for hashtag in status['entities']['hashtags'] ]


	#hashtags = [ hashtag['text'] for hashtag in status['entities']['hashtags'] ]

	# Compute a collection of all words from all tweets
	words = [ w for t in status_texts 
	              for w in t.split() ]

	# Explore the first 5 items for each...

	# print(json.dumps(status_texts[0:5], indent=1))
	# print(json.dumps(screen_names[0:5], indent=1))
	# print(json.dumps(hashtags[0:5], indent=1))
	# print(json.dumps(words[0:5], indent=1))


	return status_texts

if __name__ == "__main__":
	hashtag = "ahsfreakshow"
	t = retrieveTweetText(hashtag)
	for tw in t:
		print(tw)