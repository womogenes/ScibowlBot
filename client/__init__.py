# TODO: Replace channel IDs.

import discord
from discord.ext import commands
from discord.utils import get

import random
import sys
sys.path.append("./client")
import os
import time
import json
from datetime import datetime as dt
import collections
from ServerHelper import *

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
    from ._on_message import _on_message

    def __init__(self, *args):
        discord.Client.__init__(self, *args)

        self.cpoints = 2
        self.wpoints = -1

        self.prefix = "-"
        self.qList = collections.defaultdict(list)
        
        self.helpEmbed = None

        self.categories = {
            'astro': 'astronomy',
            'bio': 'biology',
            'chem': 'chemistry',
            'cs': 'computer science',
            'eas': 'earth and space',
            'es': 'earth science',
            'energy': 'energy',
            'gen': 'general science',
            'math': 'math',
            'phy': 'physics'
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
        self.on_message = self._on_message
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{self.prefix}help"))

        self.s = {}
        for g in self.guilds:
            idx = g.id
            self.s[idx] = ServerHelper()
    
    
    async def send_question(self, message):
        x = message.content.strip().split(" ")
        if len(x) != 2:
            await message.channel.send("Please use the format `-q <category>`.")
            return

        cat = x[1]
        idx = message.guild.id
        if cat not in self.categories:
            text = "Category should be one of the following:\n```\n"
            for i in self.categories:
                text += i + "\n"
            text = text[:-1] + "```"
            await message.channel.send(text)
            return
        
        if self.s[idx].answered[cat]:
            self.s[idx].question[cat] = f"**{cat.capitalize()} question:**\n"
            
            q = random.choice(self.qList[cat])
            self.s[idx].question[cat] += q["tossup_question"]
                
            if q["tossup_format"] == "Short Answer":
                self.s[idx].answers[cat] = [q["tossup_answer"]]
            else:
                self.s[idx].answers[cat] = [q["tossup_answer"][0], q["tossup_answer"][3:]]
            
            self.s[idx].answered[cat] = False
            
            await message.channel.send(self.s[idx].question[cat])
            self.s[idx].lastSentQuestion[cat] = time.time()
            self.s[idx].channelToCat[message.channel.id] = cat
            
        elif not self.s[idx].answered[cat]:
            if time.time() - self.s[idx].lastSentQuestion[cat] > 10:
                await message.channel.send(self.s[idx].question[cat])
            
        
    async def answer_question(self, message):
        x = message.content.strip().split(" ")
        if len(x) != 2:
            await message.channel.send("Please use the format `-a <answer>`.")
            return

        idx = message.guild.id
        cat = self.s[idx].channelToCat[message.channel.id]
        if cat not in self.categories:
            await message.channel.send("Please use `-q <category>` to get a question.")
            return

        if cat == None:
            return
            
        if self.s[idx].answered[cat]:
            return
            
        if len(message.content) < 4:
            return
        
        answer = message.content[3:]
        correct = answer.lower() in [i.lower() for i in self.s[idx].answers[cat]]
            
        self.s[idx].answered[cat] = True
        
        if correct:
            await message.add_reaction("🧠")
            self.give_points(message.author.id, self.cpoints)
            await message.channel.send(f"""That was correct, **{message.author.display_name}**! You now have **{self.points[message.author.id]}** points. (+{self.cpoints})""")
            
        else:
            if len(self.s[idx].answers[cat]) == 2:
                rightAnswer = f"{self.s[idx].answers[cat][0]}) {self.s[idx].answers[cat][1]}"
            else:
                rightAnswer = self.s[idx].answers[cat][0]
            await message.add_reaction("☹️")
            self.give_points(message.author.id, self.wpoints)
            await message.channel.send(f"""Incorrect, **{message.author.display_name}**. The right answer was **{rightAnswer}**. You now have **{self.points[message.author.id]}** points. ({self.wpoints})""")


        self.s[idx].channelToCat[cat] = ""
        
        
    async def ping(self, message):
        if message.content.strip() == "<@!765264293818007584>":
            await message.channel.send("Active and ready to serve up some questions!")