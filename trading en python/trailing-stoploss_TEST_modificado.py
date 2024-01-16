import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import time
import numpy as np

# Inicializar boost globalmente
boost = 0

# Retorna los valores de ATR
def atr(high, low, close, n=14):
    tr = np.amax(np.vstack(((high - low).to_numpy(), (abs(high - close)).to_numpy(), (abs(low - close)).to_numpy())).T, axis=1)
    return pd.Series(tr).rolling(n).mean().to_numpy()

# Función para trailing stop-loss
def trail_sl():
    global TICKET, boost  # Agrega esta línea para acceder a las variables globales

    # Obtener posición basada en el ticket_id
    position = mt5.positions_get(ticket=TICKET)

    # Verificar si la posición existe
    if position:
        position = position[0]
    elif direction != 'neutral':
        market_order(SYMBOL, VOLUME, direction)

    # Obtener datos de la posición
    order_type = position.type
    price_current = position.price_current
    price_open = position.price_open
    sl = position.sl
    boost = 0
    dist_from_sl = abs(round(price_current - sl, 5))

    if dist_from_sl > MAX_DIST_SL:
        # Calcular nuevo SL
        if sl != 0.0:
            if order_type == 0:  # 0 representa BUY
                new_sl = sl - (TRAIL_AMOUNT * 0.35)
                if price_current > price_open:
                    new_sl = sl + (TRAIL_AMOUNT * 2)
                    if boost == 0:
                        boost = 1
                        new_sl = new_sl + (TRAIL_AMOUNT * 5)
            elif order_type == 1:  # 1 representa SELL
                new_sl = sl + (TRAIL_AMOUNT * 0.35)
                if price_current < price_open:
                    new_sl = sl - (TRAIL_AMOUNT * 2)
                    if boost == 0:
                        boost = 1
                        new_sl = new_sl - (TRAIL_AMOUNT * 5)
        else:
            # Establecer SL predeterminado si no hay SL en el símbolo
            new_sl = price_open - DEFAULT_SL if order_type == 0 else price_open + DEFAULT_SL

        request = {
            'action': mt5.TRADE_ACTION_SLTP,
            'position': position.ticket,
            'sl': new_sl,
        }

        result = mt5.order_send(request)
        return result

# Función para enviar una orden de mercado
def market_order(symbol, volume, order_type, **kwargs):
    tick = mt5.symbol_info_tick(symbol)
    TAKEPROFIT = 80  # 600 para us100.cash
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
        "type": type_execution,
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

# Función para cerrar una orden basada en el ticket id
def close_order(ticket):
    positions = mt5.positions_get()

    for pos in positions:
        tick = mt5.symbol_info_tick(pos.symbol)
        type_dict = {0: 1, 1: 0}  # 0 representa buy, 1 representa sell - invertir order_type para cerrar la posición
        price_dict = {0: tick.ask, 1: tick.bid}
        type_execution = ""

        if pos.ticket == ticket:
            type_execution = mt5.ORDER_TYPE_BUY if pos.type == 0 else mt5.ORDER_TYPE_SELL  # Corregir la comparación del tipo de orden
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

# Función para obtener la exposición de un símbolo
def get_exposure(symbol):
    positions = mt5.positions_get(symbol=symbol)
    if positions:
        pos_df = pd.DataFrame(positions, columns=positions[0]._asdict().keys())
        exposure = pos_df['volume'].sum()

        return exposure

# Función para buscar señales de trading
def signal(symbol, timeframe, sma_period):
    bars = mt5.copy_rates_from_pos(symbol, timeframe, 1, sma_period)
    bars_df = pd.DataFrame(bars)
    last_close = bars_df.iloc[-1].close

    # Indicador de color de la vela
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

    c1g = c1o < c1c  # vela 1 verde
    c2g = c2o < c2c  # vela 2 verde
    c3g = c3o < c3c  # vela 3 verde
    c4g = c4o < c4c  # vela 4 verde
    c5g = c5o < c5c  # vela 5 verde
    c6g = c6o < c6c  # vela 6 verde
    c7g = c7o < c7c  # vela 7 verde

    c1r = c1o > c1c  # vela 1 roja
    c2r = c2o > c2c  # vela 2 roja
    c3r = c3o > c3c  # vela 3 roja
    c4r = c4o > c4c  # vela 4 roja
    c5r = c5o > c5c  # vela 5 roja
    c6r = c6o > c6c  # vela 6 roja
    c7r = c7o > c7c  # vela 7 roja

    c1d = c1o == c1c  # vela 1 doji
    c2d = c2o == c2c  # vela 2 doji
    c3d = c3o == c3c  # vela 3 doji
    c4d = c4o == c4c  # vela 4 doji
    c5d = c5o == c5c  # vela 5 doji
    c6d = c6o == c6c  # vela 6 doji
    c7d = c7o == c7c  # vela 7 doji

    # Evaluar señales de compra y venta basadas en patrones de velas
    if c5c > c6o and c5o < c6c:  # Engulfing alcista
        direction = 'buy'
        print("patrón alcista")  # alcista
    elif c5o > c6c and c5c < c6o:  # Engulfing bajista
        direction = 'sell'
        print("patrón bajista")  # bajista
    else:
        direction = 'neutral'
        print("No hay señal de entrada")  # neutral

    # Indicador SMA
    sma = bars_df.close.mean()

    return last_close, sma, direction


if __name__ == '__main__':
    # Parámetros de estrategia
    SYMBOL = "EURUSD"
    VOLUME = 1.0
    TIMEFRAME = mt5.TIMEFRAME_M1
    SMA_PERIOD = 10
    DEVIATION = 20
    MAX_DIST_SL = 0.00005  # Máxima distancia entre el precio actual y SL, de lo contrario, SL se actualizará
    TRAIL_AMOUNT = 0.000015  # Monto por el cual se actualiza SL
    DEFAULT_SL = 0.4  # Si la posición no tiene SL, establecer un SL predeterminado

    mt5.initialize(login=1051991621, server='FTMO-Demo', password='JBRawHggBI2*')

    while True:
        try:
            # Calcular exposición de la cuenta
            exposure = get_exposure(SYMBOL)

            # Calcular cierre de la última vela, media móvil simple y señal de trading
            last_close, sma, direction = signal(SYMBOL, TIMEFRAME, SMA_PERIOD)

            # Verificar si hay una señal y el número de posiciones abiertas es menor a 5
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

            # Recorrer las posiciones abiertas y aplicar trailing stop-loss
            for pos in mt5.positions_get():
                TICKET = pos.ticket
                trail_sl()

            # Actualizar cada 1 segundo
            time.sleep(1)

        except Exception as e:
            print(f'Error en el bucle principal: {e}')
