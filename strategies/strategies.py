import backtrader as bt


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
