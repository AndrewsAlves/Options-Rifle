import logging
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from kiteconnect import KiteConnect
import OptionsRifleMain
import threading
from threading import Event
import trace
from PySide6.QtCore import QTimer
from PySide6 import QtGui as gui
from PySide6 import QtCore as core
from PySide6.QtCore import QObject, QThread, Signal


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

            # Generate the access token using the request token
        data = kite.generate_session(request_token, api_secret=API_SECRET)

        # Extract the access token from the data dictionary
        access_token = data["access_token"]


        # Set the access token in the KiteConnect object
        kite.set_access_token(access_token)
        print("access token :" + access_token)
        auth_server_thread.finished.emit()
        server.shutdown()
        #OptionsRifleMain.startOptionsRifle()

    def do_POST(self) : 
        pass


server = HTTPServer(("localhost", 8000), RequestHandler)
event = Event()
class AuthServerThread(QObject):

    finished = Signal()

    def run(self):
        print("Server is started")
        server.serve_forever()

class AuthServerShutdownThread(threading.Thread) :
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        server.shutdown()

auth_server_thread = AuthServerThread()       
auth_server_shutdown_thread = AuthServerShutdownThread()

def openApp() : 
    OptionsRifleMain.startOptionsRifle()

def loginUser() : 
    print("User is not logged in")
    login_url = kite.login_url()
    webbrowser.open_new(login_url)

    thread = QThread()
    # Step 3: Create a worker object
    # Step 4: Move worker to the thread
    auth_server_thread.moveToThread(thread)
    # Step 5: Connect signals and slots
    thread.started.connect(auth_server_thread.run)
    auth_server_thread.finished.connect(thread.quit)
    auth_server_thread.finished.connect(auth_server_thread.deleteLater)
    thread.finished.connect(thread.deleteLater)
    # Step 6: Start the thread
    thread.start()

    thread.finished.connect(openOptionsRifle)
    #auth_server_thread.start()
    print("this is exxe")
    ##OptionsRifleMain.closeLoginWindow()
    ##OptionsRifleMain.startOptionsRifle()

def openOptionsRifle():
     OptionsRifleMain.closeLoginWindow()
     OptionsRifleMain.startOptionsRifle()
    
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
import threading
from threading import Event
import trace
from PySide6.QtCore import QTimer
from PySide6 import QtGui as gui
from PySide6 import QtCore as core
from PySide6.QtCore import QObject, QThread, Signal


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

            # Generate the access token using the request token
        data = kite.generate_session(request_token, api_secret=API_SECRET)

        # Extract the access token from the data dictionary
        access_token = data["access_token"]


        # Set the access token in the KiteConnect object
        kite.set_access_token(access_token)
        print("access token :" + access_token)
        server.shutdown()
        #OptionsRifleMain.startOptionsRifle()

    def do_POST(self) : 
        pass


server = HTTPServer(("localhost", 8000), RequestHandler)
event = Event()
class AuthServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        server.serve_forever()

    def kill(self):
        self.killed = True    

class AuthServerShutdownThread(threading.Thread) :
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        server.shutdown()

auth_server_thread = AuthServerThread()       
auth_server_shutdown_thread = AuthServerShutdownThread()

def openApp() : 
    OptionsRifleMain.startOptionsRifle()

def loginUser() : 
    print("User is not logged in")
    login_url = kite.login_url()
    webbrowser.open_new(login_url)
    auth_server_thread.start()
    print("this is exxe")
    ##OptionsRifleMain.closeLoginWindow()
    ##OptionsRifleMain.startOptionsRifle()
    
def isUserLoggedIn() : 
    if kite.access_token:
        print("User is logged in")
        return True 
    else : 
        return False"""