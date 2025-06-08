import os,sys
import csv
import logging


parent_dir=os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from tradingapi_a.mconnect import *
from tradingapi_a import __config__

# Create and configure logger
logging.basicConfig(filename="miraesdk_typeA.log",
                    format='%(asctime)s %(message)s',
                    filemode='a',)

# Creating an object
test_logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
test_logger.setLevel(logging.INFO)


#Testing NConnect API
#Object for NConnect API
mconnect_obj=MConnect()

#Login Via Tasc API, Receive Token in response
login_response=mconnect_obj.login("RAHUL","Macm@123")
test_logger.info(f"Request : Login. Response received : {login_response.json()}")

#Generate access token by calling generate session
gen_response=mconnect_obj.generate_session(__config__.API_KEY,"123","W")
test_logger.info(f"Request : Generate Session. Response received : {gen_response.json()}")


#Getting API Key
api_key=__config__.API_KEY

#Getting Access token
access_token=mconnect_obj.access_token

#Test Order Placement, Modification etc

#Place Order
porder_resp=mconnect_obj.place_order("SBICARD","NSE","BUY","MARKET","10","CNC","DAY","0","0")
test_logger.info(f"Request : Place Order. Response received : {porder_resp.json()}")

#Modify Order
modify_resp=mconnect_obj.modify_order("1181250203103","SL","5","723","DAY","720","0")
test_logger.info(f"Request : Modify Order. Response received : {modify_resp.json()}")

#Cancel Order by Order ID
cancel_resp=mconnect_obj.cancel_order("1181250205102")
test_logger.info(f"Request : Cancel Order. Response received : {cancel_resp}")

#Get Order book for logged in user
get_ord_bk=mconnect_obj.get_order_book()
test_logger.info(f"Request : Get Order Book. Response received : {get_ord_bk.json()}")

#Get Net position for logged in user
get_net_pos=mconnect_obj.get_net_position()
test_logger.info(f"Request : Get Net Positions. Response received : {get_net_pos.json()}")

#Calculate order MArgin given the details
calc_ord_margin=mconnect_obj.calculate_order_margin("NSE","INFY","BUY","regular","CNC","MARKET","1","0","0")
test_logger.info(f"Request : Calculate Order Margin. Response received : {calc_ord_margin.json()}")

#CANCEl All orders
cancel_all=mconnect_obj.cancel_all()
test_logger.info(f"Request : Cancel All. Response received : {cancel_all.json()}")

#Order Details
order_det=mconnect_obj.get_order_details("1151250205102","E")
test_logger.info(f"Request : Order Details. Response received : {order_det.json()}")

#Get Holdings
holdings=mconnect_obj.get_holdings()
test_logger.info(f"Request : Holdings. Response received : {holdings.json()}")

#Get Historical Chart
historical_chart=mconnect_obj.get_historical_chart("11536","60minute","2025-01-05","2025-01-10") 
test_logger.info(f"Request : Historical Chart. Response received : {historical_chart.json()}")

#Trade History
trade_history=mconnect_obj.get_trade_history("2025-01-05","2025-01-10")
test_logger.info(f"Request : Trade History. Response received : {trade_history.json()}")

#OHLC
get_ohlc=mconnect_obj.get_ohlc(["NSE:ACC","BSE:ACC"])
test_logger.info(f"Request : Fetch Market Data OHLC. Response received : {get_ohlc.json()}")

#LTP
get_ltp=mconnect_obj.get_ltp(["NSE:ACC","BSE:ACC"])
test_logger.info(f"Request : Fetch Market Data LTP. Response received : {get_ltp.json()}")

#Get Instrument Scrip Master
get_instruments=mconnect_obj.get_instruments()
split_data=get_instruments.text.split("\n")
data=[row.strip().split(",") for row in split_data]
#Writing response into a csv file for reference
#Open the file in write mode
with open('instrument_scrip_master.csv', mode='w') as file:
    # Create a csv.writer object
    writer = csv.writer(file,delimiter=",")
    # Write data to the CSV file
    for row in data:
        writer.writerow(row)

test_logger.info(f"Request : Fetch Instrument Scrip Master. Response received and stored in a csv file.")


#Get fund Summary
get_fund_summary=mconnect_obj.get_fund_summary()
test_logger.info(f"Request : Fetch Fund Summary. Response received : {get_fund_summary.json()}")

# #Convert Position
conv_position=mconnect_obj.convert_position("TCS","NSE","BUY","DAY","3","CNC","MIS")
test_logger.info(f"Request : Position Conversion. Response received : {conv_position.json()}")














