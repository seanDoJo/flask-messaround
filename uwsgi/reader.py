from flask import Flask, request, json, jsonify
import redis
from utils.utils import validateToken, getAccessToken

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)
accessToken = getAccessToken()

@app.route('/orders/get/list/<token>', methods=['POST'])
@validateToken(accessToken, r)
def list():
    hostData = r.get(
        "{}_pending".format(request.json['host'])
    )
    if not hostData:
        return jsonify({"error":"host doesn't exist"}), 400

    return hostData, 200
