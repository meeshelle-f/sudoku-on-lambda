"""Sudoku web app for the Docker course, Lesson 04.

In the lesson you write its Dockerfile, run it in a container on your computer, push the image to Amazon ECR and run
it on Amazon ECS with AWS Fargate behind a load balancer. Inside the container, gunicorn serves it on port 80.
"""
import os
import socket

from flask import Flask, jsonify, render_template, request

from sudoku import MODES, new_puzzle

app = Flask(__name__)
VERSION = os.getenv("APP_VERSION", "dev")    # set with ENV in the Dockerfile
CONTAINER = socket.gethostname()             # which copy of the app answered: watch it change behind a load balancer


@app.get("/")
def home():
    return render_template("index.html", version=VERSION, container=CONTAINER, modes=MODES)


@app.get("/api/new")
def api_new():
    mode = request.args.get("mode", "beginner")
    if mode not in MODES:
        return jsonify(error=f"unknown mode {mode!r}: use beginner, medium or hard"), 400
    return jsonify(mode=mode, puzzle=new_puzzle(mode), served_by=CONTAINER, version=VERSION)


@app.get("/health")
def health():
    return "ok\n"


if __name__ == "__main__":    # only for a quick test without Docker: python app.py, then open http://127.0.0.1:5000
    app.run(host="127.0.0.1", port=5000, debug=True)
