import sys
from subprocess import Popen, PIPE
import json
import os
import tempfile
import re
import requests

host = sys.argv[1]
number = sys.argv[2]
address = sys.argv[3]

def hostify(h):
    s = re.sub(r"[^\w\s]", "", h.lower())
    return re.sub(r"\s+", "-", s)

def spawn(securityGroupID, subnetID, userData):
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
            '{}'.format(securityGroupID),
            '--subnet-id',
            '{}'.format(subnetID),
            '--user-data',
            'file://{}'.format(userData)
        ],
        stdout=PIPE,
        stderr=PIPE
    )

    stdout, stderr = front.communicate()
    j = json.loads(stdout)

    ip = j['Instances'][0]['PrivateIpAddress']
    iid = j['Instances'][0]['InstanceId']

    return ip,iid

def tempAndSpawn(launchData, securityGroupID, subnetID):
    fname = "launch/{}_{}_{}.launch".format(host, number, securityGroupID)
    tmp = open(fname, "w+")
    ip = None
    iid = None
    tmp.write(launchData)
    tmp.close()
    ip, iid = spawn(securityGroupID, subnetID, fname)

    return ip,iid
            

#TODO: determine region from google
#TODO: select ami based on region
#TODO: determine key name from region
#TODO: determine security group from region
#TODO: determine subnet from region

frontData = """
#!/bin/bash

yum update -y
yum install -y git
cd /home/ec2-user && git clone https://github.com/seanDoJo/flask-messaround.git
chown -R ec2-user /home/ec2-user/flask-messaround
export APP_ID={}
export APP_SECRET={}
export HOST="{}"
cd /home/ec2-user/flask-messaround/app && make go
""".format(os.environ['APP_ID'], os.environ['APP_SECRET'], host+str(number))

queueData = """
#!/bin/bash

yum update -y
yum install -y git
cd /home/ec2-user && git clone https://github.com/seanDoJo/flask-messaround.git
chown -R ec2-user /home/ec2-user/flask-messaround
export APP_ID={}
export APP_SECRET={}
export HOST={}{}
cd /home/ec2-user/flask-messaround/uwsgi && make go
""".format(os.environ['APP_ID'], os.environ['APP_SECRET'], hostify(host), number)

#front_ip, front_id = tempAndSpawn(frontData, 'sg-0cae6e997c3bbcb91', 'subnet-3ee3df73')
queue_ip, queue_id = tempAndSpawn(queueData, 'sg-0b4efff588cd6b30e', 'subnet-3ee3df73')

r = requests.post(
    "http://ec2-18-217-113-46.us-east-2.compute.amazonaws.com:8000/addqueue",
    json={
        'url': "{}{}".format(hostify(host), number),
        'ip_addr': queue_ip,
        'read_port': 8000,
        'write_port': 8080
    }
)
print(r)
