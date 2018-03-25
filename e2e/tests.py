import requests

d = "EAADPy1iOzAQBAPMKrmWG6GAqO2PYpRxZAsBfVdpWHxckPUNT64XEtcrrMQ0oJRatXZAZBUA0lKJNkgtUmLD80A1yEtQyxtjtIsZAprawshiajAl21lEH0pcju4kZBQaHXKWTtTqAFLecwvnAitZAe1fpclopcWrQVSpu9IV2w0Bj6R9e6XEpi4vLjOK7riNpcZD"

r = requests.post("http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/create/{}".format(d),json={"host":"The Walrus"})

print(r.json())

exit(0)

r = requests.post("http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/get",json={"host":"The Walrus"})

print(r.json())

r = requests.post(
        "http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/put",
        json={
            "host":"The Walrus",
            "categories" : {
                "Beer" : {
                    "Left Hand Milk Stout" : {
                        "price":5.00,
                        "availability":True
                    }
                }
            }
        }
)

print(r.json())

r = requests.post(
        "http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/get",
        json={
            "host":"The Walrus"
        }
)

print(r.json())

r = requests.post(
        "http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/put",
        json={
            "host":"The Walrus",
            "categories" : {
                "Beer" : {
                    "Left Hand Milk Stout" : {
                        "price":6.00,
                        "availability":True
                    }
                }
            }
        }
)

print(r.json())

r = requests.post(
        "http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/get",
        json={
            "host":"The Walrus"
        }
)

print(r.json())

r = requests.get("http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/list")
print(r.json())

r = requests.get("http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/lookup/walr")
print(r.json())

r = requests.post(
        "http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/place",
        json={
            "host" : "The Walrus",
            "order" : {
                "Sean Donohoe" : {
                    "Left Hand Milk Stout" : {
                        "quantity" : 2
                    }
                }
            }
        }
)
print(r.json())

r = requests.post(
        "http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/get",
        json={
            "host":"The Walrus"
        }
)

print(r.json())
