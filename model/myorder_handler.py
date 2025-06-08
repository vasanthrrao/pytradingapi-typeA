import os
import json
import requests
from dotenv import load_dotenv

from model.token_handler import TokenHandler
# from model.database_handler import DatabaseHandler
# Load environment variables from .env file
load_dotenv()

token_handler = TokenHandler()

class MyOrderHandler:
    def __init__(self):
        self.API_KEY = os.getenv("API_KEY")
        self.Access_token = token_handler.load_access_token_from_file()


    def get_headers(self):
        """Construct headers for the API call."""
        if not self.API_KEY or not self.Access_token:
            print("API_KEY or Access_token is missing.")
            return None
        return {
            'X-Mirae-Version': '1',
            'Authorization': f'token {self.API_KEY}:{self.Access_token}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

    def get_order_history_data(self):
        """Construct data for the API call with last 1 month date range."""
        from datetime import datetime, timedelta
        to_date = datetime.today()
        from_date = to_date - timedelta(days=30)
        return {
            'fromdate': from_date.strftime('%Y-%m-%d'),
            'todate': to_date.strftime('%Y-%m-%d'),
        }

    def get_order_book(self):
        """Perform GET request to fetch order details and store in order_book table."""
        from model.database_handler import DatabaseHandler
        headers = self.get_headers()
        if not headers:
            return

        url = 'https://api.mstock.trade/openapi/typea/orders'

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                formatted = json.dumps(response.json(), indent=4)
                print("Response JSON:\n", formatted)
                data = response.json()
                # Create table if not exists
                db = DatabaseHandler()
                conn = db.get_connection()
                db.create_order_book_table("order_book")

                db.clear_order_book_table("order_book")

                
                # Insert each order with validation
                orders = data.get('data', []) if isinstance(data, dict) else []
                if not orders or not isinstance(orders, list):
                    print("No orders found in response.")
                else:
                    cursor = conn.cursor()
                    for order in orders:
                        cursor.execute(
                            """
                            INSERT INTO order_book (
                                placed_by, order_id, exchange_order_id, parent_order_id, status, status_message, status_message_raw, order_timestamp, exchange_update_timestamp, exchange_timestamp, variety, modified, exchange, tradingsymbol, instrument_token, order_type, transaction_type, validity, product, quantity, disclosed_quantity, price, trigger_price, average_price, filled_quantity, pending_quantity, cancelled_quantity, market_protection, meta, tag, guid, raw_json
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """,
                            (
                                order.get('placed_by'),
                                order.get('order_id'),
                                order.get('exchange_order_id'),
                                order.get('parent_order_id'),
                                order.get('status'),
                                order.get('status_message'),
                                order.get('status_message_raw'),
                                order.get('order_timestamp'),
                                order.get('exchange_update_timestamp'),
                                order.get('exchange_timestamp'),
                                order.get('variety'),
                                order.get('modified'),
                                order.get('exchange'),
                                order.get('tradingsymbol'),
                                order.get('instrument_token'),
                                order.get('order_type'),
                                order.get('transaction_type'),
                                order.get('validity'),
                                order.get('product'),
                                order.get('quantity'),
                                order.get('disclosed_quantity'),
                                order.get('price'),
                                order.get('trigger_price'),
                                order.get('average_price'),
                                order.get('filled_quantity'),
                                order.get('pending_quantity'),
                                order.get('cancelled_quantity'),
                                order.get('market_protection'),
                                json.dumps(order.get('meta')) if order.get('meta') is not None else None,
                                json.dumps(order.get('tag')) if order.get('tag') is not None else None,
                                order.get('guid'),
                                json.dumps(order)
                            )
                        )
                    conn.commit()
                    cursor.close()
                    print("Order book data inserted into order_book table.")
                conn.close()
                return data
            else:
                print("Error Response:", response.text)
        except requests.RequestException as e:
            print("Request failed:", str(e))

    def get_order_history(self):
        from model.database_handler import DatabaseHandler
        headers = self.get_headers()
        if not headers:
            return

        url = 'https://api.mstock.trade/openapi/typea/trades'

        try:
            response = requests.get(url, headers=headers, data=self.get_order_history_data())
            if response.status_code == 200:
                formatted = json.dumps(response.json(), indent=4)
                #print("Response JSON:\n", formatted)
                data = response.json()
                # Create table if not exists
                db = DatabaseHandler()
                conn = db.get_connection()
                cursor = conn.cursor()
                db.create_order_history_table("order_history")

                conn.commit()
                # Clear existing data in order_history table
                db.clear_order_history_table("order_history")


                # Insert each trade
                trades = data.get('data', []) if isinstance(data, dict) else []
                for trade in trades:
                    cursor.execute(
                        """
                        INSERT INTO order_history (
                            trade_id, order_id, exchange, tradingsymbol, instrument_token, product, average_price, quantity, exchange_order_id, transaction_type, fill_timestamp, order_timestamp, exchange_timestamp, raw_json
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            trade.get('trade_id'),
                            trade.get('order_id'),
                            trade.get('exchange'),
                            trade.get('tradingsymbol'),
                            trade.get('instrument_token'),
                            trade.get('product'),
                            trade.get('average_price'),
                            trade.get('quantity'),
                            trade.get('exchange_order_id'),
                            trade.get('transaction_type'),
                            trade.get('fill_timestamp'),
                            trade.get('order_timestamp'),
                            trade.get('exchange_timestamp'),
                            json.dumps(trade)
                        )
                    )
                conn.commit()
                cursor.close()
                conn.close()
                print("Order history data inserted into order_history table.")
                return data
            else:
                print("Error Response:", response.text)
        except requests.RequestException as e:
            print("Request failed:", str(e))

