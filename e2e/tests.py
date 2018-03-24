import requests

r = requests.post("http://localhost:5000/create",json={"host":"The Walrus"})

print(r.json())

r = requests.post("http://localhost:5000/get",json={"host":"The Walrus"})

print(r.json())

r = requests.post(
        "http://localhost:5000/put",
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
        "http://localhost:5000/get",
        json={
            "host":"The Walrus"
        }
)

print(r.json())

r = requests.post(
        "http://localhost:5000/put",
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
        "http://localhost:5000/get",
        json={
            "host":"The Walrus"
        }
)

print(r.json())

r = requests.get("http://localhost:5000/list")
print(r.json())

r = requests.get("http://localhost:5000/lookup/walr")
print(r.json())
