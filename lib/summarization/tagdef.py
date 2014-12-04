import httplib
import json

def lookup(hashtag):
    try:
        connection = httplib.HTTPConnection("api.tagdef.com")
        connection.request("GET","/one." + hashtag + ".json")
        response = connection.getresponse()
        return json.loads(response.read())["defs"]["def"]["text"]
    except:
        return ""

if __name__ == "__main__":
    print(lookup("wcw"))
