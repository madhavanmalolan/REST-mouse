import BaseHTTPServer
import urlparse
import socket

import Xlib.display

HOST_NAME = ""
PORT_NUMBER = 12001

class MyHTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
	self.send_header("Content-type","text")
	self.end_headers()
    def do_GET(self):
        self.send_response(200)
	#Set HTTP Headers
	#Set Content Type(Return) as Text
	self.send_header("Content-type","text")
	self.end_headers()

	#Process the URL to get the GET Variables
	#Dictionary consisting of {variable_name: variable_value} pairs
	get_params = self.get_URL_params(self.path)

	#Process the request
	response = self.process_request(self.path.split("?")[0], get_params)

	self.wfile.write(response)
    def process_request(self, absolute_path, get_params):
        global CURSOR_X, CURSOR_Y
        fin = open("home.html","r")
        html_page = fin.read();
        operation = int(get_params['operation'][0])
        display = Xlib.display.Display()
        screen = display.screen()
        SMALL_MOVE = 20
        BIG_MOVE = 70
      
        root  = screen.root
        if operation == 1:
            CURSOR_X = CURSOR_X - SMALL_MOVE
        elif operation == 2:
            CURSOR_Y = CURSOR_Y + SMALL_MOVE
        elif operation == 3:
            CURSOR_X = CURSOR_X + SMALL_MOVE
        elif operation == 4:
            CURSOR_Y = CURSOR_Y - SMALL_MOVE
        elif operation == 7:
            CURSOR_X = CURSOR_X - BIG_MOVE
        elif operation == 8:
            CURSOR_Y = CURSOR_Y + BIG_MOVE
        elif operation == 9:
            CURSOR_X = CURSOR_X + BIG_MOVE
        elif operation == 10:
            CURSOR_Y = CURSOR_Y - BIG_MOVE
        root.warp_pointer(CURSOR_X,CURSOR_Y)
        if operation == 5:
            Xlib.ext.xtest.fake_input(display,Xlib.X.ButtonPress,1)
            Xlib.ext.xtest.fake_input(display,Xlib.X.ButtonRelease,1)
        elif operation == 6:
            Xlib.ext.xtest.fake_input(display,Xlib.X.ButtonPress,3)
            Xlib.ext.xtest.fake_input(display,Xlib.X.ButtonRelease,3)

        display.sync()
        print str(CURSOR_X)+ ","+str(CURSOR_Y)
            
        return html_page


    def get_URL_params(self, path):
        variables_section_of_url = path.split("?")[-1]
	dictionary_of_variables = urlparse.parse_qs(variables_section_of_url)
	return dictionary_of_variables






def main():
    server_class = BaseHTTPServer.HTTPServer
    global HOST_NAME, PORT_NUMBER
    global CURSOR_X, CURSOR_Y
    CURSOR_X = 200
    CURSOR_Y = 200
    try:
        httpd = server_class((HOST_NAME, PORT_NUMBER), MyHTTPHandler)
        httpd.serve_forever()
    except Exception as e:
        print e
if __name__=="__main__":
    main()
