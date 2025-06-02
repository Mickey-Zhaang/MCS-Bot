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
intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


@client.event
async def on_ready():
    """
    Indicates when the bot logs online
    """
    SERVER = discord.Object(id=807388338449416283)
    await tree.sync(guild=SERVER)

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

@tree.command(
    name="hello",
    description="Replies with a simple greeting."
)
async def hello(interaction: discord.Interaction):
    """
    first slash command
    """
    await interaction.response.send_message(f"Hello, {interaction.user.mention}!")

keep_alive()
client.run(os.getenv("DISCORD_TOKEN"))
