from flask import jsonify, json
from datetime import datetime

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

