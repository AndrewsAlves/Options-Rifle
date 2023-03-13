from kiteconnect import KiteConnect
import webbrowser
import pandas as pd
import datetime as dt
import os
from kiteconnect.ticker import KiteTicker
import mibian
import Utils.Utilities
import threading
import time 



API_KEY= "yzczdzxsmw9w9tq9"
API_SECRET = "2k7oo9x1w0xl5g9789wl8j6v4u03lq0x"

KEY_NIFTYBANK = "NIFTY BANK"
KEY_BANKNIFTY_FUT = "BANKNIFTY"
KEY_CE = "CE"
KEY_PE = "PE"
KEY_FUT = "FUT"
KEY_EQ = "EQ"

KEY_LONG = "long"
KEY_SHORT = "short"

RISK_FREE_INTEREST_RATE = 6.5

MARKET_OPEN_TIME = '09:00:00'
MARKET_CLOSE_TIME = '15:30:00'

BNF_STRIKE_INTERVAL = 100




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

        self.bnfLtp= 0
        self.bnfSpotLtp = 0
        self.tokensLtp = {}
        self.optionsDf = None
        self.optionChain = None

        self.optionsRaceLock = threading.Lock()
        self.executionRaceLock = threading.Lock()

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
    def ins() :
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
    
    def getAllRequiredInstrumentListTokens(self) :
        tokenList = [int(x) for x in self.localRequirmentList['instrument_token'].tolist()]
        print(tokenList)
        return tokenList
    
    def setRequiredOptionsDf(self) : 
        self.optionsDf = self.localRequirmentList.loc[(self.localRequirmentList['instrument_type'] == "CE") | (self.localRequirmentList['instrument_type'] == "PE")] 

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
    
    def getSelectedStrikeOption(self,name = "", instrumentType = KEY_CE, expiry = "", strike = 0) :
        df1 = self.localRequirmentList.loc[(self.localRequirmentList['name'] == name) & (self.localRequirmentList['instrument_type'] == instrumentType)]
        df2 = df1.loc[(df1['expiry'] == expiry) & (df1['strike'] == strike)]
        
        if df2.size == 0:
            return None
        
        return df2.iloc[0]
    
    def getInstruments(self) :
        result = "Success"

        yesterdayDateStr= (dt.date.today() - dt.timedelta(days=1)).strftime("%d-%m-%Y")
        todayDateStr = dt.date.today().strftime("%d-%m-%Y")

        filename = yesterdayDateStr+"_required_instrument_list.csv"

        now = dt.datetime.now()
        eight_thirty_am = now.replace(hour=8, minute=30, second=0, microsecond=0)

        if now > eight_thirty_am:
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

        # Convert expiry colums into datatime format
        self.localRequirmentList['expiry'] = pd.to_datetime(self.localRequirmentList['expiry'])
        self.upcomingOptionsExpiry = pd.to_datetime(self.upcomingOptionsExpiry)
        self.upcomingFutureExpiry = pd.to_datetime(self.upcomingFutureExpiry)
        
        self.localRequirmentList.to_csv("G:\\andyvoid\\projects\\andyvoid_tools\\options_rifle\\database\\" + filename, index= False)
        
        return result
    
    def setOptionPrices(self, ticks) :
        self.optionsRaceLock.acquire()

        if self.optionsDf is None:
            self.setRequiredOptionsDf()

        if self.optionsDf.empty:
            return

        for tick in ticks :
            for index, row in self.optionsDf.iterrows():
                    if tick['instrument_token'] == row['instrument_token'] : 
                        row['last_price'] = tick['last_price']
        self.optionsRaceLock.release()

    def setLTPforRequiredTokens(self, ticks) :
        self.optionsRaceLock.acquire()
        for tick in ticks:
            self.tokensLtp[tick["instrument_token"]] = tick['last_price']
        self.optionsRaceLock.release()


    def deriveOptionsGreeks(self) : 

        if self.optionsDf is None:
            self.setRequiredOptionsDf()

        if self.optionsDf.empty:
            return

        self.optionsRaceLock.acquire()

        start_time = time.time()

        for index, row in self.optionsDf.iterrows():
            
            if row['last_price'] == 0 :
                continue

            time_obj = dt.datetime.strptime(MARKET_CLOSE_TIME, '%H:%M:%S').time()
            timeToExpiration = dt.datetime.combine(row['expiry'], time_obj)

            timetoExpirationInHours = Utils.Utilities.getTimetoExpirationInHours(timeToExpiration)

            iv = 0
            if row['instrument_type'] == KEY_CE :
                c = mibian.BS([self.bnfSpotLtp
                            , row['strike'], 
                            RISK_FREE_INTEREST_RATE, 
                            timetoExpirationInHours], 
                            callPrice = row['last_price'])
                iv = c.impliedVolatility
            elif row['instrument_type'] == KEY_PE:    
                c = mibian.BS([self.bnfSpotLtp
                            , row['strike'], 
                            RISK_FREE_INTEREST_RATE, 
                            timetoExpirationInHours], 
                            putPrice = row['last_price'])
                iv = c.impliedVolatility
                # Calculate Greeks

            c = mibian.BS([self.bnfSpotLtp
                            , row['strike'], 
                            RISK_FREE_INTEREST_RATE, 
                            timetoExpirationInHours], 
                            volatility = iv)

            if row['instrument_type'] == KEY_CE :
                row['delta'] = c.callDelta
                row['gammma'] = c.gamma
                row['theta'] = c.callTheta
                row['vega'] = c.vega
                row['iv'] = c.impliedVolatility

            elif row['instrument_type'] == KEY_PE :    
                row['delta'] = c.callDelta
                row['gammma'] = c.gamma
                row['theta'] = c.callTheta
                row['vega'] = c.vega
                row['iv'] = c.impliedVolatility
            
        self.optionsDf.round(3)    
            
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Time taken: {time_taken} seconds")

        self.optionsRaceLock.release()

        return
    

    def executeTrade(self, type, SLSpot, maxRiskPerTrade) : 
        self.executionRaceLock.acquire() 

        ce_or_pe = KEY_CE if type != KEY_SHORT else KEY_PE

        strike = Utils.Utilities.getStrikePrice(self.bnfSpotLtp)
        df = self.getSelectedStrikeOption(KEY_BANKNIFTY_FUT, ce_or_pe, self.upcomingOptionsExpiry, strike)
        
        instrumentType = df['instrument_type'][0]
        expiry = df['expiry'][0]
        lotSize = df['lot_size'][0]
        ltp = self.tokensLtp[df['instrument_token'][0]]

        time_obj = dt.datetime.strptime(MARKET_CLOSE_TIME, '%H:%M:%S').time()
        timeToExpiration = dt.datetime.combine(expiry, time_obj)
        timetoExpirationInHours = Utils.Utilities.getTimetoExpirationInHours(timeToExpiration)

        iv = 0
        if instrumentType == KEY_CE :
                c = mibian.BS([self.bnfSpotLtp,
                            strike, 
                            RISK_FREE_INTEREST_RATE, 
                            timetoExpirationInHours], 
                            callPrice = ltp)
                iv = c.impliedVolatility
        elif instrumentType == KEY_PE:    
            c = mibian.BS([self.bnfSpotLtp,
                        strike, 
                        RISK_FREE_INTEREST_RATE, 
                        timetoExpirationInHours], 
                        putPrice = ltp)
            iv = c.impliedVolatility

        c = mibian.BS([self.bnfSpotLtp, 
                        strike, 
                        RISK_FREE_INTEREST_RATE, 
                        timetoExpirationInHours], 
                        volatility = iv)


        slNormal = SLSpot * float(c.callDelta)

        ### SL based on future IV drop 
        ivDropbuffer = (c.vega / 100) * 25
        slSpecial = slNormal + ((c.vega / 100) * 25)

        







