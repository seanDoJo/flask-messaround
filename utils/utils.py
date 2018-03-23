from flask import jsonify

def processUpdate(form, red):
    if 'host' not in form:
        return False

    host = form['host']
    data = red.get(host)
    if not data:
        return False

    # TODO: add keyerror handling and logging
    for category in form['categories']:
        if category not in data['categories']:
            data['categories'][category] = []

        for item in form['categories'][category]:
            if item not in data['categories'][category]:
                data['categories'][category][item] = {
                        'price' : -1., 
                        'availability' : False
                }

            #TODO: only allow valid keys
            for k in form['categories'][category][item]:
                data['categories'][category][item][k] = form['categories'][category][item][k]

    return True

