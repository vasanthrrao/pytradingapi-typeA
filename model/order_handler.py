import os
import json
import requests
from dotenv import load_dotenv

from model.token_handler import TokenHandler
from model.database_handler import DatabaseHandler
       
# Load environment variables from .env file
load_dotenv()

token_handler = TokenHandler()
class OrderHandler:
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

    def get_js_data(self):
        """Construct data for the API call."""
        return {
            'tradingsymbol': 'INFY',
            'exchange': 'NSE',
            'transaction_type': 'BUY',
            'order_type': 'LIMIT',
            'quantity': '1',
            'product': 'MIS',
            'validity': 'IOC',
            'price': '1500',
        }

    def place_order(self):
        """Perform POST request to place an order."""
        from model.database_handler import DatabaseHandler
        db = DatabaseHandler()
        headers = self.get_headers()
        if not headers:
            return
        url = 'https://api.mstock.trade/openapi/typea/orders/regular'

        try:
            response = requests.post(url, headers=headers, data=self.get_js_data())
            print("Status Code:", response.status_code)
            if response.status_code == 200:
                print("Response JSON:", response.json())
                return response.json()
            else:
                print("Error Response:", response.text)
        except requests.RequestException as e:
            print("Request failed:", str(e))

    def modify_order_with_stoploss(self):
        """
        Find latest order_id for tradingsymbol, calculate 10% stop loss, and call modify order API.
        """
        db = DatabaseHandler()
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)

        # Get latest order_id and average_price for the tradingsymbol, handling '-EQ' suffix
        cursor.execute("""
                            SELECT  pm.tradingsymbol,pm.average_price,pm.quantity,        MAX(oh.order_id) AS latest_order_id
                            FROM position_mast pm JOIN  order_history oh 
                            ON pm.tradingsymbol = REPLACE(oh.tradingsymbol, '-EQ', '')
                    WHERE  
                        oh.transaction_type = 'BUY'
                    GROUP BY  
                        pm.tradingsymbol, pm.average_price, pm.quantity
                    ORDER BY  
                        MAX(oh.order_timestamp) DESC
                LIMIT 1;

                """)
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if not row:
            print(f"No order found for")
            return

        order_id = row['latest_order_id']
        quantity = row['quantity']
        tradingsymbol = row['tradingsymbol']
        avg_price = float(row['average_price'])
        stop_loss_price =avg_price - round(avg_price * 0.9, 2)  # 10% stop loss

        print(f"Modifying order {order_id} for {tradingsymbol} with stop loss at {stop_loss_price}")

        # Prepare headers and data for modify order API
        headers = {
            'X-Mirae-Version': '1',
            'Authorization': f'token {self.API_KEY}:{self.Access_token}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'order_id': order_id,
            'tradingsymbol': tradingsymbol,
            'trigger_price': stop_loss_price,
            'exchange': 'NSE',
            'transactiontype': 'SELL',
            'order_type': 'SL',
            'quantity': quantity,
            'validity': 'DAY',
            'price': stop_loss_price,
            'variety': 'regular',
            'product': 'MIS',
        }
        print("Data for modify order:", data)
        url = 'https://api.mstock.trade/openapi/typea/orders/modify'
        try:
            response = requests.post(url, headers=headers, data=data)
            print("Status Code:", response.status_code)
            if response.status_code == 200:
                print("Order modified successfully:", response.json())
                return response.json()
            else:
                print("Error modifying order:", response.text)
        except requests.RequestException as e:
            print("Request failed:", str(e))
