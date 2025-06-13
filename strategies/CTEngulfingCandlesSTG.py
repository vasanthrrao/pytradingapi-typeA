import yfinance as yf
import pandas as pd



class CTEngulfingCandlesSTG:

    def get_candle_data(self, symbol, start_date, end_date, interval='1d'):
        """Fetch historical candle data for a specific symbol."""
        df = yf.download(symbol, start=start_date, end=end_date, interval=interval)
        return df

    def identify_engulfing_candles(self, df):
        """Identify bullish and bearish engulfing candles in the DataFrame."""
        df['Bullish_Engulfing'] = (df['Open'].shift(1) > df['Close'].shift(1)) & \
                                  (df['Open'] < df['Close']) & \
                                  (df['Open'] < df['Close'].shift(1)) & \
                                  (df['Close'] > df['Open'].shift(1))

        df['Bearish_Engulfing'] = (df['Open'].shift(1) < df['Close'].shift(1)) & \
                                  (df['Open'] > df['Close']) & \
                                  (df['Open'] > df['Close'].shift(1)) & \
                                  (df['Close'] < df['Open'].shift(1))

        return df

    def get_engulfing_candles(self, symbol, start_date, end_date, interval='1d'):
        df = self.get_candle_data(symbol, start_date, end_date, interval)
        df = self.identify_engulfing_candles(df)
        return df[df['Bullish_Engulfing'] | df['Bearish_Engulfing']]

def signal_generator(df):
    open = df.Open.iloc[-1]
    close = df.Close.iloc[-1]
    previous_open = df.Open.iloc[-2]
    previous_close = df.Close.iloc[-2]
    
    # Bearish Pattern
    if (open>close and 
    previous_open<previous_close and 
    close<previous_open and
    open>=previous_close):
        return 1

    # Bullish Pattern
    elif (open<close and 
        previous_open>previous_close and 
        close>previous_open and
        open<=previous_close):
        return 2
    
    # No clear pattern
    else:
        return 0

    signal = []
    signal.append(0)
    for i in range(1,len(dataF)):
        df = dataF[i-1:i+1]
        signal.append(signal_generator(df))
    #signal_generator(data)
    dataF["signal"] = signal

    return dataF

def main():
    symbol = 'AAPL'
    start_date = '2023-01-01'
    end_date = '2023-10-01'
    interval = '1d'
    
    strategy = CTEngulfingCandlesSTG()
    engulfing_candles_df = strategy.get_engulfing_candles(symbol, start_date, end_date)
    
    if not engulfing_candles_df.empty:
        print("Engulfing Candles Found:")
        print(engulfing_candles_df[['Open', 'Close', 'Bullish_Engulfing', 'Bearish_Engulfing']])
    else:
        print("No engulfing candles found.")      