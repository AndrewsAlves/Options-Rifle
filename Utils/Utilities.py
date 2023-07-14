from PySide6.QtCore import QThread, Signal
import datetime as dt
import time
import math
import requests
import os, sys

def resourcePath(relativePath) : 
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relativePath)

class WorkerThread(QThread):
    finished = Signal(str)
    result = Signal()

    def __init__(self, func, *args, **kwargs):
        super(WorkerThread, self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        res = self.func(*self.args, **self.kwargs)
        self.finished.emit(res)


class WorkerLoopedThread(QThread):
    finished = Signal(str)
    result = Signal()
    stopped = Signal()

    def __init__(self, func, *args, **kwargs):
        super(WorkerLoopedThread, self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.is_running = True
        self.loopsEverySec = kwargs.get('loopsEverySec', 0)
        self.startMessage = kwargs.get('startedMessage', " ")
        self.stoppedMessage = kwargs.get('stoppedMessage', " ")


    def run(self):
        print(__class__.__name__ + " : " +  self.startMessage)
        while self.is_running :
            self.func()
            #self.finished.emit(res)
            time.sleep(self.loopsEverySec)

        self.is_running = False

    def stop(self) :
        self.is_running = False
        self.stopped.emit()
        print(__class__.__name__ + " : " +  self.stoppedMessage)

class TickLooperThread(QThread):
    stopped = Signal()
    UpdateUi = Signal()

    def __init__(self, func, *args, **kwargs):
        super(TickLooperThread, self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.is_running = True
        self.loopsEverySec = kwargs.get('loopsEverySec', 0)
        self.startMessage = kwargs.get('startedMessage', " ")
        self.stoppedMessage = kwargs.get('stoppedMessage', " ")
        self.ticks = {}

    def setTickReceived(self,ticks) :
        self.ticks = ticks

    def run(self):
        print(__class__.__name__ + " : " +  self.startMessage)
        while self.is_running :
            self.func(self.ticks)
            self.UpdateUi.emit()
            time.sleep(self.loopsEverySec)

        self.is_running = False

    def stop(self) :
        self.is_running = False
        self.stopped.emit()
        print(__class__.__name__ + " : " +  self.stoppedMessage)


def getTimetoExpirationInHoursFromDays(expirtDatetime) : 
    currentDatetime = dt.datetime.combine(dt.date.today(), dt.datetime.min.time())
    time_to_expiry_hours = float((expirtDatetime - currentDatetime).total_seconds() / 3600)
    time_to_expiry_days_in_hours = (1 / 24) * time_to_expiry_hours
    return time_to_expiry_days_in_hours

def getStrikePrice(ltp, CeOrPe = "CE" , ItmOTmStrikeLevel = 1, optionStrikeInterval = 100, debug = True) :
    rounded_ltp = round(ltp / 100) * 100

    strikeSelectionPoint = ItmOTmStrikeLevel * optionStrikeInterval

    if CeOrPe == "CE" :
        strike_price = rounded_ltp + strikeSelectionPoint
    else :
        strike_price = rounded_ltp - strikeSelectionPoint

    #print("Strike :", strike_price)
    return strike_price

def getPositionsSizing(stoplossPoints, risk_per_trade, lotSize, debug = True) :

    return lotSize

    if debug :
        # min lot size to test 
        return lotSize
    # calculate risk per option
    if stoplossPoints == 0 :
        return 0

    noOfUnitsPossible = risk_per_trade / stoplossPoints
    # calculate number of options
    position_size = (int(noOfUnitsPossible) // lotSize) * lotSize

    if position_size > 800: position_size = 800

    print("Position size:", position_size)
    return position_size

def getMaximumBuyPrice(SLPoints, Ltp) : 
    maxSlippage = 10 #% 
    return Ltp + ((SLPoints / 100) * maxSlippage)

def checkInternetConnection():
    url = "http://www.google.com"
    timeout = 5
    try:
        response = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False



