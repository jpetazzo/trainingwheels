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


@app.errorhandler(500)
def error(e):
    return render_template('error.html',
        hostname=hostname, error=e), 500


@app.route("/")
def index():
    redis.zincrby("counters", 1, hostname)
    counters = redis.zrevrange("counters", 0, -1, withscores=True)
    counters = [ (s.decode(), int(i)) for (s,i) in counters ]
    thiscount = int(redis.zscore("counters", hostname))
    totalcount = sum(i for (s,i) in counters)
    return render_template( "index.html",
        hostname=hostname, counters=counters,
        thiscount=thiscount, totalcount=totalcount)


@app.route("/assets/<path:path>")
def assets(path):
    return send_from_directory("assets", path)


if __name__ == "__main__":
    app.run(host="0.0.0.0")

