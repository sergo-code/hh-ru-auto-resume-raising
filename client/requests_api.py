import requests
from dotenv import load_dotenv
import json


load_dotenv()

url = 'http://127.0.0.1:8000/auth/sign-up/'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}
data = {
  "email": "first2@exaple.com",
  "username": "api_check2",
  "password": "123"
}

sign_up = requests.post(url, headers=headers, data=json.dumps(data))
print(sign_up.status_code)
print(sign_up.text)
token_jwt = json.loads(sign_up.text)['access_token']
url = 'http://127.0.0.1:8000/auth/user/'
headers = {
    'accept': 'application/json',
    'Authorization': f'Bearer {token_jwt}'
}
operations = requests.get(url, headers=headers)
print(operations.status_code)
print(operations.text)
url = 'http://127.0.0.1:8000/auth/operations/'
operations = requests.get(url, headers=headers)
print(operations.status_code)
print(operations.text)