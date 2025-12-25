import requests
n=int(input())
api_root="https://2factor.in/API/V1/"
api_key="a0780a7e-aa8b-11ef-8b17-0200cd936042/"
type_otp="SMS/"
cuntry_code="+91"
number="9554692731/"
otp="102020"
url=api_root+api_key+type_otp+cuntry_code+number+otp

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

#
