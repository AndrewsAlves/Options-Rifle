import kiteconnect
from kiteconnect import KiteConnect
import webbrowser
import pandas as pd
import datetime as dt
import os
from kiteconnect.ticker import KiteTicker
import Utils.Utilities
import Utils.StaticVariables as statics
import threading
import time 
from Model.Trade import Trade
import logging
from requests.exceptions import ReadTimeout
from KiteApi import KiteApi

class BrokerManager() : 
     
    __instance = None

    def __init__(self) : 
        self.selectedBroker = statics.NOBROKER
    
    @staticmethod
    def ins() :
        if BrokerManager.__instance is None:
           BrokerManager.__instance = BrokerManager()
        return BrokerManager.__instance
    
    def getIntrumentList(self) : 
        if self.selectedBroker == statics.ZERODHA : return KiteApi.ins().kite.instruments()

    def enterTrade(self, trade) :
        status = statics.ORDER_ERROR
        if self.selectedBroker == statics.ZERODHA : 
            status = KiteApi.ins().enterTrade(trade)

        return status
    
    def exitTrade(self, trade) :
        status = statics.ORDER_ERROR
        if self.selectedBroker == statics.ZERODHA : 
            status = KiteApi.ins().exitCurrentPosition(trade)

        return status
    
    

        
