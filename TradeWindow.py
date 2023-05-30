from PySide6.QtWidgets import QApplication, QWidget, QPushButton,QMainWindow,QFrame,QLabel
from PySide6  import  QtCore
from PySide6.QtGui import *
from PySide6.QtCore  import  QFile,QIODevice,QTimer,QDateTime
from PySide6.QtUiTools import QUiLoader
import sys
import logging
from KiteApi import KiteApi
from Utils.Utilities import WorkerThread,WorkerLoopedThread,TickLooperThread
import Utils.StaticVariables as statics
import time
import threading 
from Utils import Utilities

cssBtnEnabled = "background-color: #F3EF52;""color: #27292F;""border-radius: 15px;"
cssBtnDisabled = "color: #757575;" "background-color: #27292F;" "border-radius: 15px;" "border: 2px solid #9F9F9F;"
cssBtnExecute = "color: #000000;""background: #F3EF52;""border-radius: 15px;"
cssBtnExecuting = "color: #000000;""background: #A4A13A;""border-radius: 15px;"
cssBtnExit = "color: white;""background: #F53535;""border-radius: 15px;"
cssBtnExiting = "color: white;""background: #D82929;""border-radius: 15px;"

cssBtnlongEnabled = "color: #000000;""border-radius: 15px;""background-color: rgba(255, 255, 255, 0);""border: 2px solid #0DFF00;"
cssBtnlongDisabled = "color: #000000;""border-radius: 15px;""background-color: rgba(255, 255, 255, 0);""border: 2px solid #9F9F9F;"
cssBtnShortEnabled = "color: #000000;""border-radius: 15px;""background-color: rgba(255, 255, 255, 0);""border: 2px solid #FF0000;"
cssBtnShortDisabled = "color: #000000;""border-radius: 15px;""background-color: rgba(255, 255, 255, 0);""border: 2px solid #9F9F9F;"
cssEtEditRiskDisabled = """QLineEdit {
        background-color: #0000000;
        border: 1px solid #9F9F9F;
		color:white;
		border-radius:5px
    }"""
cssEtEditRiskEnabled = """QLineEdit {
        background-color: #0000000;
        border: 1px solid white;
		color:white;
		border-radius:5px
    }"""

cssEtEditSlDisabled = """QLineEdit {
        background-color: #0000000;
        border: 1px solid #00000000;
		color:#B2B2B2;
        border-radius:5px
    }"""

cssEtEditSlEnabled = """QLineEdit {
        background-color: #0000000;
        border: 1px solid #00000000;
		color:white;
        border-radius:5px
    }"""

cssMTMRed = "color: #F53535;"
cssMTMGreen = "color: #4BF941;"
cssMTMWhite = "color: #C5C5C5;"


logging.basicConfig(level=logging.DEBUG)

AGGRESIVE = "aggresive"
DEFENSIVE = "defensive"
BOUNCE = "bounce"

LONG = "long"
SHORT = "short"

ORDER_PLACED = "orderplaced"
ORDER_ERROR = "ordererror"
ORDER_ERROR_0_POSITION_SIZING = "ordererror_0_position_sizing"
ORDER_ERROR_READ_TIMEOUT = "readtimeout"


EXECUTED = 1
PENDING = -1
CANCELLED = -2
REJECTED = -3
NO_RESPONSE = 0
NOT_INITIATED = -4
INITIATED = -5

STATUS_OPEN = "OPEN"
STATUS_COMPLETE = "COMPLETE"
STATUS_CANCELLED = "CANCELLED"
STATUS_REJECTED = "REJECTED"

BUY = "BUY"
SELL = "SELL"

DEBUG_MODE = False
KEY_CE = "CE"
KEY_PE = "PE"


class TradeWindow(QMainWindow):

    __instance = None

    def __init__(self):
        super().__init__()


        self.onTickRaceLock = threading.Lock()
        self.tickLooperraceLock = threading.Lock()
        self.orderUpdateraceLock = threading.Lock()

        self.greeksThread = WorkerLoopedThread(KiteApi.ins().deriveOptionsGreeks, loopsEverySec = 1, 
                                               startedMessage = "Started Greeks Calucations", 
                                               stoppedMessage = "Stopped Greeks Calculations")
        self.ticksThread = TickLooperThread(self.tickLooperThreadFunc, loopsEverySec = 0.25,
                                            startedMessage = "Started Ticks process", 
                                               stoppedMessage = "Stopped Ticks process")
        self.ticksThread.UpdateUi.connect(self.updatePriceLabels)
        

        self.executionThread = WorkerThread(self.executionThreadFunc)
        self.statusBartimer = None
        self.orderStatusTimer = None
        self.orderPlaceErrorTimer = None

        self.updateQTProcesEvents = WorkerLoopedThread(self.process_events, loopsEverySec = 30)
        self.updateQTProcesEvents.start()

        ui_file_name = "ui_templates/options_rifle_UI_2.ui"
        ui_file = QFile(ui_file_name)

        print("Started UI")

        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)

        self.loader = QUiLoader()
        self.window = self.loader.load(ui_file)
        ui_file.close()
        self.window.setWindowTitle("Scalp M16")
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
        self.window.btn_editrisk.clicked.connect(self.clickedEditRisk)
        self.window.btn_execute.clicked.connect(self.clickedExecute)

        self.window.spin_stoploss.setMinimum(5)

        ## SET BUTTONGS AND ITS FUNCTIONS FOR TRADE FRAME 
        self.window.btn_decrease_sl.clicked.connect(self.clickeddedcreaseSL)
        self.window.btn_increase_sl.clicked.connect(self.clickedIncreaseSL)
        self.window.btn_edit_sl.clicked.connect(self.clickedEditSL)
        self.window.btn_increase_sl.setIcon(QIcon('icons/btn_plus.png'))
        self.window.btn_decrease_sl.setIcon(QIcon('icons/btn_minus.png'))
        self.window.btn_edit_sl.setIcon(QIcon('icons/btn_edit_sl.png'))
        self.window.btn_auto_trail.setIcon(QIcon('icons/btn_auto_trail_off.png'))


        self.window.btn_exit.clicked.connect(self.clickedExitTrade)
        self.window.btn_exit.setStyleSheet(cssBtnExit)
        self.window.btn_exit.hide()
        self.window.frame_trade.hide()
        self.window.label_no_position.show()


        # Set the validator to accept INT point numbers only
        self.riskValidator = QIntValidator(1,999999) 
        self.slValidator = QIntValidator(0,999999)
        self.window.et_risk.setValidator(self.riskValidator)
        #self.window.et_stoploss.setValidator(self.slValidator)

        #inititalise Startup Parameters
        self.clickedBounce()
        self.clickedLong()
        self.window.spinner_ticker.addItem("BANKNIFTY")
        self.updateLabelMtMAmount(round(KiteApi.ins().finalPnL, 2))

        ##self.window.spinner_ticker.addItem("NIFTY")

        self.enableOptionsRifleUi()
        self.updateStatusBar()

        self.riskPerTrade = 5000
        self.window.et_risk.setText("5000")
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

    def disableOptionsRifleUI(self) :
        self.window.MainWinodw2.setEnabled(False)
        self.overlay_frame.show()

    def enableOptionsRifleUi(self) : 
        self.window.MainWinodw2.setEnabled(True)
        self.overlay_frame.hide()

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
        self.window.btn_long.setStyleSheet(cssBtnlongEnabled)
        self.window.btn_short.setStyleSheet(cssBtnShortDisabled)
        self.window.btn_long.setIcon(QIcon('icons/btn_long_enabled.png'))
        self.window.btn_short.setIcon(QIcon('icons/btn_short_disabled.png'))

        return          
    def clickedShort(self):

        self.tradeType = SHORT
        self.window.btn_long.setStyleSheet(cssBtnlongDisabled)
        self.window.btn_short.setStyleSheet(cssBtnShortEnabled)
        self.window.btn_long.setIcon(QIcon('icons/btn_long_disabled.png'))
        self.window.btn_short.setIcon(QIcon('icons/btn_short_enabled.png'))
        return 
    
    
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
            self.window.et_risk.setFocus()
            self.window.btn_editrisk.setIcon(QIcon('icons/btn_set_risk.png'))
            self.window.et_risk.setStyleSheet(cssEtEditRiskEnabled)
        return    
    
    def clickedExecute(self):
        self.window.btn_execute.setEnabled(False)
        self.executionThread.start()
        return     
    
    def executionThreadFunc(self) :
        slPrice = self.window.spin_stoploss.value()
        self.executeButtonUIupdate(1)
        status = KiteApi.ins().executeTrade(self.tradeType, slPrice, self.riskPerTrade,self.stg)
        if status == ORDER_PLACED :
            self.updateStatusBar("Entry Order Placed!", delayReset= True)
        elif status == ORDER_ERROR_READ_TIMEOUT:
            self.updateStatusBar(">>> Entry Order request Timed Out! Try Again", delayReset= True)
            self.executeButtonUIupdate(0)
        elif status == ORDER_ERROR :
            print("Kite Order Error")
            if self.orderPlaceErrorTimer is not None :
                self.orderPlaceErrorTimer.cancel()
            self.orderPlaceErrorTimer = threading.Timer(5.0, self.checkResponseFromEntryOrderupdate)
            self.orderPlaceErrorTimer.start()

        elif status == ORDER_ERROR_0_POSITION_SIZING :
            self.updateStatusBar("0 Qty possible", delayReset= True)
            self.executeButtonUIupdate(0)

    def checkResponseFromEntryOrderupdate(self) :
        if KiteApi.ins().currentTradePosition.tradeEntryStatus == NO_RESPONSE :
            self.updateStatusBar("Kite order placing error... ", delayReset= True)
            self.executeButtonUIupdate(0)

    def checkResponseFromExitOrderupdate(self) :
        if KiteApi.ins().currentTradePosition.tradeExitStatus == NO_RESPONSE :
            self.updateStatusBar("Kite order placing error... ", delayReset= True)
            self.exitButtonUIupdate(0)

    def exitButtonUIupdate(self,exiting = 1) :
        if exiting == 1 :
            self.window.btn_Exit.setEnabled(False)
            self.window.btn_Exit.setText("...")
            self.window.btn_Exit.setStyleSheet(cssBtnExiting)
        else :
            self.window.btn_Exit.setEnabled(True)
            self.window.btn_Exit.setText("Exit")
            self.window.btn_Exit.setStyleSheet(cssBtnExit)

    def executeButtonUIupdate(self,executing = 1) :
        if executing == 1 :
            self.window.btn_execute.setEnabled(False)
            self.window.btn_execute.setText("...")
            self.window.btn_execute.setStyleSheet(cssBtnExecuting)
        else :
            self.window.btn_execute.setEnabled(True)
            self.window.btn_execute.setText("Execute")
            self.window.btn_execute.setStyleSheet(cssBtnExecute)

    def updateStatusBar(self, message = " ", delayReset = False) : 
        self.window.statusbar.showMessage(message)
        if delayReset : 
            if self.statusBartimer is not None :
                self.statusBartimer.cancel()
            self.statusBartimer = threading.Timer(3.0, self.resetStatusBarText)
            self.statusBartimer.start()
    
    def resetStatusBarText(self) : 
        self.updateStatusBar(" ") 

    def updateLabelMtMAmount(self, MTM) :
        if MTM < 0 :
            rewardStr = str(MTM)
        else :
            rewardStr = "+" + str(MTM)
        
        if MTM < 0 :  self.window.label_MTM.setStyleSheet(cssMTMRed) 
        else : self.window.label_MTM.setStyleSheet(cssMTMGreen)

        self.window.label_MTM.setText(rewardStr)

    def updatePriceLabels(self) :

        strike_diff = -2
        if statics.DEBUG_MODE :
            strike_diff = 7

        CEStrike = Utilities.getStrikePrice(KiteApi.ins().bnfSpotLtp,KEY_CE, strike_diff)
        PEStrike = Utilities.getStrikePrice(KiteApi.ins().bnfSpotLtp,KEY_PE, strike_diff)

        self.window.label_call_strike.setText(str(CEStrike))
        self.window.label_put_strike.setText(str(PEStrike))        

        #preDiff = round(KiteApi.ins().bnfLtp - KiteApi.ins().bnfSpotLtp, 1)

        self.window.label_spot.setText(str(KiteApi.ins().bnfSpotLtp))

        if KiteApi.ins().currentTradePosition is not None :
            trade = KiteApi.ins().currentTradePosition
            self.window.label_trade_ltp.setText(str(trade.ltp))
            unRealisedMtm = KiteApi.ins().finalPnL + trade.unRealisedProfit
            if trade.tradeEntryStatus == EXECUTED :
                self.updateLabelMtMAmount(round(unRealisedMtm, 2))
                self.updateLabelUnrealisedRewardAmount(trade.unRealisedProfit, 
                                                       trade.unRealisedProfitInPoints, 
                                                       trade.getHitRewardPointsStr())

    
    """
    #################################################################################################
    #################################################################################################
    #################################################################################################
    #################################################################################################
    """


    def entryOrderExecuted(self) :

        trade = KiteApi.ins().currentTradePosition
        if trade.tradeType == LONG :
            self.window.icon_trade_type.setIcon(QIcon('icons/icon_arrow_long.png'))    
        else :
            self.window.icon_trade_type.setIcon(QIcon('icons/icon_arrow_short.png'))    

        if trade.strategy == AGGRESIVE :
            self.window.label_strategy.setText('AT')
        elif trade.strategy == DEFENSIVE :
            self.window.label_strategy.setText('DT')
        else:
            self.window.label_strategy.setText('BT')

        self.window.label_instrument.setText(trade.strikeStr)
        self.window.label_trade_qty.setText(str(trade.qty))
        self.window.label_avg_price.setText(str(trade.entryPrice))
        self.window.label_trade_ltp.setText(str(trade.ltp))


        self.window.et_stoploss.setText(str(trade.stoplossPrice))
        self.window.et_stoploss.setEnabled(False)
        #self.window.btn_edit_sl.hide()

        ##self.updateSLMaxPrice(trade.ltp)

        self.updateLabelRiskAmount(trade.riskAmount, trade.stoplossPoints, trade.initialSLPoints)
        self.updateLabelUnrealisedRewardAmount(trade.unRealisedProfit, 
                                               trade.unRealisedProfitInPoints,
                                               trade.getHitRewardPointsStr())


        self.window.label_no_position.hide()
        self.window.frame_trade.show()
        self.window.btn_exit.setText("Exit")
        self.window.btn_exit.setStyleSheet(cssBtnExit)
        self.window.btn_exit.show()
        self.window.btn_execute.hide()



    def clickedIncreaseSL(self) :
        KiteApi.ins().currentTradePosition.incrementSl()
        self.window.et_stoploss.setText(str(KiteApi.ins().currentTradePosition.stoplossPrice))
        self.updateLabelRiskAmount(KiteApi.ins().currentTradePosition.riskAmount, 
                                   KiteApi.ins().currentTradePosition.stoplossPoints, 
                                   KiteApi.ins().currentTradePosition.initialSLPoints)
        return
    
    def clickeddedcreaseSL(self) :
        if KiteApi.ins().currentTradePosition.stoplossPrice < 1 :
            return

        KiteApi.ins().currentTradePosition.decrementSl()
        
        self.window.et_stoploss.setText(str(KiteApi.ins().currentTradePosition.stoplossPrice))
        self.updateLabelRiskAmount(KiteApi.ins().currentTradePosition.riskAmount, 
                                   KiteApi.ins().currentTradePosition.stoplossPoints,
                                   KiteApi.ins().currentTradePosition.initialSLPoints)
        return
    
    def clickedEditSL(self) :

        if self.window.et_stoploss.isEnabled() : 
             ## set Risk
             self.window.et_stoploss.setEnabled(False)
             self.window.btn_edit_sl.setIcon(QIcon('icons/btn_edit_sl.png'))
             self.window.et_stoploss.setStyleSheet(cssEtEditSlDisabled)
             KiteApi.ins().currentTradePosition.setStoploss(int(self.window.et_stoploss.text()))
             self.updateLabelRiskAmount(KiteApi.ins().currentTradePosition.riskAmount, 
                                        KiteApi.ins().currentTradePosition.stoplossPoints,
                                        KiteApi.ins().currentTradePosition.initialSLPoints)

        else:
            ## edit risk
            self.window.et_stoploss.setEnabled(True)
            self.window.et_stoploss.setFocus()
            self.window.btn_edit_sl.setIcon(QIcon('icons/btn_set_sl.png'))
            self.window.et_stoploss.setStyleSheet(cssEtEditSlEnabled)


        return    
    
    def updateLabelRiskAmount(self, riskAmount, riskPoints, initialRiskPoints) :
        if riskAmount < 0 :
            riskPointStr = str(initialRiskPoints) + " | " + "+" + str(riskPoints)
            riskStr = "+" + str(abs(riskAmount))
        else :
           riskPointStr = str(initialRiskPoints) + " | " + str(riskPoints)
           riskStr = str(riskAmount)

        if riskAmount < 0 :  self.window.label_risk.setStyleSheet(cssMTMGreen) 
        elif riskAmount == 0 : self.window.label_risk.setStyleSheet(cssMTMWhite)
        else : self.window.label_risk.setStyleSheet(cssMTMRed)
        
        self.window.label_risk_points.setText(riskPointStr)
        self.window.label_risk.setText(riskStr)
        return
    
    def updateLabelUnrealisedRewardAmount(self, rewardAmount, rewardPoints, hitRewardPointsStr) :
        if rewardAmount <= 0 :
            rewardPointStr =  str(rewardPoints) + " | "  + hitRewardPointsStr
            rewardStr = str(rewardAmount) + " | " + str(rewardPoints)
        else :
            rewardPointStr = "+" + str(rewardPoints) + " | " + hitRewardPointsStr
            rewardStr = "+" + str(rewardAmount)  + " | " + "+" + str(rewardPoints)

        if rewardAmount < 0 :  self.window.label_profit.setStyleSheet(cssMTMRed) 
        elif rewardAmount == 0 : self.window.label_profit.setStyleSheet(cssMTMWhite)
        else : self.window.label_profit.setStyleSheet(cssMTMGreen)
        
        self.window.label_profit_points.setText(hitRewardPointsStr)
        self.window.label_profit.setText(rewardStr)
        return
    
    def clickedExitTrade(self) :
        status = KiteApi.ins().exitCurrentPosition()

        if status == ORDER_PLACED :
            self.updateStatusBar("Exit Order Placed!", delayReset= True)
        elif status == ORDER_ERROR_READ_TIMEOUT:
            self.updateStatusBar("<<< Exit Order request Timed Out! Try Again", delayReset= True)
            self.executeButtonUIupdate(0)
        elif status == ORDER_ERROR :
            print("Kite Order Error")
            if self.orderPlaceErrorTimer is not None :
                self.orderPlaceErrorTimer.cancel()
            self.orderPlaceErrorTimer = threading.Timer(5.0, self.checkResponseFromExitOrderupdate)
            self.orderPlaceErrorTimer.start()
            self.exitButtonUIupdate(1)

    """def updateOrderStatusLabel(self,str, delayedHide = False) : 
        self.window.label_order_status.show()
        self.window.label_order_status.setText(str)
        if delayedHide : 
            if self.orderStatusTimer is not None :
                self.orderStatusTimer.cancel()
            self.orderStatusTimer = threading.Timer(2.0, self.hideOrderstatus)
            self.orderStatusTimer.start()"""

    def exitOrderExecuted(self) :
        KiteApi.ins().addLastTradeToTradesList()
        KiteApi.ins().currentTradePosition = None

        self.updateLabelMtMAmount(round(KiteApi.ins().finalPnL, 2))
        self.window.btn_execute.show()
        self.window.btn_execute.setEnabled(True)
        self.window.btn_execute.setText("Execute")
        self.window.btn_execute.setStyleSheet(cssBtnExecute)
        self.window.btn_exit.hide()
        
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
        #print("tick recived")
        self.onTickRaceLock.acquire()
        self.ticksThread.setTickReceived(ticks)
        self.onTickRaceLock.release()
        return
    
        

    def tickLooperThreadFunc(self, ticks) :
        self.tickLooperraceLock.acquire()
        start_time = time.time()

        for tick in ticks :

            if tick['instrument_token'] == KiteApi.ins().getbnfSpotToken() :
                KiteApi.ins().bnfSpotLtp = tick['last_price']
            if tick['instrument_token'] == KiteApi.ins().getUpcomingbnfFutureToken() :
                KiteApi.ins().bnfLtp = tick['last_price']
            if KiteApi.ins().currentTradePosition is not None :
                trade = KiteApi.ins().currentTradePosition
                if tick['instrument_token'] == trade.tickerToken :
                    trade.updateLtp(tick['last_price'])
                    
        KiteApi.ins().setLTPforRequiredTokens(ticks)

        if KiteApi.ins().currentTradePosition is not None :
            trade = KiteApi.ins().currentTradePosition
            if trade.tradeEntryStatus == EXECUTED :
                if KiteApi.ins().tokensLtp[trade.tickerToken] <= trade.stoplossPrice :
                    if trade.tradeExitStatus == NOT_INITIATED:
                        trade.tradeExitStatus = INITIATED
                        self.clickedExitTrade()
                        print('TRADE ALERT : Position SL hit, Exiting the trade')

        end_time = time.time()
        time_taken = end_time - start_time
        #print(f"Time taken: {time_taken} seconds")
        self.tickLooperraceLock.release()

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
        self.orderUpdateraceLock.acquire()
        if KiteApi.ins().currentTradePosition is not None :
            trade = KiteApi.ins().currentTradePosition

            if trade.tickerToken == data['instrument_token'] and data['transaction_type'] == BUY and trade.tradeEntryStatus != EXECUTED:

                trade.entryOrderId = data['order_id']

                if data['status'] == STATUS_OPEN:
                    trade.updateTradeEntryStatus(PENDING)
                    self.updateStatusBar(">>> Order Waiting for execution...")
                    print('ORDER UPDATE : >>> Entry Order Pending')

                if data['status'] == STATUS_COMPLETE :
                    trade.updateTradeEntryStatus(EXECUTED, data['average_price'])
                    self.entryOrderExecuted()
                    self.updateStatusBar(">>> Order executed!", True)
                    print('ORDER UPDATE : >>> Entry Order Executed at ' + str(data['average_price']))

                if data['status'] == STATUS_CANCELLED :
                    trade.updateTradeEntryStatus(CANCELLED, data['average_price'])
                    self.updateStatusBar(">>> Order Cancelled !", True)
                    print('ORDER UPDATE : >>> Entry Order Cancelled due to ' + data['status_message'])
                    KiteApi.ins().currentTradePosition = None
                    self.executeButtonUIupdate(0)
                    self.window.label_no_position.show()
                    return

                if data['status'] == STATUS_REJECTED :
                    trade.updateTradeEntryStatus(REJECTED, data['average_price'])
                    self.updateStatusBar(">>> Rejected | " + data['status_message'], True)
                    print('ORDER UPDATE : >>> Entry Order Rejected due to ' + data['status_message'])
                    KiteApi.ins().currentTradePosition = None
                    self.executeButtonUIupdate(0)
                    self.window.label_no_position.show()
                    return

            if trade.tickerToken == data['instrument_token'] and data['transaction_type'] == SELL and trade.tradeExitStatus != EXECUTED:

                trade.exitOrderId = data['order_id']

                if data['status'] == STATUS_OPEN:
                    trade.updateTradeExitStatus(PENDING)
                    self.updateStatusBar("<<< Order Waiting for execution...")
                    print('ORDER UPDATE : <<< Exit Order Pending')

                if data['status'] == STATUS_COMPLETE :
                    
                    trade.updateTradeExitStatus(EXECUTED, data['average_price'])
                    self.exitOrderExecuted()
                    self.updateStatusBar("<<< Order executed!")
                    print('ORDER UPDATE : <<< Exit Order Executed at ' + str(data['average_price']))

                if data['status'] == STATUS_CANCELLED :
                    trade.updateTradeExitStatus(CANCELLED, data['average_price'])
                    self.updateStatusBar("<<< Exit Order cancelled, Need manual Intervention", True)
                    self.exitButtonUIupdate(0)
                    print('ORDER UPDATE : <<< Exit Order Cancelled due to ' + data['status_message'])

                if data['status'] == STATUS_REJECTED :
                    trade.updateTradeExitStatus(REJECTED, data['average_price'])
                    self.updateOrderStatusLabel("Exit Rejected", True)
                    self.updateStatusBar("<<< Exit Order Rejected, Need manual Intervention", True)
                    self.exitButtonUIupdate(0)
                    print('ORDER UPDATE : <<< Exit Order Rejected due to ' + data['status_message'])


        self.orderUpdateraceLock.release()

        #logging.debug("Order Update: {}".format(data))
        return
    

   
    #############################################################################################
    #############################################################################################
    #############################################################################################
    #############################################################################################
    #############################################################################################
    #############################################################################################
    #############################################################################################

    def timerEventCheckWidnowA(self, event):
        if not self.isActiveWindow():
            print('Window is inactive')

    def process_events(self):
        QApplication.processEvents()
        KiteApi.ins().sendEmptyOrderTokeepTheServerAlive()
        print("Processed QT events at", QDateTime.currentDateTime().toString())



