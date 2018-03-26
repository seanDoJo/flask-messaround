from flask import Flask, request, json, jsonify
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/orders/update/create', methods=['POST'])
def create():
    host = "{}_pending".format(request.json['host'])
    if r.get(host):
        return jsonify({'error': 'host already exists'}), 400

    host = "{}_pending".format(request.json['host'])

    r.set(host, json.dumps([]))
    return jsonify({'success': 'true'}), 200

@app.route('/orders/update/add', methods=['POST'])
def add():
    host = "{}_pending".format(request.json['host'])
    hostData = r.get(host)
    if not hostData:
        return jsonify({"error":"host doesn't exist"}), 400

    hostData = json.loads(hostData)

    hostData.append(request.json['order'])

    r.set(host, json.dumps(hostData))

    return jsonify({'success':True}), 200
