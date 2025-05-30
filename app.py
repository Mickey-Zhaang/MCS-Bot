"""
The Main App factory
"""
import os
import discord
from dotenv import load_dotenv
from support import chatting
from keep import keep_alive

load_dotenv()

intents = discord.Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    """
    Indicates when the bot logs online
    """
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    """
    actual chatbot
    """
    if client.user in message.mentions:
        content = message.content.replace(f"<@!{client.user.id}>", "").strip()
        response = chatting(content)
        await message.channel.send(response)
    else:
        return

keep_alive()
client.run(os.getenv("DISCORD_TOKEN"))
