# MT5 Automatic Risk Manager Bot 

A Python-based trading utility designed to automatically manage risk parameters (Stop Loss and Take Profit) for open positions in **MetaTrader 5 (MT5)**. It acts as a background monitor that protects raw orders executed in the market.

##  Features & Logic Breakdown

- **Active Monitoring Loop**: Runs an infinite `while True` loop scanning open orders every 1 second (`time.sleep(1)`) to guarantee fast execution without memory leaks.
- **Automated Protection Filter**: Target positions are filtered via `if pos.sl == 0.0`. It only modifies open trades that lack a predefined Stop Loss.
- **Asset-Specific Scaled Distances**: Adjusts point distances dynamically depending on the asset volatility:
  - **Bitcoin (BTC)**: Applies a safe 50,000 point distance buffer (optimized for brokers like Pepperstone).
  - **Gold (GOLD/XAU)**: Tailored 500 point risk adjustment ($5 move on Gold).
  - **Forex**: Uses a default 300 point parameter (equivalent to 30 pips on standard currency pairs).
- **Dynamic Reward-to-Risk Ratio**: Automatically calculates TP based on a pre-defined risk multiplier ratio (`ratio = 2.0`) to target a 1:2 Risk/Reward execution.
- **Order Execution**: Uses the native `mt5.TRADE_ACTION_SLTP` structure via `mt5.order_send` to update levels directly on the broker's server.
- **Safe System Shutdown**: Includes a `try-finally` block ensuring `mt5.shutdown()` executes if the user interrupts the script (`Ctrl + C`), preventing ghost background processes.

## Tech Stack & Requirements

- **Language**: Python 3.x
- **Libraries**: `MetaTrader5`, `time`
- **Trading Platform**: MetaTrader 5 Terminal (Windows environment required).

##  How to Run

1. Open your MetaTrader 5 terminal and ensure **Algo Trading** is enabled.
2. Install the official library wrapper in your terminal:
   ```bash
   pip install MetaTrader5
   ```
3. Run the script:
   ```bash
   python BotXAU.py
   ```

---
*Disclaimer: This project was created for educational and portfolio presentation purposes. Always test algorithmic execution on demo accounts before risking live capital.*
