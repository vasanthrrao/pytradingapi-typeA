import http.client
import json

conn = http.client.HTTPSConnection('api.mstock.trade')
headers = {
    'X-Mirae-Version': '1',
    'Content-Type': 'application/json',
}
json_data = {
    'clientcode': '9845299953',
    'password': 'Pury',
    'totp': '',
    'state': '',
}
conn.request(
    'POST',
    '/openapi/typeb/connect/login',
    json.dumps(json_data),
    # '{\n    "clientcode": "XXXXX",\n    "password": "YYYYY",\n    "totp": "",\n    "state": ""\n    }',
    headers
)
response = conn.getresponse()
data = response.read()
print(response.status)
print(response.reason)
print(data.decode('utf-8'))




