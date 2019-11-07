import requests
import json


class SlackDriver():
    def __init__(self, conf):
        print("INIT: Setup slack driver.")
        self.conf = conf
        self.s = requests.session()

    def send_data(self, data):
        print("POST: From discord driver. Data is " + data)
        content = self.conf['SLACK']['command_head'] + " " + data
        payload = {"text": content}
        r = self.s.post(self.conf['SLACK']['webhook_url'], data = json.dumps(payload))
        #print(r.text.encode("utf-8"))
