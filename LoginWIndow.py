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
from TradeWindow import TradeWindow
from KiteApi import KiteApi
from Utils.Utilities import WorkerThread
from Utils import Utilities
from Utils import StaticVariables as statics
import time 

#smart connect libs
from SmartApi import SmartConnect #or from SmartApi.smartConnect import SmartConnect
import pyotp


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
getInstrumentThread = WorkerThread(KiteApi.ins().getInstrumentsAndTrades)

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
        self.window.setWindowIcon(QIcon("icons/icon_options_rifle_small.png"))
        self.window.setWindowTitle("Login to a Zerodha")
        self.window.btn_login.clicked.connect(self.clickedLogintoZerodha)
        self.window.btn_login_angel.clicked.connect(self.clickedLogintoAngelOne)

        self.window.frame_login_zerodha_api.hide()

    def initialiseFrameZerodhaApi(self) : 
        self.window.frame_login_zerodha_api.show()
        self.window.btn_login_zerodha_api.clicked.connect(self.clickedLogin)

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
    
    def clickedLogintoZerodha(self) : 
        self.initialiseFrameZerodhaApi()

    def clickedLogintoAngelOne(self) : 
        self.clickedLoginAngel()
    
    ###----------------------------------------------------------###
    ### ZERODHA LOGIN 
    ###----------------------------------------------------------###

    def clickedLogin(self) : 
        #KiteApi.ins().initialiseKite(self.window.lineedit_apikey.text(), self.window.lineedit_api_secret.text())
        KiteApi.ins().initialiseKite(statics.API_KEY, statics.API_SECRET)
        self.loginUser()

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
        self.userInterface = TradeWindow.get_instance()
        self.userInterface.show()
        self.close()
        return 
    

    ###----------------------------------------------------------###
    ### ANGEL ONE LOGIN 
    ###----------------------------------------------------------###

    def clickedLoginAngel(self) : 
        smartApi = SmartConnect(statics.ANGEL_API_KEY)
        totp = pyotp.TOTP(statics.ANGEL_QR_CODE).now()
        #login API
        data = smartApi.generateSession(statics.ANGEL_CLIENT_ID, statics.ANGEL_PASSWORD, totp)
        print(data)
        authToken = data['data']['jwtToken']
        refreshToken= data['data']['refreshToken']

        #fetch the feedtoken
        feedToken = smartApi.getfeedToken()

        #fetch User Profile
        userProfile = smartApi.getProfile(refreshToken)





