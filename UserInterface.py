from PySide6.QtWidgets import QApplication, QWidget, QPushButton,QMainWindow,QFrame,QLabel
from PySide6  import  QtCore
from PySide6.QtGui import *
from PySide6.QtCore  import  QFile,QIODevice
from PySide6.QtUiTools import QUiLoader
import sys
import logging
from KiteApi import KiteApi


cssBtnEnabled = "background-color: #F3EF52;""color: #27292F;""border-radius: 15px;"
cssBtnDisabled = "color: #757575;" "background-color: #27292F;" "border-radius: 15px;" "border: 2px solid #9F9F9F;"
cssBtnExecute = "color: #000000;""background: #F3EF52;"#"border-radius: 15px;"

cssBtnlongEnabled = "color: #000000;""border-radius: 15px;""background-color: rgba(255, 255, 255, 0);""border: 2px solid #0DFF00;"
cssBtnlongDisabled = "color: #000000;""border-radius: 15px;""background-color: rgba(255, 255, 255, 0);""border: 2px solid #9F9F9F;"
cssBtnShortEnabled = "color: #000000;""border-radius: 15px;""background-color: rgba(255, 255, 255, 0);""border: 2px solid #FF0000;"
cssBtnShortDisabled = "color: #000000;""border-radius: 15px;""background-color: rgba(255, 255, 255, 0);""border: 2px solid #9F9F9F;"
cssEtEditRiskDisabled = "color: #9F9F9F;""border: 2px solid #9F9F9F"
cssEtEditRiskEnabled = "color: white;""border: 2px solid White"

logging.basicConfig(level=logging.DEBUG)


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
        self.window.setWindowTitle("Options Rifle")
        self.window.setWindowIcon(QIcon("icons/icon_options_rifle_small.png"))

        #create Overlay frame to stop accessing Button if some process or Error in the Process
        self.overlay_frame = QFrame(self.window)
        self.overlay_frame.setFixedSize(self.window.size())
        self.overlay_frame.setStyleSheet('background-color: rgba(0, 0, 0, 100);')
        self.overlay_frame.hide()

        ## initialise Button and its funtions
        self.window.btn_aggresive.clicked.connect(self.clickedAggresive)
        self.window.btn_defensive.clicked.connect(self.clickedDefensive)
        self.window.btn_bounce.clicked.connect(self.clickedBounce)

        self.window.btn_long.clicked.connect(self.clickedLong)
        self.window.btn_short.clicked.connect(self.clickedShort)

        #this button is a transparent button
        self.window.btn_trans_label_Fut.clicked.connect(self.setFuturesSLInSpin)

        self.window.btn_editrisk.clicked.connect(self.clickedEditRisk)

        self.window.btn_execute.clicked.connect(self.clickedExecute)


        #inititalise Startup Parameters
        self.clickedAggresive()
        self.clickedLong()
        self.window.spinner_ticker.addItem("BANKNIFTY")
        ##self.window.spinner_ticker.addItem("NIFTY")

        self.enableOptionsRifleUi()
        self.updateStatusBar()

        self.window.et_risk.setText("2500")
        self.window.et_risk.setEnabled(False)
        self.window.btn_editrisk.setIcon(QIcon('icons/btn_edit_risk.png'))
        self.window.et_risk.setStyleSheet(cssEtEditRiskDisabled)
        
        self.window.btn_execute.setStyleSheet(cssBtnExecute)

        KiteApi.ins().connetInitialTickerSockets(self.onTicks,
                                                         self.onConnect,
                                                         self.onClose,
                                                         self.onError,
                                                         self.onMessage,
                                                         self.onReConnect,
                                                         self.onNoReConnect,
                                                         self.onOrderUpdate)


    def disableOptionsRifleUI(self) :
        self.window.MainWinodw2.setEnabled(False)
        self.overlay_frame.show()

    def enableOptionsRifleUi(self) : 
        self.window.MainWinodw2.setEnabled(True)
        self.overlay_frame.hide()

    def updateStatusBar(self, message = 'All Set :)') : 
        self.window.statusbar.showMessage(message)

    @staticmethod
    def get_instance():
        if UserInterface.__instance is None:
           UserInterface.__instance = UserInterface()
        return UserInterface.__instance

    def updateQuote(self) : 
        return

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
    
    def setFuturesSLInSpin(self) :
        print("clicked futures spot")
        self.window.spin_stoploss.setValue(KiteApi.ins().bnfLtp)
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
    
    """Callbacks
    ---------
    In below examples `ws` is the currently initialised WebSocket object.
    - `on_ticks(ws, ticks)` -  Triggered when ticks are recevied.
        - `ticks` - List of `tick` object. Check below for sample structure.
    - `on_close(ws, code, reason)` -  Triggered when connection is closed.
        - `code` - WebSocket standard close event code (https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent)
        - `reason` - DOMString indicating the reason the server closed the connection
    - `on_error(ws, code, reason)` -  Triggered when connection is closed with an error.
        - `code` - WebSocket standard close event code (https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent)
        - `reason` - DOMString indicating the reason the server closed the connection
    - `on_connect` -  Triggered when connection is established successfully.
        - `response` - Response received from server on successful connection.
    - `on_message(ws, payload, is_binary)` -  Triggered when message is received from the server.
        - `payload` - Raw response from the server (either text or binary).
        - `is_binary` - Bool to check if response is binary type.
    - `on_reconnect(ws, attempts_count)` -  Triggered when auto reconnection is attempted.
        - `attempts_count` - Current reconnect attempt number.
    - `on_noreconnect(ws)` -  Triggered when number of auto reconnection attempts exceeds `reconnect_tries`.
    - `on_order_update(ws, data)` -  Triggered when there is an order update for the connected user."""

    #######   KITE CONNECT       ############
    ####### ___________________ ############ 

    def onTicks(self, ws, ticks) :
        # Callback to receive ticks.
        logging.debug("Ticks: {}".format(ticks))
        for tick in ticks :
            
            KiteApi.ins().tokensLtp[tick["instrument_token"]] = tick['last_price']

            if tick['instrument_token'] == KiteApi.ins().getbnfSpotToken() :
                KiteApi.ins().bnfLtp = tick['last_price']
                self.window.label_spot.setText(str(KiteApi.ins().bnfLtp))
            if tick['instrument_token'] == KiteApi.ins().getUpcomingbnfFutureToken() :
                KiteApi.ins().bnfSpotLtp = tick['last_price']
                self.window.label_futures.setText(str(KiteApi.ins().bnfSpotLtp))
            self.window.label_future_diff.setText(str(KiteApi.ins().bnfLtp - KiteApi.ins().bnfSpotLtp))        
        return
    
    def onConnect(self, ws, response) :
        niftyBankTk = KiteApi.ins().getbnfSpotToken()
        bnfTk = KiteApi.ins().getUpcomingbnfFutureToken()
        tokenList = KiteApi.ins().getAllRequiredInstrumentListTokens()
        ws.subscribe(tokenList)
        ws.set_mode(ws.MODE_LTP ,tokenList)

        return
    def onClose(self, ws, code, reason) :
        ws.stop()
        return
    def onError(self, ws, code, reason) :
        self.updateStatusBar("Web socket Error...")
        print("server error : " + reason)
        return
    def onMessage(self,ws, payload, isBinary) :
        ##if not isBinary :
         ##   print("message from kite server : " + payload)
        return
    def onReConnect(self, attemptCount) :
        print("server reconnect attemps : " + attemptCount)
        return
    def onNoReConnect(self, ws) :
        return
    def onOrderUpdate(self, ws, data) :
        return
    

