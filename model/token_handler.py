import http.client
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class TokenHandler:
    def __init__(self):
        self.vUSERNAME = os.getenv("vUSERNAME")
        self.API_KEY = os.getenv("API_KEY")
        self.Access_token = None  # Initialize Access_token

    def getHeaders(self):
        return {
            'X-Mirae-Version': '1',
            'X-PrivateKey': self.API_KEY,
            'Content-Type': 'application/json',
            'X-ClientCode': self.vUSERNAME,
        }

    def get_json_data(self, otp_code, refresh_token):
        return {
            'refreshToken': refresh_token,
            'otp': otp_code,
        }

    def get_response(self, otp_code, refresh_token):
        conn = http.client.HTTPSConnection('api.mstock.trade')
        json_data = json.dumps(self.get_json_data(otp_code, refresh_token))
        headers = self.getHeaders()

        conn.request(
            'POST',
            '/openapi/typeb/session/token',
            body=json_data,
            headers=headers
        )

        response = conn.getresponse()
        data = response.read().decode()
        print("Status:", response.status)
       
        try:
            response_json = json.loads(data)
            if response_json.get("status") is True and "data" in response_json:
                tokens = {
                    "jwtToken": response_json["data"].get("jwtToken"),
                    "refreshToken": response_json["data"].get("refreshToken"),
                    "feedToken": response_json["data"].get("feedToken")
                }

                # Save tokens to tokens.txt
                with open("tokens.txt", "w") as f:
                    for key, value in tokens.items():
                        f.write(f"{key}: {value}\n")

                print("Tokens saved to tokens.txt")
                return tokens
            else:
                print("Error:", response_json.get("message"))
                return None
        except json.JSONDecodeError:
            print("Failed to decode response JSON.")
            return None

    def load_access_token_from_file(self, filepath="tokens.txt"):
        """Read jwtToken from tokens.txt and assign to self.Access_token."""
        if not os.path.exists(filepath):
            print(f"File {filepath} does not exist.")
            return None
        with open(filepath, "r") as f:
            for line in f:
                if line.strip().startswith("jwtToken:"):
                    token = line.split(":", 1)[1].strip()
                    self.Access_token = token
                    return token
        print("jwtToken not found in tokens.txt.")
        return None

# Example usage:
# handler = TokenHandler()
# handler.get_response("123456", "<your_refresh_token>")
