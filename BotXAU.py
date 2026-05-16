import MetaTrader5 as mt5
import time

def gestor_final_universal():
    if not mt5.initialize():
        print("Error al iniciar MT5")
        return

    print("--- VIGILANTE TOTAL ACTIVADO (ORO, FOREX, BTC) ---")
    
    ratio = 2.0

    try:
        while True:
            posiciones = mt5.positions_get()
            if posiciones:
                for pos in posiciones:
                    if pos.sl == 0.0:
                        symbol = pos.symbol
                        info = mt5.symbol_info(symbol)
                        if info is None: continue

                        precio = pos.price_open
                        punto = info.point
                        decimales = info.digits
                        ticket = pos.ticket

                        # AJUSTE DE DISTANCIA SEGÚN EL ACTIVO
                        if "BTC" in symbol:
                            # Para Bitcoin, 50,000 puntos es una distancia segura en Pepperstone
                            distancia = 50000 
                        elif "XAU" in symbol or "GOLD" in symbol:
                            distancia = 500 # 5 dólares en el Oro
                        else:
                            distancia = 300 # 30 pips en Forex

                        # Cálculo de niveles
                        if pos.type == mt5.ORDER_TYPE_BUY:
                            sl = round(precio - (distancia * punto), decimales)
                            tp = round(precio + (distancia * punto * ratio), decimales)
                        else:
                            sl = round(precio + (distancia * punto), decimales)
                            tp = round(precio - (distancia * punto * ratio), decimales)

                        request = {
                            "action": mt5.TRADE_ACTION_SLTP,
                            "symbol": symbol,
                            "position": ticket,
                            "sl": sl,
                            "tp": tp,
                        }

                        resultado = mt5.order_send(request)
                        
                        if resultado.retcode == mt5.TRADE_RETCODE_DONE:
                            print(f"Protección Exitosa en {symbol} | SL: {sl} TP: {tp}")
                        else:
                            print(f"Rechazado en {symbol}. Código: {resultado.retcode}")
                            print("Sugerencia: Abre el trade con el SL un poco más lejos manualmente.")

            time.sleep(1)
    except KeyboardInterrupt:
        print("Bot detenido.")
    finally:
        mt5.shutdown()

gestor_final_universal()
