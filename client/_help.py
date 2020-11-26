import discord


def create_help_embed(self):
    if self.help_embed is None:
        with open("./static/help.md") as fin:
            title = fin.readline().lstrip("#").strip()
            description = ""
            while True:
                line = fin.readline()
                if line[0] == "`":
                    break
                description += line

            description = description.strip()
            description = description.replace("<prefix>", self.prefix)

            fields = {}
            while line:
                field = line.strip()
                line = fin.readline().replace("<prefix>", self.prefix)
                fields[field] = ""
                while line and line[0] != "`":
                    fields[field] += line
                    line = fin.readline().replace("<prefix>", self.prefix)


        self.help_embed = discord.Embed(title=title, description=description, color=0x808080)
        for field, value in fields.items():
            self.help_embed.add_field(name=field, value=value.strip(), inline=True)


async def send_help_text(self, message):
    create_help_embed(self)
    print(self.help_embed)
    await message.channel.send(embed=self.help_embed)
