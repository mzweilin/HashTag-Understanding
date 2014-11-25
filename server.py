from flask import Flask
import json
from job import Job

app = Flask(__name__)

# Note: By default, routed functions only answer to GET requests
@app.route("/query/<query>")
def search(query):
    job = Job(query)
    return json.dumps(job.execute())

if __name__ == "__main__":
    app.run(debug=True)
