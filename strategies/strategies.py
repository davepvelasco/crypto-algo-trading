import backtrader as bt
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA


class BaseStrategy(bt.Strategy):
    def notify_order(self, order):
        if order.status == order.Completed:
            order_type = "buy" if order.isbuy() else "sell"

            order_record = {
                "date": self.datas[0].datetime.date(0),
                "price": order.executed.price,
                "size": round(order.executed.size, 6),
                "value": order.executed.value,
                "order_type": order_type,
            }
            indicator_values = self.get_indicator_value()
            order_record.update(indicator_values)

            self.order_history.append(order_record)

    def get_indicator_value(self):
        return {}


class SMACStrategy(BaseStrategy):
    params = dict(fast_period=10, slow_period=30)

    def __init__(self):
        self.sma1 = bt.ind.SMA(period=self.p.fast_period)
        self.sma2 = bt.ind.SMA(period=self.p.slow_period)
        self.crossover = bt.ind.CrossOver(self.sma1, self.sma2)
        self.order_history = []

    def next(self):
        size = self.broker.get_cash() / self.data.close[0]
        if not self.position:
            if self.crossover > 0:
                self.buy(size=size)
        elif self.crossover < 0:
            self.close()

    def get_indicator_value(self):
        return {"sma_fast": round(self.sma1[0], 2), "sma_slow": round(self.sma2[0], 2)}


class RSIStrategy(BaseStrategy):
    params = dict(rsi_period=14, overbought=70, oversold=30)

    def __init__(self):
        self.rsi = bt.indicators.RSI(period=self.p.rsi_period)
        self.order_history = []

    def next(self):
        size = self.broker.get_cash() / self.data.close[0]
        if not self.position:
            if self.rsi[0] <= self.p.oversold:  # Buy when RSI ≤ 30
                self.buy(size=size)
        elif self.rsi[0] >= self.p.overbought:  # Sell when RSI ≥ 70
            self.close()

    def get_indicator_value(self):
        return {"rsi": round(self.rsi[0], 2)}


class ARIMAStrategy(BaseStrategy):
    params = dict(
        p=0, d=0, q=0, lookback=30, threshold=0.01, hold_period=5, look_ahead=5
    )

    def __init__(self):
        self.order_history = []
        self.current_forecast = None
        self.current_predicted_change = None
        self.last_trade_day = None

    def next(self):
        if len(self.data) < self.p.lookback:
            return  # Not enough data to train ARIMA

        # Prepare historical prices for ARIMA
        prices = pd.Series(self.data.close.get(size=self.p.lookback))

        # Create and fit the ARIMA model using p, d, q parameters
        model = ARIMA(prices, order=(self.p.p, self.p.d, self.p.q))
        model_fit = model.fit()

        # Forecast prices for the look-ahead period
        forecast = model_fit.forecast(steps=self.p.look_ahead)

        # Use the last forecasted price for percentage change
        self.current_forecast = forecast.iloc[-1]
        print(forecast)

        # Compute the percentage change over the look-ahead period
        price_today = self.data.close[0]
        self.current_predicted_change = (
            self.current_forecast - price_today
        ) / price_today

        # Enforce holding period only if a trade has occurred
        size = self.broker.get_cash() / price_today
        if self.last_trade_day is not None:
            days_since_last_trade = (
                self.data.datetime.date(0) - self.last_trade_day
            ).days
            if days_since_last_trade < self.p.hold_period:
                return

        # Buy if prediction is above threshold, sell if otherwise
        if not self.position:
            if self.current_predicted_change > self.p.threshold:
                self.buy(size=size)
                self.last_trade_day = self.data.datetime.date(0)
        elif self.current_predicted_change < -self.p.threshold:
            self.close()
            self.last_trade_day = self.data.datetime.date(0)

    def get_indicator_value(self):
        return {
            "forecast": self.current_forecast,
            "predicted_change": self.current_predicted_change,
        }
