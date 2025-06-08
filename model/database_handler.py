import mysql.connector  # type: ignore
from datetime import datetime, timedelta
import os
import logging

log_folder = "log"
logging.basicConfig(
    filename=os.path.join(log_folder, 'db_err.log'),
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DatabaseHandler:
    def __init__(self):
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "myalgo_db"
        }

    def get_connection(self):
        return mysql.connector.connect(**self.db_config)

    def create_profile_table(self, table_name):
        """Create a profile table if it does not exist."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        create_table_sql = '''
                CREATE TABLE IF NOT EXISTS portfolio_mast (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    tradingsymbol VARCHAR(50),
                    exchange VARCHAR(10),
                    instrument_token BIGINT,
                    isin VARCHAR(20),
                    product VARCHAR(10),
                    price FLOAT,
                    quantity FLOAT,
                    used_quantity FLOAT,
                    t1_quantity FLOAT,
                    realised_quantity FLOAT,
                    authorised_quantity FLOAT,
                    authorised_date VARCHAR(30),
                    opening_quantity FLOAT,
                    collateral_quantity FLOAT,
                    collateral_type VARCHAR(20),
                    discrepancy BOOLEAN,
                    average_price FLOAT,
                    last_price FLOAT,
                    close_price FLOAT,
                    pnl FLOAT,
                    day_change FLOAT,
                    day_change_percentage FLOAT,
                    raw_json JSON,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )'''
        cursor.execute(create_table_sql)

        try:
           
            conn.commit()
         
        except mysql.connector.Error as err:
            logging.error(f"Error creating table {table_name}: {err}")
        finally:
            cursor.close()
            conn.close()
    def clear_profile_table(self, table_name):
        """Clear all records from the profile table."""
        conn = self.get_connection()
        cursor = conn.cursor()
        delete_query = f"DELETE FROM {table_name}"
        cursor.execute(delete_query)
        try:
            # Commit the changes to the database.
            conn.commit()
            #print(f"Cleared all records from {table_name}.")
            
        except mysql.connector.Error as err:
            logging.error(f"Error clearing table {table_name}: {err}")
        
        finally:
            cursor.close()
            conn.close()

    def create_position_table(self, table_name):
        """Create a position table if it does not exist."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        create_table_sql = fcreate_table_sql = '''
                CREATE TABLE IF NOT EXISTS position_mast (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    tradingsymbol VARCHAR(50),
                    exchange VARCHAR(10),
                    instrument_token BIGINT,
                    product VARCHAR(10),
                    quantity FLOAT,
                    overnight_quantity FLOAT,
                    multiplier FLOAT,
                    average_price FLOAT,
                    close_price FLOAT,
                    last_price FLOAT,
                    value FLOAT,
                    pnl FLOAT,
                    m2m FLOAT,
                    unrealised FLOAT,
                    realised FLOAT,
                    buy_quantity FLOAT,
                    buy_price FLOAT,
                    buy_value FLOAT,
                    buy_m2m FLOAT,
                    sell_quantity FLOAT,
                    sell_price FLOAT,
                    sell_value FLOAT,
                    sell_m2m FLOAT,
                    day_buy_quantity FLOAT,
                    day_buy_price FLOAT,
                    day_buy_value FLOAT,
                    day_sell_quantity FLOAT,
                    day_sell_price FLOAT,
                    day_sell_value FLOAT,
                    raw_json JSON,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )'''
        cursor.execute(create_table_sql)

        try:
            conn.commit()
            print(f"Table {table_name} created or already exists.")
            
        except mysql.connector.Error as err:
            logging.error(f"Error creating table {table_name}: {err}")
        
        finally:
            cursor.close()
            conn.close()

    def clear_position_table(self, table_name):
        """Clear all records from the position table."""
        conn = self.get_connection()
        cursor = conn.cursor()
        delete_query = f"DELETE FROM {table_name}"
        cursor.execute(delete_query)
        try:
            # Commit the changes to the database.
            conn.commit()
            #print(f"Cleared all records from {table_name}.")

        except mysql.connector.Error as err:
            logging.error(f"Error clearing table {table_name}: {err}")
        
        finally:
            cursor.close()
            conn.close()


    def create_order_history_table(self, table_name):
        """Create an order history table if it does not exist."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        create_table_sql = f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    trade_id VARCHAR(50),
                    order_id VARCHAR(50),
                    exchange VARCHAR(10),
                    tradingsymbol VARCHAR(100),
                    instrument_token BIGINT,
                    product VARCHAR(10),
                    average_price FLOAT,
                    quantity FLOAT,
                    exchange_order_id VARCHAR(50),
                    transaction_type VARCHAR(10),
                    fill_timestamp VARCHAR(20),
                    order_timestamp DATETIME,
                    exchange_timestamp DATETIME,
                    raw_json JSON,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )'''
        cursor.execute(create_table_sql)

        try:
            conn.commit()
            print(f"Table {table_name} created or already exists.")
            
        except mysql.connector.Error as err:
            logging.error(f"Error creating table {table_name}: {err}")
        
        finally:
            cursor.close()
            conn.close()
    def clear_order_history_table(self, table_name):
        """Clear all records from the order history table."""
        conn = self.get_connection()
        cursor = conn.cursor()
        delete_query = f"DELETE FROM {table_name}"
        cursor.execute(delete_query)
        try:
            # Commit the changes to the database.
            conn.commit()
            #print(f"Cleared all records from {table_name}.")

        except mysql.connector.Error as err:
            logging.error(f"Error clearing table {table_name}: {err}")
        
        finally:
            cursor.close()
            conn.close()

    def create_order_book_table(self, table_name):
        """Create an order book table if it does not exist."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        create_table_sql = '''
                CREATE TABLE IF NOT EXISTS order_book (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    placed_by VARCHAR(50),
                    order_id VARCHAR(50),
                    exchange_order_id VARCHAR(50),
                    parent_order_id VARCHAR(50),
                    status VARCHAR(30),
                    status_message VARCHAR(100),
                    status_message_raw VARCHAR(100),
                    order_timestamp DATETIME,
                    exchange_update_timestamp DATETIME,
                    exchange_timestamp DATETIME,
                    variety VARCHAR(20),
                    modified BOOLEAN,
                    exchange VARCHAR(10),
                    tradingsymbol VARCHAR(50),
                    instrument_token BIGINT,
                    order_type VARCHAR(20),
                    transaction_type VARCHAR(10),
                    validity VARCHAR(10),
                    product VARCHAR(10),
                    quantity FLOAT,
                    disclosed_quantity FLOAT,
                    price FLOAT,
                    trigger_price FLOAT,
                    average_price FLOAT,
                    filled_quantity FLOAT,
                    pending_quantity FLOAT,
                    cancelled_quantity FLOAT,
                    market_protection FLOAT,
                    meta JSON,
                    tag JSON,
                    guid VARCHAR(100),
                    raw_json JSON,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )'''
        cursor.execute(create_table_sql)

        try:
            conn.commit()
            print(f"Table {table_name} created or already exists.")
            
        except mysql.connector.Error as err:
            logging.error(f"Error creating table {table_name}: {err}")
        
        finally:
            cursor.close()
            conn.close()

    def clear_order_book_table(self, table_name):
        """Clear all records from the order book table."""
        conn = self.get_connection()
        cursor = conn.cursor()
        delete_query = f"DELETE FROM {table_name}"
        cursor.execute(delete_query)
        try:
            # Commit the changes to the database.
            conn.commit()
            #print(f"Cleared all records from {table_name}.")

        except mysql.connector.Error as err:
            logging.error(f"Error clearing table {table_name}: {err}")
        
        finally:
            cursor.close()
            conn.close()



    def insert_candle(self, table_name, candle):
        """Insert a historical candle object into the database, avoiding duplicates."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # First, check if the record already exists.
        select_query = f"""
        SELECT COUNT(*) FROM {table_name}
        WHERE instrument_key = %s AND timestamp = %s
        """
        cursor.execute(select_query, (candle.instrument_key, candle.timestamp))
        result = cursor.fetchone()
        
        if result[0] == 0:
            # Record does not exist, perform the insert.
            insert_query = f"""
            INSERT INTO {table_name} (instrument_key, timestamp, open_price, high_price, low_price, close_price, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                candle.instrument_key, candle.timestamp, candle.open_price,
                candle.high_price, candle.low_price, candle.close_price, candle.volume
            ))
            conn.commit()
        else:
            # Optional: Log that a duplicate record was detected.
            print(f"Candle for {candle.instrument_key} at {candle.timestamp} already exists. Skipping insert.")

        cursor.close()
        conn.close()


    def insert_historical_candle(self, table_name, instrument_key, candles):
        """Insert a list of historical candle objects into the database."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Prepare the insert query with placeholders for multiple rows.
        insert_query = f"""
        INSERT INTO {table_name} (instrument_key, timestamp, open_price, high_price, low_price, close_price, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        # Create a list of tuples for the values to be inserted.
        values = [
            (instrument_key, candle.timestamp, candle.open_price,
             candle.high_price, candle.low_price, candle.close_price, candle.volume)
            for candle in candles
        ]
        
        try:
            cursor.executemany(insert_query, values)
            conn.commit()
            print(f"Inserted {cursor.rowcount} rows into {table_name}.")
            
        except mysql.connector.Error as err:
            logging.error(f"Error inserting candles: {err}")
        
        finally:
            cursor.close()
            conn.close()

    def get_instrument_key(self, stocks):
        try:  
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT instrument_key FROM nse_data WHERE tradingsymbol = %s", (stocks,))
            result = cursor.fetchone()
            if result:
                #print(f"Matched stock: {stocks} -> {result[0]}")
                return result[0]
            
        except Exception as err:
            logging.error(f"Database error during instrument lookup: {err}")
        finally:
            cursor.close()
            conn.close()
    
    def insert_goldTrade_log(self,subject, from_email, exchange, ticker, price, volume):
        """Insert a trade log into the database."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        insert_query = f"""
        INSERT INTO goldTrade_log (subject, from_email, exchange, ticker, price, volume)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(insert_query, (subject, from_email, exchange, ticker, price, volume))
            conn.commit()
            #print(f"Inserted gold trade log into .")
            
        except mysql.connector.Error as err:
            logging.error(f"Error inserting trade log: {err}")
        
        finally:
            cursor.close()
            conn.close()
    def convert_instrument_key(self, instrument_key):
        return instrument_key.replace("|", "%7C")


    def get_date_range_for_fetch(self, table_name, instrument_key):
        """
        Return a tuple (from_date, to_date) as strings in YYYY-MM-DD format.
        
        - from_date: is one day after the latest recorded candle for the given instrument and table.
        - to_date: is the current date.
        
        If no candle exists for the instrument, from_date is set to the current date.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        query = f"SELECT MAX(timestamp) FROM {table_name} WHERE instrument_key = %s"
        cursor.execute(query, (instrument_key,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result[0] is not None:
            latest_date = result[0].date()  # Extract date from datetime
            from_date = latest_date + timedelta(days=1)
        else:
            
            # No existing record found; set from_date to current date or a default start date
            from_date = datetime.today().date()
        
        to_date = datetime.today().date()
        return from_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d")
