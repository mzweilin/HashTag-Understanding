import twitter
import json

jsonResults = []
twitter_api = None

# Use this module by running either 
# retrieveJSON(hashtag), or retrieveTweetText(hashtag)
# both return an array of either JSON or tweet text elements
# After calling retrieveTweetText(), you can call 
# retrieveOtherHashtags(hashtag), which returns all other 
# hashtags in the tweets with the original hashtag

def retreiveJSON(hashtag):
	initOauth()
	global jsonResults
	jsonResults = collectSearchResults(hashtag)

	jsonFormatted = []
	for i in range(0,len(jsonResults)):
		jsonFormatted.append(str(json.dumps(jsonResults[i], indent=1)))

	return jsonFormatted


def retreiveTweetText(hashtag):
	initOauth()
	global jsonResults
	jsonResults = collectSearchResults(hashtag)
	status_texts = [ result['text'] for result in jsonResults ]

	tweetTexts = []
	for i in range(0,len(status_texts)):
		tweetTexts.append((json.dumps(status_texts[i], indent=1))[1:-1])

	return tweetTexts

# returns all other hashtags in the tweets with the original hashtag
def retrieveOtherHashtags(origHashtag):
	tags = [ hTag['text'] 
					for json_i in jsonResults
						for hTag in json_i['entities']['hashtags'] ]


	hashtags = []
	for i in range(0,len(tags)):
		if ((json.dumps(tags[i], indent=1)[1:-1]).lower() != origHashtag.lower()):
			hashtags.append((json.dumps(tags[i], indent=1)[1:-1]))

	return hashtags


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

#################### Retrieving trends #####################
def retreiveTrends():
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

    print json.dumps(world_trends, indent=1)
    print
    print json.dumps(us_trends, indent=1)


################ Collecting search results #################
def collectSearchResults(hashtag):

    count = 100

    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets

    search_results = twitter_api.search.tweets(q=hashtag, count=count)

    jsonResults = search_results['statuses']


    # Iterate through K more batches of results by following the cursor
    K = 0
    for _ in range(K):
        print "Length of jsonResults", len(jsonResults)
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError, e: # No more results when next_results doesn't exist
            break
            
        # Create a dictionary from next_results, which has the following form:
        # ?max_id=313519052523986943&q=NCAA&include_entities=1
        kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])
        
        search_results = twitter_api.search.tweets(**kwargs)
        jsonResults += search_results['jsonResults']


    # Show one sample search result by slicing the list...
    # print str(json.dumps(jsonResults[0], indent=1))

    return jsonResults



    #############################################################
    ## Extracting text, screen names, and hashtags from tweets ##
    #############################################################
def retrieveData(jsonResults):     

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

	print json.dumps(status_texts[0:5], indent=1)
	print json.dumps(screen_names[0:5], indent=1) 
	print json.dumps(hashtags[0:5], indent=1)
	print json.dumps(words[0:5], indent=1)


	return status_texts

if __name__ == "__main__":
	hashtag = "ahsfreakshow"
	t = retreiveTweetText(hashtag)
	for tw in t:
		print tw
