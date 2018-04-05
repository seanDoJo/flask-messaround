from flask import Flask, request, json, jsonify
import requests
import os

app = Flask(__name__)

adminToken = requests.get("http://172.31.36.195:8000/get_preauth/ADMIN_TOKEN").json()['success']

@app.route('/create/<token>', methods=['POST'])
def create(token):
    if token != adminToken:
        return jsonify({"error":"not authorized"}), 400

    s = {}

    host = request.json['host']
    store_id = 1
    if 'store_id' in request.json:
        store_id = request.json['store_id']
    address = request.json['address']

    s['host'] = host
    s['store_id'] = store_id
    s['address'] = address

    with open('/dev/shm/{}_{}'.format(host, store_id), 'w+') as newHost:
        newHost.write(json.dumps(s))

    return jsonify({"success":"received"}), 201
