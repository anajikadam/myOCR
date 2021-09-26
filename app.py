import os
import time

from flask import request
from flask import jsonify

from flask import Flask, redirect, url_for, flash, request, render_template, session, jsonify
from werkzeug.utils import secure_filename


# Define a flask app
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"+request.environ['REMOTE_ADDR']

@app.route("/myip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200

if __name__ == '__main__':
    app.secret_key = "Drmhze6EPcv0fN_81Bj-nA"
    app.config['JSON_SORT_KEYS'] = False
    app.run()
