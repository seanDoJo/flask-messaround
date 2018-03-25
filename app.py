from flask import Flask, request, jsonify, json
from utils.utils import processUpdate, processCreate, placeOrder, fulfillOrder, validateToken, getAccessToken
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
@validateToken(token, accessToken)
def create():
    if not request.json:
        return jsonify({"error":"invalid format"}), 400
    if processCreate(request.json, r, lookupTree):
        return jsonify({"success":"true"}), 201
    return jsonify({"error":"entry already exists"}), 500

# updating restaurant data
@app.route('/put/<token>', methods=['POST'])
def put(token):
    if not request.json:
        return jsonify({"error":"invalid format"}), 400
    if not validateToken(token, accessToken):
        if processUpdate(request.json, r):
            return jsonify({"success":"true"}), 201
        return jsonify({"error":"couldn't process update"}), 500
    return jsonify({"error":"invalid token"}), 500

# fetching restaurant data
@app.route('/get/<token>', methods=['POST'])
def get(token):
    if not request.json:
        return jsonify({"error":"invalid format"}), 400
    if not validateToken(token, accessToken):
        d = r.get(request.json["host"])
        if d:
            return jsonify(json.loads(d)),200
        return jsonify({"error":"entry doesn't exist"}),400
    return jsonify({"error":"invalid token"}), 500

# list restaurants
# TODO: list restaurants nearby
@app.route('/list/<token>', methods=['GET'])
def list(token):
    if not validateToken(token, accessToken):
        return jsonify({
            k.decode('utf-8'):True
            for k in r.keys('*')
        })
    return jsonify({"error":"invalid token"}), 500

# autocomplete search
# TODO: only return a fixed number
@app.route('/lookup/<token>/<prefix>', methods=['GET'])
def lookup(token, prefix):
    if not validateToken(token, accessToken):
        l = lookupTree.lookup(prefix)
        return jsonify(l)
    return jsonify({"error":"invalid token"}), 500

# placing orders
@app.route('/place/<token>', methods=['POST'])
def place(token):
    if not request.json:
        return jsonify({"error":"invalid format"}), 400
    if not validateToken(token, accessToken):
        if placeOrder(request.json, r):
            return jsonify({"success":"true"}),201
        return jsonify({"error":"invalid format"}), 400
    return jsonify({"error":"invalid token"}), 500

@app.route('/fulfill/<token>', methods=['POST'])
def fulfill(token):
    if not request.json:
        return jsonify({"error":"invalid format"}), 400
    if not validateToken(token, accessToken):
        if fulfillOrder(request.json, r):
            return jsonify({"success":"true"}),201
        return jsonify({"error":"invalid format"}), 400
    return jsonify({"error":"invalid token"}), 500
