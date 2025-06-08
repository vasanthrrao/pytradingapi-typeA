import os
import json
import requests
from dotenv import load_dotenv
from model.token_handler import TokenHandler

# Load environment variables from .env file
load_dotenv()
token_handler = TokenHandler()

class BasketHandler:
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

    def create_data(self,name=None, description=None):
        """Construct data for the API call."""
        return {
            'BaskName': name or 'BasketTest-1',
            'BaskDesc': description or 'Basket Description'
        }
    def rename_data(self,name=None, basket_id=None):
        """Construct data for the API call."""
        return {
            'BaskName': name or 'BasketTest-1',
            'BasketId': basket_id or '1234567890'
        }
    def delete_data(self,basket_id=None):
        """Construct data for the API call."""
        return {
            'BasketId': basket_id or '1234567890'
        }
    def calculate_data(self,name=None, basket_id=None,script_code=None):
        """Construct data for the API call."""
        return {
                'include_exist_pos': '0',
                'ord_product': 'C',
                'disc_qty': '0',
                'segment': 'E',
                'trigger_price': '0',
                'scriptcode': script_code or '11915',
                'ord_type': 'LMT',
                'basket_name': name or 'BasketTest-1',
                'operation': 'I',
                'order_validity': 'DAY',
                'order_qty': '1',
                'script_stat': 'A',
                'buy_sell_indi': 'B',
                'basket_priority': '1',
                'order_price': '19.02',
                'basket_id': basket_id or '1234567890',
                'exch_id': 'NSE'
        }
   
    def create_basket(self):
        """Perform POST request to create a basket."""
        self.load_access_token_from_file()
        headers = self.get_headers()
        if not headers:
            return

        url = 'https://api.mstock.trade/openapi/typea/CreateBasket'

        try:
            response = requests.post(url, headers=headers, data=self.create_data())
            print("Status Code:", response.status_code)
            if response.status_code == 200:
                formatted = json.dumps(response.json(), indent=4)
                print("Response JSON:\n", formatted)
                return response.json()
            else:
                print("Error Response:", response.text)
        except requests.RequestException as e:
            print("Request failed:", str(e))

    def rename_basket(self):
        """Perform POST request to create a basket."""
        self.load_access_token_from_file()
        headers = self.get_headers()
        if not headers:
            return

        url = 'https://api.mstock.trade/openapi/typea/RenameBasket'

        try:
            response = requests.post(url, headers=headers, data=self.rename_data())
            print("Status Code:", response.status_code)
            if response.status_code == 200:
                formatted = json.dumps(response.json(), indent=4)
                print("Response JSON:\n", formatted)
                return response.json()
            else:
                print("Error Response:", response.text)
        except requests.RequestException as e:
            print("Request failed:", str(e))

    def delete_basket(self):
        """Perform POST request to delete a basket."""
        self.load_access_token_from_file()
        headers = self.get_headers()
        if not headers:
            return

        url = 'https://api.mstock.trade/openapi/typea/DeleteBasket'

        try:
            response = requests.post(url, headers=headers, data=self.delete_data())
            print("Status Code:", response.status_code)
            if response.status_code == 200:
                formatted = json.dumps(response.json(), indent=4)
                print("Response JSON:\n", formatted)
                return response.json()
            else:
                print("Error Response:", response.text)
        except requests.RequestException as e:
            print("Request failed:", str(e))


    def fetch_basket(self):
        """Perform POST request to create a basket."""
        self.load_access_token_from_file()
        headers = self.get_headers()
        if not headers:
            return

        url = 'https://api.mstock.trade/openapi/typea/FetchBasket'

        try:
            response = requests.post(url, headers=headers)
            print("Status Code:", response.status_code)
            if response.status_code == 200:
                formatted = json.dumps(response.json(), indent=4)
                print("Response JSON:\n", formatted)
                return response.json()
            else:
                print("Error Response:", response.text)
        except requests.RequestException as e:
            print("Request failed:", str(e))
     def create_basket(self):
        """Perform POST request to create a basket."""
        self.load_access_token_from_file()
        headers = self.get_headers()
        if not headers:
            return

        url = 'https://api.mstock.trade/openapi/typea/CreateBasket'

        try:
            response = requests.post(url, headers=headers, data=self.create_data())
            print("Status Code:", response.status_code)
            if response.status_code == 200:
                formatted = json.dumps(response.json(), indent=4)
                print("Response JSON:\n", formatted)
                return response.json()
            else:
                print("Error Response:", response.text)
        except requests.RequestException as e:
            print("Request failed:", str(e))

    def calculate_basket(self):
        """Perform POST request to create a basket."""
        self.load_access_token_from_file()
        headers = self.get_headers()
        if not headers:
            return

        url = 'https://api.mstock.trade/openapi/typea/CalculateBasket'

        try:
            response = requests.post(url, headers=headers, data=self.calculate_data())
            print("Status Code:", response.status_code)
            if response.status_code == 200:
                formatted = json.dumps(response.json(), indent=4)
                print("Response JSON:\n", formatted)
                return response.json()
            else:
                print("Error Response:", response.text)
        except requests.RequestException as e:
            print("Request failed:", str(e))

# Example usage:
# handler = UserHandler()
# handler.get_fund_summary()
# handler.get_portfolio()
