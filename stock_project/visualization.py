from turtle import title
import plotly.graph_objects as go
import pandas as pd

class visual_graph:

    def plot_moving_averages(self, stock_data):
        ma_fig = go.Figure()
        for window in [50, 200]:
            ma_fig.add_trace(go.Scatter(
                x=stock_data.index,
                y=stock_data[f'SMA_{window}'],
                name=f'SMA {window}',
                mode='lines'
            ))
        ma_fig.update_layout(title="Moving Averages (MA)", xaxis_title="Date", yaxis_title="MA",
        template="plotly_dark")
        return ma_fig

    def plot_bollinger_bands(self, stock_data):
        bb_fig = go.Figure()
        bb_fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Bollinger High'], fill=None, mode='lines', name='Bollinger High'))
        bb_fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], fill='tonexty', mode='lines', name='Close'))
        bb_fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Bollinger Low'], fill='tonexty', mode='lines', name='Bollinger Low'))
        bb_fig.update_layout(title="Boillinger_Bands(BB)", xaxis_title="Date",
        template="plotly_dark")
        return bb_fig

    def plot_rsi(self, stock_data):
        rsi_fig = go.Figure()
        rsi_fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['RSI'], name='RSI'))
        rsi_fig.update_layout(title="Relative Strength Index (RSI)", xaxis_title="Date", yaxis_title="RSI",
        template="plotly_dark")
        return rsi_fig

    def plot_macd(self, stock_data):
        macd_fig = go.Figure()
        macd_fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['MACD'], name='MACD Line'))
        macd_fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Signal_Line'], name='Signal Line'))
        macd_fig.update_layout(title="Moving Average Convergence Divergence (MACD)", xaxis_title="Date", yaxis_title="MACD",
        template="plotly_dark")
        return macd_fig

    def plot_atr(self, stock_data):
        atr_fig = go.Figure()
        atr_fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['ATR'], name='ATR'))
        atr_fig.update_layout(title="Average True Range (ATR)", xaxis_title="Date", yaxis_title="ATR",
        template="plotly_dark")
        return atr_fig

    def plot_line_chart(self, stock_data, tickers,is_comparison=False):
        line_fig = go.Figure()
        if is_comparison:
            title= " vs ".join(tickers)
            for ticker in tickers:
                if ticker in stock_data['Close'].columns:
                    line_fig.add_trace(go.Scatter(
                        x=stock_data.index,
                        y=stock_data['Close'][ticker],
                        name=ticker,
                        mode='lines'
                    ))
        else:
            title=tickers
            if ('Close', tickers) not in stock_data.columns:
                print(f"Error: Missing Close price data for {tickers}")
                return go.Figure()
            stock_data = stock_data.xs(tickers, axis=1, level=1)  # Select only the specific ticker data
            stock_data.index = pd.to_datetime(stock_data.index)
            stock_data = stock_data[['Close']].dropna()
            line_fig.add_trace(go.Scatter(
            x=stock_data.index,
            y=stock_data['Close'],
            mode='lines',
            name=f'{tickers} Closing Price'
        ))

        line_fig.update_layout(title=f"{title} Line Chart",
        xaxis_title="Date",
        yaxis_title="Stock Price (USD)",
        legend_title="Stock",
        template="plotly_dark",
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x", )
        return line_fig

    def plot_candlestick(self, stock_data, ticker="AAPL"):
        required_columns = ['Open', 'High', 'Low', 'Close']
        for col in required_columns:
            if (col, ticker) not in stock_data.columns:
                print(f"Error: Missing {col} data for {ticker}")
                return go.Figure()
        stock_data = stock_data.xs(ticker, axis=1, level=1)  # Extract single ticker data
        stock_data.index = pd.to_datetime(stock_data.index)
        stock_data = stock_data[['Open', 'High', 'Low', 'Close']].dropna()
        candlestick_fig = go.Figure()
        candlestick_fig.add_trace(go.Candlestick(
            x=stock_data.index,
            open=stock_data['Open'],
            high=stock_data['High'],
            low=stock_data['Low'],
            close=stock_data['Close'],
            name=f'{ticker} Candlestick'
        ))

        candlestick_fig.update_layout(
            title=f"{ticker} Candlestick Chart",
            xaxis_title="Date",
            yaxis_title="Price",
            xaxis_rangeslider_visible=False,
        template="plotly_dark"
        )

        return candlestick_fig




