from PySide6.QtWidgets import QApplication, QWidget, QPushButton,QMainWindow,QFrame,QLabel
from PySide6  import  QtCore
from PySide6.QtGui import *
from PySide6.QtCore  import  QFile,QIODevice
from PySide6.QtUiTools import QUiLoader
import sys
import logging
from KiteApi import KiteApi
from Utils.Utilities import WorkerThread,WorkerLoopedThread,TickLooperThread
import time
import threading 
from Utils import Utilities



cssBtnEnabled = "background-color: #F3EF52;""color: #27292F;""border-radius: 15px;"
cssBtnDisabled = "color: #757575;" "background-color: #27292F;" "border-radius: 15px;" "border: 2px solid #9F9F9F;"
cssBtnExecute = "color: #000000;""background: #F3EF52;"#"border-radius: 15px;"

cssBtnlongEnabled = "color: #000000;""border-radius: 15px;""background-color: rgba(255, 255, 255, 0);""border: 2px solid #0DFF00;"
cssBtnlongDisabled = "color: #000000;""border-radius: 15px;""background-color: rgba(255, 255, 255, 0);""border: 2px solid #9F9F9F;"
cssBtnShortEnabled = "color: #000000;""border-radius: 15px;""background-color: rgba(255, 255, 255, 0);""border: 2px solid #FF0000;"
cssBtnShortDisabled = "color: #000000;""border-radius: 15px;""background-color: rgba(255, 255, 255, 0);""border: 2px solid #9F9F9F;"
cssEtEditRiskDisabled = "color: #9F9F9F;""border: 2px solid #9F9F9F"
cssEtEditRiskEnabled = "color: white;""border: 2px solid White"

cssMTMRed = "color: red;"
cssMTMGreen = "color: green;"


logging.basicConfig(level=logging.DEBUG)

AGGRESIVE = "aggresive"
DEFENSIVE = "defensive"
BOUNCE = "bounce"

LONG = "long"
SHORT = "short"

ORDER_PLACED = "orderplaced"
ORDER_ERROR = "ordererror"
ORDER_ERROR_0_POSITION_SIZING = "ordererror_0_position_sizing"


EXECUTED = 1
PENDING = -1
CANCELLED = -2

class TradeWindow(QMainWindow):

    __instance = None

    def __init__(self):
        super().__init__()

        self.tickraceLock = threading.Lock()
        self.greeksThread = WorkerLoopedThread(KiteApi.ins().deriveOptionsGreeks, loopsEverySec = 1, 
                                               startedMessage = "Started Greeks Calucations", 
                                               stoppedMessage = "Stopped Greeks Calculations")
        self.ticksThread = TickLooperThread(self.tickLooperThreadFunc, loopsEverySec = 0.25,
                                            startedMessage = "Started Ticks process", 
                                               stoppedMessage = "Stopped Ticks process")
        
        
        self.executionThread = WorkerThread(self.executionThreadFunc)
        self.statusBartimer = None
        self.orderStatusTimer = None

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


        ## SET BUTTONGS AND ITS FUNCTIONS FOR TRADE FRAME 
        self.window.btn_exit_trade.clicked.connect(self.clickedExitTrade)
        self.window.btn_decrease_sl.clicked.connect(self.clickeddedcreaseSL)
        self.window.btn_increase_sl.clicked.connect(self.clickedIncreaseSL)
        self.window.btn_edit_sl.clicked.connect(self.clickedEditSL)
        self.window.btn_increase_sl.setIcon(QIcon('icons/btn_plus.png'))
        self.window.btn_decrease_sl.setIcon(QIcon('icons/btn_minus.png'))
        self.window.btn_edit_sl.setIcon(QIcon('icons/btn_edit_sl.png'))
        self.window.btn_exit_trade.setIcon(QIcon('icons/btn_exit.png'))


        self.window.frame_trade.hide()
        self.window.label_no_position.show()


        # Set the validator to accept INT point numbers only
        self.riskValidator = QIntValidator(1,999999) 
        self.slValidator = QIntValidator(0,999999)
        self.window.et_risk.setValidator(self.riskValidator)
        self.window.spin_sl.setMinimum(0)

        #inititalise Startup Parameters
        self.clickedAggresive()
        self.clickedLong()
        self.window.spinner_ticker.addItem("BANKNIFTY")
        ##self.window.spinner_ticker.addItem("NIFTY")

        self.enableOptionsRifleUi()
        self.updateStatusBar()

        self.riskPerTrade = 2500
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
        
        #self.greeksThread.start()
        self.ticksThread.start()


    @staticmethod
    def get_instance():
        if TradeWindow.__instance is None:
           TradeWindow.__instance = TradeWindow()
        return TradeWindow.__instance

    def updateUi(self) : 
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
        self.stg = AGGRESIVE
        return

    def clickedDefensive(self) :
        self.window.btn_aggresive.setStyleSheet(cssBtnDisabled)
        self.window.btn_defensive.setStyleSheet(cssBtnEnabled)
        self.window.btn_bounce.setStyleSheet(cssBtnDisabled)
        self.stg = DEFENSIVE

        return

    def clickedBounce(self):
        self.window.btn_aggresive.setStyleSheet(cssBtnDisabled)
        self.window.btn_defensive.setStyleSheet(cssBtnDisabled)
        self.window.btn_bounce.setStyleSheet(cssBtnEnabled)
        self.stg = BOUNCE
        return           

    def clickedLong(self):

        self.tradeType = LONG
        self.updateSpotSLMinMax(KiteApi.ins().bnfLtp)
        self.window.btn_long.setStyleSheet(cssBtnlongEnabled)
        self.window.btn_short.setStyleSheet(cssBtnShortDisabled)
        self.window.btn_long.setIcon(QIcon('icons/btn_long_enabled.png'))
        self.window.btn_short.setIcon(QIcon('icons/btn_short_disabled.png'))

        return          
    def clickedShort(self):

        self.tradeType = SHORT
        self.updateSpotSLMinMax(KiteApi.ins().bnfLtp)
        self.window.btn_long.setStyleSheet(cssBtnlongDisabled)
        self.window.btn_short.setStyleSheet(cssBtnShortEnabled)
        self.window.btn_long.setIcon(QIcon('icons/btn_long_disabled.png'))
        self.window.btn_short.setIcon(QIcon('icons/btn_short_enabled.png'))
        return 
    
    def setFuturesSLInSpin(self) :
        print("clicked spin stop")
        self.window.spin_stoploss.setValue(KiteApi.ins().bnfLtp)
        return
    
    def clickedTrades(self):
        return     
    def clickedPnLChart(self):
        return 
    def clickedExecute(self):
        self.window.btn_execute.setEnabled(False)
        self.executionThread.start()
        return     
    
    def executionThreadFunc(self) :
        slPrice = self.window.spin_stoploss.value()
        
        status = KiteApi.ins().executeTrade(self.tradeType, slPrice, self.riskPerTrade,self.stg)
        if status == ORDER_PLACED :
            self.initTradePositionUI()
            self.updateOrderStatus("Pending...")
        elif status == ORDER_ERROR :
            self.updateStatusBar("Order Placing Error", delayReset= True)
        elif status == ORDER_ERROR_0_POSITION_SIZING :
            self.updateStatusBar("0 Qty possible", delayReset= True)

        self.window.btn_execute.setEnabled(True)


    def clickedEditRisk(self):
        if self.window.et_risk.isEnabled() : 
             ## set Risk
             self.riskPerTrade = int(self.window.et_risk.text())
             self.window.et_risk.setEnabled(False)
             self.window.btn_editrisk.setIcon(QIcon('icons/btn_edit_risk.png'))
             self.window.et_risk.setStyleSheet(cssEtEditRiskDisabled)
        else:
            ## edit risk
            self.window.et_risk.setEnabled(True)
            self.window.btn_editrisk.setIcon(QIcon('icons/btn_set_risk.png'))
            self.window.et_risk.setStyleSheet(cssEtEditRiskEnabled)

        return    
    
    def disableOptionsRifleUI(self) :
        self.window.MainWinodw2.setEnabled(False)
        self.overlay_frame.show()

    def enableOptionsRifleUi(self) : 
        self.window.MainWinodw2.setEnabled(True)
        self.overlay_frame.hide()

    def updateStatusBar(self, message = " ", delayReset = False) : 
        self.window.statusbar.showMessage(message)
        if delayReset : 
            if self.statusBartimer is not None :
                self.statusBartimer.cancel()
            self.statusBartimer = threading.Timer(2.0, self.resetStatusBarText)
            self.statusBartimer.start()
    
    def resetStatusBarText(self) : 
        self.updateStatusBar(" ")

    def updateSpotSLMinMax(self,maxPrice) :
        if maxPrice <= 0 : return
        if self.tradeType == LONG :
            self.window.spin_stoploss.setMaximum(maxPrice)
            self.window.spin_stoploss.setMinimum(0)
        else :
            self.window.spin_stoploss.setMaximum(9999999)
            self.window.spin_stoploss.setMinimum(maxPrice)


    """
    #################################################################################################
    #################################################################################################
    #################################################################################################
    #################################################################################################
    """



    def initTradePositionUI(self) :

        trade = KiteApi.ins().currentTradePosition
        if trade.tradeType == LONG :
            self.window.icon_trade_type.setIcon('icons/icon_arrow_long.png')    
        else :
            self.window.icon_trade_type.setIcon('icons/icon_arrow_short.png')    

        if trade.strategy == AGGRESIVE :
            self.window.label_strategy.setText('AT')
        elif trade.strategy == DEFENSIVE :
            self.window.label_strategy.setText('DT')
        else:
            self.window.label_strategy.setText('BT')

        self.window.label_instrument.setText(trade.tickerSymbol)
        self.window.label_trade_qty.setText(trade.qty)
        self.window.label_avg_price.setText(trade.entryPrice)
        self.window.label_trade_ltp.setText(trade.ltp)

        self.window.spin_sl.setValue(trade.stoplossPrice)
        self.updateSLMaxPrice(trade.ltp)

        self.updateLabelRiskAmount(trade.riskAmount)
        self.updateLabelUnrealisedRewardAmount(trade.unRealisedProfit)

        self.window.label_no_position.hide()
        self.window.frame_trade.show()

    def clickedIncreaseSL(self) :
        return
    
    def clickeddedcreaseSL(self) :
        return
    
    def clickedEditSL(self) :

        if self.window.spin_sl.isEnabled() : 
             ## set Risk
             self.window.spin_sl.setEnabled(False)
             self.window.btn_edit_sl.setIcon(QIcon('icons/btn_edit_sl.png'))
             self.window.spin_sl.setStyleSheet(cssEtEditRiskDisabled)
             KiteApi.ins().currentTradePosition.setStoploss(int(self.window.spin_sl.text()))

        else:
            ## edit risk
            self.window.spin_sl.setEnabled(True)
            self.window.btn_edit_sl.setIcon(QIcon('icons/btn_set_sl.png'))
            self.window.spin_sl.setStyleSheet(cssEtEditRiskEnabled)

        return    
    
    def updateSLMaxPrice(self, optiosLtp) :
        self.window.spin_sl.setMaximum(optiosLtp)
        self.window.spin_sl.setMinimum(0)
        return
    
    def updateLabelRiskAmount(self, riskAmount) :
        if riskAmount < 0 :
            riskStr = "+" + str(abs(riskAmount))
        else :
           riskStr = str(riskAmount)

        if riskAmount < 0 :  self.window.label_profit.setStyleSheet(cssMTMGreen) 
        else : self.window.label_profit.setStyleSheet(cssMTMRed)
        
        self.window.label_risk.setText(riskStr)
        return
    
    def updateLabelUnrealisedRewardAmount(self, rewardAmount) :
        if rewardAmount < 0 :
            rewardStr = str(rewardAmount)
        else :
            rewardStr = "+" + str(rewardAmount)

        if rewardAmount < 0 :  self.window.label_profit.setStyleSheet(cssMTMRed) 
        else : self.window.label_profit.setStyleSheet(cssMTMGreen)
        
        self.window.label_profit.setText(rewardStr)
        return
    
    def updateMtMAmount(self, MTM) :
        if MTM < 0 :
            rewardStr = str(MTM)
        else :
            rewardStr = "+" + str(MTM)
        
        if MTM < 0 :  self.window.label_MTM.setStyleSheet(cssMTMRed) 
        else : self.window.label_MTM.setStyleSheet(cssMTMGreen)

        self.window.label_MTM.setText(rewardStr)

    
    def clickedExitTrade(self) :
        status = KiteApi.ins().exitCurrentPosition()
        if status == ORDER_PLACED :
            self.updateOrderStatus("Exiting...")
        elif status == ORDER_ERROR :
            self.updateStatusBar("Order Exiting Error", delayReset= True)
        return
    
    def updateOrderStatus(self,str, delayedHide = False) : 
        self.window.label_order_status.show()
        self.window.label_order_status.setText(str)
        if delayedHide : 
            if self.orderStatusTimer is not None :
                self.orderStatusTimer.cancel()
            self.orderStatusTimer = threading.Timer(2.0, self.hideOrderstatus)
            self.orderStatusTimer.start()

    def hideOrderstatus(self) : 
        self.window.label_order_status.hide()

    def exitOrderExecuted(self) :
        self.updateOrderStatus("Exited")
        self.window.label_order_status.hide()
        KiteApi.ins().addLastTradeToTradesList()
        KiteApi.ins().currentTradePosition = None
        self.window.frame_trade.hide()
        self.window.label_no_position.show()
    
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

    def connectNewWebsocket(self) :
        KiteApi.ins().connetInitialTickerSockets(self.onTicks,
                                                         self.onConnect,
                                                         self.onClose,
                                                         self.onError,
                                                         self.onMessage,
                                                         self.onReConnect,
                                                         self.onNoReConnect,
                                                         self.onOrderUpdate)
        

    def onTicks(self, ws, ticks) :
        # Callback to receive ticks.
        #logging.debug("Ticks: {}".format(ticks))
        print("tick recived")
        self.ticksThread.setTickReceived(ticks)
        return
    
    def tickLooperThreadFunc(self, ticks) :
        self.tickraceLock.acquire()
        start_time = time.time()
        for tick in ticks :
            if tick['instrument_token'] == KiteApi.ins().getbnfSpotToken() :
                KiteApi.ins().bnfSpotLtp = tick['last_price']
                self.window.label_spot.setText(str(KiteApi.ins().bnfSpotLtp))
            if tick['instrument_token'] == KiteApi.ins().getUpcomingbnfFutureToken() :
                KiteApi.ins().bnfLtp = tick['last_price']
                self.window.label_futures.setText(str(KiteApi.ins().bnfLtp))
            if KiteApi.ins().currentTradePosition is not None :
                trade = KiteApi.ins().currentTradePosition
                if tick['instrument_token'] == trade.tickerToken :
                    trade.updateLtp(tick['last_price'])

        preDiff = round(KiteApi.ins().bnfLtp - KiteApi.ins().bnfSpotLtp, 1)
        self.window.label_future_diff.setText(str(preDiff))        


        KiteApi.ins().setLTPforRequiredTokens(ticks)

        if KiteApi.ins().currentTradePosition is not None :
            trade = KiteApi.ins().currentTradePosition
            unRealisedMtm = KiteApi.ins().finalPnL + trade.unRealisedProfit
            self.updateMtMAmount(unRealisedMtm)
            self.updateLabelUnrealisedRewardAmount(trade.unRealisedProfit)

            if trade.tradeEntryStatus == EXECUTED :
                if KiteApi.ins().tokensLtp[trade.tickerToken] <= trade.stoplossPrice :
                    self.clickedExitTrade()
                
                    print('Alert : Position SL hit, Exiting the trade')




        end_time = time.time()
        time_taken = end_time - start_time
        #print(f"Time taken: {time_taken} seconds")
        self.tickraceLock.release()

    def onConnect(self, ws, response) :
        tokenList = KiteApi.ins().getAllRequiredInstrumentListTokens()
        ws.subscribe(tokenList)
        ws.set_mode(ws.MODE_LTP ,tokenList)

        return
    def onClose(self, ws, code, reason) :
        ws.stop()
        return
    def onError(self, ws, code, reason) :
        self.updateStatusBar("Web socket closed due to an error...")
        print("server error : " + reason)
        return
    def onMessage(self,ws, payload, isBinary) :
        ##if not isBinary :
         ##   print("message from kite server : " + payload)
        return
    def onReConnect(self, attemptCount) :
        if Utilities.checkInternetConnection() :
            self.updateStatusBar("Socket issue Reconnecting...   " + str(attemptCount))
        else :
            self.updateStatusBar("Internet issue Reconnecting...   " + str(attemptCount))

        print("server reconnect attemps : " + attemptCount)
        return
    def onNoReConnect(self, ws) :
        KiteApi.ins().ticker.close()
        if Utilities.checkInternetConnection() :
            self.updateStatusBar("Socket issue closed connection !  ")
        else :
            self.updateStatusBar("Internet issue closed connection !  ")
        return
    def onOrderUpdate(self, ws, data) :

        logging.debug("Order Update: {}".format(data))
        return
    

   



