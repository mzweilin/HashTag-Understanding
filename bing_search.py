import json
import subprocess as proc
import os.path
import sys
 
def main():
    print(search(sys.argv[1], sys.argv[2]))

def search(query, num_results):
    urls = []
    file_path = "queries/" + query 
    cmd = ["ruby bing_search.rb " + ('%s ' % query) + num_results]
    if not os.path.exists(file_path):
        with open(file_path, mode="w") as f:
            proc.call(cmd, shell=True, stdout=f)
    with open(file_path, mode='r') as f:
        data = json.loads(f.read())
        for site in data[0]['Web']:
            urls.append(site['Url'])
    return urls
 
if __name__ == "__main__":
    main()
