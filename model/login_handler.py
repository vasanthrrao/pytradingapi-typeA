import http.client
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class LoginHandler:
    def __init__(self):
        self.vUSERNAME = os.getenv("vUSERNAME")
        self.vPASSWORD = os.getenv("vPASSWORD")

    def getHeaders(self):
        return {
            'X-Mirae-Version': '1',
            'Content-Type': 'application/json',
        }

    def get_json_data(self):
        return {
            'clientcode': self.vUSERNAME,
            'password': self.vPASSWORD,
            'totp': '',
            'state': '',
        }

    def get_response(self):
        conn = http.client.HTTPSConnection('api.mstock.trade')
        json_data = json.dumps(self.get_json_data())
        conn.request(
            'POST',
            '/openapi/typeb/connect/login',
            json_data,
            self.getHeaders()
        )
        response = conn.getresponse()
        data = response.read().decode("utf-8")

        try:
            response_json = json.loads(data)
            if response_json.get("status") is True and "data" in response_json:
                refresh_token = response_json["data"].get("refreshToken")
                return refresh_token
            else:
                return f"Login failed or OTP required: {response_json.get('message')}"
        except json.JSONDecodeError:
            return "Invalid JSON response"