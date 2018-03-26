import requests
import os

d = os.getenv("ACCESS_TOKEN", "none")
r = requests.post("http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/data/create/{}".format(d),json={"host":"The Walrus"})
print(r.json())
exit(0)

r = requests.post("http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/get/{}".format(d),json={"host":"The Walrus"})
print(r)
print(r.json())

r = requests.post("http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/listorders/{}".format(d), json={'host':'The Walrus'})
print(r.json())

r = requests.post(
        "http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/put/{}".format(d),
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
print(r)
print(r.json())

r = requests.post(
        "http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/place/{}".format(d),
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

r = requests.post("http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/listorders/{}".format(d), json={'host':'The Walrus'})

print(r.json())

exit(0)

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
