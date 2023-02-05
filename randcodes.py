import requests
import json

api_key="Token e82c490f44603ed8428092e84ac62198248b68c6"
url = "http://localhost:8000/api/income/"


headers= {
"Authorization": api_key
}

data = {
    "username":"sidney",
    "password":'pass'
}
param={
"description":"none",
"source":"freelance",
"amount":90000
}

response = requests.request("GET", url, data=param, headers=headers)

status_code = response.status_code
result = response.text
result=json.loads(result)
print(result)
