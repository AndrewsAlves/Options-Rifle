import datetime
import KiteApi

EXECUTED = 1
PENDING = -1
CANCELLED = -2
REJECTED = -3
NO_RESPONSE = 0
NOT_INITIATED = -4
INITIATED = -5

KEY_LONG = "long"
KEY_SHORT = "short"

KEY_CE = "CE"
KEY_PE = "PE"

class Trade() :

    """
    trade id = tradeId
    tradeType = Long or short, "tradeType"
    strategy = AT,DT,BT
    tradeEntryStatus = Pending, Executed or cancelled
    tradeExitStatus = pending, executed or cancelled

    tickersymbol 
    Qty
    entry price 
    exit price 
    Ltp 
    Sl
    Risk amount
    risk In Points
    P/L in amount
    P/L in points

    Tag
    Notes

    """

    def __init__(self, tickerToken, tradeType, stg, sym, qty, ltp, slPoints, strike) :
       self.tradeEntryStatus = NOT_INITIATED
       self.tradeExitStatus = NOT_INITIATED
       self.entryOrderId =  0
       self.exitOrderId = 0
       self.tickerToken = tickerToken
       self.tradeType = tradeType
       self.strategy = stg

       ce_or_pe = KEY_CE if tradeType != KEY_SHORT else KEY_PE
       self.strikeStr = str(strike) + " " + ce_or_pe
       self.tickerSymbol = sym
       self.qty = qty
       self.ltp = ltp
       self.stoplossPoints = slPoints
       self.stoplossPrice = int(ltp - slPoints)
       self.riskAmount = round(self.qty*self.stoplossPoints,2)

       self.ltp = ltp


       self.entryPrice = 0
       self.exitPrice = 0
       self.unRealisedProfit = 0
       self.unRealisedProfitInPoints = 0
       self.tag = ""
       self.notes = ""
       


    def setStoploss(self, sl) :
        if self.tradeEntryStatus == EXECUTED :
            if sl < 1 : sl = 0
            self.stoplossPrice = sl
            self.stoplossPoints = self.entryPrice - sl
            self.riskAmount = round(self.qty*self.stoplossPoints,2)

    def updateTradeEntryStatus(self, status, executedPrice = 0) :
        self.tradeEntryStatus = status
        if (status == EXECUTED) :
            self.tradeEntryTime = datetime.datetime.now()
            self.entryPrice = executedPrice

    def updateTradeExitStatus(self, status, executedPrice = 0) :
        if (status == EXECUTED) :
            self.tradeExitTime = datetime.datetime.now()
            self.exitPrice = executedPrice
            self.realisedProfit = round((executedPrice-self.entryPrice) * self.qty,2)
            self.realisedProfitInPoints = executedPrice-self.entryPrice
        self.tradeExitStatus = status
        
        
    def updateLtp(self, ltp):
        self.ltp = ltp
        self.unRealisedProfit = round((ltp - self.entryPrice) * self.qty,2)
        self.unRealisedProfitInPoints = round(ltp - self.entryPrice, 1)

    def incrementSl(self) :
        self.stoplossPrice += 1
        self.setStoploss(self.stoplossPrice)
        
    def decrementSl(self) :
        self.stoplossPrice -= 1
        self.setStoploss(self.stoplossPrice)

    def getAsDict(self) :

        """
        KEYS 

        ticker_token
        trade_type
        strategy
        ticker_symbol
        qty
        entry_time
        entry_price
        exit_time
        exit_price
        pnl
        tag
        notes
        """

        tradeDic = {}
        tradeDic['ticker_token'] = self.tickerToken
        tradeDic['trade_type'] = self.tradeType
        tradeDic['strategy'] = self.strategy
        tradeDic['ticker_symbol'] = self.tickerSymbol
        tradeDic['qty'] = self.qty
        tradeDic['entry_time'] = self.tradeEntryTime
        tradeDic['entry_price'] = self.entryPrice
        tradeDic['exit_time'] = self.tradeExitTime
        tradeDic['exit_price'] = self.exitPrice
        tradeDic['pnl'] = self.realisedProfit
        tradeDic['tag'] = self.tag
        tradeDic['notes'] = self.notes
        tradeDic['debug'] = KiteApi.DEBUG_MODE

        return tradeDic







    



        