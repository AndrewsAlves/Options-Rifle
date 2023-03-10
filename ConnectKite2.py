import logging
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from kiteconnect import KiteConnect
import OptionsRifleMain
import threading

logging.basicConfig(level=logging.DEBUG)

API_KEY= "yzczdzxsmw9w9tq9"
API_SECRET = "2k7oo9x1w0xl5g9789wl8j6v4u03lq0x"
kite = KiteConnect(api_key=API_KEY)

# Set up a web server to listen for incoming requests
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the query parameters from the request URL
        query = urlparse(self.path).query
        params = parse_qs(query)

        # Extract the request token from the query parameters
        request_token = params["request_token"][0]

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body><h1>Authorization complete : You can close this window</h1></body></html>")

        print(request_token)
        startSession(request_token)

class AuthServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.server = HTTPServer(("localhost", 8000), RequestHandler)

    def run(self):
        self.server.serve_forever()

    def shutdownServer(self) :
        self.server.shutdown()

auth_server_thread = AuthServerThread()        

def startSession(request_token):
    # Generate the access token using the request token
    data = kite.generate_session(request_token, api_secret=API_SECRET)

    # Extract the access token from the data dictionary
    access_token = data["access_token"]

    # Set the access token in the KiteConnect object
    ##kite.set_access_token(access_token)

    OptionsRifleMain.closeLoginWindow()
    auth_server_thread.shutdownServer()
    OptionsRifleMain.startOptionsRifle()

def loginUser() : 
    print("User is not logged in")
    login_url = kite.login_url()
    webbrowser.open_new(login_url)
    auth_server_thread.start()

def isUserLoggedIn() : 
    if kite.access_token:
        print("User is logged in")
        return True 
    else : 
        return False


"""import logging
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from kiteconnect import KiteConnect
import OptionsRifleMain

logging.basicConfig(level=logging.DEBUG)

API_KEY= "yzczdzxsmw9w9tq9"
API_SECRET = "2k7oo9x1w0xl5g9789wl8j6v4u03lq0x"
kite = KiteConnect(api_key=API_KEY)

# Set up a web server to listen for incoming requests
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the query parameters from the request URL
        query = urlparse(self.path).query
        params = parse_qs(query)

        # Extract the request token from the query parameters
        request_token = params["request_token"][0]

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body><h1>Authorization complete : You can close this window</h1></body></html>")

        print(request_token)
        startSession(request_token)
        
server = HTTPServer(("localhost", 8000), RequestHandler)

def startSession(request_token):
    # Generate the access token using the request token
    data = kite.generate_session(request_token, api_secret=API_SECRET)

    # Extract the access token from the data dictionary
    access_token = data["access_token"]

    # Set the access token in the KiteConnect object
    kite.set_access_token(access_token)

    OptionsRifleMain.closeLoginWindow()
    server.shutdown()
    print("this code is exe")
    OptionsRifleMain.startOptionsRifle()


def loginUser() : 
        print("User is not logged in")
        login_url = kite.login_url()
        webbrowser.open_new(login_url)
        server.serve_forever()

def isUserLoggedIn() : 
    if kite.access_token:
        print("User is logged in")
        return True 
    else : 
        return False"""