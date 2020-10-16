# TODO: Replace channel IDs.

import discord
from discord.ext import commands
from discord.utils import get

import random
import sys
import os
import time
import json
from datetime import datetime as dt

from html import unescape

import discord

ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
shorten = lambda x: x if len(x) < 16 else x[:13] + "..."
signify = lambda x: "+" + str(x) if x > 0 else x

class MyClient(discord.Client):
    
    def initialize(self):        
        self.question = None
        self.answers = None
        self.answered = True
        self.lastSentQuestion = 0
        
        self.bioChannel = self.get_channel(766681561977847809)
        with open("./questions/biology.json") as fin:
            self.bioQuestions = json.load(fin)
        
        
    async def on_ready(self):
        """
        This function is called when the client is ready.
        """
        print("Logged on as " + str(self.user) + "!")
        self.initialize()
        
    
    async def on_message(self, message):
        clippedMessage = message.content if len(message.content) < 64 else message.content[:64]
        print(str(message.author).ljust(32) + "> " + clippedMessage + " " + str(dt.now()))
        
        channel = message.channel
        text = message.content
        
        if message.author == self.user:
            return
            
        # Do commands!
        if text.lower().strip() == "-q":
            await self.send_bioq()
            return
            
        if channel.id == 766681561977847809 and text.lower().startswith("-a"):
            await self.answer_bioq(message)
            return
            
        await self.ping(message)
        
    
    async def send_bioq(self):
        if self.question == None or self.answered:                
            self.question = f"**Biology question:**\n"
            
            q = random.choice(self.bioQuestions)
            self.question += q["tossup_question"]
                
            if q["tossup_format"] == "Short Answer":
                self.answers = [q["tossup_answer"]]
            else:
                self.answers = [q["tossup_answer"][0], q["tossup_answer"][3:]]
            
            self.answered = False
            
            await self.bioChannel.send(self.question)
            self.lastSentQuestion = time.time()
            
            
        elif not self.answered and time.time() - self.lastSentQuestion > 10:
            await self.bioChannel.send(self.question)
            
        
    async def answer_bioq(self, message):    
        if self.answered:
            return
            
        if len(message.content) < 4:
            return
        
        answer = message.content[3:]
        correct = answer.lower() in [i.lower() for i in self.answers]
            
        self.answered = True
        
        if correct:
            await self.bioChannel.send(f"""That was correct, **{message.author.display_name}**! 🙂""")
            
        else:
            if len(self.answers) == 2:
                rightAnswer = f"{self.answers[0]}) {self.answers[1]}"
            else:
                rightAnswer = self.answers[0]
            await self.bioChannel.send(f"""Sorry, {message.author.display_name} ☹ The right answer was **{rightAnswer}**.""")
        
        
    async def ping(self, message):
        if "<@!765264293818007584>" in message.content:
            await message.channel.send("Active and ready to serve up some questions!")



client = MyClient()
client.run('NzY1MjY0MjkzODE4MDA3NTg0.X4SR6Q.hzbbRcSXWY4xINOsKPUb5KbCAgk')