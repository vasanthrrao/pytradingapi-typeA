import pandas as pd
import pandas_ta as ta

class CTBollingerBandsRSISTG:
    def get_candle_data(self, symbol, start_date, end_date, interval='1d'):
        """Fetch historical candle data for a specific symbol."""
        df = yf.download(symbol, start=start_date, end=end_date, interval=interval)
        return df

    def calculate_bollinger_bands(self, df, window=20, num_std=2):
        """Calculate Bollinger Bands."""
        df['MA'] = df['Close'].rolling(window=window).mean()
        df['Upper Band'] = df['MA'] + (df['Close'].rolling(window=window).std() * num_std)
        df['Lower Band'] = df['MA'] - (df['Close'].rolling(window=window).std() * num_std)
        return df

    def calculate_rsi(self, df, window=14):
        """Calculate RSI."""
        df['RSI'] = ta.rsi(df['Close'], length=window)
        return df

    def preprocess_data(self, df):
        df["Gmt time"] = df["Gmt time"].str.replace(".000", "")
        df['Gmt time'] = pd.to_datetime(df['Gmt time'], format='%d.%m.%Y %H:%M:%S')
        df = df[df.High != df.Low]
        df.reset_index(inplace=True, drop=True)
        return df

    def get_bollinger_bands_rsi(self, symbol, start_date, end_date, interval='1d'):
        pass


    def test(self, symbol, start_date, end_date, interval='1d'):
        df = self.get_candle_data(symbol, start_date, end_date, interval)
        df = self.preprocess_data(df)
        df = self.calculate_bollinger_bands(df)
        df = self.calculate_rsi(df)
        df["Gmt time"] = df["Gmt time"].str.replace(".000", "")
        df['Gmt time'] = pd.to_datetime(df['Gmt time'], format='%d.%m.%Y %H:%M:%S')

        df = df[df.High != df.Low]
        df.reset_index(inplace=True, drop=True)
        # Calculate Bollinger Bands and RSI using pandas_ta
        df.ta.bbands(append=True, length=30, std=2)
        df.ta.rsi(append=True, length=14)
        df["atr"] = ta.atr(low=df.Low, close=df.Close, high=df.High, length=14)

        # Rename columns for clarity if necessary
        df.rename(columns={
            'BBL_30_2.0': 'bbl', 'BBM_30_2.0': 'bbm', 'BBU_30_2.0': 'bbh', 'RSI_14': 'rsi'
        }, inplace=True)

        # Calculate Bollinger Bands Width
        df['bb_width'] = (df['bbh'] - df['bbl']) / df['bbm']
        print(df)