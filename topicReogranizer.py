import json
import shutil
import os
import concurrent.futures

total = 7694

def recategorize(n):
    try:
        with open(f"./questions/question_{str(n).zfill(4)}.json") as fin:
            x = json.load(fin)
            category = x["question"]["category"].lower()
        
        if category not in os.listdir("./questions"):
            os.mkdir(f"./questions/{category}")
        shutil.move(f"./questions/question_{str(n).zfill(4)}.json", f"./questions/{category}/question_{str(n).zfill(4)}.json")
    
    except:
        pass
    
ns = list(range(1258, total + 1))

for i in ns:
    recategorize(i)