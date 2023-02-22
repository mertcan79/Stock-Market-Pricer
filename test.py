import requests

url = "http://localhost:8000/"

payload1 = {"symbol": "AAPL", "currency":"EUR", "dates": "10.01.2023-10.02.2023"}
payload2 = {"symbol": "AAPL", "currency":"EUR", "dates": "10/01/2023-10/02/2023"}
payload3 = {"symbol": "AAPL", "currency":"EUR", "dates": "January 10, 2023-February 10, 2023"}
payload4 = {"symbol": "AAPL", "currency":"EUR", "dates": None}

response1 = requests.get(url, json=payload1)
response2 = requests.get(url, json=payload2)
response3 = requests.get(url, json=payload3)
response4 = requests.get(url, json=payload4)

print("API call with %d.%m.%Y date format")
print(response1.text)

print("\n API call with %d/%m/%Y date format")
print("-"*30)
print(response2.text)

print("\n API call with %B %d, %Y date format")
print("-"*30)
print(response3.text)

print("\n API call with missing dates")
print("-"*30)
print(response4.text)
print("-"*30)
