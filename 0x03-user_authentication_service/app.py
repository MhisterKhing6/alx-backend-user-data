#!/usr/bin/env python3
""" simple flask view for the api """

from flask import Flask, jsonify
app = Flask(__name__)


@app.route('/', methods=['GET'])
def js():
    """ Return the firsts view """
    return jsonify({"message": "Bienvenue"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
