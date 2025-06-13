import yfinance as yf
import requests
import os
import pandas as pd
import numpy as np
from backtesting import Strategy, Backtest
import mysql.connector
from datetime import date
import csv

try:
    from bs4 import BeautifulSoup
except (ModuleNotFoundError, ImportError):
    print("BeautifulSoup module not found")
    os.system(f"{sys.executable} -m pip install -U beautifulsoup4")
finally:
    from bs4 import BeautifulSoup

Charting_Link = "https://chartink.com/screener/"
Charting_url = 'https://chartink.com/screener/process'

class CTMarkov97STG:



    def get_candle_data(self, symbol, start_date, end_date, group_by='ticker', interval='1d'):
            """Fetch historical candle data for a specific symbol."""
            df = yf.download(symbol, start=start_date, end=end_date, group_by=group_by, interval=interval)
            return df

    def GetDataFromChartink(self,payload):
        payload = {'scan_clause': payload}
        
        with requests.Session() as s:
            r = s.get(Charting_Link)
            soup = BeautifulSoup(r.text, "html.parser")
            csrf = soup.select_one("[name='csrf-token']")['content']
            s.headers['x-csrf-token'] = csrf
            r = s.post(Charting_url, data=payload)

            df = pd.DataFrame()
            data_list = []
            for item in r.json()['data']:
                if len(item) > 0:
                    data_list.append(item)
            df = pd.DataFrame(data_list)
        return df
         

    def count_candle_streaks(n, data):
        up_streaks = 0
        up_followed_by_red = 0
        down_streaks = 0
        down_followed_by_green = 0

        for ticker in tickers:
            df = data[ticker][['Open', 'Close']].dropna()
            candle_color = df['Close'] > df['Open']  # True: green, False: red
            candle_series = candle_color.values

            i = 0
            while i < len(candle_series) - n:
                # Check for green streak
                if all(candle_series[i + j] for j in range(n)):
                    up_streaks += 1
                    if i + n < len(candle_series) and not candle_series[i + n]:
                        up_followed_by_red += 1
                    i += n
                # Check for red streak
                elif all(not candle_series[i + j] for j in range(n)):
                    down_streaks += 1
                    if i + n < len(candle_series) and candle_series[i + n]:
                        down_followed_by_green += 1
                    i += n
                else:
                    i += 1

        up_fraction = up_followed_by_red / up_streaks if up_streaks > 0 else 0
        down_fraction = down_followed_by_green / down_streaks if down_streaks > 0 else 0

        return {
            f"{n} Green Candles Followed by Red (Fraction)": up_fraction,
            f"{n} Red Candles Followed by Green (Fraction)": down_fraction
        }

    def three_red_import_chartink(self):

        Condition = "( {57960} ( latest close < latest open and 1 day ago close < 1 day ago open and 2 days ago close < 2 days ago open ) )" 

        data = self.GetDataFromChartink(Condition)

        data = data.sort_values(by='per_chg', ascending=False)

        print(data)

        data.to_csv("data/3redData/Chartink_result.csv") 

        file_path = "data/3redData/Chartink_result.csv"

        # MySQL connection
        db = mysql.connector.connect(
            host="localhost",      # update if different
            user="root",   # update
            password="",  # update
            database="myalgo_db"   # update
        )
        cursor = db.cursor()
        cursor.execute("TRUNCATE TABLE three_red_stocks")
        print("✅ Cleared existing data in `three_red_stocks`.")

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            inserted = 0

            for row in reader:
                sr = int(row["sr"].strip())
                symbol = row["nsecode"].strip()
                price = row["close"].strip()
                volume = row["volume"].strip()


                # Look up yfinsymbol from nse_data using tradingsymbol
                cursor.execute("SELECT yfinsymbol FROM nse_data WHERE tradingsymbol = %s LIMIT 1", (symbol,))
                result = cursor.fetchone()
                yfinsymbol = result[0] if result else None

                # Insert into table
                cursor.execute("""
                    INSERT INTO three_red_stocks (Sr,  Symbol,  Price, Volume, yfinsymbol)
                    VALUES (%s, %s, %s, %s, %s)
                """, (sr,  symbol, price, volume, yfinsymbol))
                inserted += 1

        db.commit()
        cursor.close()
        db.close()

        print(f"✅ Imported {inserted} rows from {file_path}")

    def three_red_import_manual(self):
        file_path = "3redData/3red, Technical Analysis Scanner.csv"

        # MySQL connection
        db = mysql.connector.connect(
            host="localhost",      # update if different
            user="root",   # update
            password="",  # update
            database="myalgo_db"   # update
        )
        cursor = db.cursor()
        cursor.execute("TRUNCATE TABLE three_red_stocks")
        print("✅ Cleared existing data in `three_red_stocks`.")

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            inserted = 0

            for row in reader:
                sr = int(row["Sr."].strip())
                name = row["Stock Name"].strip()
                symbol = row["Symbol"].strip()
                change = row["% Chg"].strip()
                price = row["Price"].strip()
                volume = row["Volume"].strip()


                # Look up yfinsymbol from nse_data using tradingsymbol
                cursor.execute("SELECT yfinsymbol FROM nse_data WHERE tradingsymbol = %s LIMIT 1", (symbol,))
                result = cursor.fetchone()
                yfinsymbol = result[0] if result else None

                # Insert into table
                cursor.execute("""
                    INSERT INTO three_red_stocks (Sr, StockName, Symbol, ChangePct, Price, Volume, yfinsymbol)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (sr, name, symbol, change, price, volume, yfinsymbol))
                inserted += 1

        db.commit()
        cursor.close()
        db.close()

        print(f"✅ Imported {inserted} rows from {file_path}")

    def best_three(self):
        print("🔥 Fetching top 3 best performing stocks...")
        # Connect to MySQL
        db = mysql.connector.connect(
            host="localhost",      # update if different
            user="root",   # update
            password="",  # update
            database="myalgo_db"   # update
        )
        cursor = db.cursor(dictionary=True)

        # Step 1: Fetch yfinsymbols from three_red_stocks
        cursor.execute("SELECT yfinsymbol FROM three_red_stocks WHERE yfinsymbol IS NOT NULL AND yfinsymbol != ''")
        red_symbols = [row['yfinsymbol'] for row in cursor.fetchall()]

        if not red_symbols:
            print("❌ No valid yfinsymbols in `three_red_stocks`.")
            return []

        # Step 2: Load return data from markov_result (all time)
        cursor.execute("SELECT yfinsymbol, return_percent FROM markov_result")
        all_time_returns = {row['yfinsymbol']: row['return_percent'] for row in cursor.fetchall()}

        # Step 3: Load return data from markov_result_year (1-year)
        cursor.execute("SELECT yfinsymbol, return_percent FROM markov_result_year")
        one_year_returns = {row['yfinsymbol']: row['return_percent'] for row in cursor.fetchall()}

        # Step 4: Match symbols and compute combined metrics
        combined = []
        for symbol in red_symbols:
            if symbol in all_time_returns and symbol in one_year_returns:
                all_ret = all_time_returns[symbol]
                year_ret = one_year_returns[symbol]
                avg_ret = (all_ret + year_ret) / 2
                combined.append({
                    'yfinsymbol': symbol,
                    'all_time_return': all_ret,
                    'year_return': year_ret,
                    'avg_return': avg_ret
                })

        if not combined:
            print("⚠️ No matching symbols found in both markov tables.")
            return []

        # Step 5: Sort by average return
        combined_sorted = sorted(combined, key=lambda x: x['avg_return'], reverse=True)

        # Step 6: Display all
        print("\n📊 All Matching Stocks from Three-Red Screener:")
        print("{:<20} {:>15} {:>15} {:>15}".format("YF Symbol", "All Return (%)", "1Y Return (%)", "Avg Return (%)"))
        print("-" * 70)
        for row in combined_sorted:
            print("{:<20} {:>15.2f} {:>15.2f} {:>15.2f}".format(
                row['yfinsymbol'],
                row['all_time_return'],
                row['year_return'],
                row['avg_return']
            ))

        # Step 7: Show top 3 separately
        print("\n🔥 Top 3 Stocks by Average Return:")
        for row in combined_sorted[:3]:
            print(f"{row['yfinsymbol']}: Avg = {row['avg_return']:.2f}%, All = {row['all_time_return']:.2f}%, Year = {row['year_return']:.2f}%")

        cursor.close()
        db.close()

        return combined_sorted[:3]

def import_stock_returns():
    print("📥 Importing stock returns...")

    # DB Connection
    db = mysql.connector.connect(
        host="localhost",      # update if different
        user="root",   # update
        password="",  # update
        database="myalgo_db"   # update
    )
    cursor = db.cursor(dictionary=True)

    # Step 1: Get 10 valid yfinsymbols not already processed or failed
    cursor.execute("""
        SELECT yfinsymbol 
        FROM nse_data 
        WHERE yfinsymbol IS NOT NULL AND yfinsymbol != ''
        AND yfinsymbol NOT IN (SELECT yfinsymbol FROM markov_result_year)
        AND yfinsymbol NOT IN (SELECT yfinsymbol FROM markov_failed)
        LIMIT 450
    """)
    rows = cursor.fetchall()
    tickers = [row['yfinsymbol'] for row in rows]

    if not tickers:
        print("✅ No new symbols to process.")
        return

    print(f"📥 Selected {len(tickers)} new tickers:", tickers)

    # Step 2: Download data
    strategy = CTMarkov97STG()
    start = "2024-01-01"
    end = str(date.today())

    try:
        data = strategy.get_candle_data(tickers, start_date=start, end_date=end, group_by='ticker', interval='1d')
    except Exception as e:
        print("❌ Global data download error:", e)
        # Log each ticker as failed
        for symbol in tickers:
            log_failure(cursor, db, symbol, str(e))
        return

    # Step 3: Run Backtest
    for symbol in tickers:
        try:
            if symbol not in data or data[symbol].empty or len(data[symbol].dropna()) < 100:
                print(f"⚠️ Skipping {symbol} due to insufficient or missing data.")
                log_failure(cursor, db, symbol, "Insufficient data or symbol not found")
                continue

            df = data[symbol][['Open', 'High', 'Low', 'Close', 'Volume']].dropna()

            bt = Backtest(df,
                          ConsecutiveRedStrategy,
                          cash=100_000,
                          commission=0.0004,
                          exclusive_orders=True,
                          margin=1.0)

            stats = bt.run()

            return_percent = round(stats['Return [%]'], 2)
            max_drawdown = round(stats['Max. Drawdown [%]'], 2)

            print(f"✅ {symbol}: Return={return_percent}%, MaxDD={max_drawdown}%")

            # Step 4: Insert result
            cursor.execute("""
                INSERT INTO markov_result_year (yfinsymbol, return_percent, max_drawdown_percent, start_date, end_date)
                VALUES (%s, %s, %s, %s, %s)
            """, (symbol, return_percent, max_drawdown, start, end))
            db.commit()

        except Exception as e:
            print(f"❌ Error processing {symbol}: {e}")
            log_failure(cursor, db, symbol, str(e))
   
    cursor.close()
    db.close()
    

def log_failure(cursor, db, symbol, reason):
    try:
        cursor.execute("""
            INSERT INTO markov_failed (yfinsymbol, reason)
            VALUES (%s, %s)
        """, (symbol, reason[:500]))  # Limit to 500 chars for storage safety
        db.commit()
    except Exception as e:
        print(f"⚠️ Could not log failure for {symbol}: {e}")
