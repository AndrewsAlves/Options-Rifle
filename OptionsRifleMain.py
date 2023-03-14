
import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton
from PySide6.QtCore import QFile,QIODevice,Slot,QThread
from PySide6.QtUiTools import QUiLoader
from TradeWindow import TradeWindow
from LoginWIndow import LoginWindow


class OptionsRifleMain() : 
    __instance = None

    def __init__(self):
        if QApplication.instance():
            self.app = QApplication.instance()
        else:
            self.app = QApplication(sys.argv)
        return
    
    @staticmethod
    def get_instance():
        if OptionsRifleMain.__instance is None:
            OptionsRifleMain.__instance = OptionsRifleMain()
            return OptionsRifleMain.__instance

if __name__ == "__main__": 

    print ("Starting Application")
    optionsRifle = OptionsRifleMain.get_instance()

    LoginWindow.get_instance().show()

    sys.exit(optionsRifle.app.exec())
    



        





