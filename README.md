## TradingAPI SDK - Python Client for accessing TradingAPI and Streaming Market Data

### Description
TradingAPI is a complete SDK that allows you to build a trading and investment platform which includes executing orders in real time, streaming live trade and order data (Using Websockets) and more. 

### Installation


> [!IMPORTANT]
> You can install the python client with below command. For requirements.txt file [refer here](https://github.com/MiraeAsset-mStock/pytradingapi-typeA/blob/main/requirements.txt).

```
pip install -r requirements.txt

pip install --upgrade mStock-TradingApi-A
```

It is recommended to update 'pip' and `setuptools` to the latest version if you are facing any issues during installation

```
pip install -U pip setuptools
```

>[!NOTE]
>The package can be used with the name **tradingapi_a**

### API Usage

```python
import logging
from tradingapi_a.mconnect import *

logging.basicConfig(level=logging.DEBUG)

#Object for MConnect API
mconnect_obj=MConnect()

#Login
login_response=mconnect_obj.login("<user_id>","<password>")

#Generate access token by calling generate session
gen_response=mconnect_obj.generate_session("<API_Key>","<request_token_here>","<checksum>")

#Place Order
try:
    porder_resp=mconnect_obj.place_order(_tradingsymbol="SBICARD",_exchange="NSE",_transaction_type="BUY",_order_type="MARKET",_quantity="10",_product="CNC",_validity="DAY",_price="0",_trigger_price="0")
    
    logging.info("Order placed. ID is: {}".format(porder_resp["data"]["order_id"]))

except Exception as e:
    logging.info("Order placement failed: {}".format(e.message))

#Fetch all orders
mconnect_obj.get_order_book()

#Fetch all holdings
mconnect_obj.get_holdings()

#Get Net position for logged in user
mconnect_obj.get_net_position()

#Cancel All orders
mconnect_obj.cancel_all()

#Get fund Summary
mconnect_obj.get_fund_summary()

```

### Websocket Usage
```python
from tradingapi_a.mticker import *
import logging

logging.basicConfig(level=logging.DEBUG)

#Testing Web Socket or MTicker
m_ticker=MTicker("<API_KEY>","<ACCESS_TOKEN>","<WEB_SOCKET_URL>")


#Defining Callbacks
def on_ticks(ws, ticks):
    # Callback to receive ticks.
    logging.info("Ticks: {}".format(ticks))

def on_order_update(ws,data):
    #Callback to receive Order Updates
    logging.info("On Order Updates Packet received : {}".format(data))

def on_trade_update(ws,data):
    #Callback to receive Trade Updates
    logging.info("On Trade Updates Packet received : {}".format(data))

def on_connect(ws, response):
    # Callback on successful connect.
    m_ticker.send_login_after_connect()
    # Subscribe to a list of instrument_tokens .
    ws.subscribe([5633])
    # Set tick in `full` mode.
    ws.set_mode(m_ticker.MODE_FULL, [5633])

def on_close(ws, code, reason):
    # On connection close stop the event loop.
    # Reconnection will not happen after executing `ws.stop()`
    ws.stop()

# Assign the callbacks.
m_ticker.on_ticks = on_ticks
m_ticker.on_connect = on_connect
m_ticker.on_close = on_close
m_ticker.on_order_update=on_order_update
m_ticker.on_trade_update=on_trade_update

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
m_ticker.connect()

logging.info('Now Closing Web socket connection')

m_ticker.close()

logging.info('Testing complete')


```

**Quick Start Guide: Running Your Script in VS Code**  
Follow these steps to set up and run your script smoothly.
 
---
 
### 1. 🗂️ Open the Project Folder
- Launch **Visual Studio Code**.
- Click on **File > Open Folder**.
- Select your project directory (e.g., `pytradingapi-typeA-1`) and click **Open**.
 
---
 
### 2. 💻 Open a New Terminal
- Go to the top menu and click **Terminal > New Terminal**.
- This will open a terminal window at the bottom of VS Code.
 
---
 
### 3. 📁 Navigate to the Script Directory
In the terminal, run:
```bash
cd examples/All_Api
 
---
 
4. 🔑 Update Your Credentials
Open the file named 'Login.py' (this file is located inside the 'examples/All_Api' directory).
Locate the lines where the 'user_id' and 'password' variables are defined.
Replace the placeholder values with your actual trading account credentials. For example:
user_id = "your_actual_user_id"
password = "your_actual_password"
5. 🗝️ Set Your API Key
Open the file named 'config.py' (this file is located within the 'tradingapi_a' directory).
Find the line that defines the 'API_KEY' variable.
Update the placeholder value with your legitimate API key. For example:
API_KEY = "your_actual_api_key"
6. ▶️ Run Any Example Script
You have two primary methods to run your scripts:
- Using the command line: # In the integrated terminal, execute the following command to run a script:
Bash
 
python Login.py
You can replace 'Login.py' with the filename of any other script you wish to execute from the 'examples/All_Api' directory, for instance:
python Order_Placement.py
- Using the Run icon:
 Using the Run icon:
 Open any Python file (.py) within the VS Code editor that is located inside the 'examples/All_Api' folder.
 This could be 'Login.py', 'Order_Placement.py', or any other script you wish to run from that directory.
 Once the file is open, click the 'Run' icon (typically a green triangle) located in the top-right corner of the VS Code interface to execute the currently displayed script.
Tip:
It is crucial to always update your credentials in 'Login.py' and your API key in 'config.py' before running any script for the very first time, and whenever these credentials change.

### Running Unit Tests

This requires having pytest library pre installed. You can install the same via pip:

``` pip install pytest ```

Navigate to the ```unit``` directory and run the ```connect_test.py``` file using pytest

```
cd unit
pytest connect_test.py
```

### Support
For issues, please open an issue on GitHub.

### Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a new branch (feature-xyz)
3. Commit your changes
4. Push the branch and create a pull request
