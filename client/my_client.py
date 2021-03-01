# TODO: Replace channel IDs.

import collections
import json
import os
import random
import time

import discord

from client.server_helper import ServerHelper

if ".env" in os.listdir():
    from dotenv import find_dotenv, load_dotenv
    load_dotenv(find_dotenv())

class MyClient(discord.Client):

    from ._help import send_help_text
    from ._on_message import _on_message
    from ._override import on_raw_reaction_add

    def __init__(self, *args):
        discord.Client.__init__(self, *args)

        self.correct_points = 2
        self.incorrect_points = -1

        self.prefix = "-"
        self.question_list = collections.defaultdict(list)

        self.help_embed = None

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
                self.question_list[c] = json.load(fin)

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
            await message.channel.send(f"**{message.author.display_name}**, you have **{self.points[idx]}** points.")

    async def on_ready(self):
        """
        This function is called when the client is ready.
        """
        print("Logged on as " + str(self.user) + "!")
        self.on_message = self._on_message
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{self.prefix}help"))

        self.servers = {
            guild.id: ServerHelper()
            for guild in self.guilds
        }

    async def send_question(self, message):
        x = message.content.strip().split(" ")
        if len(x) != 2:
            await message.channel.send("Please use the format `-q <category>`.")
            return

        cat = x[1]
        idx = message.guild.id
        if cat not in self.categories:
            category_text = "\n".join(self.categories)
            text = f"Category should be one of the following:\n```{category_text}```"
            await message.channel.send(text)
            return
        
        try:
            if self.servers[idx].answered[cat]:
                self.servers[idx].question[cat] = f"**{cat.capitalize()} question:**\n"

                q = random.choice(self.question_list[cat])
                self.servers[idx].question[cat] += q["tossup_question"]

                if q["tossup_format"] == "Short Answer":
                    self.servers[idx].answers[cat] = [q["tossup_answer"]]
                else:
                    self.servers[idx].answers[cat] = [q["tossup_answer"][0], q["tossup_answer"][3:]]

                await message.channel.send(self.servers[idx].question[cat])
                self.servers[idx].last_sent_question[cat] = time.time()
                self.servers[idx].channel_to_cat[message.channel.id] = cat
                self.servers[idx].answered[cat] = False

                
            elif not self.servers[idx].answered[cat]:
                if time.time() - self.servers[idx].last_sent_question[cat] > 10:
                    await message.channel.send(self.servers[idx].question[cat])

        except:
            pass

    async def answer_question(self, message):
        x = message.content.strip().split(" ")
        if len(x) < 2:
            await message.channel.send("Please use the format `-a <answer>`.")
            return

        idx = message.guild.id
        cat = self.servers[idx].channel_to_cat[message.channel.id]
        if cat not in self.categories:
            await message.channel.send("Please use `-q <category>` to get a question.")
            return

        if cat is None:
            return

        if self.servers[idx].answered[cat]:
            return

        if len(message.content) < 4:
            return

        answer = message.content[3:]
        correct = answer.lower() in [i.lower() for i in self.servers[idx].answers[cat]]

        self.servers[idx].answered[cat] = True

        if correct:
            await message.add_reaction("✅")
            self.give_points(message.author.id, self.correct_points)
            await message.channel.send(f"""That was correct, **{message.author.display_name}**! You now have **{self.points[message.author.id]}** points. (+{self.correct_points})""")

        else:
            if len(self.servers[idx].answers[cat]) == 2:
                right_answer = f"{self.servers[idx].answers[cat][0]}) {self.servers[idx].answers[cat][1]}"
            else:
                right_answer = self.servers[idx].answers[cat][0]
            await message.add_reaction("☹️")
            self.give_points(message.author.id, self.incorrect_points)
            await message.channel.send(f"""Incorrect, **{message.author.display_name}**. The right answer was **{right_answer}**. You now have **{self.points[message.author.id]}** points. ({self.incorrect_points}).""")
            await message.add_reaction("❓")


                            

            
            
        self.servers[idx].channel_to_cat[cat] = ""

    async def ping(self, message):
        if message.content.strip() == "<@!765264293818007584>":
            await message.channel.send("Active and ready to serve up some questions!")

            

