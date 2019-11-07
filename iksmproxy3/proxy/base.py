import os
import fcntl
import time
import errno
import subprocess
from iksmproxy3.notification.driver import Notificator


class Proxy():
    def __init__(self, conf):
        self.loop = True
        self.conf = conf
        self.iksm_session = ""
        self.cmd = [self.conf['DEFAULT']['mitmdump_path'],
                "-p", self.conf['DEFAULT']['listen_port'],
                "-s", self.conf['DEFAULT']['mitmdump_ext_script_path']]
        self.notificator = Notificator(conf)

    def run(self):
        print("START: Proxy server is ready.")
        self.proc = subprocess.Popen(self.cmd, bufsize=0, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        flag = fcntl.fcntl(self.proc.stdout.fileno(), fcntl.F_GETFL)
        fcntl.fcntl(self.proc.stdout.fileno(), fcntl.F_SETFL, flag | os.O_NONBLOCK)
        output = ""
        while(self.loop):
            try:
                buf = self.proc.stdout.read()
                if buf is not None:
                    output = output + buf.decode('utf-8')
                    lines = output.splitlines()
                    for line in lines:
                        if line.find("iksm_session") != -1:
                            self.__extract_iksm_session(line)
                            self.__notificate()
                    if output[-1:] == "\n":
                        output = ""
                    else:
                        output = lines[-1]
            except IOError:
                break
            time.sleep(0.5)
        self.proc.terminate()
        self.proc.wait()


    def stop(self, signum, frame):
        print("STOP: Received a signal: " + "signal={}".format(signum))
        self.loop = False

    def __extract_iksm_session(self, msg):
        self.iksm_changed = False
        datalist = msg.split("; ")
        for data in datalist:
            if "iksm_session" in data:
                iksm_session_new = data.split("=")[1]
        if self.iksm_session != iksm_session_new:
            self.iksm_session = iksm_session_new
            self.iksm_changed = True

    def __notificate(self):
        self.notificator.push_message(self.iksm_session)
