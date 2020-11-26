from client import MyClient
import os

if "token.txt" in os.listdir("./data"):
    with open("./data/token.txt") as fin:
        token = fin.read()
else:
    token = os.environ.get("TOKEN")

client = MyClient()
client.run(token)
