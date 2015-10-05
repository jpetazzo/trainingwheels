#!/usr/bin/env python

from flask import Flask, send_from_directory, render_template
import os
import redis
import socket



app = Flask(__name__)
hostname = socket.gethostname()
redis = redis.Redis("redis")


if "DEBUG" in os.environ:
    app.debug = True


@app.route("/")
def index():
    redis.zincrby("counters", hostname)
    counters = redis.zrevrange("counters", 0, -1, withscores=True)
    return render_template("index.html", hostname=hostname, counters=counters)


@app.route("/assets/<path:path>")
def assets(path):
    return send_from_directory("assets", path)


if __name__ == "__main__":
    app.run(host="0.0.0.0")

