import kiteconnect
from kiteconnect import KiteConnect
import webbrowser
import pandas as pd
import datetime as dt
import os
from kiteconnect.ticker import KiteTicker
import mibian
import Utils.Utilities
import Utils.StaticVariables as statics
import threading
import time 
from Model.Trade import Trade
import logging
from requests.exceptions import ReadTimeout


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

MAXIMUM_STOPLOSS_SPOT = 200

ORDER_PLACED = "orderplaced"
ORDER_ERROR = "ordererror"
ORDER_ERROR_READ_TIMEOUT = "readtimeout"
ORDER_ERROR_0_POSITION_SIZING = "ordererror_0_position_sizing"


NOT_INITIATED = -4
INITIATED = -5
NO_RESPONSE = 0
EXECUTED = 1
PENDING = -1
CANCELLED = -2
REJECTED = -3

DEBUG_MODE = False

logging.basicConfig(level=logging.DEBUG)


class KiteApi() :
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

        self.optionsRaceLock = threading.Lock()
        self.executionRaceLock = threading.Lock()

        self.riskPerTrade = 0
        self.currentTradePosition = None
        self.tradesList = []
        self.finalPnL= 0.0

    def openLoginUrl(self) :
        webbrowser.open_new(self.kite.login_url())
        return 
    
    def initialiseKite(self, apiKey, apiSecret) : 
        self.apiKey = apiKey
        self.apiSecret = apiSecret
        self.kite = KiteConnect(api_key=self.apiKey, timeout= 10)    

    def generateSession(self, requestToken) : 
        data = self.kite.generate_session(requestToken, api_secret= self.apiSecret)
        access_token = data["access_token"]
        self.kite.set_access_token(access_token)
        self.ticker = KiteTicker(self.apiKey, access_token=access_token, reconnect=True, reconnect_max_delay=5,reconnect_max_tries=100,connect_timeout=300)
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
        #print(tokenList)
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
    
    def executeTrade(self, type, SLSpotPoints, maxRiskPerTrade, stg) : 

        status = ORDER_ERROR
        start_time = time.time()
        self.executionRaceLock.acquire() 

        ce_or_pe = KEY_CE if type != KEY_SHORT else KEY_PE

        strike_diff = -1
        if statics.DEBUG_MODE :
            strike_diff = 7

        strike = Utils.Utilities.getStrikePrice(self.bnfSpotLtp,ce_or_pe, strike_diff)

        try :
            df = self.getSelectedStrikeOption(KEY_BANKNIFTY_FUT, ce_or_pe, self.upcomingOptionsExpiry, strike)
            if df is None :
                self.logging.info("ERROR : Retrived dataframe empty : {}".format(e.message))
                return ORDER_ERROR
            
        except Exception as e:
           self.executionRaceLock.release() 
           end_time = time.time()
           time_taken = end_time - start_time
           print(f"Time taken to Place order: {time_taken} seconds")
           print("ERROR : Retrive Selected option From datafrom")
           return ORDER_ERROR
        
        print(df)
        
        tickerToken = df['instrument_token']
        tradingSymbol = df['tradingsymbol']
        instrumentType = df['instrument_type']
        expiry = df['expiry']
        lotSize = df['lot_size']
        ltp = self.tokensLtp[tickerToken]

        #slSpotPoints = int(self.bnfLtp - SLSpot) if type != KEY_SHORT else int(SLSpot - self.bnfLtp)

        time_obj = dt.datetime.strptime(MARKET_CLOSE_TIME, '%H:%M:%S').time()
        timeToExpiration = dt.datetime.combine(expiry, time_obj)
        timetoExpirationInHours = Utils.Utilities.getTimetoExpirationInHoursFromDays(timeToExpiration)

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
        
        """ SL based on future IV drop 
        ivDropbuffer = (c.vega / 100) * 25
        slSpecial = slNormal + ((c.vega / 100) * 25)"""

        delta = float(c.callDelta) if type != KEY_SHORT else float(c.putDelta)
        slPoints = abs(round(SLSpotPoints * delta, 2))
        qty = Utils.Utilities.getPositionsSizing(slPoints, maxRiskPerTrade,lotSize, debug = statics.DEBUG_MODE)


        if qty == 0 :
            end_time = time.time()
            time_taken = end_time - start_time
            print(f"Time taken to Place order: {time_taken} seconds")
            print("ERROR : Quantity Not satisfied with Risk per trade and Stoploss")
            self.executionRaceLock.release() 
            return ORDER_ERROR_0_POSITION_SIZING

        # Place an order
        try:
            self.currentTradePosition = Trade(tickerToken, type, stg, tradingSymbol, qty, ltp, slPoints, strike)
            self.currentTradePosition.tradeEntryStatus = INITIATED
            order_id = self.kite.place_order(tradingsymbol=tradingSymbol,
                                        exchange=self.kite.EXCHANGE_NFO,
                                        transaction_type=self.kite.TRANSACTION_TYPE_BUY,
                                        quantity= qty,
                                        variety=self.kite.VARIETY_REGULAR,
                                        order_type=self.kite.ORDER_TYPE_MARKET,
                                        product=self.kite.PRODUCT_MIS,
                                        validity=self.kite.VALIDITY_DAY)
           
            self.currentTradePosition.entryOrderId = order_id

            status = ORDER_PLACED
            logging.info("Order placed. ID is: {}".format(order_id))

        except kiteconnect.exceptions.TokenException as e:
            status = ORDER_ERROR
            logging.error("TokenException occurred: {}".format(str(e)))
        except kiteconnect.exceptions.InputException as e:
            status = ORDER_ERROR
            logging.error("InputException occurred: {}".format(str(e)))
        except kiteconnect.exceptions.OrderException as e:
            status = ORDER_ERROR
            print("Order placement failed. Reason:", e.message)
        except kiteconnect.exceptions.NetworkException as e:
            status = ORDER_ERROR
            logging.error("NetworkException occurred: {}".format(str(e)))
        except kiteconnect.exceptions.GeneralException as e:
            status = ORDER_ERROR
            logging.error("GeneralException occurred: {}".format(str(e)))
        except ReadTimeout as e:
            status = ORDER_ERROR_READ_TIMEOUT
        except Exception as e :
            logging.error("Other exception occurred: {}".format(str(e)))
            status = ORDER_ERROR

        
        self.executionRaceLock.release() 
        end_time = time.time()
        time_taken = end_time - start_time

        if status == ORDER_ERROR : 
            self.currentTradePosition.tradeEntryStatus = NO_RESPONSE

        print(f">>> Time taken to place Entry order: {time_taken} seconds")
        return status
    
        self.executionRaceLock.release() 
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Time taken to Place order: {time_taken} seconds")
        return ORDER_PLACED 
    

    def exitCurrentPosition(self) :
        # Place an order

        status = ORDER_ERROR

        trade = self.currentTradePosition
        trade.intentedExitPrice = self.tokensLtp[trade.tickerToken]
        
        try:
            trade.tradeExitStatus = INITIATED
            order_id = self.kite.place_order(tradingsymbol=trade.tickerSymbol,
                                        exchange=self.kite.EXCHANGE_NFO,
                                        transaction_type=self.kite.TRANSACTION_TYPE_SELL,
                                        quantity= trade.qty,
                                        variety=self.kite.VARIETY_REGULAR,
                                        order_type=self.kite.ORDER_TYPE_MARKET,
                                        product=self.kite.PRODUCT_MIS,
                                        validity=self.kite.VALIDITY_DAY)
            

            logging.info("Order placed. ID is: {}".format(order_id))

            return ORDER_PLACED 
        except kiteconnect.exceptions.TokenException as e:
            logging.error("TokenException occurred: {}".format(str(e)))
            status = ORDER_ERROR 
        except kiteconnect.exceptions.InputException as e:
            logging.error("InputException occurred: {}".format(str(e)))
            status = ORDER_ERROR 
        except kiteconnect.exceptions.OrderException as e:
            print("Order placement failed. Reason:", e.message)
            status = ORDER_ERROR 
        except kiteconnect.exceptions.NetworkException as e:
            logging.error("NetworkException occurred: {}".format(str(e)))
            status = ORDER_ERROR 
        except kiteconnect.exceptions.GeneralException as e:
            logging.error("GeneralException occurred: {}".format(str(e)))
            status = ORDER_ERROR 
        except ReadTimeout as e:
            status = ORDER_ERROR_READ_TIMEOUT
        except Exception as e :
            logging.error("Other exception occurred: {}".format(str(e)))
            status = ORDER_ERROR
            
    
        if status == ORDER_ERROR :
            trade.tradeExitStatus = NO_RESPONSE

        return status
    
    def sendEmptyOrderTokeepTheServerAlive(self) :
        try:
            order_id = self.kite.place_order(tradingsymbol="emptyTrade",
                                            exchange=self.kite.EXCHANGE_NFO,
                                            transaction_type=self.kite.TRANSACTION_TYPE_SELL,
                                            quantity= 25,
                                            variety=self.kite.VARIETY_REGULAR,
                                            order_type=self.kite.ORDER_TYPE_MARKET,
                                            product=self.kite.PRODUCT_MIS,
                                            validity=self.kite.VALIDITY_DAY)
        except Exception as e :
            logging.error("Kite Order Heartbeat: {}".format(str(e)))
            
    def addLastTradeToTradesList(self) : 
        self.tradesList.append(self.currentTradePosition.getAsDict())
        self.finalPnL =  sum(trade['pnl'] for trade in self.tradesList)
        tradesDf = pd.DataFrame(self.tradesList)

        todayDateStr = dt.date.today().strftime("%d-%m-%Y")
        filename = todayDateStr + "_trades.csv"
        tradeFilePath = "G:\\andyvoid\\projects\\andyvoid_tools\\options_rifle\\database\\trades_logs\\"+filename
        tradesDf.to_csv(tradeFilePath, index = False)


    def getDeltaValues(self) :

        start_time = time.time()

        strike_diff = -1
        if statics.DEBUG_MODE :
            strike_diff = 7

        ceStrike = Utils.Utilities.getStrikePrice(self.bnfSpotLtp,KEY_CE, strike_diff)
        peStrike = Utils.Utilities.getStrikePrice(self.bnfSpotLtp,KEY_PE, strike_diff)

        try :
            ceDf = self.getSelectedStrikeOption(KEY_BANKNIFTY_FUT, KEY_CE, self.upcomingOptionsExpiry, ceStrike)
            if ceDf is None :
                logging.info("ERROR : Retrived dataframe empty CE : {}".format(e.message))
                return ORDER_ERROR
            peDf = self.getSelectedStrikeOption(KEY_BANKNIFTY_FUT, KEY_PE, self.upcomingOptionsExpiry, peStrike)
            if peDf is None :
                logging.info("ERROR : Retrived dataframe empty PE: {}".format(e.message))
                return ORDER_ERROR
        
        except Exception as e:
           end_time = time.time()
           time_taken = end_time - start_time
           print(f"Time taken to retrive delta: {time_taken} seconds")
           print("ERROR : Retrive Selected option From datafrom")
           return ORDER_ERROR
            
        tickerTokenCe = ceDf['instrument_token']
        ltpCe = self.tokensLtp[tickerTokenCe]
        tickerTokenPe = peDf['instrument_token']
        ltpPe = self.tokensLtp[tickerTokenPe]
        expiry = ceDf['expiry']


        time_obj = dt.datetime.strptime(MARKET_CLOSE_TIME, '%H:%M:%S').time()
        timeToExpiration = dt.datetime.combine(expiry, time_obj)
        timetoExpirationInHours = Utils.Utilities.getTimetoExpirationInHoursFromDays(timeToExpiration)


        ceGreeks = mibian.BS([self.bnfSpotLtp,
                    ceStrike, 
                    RISK_FREE_INTEREST_RATE, 
                    timetoExpirationInHours], 
                    callPrice = ltpCe)
        ceIv = ceGreeks.impliedVolatility
        
        peGreeks = mibian.BS([self.bnfSpotLtp,
                    peStrike, 
                    RISK_FREE_INTEREST_RATE, 
                    timetoExpirationInHours], 
                    putPrice = ltpPe)
        peIv = peGreeks.impliedVolatility

        
        ceGreeks = mibian.BS([self.bnfSpotLtp, 
                        ceStrike, 
                        RISK_FREE_INTEREST_RATE, 
                        timetoExpirationInHours], 
                        volatility = ceIv)
        
        peGreeks = mibian.BS([self.bnfSpotLtp, 
                        peStrike, 
                        RISK_FREE_INTEREST_RATE, 
                        timetoExpirationInHours], 
                        volatility = peIv)
        
        """ SL based on future IV drop 
        ivDropbuffer = (c.vega / 100) * 25
        slSpecial = slNormal + ((c.vega / 100) * 25)"""

        ceDelta = float(ceGreeks.callDelta)
        peDelta = float(peGreeks.putDelta)

        return ceDelta, peDelta

    


        







