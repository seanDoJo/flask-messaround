from flask import Flask, request, jsonify, json
from utils.utils import processUpdate, processCreate, validateToken, getAccessToken
import redis
import os

# server initialization
app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

accessToken = getAccessToken()

hostName = os.environ['HOST']

exists = r.get(hostName)

if not exists:
    r.set(hostName, json.dumps({'categories': {}}))

# updating restaurant data
@app.route('/data/put/<token>', methods=['POST'])
@validateToken(accessToken, r)
def put():
    if not request.json:
        return jsonify({"error":"invalid format"}), 400
    if processUpdate(request.json, r):
        return jsonify({"success":"true"}), 201
    return jsonify({"error":"couldn't process update"}), 500

# fetching restaurant data
@app.route('/data/get/<token>', methods=['GET'])
@validateToken(accessToken, r)
def get():
    d = r.get(hostName)
    return d,200
