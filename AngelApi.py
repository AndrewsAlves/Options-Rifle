import webbrowser
import pandas as pd
import datetime as dt
import os
import Utils.Utilities
import Utils.StaticVariables as statics
import threading
import time 
from Model.Trade import Trade
import logging
from requests.exceptions import ReadTimeout

class AngelOneApi() : 
     
    __instance = None

    def __init__(self) : 
        self.selectedBroker = statics.NOBROKER
    
    @staticmethod
    def ins() :
        if AngelOneApi.__instance is None:
           AngelOneApi.__instance = AngelOneApi()
        return AngelOneApi.__instance