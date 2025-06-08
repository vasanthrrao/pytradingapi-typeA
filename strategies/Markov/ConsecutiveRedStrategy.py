class ConsecutiveRedStrategy(Strategy):
    """
    If we detect n red candles in a row, then on the *very next* bar:
      - Buy at its open
      - Close at that same bar's close
    """
    n = 3  # number of consecutive red candles required

    def init(self):
        pass

    def next(self):
        # We need at least n bars of history
        if len(self.data) < self.n:
            return

        # Check if last n candles were red: Close < Open for each of the last n bars
        # The most recent bar is at index -1, then -2, etc.
        if all(self.data.Close[-i] < self.data.Open[-i] for i in range(1, self.n + 1)):
            # Issue a Buy at the *open* of the current bar (index -1),
            # which is effectively "the next bar" from the perspective
            # of completed candles. 
            self.buy()

        # If we have an open position, close it at *this* bar's close.
        # Because Backtesting.py processes order fills at the bar open,
        # calling `self.position.close()` inside `next()` ensures the position
        # will be exited by this bar’s close.
        if self.position:
            self.position.close()

