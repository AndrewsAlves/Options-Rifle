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

class BrokerManager() : 
     
    __instance = None

    def __init__(self) : 
        self.selectedBroker = statics.NOBROKER
    
    @staticmethod
    def ins() :
        if BrokerManager.__instance is None:
           BrokerManager.__instance = BrokerManager()
        return BrokerManager.__instance