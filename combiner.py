import os
import json

def reorganize(topic):
    questions = []
    k = os.listdir(f"./questions/{topic}")
    for i in k:
        with open(f"./questions/{topic}/{i}") as fin:
            q = json.load(fin)["question"]
            questions.append(q)
            
    with open(f"./questions/{topic}.json", "w") as fout:
        json.dump(questions, fout)
        
    
k = os.listdir("./questions")
for i in k:
    reorganize(i)