import sys
import signal
import argparse
from iksmproxy3.config import base as config
import iksmproxy3.proxy.base as proxy

def main():
    print("INIT: Initialize iksmproxy3...")
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', dest='confpath',
        help='Config file path(Default: /etc/iksmproxy/iksmproxy3.conf)')
    args = parser.parse_args()
    if args.confpath is not None:
        conf = config.initConfig(args.confpath)
    else:
        conf = config.initConfig()
    if not conf:
        sys.exit(1)
    proxy_worker = proxy.Proxy(conf)
    signal.signal(signal.SIGHUP, proxy_worker.stop)
    signal.signal(signal.SIGINT, proxy_worker.stop)
    signal.signal(signal.SIGQUIT, proxy_worker.stop)
    signal.signal(signal.SIGTERM, proxy_worker.stop)
    proxy_worker.run()

