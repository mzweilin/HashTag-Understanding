from flask import Flask
import json
from job import Job
from collections import OrderedDict

app = Flask(__name__)

class Cache:
    max_entries = 100
    
    def __init__(self):
        self.entry_count = 0
        self.table = OrderedDict()

    def add(self, query, result):
        if (self.entry_count > Cache.max_entries):
            self.table.popitem(last=false) #false for fifo
            self.entry_count -= 1
        self.table[query] = result
        self.entry_count += 1

    def get(self, query):
        try:
            result = self.table[query]
        except KeyError:
            result = False
        return result
cache = Cache()

# Note: By default, routed functions only answer to GET requests
@app.route("/query/<query>")
def search(query):
    job = Job(query) #use name prep from job init
    result = cache.get(job.hashtag)
    if not result:
        result = json.dumps(job.execute()) 
        cache.add(job.hashtag, result)
    return result


if __name__ == "__main__":
    app.run(debug=True)
