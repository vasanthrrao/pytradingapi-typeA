#You need to copy paste condition in below mentioned Condition variable

Condition = "( {57960} ( latest close < latest open and 1 day ago close < 1 day ago open and 2 days ago close < 2 days ago open ) )" 
 

sleeptime = 5

from time import sleep
import os
import warnings
import sys
warnings.filterwarnings("ignore")

try:
    import xlwings as xw
except (ModuleNotFoundError, ImportError):
    print("xlwings module not found")
    os.system(f"{sys.executable} -m pip install -U xlwings")
finally:
    import xlwings as xw
    
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


def GetDataFromChartink(payload):
    payload = {'scan_clause': payload}
    
    with requests.Session() as s:
        r = s.get(Charting_Link)
        soup = BeautifulSoup(r.text, "html.parser")
        csrf = soup.select_one("[name='csrf-token']")['content']
        s.headers['x-csrf-token'] = csrf
        r = s.post(Charting_url, data=payload)

        df = pd.DataFrame()
        for item in r.json()['data']:
            
            if len(item) > 0:
                df = pd.concat([df, pd.DataFrame.from_dict(item,orient='index').T],ignore_index = True)
            
    return df


try:
    if not os.path.exists('Chartink_Result.xlsm'):
        wb = xw.Book()
        wb.save('Chartink_Result.xlsm')
        wb.close()

    wb = xw.Book('Chartink_Result.xlsm')
    try:
        result = wb.sheets('Chartink_Result')
    except Exception as e:
        wb.sheets.add('Chartink_Result')
        result = wb.sheets('Chartink_Result')
except Exception as e:
    pass
    
  
    data = GetDataFromChartink(Condition)

    if len(data) > 0:
        data = data.sort_values(by='per_chg',ascending=False)

        print(f"\n\n{data}")
        
        try:
            result.range('a:h').value = None
            result.range('a1').options(index=False).value = data
        except Exception as e:
            pass
    sleep(sleeptime)
             