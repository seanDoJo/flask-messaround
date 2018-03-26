from flask import Flask, request, json, jsonify
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/orders/get/list', methods=['POST'])
def list():
    host = "{}_pending".format(request.json['host'])
    hostData = r.get(host)
    if not hostData:
        return jsonify({"error":"host doesn't exist"}), 400

    res = {"orders": json.loads(hostData)}

    return jsonify(res), 200
