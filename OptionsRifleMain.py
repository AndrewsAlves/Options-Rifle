
import sys
import threading
from PySide6.QtWidgets import QApplication, QWidget, QPushButton
from PySide6.QtCore import QFile,QIODevice,Slot,QThread
from PySide6.QtUiTools import QUiLoader
from UserInterface import UserInterface
import ConnectKite
from LoginWIndow import LoginWindow


class OptionsRifleMain() : 
    __instance = None

    def __init__(self):
        if QApplication.instance():
            self.app = QApplication.instance()
        else:
            self.app = QApplication(sys.argv)
        self.loginwindow = LoginWindow.get_instance()
        self.userInterface = UserInterface.get_instance()
        return
    
    def startOptionsRifle(self) : 
        print("Starting Options Rifle")
        self.userInterface.show()
        #QApplication.processEvents()

    def startLoginWidow(self) :
        self.loginwindow.show()

    def closeLoginWindow(self) :
        self.loginwindow.close()   

    @staticmethod
    def get_instance():
        if OptionsRifleMain.__instance is None:
            OptionsRifleMain.__instance = OptionsRifleMain()
            return OptionsRifleMain.__instance


if __name__ == "__main__": 

    print ("Starting Application")
    optionsRifle = OptionsRifleMain.get_instance()

    if ConnectKite.isUserLoggedIn() :  
        optionsRifle.startOptionsRifle()
    else :
        optionsRifle.startLoginWidow()

    sys.exit(optionsRifle.app.exec())
    


        





