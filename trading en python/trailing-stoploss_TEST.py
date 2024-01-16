"""
Author: TraderPy
Link: https://www.youtube.com/channel/UC9xYCyyR_G3LIuJ_LlTiEVQ

Risk Disclaimer:
Trading the financial markets imposes a risk of financial loss.
TraderPy is not responsible for any financial losses that viewers suffer.
Content is educational only and does not serve as financial advice.
Information or material is provided ‘as is’ without any warranty.
"""

# Simple Moving Average Crossover Strategy

import MetaTrader5 as mt5  # install using 'pip install MetaTrader5'
import pandas as pd  # install using 'pip install pandas'
from datetime import datetime
import time
from ta.momentum import RSIIndicator
import numpy as np

# Returns ATR values
def atr(high, low, close, n=14):
    tr = np.amax(np.vstack(((high - low).to_numpy(), 
    (abs(high - close)).to_numpy(), 
    (abs(low - close)).to_numpy())).T, 
    axis=1)
    return pd.Series(tr).rolling(n).mean().to_numpy()

# function to trail SL
def trail_sl():
    # get position based on ticket_id
    position = mt5.positions_get(ticket=TICKET)

    # check if position exists
    if position:
        position = position[0]
    elif direction != 'neutral':
        market_order(SYMBOL, VOLUME, direction)

    # get position data
    order_type = position.type     
    price_current = position.price_current
    price_open = position.price_open
    sl = position.sl
    boost = 0
    dist_from_sl = abs(round(price_current - sl, 5))

    if dist_from_sl > MAX_DIST_SL:
        # calculating new sl
        if sl != 0.0:
            if order_type == 0:  # 0 stands for BUY
                new_sl = sl - (TRAIL_AMOUNT * 0.35)
                if  price_current > price_open:
                    new_sl = sl + (TRAIL_AMOUNT * 2) 
                    if boost == 0:
                        boost == 1
                        new_sl = new_sl + (TRAIL_AMOUNT * 5)
            elif order_type == 1:  # 1 stands for SELL
                new_sl = sl + (TRAIL_AMOUNT * 0.35)
                if  price_current < price_open:
                    new_sl = sl - (TRAIL_AMOUNT * 2)
                    if boost == 0:
                        boost == 1
                        new_sl = new_sl - (TRAIL_AMOUNT * 5)               
        else:
            # setting default SL if the is no SL on the symbol
            new_sl = price_open - DEFAULT_SL if order_type == 0 else price_open + DEFAULT_SL

        request = {
            'action': mt5.TRADE_ACTION_SLTP,
            'position': position.ticket,
            'sl': new_sl,
        }

        result = mt5.order_send(request)
        return result
        
# function to send a market order
def market_order(symbol, volume, order_type, **kwargs):
    tick = mt5.symbol_info_tick(symbol)
    TAKEPROFIT = 80 #600 para us100.cash
    STOPLOSS = 40
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).ask
    type_execution = ""
    if order_type == "buy":
        tp = price+TAKEPROFIT*point
        sl = price-STOPLOSS*point
        type_execution = mt5.ORDER_TYPE_BUY_STOP
    elif order_type == "sell":
        type_execution = mt5.ORDER_TYPE_SELL_STOP
        tp = price-TAKEPROFIT*point
        sl = price+STOPLOSS*point
    else:
        type_execution = "neutral"

    price_dict = {'buy': tick.ask, 'sell': tick.bid}

    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": volume,
        "type":  type_execution,
        "price": price_dict[order_type],
        "tp": tp,
        "sl": sl,
        "deviation": DEVIATION,
        "magic": 100,
        "comment": "python market order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    order_result = mt5.order_send(request)
    print(order_result)

    return order_result

# function to close an order base don ticket id
def close_order(ticket):
    positions = mt5.positions_get()

    for pos in positions:
        tick = mt5.symbol_info_tick(pos.symbol)
        type_dict = {0: 1, 1: 0}  # 0 represents buy, 1 represents sell - inverting order_type to close the position
        price_dict = {0: tick.ask, 1: tick.bid}
        type_execution = ""
        if type_dict == 0:
            type_execution = mt5.ORDER_TYPE_BUY_STOP
        elif type_dict == 1:
            type_execution = mt5.ORDER_TYPE_SELL_STOP
        else:
            type_execution = ""

        if pos.ticket == ticket:
            request = {
                "action": mt5.TRADE_ACTION_PENDING,
                "position": pos.ticket,
                "symbol": pos.symbol,
                "volume": pos.volume,
                "type": type_execution,
                "price": price_dict[pos.type],
                "deviation": DEVIATION,
                "magic": 100,
                "comment": "python close order",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

            order_result = mt5.order_send(request)
            print(order_result)

            return order_result

    return 'Ticket does not exist'


# function to get the exposure of a symbol
def get_exposure(symbol):
    positions = mt5.positions_get(symbol=symbol)
    if positions:
        pos_df = pd.DataFrame(positions, columns=positions[0]._asdict().keys())
        exposure = pos_df['volume'].sum()

        return exposure

# function to look for trading signals
def signal(symbol, timeframe, sma_period):
    bars = mt5.copy_rates_from_pos(symbol, timeframe, 1, sma_period)
    bars_df = pd.DataFrame(bars)
    last_close = bars_df.iloc[-1].close
    #Candle color indicator

    c1o = bars_df.iloc[-7].open
    c1c = bars_df.iloc[-7].close
    c2o = bars_df.iloc[-6].open
    c2c = bars_df.iloc[-6].close
    c3o = bars_df.iloc[-5].open
    c3c = bars_df.iloc[-5].close
    c4o = bars_df.iloc[-4].open
    c4c = bars_df.iloc[-4].close
    c5o = bars_df.iloc[-3].open
    c5c = bars_df.iloc[-3].close
    c6o = bars_df.iloc[-2].open
    c6c = bars_df.iloc[-2].close
    c7o = bars_df.iloc[-1].open
    c7c = bars_df.iloc[-1].close
    
    c1g = c1o < c1c # candle 1 Green
    c2g = c2o < c2c # candle 2 Green
    c3g = c3o < c3c # candle 3 Green
    c4g = c4o < c4c # candle 4 Green
    c5g = c5o < c5c # candle 5 Green
    c6g = c6o < c6c # candle 6 Green
    c7g = c7o < c7c # candle 7 Green

    c1r = c1o > c1c # candle 1 Red
    c2r = c2o > c2c # candle 2 Red
    c3r = c3o > c3c # candle 3 Red
    c4r = c4o > c4c # candle 4 Red
    c5r = c5o > c5c # candle 5 Red
    c6r = c6o > c6c # candle 6 Red
    c7r = c7o > c7c # candle 7 Red

    c1d = c1o == c1c # candle 1 Doji
    c2d = c2o == c2c # candle 2 Doji
    c3d = c3o == c3c # candle 3 Doji
    c4d = c4o == c4c # candle 4 Doji
    c5d = c5o == c5c # candle 5 Doji
    c6d = c6o == c6c # candle 6 Doji
    c7d = c7o == c7c # candle 7 Doji

    BUET = c5c > c6o and c5o < c6c # Bullish Engulfing 
    BEET = c5o > c6c and c5c < c6o # Bearish Engulfing
    PIPT = c5o > c6c and c5c > c6o # Piercing Pattern
    DCCT = c5c < c6o and c5o < c6c # Dark Cloud Cover
    BUHT = c5o > c6c and c5c < c6o # Bullish Harami
    BEHT = c5c > c6o and c5o < c6c # Bearish Harami
    BUKT = c5o == c6o                # Bullish Kicker
    BEKT = c5o == c6o                # Bearish Kicker
    MOST = c4c > c5c and c5c < c6o # Morning Star
    EVST = c4c < c5c and c5c > c6o # Evening Star
    BUABT = c4c > c5c and c5c < c6o # Bullish Abandoned Baby
    BEABT = c4c < c5c and c5c > c6o # Bearish Abandoned Baby
    BUTST = c3c > c4c and c4o > c5c and c5c < c6o # Bullish Tri Star
    BETST = c3c < c4c and c4o < c5c and c5c > c6o # Bearish Tri Star
    TWST = c4o < c5o and c5o < c6o and c4c < c5c and c5c < c6c # Three White Soldiers
    TBCT = c4o > c5o and c5o > c6o and c4c > c5c and c5c > c6c # Three Black Crows
    UGTCT = c4c < c5c and c5c > c6c and c5o < c6o # Upside Gap Two Crows
    TCT = c4c < c5c and c5c > c6c and c5o > c6o # Two Crows
    TIUT = c4c < c5o and c5o < c6o and c4o > c5c and c5c < c6c # Three Inside Up
    TIDT = c4c > c5o and c5o > c6o and c4o < c5c and c5c > c6c # Three Inside Down
    TOUT = c4c > c5o and c5o < c6o and c4o < c5c and c5c < c6c # Three Outside Up
    TODT = c4o > c5c and c5c > c6c and c4c < c5o and c5o > c6o # Three Outside Down
    BUMLT = c5c == c6c # Bullish Meeting Line
    BEMLT = c5c == c6c # Bearish Meeting Line
    TSITST = c4c == c5c and c5c > c6c # Three Stars In The South
    ABT = c4o < c5o and c5o < c6o and c4c < c5c and c5c < c6c # Advance Block
    BUSST = c4c < c5o and c5o > c6c and c4o < c5c and c5c < c6o # Bullish Stick Sandwich
    BESST = c4o > c5c and c5c > c6o and c4c > c5o and c5o < c6c # Bearish Stick Sandwich
    MLT = c5c == c6c # Matching Low
    MHT = c5c == c6c # Matching High
    TBT = c5c < c6o and c5o > c6c # Tweezer Bottom
    TTT = c5o < c6c and c5c > c6o # Tweezer Top
    BUBT = c2c > c3o and c3c > c4c and c4c > c5c and c5c < c6o and c3o > c4o and c4o > c5o and c5o < c6c # Bullish Breakaway
    BEBT = c2c < c3o and c3o < c4o and c4o < c5o and c5o > c6c and c3c < c4c and c4c < c5c and c5c > c6o # Bearish Breakaway
    DTGT = c4c > c5o and c5c < c6o and c5o < c6c # Downside Tasuki Gap
    UTGT = c4c < c5o and c5o > c6c and c5c > c6o # Upside Tasuki Gap
    FTMT = c2c < c3o and c3o < c4o and c4o < c5o and c5o < c6c and c3c < c4c and c4c < c5c and c5c > c6o and c2o > c5c and c2c > c6c # Falling Three Method
    RTMT = c2c > c3o and c3o > c4o and c4o > c5o and c5c < c6o and c3c > c4c and c4c > c5c and c5c < c6o and c2o < c5c and c2c < c6c # Rising Three Method
    BESLT = c5o == c6o # Bearish Separating Lines 
    BUSLT = c5o == c6o # Bullish Separating Lines 
    BESBSWLT = c4c > c5c and c5o == c6o and c5c == c6c # Bearish Side By Side White Lines
    BUSBSWLT = c4c < c5o and c5o == c6o and c5c == c6c # Bullish Side By Side White Lines

    BUE = c4r and c5r and c6g and c7g and BUET # Bullish Engulfing 4 candles
    BEE = c4g and c5g and c6r and c7r and BEET # Bearish Engulfing 4 candles
    PIP = c4r and c5r and c6g and c7g and PIPT # Piercing Pattern 4 candles
    DCC = c4g and c5g and c6r and c7r and DCCT # Dark Cloud Cover 4 candles
    BUH = c4r and c5r and c6g and c7g and BUHT # Bullish Harami 4 candles
    BEH = c4g and c5g and c6r and c7r and BEHT # Bearish Harami 4 candles
    BUK = c4r and c5r and c6g and c7g and BUKT # Bullish Kicker 4 candles
    BEK = c4g and c5g and c6r and c7r and BEKT # Bearish Kicker 4 candles
    MOS = c3r and c4r and c5g and c6g and c7g and MOST # Morning Star 5 candles
    EVS = c3g and c4g and c5r and c6r and c7r and EVST # Evening Star 5 candles
    BUAB = c3r and c4r and c5d and c6g and c7g and BUABT # Bullish Abandoned Baby 5 candles
    BEAB = c3g and c4g and c5d and c6r and c7r and BEABT # Bearish Abandoned Baby 5 candles
    BUTS = c2r and c3r and c4d and c5d and c6d and c7g and BUTST # Bullish Tri Star 6 candles
    BETS = c2g and c3g and c4d and c5d and c6d and c7r and BETST # Bullish Tri Star 6 candles
    TWS = c3r and c4g and c5g and c6g and c7g and TWST # Three White Soldiers 5 candles
    TBC = c3g and c4r and c5r and c6r and c7r and TBCT # Three Black Crows 5 candles
    UGTC = c3g and c4g and c5r and c6r and c7r and UGTCT # Upside Gap Two Crows 5 candles
    TC = c3g and c4g and c5r and c6r and c7r and TCT # Two Crows 5 candles
    TIU = c3r and c4r and c5g and c6g and c7g and TIUT # Three Inside Up 5 candles
    TID = c3g and c4g and c5r and c6r and c7r and TIDT # Three Inside Down 5 candles
    TOU = c3r and c4r and c5g and c6g and c7g and TOUT # Three Outside Up 5 candles
    TOD = c3g and c4g and c5r and c6r and c7r and TODT # Three Inside Down 5 candles
    BUML = c4r and c5r and c6g and c7g and BUMLT # Bullish Meeting Line 4 candles
    BEML = c4g and c5g and c6r and c7r and BEMLT # Bearish Meeting Line 4 candles
    TSITS = c3r and c4r and c5r and c6r and c7g and TSITST # Three Stars In The South 5 candles
    AB = c3g and c4g and c5g and c6g and c7r and ABT # Advance Block 5 candles
    BUSS = c3r and c4r and c5g and c6r and c7g and BUSST # Bullish Stick Sandwich 5 candles
    BESS = c3g and c4g and c5r and c6g and c7r and BESST # Bearish Stick Sandwich 5 candles
    ML = c4r and c5r and c6r and c7g and MLT # Matching Low 4 candles
    MH = c4g and c5g and c6g and c7r and MHT # Matching High 4 candles
    TB = c4r and c5r and c6g and c7g and TBT # Tweezer Bottom 4 candles
    TT = c4g and c5g and c6r and c7r and TTT # Tweezer Top 4 candles
    BUB = c1r and c2r and c3r and c4r and c5r and c6g and c7g and BUBT # Bullish Breakaway 7 candles
    BEB = c1g and c2g and c3g and c4g and c5g and c6r and c7r and BEBT # Bearish Breakaway 7 candles
    DTG = c3r and c4r and c5r and c6g and c7r and DTGT # Downside Tasuki Gap 5 candles
    UTG = c3g and c4g and c5g and c6r and c7g and UTGT # Upside Tasuki Gap 5 candles
    FTM = c1r and c2r and c3g and c4g and c5g and c6r and c7r and FTMT # Falling Three Method 7 candles
    RTM = c1g and c2g and c3r and c4r and c5r and c6g and c7g and RTMT # Rising Three Method 7 candles
    BESL = c4r and c5g and c6r and c7r and BESLT # Bearish Separating Lines 4 candles
    BUSL = c4g and c5r and c6g and c7g and BUSLT # Bullish Separating Lines 4 candles
    BESBSWL = c3r and c4r and c5g and c6g and c7r and BESBSWLT # Bearish Side By Side White Lines 5 candles
    BUSBSWL = c3g and c4g and c5g and c6g and c7g and BUSBSWLT # Bullish Side By Side White Lines 5 candles

    if BUE or PIP or BUH or BUK or MOS or BUAB or BUTS or TWS or TIU or TOU or BUML or TSITS or BUSS or ML or TB or BUB or UTG or RTM or BUSL or BUSBSWL:
        color = 1
        print("patron alcista") # bullish
    elif BEE or DCC or BEH or BEK or EVS or BEAB or BETS or TBC or UGTC or TC or TID or TOD or BEML or AB or BESS or MH or TT or BEB or DTG or FTM or BESL or BESBSWL:
        color = -1
        print("patron bajista") # bearish
    else:
        color = 0
        print("No hay entrada") # neutral
    
    # SMA indicator
    sma = bars_df.close.mean()

    # RSI indicator
    RSII = RSIIndicator(bars_df["close"], window=30, fillna=True)
    RSI = RSII.rsi()

    #Fractals
    
    # Evaluate buy and sell signals based on RSI, SMA, ATR and Fractals
    direction = 'flat'

    for index, row in bars_df.iterrows():
        if color == 1 and sma > last_close:
            direction = 'buy'
        elif color == -1 and sma < last_close:
            direction = 'sell'
        else:
            direction = 'neutral'

    return last_close, sma, direction


if __name__ == '__main__':

    # strategy parameters
    SYMBOL = "EURUSD"
    VOLUME = 1.0
    TIMEFRAME = mt5.TIMEFRAME_M1
    SMA_PERIOD = 10
    DEVIATION = 20
    MAX_DIST_SL = 0.00005  # Max distance between current price and SL, otherwise SL will update
    TRAIL_AMOUNT = .000015  # Amount by how much SL updates
    DEFAULT_SL = .4  # If position has no SL, set a default SL

    mt5.initialize(login=1051991621, server='FTMO-Demo',password='JBRawHggBI2*')

    while True:
        # calculating account exposure
        exposure = get_exposure(SYMBOL)
         # calculating last candle close and simple moving average and checking for trading signal
        last_close, sma, direction = signal(SYMBOL, TIMEFRAME, SMA_PERIOD)
        if direction != 'neutral' and mt5.positions_total() < 5:
            market_order(SYMBOL, VOLUME, direction)
            print('time: ', datetime.now())
            print('last_close: ', last_close)
            print('sma: ', sma)
            print('signal: ', direction)
            print('-------\n')

        else:
            print('time: ', datetime.now())
            print('last_close: ', last_close)
            print('sma: ', sma)
            print('signal: ', direction)
            print('-------\n')
        for pos in mt5.positions_get():
            TICKET = pos.ticket
            trail_sl()
        # update every 1 second
        time.sleep(1)



