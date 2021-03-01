import discord

async def on_raw_reaction_add(self, payload):
    # Here's the info
    print(f"""channel: {payload.channel_id}
emoji: {payload.emoji}
message_id: {payload.message_id}
user: {payload.user_id}
guild_id: {payload.guild_id}""")

    # Now let's find the message
    server = None

    for s in self.guilds: # Thisi is gonna get costly later, better figure it out
        if s.id == payload.guild_id:
            server = s
            break

    if not server:
        return # :(

    # Now we find the channel and then the message
    # https://stackoverflow.com/questions/51101717/how-to-set-channel-object-using-the-channel-id-in-discord-py
    # https://stackoverflow.com/questions/61851174/how-to-get-message-by-id-discord-py

    # Now update the message with this
    # https://stackoverflow.com/questions/55711572/how-to-edit-a-message-in-discord-py