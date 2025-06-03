"""
initializes a bot heartbeat (Flask App)
"""
import os
from threading import Thread
from flask import Flask

LOCAL = False

app = Flask("")

@app.route("/")
def home():
    """
    home route
    """
    return "I'm alive", 200

def run():
    """
    runs the heartbeat on a Port (Flask App)
    """
    if LOCAL:
        app.run(host="127.0.0.1", port=5000)
    else:
        # look for PORT from the hosting environment (Heroku)
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port)

def keep_alive():
    """
    Starts the heartbeat on a seperate thread
    """
    t = Thread(target=run)
    t.start()
