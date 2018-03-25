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
        return False

    host = form['host']
    if red.get(host):
        return False

    data = {
            'categories' : {},
            'pending_orders' : [],
    }

    t.insert(host)
    red.set(host, json.dumps(data))

    return True

# TODO: at scale, this will be littered with
# race conditions
def placeOrder(form, red):
    if 'host' not in form or 'order' not in form:
        return False

    host = form['host']
    order = form['order']

    order['ready'] = False
    order['time'] = str(datetime.now())

    hostData = red.get(host)
    if not hostData:
        return False

    hostData = json.loads(hostData) 
    hostData['pending_orders'].append(form['order'])

    red.set(host, json.dumps(hostData))

    return True

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
            data = requests.get(
                "https://graph.facebook.com/debug_token?input_token={}&access_token={}".format(token, access_token)
            ).json()['data']

            if 'error' in data:
                    return jsonify({'error' : 'invalid user token'}),400

            if not data['is_valid']:
                    return jsonify({'error' : 'invalid user token'}),400

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
