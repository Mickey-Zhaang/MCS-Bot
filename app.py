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
def on_message_slack(body, say):
    """
    [Slack]
    
    When the bot is mentioned, strip off the mention tag and pass
    the clean text to `chatting(...)`, then reply with its response.
    """

    event = body["event"]
    full_text = event["text"]
    bot_id = body["authorizations"][0]["user_id"]

    if bot_id in full_text:

        # gets rid of the @ mention so chatting only sees user question
        user_message = full_text.replace(f"<@!{discord_bot.user.id}>", "").strip()

        # takes the cleaned user input "user_message" and runs it through a LLM
        response = chatting(user_message)

        # the bot returns the response from the LLM
        say(response)

def start_slack_socket_mode():
    """
    [Slack] this must run in the main thread (so signal handlers can be registered).
    """
    # Check documentation for Slack's Socket Mode -- https://api.slack.com/apis/socket-mode
    handler = SocketModeHandler(slack_bot, os.environ["SLACK_APP_TOKEN"])
    handler.start()

# 2) DISCORD
intents = discord.Intents.default()
discord_bot = discord.Client(intents=intents)

@discord_bot.event
async def on_ready():
    """
    [Discord]  
    
    For debugging purposes  
    Is called once after the bot sucessfully logs in
    """
    pass

@discord_bot.event
async def on_message_discord(message):
    """
    [Discord]  
    
    When the bot is mentioned,
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
    # sets up a new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(discord_bot.start(os.getenv("DISCORD_TOKEN")))

if __name__ == "__main__":
    discord_thread = threading.Thread(target=start_discord_bot, daemon=True)
    discord_thread.start()

    keep_alive()

    start_slack_socket_mode()
