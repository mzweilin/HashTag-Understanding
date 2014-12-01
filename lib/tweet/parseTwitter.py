import twitter
import json
import unicodedata

filterTrends = 1
jsonResults = []
twitter_api = ''
K = 2



# Use this module by running either 
# retrieveJSON(hashtag), or retrieveTweetText(hashtag)
# both return an array of either JSON or tweet text elements
# After calling retrieveTweetText(), you can call 
# retrieveOtherHashtags(hashtag), which returns all other 
# hashtags in the tweets with the original hashtag




def retrieveTweetText(hashtag, *hundredsOfTweets):
	global K
	if len(hundredsOfTweets) == 0:
		K = 1
	else:
		K = hundredsOfTweets[0]
	initOauth()
	global jsonResults
	jsonResults = collectSearchResults(hashtag)
	status_texts = [ result['text'] for result in jsonResults ]

	if (filterTrends == 1):
		currTrends = retrieveTrends()
		try:
			currTrends.remove(hashtag)
		except ValueError:
			pass
	else:
		currTrends = []
	
	
	tweetTexts = []


	for i in range(0,len(status_texts)):
		json_i = jsonResults[i]
		tags = [ hTag['text'] for hTag in json_i['entities']['hashtags'] ]
		otherTags = []
		for i in range(0,len(tags)):
			if ((json.dumps(tags[i], indent=1)[1:-1]).lower() != hashtag.lower()):
				otherTags.append((json.dumps(tags[i], indent=1)[1:-1]))

		count = 0
		for trend in currTrends:
			#print unicodedata.normalize('NFKD', trend).encode('ascii','ignore').translate(None, '#')
			if (unicodedata.normalize('NFKD', trend).encode('ascii','ignore').translate(None, '#') in otherTags):
				count += 1
		#print count


		if count < 3:
			tweetTexts.append((json.dumps(status_texts[i], indent=1))[1:-1])

	return tweetTexts


def retrieveJSON(hashtag, *hundredsOfTweets):
	global K
	if len(hundredsOfTweets) == 0:
		K = 1
	else:
		K = hundredsOfTweets[0]
	initOauth()
	global jsonResults
	jsonResults = collectSearchResults(hashtag)

	jsonFormatted = []
	for i in range(0,len(jsonResults)):
		jsonFormatted.append(str(json.dumps(jsonResults[i], indent=1)))

	return jsonFormatted


# returns all other hashtags in the tweets with the original hashtag
def retrieveOtherHashtags(origHashtag, *hundredsOfTweets):
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
def retrieveTrends():
	WORLD_WOE_ID = 1
	world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)

    #US_WOE_ID = 23424977
    #us_trends = twitter_api.trends.place(_id=US_WOE_ID)

    #print(json.dumps(world_trends, indent=1))
	#print(json.dumps(us_trends, indent=1))

	trends = []
	for trend in world_trends[0]['trends']:
		trends.append(trend['name'])

	return trends


################ Collecting search results #################
def collectSearchResults(hashtag):

    count = 100

    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets

    search_results = twitter_api.search.tweets(q=hashtag, count=count)

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
        
        search_results = twitter_api.search.tweets(**kwargs)
        jsonResults += search_results['statuses']


    # Show one sample search result by slicing the list...
    # print(str(json.dumps(jsonResults[0], indent=1)))

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

	print(json.dumps(status_texts[0:5], indent=1))
	print(json.dumps(screen_names[0:5], indent=1))
	print(json.dumps(hashtags[0:5], indent=1))
	print(json.dumps(words[0:5], indent=1))


	return status_texts


	



if __name__ == "__main__":
	hashtag = "ahsfreakshow"
	t = retrieveTweetText(hashtag)
	for tw in t:
		print(tw)
