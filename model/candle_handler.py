import os
import json
import requests
from dotenv import load_dotenv
from model.token_handler import TokenHandler
token_handler = TokenHandler()

# Load environment variables from .env file
load_dotenv()

class CandleHandler:
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




  

# Example usage:
# handler = UserHandler()
# handler.get_fund_summary()
# handler.get_portfolio()
