from PySide6.QtWidgets import QApplication, QWidget, QPushButton,QMainWindow
from PySide6  import  QtCore
from PySide6.QtGui import *
from PySide6.QtCore  import  QFile,QIODevice
from PySide6.QtUiTools import QUiLoader
import sys


cssBtnEnabled = "background-color: #F3EF52;""color: #27292F;""border-radius: 15px;"
cssBtnDisabled = "color: #757575;" "background-color: #27292F;" "border-radius: 15px;" "border: 2px solid #9F9F9F;"
cssBtnExecute = "color: #000000;""background: #F3EF52;"#"border-radius: 15px;"

cssBtnlongEnabled = "color: #000000;""border-radius: 15px;""background-color: rgba(255, 255, 255, 0);""border: 2px solid #0DFF00;"
cssBtnlongDisabled = "color: #000000;""border-radius: 15px;""background-color: rgba(255, 255, 255, 0);""border: 2px solid #9F9F9F;"
cssBtnShortEnabled = "color: #000000;""border-radius: 15px;""background-color: rgba(255, 255, 255, 0);""border: 2px solid #FF0000;"
cssBtnShortDisabled = "color: #000000;""border-radius: 15px;""background-color: rgba(255, 255, 255, 0);""border: 2px solid #9F9F9F;"
cssEtEditRiskDisabled = "color: #9F9F9F;""border: 2px solid #9F9F9F"
cssEtEditRiskEnabled = "color: white;""border: 2px solid White"


class UserInterface(QMainWindow):

    __instance = None

    def __init__(self):
        super().__init__()

        ui_file_name = "ui_templates/options_rifle_UI_2.ui"
        ui_file = QFile(ui_file_name)

        print("Started UI")

        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)

        self.loader = QUiLoader()
        self.window = self.loader.load(ui_file)
        ui_file.close()
        self.window.setWindowTitle("Options Rifle v1")

        ## initialise Button and its funtions
        self.window.btn_aggresive.clicked.connect(self.clickedAggresive)
        self.window.btn_defensive.clicked.connect(self.clickedDefensive)
        self.window.btn_bounce.clicked.connect(self.clickedBounce)

        self.window.btn_long.clicked.connect(self.clickedLong)
        self.window.btn_short.clicked.connect(self.clickedShort)

        self.window.btn_editrisk.clicked.connect(self.clickedEditRisk)

        self.window.btn_execute.clicked.connect(self.clickedExecute)

        #inititalise Startup Parameters
        self.clickedAggresive()
        self.clickedLong()
        self.window.spinner_ticker.addItem("BANKNIFTY")
        ##self.window.spinner_ticker.addItem("NIFTY")

        self.window.et_risk.setText("2500")
        self.window.et_risk.setEnabled(False)
        self.window.btn_editrisk.setIcon(QIcon('icons/btn_edit_risk.png'))
        self.window.et_risk.setStyleSheet(cssEtEditRiskDisabled)
        
        self.window.btn_execute.setStyleSheet(cssBtnExecute)

    


    @staticmethod
    def get_instance():
        if UserInterface.__instance is None:
           UserInterface.__instance = UserInterface()
        return UserInterface.__instance

    def show(self):
        if not self.window:
            print(self.loader.errorString())
            sys.exit(-1)
        self.window.show()    

    def clickedAggresive(self):
        self.window.btn_aggresive.setStyleSheet(cssBtnEnabled)
        self.window.btn_defensive.setStyleSheet(cssBtnDisabled)
        self.window.btn_bounce.setStyleSheet(cssBtnDisabled )

        return

    def clickedDefensive(self) :

        self.window.btn_aggresive.setStyleSheet(cssBtnDisabled)
        self.window.btn_defensive.setStyleSheet(cssBtnEnabled)
        self.window.btn_bounce.setStyleSheet(cssBtnDisabled)
        return

    def clickedBounce(self):
        self.window.btn_aggresive.setStyleSheet(cssBtnDisabled)
        self.window.btn_defensive.setStyleSheet(cssBtnDisabled)
        self.window.btn_bounce.setStyleSheet(cssBtnEnabled)
        return           

    def clickedLong(self):
        self.window.btn_long.setStyleSheet(cssBtnlongEnabled)
        self.window.btn_short.setStyleSheet(cssBtnShortDisabled)
        self.window.btn_long.setIcon(QIcon('icons/btn_long_enabled.png'))
        self.window.btn_short.setIcon(QIcon('icons/btn_short_disabled.png'))

        return          
    def clickedShort(self):
        self.window.btn_long.setStyleSheet(cssBtnlongDisabled)
        self.window.btn_short.setStyleSheet(cssBtnShortEnabled)
        self.window.btn_long.setIcon(QIcon('icons/btn_long_disabled.png'))
        self.window.btn_short.setIcon(QIcon('icons/btn_short_enabled.png'))
        return 
    def clickedTrades(self):
        return     
    def clickedPnLChart(self):
        return 
    def clickedExecute(self):
        return     
    def clickedEditRisk(self):
        if self.window.et_risk.isEnabled() : 
             self.window.et_risk.setEnabled(False)
             self.window.btn_editrisk.setIcon(QIcon('icons/btn_edit_risk.png'))
             self.window.et_risk.setStyleSheet(cssEtEditRiskDisabled)
        else:
            self.window.et_risk.setEnabled(True)
            self.window.btn_editrisk.setIcon(QIcon('icons/btn_set_risk.png'))
            self.window.et_risk.setStyleSheet(cssEtEditRiskEnabled)

        return    

