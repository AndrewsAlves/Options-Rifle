
import sys
import threading


from PySide6.QtWidgets import QApplication, QWidget, QPushButton
from PySide6.QtCore import QFile,QIODevice,Slot,QThread
from PySide6.QtUiTools import QUiLoader
from UserInterface import UserInterface
import ConnectKite
from LoginWIndow import LoginWindow


if QApplication.instance():
    app = QApplication.instance()
else:
    app = QApplication(sys.argv)
    
loginwindow = LoginWindow.get_instance()
userInterface = UserInterface.get_instance()

class OptionsRifleThread(QThread):
    def run(self):
        userInterface.show()
        QApplication.processEvents()
        
qrun = OptionsRifleThread()

def startOptionsRifle() : 
    print("Starting Options Rifle")
    userInterface.show()
    QApplication.processEvents()
    #qrun.start()

def startLoginWidow() :
    loginwindow.show()

def closeLoginWindow() :
    loginwindow.close()   


if __name__ == "__main__": 

    print ("Starting Application")
    if ConnectKite.isUserLoggedIn() :  
        startOptionsRifle()
    else :
        startLoginWidow()

    sys.exit(app.exec())
    


        





