import collections


class ServerHelper:
    def __init__(self):
        self.question = collections.defaultdict(dict)
        self.answers = collections.defaultdict(str)
        self.answered = collections.defaultdict(lambda: True)
        self.lastSentQuestion = collections.defaultdict(int)
        self.channelToCat = collections.defaultdict(str)
