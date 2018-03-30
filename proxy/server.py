from flask import Flask, request, json, jsonify
from subprocess import Popen, PIPE

app = Flask(__name__)

@app.route('/addconf', methods=['POST'])
def addconf():
    path = request.json['url']
    ip = request.json['ip_addr']
    port = request.json['port']

    with open("conf/{}.conf".format(path), 'w+') as f:
        f.write(
"""
location /{} {{
    proxy_pass http://{}:{}/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Host $server_name;
}}
""".format(path, ip, port)
        )

    update = Popen(
        [
            'service',
            'nginx',
            'restart'
        ],
        stdout=PIPE,
        stderr=PIPE
    )

    stdout, stderr = update.communicate()

    return "received", 201
