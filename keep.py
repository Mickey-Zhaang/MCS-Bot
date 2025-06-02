"""
keep.py
"""
import os
from threading import Thread
from flask import Flask

LOCAL = True

app = Flask("")

@app.route("/")
def home():
    """
    home route
    """
    return "I'm alive", 200

def run():
    """
    run
    """
    if LOCAL:
        app.run(host="127.0.0.1", port=5000)
    else:
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port)

def keep_alive():
    """
    Keeps our bot alive
    """
    t = Thread(target=run)
    t.start()
