from subprocess import Popen, PIPE
import json
import os
import re
import requests
from sql import Host
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from time import sleep

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

def genLaunch(url):
    queueData = """
#!/bin/bash

yum update -y
yum install -y git
cd /home/ec2-user && git clone https://github.com/seanDoJo/flask-messaround.git
chown -R ec2-user /home/ec2-user/flask-messaround
export APP_ID={}
export APP_SECRET={}
export HOST={}
cd /home/ec2-user/flask-messaround/uwsgi && make go
""".format(os.environ['APP_ID'], os.environ['APP_SECRET'], url)
    return queueData

def notifyProxy(url, ip, read, write):
    return requests.post(
        "http://ec2-18-217-113-46.us-east-2.compute.amazonaws.com:8000/addqueue",
        json={
            'url': "{}".format(url),
            'ip_addr': ip,
            'read_port': read,
            'write_port': write
        }
    )

if __name__ == '__main__':
    shdir = '/dev/shm'
    engine = create_engine("sqlite:///test_db.db")
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    while True:
        filenames = []
        for (paths, names, filenames) in os.walk(shdir):
            files.extend(filenames)

        if len(filenames):
            with open(filenames[0], 'r') as ftoadd:
                newData = json.loads(ftoadd.read())
            host = newData['host']
            number = newData['store_id']
            url = "{}{}".format(hostify(host), number)
            address = newData['address']

            queue_ip, queue_id = tempAndSpawn(genLaunch(url), 'sg-0b4efff588cd6b30e', 'subnet-3ee3df73')

            newHost = Host(
                host=host,
                url=url,
                address=address,
                latitude="wip",
                longitude="wip",
                queue=queue_ip
            )

            session.add(newHost)
            session.commit()

            notifyProxy(url, queue_ip, 8000, 8080)
            os.remove(filenames[0])
        sleep(5)
