from flask import Flask, request, jsonify, json
from utils.utils import processUpdate, processCreate, validateToken, getAccessToken
from utils.tri import Tri
import redis

# server initialization
app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)
lookupTree = Tri()

accessToken = getAccessToken()

# fill out the autocomplete tree
# if data already exists
for k in r.keys('*'):
    lookupTree.insert(k.decode('utf-8'))

# creating a new restaurant
# TODO: validate the creator
# TODO: pass data in on creation?
@app.route('/data/create/<token>', methods=['POST'])
@validateToken(accessToken, r)
def create():
    if not request.json:
        return jsonify({"error":"invalid format"}), 400
    return processCreate(request.json, r, lookupTree)

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
@app.route('/data/get/<token>', methods=['POST'])
@validateToken(accessToken, r)
def get():
    if not request.json:
        return jsonify({"error":"invalid format"}), 400
    d = r.get(request.json["host"])
    if d:
        return d,200
    return jsonify({"error":"entry doesn't exist"}),400

# list restaurants
# TODO: list restaurants nearby
@app.route('/data/list/<token>', methods=['GET'])
@validateToken(accessToken, r)
def list():
    return jsonify({
        k.decode('utf-8'):True
        for k in r.keys('*')
    })

# autocomplete search
# TODO: only return a fixed number
@app.route('/data/lookup/<token>/<prefix>', methods=['GET'])
@validateToken(accessToken, r)
def lookup(prefix):
    l = lookupTree.lookup(prefix)
    return jsonify(l)
