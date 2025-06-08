from model.email_handler import EmailHandler
from model.login_handler import LoginHandler
from model.token_handler import TokenHandler
from time import sleep



email_handler = EmailHandler()
login_handler = LoginHandler()
token_handler = TokenHandler()


refresh_token = login_handler.get_response()
#print(f"Login Response : {response}")

sleep(15)  # Wait for 5 seconds to ensure the email is received
otp_code = email_handler.fetch_code_emails()
#print(f"OTP Code : {otp_code}")

token_handler.get_response(otp_code, refresh_token)