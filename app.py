from flask import Flask, request, jsonify
from utils.utils import processUpdate, processCreate, placeOrder, fulfillOrder
from utils.tri import Tri
import redis

# server initialization
app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)
lookupTree = Tri()

# fill out the autocomplete tree
# if data already exists
for k in r.keys('*'):
    lookupTree.insert(k.decode('utf-8'))

# creating a new restaurant
# TODO: validate the creator
# TODO: pass data in on creation?
@app.route('/create', methods=['POST'])
def create():
    if not request.json:
        return jsonify({"error":"invalid format"}), 400
    if processCreate(request.json, r, lookupTree):
        return jsonify({"success":"true"}), 201
    return jsonify({"error":"entry already exists"}), 500

# updating restaurant data
@app.route('/put', methods=['POST'])
def put():
    if not request.json:
        return jsonify({"error":"invalid format"}), 400
    if processUpdate(request.json, r):
        return jsonify({"success":"true"}), 201
    return jsonify({"error":"couldn't process update"}), 500

# fetching restaurant data
@app.route('/get', methods=['POST'])
def get():
    if not request.json:
        return jsonify({"error":"invalid format"}), 400
    d = r.get(request.json["host"])
    if d:
        return jsonify(d),200
    return jsonify({"error":"entry doesn't exist"}),400

# list restaurants
# TODO: list restaurants nearby
@app.route('/list', methods=['GET'])
def list():
    return jsonify({
        k:True
        for k in r.keys('*')
    })

# autocomplete search
# TODO: only return a fixed number
@app.route('/lookup/<prefix>', methods=['GET'])
def lookup(prefix):
    l = lookupTree.lookup(prefix)
    return jsonify(l)

# placing orders
@app.route('/place', methods=['POST'])
def place():
    if not request.json:
        return jsonify({"error":"invalid format"}), 400
    if placeOrder(request.json, r):
        return jsonify({"success":"true"}),201
    return jsonify({"error":"invalid format"}), 400

@app.route('/fulfill', methods=['POST'])
def fulfill():
    if not request.json:
        return jsonify({"error":"invalid format"}), 400
    if fulfillOrder(request.json, r):
        return jsonify({"success":"true"}),201
    return jsonify({"error":"invalid format"}), 400
