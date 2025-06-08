import os
import json
import requests
from dotenv import load_dotenv

from model.token_handler import TokenHandler
# from model.database_handler import DatabaseHandler
# Load environment variables from .env file
load_dotenv()

token_handler = TokenHandler()

class OptionHandler:
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


    def get_option_chain(self):
        """Perform GET request to get option chain and pretty print the output."""
        self.load_access_token_from_file()
        headers = self.get_headers()
        if not headers:
            return
        url = 'https://api.mstock.trade/openapi/typea/getoptionchainmaster/2'

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


