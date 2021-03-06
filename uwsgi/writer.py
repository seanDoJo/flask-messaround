from flask import Flask, request, json, jsonify
from utils.utils import validateToken, getAccessToken
import redis
import os

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)
accessToken = getAccessToken()

host = os.environ['HOST']

@app.route('/update/{}/<token>'.format(host), methods=['POST'])
@validateToken(accessToken, r)
def state():
    host = "{}_pending".format(request.json['host'])
    hostData = r.get(host)
    if not hostData:
        return jsonify({"error":"host doesn't exist"}), 400

    hostData = json.loads(hostData)

    order_no = request.json['order_no']

    for i,order in enumerate(hostData['pending']):
        if order['order_no'] == order_no:
            hostData['pending'][i]['state'] = request.json['state']
            break
    r.set(host, json.dumps(hostData))
    return jsonify({'success':True}), 201

@app.route('/orders/update/create', methods=['POST'])
def create():
    host = "{}_pending".format(request.json['host'])
    if r.get(host):
        return jsonify({'error': 'host already exists'}), 400

    r.set(host, json.dumps({'pending':[],'lon':0}))
    return jsonify({'success': 'true'}), 200

@app.route('/orders/update/add/<token>', methods=['POST'])
@validateToken(accessToken, r)
def add():
    host = "{}_pending".format(request.json['host'])
    hostData = r.get(host)
    if not hostData:
        return jsonify({"error":"host doesn't exist"}), 400

    order = request.json['order']
    hostData = json.loads(hostData)


    order['state'] = 0
    hostData['lon'] += 1
    order['order_no'] = hostData['lon']
    hostData['pending'].append(order)

    r.set(host, json.dumps(hostData))

    return jsonify({'order':hostData['lon']}), 200
