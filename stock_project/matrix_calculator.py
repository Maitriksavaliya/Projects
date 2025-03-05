import pandas as pd
import numpy as np


class calculation_matrix:
    
    def moving_averages(self, stock_data):
        for window in [50, 200]:
            stock_data[f'SMA_{window}'] = stock_data['Close'].rolling(window=window, min_periods=0).mean()
        return stock_data

    def bollinger_bands(self, stock_data):
        window = 20
        rolling_mean = stock_data['Close'].rolling(window=window).mean()
        rolling_std = stock_data['Close'].rolling(window=window).std()
        stock_data['Bollinger High'] = rolling_mean + (rolling_std * 2)
        stock_data['Bollinger Low'] = rolling_mean - (rolling_std * 2)
        return stock_data
    
    def rsi(self, stock_data, window=14):
        delta = stock_data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).fillna(0)
        loss = (-delta.where(delta < 0, 0)).fillna(0)

        avg_gain = gain.rolling(window=window, min_periods=1).mean()
        avg_loss = loss.rolling(window=window, min_periods=1).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        stock_data['RSI'] = rsi
        return stock_data
    
    def macd(self, stock_data, slow=26, fast=12, signal=9):
        exp1 = stock_data['Close'].ewm(span=fast, adjust=False).mean()
        exp2 = stock_data['Close'].ewm(span=slow, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=signal, adjust=False).mean()

        stock_data['MACD'] = macd
        stock_data['Signal_Line'] = signal_line
        return stock_data
    
    def atr(self, stock_data, window=14):
        high_low = stock_data['High'] - stock_data['Low']
        high_close = np.abs(stock_data['High'] - stock_data['Close'].shift())
        low_close = np.abs(stock_data['Low'] - stock_data['Close'].shift())

        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        atr = true_range.rolling(window=window).mean()
        stock_data['ATR'] = atr
        return stock_data