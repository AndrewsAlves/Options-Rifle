import datetime



EXECUTED = 1
PENDING = -1
CANCELLED = -2

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

    def __init__(self, entryOrderId, tickerToken, tradeType, stg, sym, qty, ltp, slPoints) :
       self.entryOrderId =  entryOrderId
       self.tickerToken = tickerToken
       self.tradeType = tradeType
       self.strategy = stg

       self.tickerSymbol = sym
       self.qty = qty
       self.stoplossPoints = slPoints
       self.stoplossPrice = ltp - slPoints
       self.riskAmount = self.qty*self.stoplossPrice

       self.unRealisedProfit = 0
       self.unRealisedProfitInPoints = 0
       self.tag = ""
       self.notes = ""

    def setStoploss(self, sl) :
        if self.tradeEntryStatus == EXECUTED :
            self.stoplossPrice = sl
            self.stoplossPoints = self.entryPrice - sl
            self.riskAmount = self.qty*self.stoplossPoints

    def updateTradeEntryStatus(self, status, executedPrice = 0) :
        self.tradeEntryStatus = status
        self.entryPrice = executedPrice
        if (status == EXECUTED) :
            self.tradeEntryTime = datetime.datetime.now()
    def updateTradeExitStatus(self, status, executedPrice = 0) :
        if (status == EXECUTED) :
            self.tradeExitTime = datetime.datetime.now()
        self.tradeExitStatus = status
        self.exitPrice = executedPrice
        self.realisedProfit = (executedPrice-self.entryPrice) * self.qty
        self.realisedProfitInPoints = executedPrice-self.entryPrice
    
    def updateLtp(self, ltp):
        self.ltp = ltp
        self.unRealisedProfit = (ltp-self.entryPrice) * self.qty
        self.unRealisedProfitInPoints = ltp-self.entryPrice

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

        return tradeDic







    



        