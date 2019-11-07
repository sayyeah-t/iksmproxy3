from iksmproxy3.notification.drivers.discord import DiscordDriver
from iksmproxy3.notification.drivers.slack import SlackDriver


class ExampleDriver:
    def __init__(self):
        print("INIT: Setup example driver.")

    def send_data(self, data):
        print("POST: Just print a data from example driver. Data is " + data)


class Notificator:
    def __init__(self, conf):
        if conf['NOTIFICATION']['driver'] == 'discord':
            self.driver = DiscordDriver(conf)
        elif conf['NOTIFICATION']['driver'] == 'slack':
            self.driver = SlackDriver(conf)
        else:
            self.driver = ExampleDriver()

    def push_message(self, message):
        self.driver.send_data(message)

