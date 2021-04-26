import requests
import json


data = {
 "loginId": "demouser@5daerosafe.com",
 "password": "demodemo"
}

response = requests.post('https://api.5daerosafe.finot.cloud/auth/jwt/login', data= data)
print(response)

