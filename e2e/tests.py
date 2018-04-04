import requests
import os

d = os.getenv("ACCESS_TOKEN", "none")
r = requests.get("http://ec2-18-217-113-46.us-east-2.compute.amazonaws.com/orders/the-walrus1/{}".format(d))
print(r)
print(r.json())
exit(0)

r = requests.post("http://ec2-52-14-58-91.us-east-2.compute.amazonaws.com/test1/",json={"host":"The Walrus"})
print(r)
print(r.json())

exit(0)

r = requests.post("http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/orders/get/list/{}".format(d), json={'host':'The Walrus'})
print(r.json())

r = requests.post(
        "http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/data/put/{}".format(d),
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
        "http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/data/put/{}".format(d),
        json={
            "host":"The Walrus",
            "categories" : {
                "Beer" : {
                    "Fat Tire" : {
                        "price":6.00,
                        "availability":True
                    }
                }
            }
        }
)
print(r.json())

r = requests.post(
        "http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/orders/update/add/{}".format(d),
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

r = requests.post("http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/orders/get/list/{}".format(d), json={'host':'The Walrus'})
print(r.json())

r = requests.post("http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/orders/update/state/{}".format(d), json={'host':'The Walrus', 'order_no' : 1, 'state' : 1})
print(r.json())

r = requests.get("http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/data/list/{}".format(d))
print(r.json())

r = requests.get("http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/data/lookup/{}/walr".format(d))
print(r.json())
