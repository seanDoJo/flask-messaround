from flask import Flask, request, json, jsonify
from subprocess import Popen, PIPE

app = Flask(__name__)

@app.route('/create/<token>', methods=['POST'])
def create(token):
    host = request.json['host']
    store_number = 1
    if 'store_no' in request.json:
        store_number = request.json['store_no']
    address = request.json['address']
    
    creator = Popen(
        [
            'python35', 
            'create.py', 
            host, 
            store_number,
            address
        ],
        stdout=PIPE,
        stderr=PIPE
    )

    return "received", 201
