import usocket as socket
import network
import time


class WifiModule(object):

    def __init__(self):
        self.ssid = 'NombreRed'
        self.access_point = None
        self.conn = None
        #self.CONTENT = """HTTP/1.0 200 OK
        #Content-Type: text/html
        #<!DOCTYPE html>
        self.CONTENT = """<html> <head> <title>NodeMCU Configuracion de red</title> <meta name="viewport" content="width=device-width, initial-scale=1"> <meta charset="utf8"> <style type="text/css"> .login-page{width:360px;margin:auto}.form{position:relative;z-index:1;background:#FFF;max-width:360px;padding:45px;text-align:center;box-shadow:0 0 20px 0 rgba(0,0,0,0.2),0 5px 5px 0 rgba(0,0,0,0.24)}.form input{font-family:"Roboto",sans-serif;outline:0;background:#f2f2f2;width:100%;border:0;margin:0 0 15px;padding:15px;box-sizing:border-box;font-size:14px}.form .button{font-family:"Roboto",sans-serif;text-transform:uppercase;outline:0;background:#4CAF50;width:100%;border:0;padding:15px;color:#FFF;font-size:14px;-webkit-transition:all .3 ease;transition:all .3 ease;cursor:pointer}.form .button:hover,.form .button:active,.form .button:focus{background:#43A047}.form .message{margin:15px 0 0;color:#b3b3b3;font-size:12px}.form .message a{color:#4CAF50;text-decoration:none}.form .register-form{display:none}.container{position:relative;z-index:1;max-width:300px;margin:0 auto}.container:before,.container:after{content:"";display:block;clear:both}.container .info{margin:50px auto;text-align:center}.container .info h1{margin:0 0 15px;padding:0;font-size:36px;font-weight:300;color:#1a1a1a}.container .info span{color:#4d4d4d;font-size:12px}.container .info span a{color:#000;text-decoration:none}.container .info span .fa{color:#EF3B3A}body{background:#76b852;background:-webkit-linear-gradient(right,#76b852,#8DC26F);background:-moz-linear-gradient(right,#76b852,#8DC26F);background:-o-linear-gradient(right,#76b852,#8DC26F);background:linear-gradient(to left,#76b852,#8DC26F);font-family:"Roboto",sans-serif;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale} .styled-select{height:45px;overflow:hidden}.styled-select select{background:transparent;border:none;font-size:18px;height:29px;padding:5px;width:268px}.rounded{-webkit-border-radius:20px;-moz-border-radius:20px;border-radius:20px}.semi-square{-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px}.slate{background-color:#ddd}.green{background-color:#43A047}.blue{background-color:#3b8ec2}.yellow{background-color:#eec111}.black{background-color:#000}.slate select{color:#000}.green select{color:#fff}.blue select{color:#fff}.yellow select{color:#000}.black select{color:#fff} </style> </head> <body> <div class="login-page"> <div class="form">%%MSG%% <h2>Configurar Red</h2> <form class="login-form" action="/config"> <div class="styled-select green semi-square"> <select name="ssid"> %%SELECT%% </select> </div> <br> <input name="password" type="password" placeholder="password"/> <input class="button" type="submit" value="conectar"> </form> </div> </div> </body></html>
        """

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

    def scan(self):
        self.conn = network.WLAN(network.STA_IF)
        self.conn.active(True)
        wifis = self.conn.scan()
        self.external_aps = wifis if len(wifis) < 6 else wifis[:6]
        wifis = None
        self.conn.active(False)
        self.conn = None

    def webserver(self, led=None):
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
        while not configured:
            print("4")
            client_sock, client_addr = s.accept()
            client_stream = client_sock
            print("Request:")
            req = client_stream.readline()
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
                    ssid = d["ssid"].replace("+", " ")
                    password = d["password"]
                    print("Red: {}, Password: {}".format(ssid, password))
                    configured = True
                    client_sock.sendall(self.htmlconf)
                except Exception as e:
                    print("Config Error: {}".format(str(e)))

            elif api == b'/':
                print("send content")
                self.CONTENT = self.CONTENT.replace("%%SELECT%%", selects).replace("%%MSG%%", msg)
                print(self.CONTENT)
                client_sock.send(self.CONTENT)
                print("close socket")

            client_sock.close()
        print("end while webserver")


if __name__ == "__main__":
    print("Start module")
    wifi = WifiModule()
    wifi.scan()
    wifi.start_ap()
    wifi.webserver()
