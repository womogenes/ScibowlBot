import collections


class ServerHelper:
    def __init__(self):
        self.question = collections.defaultdict(dict)
        self.answers = collections.defaultdict(str)
        self.answered = collections.defaultdict(lambda: True)
        self.last_sent_question = collections.defaultdict(int)
        self.channel_to_cat = collections.defaultdict(str)
