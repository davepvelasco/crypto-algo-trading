import backtrader as bt
import pandas as pd


class CommInfoFractional(bt.CommissionInfo):
    def getsize(self, price, cash):
        """Returns fractional size instead of rounding."""
        return self.p.leverage * (cash / price)


def backtest(data, initial_balance, strategy_class, strategy_inputs):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(strategy_class, **strategy_inputs)
    cerebro.broker.addcommissioninfo(CommInfoFractional())
    cerebro.adddata(data)
    cerebro.broker.set_cash(initial_balance)
    cerebro.broker.set_coc(True)

    # Run Backtest
    results = cerebro.run()
    strategy_instance = results[0]

    # Conver order history to a dataframe
    order_history_df = pd.DataFrame(strategy_instance.order_history)

    # Store Final Value
    final_value = cerebro.broker.getvalue()
    profit = final_value - initial_balance

    return order_history_df, profit, final_value
