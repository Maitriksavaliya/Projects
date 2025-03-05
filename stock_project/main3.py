# Importing necessary libraries
import streamlit as st
import pandas as pd
import yfinance as yf
from matrix_calculator import calculation_matrix
from visualization import visual_graph

# Streamlit Dashboard App
class StockDashboardApp:
    def __init__(self):
        self.calc = calculation_matrix()
        self.visuals = visual_graph()

    def run(self):
        st.set_page_config(page_title="TradeViz - Stock Dashboard", layout="wide", page_icon="📈")
        st.sidebar.markdown("""
            # **TradeViz**
            ### Your Ultimate Stock Analysis Tool 📊
        """)

        # Stock Selection
        st.sidebar.subheader("Stock Selection")
        popular_ticker = ["AAPL", "GOOGL", "MSFT", "META", "NVDA"]
        new_ticker = st.sidebar.text_input("Input a new ticker:")
        if new_ticker:
            popular_ticker.append(new_ticker.upper())
            st.sidebar.success(f"Added {new_ticker.upper()} to the list")

        period = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "YTD", "max"]
        selected_time_range = st.sidebar.selectbox("Select period:", period, index=2)
        ticker = st.sidebar.selectbox("Select a ticker", popular_ticker, index=0)

        # Chart Options
        st.sidebar.subheader("Chart Options")
        show_candlestick_chart = st.sidebar.checkbox("Candlestick Chart", value=True)
        show_line_chart = st.sidebar.checkbox("Line Chart", value=False)

        # Stock Comparison
        st.sidebar.subheader("Stock Comparison")
        show_comparison = st.sidebar.checkbox("Compare Stocks", value=False)
        comp_ticker = []
        if show_comparison:
            comp_ticker = st.sidebar.multiselect("Select tickers to compare:", popular_ticker, default=[ticker, "GOOGL"])

        # Hide Technical Indicators if comparison is checked
        if not show_comparison:
            st.sidebar.subheader(f"Technical Indicators for {ticker}")
            show_moving_averages = st.sidebar.checkbox("Moving Averages", value=False)
            show_bollinger_bands = st.sidebar.checkbox("Bollinger Bands", value=False)
            show_rsi = st.sidebar.checkbox("Relative Strength Index (RSI)", value=False)
            show_macd = st.sidebar.checkbox("Moving Average Convergence Divergence (MACD)", value=False)
            show_atr = st.sidebar.checkbox("Average True Range (ATR)", value=False)
        else:
            # Ensure all indicators are reset when hiding
            show_moving_averages = show_bollinger_bands = show_rsi = show_macd = show_atr = False

        # Summary & Data Export
        st.sidebar.subheader("Summary & Data Export")
        show_summary = st.sidebar.checkbox("Show Summary", value=True)

        # Add Help Section
        st.sidebar.subheader("Help & User Guide")
        show_help = st.sidebar.toggle("Show Help Guide", value=False)

        # Load data from Yahoo Finance
        data = yf.download(ticker, period=selected_time_range)
        if data.empty:
            st.error("No data found for the selected ticker and time period.")
            return

        if show_comparison and comp_ticker:
            cdata = yf.download(comp_ticker, period=selected_time_range)

        # Page Title
        st.title(" vs ".join(comp_ticker) if show_comparison else f"{ticker}")

        if show_help:
            st.subheader("Help & User Guide")
            st.markdown("""
                ### How to Use This Dashboard:
                - **Select a Stock:** Use the sidebar to choose a stock ticker.
                - **Choose Time Period:** Pick a time range for stock data.
                - **Enable Charts:** Check "Candlestick Chart" or "Line Chart" to visualize stock prices.
                - **Compare Stocks:** Enable "Compare Stocks" to analyze multiple stocks.
                - **Use Technical Indicators:** Select indicators like RSI, MACD, etc. (Disabled in comparison mode).
                - **Export Data:** Download stock data in CSV format for further analysis.
                - **Navigate Tabs:** Tabs appear dynamically based on selected options.
            """)
            return 

        # Dynamically create the list of active tabs based on user selections
        tabs_list = []
        if show_candlestick_chart:
            tabs_list.append("Candlestick Chart")
        if show_line_chart:
            tabs_list.append("Line Chart")
        if not show_comparison and (show_moving_averages or show_bollinger_bands or show_rsi or show_macd or show_atr):
            tabs_list.append("Technical Indicators")
        tabs_list.append("Summary & Data")  # Always include summary

        # Create the tabs dynamically
        tabs = st.tabs(tabs_list)

        # Track the index of each tab
        tab_index = 0

        # Tab: Candlestick Chart
        if show_candlestick_chart:
            with tabs[tab_index]:
                st.subheader("Candlestick Chart")
                if show_comparison and comp_ticker:
                    for ticker in comp_ticker:
                        ticker_data = yf.download(ticker, period=selected_time_range)
                        if not ticker_data.empty:
                            st.write(f"### {ticker}")
                            candlestick_fig = self.visuals.plot_candlestick(ticker_data, ticker)
                            st.plotly_chart(candlestick_fig, use_container_width=True)
                        else:
                            st.error(f"No data available for {ticker}")
                else:
                    candlestick_fig = self.visuals.plot_candlestick(data, ticker)
                    st.plotly_chart(candlestick_fig, use_container_width=True)
            tab_index += 1

        # Tab: Line Chart
        if show_line_chart:
            with tabs[tab_index]:
                st.subheader("Line Chart")
                line_fig = self.visuals.plot_line_chart(cdata if show_comparison else data,
                                                        comp_ticker if show_comparison else ticker,
                                                        is_comparison=show_comparison)
                st.plotly_chart(line_fig, use_container_width=True)
            tab_index += 1

        # Tab: Technical Indicators (Only show if not comparing stocks)
        if not show_comparison and (show_moving_averages or show_bollinger_bands or show_rsi or show_macd or show_atr):
            with tabs[tab_index]:
                st.subheader("Technical Indicators")
                col1, col2 = st.columns(2)

                if show_moving_averages:
                    with col1:
                        st.write("### Moving Averages")
                        data = self.calc.moving_averages(data)
                        st.plotly_chart(self.visuals.plot_moving_averages(data), use_container_width=True)

                if show_bollinger_bands:
                    with col2:
                        st.write("### Bollinger Bands")
                        data = self.calc.bollinger_bands(data)
                        st.plotly_chart(self.visuals.plot_bollinger_bands(data), use_container_width=True)

                if show_rsi:
                    with col1:
                        st.write("### Relative Strength Index (RSI)")
                        data = self.calc.rsi(data)
                        st.plotly_chart(self.visuals.plot_rsi(data), use_container_width=True)

                if show_macd:
                    with col2:
                        st.write("### Moving Average Convergence Divergence (MACD)")
                        data = self.calc.macd(data)
                        st.plotly_chart(self.visuals.plot_macd(data), use_container_width=True)

                if show_atr:
                    st.write("### Average True Range (ATR)")
                    data = self.calc.atr(data)
                    st.plotly_chart(self.visuals.plot_atr(data), use_container_width=True)
            tab_index += 1

        # Tab: Summary & Data (Always visible)
        with tabs[tab_index]:
            st.subheader("Data Summary")
            if show_summary:
                st.write(cdata.describe() if show_comparison else data.describe())

            if show_comparison:
                st.subheader("Comparison Data")
                selected_data = cdata.loc[:, cdata.columns.get_level_values(1).isin(comp_ticker)]
                st.dataframe(selected_data)
                st.download_button(label=f"Download CSV for {', '.join(comp_ticker)}",
                                   data=selected_data.to_csv(index=True),
                                   file_name=f"{','.join(comp_ticker)}_data.csv",
                                   mime="text/csv")
            else:
                st.subheader(f"Download {ticker} Data")
                st.dataframe(data)
                st.download_button(label=f"Download CSV for {ticker}",
                                   data=data.to_csv(),
                                   file_name=f"{ticker}_data.csv",
                                   mime="text/csv")

# Run the app
if __name__ == "__main__":
    app = StockDashboardApp()
    app.run()
