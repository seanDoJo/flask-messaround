from flask import Flask, request, jsonify, json
from utils.utils import processUpdate, processCreate, validateToken, getAccessToken
from utils.sql import Host, Base, HostData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests
import redis
import os

def setupSqlSession():
    mysqlAddr = requests.get("http://172.31.36.195:8000/get_preauth/MYSQL_IP").json()['success']
    mysqlUser = requests.get("http://172.31.36.195:8000/get_preauth/MYSQL_USR").json()['success']
    mysqlPass = requests.get("http://172.31.36.195:8000/get_preauth/MYSQL_PASS").json()['success']
    mysqlUrl = "mysql+pymysql://{}:{}@{}:3306/metadata".format(mysqlUser, mysqlPass, mysqlAddr)

    engine = create_engine(mysqlUrl)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    return session

# server initialization
app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)
session = setupSqlSession()

accessToken = getAccessToken()

# fetching restaurant data
@app.route('/get/<host>/<token>', methods=['GET'])
@validateToken(accessToken, r)
def get(host):
    hostname = r.get(host)
    if not hostname:
        exists = False
        for h in session.query(Host).filter_by(url=host):
            exists = True
            r.set(host, h.host)
            hostname = h.host
            break
        if not exists:
            return jsonify({"error": "host doesn't exist"}), 400

    # TODO: this is terrible
    data = {"categories": {}}
    for item in session.query(HostData).filter_by(host=hostname):
        if item.category not in data["categories"]:
            data["categories"][item.category] = {}

        data["categories"][item.category][item.item] = {
                "price": item.price,
                "description": item.description,
                "photo": item.photo,
                "options": item.options,
                "availability": item.availability,
        }
    return jsonify(data), 200

@app.route('/list/<token>', methods=['GET'])
@validateToken(accessToken, r)
def list():
    hosts = {}
    for h in session.query(Host):
        hosts[h.host] = {
            'url': h.url,
            'lat': h.latitude,
            'long': h.longitude,
            'addr': h.address,
            'photo': h.photo,
        }
    return jsonify(hosts), 200

@app.route('/update/<host>/<token>', methods=['POST'])
@validateToken(accessToken, r)
def update(host):
    if not request.json:
        return jsonify({"error": "invalid request format"}), 400
    if 'categories' not in request.json:
        return jsonfiy({"error": "update format incorrect"}), 400

    hostname = r.get(host)
    if not hostname:
        exists = False
        for h in session.query(Host).filter_by(url=host):
            exists = True
            r.set(host, h.host)
            hostname = h.host
            break
        if not exists:
            return jsonify({"error": "host doesn't exist"}), 400

    # TODO: move all updates to single transaction
    for cat in request.json['categories']:
        for item in request.json['categories'][cat]:
            exists = False
            for existingItem in session.query(HostData).filter_by(host=hostname, category=cat, item=item):
                exists = True
                existingItem.price = request.json['categories'][cat][item]['price']
                session.commit()
                break
            if not exists:
                newItem = HostData(
                    host=hostname,
                    item=item,
                    category=cat,
                    price=request.json['categories'][cat][item]['price'],
                    description="NULL",
                    photo="NULL",
                    options="NULL",
                    availability="NULL",
                )

                session.add(newItem)
                session.commit()
    return jsonify({"success": "received"}), 201
