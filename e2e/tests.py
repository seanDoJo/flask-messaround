import requests

r = requests.post("http://localhost:8080/create",json={"host":"The Walrus"})

print(r.json())

r = requests.post("http://localhost:8080/get",json={"host":"The Walrus"})

print(r.json())

r = requests.post(
        "http://localhost:8080/put",
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
        "http://localhost:8080/get",
        json={
            "host":"The Walrus"
        }
)

print(r.json())

r = requests.post(
        "http://localhost:8080/put",
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
        "http://localhost:8080/get",
        json={
            "host":"The Walrus"
        }
)

print(r.json())

r = requests.get("http://localhost:8080/list")
print(r.json())

r = requests.get("http://localhost:8080/lookup/walr")
print(r.json())

r = requests.post(
        "http://localhost:8080/place",
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
        "http://localhost:8080/get",
        json={
            "host":"The Walrus"
        }
)

print(r.json())
