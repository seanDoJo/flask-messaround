from flask import Flask, request, json, jsonify
from subprocess import Popen, PIPE

app = Flask(__name__)

@app.route('/addqueue', methods=['POST'])
def addconf():
    path = request.json['url']
    ip = request.json['ip_addr']
    read_port = request.json['read_port']
    write_port = request.json['write_port']

    with open("conf/{}.conf".format(path), 'w+') as f:
        f.write(
"""
location /update/{} {{
    include uwsgi_params;
    uwsgi_pass {}:{};

    proxy_redirect off;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Host $server_name;
}}
""".format(path, ip, write_port)
        )

        f.write(
"""
location /orders/{} {{
    include uwsgi_params;
    uwsgi_pass {}:{};

    proxy_redirect off;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Host $server_name;
}}
""".format(path, ip, read_port)
        )

    with open('lastupdate.log', 'w+') as log:
        update = Popen(
            [
                'service',
                'nginx',
                'restart'
            ],
            stdout=log,
            stderr=log
        )

    return "received", 201
