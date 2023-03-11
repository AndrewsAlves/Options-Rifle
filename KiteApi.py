from kiteconnect import KiteConnect
import webbrowser
import pandas as pd
import datetime as dt
import os
from kiteconnect.ticker import KiteTicker


API_KEY= "yzczdzxsmw9w9tq9"
API_SECRET = "2k7oo9x1w0xl5g9789wl8j6v4u03lq0x"

KEY_NIFTYBANK = "NIFTY BANK"
KEY_BANKNIFTY_FUT = "BANKNIFTY"
KEY_CE = "CE"
KEY_PE = "PE"
KEY_FUT = "FUT"
KEY_EQ = "EQ"

class KiteApi() :
    __instance = None

    def __init__(self) : 
        self.kite = KiteConnect(api_key=API_KEY)    
        self.localRequirmentList = None
        self.upcomingFutureExpiry = None
        self.upcomingOptionsExpiry = None
        self.bnfSpotToken = 0
        self.bnfFuturesToken = 0
        self.ticker = None

    def openLoginUrl(self) :
        webbrowser.open_new(self.kite.login_url())
        return 
    
    def generateSession(self, requestToken) : 
        data = self.kite.generate_session(requestToken, api_secret=API_SECRET)
        access_token = data["access_token"]
        self.kite.set_access_token(access_token)
        self.ticker = KiteTicker(API_KEY, access_token=access_token)
        print("Request Token : " + requestToken)
        print("Access Token : " + access_token)
        return

    @staticmethod
    def getInstance() :
        if KiteApi.__instance is None:
           KiteApi.__instance = KiteApi()
        return KiteApi.__instance
    
    
    def connetInitialTickerSockets(self, funTicks, funConnect, funClose, funError, funMessage, funReconnect, funNoReconnect, funOnOrderUpdate) :
        self.ticker.on_ticks = funTicks
        self.ticker.on_connect = funConnect
        self.ticker.on_close = funClose
        self.ticker.on_error = funError
        self.ticker.on_message = funMessage
        self.ticker.on_reconnect = funReconnect
        self.ticker.on_noreconnect = funNoReconnect
        self.ticker.on_order_update = funOnOrderUpdate

        self.ticker.connect(threaded=True)
        return

    def getbnfSpotToken(self) :
        if (self.bnfSpotToken != 0) :
            return self.bnfSpotToken
        self.bnfSpotToken = int(self.getInstrumentToken(name = "NIFTY BANK", instrumentType=KEY_EQ))
        return self.bnfSpotToken
    
    def getUpcomingbnfFutureToken(self) :
        if (self.bnfFuturesToken != 0) :
            return self.bnfFuturesToken
        self.bnfFuturesToken = int(self.getInstrumentToken(name = "BANKNIFTY", instrumentType=KEY_FUT, expiry=self.upcomingFutureExpiry))
        return self.bnfFuturesToken
    
    def getInstrumentToken(self,name = "", instrumentType = KEY_EQ, expiry = "", strike = 0) :
        tokenId = 0
        if instrumentType == KEY_EQ : 
            df1 = self.localRequirmentList.loc[(self.localRequirmentList['name'] == name) & (self.localRequirmentList['instrument_type'] == instrumentType)]
            tokenId = df1['instrument_token']
        elif instrumentType == KEY_FUT:
            df1 = self.localRequirmentList.loc[(self.localRequirmentList['name'] == name) & (self.localRequirmentList['instrument_type'] == instrumentType)]
            df2 = df1.loc[df1['expiry'] == expiry]
            tokenId = df2['instrument_token']
        elif instrumentType == KEY_CE or instrumentType == KEY_PE :
            df1 = self.localRequirmentList.loc[(self.localRequirmentList['name'] == name) & (self.localRequirmentList['instrument_type'] == instrumentType)]
            df2 = df1.loc[(df1['expiry'] == expiry) & (df1['strike'] == strike)]
            tokenId = df2['instrument_token']
        
        if len(tokenId) == 0:
            return 0
        
        return tokenId.iloc[0]

    def getInstruments(self) :
        result = "Success"

        todayDateStr = dt.date.today().strftime("%d-%m-%Y")
        filename = todayDateStr+"_required_instrument_list.csv"
        requirmentsFilePath = "G:\\andyvoid\\projects\\andyvoid_tools\\options_rifle\\database\\"+filename

        if os.path.exists(requirmentsFilePath):
            self.localRequirmentList = pd.read_csv(requirmentsFilePath, parse_dates= True)
            self.upcomingFutureExpiry = self.localRequirmentList.loc[self.localRequirmentList['instrument_type'] == "FUT"]['expiry'].min()
            self.upcomingOptionsExpiry = self.localRequirmentList.loc[(self.localRequirmentList['instrument_type'] == "CE") | (self.localRequirmentList['instrument_type'] == "PE")]['expiry'].min()
            print(self.upcomingFutureExpiry)
            print(self.upcomingOptionsExpiry)
            return result
    
        instrumentList = self.kite.instruments()

        instrumentMain = []
        banknifty_instrumenttk = []
        for instrument in instrumentList: 
            if "INDICES" in instrument["segment"] and "NIFTY BANK" in instrument["tradingsymbol"]:
                instrumentMain.append(instrument)
            if "FUT" in instrument["instrument_type"] and "BANKNIFTY" in instrument["tradingsymbol"]:
                banknifty_instrumenttk.append(instrument)
            if "CE" in instrument["instrument_type"] and "BANKNIFTY" in instrument["tradingsymbol"]:
                banknifty_instrumenttk.append(instrument)
            if "PE" in instrument["instrument_type"] and "BANKNIFTY" in instrument["tradingsymbol"]:
                banknifty_instrumenttk.append(instrument)    

        niftyBankInstruments = pd.DataFrame(banknifty_instrumenttk)
        self.upcomingFutureExpiry = niftyBankInstruments.loc[niftyBankInstruments['instrument_type'] == "FUT"]['expiry'].min()
        self.upcomingOptionsExpiry = niftyBankInstruments.loc[(niftyBankInstruments['instrument_type'] == "CE") | (niftyBankInstruments['instrument_type'] == "PE")]['expiry'].min()
        
        requiredInstrumentsFut = niftyBankInstruments.loc[(niftyBankInstruments['instrument_type'] == "FUT") & (niftyBankInstruments['expiry'] == self.upcomingFutureExpiry)]
        requiredInstrumentsOpt = niftyBankInstruments.loc[((niftyBankInstruments['instrument_type'] == "CE") | (niftyBankInstruments['instrument_type'] == "PE")) & (niftyBankInstruments['expiry'] == self.upcomingOptionsExpiry)]
        
        self.localRequirmentList = pd.DataFrame(instrumentMain)
        self.localRequirmentList = self.localRequirmentList.append(requiredInstrumentsFut)
        self.localRequirmentList = self.localRequirmentList.append(requiredInstrumentsOpt)

        print(self.upcomingFutureExpiry)
        print(self.upcomingOptionsExpiry)
        
        self.localRequirmentList.to_csv("G:\\andyvoid\\projects\\andyvoid_tools\\options_rifle\\database\\" + filename, index= False)
        
        return result



