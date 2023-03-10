from PySide6.QtWidgets import QApplication, QWidget, QPushButton,QMainWindow
from PySide6  import  QtCore
from PySide6.QtGui import *
from PySide6.QtCore  import  QFile,QIODevice
from PySide6.QtUiTools import QUiLoader
import sys
import logging
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from kiteconnect import KiteConnect
import OptionsRifleMain
from PySide6.QtCore import QThread, Signal
from UserInterface import UserInterface

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
        print("Server is closed")

        auth_server_thread.finished.emit()
        server.shutdown()

    def do_POST(self) : 
        pass

class AuthServerThread(QThread):

    finished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def run(self):
        print("Server is started")
        server.serve_forever()

server = HTTPServer(("localhost", 8000), RequestHandler)
auth_server_thread = AuthServerThread()       

class LoginWindow(QMainWindow) : 

    __instance = None

    def __init__(self):
        super().__init__()

        ui_file_name = "ui_templates/options_rifle_login_window.ui"
        ui_file = QFile(ui_file_name)

        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)

        self.loader = QUiLoader()
        self.window = self.loader.load(ui_file)
        ui_file.close()
        self.window.setWindowTitle("Login to a Zerodha")
        self.window.btn_login.clicked.connect(self.clickedLogintoZerodha)

    @staticmethod
    def get_instance():
        if LoginWindow.__instance is None:
           LoginWindow.__instance = LoginWindow()
        return LoginWindow.__instance

    def show(self):
        if not self.window:
            print(self.loader.errorString())
            sys.exit(-1)
        self.window.show()    

    def close(self) :
        self.window.close()    
    
    def loginUser(self) : 
        print("User is not logged in")
        login_url = kite.login_url()
        webbrowser.open_new(login_url)
        auth_server_thread.finished.connect(self.openOptionsRifle)
        auth_server_thread.start()    

    def openOptionsRifle(self):
     self.close()
     self.userInterface = UserInterface.get_instance()
     self.userInterface.show()

    def clickedLogintoZerodha(self) : 
        self.loginUser()

