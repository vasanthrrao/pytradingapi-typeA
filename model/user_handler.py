import os
import json
import requests
from dotenv import load_dotenv
from model.token_handler import TokenHandler
# Load environment variables from .env file
load_dotenv()
token_handler = TokenHandler()

class UserHandler:
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
        }

    def get_fund_summary(self):
        """Perform GET request to fetch fund summary."""
        self.load_access_token_from_file()
        headers = self.get_headers()
        if not headers:
            return

        url = 'https://api.mstock.trade/openapi/typea/user/fundsummary'

        try:
            response = requests.get(url, headers=headers)
            print("Status Code:", response.status_code)
            if response.status_code == 200:
                formatted = json.dumps(response.json(), indent=4)
                print("Response JSON:\n", formatted)
                return response.json()
            else:
                print("Error Response:", response.text)
        except requests.RequestException as e:
            print("Request failed:", str(e))

    def get_portfolio(self):
        """Perform GET request to fetch portfolio and store response in portfolio_mast table."""
        from model.database_handler import DatabaseHandler
        headers = self.get_headers()
        if not headers:
            return

        url = 'https://api.mstock.trade/openapi/typea/portfolio/holdings'

        try:
            response = requests.get(url, headers=headers)
            print("Status Code:", response.status_code)
            if response.status_code == 200:
                formatted = json.dumps(response.json(), indent=4)
                print("Response JSON:\n", formatted)
                data = response.json()
                # Create table if not exists
                db = DatabaseHandler()
                conn = db.get_connection()
                cursor = conn.cursor()

                db.create_profile_table("portfolio_mast")

                # Delete old records
                db.clear_profile_table("portfolio_mast")
               

                # Insert each holding
                holdings = data.get('data', []) if isinstance(data, dict) else []
                for holding in holdings:
                    cursor.execute(
                        """
                        INSERT INTO portfolio_mast (
                            tradingsymbol, exchange, instrument_token, isin, product, price, quantity, used_quantity, t1_quantity, realised_quantity, authorised_quantity, authorised_date, opening_quantity, collateral_quantity, collateral_type, discrepancy, average_price, last_price, close_price, pnl, day_change, day_change_percentage, raw_json
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            holding.get('tradingsymbol'),
                            holding.get('exchange'),
                            holding.get('instrument_token'),
                            holding.get('isin'),
                            holding.get('product'),
                            holding.get('price'),
                            holding.get('quantity'),
                            holding.get('used_quantity'),
                            holding.get('t1_quantity'),
                            holding.get('realised_quantity'),
                            holding.get('authorised_quantity'),
                            holding.get('authorised_date'),
                            holding.get('opening_quantity'),
                            holding.get('collateral_quantity'),
                            holding.get('collateral_type'),
                            holding.get('discrepancy'),
                            holding.get('average_price'),
                            holding.get('last_price'),
                            holding.get('close_price'),
                            holding.get('pnl'),
                            holding.get('day_change'),
                            holding.get('day_change_percentage'),
                            json.dumps(holding)
                        )
                    )
                conn.commit()
                cursor.close()
                conn.close()
                print("Portfolio data inserted into portfolio_mast table.")
                return data
            else:
                print("Error Response:", response.text)
        except requests.RequestException as e:
            print("Request failed:", str(e))

    def get_position(self):
        """Perform GET request to fetch positions and store response in position_mast table."""
        from model.database_handler import DatabaseHandler
        headers = self.get_headers()
        if not headers:
            return

        url = 'https://api.mstock.trade/openapi/typea/portfolio/positions'

        try:
            response = requests.get(url, headers=headers)
            #print("Status Code:", response.status_code)
            if response.status_code == 200:
                formatted = json.dumps(response.json(), indent=4)
                #print("Response JSON:\n", formatted)
                data = response.json()
                # Create table if not exists
                db = DatabaseHandler()
                conn = db.get_connection()
                cursor = conn.cursor()
                
                db.create_profile_table("position_mast")



                # Delete old records
                db.clear_profile_table("position_mast")

                 


                # Insert each net position
                net_positions = data.get('data', {}).get('net', []) if isinstance(data, dict) else []
                for pos in net_positions:
                    cursor.execute(
                        """
                        INSERT INTO position_mast (
                            tradingsymbol, exchange, instrument_token, product, quantity, overnight_quantity, multiplier, average_price, close_price, last_price, value, pnl, m2m, unrealised, realised, buy_quantity, buy_price, buy_value, buy_m2m, sell_quantity, sell_price, sell_value, sell_m2m, day_buy_quantity, day_buy_price, day_buy_value ,day_sell_quantity, day_sell_price, day_sell_value
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            pos.get('tradingsymbol'),
                            pos.get('exchange'),
                            pos.get('instrument_token'),
                            pos.get('product'),
                            pos.get('quantity'),
                            pos.get('overnight_quantity'),
                            pos.get('multiplier'),
                            pos.get('average_price'),
                            pos.get('close_price'),
                            pos.get('last_price'),
                            pos.get('value'),
                            pos.get('pnl'),
                            pos.get('m2m'),
                            pos.get('unrealised'),
                            pos.get('realised'),
                            pos.get('buy_quantity'),
                            pos.get('buy_price'),
                            pos.get('buy_value'),
                            pos.get('buy_m2m'),
                            pos.get('sell_quantity'),
                            pos.get('sell_price'),
                            pos.get('sell_value'),
                            pos.get('sell_m2m'),
                            pos.get('day_buy_quantity'),
                            pos.get('day_buy_price'),
                            pos.get('day_buy_value'),
                            pos.get('day_sell_quantity'),
                            pos.get('day_sell_price'),
                            pos.get('day_sell_value')
                        )
                    )
                conn.commit()
                cursor.close()
                conn.close()
                print("Position data inserted into position_mast table.")
                return data
            else:
                print("Error Response:", response.text)
        except requests.RequestException as e:
            print("Request failed:", str(e))




# Example usage:
# handler = UserHandler()
# handler.get_fund_summary()
# handler.get_portfolio()
