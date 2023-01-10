import requests


class Move:

    def __init__(self, url):
        req = requests.get(url)
        self.json = req.json()
        self.name = self.json["name"]
        self.power = self.json["power"]
        self.type = self.json["type"]["name"]


