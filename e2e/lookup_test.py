import requests

word = "walrus"
for i in range(1, len(word)+1):
    r = requests.get("http://ec2-18-188-95-46.us-east-2.compute.amazonaws.com:8080/lookup/{}".format(word[:i]))
    print("{} : {}".format(word[:i], r.json()))

