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
if ".env" in os.listdir():
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())

import discord

ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
shorten = lambda x: x if len(x) < 16 else x[:13] + "..."
signify = lambda x: "+" + str(x) if x > 0 else x

class MyClient(discord.Client):

    from ._help import send_help_text
    
    async def initialize(self):
        self.cpoints = 2
        self.wpoints = -1
        
        self.question = collections.defaultdict(dict)
        self.qList = collections.defaultdict(list)
        self.answers = collections.defaultdict(str)
        self.answered = collections.defaultdict(lambda: True)
        self.lastSentQuestion = collections.defaultdict(int)
        self.channelToCat = collections.defaultdict(str)
        self.prefix = "-"
        
        self.helpEmbed = None

        self.categories = {
            'astronomy': 'astronomy',
            'biology': 'biology',
            'chemistry': 'chemistry',
            'cs': 'computer science',
            'eas': 'earth and space',
            'es': 'earth science',
            'energy': 'energy',
            'general': 'general science',
            'math': 'math',
            'physics': 'physics'
        }
        
        for c in self.categories:
            with open(f"./questions/{self.categories[c]}.json") as fin:
                self.qList[c] = json.load(fin)
                
        with open("./data/point-info.json") as fin:
            self.points = json.load(fin)
        
    
    def give_points(self, idx, points):
        if idx not in self.points:
            self.points[idx] = 0
        self.points[idx] += points
        with open("./data/point-info.json", "w") as fout:
            json.dump(self.points, fout)
        
        
    async def query_points(self, message):
        idx = message.author.id
        if idx not in self.points:
            await message.channel.send(f"**{message.author.display_name}**, you don't have any points.")
        else:
            await message.channel.send(f"**{message.author.display_name}, you have **{self.points[idx]}** points.")
        
        
    async def on_ready(self):
        """
        This function is called when the client is ready.
        """
        print("Logged on as " + str(self.user) + "!")
        await self.initialize()
        self.on_message = self._on_message
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{self.prefix}help"))
        
    
    async def _on_message(self, message):
        clippedMessage = message.content if len(message.content) < 64 else message.content[:64]
        print(str(message.author).ljust(32) + "> " + clippedMessage + " " + str(dt.now()))
        
        text = message.content
        
        if message.author == self.user:
            return
            
        # Do commands!
        if text.lower().strip().startswith(f"{self.prefix}q"):
            await self.send_question(message)
            return
            
        if text.lower().strip().startswith(f"{self.prefix}a"):
            await self.answer_question(message)
            return
            
        if text.lower().strip() == f"{self.prefix}points":
            await self.query_points(message)
            return

        if text.lower().strip() == f"{self.prefix}help":
            await self.send_help_text(message)
            return
            
        await self.ping(message)
    
    
    async def send_question(self, message):
        x = message.content.strip().split(" ")
        if len(x) != 2:
            message.channel.send("Please use the format `-q <category>`.")

        cat = x[1]
        if cat not in self.categories:
            text = "Category should be one of the following:\n```\n"
            for i in self.categories:
                text += i + "\n"
            text = text[:-1] + "```"
            message.channel.send(text)
        
        if self.answered[cat]:
            self.question[cat] = f"**{cat.capitalize()} question:**\n"
            
            q = random.choice(self.qList[cat])
            self.question[cat] += q["tossup_question"]
                
            if q["tossup_format"] == "Short Answer":
                self.answers[cat] = [q["tossup_answer"]]
            else:
                self.answers[cat] = [q["tossup_answer"][0], q["tossup_answer"][3:]]
            
            self.answered[cat] = False
            
            await message.channel.send(self.question[cat])
            self.lastSentQuestion[cat] = time.time()
            self.channelToCat[message.channel.id] = cat
            
        elif not self.answered[cat] and time.time() - self.lastSentQuestion[cat] > 10:
            await message.channel.send(self.question[cat])
            
        
    async def answer_question(self, message):
        x = message.content.strip().split(" ")
        if len(x) != 2:
            message.channel.send("Please use the format `-a <answer>`.")

        cat = self.channelToCat[message.channel.id]
        if cat not in self.categories:
            message.channel.send("Question does not exist. Please use `-q <category>` to get a question.")

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
            self.give_points(message.author.id, self.cpoints)
            await message.channel.send(f"""That was correct, **{message.author.display_name}**! You now have **{self.points[message.author.id]}** points. (+{self.cpoints})""")
            
        else:
            if len(self.answers[cat]) == 2:
                rightAnswer = f"{self.answers[cat][0]}) {self.answers[cat][1]}"
            else:
                rightAnswer = self.answers[cat][0]
            await message.add_reaction("☹️")
            self.give_points(message.author.id, self.wpoints)
            await message.channel.send(f"""Incorrect, **{message.author.display_name}**. The right answer was **{rightAnswer}**. You now have **{self.points[message.author.id]}** points. ({self.wpoints})""")


        self.channelToCat[cat] = ""
        
        
    async def ping(self, message):
        if message.content.strip() == "<@!765264293818007584>":
            await message.channel.send("Active and ready to serve up some questions!")