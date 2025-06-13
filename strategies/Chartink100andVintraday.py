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

class Chartink100andVintraday:
    def __init__(self):
        pass

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
         

    def hundred_import_chartink(self):

        Condition = "( {33489} ( ( latest high - latest low ) > ( 1 day ago high - 1 day ago low ) and ( latest high - latest low ) > ( 2 days ago high - 2 days ago low ) and ( latest high - latest low ) > ( 3 days ago high - 3 days ago low ) and ( latest high - latest low ) > ( 4 days ago high - 4 days ago low ) and ( latest high - latest low ) > ( 5 days ago high - 5 days ago low ) and ( latest high - latest low ) > ( 6 days ago high - 6 days ago low ) and ( latest high - latest low ) > ( 7 days ago high - 7 days ago low ) and latest close > latest open and latest close > 1 day ago close and weekly close > weekly open and monthly close > monthly open and 1 day ago volume > 10000 and latest sma ( close,20 ) > latest sma ( close,40 ) and latest sma ( close,40 ) > latest sma ( close,60 ) and ( latest volume ) > ( 1 day ago volume ) * 1.25 ) ) " 

        data = self.GetDataFromChartink(Condition)

        data = data.sort_values(by='per_chg', ascending=False)

        #print(data)

        data.to_csv("data/100Data/Chartink_100_result.csv") 

        file_path = "data/100Data/Chartink_100_result.csv"

        # MySQL connection
        db = mysql.connector.connect(
            host="localhost",      # update if different
            user="root",   # update
            password="",  # update
            database="myalgo_db"   # update
        )
        cursor = db.cursor()
        cursor.execute("DELETE FROM chartink_stocks WHERE strategy = %s AND fetch_date = %s", ("hundred_percent", date.today()))
        db.commit()

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            inserted = 0

            for row in reader:
                sr = int(row["sr"].strip())
                name = row["name"].strip()
                per_chg = row["per_chg"].strip()
                symbol = row["nsecode"].strip()
                price = row["close"].strip()
                volume = row["volume"].strip()


                # Look up yfinsymbol from nse_data using tradingsymbol
                cursor.execute("SELECT yfinsymbol FROM nse_data WHERE tradingsymbol = %s LIMIT 1", (symbol,))
                result = cursor.fetchone()
                yfinsymbol = result[0] if result else None

                # Insert into table
                cursor.execute("""
                    INSERT INTO chartink_stocks (Sr, Name, Symbol, per_chg, Price, Volume, yfinsymbol, strategy, fetch_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (sr, name, symbol, per_chg, price, volume, yfinsymbol, "hundred_percent", date.today()))
                inserted += 1

        db.commit()
        cursor.close()
        db.close()


    def vintraday_import_chartink(self):

        Condition1 = "( {33489} ( latest parabolic sar ( 0.04,0.02,0.2 ) < latest ema ( close,9 ) and 1 day ago  parabolic sar ( 0.04,0.02,0.2 ) >= 1 day ago  ema ( close,9 ) ) ) " 


        data = self.GetDataFromChartink(Condition1)
        print(data)
        data = data.sort_values(by='per_chg', ascending=False)

    

        data.to_csv("data/vintraday/Chartink_vintraday_result.csv") 

        file_path = "data/vintraday/Chartink_vintraday_result.csv"

        # MySQL connection
        db = mysql.connector.connect(
            host="localhost",      # update if different
            user="root",   # update
            password="",  # update
            database="myalgo_db"   # update
        )
        cursor = db.cursor()
        cursor.execute("DELETE FROM chartink_stocks WHERE strategy = %s AND fetch_date = %s", ("vintraday", date.today()))
        db.commit()
        
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            inserted = 0

            for row in reader:
                sr = int(row["sr"].strip())
                name = row["name"].strip()
                per_chg = row["per_chg"].strip()
                symbol = row["nsecode"].strip()
                price = row["close"].strip()
                volume = row["volume"].strip()


                # Look up yfinsymbol from nse_data using tradingsymbol
                cursor.execute("SELECT yfinsymbol FROM nse_data WHERE tradingsymbol = %s LIMIT 1", (symbol,))
                result = cursor.fetchone()
                yfinsymbol = result[0] if result else None

                # Insert into table
                cursor.execute("""
                    INSERT INTO chartink_stocks (Sr, name, Symbol, per_chg, Price, Volume, yfinsymbol, strategy, fetch_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (sr, name, symbol, per_chg, price, volume, yfinsymbol, "vintraday", date.today()))
                inserted += 1

        db.commit()
        cursor.close()
        db.close()
        