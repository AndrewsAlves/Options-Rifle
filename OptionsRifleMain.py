
import sys

from PySide6.QtWidgets import QApplication, QWidget, QPushButton
from PySide6.QtCore import QFile,QIODevice,Slot
from PySide6.QtUiTools import QUiLoader
from UserInterface import UserInterface
from TerminalConnection import ConnectKite

if __name__ == "__main__": 

    app = QApplication(sys.argv)

    if ConnectKite.loginUser() :  
        window = UserInterface()
        window.show()
        sys.exit(app.exec())



