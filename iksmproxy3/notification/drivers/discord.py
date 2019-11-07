import webcord

class DiscordDriver():
    def __init__(self, conf):
        print("INIT: Setup discord driver.")
        self.conf = conf
        self.hook = webcord.Webhook(self.conf['DISCORD']['webhook_url'])

    def send_data(self, data):
        print("POST: From discord driver. Data is " + data)
        content = self.conf['DISCORD']['command_head'] + " " + data
        self.hook.send_message(content, self.conf['DISCORD']['webhook_username'])
