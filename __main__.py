import os
from pathlib import Path

from client import MyClient

token_file = Path("data", "token.txt")
if token_file.exists():
    with open(token_file) as fin:
        token = fin.read()
else:
    token = os.environ.get("TOKEN")

client = MyClient()
client.run("TOKEN")
