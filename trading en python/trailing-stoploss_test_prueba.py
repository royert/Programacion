import MetaTrader5 as mt5  # instala usando 'pip install MetaTrader5'
import pandas as pd  # instala usando 'pip install pandas'
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

# función para trail SL
def trail_sl():
    # obtener posición basada en ticket_id
    position = mt5.positions_get(ticket=TICKET)

    # comprobar si la posición existe
    if position:
        position = position[0]
    elif direction != 'neutral':
        market_order(SYMBOL, VOLUME, direction)

    # obtener datos de la posición
    order_type = position.type     
    price_current = position.price_current
    price_open = position.price_open
    sl = position.sl
    boost = 0
    dist_from_sl = abs(round(price_current - sl, 5))

    if dist_from_sl > MAX_DIST_SL:
        # calcular nuevo SL
        if sl != 0.0:
            if order_type == 0:  # 0 significa BUY
                new_sl = sl - (TRAIL_AMOUNT * 0.35)
                if  price_current > price_open:
                    new_sl = sl + (TRAIL_AMOUNT * 2) 
                    if boost == 0:
                        boost == 1
                        new_sl = new_sl + (TRAIL_AMOUNT * 5)
            elif order_type == 1:  # 1 significa SELL
                new_sl = sl + (TRAIL_AMOUNT * 0.35)
                if  price_current < price_open:
                    new_sl = sl - (TRAIL_AMOUNT * 2)
                    if boost == 0:
                        boost == 1
                        new_sl = new_sl - (TRAIL_AMOUNT * 5)               
        else:
            # establecer SL predeterminado si no hay SL en el símbolo
            new_sl = price_open - DEFAULT_SL if order_type == 0 else price_open + DEFAULT_SL

        request = {
            'action': mt5.TRADE_ACTION_SLTP,
            'position': position.ticket,
            'sl': new_sl,
        }

        result = mt5.order_send(request)
        return result

# función para enviar una orden de mercado
def market_order(symbol, volume, order_type, **kwargs):
    tick = mt5.symbol_info_tick(symbol)
    TAKEPROFIT = 80
    STOPLOSS = 40
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).ask
    type_execution = ""
    if order_type == "buy":
        tp = price + TAKEPROFIT * point
        sl = price - STOPLOSS * point
        type_execution = mt5.ORDER_TYPE_BUY_STOP
    elif order_type == "sell":
        type_execution = mt5.ORDER_TYPE_SELL_STOP
        tp = price - TAKEPROFIT * point
        sl = price + STOPLOSS * point
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

# función para cerrar una orden basada en el ticket id
def close_order(ticket):
    positions = mt5.positions_get()

    for pos in positions:
        tick = mt5.symbol_info_tick(pos.symbol)
        type_dict = {0: 1, 1: 0}  # 0 representa buy, 1 representa sell - invirtiendo order_type para cerrar la posición
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

# función para obtener la exposición de un símbolo
def get_exposure(symbol):
    positions = mt5.positions_get(symbol=symbol)
    if positions:
        pos_df = pd.DataFrame(positions, columns=positions[0]._asdict().keys())
        exposure = pos_df['volume'].sum()

        return exposure

# función para buscar señales de trading
def signal(symbol, timeframe, sma_period):
    # ... (código existente)

    # calcular la dirección basada en los patrones de velas
    if BUE or PIP or BUH or BUK or MOS or BUAB or BUTS or TWS or TIU or TOU or BUML or TSITS or BUSS or ML or TB or BUB or UTG or RTM or BUSL or BUSBSWL:
        color = 1
        print("patron alcista")  # alcista
        # enviar un bloque de órdenes de compra
        orders = [-10, -20, -30]  # ajusta estos valores según tu estrategia
        send_order_block(symbol, VOLUME, "buy", orders)
    elif BEE or DCC or BEH or BEK or EVS or BEAB or BETS or TBC or UGTC or TC or TID or TOD or BEML or AB or BESS or MH or TT or BEB or DTG or FTM or BESL or BESBSWL:
        color = -1
        print("patron bajista")  # bajista
        # enviar un bloque de órdenes de venta
        orders = [10, 20, 30]  # ajusta estos valores según tu estrategia
        send_order_block(symbol, VOLUME, "sell", orders)
    else:
        color = 0
        print("No hay entrada")  # neutral

    # ... (código existente)

# función para enviar un bloque de órdenes pendientes
def send_order_block(symbol, volume, order_type, orders, **kwargs):
    tick = mt5.symbol_info_tick(symbol)
    point = mt5.symbol_info(symbol).point

    for i, price_offset in enumerate(orders):
        price = tick.ask if order_type == "buy" else tick.bid
        order_price = price + price_offset * point

        request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "price": order_price,
            "deviation": DEVIATION,
            "magic": 100,
            "comment": f"python pending order {i+1}",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        order_result = mt5.order_send(request)
        print(order_result)

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
    
    mt5.initialize(login=1052053155, server='FTMO-Demo',password='JBRawHggBI2*')

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
