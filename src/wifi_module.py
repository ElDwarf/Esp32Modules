import network
import time


class WifiModule(object):

    def __init__(self):
        self.ssid = 'NombreRed'
        self.access_point = None
        self.conn = None

    def start_ap(self):
        """
        Start your own ap to allow configuring wifi connection.
        """
        self.access_point = network.WLAN(network.AP_IF)
        self.access_point.active(True)
        self.access_point.config(essid=self.ssid, authmode=1)

    def stop_ap(self):
        """
        Stop your own ap to allow configuring wifi connection.
        """
        self.access_point.active(False)
        self.access_point = None

    def connect(self, ssid, pwd):
        """
        Connect wifi network
        """
        self.conn = network.WLAN(network.STA_IF)
        self.conn.active(True)
        intent_counter = 0
        if not self.conn.isconnected():
            self.conn.connect(ssid, pwd)
            while self.conn is not None and not self.conn.isconnected():
                time.sleep(.1)
                if intent_counter > 5:
                    break
                intent_counter += 1
        if not self.conn.isconnected():
            self.conn.active(False)
            self.conn = None
            return False
        else:
            return self.conn.isconnected()

    def disconnect(self):
        if self.conn is not None:
            self.conn.disconnect()
