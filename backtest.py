import pandas as pd
import requests


class Backtest:

    def __init__(self, alpha, beta, bal, window, timeframe):
        self.alpha = alpha.upper()  # long ticker symbol
        self.beta = beta.upper()  # hedge ticker symbol
        self.bal = bal  # current balance
        self.starting_bal = bal  # starting balance
        self.window = window  # rolling window i.e. MA
        self.timeframe = timeframe  # e.g. daily, weekly, monthly
        self.long = False
        self.shares = 0
        self.price_bought = 0
        self.data = pd.DataFrame()
        self.backtest(window)
        self.open = 0
        self.close = 0
        # lev = False

    # TODO: leverage without 3x ETF

    def read(self, alpha=None):
        print("reading...")
        if not alpha:
            alpha = self.alpha
        try:
            path = "data/" + alpha + "_" + self.timeframe + ".csv"
            print("path: ", path)
            self.data = pd.read_csv(path)
        except:
            print("error reading, fetching from Yahoo Finance...")

    def set_params(self):
        self.open = self.data['Close'].iloc[0]
        self.close = self.data['Close'].iloc[-1]
        self.shares = self.bal // self.open

    def update_positions(self, shares, close):
        return shares * close

    def calculate_profit(self, data):
        ma_index = 'ma_' + str(self.window)

        print()
        print("calculating...")

        print("close: ", str(round(data['Close'], 2)))
        print(ma_index, ": ", str(round(data[ma_index], 2)))

        print()

        if not data[ma_index]:
            return 0

        if data['Close'] > data[ma_index] and not self.long:
            self.price_bought = data['Close']
            self.long = True
            print("opened at: ", str(round(self.price_bought, 2)))
            return 0
        elif data['Close'] < data[ma_index] and self.long:
            self.long = False
            profit = (self.shares * data['Close']) - \
                (self.shares * self.price_bought)
            self.bal += profit
            print("closed at: ", str(round(data['Close'], 2)))
            print('profit: $', str(round(profit, 2)))
            return profit
        else:
            print("hold")
            return 0

    def backtest(self, window):
        if not self.data.shape[0]:
            self.read(self.alpha)

        self.set_params()
        self.data['ma_' +
                  str(window)] = self.data['Close'].rolling(window=window).mean()
        self.data['profit'] = self.data.apply(
            self.calculate_profit, axis=1)
        pct_gain = 100 * ((self.bal - self.starting_bal) / self.starting_bal)
        pct_gain = str(round(pct_gain, 2))
        print("\nstarting balance: $", self.starting_bal)
        print("ending balance: $", round(self.bal, 2))
        print("\nMA profit: $", str(round(self.data['profit'].sum(), 2)))
        bh = round((self.shares * self.close) - self.starting_bal, 2)
        print("buy-and-hold profit: $", bh)
        print("\nMA % gain: ", pct_gain)

    def __str__(self):
        print("starting balance: ", self.starting_bal)
        print("ending balance: ", self.bal)

    # def backtest_many(self, small_window, large_window):
    #    return 0
