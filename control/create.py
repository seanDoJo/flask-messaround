import sys
from subprocess import Popen, PIPE
import json
import os
import tempfile
import re
import requests

def hostify(h):
    s = re.sub(r"[^\w\s]", "", h.lower())
    return re.sub(r"\s+", "-", s)

host = sys.argv[1]
number = sys.argv[2]
address = sys.argv[3]

#TODO: determine region from google
#TODO: select ami based on region
#TODO: determine key name from region
#TODO: determine security group from region
#TODO: determine subnet from region

front = Popen(
    [
        'aws',
        'ec2',
        'run-instances',
        '--region',
        'us-east-2',
        '--image-id',
        'ami-25615740',
        '--count',
        '1',
        '--instance-type',
        't2.micro',
        '--key-name',
        'instance1',
        '--security-group-ids',
        'sg-0cae6e997c3bbcb91',
        '--subnet-id',
        'subnet-3ee3df73',
        '--user-data',
        'file://launch/front.launch'
    ],
    stdout=PIPE,
    stderr=PIPE
)

stdout, stderr = front.communicate()

j = json.loads(stdout)

front_ip = j['Instances'][0]['PrivateIpAddress']
front_id = j['Instances'][0]['InstanceId']

queue = Popen(
    [
        'aws',
        'ec2',
        'run-instances',
        '--region',
        'us-east-2',
        '--image-id',
        'ami-25615740',
        '--count',
        '1',
        '--instance-type',
        't2.micro',
        '--key-name',
        'instance1',
        '--security-group-ids',
        'sg-0b4efff588cd6b30e',
        '--subnet-id',
        'subnet-3ee3df73',
        '--user-data',
        'file://launch/queue.launch'
    ],
    stdout=PIPE,
    stderr=PIPE
)

stdout, stderr = queue.communicate()

j = json.loads(stdout)

queue_ip = j['Instances'][0]['PrivateIpAddress']
queue_id = j['Instances'][0]['InstanceId']

try:
    with open("launch/nginx.launch", 'w+') as tmp:
        tmp.write(
"""
#!/bin/bash

yum update -y
yum install -y git python35
cd /home/ec2-user && git clone https://github.com/seanDoJo/flask-messaround.git
mkdir /home/ec2-user/flask-messaround/nginx/conf
chown -R ec2-user /home/ec2-user/flask-messaround
cd /home/ec2-user/flask-messaround/nginx && /usr/bin/python35 gen_conf.py {} {}
chown -R ec2-user /home/ec2-user/flask-messaround
cd /home/ec2-user/flask-messaround && make nginx
""".format(front_ip, queue_ip)
            )

    nginx = Popen(
        [
            'aws',
            'ec2',
            'run-instances',
            '--region',
            'us-east-2',
            '--image-id',
            'ami-25615740',
            '--count',
            '1',
            '--instance-type',
            't2.micro',
            '--key-name',
            'instance1',
            '--security-group-ids',
            'sg-0a0a33d5d5babbeab',
            '--subnet-id',
            'subnet-3ee3df73',
            '--user-data',
            'file://launch/nginx.launch'
        ],
        stdout=PIPE,
        stderr=PIPE
    )

    stdout, stderr = nginx.communicate()

    j = json.loads(stdout)

    nginx_ip = j['Instances'][0]['PrivateIpAddress']
    nginx_id = j['Instances'][0]['InstanceId']

    r = requests.post(
        "http://ec2-52-14-58-91.us-east-2.compute.amazonaws.com:8000/addconf",
        json={
            'url': "{}{}".format(hostify(host), number),
            'ip_addr': nginx_ip,
            'port': 8080
        }
    )

    print(r)

finally:
    os.remove("/home/ec2-user/flask-messaround/control/launch/nginx.launch")
