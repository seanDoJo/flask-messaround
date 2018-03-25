from flask import Flask, request, jsonify, json
from utils.utils import processUpdate, processCreate, placeOrder, fulfillOrder, validateToken, getAccessToken, getOrders
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
@app.route('/create/<token>', methods=['POST'])
@validateToken(accessToken)
def create():
    if not request.json:
        return jsonify({"error":"invalid format"}), 400
    return processCreate(request.json, r, lookupTree)

# updating restaurant data
@app.route('/put/<token>', methods=['POST'])
@validateToken(accessToken)
def put():
    if not request.json:
        return jsonify({"error":"invalid format"}), 400
    if processUpdate(request.json, r):
        return jsonify({"success":"true"}), 201
    return jsonify({"error":"couldn't process update"}), 500

# fetching restaurant data
@app.route('/get/<token>', methods=['POST'])
@validateToken(accessToken)
def get():
    if not request.json:
        return jsonify({"error":"invalid format"}), 400
    d = r.get(request.json["host"])
    if d:
        return jsonify(json.loads(d)),200
    return jsonify({"error":"entry doesn't exist"}),400

# list restaurants
# TODO: list restaurants nearby
@app.route('/list/<token>', methods=['GET'])
@validateToken(accessToken)
def list():
    return jsonify({
        k.decode('utf-8'):True
        for k in r.keys('*')
    })

# autocomplete search
# TODO: only return a fixed number
@app.route('/lookup/<token>/<prefix>', methods=['GET'])
@validateToken(accessToken)
def lookup(prefix):
    l = lookupTree.lookup(prefix)
    return jsonify(l)

# placing orders
@app.route('/place/<token>', methods=['POST'])
@validateToken(accessToken)
def place():
    if not request.json:
        return jsonify({"error":"invalid format"}), 400
    return placeOrder(request.json, r)

@app.route('/listorders/<token>', methods=['POST'])
@validateToken(accessToken)
def listorders():
    if not request.json:
        return jsonify({"error":"invalid format"}), 400
    return getOrders(request.json, r)

@app.route('/fulfill/<token>', methods=['POST'])
@validateToken(accessToken)
def fulfill():
    if not request.json:
        return jsonify({"error":"invalid format"}), 400
    if fulfillOrder(request.json, r):
        return jsonify({"success":"true"}),201
    return jsonify({"error":"invalid format"}), 400
