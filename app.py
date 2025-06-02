"""
The Main App factory (Slack in main thread; Discord in its own thread)
"""
import os
import asyncio
import threading
import discord
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from support import chatting
from keep import keep_alive

load_dotenv()

# 1) SLACK
slack_bot = App(token=os.environ["SLACK_BOT_TOKEN"])

@slack_bot.event("app_mention")
def handle_app_mention_events(body, say):
    """
    [Slack] respond to @mention, forward to `chatting(...)`
    """
    event = body["event"]
    full_text = event["text"]
    bot_id = body["authorizations"][0]["user_id"]
    if full_text.startswith(f"<@{bot_id}>"):
        user_message = full_text.split(">", 1)[1].strip()
    else:
        user_message = full_text

    response = chatting(user_message)
    say(response)

def start_slack_socket_mode():
    """
    [Slack] this must run in the main thread (so signal handlers can be registered).
    """
    handler = SocketModeHandler(slack_bot, os.environ["SLACK_APP_TOKEN"])
    handler.start()

# 2) DISCORD
intents = discord.Intents.default()
discord_bot = discord.Client(intents=intents)

@discord_bot.event
async def on_ready():
    """
    [Discord] on_ready
    """
    print(f"[Discord] Logged in as {discord_bot.user}")

@discord_bot.event
async def on_message(message):
    """
    [Discord] if bot is mentioned, forward to `chatting(...)`
    """
    if discord_bot.user in message.mentions:
        content = message.content.replace(f"<@!{discord_bot.user.id}>", "").strip()
        response = chatting(content)
        await message.channel.send(response)

def start_discord_bot():
    """
    [Discord] create a fresh asyncio loop inside this thread,
    then run `discord_bot.start()` on it.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(discord_bot.start(os.getenv("DISCORD_TOKEN")))

if __name__ == "__main__":
    discord_thread = threading.Thread(target=start_discord_bot, daemon=True)
    discord_thread.start()

    keep_alive()

    start_slack_socket_mode()
