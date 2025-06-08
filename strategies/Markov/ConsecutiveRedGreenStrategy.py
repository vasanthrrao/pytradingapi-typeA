class ConsecutiveRedGreenStrategy(Strategy):
    n = 3  # number of consecutive red/green candles required

    def init(self):
        pass

    def next(self):
        # We need at least n bars of history
        if len(self.data) < self.n:
            return

        # Check for n consecutive red candles
        if all(self.data.Close[-i] < self.data.Open[-i] for i in range(1, self.n + 1)):
            self.buy()
        # Check for n consecutive green candles
        if all(self.data.Close[-i] > self.data.Open[-i] for i in range(1, self.n + 1)):
            self.sell()
        # Always close position at the end of the bar
        if self.position:
            self.position.close()
