from datetime import datetime
from client.server_helper import ServerHelper


async def _on_message(self, message):
    if message.guild.id not in self.servers:
        self.servers[message.guild.id] = ServerHelper()
    clipped_message = message.content if len(message.content) < 64 else message.content[:64]
    print(f"{str(message.author).ljust(32)}> {clipped_message} {datetime.now()}")
    
    if message.author == self.user:
        return

    text = message.content.lower().strip()

    # Do commands!
    if text.startswith(self.prefix):
        text = text[1:]
        if text.startswith("q"):
            await self.send_question(message)

        elif text.startswith("a"):
            await self.answer_question(message)

        elif text == "points":
            await self.query_points(message)

        elif text == "help":
            await self.send_help_text(message)
        
        elif text == "hello":
            await message.channel.send('Hello!')
            
        elif text == "ping":
            await message.channel.send("Pong! 🏓")

    else:
        await self.ping(message)

