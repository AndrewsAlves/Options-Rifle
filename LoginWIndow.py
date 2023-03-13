from PySide6.QtWidgets import QApplication, QWidget, QPushButton,QMainWindow
from PySide6  import  QtCore
from PySide6.QtGui import *
from PySide6.QtCore  import  QFile,QIODevice
from PySide6.QtUiTools import QUiLoader
import sys
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from PySide6.QtCore import QThread, Signal
from UserInterface import UserInterface
from KiteApi import KiteApi
from Utils.Utilities import WorkerThread
import time 


logging.basicConfig(level=logging.DEBUG)

# Set up a web server to listen for incoming requests
class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        query = urlparse(self.path).query
        params = parse_qs(query)
        request_token = params["request_token"][0]

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body><h1>Authorization complete : You can close this window</h1></body></html>")

        KiteApi.ins().generateSession(request_token)
        auth_server_thread.finished.emit()

        print("Server is closed")
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
getInstrumentThread = WorkerThread(KiteApi.ins().getInstruments)

                ### LOGIN WINDOW ###
###--------------------------------------------------------###

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
        KiteApi.ins().openLoginUrl()
        auth_server_thread.finished.connect(self.loginFlowFinished)
        auth_server_thread.start()    
    
    def loginFlowFinished(self):
     print("Login Flow Finished")
     ## Start getting everyday Instruments data and store it in local database
     self.window.label_process.setText("Getting Instrument List for the Day...")   
     getInstrumentThread.finished.connect(self.handleGetInstrumentResult)
     getInstrumentThread.start()
    
    def handleGetInstrumentResult(self, result):
        print("Starting Options Rifle...")
        self.userInterface = UserInterface.get_instance()
        self.userInterface.show()
        self.close()
        return 

    def clickedLogintoZerodha(self) : 
        self.loginUser()

