from PySide6.QtWidgets import QApplication, QWidget, QPushButton,QMainWindow
from PySide6  import  QtCore
from PySide6.QtGui import *
from PySide6.QtCore  import  QFile,QIODevice
from PySide6.QtUiTools import QUiLoader
import sys
import ConnectKite


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

    def clickedLogintoZerodha(self) :   
        ConnectKite.loginUser()
        
