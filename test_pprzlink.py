#!/usr/bin/python3

#exemple @ ~/paparazzi/sw/ground_segment/python/opensky-network/opensky.py


import sys
from os import path, getenv
import time

PPRZ_HOME = getenv("PAPARAZZI_HOME", path.normpath(path.join(path.dirname(path.abspath(__file__)), '..')))
sys.path.append(PPRZ_HOME + "/var/lib/python")

#print(PPRZ_HOME + "/var/lib/python")

from pprzlink.ivy import IvyMessagesInterface
from pprzlink.message import PprzMessage


class UTM_center(object):
    def __init__(self, verbose=True):
        self._interface = IvyMessagesInterface("UTM_center")
        self.msg_list = {}
        self.last_receive = time.time()
        self.verbose = verbose
        if self.verbose:
            print("Starting UTM center")
        self._interface.subscribe(self.update_ac, PprzMessage("ground", "FLIGHT_PARAM"))


    def stop(self):
        if self.verbose:
            print("Shutting down UTM center")
        if self._interface is not None:
            self._interface.shutdown()

    def __del__(self):
        self.stop()

    def update_ac(self, msg_id, msg):
        self.last_receive = time.time()
        self.msg_list[msg_id] = (self.last_receive, float(msg['lat']), float(msg['long']))
        print ("update_ac msg= " + str(msg))

    def send_intruder_msg(self):
        msg = PprzMessage("ground", "INTRUDER")
        msg['id'] = 1
        msg['name'] = 'Test'
        msg['lat'] = 363970000
        msg['lon'] = 280500000
        msg['alt'] = 300000
        msg['course'] = 10.0
        msg['speed'] = 12.0
        msg['climb'] = 1.0
        msg['itow'] = 1
        if self.verbose:
            print (msg)
        self._interface.send(msg)

if __name__ == "__main__":
    utm = UTM_center()
    time.sleep(0.1)
    utm.send_intruder_msg()




