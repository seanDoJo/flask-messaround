from flask import Flask, request, jsonify
from utils.utils import processUpdate
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
def hello_world():
    return 'Hello, World'

@app.route('/put', methods=['POST'])
def put():
    processUpdate(request.form, r)
    for k in request.form:
        print(k)
    r.set(key, value)

@app.route('/get/<key>', methods=['GET'])
def get(key):
    return r.get(key)
