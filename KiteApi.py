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

logging.basicConfig(level=logging.DEBUG)

class KiteApi() :
    __instance = None

    def __init__(self) : 
        self.ticker = None
        self.executionRaceLock = threading.Lock()

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

    def enterTrade(self, trade : Trade) :

        status = statics.ORDER_ERROR
        start_time = time.time()
        self.executionRaceLock.acquire() 

        # Place an order
        try:
            trade.tradeEntryStatus = statics.INITIATED
            order_id = self.kite.place_order(tradingsymbol= trade.tickerSymbol,
                                        exchange=self.kite.EXCHANGE_NFO,
                                        transaction_type=self.kite.TRANSACTION_TYPE_BUY,
                                        quantity= trade.qty,
                                        variety=self.kite.VARIETY_REGULAR,
                                        order_type=self.kite.ORDER_TYPE_MARKET,
                                        product=self.kite.PRODUCT_MIS,
                                        validity=self.kite.VALIDITY_DAY)
           
            trade.entryOrderId = order_id

            status = statics.ORDER_PLACED
            logging.info("Order placed. ID is: {}".format(order_id))

        except kiteconnect.exceptions.TokenException as e:
            status = statics.ORDER_ERROR
            logging.error("TokenException occurred: {}".format(str(e)))
        except kiteconnect.exceptions.InputException as e:
            status = statics.ORDER_ERROR
            logging.error("InputException occurred: {}".format(str(e)))
        except kiteconnect.exceptions.OrderException as e:
            status = statics.ORDER_ERROR
            print("Order placement failed. Reason:", e.message)
        except kiteconnect.exceptions.NetworkException as e:
            status = statics.ORDER_ERROR
            logging.error("NetworkException occurred: {}".format(str(e)))
        except kiteconnect.exceptions.GeneralException as e:
            status = statics.ORDER_ERROR
            logging.error("GeneralException occurred: {}".format(str(e)))
        except ReadTimeout as e:
            status = statics.ORDER_ERROR_READ_TIMEOUT
        except Exception as e :
            logging.error("Other exception occurred: {}".format(str(e)))
            status = statics.ORDER_ERROR

        self.executionRaceLock.release() 
        end_time = time.time()
        time_taken = end_time - start_time

        if status == statics.ORDER_ERROR : 
            trade.tradeEntryStatus = statics.NO_RESPONSE

        print(f">>> Time taken to place Entry order: {time_taken} seconds")
        return status


    def exitCurrentPosition(self, trade :Trade) :
        # Place an order

        status = statics.ORDER_ERROR

        try:
            trade.tradeExitStatus = statics.INITIATED
            order_id = self.kite.place_order(tradingsymbol=trade.tickerSymbol,
                                        exchange=self.kite.EXCHANGE_NFO,
                                        transaction_type=self.kite.TRANSACTION_TYPE_SELL,
                                        quantity= trade.qty,
                                        variety=self.kite.VARIETY_REGULAR,
                                        order_type=self.kite.ORDER_TYPE_MARKET,
                                        product=self.kite.PRODUCT_MIS,
                                        validity=self.kite.VALIDITY_DAY)
            

            logging.info("Order placed. ID is: {}".format(order_id))

            return statics.ORDER_PLACED 
        except kiteconnect.exceptions.TokenException as e:
            logging.error("TokenException occurred: {}".format(str(e)))
            status = statics.ORDER_ERROR 
        except kiteconnect.exceptions.InputException as e:
            logging.error("InputException occurred: {}".format(str(e)))
            status = statics.ORDER_ERROR 
        except kiteconnect.exceptions.OrderException as e:
            print("Order placement failed. Reason:", e.message)
            status = statics.ORDER_ERROR 
        except kiteconnect.exceptions.NetworkException as e:
            logging.error("NetworkException occurred: {}".format(str(e)))
            status = statics.ORDER_ERROR 
        except kiteconnect.exceptions.GeneralException as e:
            logging.error("GeneralException occurred: {}".format(str(e)))
            status = statics.ORDER_ERROR 
        except ReadTimeout as e:
            status = statics.ORDER_ERROR_READ_TIMEOUT
        except Exception as e :
            logging.error("Other exception occurred: {}".format(str(e)))
            status = statics.ORDER_ERROR
            
        if status == statics.ORDER_ERROR :
            trade.tradeExitStatus = statics.NO_RESPONSE

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
            

    """def getDeltaValues(self) :

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
        
        SL based on future IV drop 
        ivDropbuffer = (c.vega / 100) * 25
        slSpecial = slNormal + ((c.vega / 100) * 25)

        ceDelta = float(ceGreeks.callDelta)
        peDelta = float(peGreeks.putDelta)

        return ceDelta, peDelta"""
    
    

    


        







