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
import collections

from html import unescape

import discord

ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
shorten = lambda x: x if len(x) < 16 else x[:13] + "..."
signify = lambda x: "+" + str(x) if x > 0 else x

class MyClient(discord.Client):
    
    async def initialize(self):
        self.question = collections.defaultdict(dict)
        self.qList = collections.defaultdict(list)
        self.answers = collections.defaultdict(str)
        self.answered = collections.defaultdict(lambda: True)
        self.lastSentQuestion = collections.defaultdict(int)
        
        self.channels = {
            "biology": await self.fetch_channel(766681561977847809),
            "physics": await self.fetch_channel(767943535085092864),
            "chemistry": await self.fetch_channel(767943402082926602),
            "earth science": await self.fetch_channel(767943627397005343)
        }
        for c in self.channels:
            with open(f"./questions/{c}.json") as fin:
                self.qList[c] = json.load(fin)
        
        
    async def on_ready(self):
        """
        This function is called when the client is ready.
        """
        print("Logged on as " + str(self.user) + "!")
        await self.initialize()
        
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="@Bill9000, my creator"))
        
    
    async def on_message(self, message):
        clippedMessage = message.content if len(message.content) < 64 else message.content[:64]
        print(str(message.author).ljust(32) + "> " + clippedMessage + " " + str(dt.now()))
        
        channel = message.channel
        text = message.content
        
        if message.author == self.user:
            return
            
        # Do commands!
        if text.lower().strip() == "-q":
            await self.send_question(message)
            return
            
        if text.lower().startswith("-a"):
            await self.answer_question(message)
            return
            
        await self.ping(message)
        
    
    def cat_from_idx(self, idx):
        for c in self.channels:
            if self.channels[c].id == idx:
                return c
    
    
    async def send_question(self, message):
        cat = self.cat_from_idx(message.channel.id)
        if cat == None:
            return
        
        if self.answered[cat]:
            self.question[cat] = f"**{cat.capitalize()} question:**\n"
            
            q = random.choice(self.qList[cat])
            self.question[cat] += q["tossup_question"]
                
            if q["tossup_format"] == "Short Answer":
                self.answers[cat] = [q["tossup_answer"]]
            else:
                self.answers[cat] = [q["tossup_answer"][0], q["tossup_answer"][3:]]
            
            self.answered[cat] = False
            
            await self.channels[cat].send(self.question[cat])
            self.lastSentQuestion[cat] = time.time()
            
            
        elif not self.answered[cat] and time.time() - self.lastSentQuestion[cat] > 10:
            await self.channels[cat].send(self.question[cat])
            
        
    async def answer_question(self, message):
        cat = self.cat_from_idx(message.channel.id)
        if cat == None:
            return
            
        if self.answered[cat]:
            return
            
        if len(message.content) < 4:
            return
        
        answer = message.content[3:]
        correct = answer.lower() in [i.lower() for i in self.answers[cat]]
            
        self.answered[cat] = True
        
        if correct:
            await message.add_reaction("🧠")
            await self.channels[cat].send(f"""That was correct, **{message.author.display_name}**! 🙂""")
            
        else:
            if len(self.answers[cat]) == 2:
                rightAnswer = f"{self.answers[cat][0]}) {self.answers[cat][1]}"
            else:
                rightAnswer = self.answers[cat][0]
            await message.add_reaction("☹️")
            await self.channels[cat].send(f"""Incorrect, {message.author.display_name} ☹ The right answer was **{rightAnswer}**.""")
        
        
    async def ping(self, message):
        if "<@!765264293818007584>" in message.content:
            await message.channel.send("Active and ready to serve up some questions!")



client = MyClient()
client.run('NzY1MjY0MjkzODE4MDA3NTg0.X4SR6Q.hzbbRcSXWY4xINOsKPUb5KbCAgk')