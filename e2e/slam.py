import grequests

def response_handler(i):
    def re(response, **kwargs):
        print(response.json())
    return re

rs = [grequests.post("http://ec2-52-14-58-91.us-east-2.compute.amazonaws.com/thewalrus/data/get/token", json={"host":"The Walrus"}, callback=response_handler(i)) for i in range(2)]

rs += [grequests.post("http://ec2-52-14-58-91.us-east-2.compute.amazonaws.com/thewalrus/orders/get/list/token", json={"host":"The Walrus"}, callback=response_handler(i)) for i in range(2)]

r = grequests.map(rs)
