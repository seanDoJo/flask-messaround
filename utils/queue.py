from flask import Flask, request, json
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/create', methods=['POST'])
def create():
    host = r.get(request.json['host'])
    if host:
        return jsonify({'error': 'host already exists'}), 400

    r.set(request.json['host'], json.dumps([]))
    return jsonify({'success': 'true'}), 200

@app.route('/add', methods=['POST'])
def add():
    hostData = r.get(request.json['host'])
    if not hostData:
        return jsonify({"error":"host doesn't exist"}), 400

    hostData = json.loads(hostData)

    hostData.append(request.json['order'])

    r.set(request.json['host'], json.dumps(hostData))

    return jsonify({'success':True}), 200

@app.route('/list/<host>', methods=['GET'])
def list(host):
    hostData = r.get(host)
    if not hostData:
        return jsonify({"error":"host doesn't exist"}), 400

    res = {"orders": json.loads(hostData)}

    return jsonify(res), 200
