import requests

<<<<<<< HEAD
r = requests.post("http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/create",json={"host":"The Walrus"})

print(r.json())

r = requests.post("http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/get",json={"host":"The Walrus"})
=======
r = requests.post("http://localhost:8080/create",json={"host":"The Walrus"})

print(r.json())

r = requests.post("http://localhost:8080/get",json={"host":"The Walrus"})
>>>>>>> 4f57714c39d31fbfa5f1be15f2d7c471d1ade81e

print(r.json())

r = requests.post(
<<<<<<< HEAD
        "http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/put",
=======
        "http://localhost:8080/put",
>>>>>>> 4f57714c39d31fbfa5f1be15f2d7c471d1ade81e
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
<<<<<<< HEAD
        "http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/get",
=======
        "http://localhost:8080/get",
>>>>>>> 4f57714c39d31fbfa5f1be15f2d7c471d1ade81e
        json={
            "host":"The Walrus"
        }
)

print(r.json())

r = requests.post(
<<<<<<< HEAD
        "http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/put",
=======
        "http://localhost:8080/put",
>>>>>>> 4f57714c39d31fbfa5f1be15f2d7c471d1ade81e
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
