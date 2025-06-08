import http.client
import json

conn = http.client.HTTPSConnection('api.mstock.trade')  # HTTPS instead of HTTP

headers = {
    'X-Mirae-Version': '1',
    'X-PrivateKey': 'KDOgbgg3H9D3P2aZ2BzkJJ9ZSMxihnrPXzQAvrEafdk@',
    'Content-Type': 'application/json',
    'X-ClientCode': '9845299953',

}

json_data = {
    'refreshToken': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVU0VSTkFNRSI6Ik1BMzA2NTEyNSIsIkFQSVRZUEUiOiJUWVBFQiIsIm5iZiI6MTc0NzcwNDUyOSwiZXhwIjoxNzQ3NzA0ODI5LCJpYXQiOjE3NDc3MDQ1Mjl9.-CiPdrH3A-GVkKIYcYt2vdr3GjwKXZxF0MZ5B4CY22M',
    'otp': '618',
}

conn.request(
    'POST',
    '/openapi/typeb/session/token',
    body=json.dumps(json_data),
    headers=headers
)

response = conn.getresponse()
data = response.read()

print("Status:", response.status)
print("Response:", data.decode())
