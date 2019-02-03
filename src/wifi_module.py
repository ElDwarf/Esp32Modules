import machine
import usocket as socket
import network
import time
from configuration import Configuration


class WifiModule(object):

    def __init__(self):
        self.access_point = None
        self.conn = None
        conf = Configuration()
        ssid_temp = conf.get_settings(category="network", name="ssid")
        pass_temp = conf.get_settings(category="network", name="password")
        if ssid_temp and pass_temp:
            self.ssid = ssid_temp
            self.password = pass_temp
            if not self.connect():
                self.ssid = "Esp32"
                self.scan()
                print("Prueba1")
                self.start_ap()
                print("Prueba2")
                self.webserver()
                pin_dis = machine.Pin(25, machine.Pin.OUT)
                pin_dis.value(1)
                pin_con = machine.Pin(13, machine.Pin.OUT)
                pin_con.value(0)
            else:
                pin_dis = machine.Pin(25, machine.Pin.OUT)
                pin_dis.value(0)
                pin_con = machine.Pin(13, machine.Pin.OUT)
                pin_con.value(1)
        else:
            self.ssid = "Esp32"
            print("Prueba3")
            self.scan()
            print("Prueba4")
            self.start_ap()
            print("Prueba5")
            self.webserver()
            pin_dis = machine.Pin(25, machine.Pin.OUT)
            pin_dis.value(1)
            pin_con = machine.Pin(13, machine.Pin.OUT)
            pin_con.value(0)
        #self.CONTENT = """HTTP/1.0 200 OK
        #Content-Type: text/html
        #<!DOCTYPE html>
        #self.htmlconf = """HTTP/1.0 200 OK
        #Content-Type: text/html
        #
        #<!DOCTYPE html>
        #<html>
        #    <head> <title>ESP8266 Pins</title> </head>
        #    <body> <h1>Conectando NodeMCU a su red...</h1>
        #
        #    </body>
        #</html>
        #"""

    def start_ap(self):
        """
        Start your own ap to allow configuring wifi connection.
        """
        pin_ap = machine.Pin(14, machine.Pin.OUT)
        pin_ap.value(1)
        self.access_point = network.WLAN(network.AP_IF)
        self.access_point.active(True)
        self.access_point.config(essid=self.ssid, authmode=1)

    def stop_ap(self):
        """
        Stop your own ap to allow configuring wifi connection.
        """
        pin_ap = machine.Pin(14, machine.Pin.OUT)
        pin_ap.value(0)
        self.access_point.active(False)
        self.access_point = None

    def connect(self, ssid="", pwd=""):
        """
        Connect wifi network
        """
        if ssid == "":
            ssid = self.ssid
            pwd = self.password
        print(ssid)
        print(pwd)
        self.conn = network.WLAN(network.STA_IF)
        self.conn.active(True)
        intent_counter = 0
        if not self.conn.isconnected():
            self.conn.connect(ssid, pwd)
            while not self.conn.isconnected():
                time.sleep(.2)
                if intent_counter > 50:
                    break
                intent_counter += 1
        print("a1")
        if not self.conn.isconnected():
            print("a2")
            self.conn.active(False)
            self.conn = None
            pin_dis = machine.Pin(25, machine.Pin.OUT)
            pin_dis.value(1)
            pin_con = machine.Pin(13, machine.Pin.OUT)
            pin_con.value(0)
            print("a3")
            return False
        else:
            conf = Configuration()
            ssid_temp = conf.set_settings(ssid, category="network", name="ssid")
            pass_temp = conf.set_settings(pwd, category="network", name="password")
            print("a4")
            pin_dis = machine.Pin(25, machine.Pin.OUT)
            pin_dis.value(0)
            pin_con = machine.Pin(13, machine.Pin.OUT)
            pin_con.value(1)
            return self.conn.isconnected()

    def disconnect(self):
        if self.conn is not None:
            self.conn.disconnect()

    def scan(self):
        pin_scan = machine.Pin(12, machine.Pin.OUT)
        pin_scan.value(1)
        self.conn = network.WLAN(network.STA_IF)
        self.conn.active(True)
        wifis = self.conn.scan()
        self.external_aps = wifis if len(wifis) < 6 else wifis[:6]
        wifis = None
        self.conn.active(False)
        self.conn = None
        pin_scan.value(0)

    def webserver(self, led=None):
        print("00")
        HTML_PAGE = """<html> <head> <title>NodeMCU Configuracion de red</title> <meta name="viewport" content="width=device-width, initial-scale=1"> <meta charset="utf8"> <style type="text/css"> .login-page{width:360px;margin:auto}.form{position:relative;z-index:1;background:#FFF;max-width:360px;padding:45px;text-align:center;box-shadow:0 0 20px 0 rgba(0,0,0,0.2),0 5px 5px 0 rgba(0,0,0,0.24)}.form input{font-family:"Roboto",sans-serif;outline:0;background:#f2f2f2;width:100%;border:0;margin:0 0 15px;padding:15px;box-sizing:border-box;font-size:14px}.form .button{font-family:"Roboto",sans-serif;text-transform:uppercase;outline:0;background:#4CAF50;width:100%;border:0;padding:15px;color:#FFF;font-size:14px;-webkit-transition:all .3 ease;transition:all .3 ease;cursor:pointer}.form .button:hover,.form .button:active,.form .button:focus{background:#43A047}.form .message{margin:15px 0 0;color:#b3b3b3;font-size:12px}.form .message a{color:#4CAF50;text-decoration:none}.form .register-form{display:none}.container{position:relative;z-index:1;max-width:300px;margin:0 auto}.container:before,.container:after{content:"";display:block;clear:both}.container .info{margin:50px auto;text-align:center}.container .info h1{margin:0 0 15px;padding:0;font-size:36px;font-weight:300;color:#1a1a1a}.container .info span{color:#4d4d4d;font-size:12px}.container .info span a{color:#000;text-decoration:none}.container .info span .fa{color:#EF3B3A}body{background:#76b852;background:-webkit-linear-gradient(right,#76b852,#8DC26F);background:-moz-linear-gradient(right,#76b852,#8DC26F);background:-o-linear-gradient(right,#76b852,#8DC26F);background:linear-gradient(to left,#76b852,#8DC26F);font-family:"Roboto",sans-serif;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale} .styled-select{height:45px;overflow:hidden}.styled-select select{background:transparent;border:none;font-size:18px;height:29px;padding:5px;width:268px}.rounded{-webkit-border-radius:20px;-moz-border-radius:20px;border-radius:20px}.semi-square{-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px}.slate{background-color:#ddd}.green{background-color:#43A047}.blue{background-color:#3b8ec2}.yellow{background-color:#eec111}.black{background-color:#000}.slate select{color:#000}.green select{color:#fff}.blue select{color:#fff}.yellow select{color:#000}.black select{color:#fff} </style> </head> <body> <div class="login-page"> <div class="form">%%MSG%% <h2>Configurar Red</h2> <form class="login-form" action="/config"> <div class="styled-select green semi-square"> <select name="ssid"> %%SELECT%% </select> </div> <br> <input name="password" type="password" placeholder="password"/> <input class="button" type="submit" value="conectar"> </form> </div> </div> </body></html>
        """
        pin_ac = machine.Pin(27, machine.Pin.OUT)
        configured = False
        print("0")
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        print("1")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 80))
        s.listen(5)
        print("2")

        select = '<option value="{0}">{0}</option>'
        selects = "".join([select.format(str(i[0], 'utf-8')) for i in self.external_aps])

        #if self.settings.get("msg"):
        #    msg = '<h2 style="color:red;">{}</h2>'.format(self.settings["msg"])
        #else:
        #    msg = ""
        msg = ""
        print("3")
        while self.conn is None:
            print("4")
            client_sock, client_addr = s.accept()
            client_stream = client_sock
            print("Request:")
            req = client_stream.readline()
            pin_ac.value(1)
            print(req)


            print('client connected from', addr)
            while True:
                h = client_stream.readline()
                if h == b"" or h == b"\r\n" or h == None:
                    break
                print(h)
            print("\n\n")
            request_url = req[4:-11]

            api = request_url[:7]
            print("url {}".format(api))
            if api == b'/config':
                params = str(request_url[8:],  'utf-8')
                print("params: {}".format(params))
                try:
                    d = {key: value for (key, value) in [x.split('=') for x in params.split('&')]}
                    print("dict {}".format(str(d)))
                    self.ssid = d["ssid"].replace("+", " ")
                    self.password = d["password"].replace("+", " ")
                    self.stop_ap()
                    connected = self.connect()
                    time.sleep(.1)
                    if not connected:
                        print("start_ap")
                        self.start_ap()
                    else:
                        print("connect")
                        client_sock.close()
                        return
                except Exception as e:
                    print("Config Error: {}".format(str(e)))

            elif api == b'/':
                print("send content")
                HTML_PAGE = HTML_PAGE.replace("%%SELECT%%", selects).replace("%%MSG%%", msg)
                print(HTML_PAGE)
                client_sock.send(HTML_PAGE)
                print("close socket")
            pin_ac.value(0)
            client_sock.close()
        print("end while webserver")


if __name__ == "__main__":
    print("Start module")
    wifi = WifiModule()
    wifi.scan()
    wifi.start_ap()
    wifi.webserver()
