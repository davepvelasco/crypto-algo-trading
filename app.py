import json
from pathlib import Path

import backtrader as bt
import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

from backtest import backtest
from data_pipeline import CoinGeckoFetcher
from strategies import ARIMAStrategy, RSIStrategy, SMACStrategy

st.set_page_config(layout="wide")

# Define the file path to store the coin list
COINS_FILE = Path("coins.json")

# Check if the file exists
if COINS_FILE.exists():
    # ✅ Read from file
    with COINS_FILE.open("r") as file:
        coins_json = json.load(file)
        coins = [item.get("id") for item in coins_json]
else:
    # ✅ Fetch from CoinGecko API
    response = requests.get("https://api.coingecko.com/api/v3/coins/list")
    if response.status_code == 200:
        coins_json = response.json()
        coins = [item.get("id") for item in coins_json]

        # ✅ Save to file for future use
        with COINS_FILE.open("w") as file:
            json.dump(coins_json, file, indent=4)
    else:
        raise Exception("Failed to fetch coins from CoinGecko API")

STRATEGY_MAP = {
    "ARIMA Strategy": ARIMAStrategy,
    "SMAC Strategy": SMACStrategy,
    "RSI Strategy": RSIStrategy,
}


def plot_candlestick(df, order_history_df, title):
    fig = go.Figure()

    # Candlestick Chart
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name="Candlestick",
        )
    )

    if not order_history_df.empty:
        # Buy/Sell Signals
        buy_signals = order_history_df[order_history_df["order_type"] == "buy"]
        sell_signals = order_history_df[order_history_df["order_type"] == "sell"]

        # Buy Markers
        fig.add_trace(
            go.Scatter(
                x=buy_signals["date"],
                y=buy_signals["price"],
                mode="markers",
                marker=dict(symbol="triangle-up", color="green", size=10),
                name="Buy Signal",
            )
        )

        # Sell Markers
        fig.add_trace(
            go.Scatter(
                x=sell_signals["date"],
                y=sell_signals["price"],
                mode="markers",
                marker=dict(symbol="triangle-down", color="red", size=10),
                name="Sell Signal",
            )
        )

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark",
        height=700,
    )

    return fig


def get_strategy_params(strategy_class):
    if strategy_class == SMACStrategy:
        return dict(fast_period=10, slow_period=30)
    if strategy_class == RSIStrategy:
        return dict(rsi_period=14, overbought=70, oversold=30)
    if strategy_class == ARIMAStrategy:
        return dict(
            p=0,
            d=0,
            q=0,
            look_ahead=5,
            lookback=30,
            threshold=0.01,
            hold_period=5,
        )


def create_sidebar_inputs(params):
    user_inputs = {}
    for param_name, default_value in params.items():
        # Sliders for ARIMA
        if param_name in ["p", "d", "q"]:
            user_inputs[param_name] = st.sidebar.slider(
                f"ARIMA {param_name.upper()} (Order)",
                min_value=0,
                max_value=5,
                value=default_value,
            )
        elif isinstance(default_value, int):
            user_inputs[param_name] = st.sidebar.slider(
                f"{param_name.replace('_', ' ').capitalize()}",
                min_value=1,
                max_value=100,
                value=default_value,
            )
        elif isinstance(default_value, float):
            user_inputs[param_name] = st.sidebar.slider(
                f"{param_name.replace('_', ' ').capitalize()}",
                min_value=0.0,
                max_value=1.0,
                value=default_value,
                step=0.01,
            )
        else:
            user_inputs[param_name] = st.sidebar.text_input(
                f"{param_name.replace('_', ' ').capitalize()}", value=str(default_value)
            )
    return user_inputs


st.title("Crypto Trading Strategy Dashboard")

st.sidebar.subheader("Settings")
coin = st.sidebar.selectbox(
    "Select Cryptocurrency", coins, index=coins.index("bitcoin")
)
days = st.sidebar.slider("Select Days", min_value=30, max_value=365, value=180)
initial_balance = st.sidebar.slider(
    "Select Balance", min_value=100, max_value=100000, value=10000
)

strategy_name = st.sidebar.selectbox("Select Strategy", STRATEGY_MAP.keys())
strategy_class = STRATEGY_MAP.get(strategy_name)
if strategy_class:
    strategy_params = get_strategy_params(strategy_class)
    strategy_inputs = create_sidebar_inputs(strategy_params)


if st.sidebar.button("Backtest"):
    with st.spinner("Fetching data and running backtest..."):
        df = CoinGeckoFetcher.fetch_historical_data(coin_id=coin, days=days)
        df["open"], df["high"], df["low"], df["close"] = (
            df["price"],
            df["price"],
            df["price"],
            df["price"],
        )
        df["open"] = df["open"].shift(1)
        df = df.dropna()
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df.set_index("timestamp", inplace=True)

        data = bt.feeds.PandasData(dataname=df)
        order_history_df, profit, final_value = backtest(
            data=data,
            initial_balance=initial_balance,
            strategy_class=strategy_class,
            strategy_inputs=strategy_inputs,
        )

    # Show Candlestick Chart
    st.plotly_chart(
        plot_candlestick(df, order_history_df, f"{coin.upper()} Trading Signals"),
        use_container_width=True,
    )

    # Results
    st.subheader("Backtest Results")
    st.write(f"**Profit:** ${profit}")
    st.write(order_history_df)
