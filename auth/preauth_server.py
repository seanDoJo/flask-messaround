from flask import Flask, request, json, jsonify
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/get_preauth/<data>', methods=['GET'])
def get_preauth(data):
    d = r.get(data)
    if not d:
        return jsonify({'error':'data does not exist'}), 400

    return jsonify({'success': d}), 200
