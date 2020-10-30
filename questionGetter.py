import requests
import json
import concurrent.futures

# 7694 questions total.
total = 7694

url = "https://scibowldb.com/api/questions/"

def cache(n):
    x = json.loads(requests.get(url + str(n)).content)  
    with open(f"./questions/question_{str(n).zfill(4)}.json", "w") as fout:
        json.dump(x, fout, indent=2)

ns = list(range(1, total + 1))

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results = pool.map(cache, ns)