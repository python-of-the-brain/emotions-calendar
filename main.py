from requests import post

url = "https://api.monkeylearn.com/v3/classifiers/cl_pi3C7JiL/classify/"

headers = {
    'Authorization': 'Token 2412c64fd392b0ea440c6d16a6b346363162d2f1',
    'Content-Type': 'application/json',
}

body = {
    'data': ['I am so sad....']
}

response = post(url, headers=headers, json=body)

print(response.json())
