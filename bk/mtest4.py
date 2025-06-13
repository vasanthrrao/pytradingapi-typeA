from tradingapi_a.mticker import *
from tradingapi_a.mconnect import *
from tradingapi_a import __config__

from model.email_handler import EmailHandler

email_handler = EmailHandler()



mconnect_obj=MConnect()
#Login Via Tasc API, Receive Token in response
login_response=mconnect_obj.login("9845299953","Pury")
print(f"Request : Login. Response received : {login_response.json()}")




otp_code=email_handler.fetch_code_emails()
print(f"OTP Code : {otp_code}")




#Generate access token by calling generate session
gen_response=mconnect_obj.generate_session(__config__.API_KEY,otp_code,"W")
print(f"Request : Generate Session. Response received : {gen_response.json()}")     
#Getting API Key
api_key=__config__.API_KEY
#Getting Access token
access_token=mconnect_obj.access_token  
