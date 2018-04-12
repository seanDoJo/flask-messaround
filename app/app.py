from flask import Flask, request, jsonify, json
from utils.utils import processUpdate, processCreate, validateToken, getAccessToken
from utils.sql import Host, Base, HostData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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
