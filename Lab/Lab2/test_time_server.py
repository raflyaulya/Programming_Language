import requests

# Test GET /
print()
response = requests.get('http://127.0.0.1:8000/')
print(response.text)
print()

# Test GET /<tz name>
response1 = requests.get('http://127.0.0.1:8000/Europe/London')
response2 = requests.get('http://127.0.0.1:8000/Asia/Singapore')
response3 = requests.get('http://127.0.0.1:8000/Africa/Cairo')
print(response1.text)
print(response2.text)
print(response3.text)
print()

# Test POST /api/v1/time
# please input your continent & city
continent1 = input('1st continent: ') # America
city1 = input('1st city: ') # New_york
continent2 = input('2nd continent: ') # Asia
city2 = input('2nd city: ') # Jakarta
continent3 = input('3rd continent: ') # Europe
city3 = input('3rd city: ') # Moscow
print()

response1 = requests.post('http://127.0.0.1:8000/api/v1/time', json={'tz': f'{continent1}/{city1}'})
response2 = requests.post('http://127.0.0.1:8000/api/v1/time', json={'tz': f'{continent2}/{city2}'})
response3 = requests.post('http://127.0.0.1:8000/api/v1/time', json={'tz': f'{continent3}/{city3}'})
print(f'time in {continent1}/{city1}',response1.json())
print(f'time in {continent2}/{city2}',response2.json())
print(f'time in {continent3}/{city3}',response3.json())
print()
