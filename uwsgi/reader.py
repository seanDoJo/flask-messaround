from flask import Flask, request, json, jsonify
import redis
from utils.utils import validateToken, getAccessToken
import os

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)
accessToken = getAccessToken()
host = os.environ['HOST']

@app.route('/orders/{}/<token>'.format(host), methods=['POST'])
@validateToken(accessToken, r)
def list():
    hostData = r.get("queue")
    if not hostData:
        return jsonify({}), 200

    return hostData, 200
