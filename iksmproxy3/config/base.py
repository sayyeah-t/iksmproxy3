import configparser

def initConfig(confPath = '/etc/iksmproxy3/iksmproxy3.conf'):
    print("INIT:Initialize configuration...(" + confPath + ")")
    conf = configparser.ConfigParser()
    try:
        conf.read(confPath)
    except configparser.Error:
        print("ERROR:Failedtoreadconfiguration.")
        return None
    return conf

