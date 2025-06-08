try:
    import requests
except (ModuleNotFoundError, ImportError):
    print("requests module not found")
    os.system(f"{sys.executable} -m pip install -U requests")
finally:
    import requests

try:
    import pandas as pd
except (ModuleNotFoundError, ImportError):
    print("pandas module not found")
    os.system(f"{sys.executable} -m pip install -U pandas")
finally:
    import pandas as pd
	
try:
    from bs4 import BeautifulSoup
except (ModuleNotFoundError, ImportError):
    print("BeautifulSoup module not found")
    os.system(f"{sys.executable} -m pip install -U beautifulsoup4")
finally:
    from bs4 import BeautifulSoup
	
	
Charting_Link = "https://chartink.com/screener/"
Charting_url = 'https://chartink.com/screener/process'

#You need to copy paste condition in below mentioned Condition variable

#Condition = "( {57960} ( [0] 15 minute close > [-1] 15 minute max ( 20 , [0] 15 minute close ) and [0] 15 minute volume > [0] 15 minute sma ( volume,20 ) ) ) "


Condition = "( {33489} ( latest volume > latest sma( latest volume , 10 ) * 2 ) )" 


def GetDataFromChartink(payload):
    payload = {'scan_clause': payload}
    
    with requests.Session() as s:
        r = s.get(Charting_Link)
        soup = BeautifulSoup(r.text, "html.parser")
        csrf = soup.select_one("[name='csrf-token']")['content']
        s.headers['x-csrf-token'] = csrf
        r = s.post(Charting_url, data=payload)

        df = pd.DataFrame()
        data_list = []
        for item in r.json()['data']:
            if len(item) > 0:
                data_list.append(item)
        df = pd.DataFrame(data_list)
    return df

data = GetDataFromChartink(Condition)

data = data.sort_values(by='per_chg', ascending=False)

print(data)

data.to_csv("Chartink_result.csv")