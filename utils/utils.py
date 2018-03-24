from flask import jsonify, json
from datetime import datetime
import requests

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

def validateToken(user_token, access_token):
    url = "https://graph.facebook.com/debug_token?input_token={}&access_token={}".format(user_token, access_token)
    r = requests.get(url)
    data = r.json()

    if 'error' in data:
        return 1

    if not data['is_valid']:
        return 2

    return 0

def getAccessToken():
    # dummy data
    app_id = '22847227106406a'
    app_secret = '6c78b1d22492ec45834762db2e4dcfef'
    link = 'https://graph.facebook.com/oauth/access_token?client_id={}&client_secret={}&grant_type=client_credentials'.format(app_id, app_secret)

    return requests.get(link).json()['access_token']
