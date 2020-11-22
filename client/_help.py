import discord

def create_help_embed(self):
    if self.helpEmbed == None:
        with open("./static/help.md") as fin:
            title = fin.readline()[1:].strip()
            description = ""
            while True:
                x = fin.readline()
                if x[0] == "`":
                    break
                description += x
                
            description = description.strip()
            description = description.replace("<prefix>", self.prefix)
            
            fields = {}
            field = x.strip()
            x = fin.readline().replace("<prefix>", self.prefix)
            while x:
                value = ""
                while x:
                    if x[0] == "`":
                        break
                    value += x                    
                    x = fin.readline().replace("<prefix>", self.prefix)
                value = value.strip()
                fields[field] = value
                field = x.strip()
                
                x = fin.readline().replace("<prefix>", self.prefix)
                
        self.helpEmbed = discord.Embed(title=title, description=description, color=0x808080)
        for f in fields:
            self.helpEmbed.add_field(name=f, value=fields[f], inline=True)
        
        
async def send_help_text(self, message):
    create_help_embed(self)
    print(self.helpEmbed)
    await message.channel.send(embed=self.helpEmbed)