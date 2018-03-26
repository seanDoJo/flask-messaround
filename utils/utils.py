from flask import jsonify, json
from datetime import datetime
import requests

import os

def processUpdate(form, red):
    if 'host' not in form:
        return False

    host = form['host']
    data = red.get(host)
    if not data:
        return False
    data = json.loads(data)

    # TODO: add keyerror handling and logging
    for category in form['categories']:
        if category not in data['categories']:
            data['categories'][category] = {}

        for item in form['categories'][category]:
            if item not in data['categories'][category]:
                data['categories'][category][item] = {
                        'price' : -1., 
                        'availability' : False
                }

            #TODO: only allow valid keys
            for k in form['categories'][category][item]:
                data['categories'][category][item][k] = form['categories'][category][item][k]
    red.set(host, json.dumps(data))

    return True

def processCreate(form, red, t):
    if 'host' not in form:
        return jsonify({"error":"invalid format"}), 400

    host = form['host']
    if red.get(host):
        return jsonify({"error":"entry already exists"}), 400

    data = {
            'categories' : {},
    }

    t.insert(host)
    red.set(host, json.dumps(data))

    res = requests.post("http://172.31.37.250:8080/orders/update/create", json={"host": host})

    print(res)

    return jsonify(res.json()), 200

def placeOrder(form, red):
    if 'host' not in form or 'order' not in form:
        return jsonify({'error':'invalid format'}), 400

    host = form['host']
    order = form['order']

    order['state'] = 0
    order['time'] = str(datetime.now())

    d = {'host':host, 'order':order}

    res = requests.post("http://172.31.34.71/write/add", json=d)

    return jsonify(res.json()), 200

def getOrders(form, red):
    if 'host' not in form:
        return jsonify({'error':'invalid format'}), 400

    res = requests.post("http://172.31.34.71/read/list", json={'host':form['host']})

    return jsonify(res.json()), 200


def fulfillOrder(form, red):
    if 'host' not in form:
        return False

    host = form['host']
    hostData = red.get(host)
    if not hostData:
        return False

    hostData = json.loads(hostData)

def validateToken(access_token):
    def dec(func):
        def handle(*args, **kwargs):
            token = kwargs.pop("token", None)

            """
            data = requests.get(
                "https://graph.facebook.com/debug_token?input_token={}&access_token={}".format(token, access_token)
            ).json()['data']

            if 'error' in data:
                    return jsonify({'error' : 'invalid user token'}),400

            if not data['is_valid']:
                    return jsonify({'error' : 'invalid user token'}),400
            """

            return func(*args, **kwargs)

        handle.__name__ = func.__name__
        return handle 
    return dec

def getAccessToken():
    app_id = os.environ["APP_ID"]
    app_secret = os.environ["APP_SECRET"]
    link = 'https://graph.facebook.com/oauth/access_token?client_id={}&client_secret={}&grant_type=client_credentials'.format(app_id, app_secret)

    j = requests.get(link).json()

    return j["access_token"]
