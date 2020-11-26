from datetime import datetime as dt
from client.server_helper import ServerHelper


async def _on_message(self, message):
    if message.guild.id not in self.s:
        self.s[message.guild.id] = ServerHelper()
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
