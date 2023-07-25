import kiteconnect
from kiteconnect import KiteConnect
import webbrowser
import pandas as pd
import datetime as dt
import os
import mibian
from kiteconnect.ticker import KiteTicker
import Utils.Utilities
import Utils.StaticVariables as statics
import threading
import time 
from Model.Trade import Trade
import logging
from requests.exceptions import ReadTimeout
from BrokerManager import BrokerManager

class DBManager() : 
     
    __instance = None

    def __init__(self) : 

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

        self.riskPerTrade = 0
        self.currentTradePosition = None
        self.tradesList = []
        self.finalPnL= 0.0

        self.optionsRaceLock = threading.Lock()
        self.executionRaceLock = threading.Lock()
    
    @staticmethod
    def i() :
        if DBManager.__instance is None:
           DBManager.__instance = DBManager()
        return DBManager.__instance
    
    def getbnfSpotToken(self) :
        if (self.bnfSpotToken != 0) :
            return self.bnfSpotToken
        self.bnfSpotToken = int(self.getInstrumentToken(name = "NIFTY BANK", instrumentType= statics.KEY_EQ))
        return self.bnfSpotToken
    
    def getUpcomingbnfFutureToken(self) :
        if (self.bnfFuturesToken != 0) :
            return self.bnfFuturesToken
        self.bnfFuturesToken = int(self.getInstrumentToken(name = "BANKNIFTY", instrumentType= statics.KEY_FUT, expiry=self.upcomingFutureExpiry))
        return self.bnfFuturesToken
    
    def getAllRequiredInstrumentListTokens(self) :
        tokenList = [int(x) for x in self.localRequirmentList['instrument_token'].tolist()]
        #print(tokenList)
        return tokenList
    
    def setRequiredOptionsDf(self) : 
        self.optionsDf = self.localRequirmentList.loc[(self.localRequirmentList['instrument_type'] == "CE") | (self.localRequirmentList['instrument_type'] == "PE")] 

    def getInstrumentToken(self,name = "", instrumentType = statics.KEY_EQ, expiry = "", strike = 0) :
        tokenId = 0
        if instrumentType == statics.KEY_EQ : 
            df1 = self.localRequirmentList.loc[(self.localRequirmentList['name'] == name) & (self.localRequirmentList['instrument_type'] == instrumentType)]
            tokenId = df1['instrument_token']
        elif instrumentType == statics.KEY_FUT:
            df1 = self.localRequirmentList.loc[(self.localRequirmentList['name'] == name) & (self.localRequirmentList['instrument_type'] == instrumentType)]
            df2 = df1.loc[df1['expiry'] == expiry]
            tokenId = df2['instrument_token']
        elif instrumentType == statics.KEY_CE or instrumentType == statics.KEY_PE :
            df1 = self.localRequirmentList.loc[(self.localRequirmentList['name'] == name) & (self.localRequirmentList['instrument_type'] == instrumentType)]
            df2 = df1.loc[(df1['expiry'] == expiry) & (df1['strike'] == strike)]
            tokenId = df2['instrument_token']
        
        if len(tokenId) == 0:
            return 0
        
        return tokenId.iloc[0]
    
    def getSelectedStrikeOption(self,name = "", instrumentType = statics.KEY_CE, expiry = "", strike = 0) :
        df1 = self.localRequirmentList.loc[(self.localRequirmentList['name'] == name) & (self.localRequirmentList['instrument_type'] == instrumentType)]
        df2 = df1.loc[(df1['expiry'] == expiry) & (df1['strike'] == strike)]
        
        if df2.size == 0:
            return None
        
        return df2.iloc[0]
    
    def getInstrumentsAndTrades(self) :
        result = "Success"

        todayDateStr = dt.date.today().strftime("%d-%m-%Y")
        filename = todayDateStr + "_trades.csv"
        tradeFilePath = "G:\\andyvoid\\projects\\andyvoid_tools\\options_rifle\\database\\trades_logs\\"+filename

        if os.path.exists(tradeFilePath) :
           tradeDf =  pd.read_csv(tradeFilePath, parse_dates = ['entry_time', 'exit_time'])
           self.tradesList = tradeDf.to_dict('records')
           self.finalPnL =  sum(trade['pnl'] for trade in self.tradesList)

        yesterdayDateStr= (dt.date.today() - dt.timedelta(days=1)).strftime("%d-%m-%Y")

        filename = yesterdayDateStr+"_required_instrument_list.csv"
        filename2 = yesterdayDateStr+"_required_instrument_list_2.csv"


        now = dt.datetime.now()
        eight_thirty_am = now.replace(hour=8, minute=30, second=0, microsecond=0)

        if now > eight_thirty_am:
            filename = todayDateStr+"_required_instrument_list.csv"

        requirmentsFilePath = "G:\\andyvoid\\projects\\andyvoid_tools\\options_rifle\\database\\instrument_list\\"+filename

        ### Get todays trades if file exits

        if os.path.exists(requirmentsFilePath):
            self.localRequirmentList = pd.read_csv(requirmentsFilePath, parse_dates = ['expiry'])
            self.upcomingFutureExpiry = self.localRequirmentList.loc[self.localRequirmentList['instrument_type'] == "FUT"]['expiry'].min()
            self.upcomingOptionsExpiry = self.localRequirmentList.loc[(self.localRequirmentList['instrument_type'] == "CE") | (self.localRequirmentList['instrument_type'] == "PE")]['expiry'].min()
            print(self.upcomingFutureExpiry)
            print(self.upcomingOptionsExpiry)
            return result
        
        ### GET REQUIRED INSTRUMENTS 
    
        instrumentList = BrokerManager.ins().getIntrumentList()

        instrumentMain = []
        banknifty_instrumenttk = []
        for instrument in instrumentList: 
            if "INDICES" in instrument["segment"]:
                if "NIFTY BANK" == instrument["tradingsymbol"] or  "NIFTY 50" == instrument["tradingsymbol"] or  "NIFTY FIN SERVICE" == instrument["tradingsymbol"] : 
                    instrumentMain.append(instrument)
            if "FUT" in instrument["instrument_type"] :
                if "BANKNIFTY" == instrument["name"] or "NIFTY" == instrument["name"] or "FINNIFTY" == instrument["name"] : 
                    banknifty_instrumenttk.append(instrument)
            if "CE" in instrument["instrument_type"] or "PE" in instrument["instrument_type"]:
                if "BANKNIFTY" == instrument["name"] or "NIFTY" == instrument["name"] or "FINNIFTY" == instrument["name"] : 
                    banknifty_instrumenttk.append(instrument)

        niftyBankInstruments = pd.DataFrame(banknifty_instrumenttk)
        niftyBankInstruments.to_csv("G:\\andyvoid\\projects\\andyvoid_tools\\options_rifle\\database\\instrument_list\\" + filename2, index= False)

        self.upcomingFutureExpiry = niftyBankInstruments.loc[niftyBankInstruments['instrument_type'] == "FUT"]['expiry'].min()
        self.upcomingOptionsExpiry = niftyBankInstruments.loc[(niftyBankInstruments['instrument_type'] == "CE") | (niftyBankInstruments['instrument_type'] == "PE")]['expiry'].min()
        
        requiredInstrumentsFut = niftyBankInstruments.loc[(niftyBankInstruments['instrument_type'] == "FUT")] #& (niftyBankInstruments['expiry'] == self.upcomingFutureExpiry)]
        requiredInstrumentsOpt = niftyBankInstruments.loc[((niftyBankInstruments['instrument_type'] == "CE") | (niftyBankInstruments['instrument_type'] == "PE"))] #& (niftyBankInstruments['expiry'] == self.upcomingOptionsExpiry)]
        
        self.localRequirmentList = pd.DataFrame(instrumentMain) 
        self.localRequirmentList = self.localRequirmentList.append(requiredInstrumentsFut)
        self.localRequirmentList = self.localRequirmentList.append(requiredInstrumentsOpt)

        print(self.upcomingFutureExpiry)
        print(self.upcomingOptionsExpiry)

        # Convert expiry colums into datatime format
        self.localRequirmentList['expiry'] = pd.to_datetime(self.localRequirmentList['expiry'])
        self.upcomingOptionsExpiry = pd.to_datetime(self.upcomingOptionsExpiry)
        self.upcomingFutureExpiry = pd.to_datetime(self.upcomingFutureExpiry)
        
        self.localRequirmentList.to_csv("G:\\andyvoid\\projects\\andyvoid_tools\\options_rifle\\database\\instrument_list\\" + filename, index= False)

        
        return result
    

    def setLTPforRequiredTokens(self, ticks) :
        self.optionsRaceLock.acquire()
        for tick in ticks:
            self.tokensLtp[tick["instrument_token"]] = tick['last_price']
        self.optionsRaceLock.release()

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


    def enterTrade(self, type, SLSpotPoints, maxRiskPerTrade) : 

        status = statics.ORDER_ERROR
        start_time = time.time()
        self.executionRaceLock.acquire() 

        ce_or_pe = statics.KEY_CE if type != statics.KEY_SHORT else statics.KEY_PE

        strike_diff = -1
        if statics.DEBUG_MODE :
            strike_diff = 7

        strike = Utils.Utilities.getStrikePrice(self.bnfSpotLtp,ce_or_pe, strike_diff)

        try :
            df = self.getSelectedStrikeOption(statics.KEY_BANKNIFTY_FUT, ce_or_pe, self.upcomingOptionsExpiry, strike)
            if df is None :
                self.logging.info("ERROR : Retrived dataframe empty : {}".format(e.message))
                return statics.ORDER_ERROR
            
        except Exception as e:
           self.executionRaceLock.release() 
           end_time = time.time()
           time_taken = end_time - start_time
           print(f"Time taken to Place order: {time_taken} seconds")
           print("ERROR : Retrive Selected option From datafrom")
           return statics.ORDER_ERROR
        
        print(df)
        
        tickerToken = df['instrument_token']
        tradingSymbol = df['tradingsymbol']
        instrumentType = df['instrument_type']
        expiry = df['expiry']
        lotSize = df['lot_size']
        ltp = self.tokensLtp[tickerToken]

        #slSpotPoints = int(self.bnfLtp - SLSpot) if type != KEY_SHORT else int(SLSpot - self.bnfLtp)

        time_obj = dt.datetime.strptime(statics.MARKET_CLOSE_TIME, '%H:%M:%S').time()
        timeToExpiration = dt.datetime.combine(expiry, time_obj)
        timetoExpirationInHours = Utils.Utilities.getTimetoExpirationInHoursFromDays(timeToExpiration)

        iv = 0
        if instrumentType == statics.KEY_CE :
            c = mibian.BS([self.bnfSpotLtp,
                        strike, 
                        statics.RISK_FREE_INTEREST_RATE, 
                        timetoExpirationInHours], 
                        callPrice = ltp)
            iv = c.impliedVolatility
        elif instrumentType == statics.KEY_PE:    
            c = mibian.BS([self.bnfSpotLtp,
                        strike, 
                        statics.RISK_FREE_INTEREST_RATE, 
                        timetoExpirationInHours], 
                        putPrice = ltp)
            iv = c.impliedVolatility

        
        c = mibian.BS([self.bnfSpotLtp, 
                        strike, 
                        statics.RISK_FREE_INTEREST_RATE, 
                        timetoExpirationInHours], 
                        volatility = iv)
        
        """ SL based on future IV drop 
        ivDropbuffer = (c.vega / 100) * 25
        slSpecial = slNormal + ((c.vega / 100) * 25)"""

        delta = float(c.callDelta) if type != statics.KEY_SHORT else float(c.putDelta)
        slPoints = abs(round(SLSpotPoints * delta, 2))
        qty = Utils.Utilities.getPositionsSizing(slPoints, maxRiskPerTrade,lotSize, debug = statics.DEBUG_MODE)

        if qty == 0 :
            end_time = time.time()
            time_taken = end_time - start_time
            print(f"Time taken to Place order: {time_taken} seconds")
            print("ERROR : Quantity Not satisfied with Risk per trade and Stoploss")
            self.executionRaceLock.release() 
            return statics.ORDER_ERROR_0_POSITION_SIZING
        
        self.currentTradePosition = Trade(tickerToken, type, tradingSymbol, qty, ltp, slPoints, strike)
        status = BrokerManager.ins().enterTrade(self.currentTradePosition)

        self.executionRaceLock.release() 
        end_time = time.time()
        time_taken = end_time - start_time

        if status == statics.ORDER_ERROR : 
            self.currentTradePosition.tradeEntryStatus = statics.NO_RESPONSE

        return status
    
        self.executionRaceLock.release() 
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Time taken to Place order: {time_taken} seconds")
        return ORDER_PLACED 
    
    def exitCurrentPosition(self) :
        trade = self.currentTradePosition
        trade.intentedExitPrice = self.tokensLtp[trade.tickerToken]
        status = BrokerManager.ins().exitTrade(trade)
        return status


    def addLastTradeToTradesList(self) : 
        self.tradesList.append(self.currentTradePosition.getAsDict())
        self.finalPnL =  sum(trade['pnl'] for trade in self.tradesList)
        tradesDf = pd.DataFrame(self.tradesList)

        todayDateStr = dt.date.today().strftime("%d-%m-%Y")
        filename = todayDateStr + "_trades.csv"
        tradeFilePath = "G:\\andyvoid\\projects\\andyvoid_tools\\options_rifle\\database\\trades_logs\\"+filename
        tradesDf.to_csv(tradeFilePath, index = False)


